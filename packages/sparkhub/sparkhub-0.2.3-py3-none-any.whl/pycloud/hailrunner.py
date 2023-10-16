
#!/usr/bin/env python

import os
import sys
import re
import subprocess
import shutil
import tempfile
import zipfile
import yaml
from .cloud_utils import execute
from .gcloud import hail_paths

from IPython.core import magic_arguments
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
from IPython.utils.io import capture_output

import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

from .slackconnector import SlackConnector

class HailRunner(object):
    def __init__(self, outdir="", input_file="", localdata="",
                 hail_jar_path="", pyhail_zip="",
                 header="", other_script_paths="", str_format='%'):
        
        # Assigns outdir and script_path
        self.outdir = os.path.dirname(outdir)
        
        # Define version
        self.version = 'debug' if 'VERSION' not in os.environ else os.environ['VERSION']

        # Create outdir and basic .jobs file structure
        if not os.path.isdir(self.outdir) or not os.path.isdir(os.path.join(self.outdir, 'log', self.version)):
            os.makedirs(os.path.join(self.outdir, "log", self.version) + '/')
        self.logdir = os.path.join(self.outdir, 'log', self.version)

        if not os.path.isdir(os.path.join(self.outdir, 'script', self.version)):
            os.makedirs(os.path.join(self.outdir, "script", self.version) + '/')
        self.scriptdir = os.path.join(self.outdir, 'script', self.version)

        # add current links
        if os.path.isdir(os.path.join(self.outdir, "current")):
            shutil.rmtree(os.path.join(self.outdir, "current"))
        os.makedirs(os.path.join(self.outdir, "current"))
        os.symlink(self.logdir, os.path.join(self.outdir, 'current', 'log'), target_is_directory=True)
        os.symlink(self.scriptdir, os.path.join(self.outdir, 'current', 'script'), target_is_directory=True)

        # add local /data folder links
        if localdata != '':
            if os.path.islink(os.path.join(self.outdir, 'data')):
                os.remove('data')
            os.symlink(localdata, os.path.join(self.outdir, 'data'), target_is_directory=True)

        # 0-based counter for submits made in script. Used for naming and tracking. 
        self.current_run = 0
        
        # 0-based counter that stores a particular run count for restoration later
        self._setr = []
        self._sig_popr = None
    
        # Initialize run-specific array attributes of PyRunner class
        self.current_job = []
    
        # Initialize Hail-related variables
        self.hail_jar_path = hail_jar_path
        self.hail_jar_base_name = os.path.basename(self.hail_jar_path)
        self.py_files = [ pyhail_zip ]
        if other_script_paths:
            if isinstance(other_script_paths, list):
                self.py_files.extend(other_script_paths)
            else:
                self.py_files.append(other_script_paths)
        self.py_files = ','.join(self.py_files)
        self.header = header
            
        # Read in inputfofn can be a list of files or read from a file 
        self.fofn = []
        if isinstance(input_file, str):
            self.fofn.append(input_file)
        else:
            self.fofn.append('')

        # Define string format rule
        self.str_format = '{' if str_format == '{' else '%'

        # set default as non-local mode
        self.local = False

        # init SlackConnector
        self.sc = SlackConnector('HailRunner')
        
    def chain_submit(self, name, command, outfile, *args):
        """ add_batch adds a batch of jobs to job_array in the form of method, output filename, input filename
        and method arguments. It maps 1-1 from previous fofn. All new output filenames are added to fofn[done_run+1] """
        # Initialize a new set of output fofn (if it does not yet exist)
        if len(self.fofn) == self.current_run + 1:
            self.fofn.append([])
        r = self.current_run if not self._sig_popr else self._setr[-1] # new code for use with setr
        self.current_job = [ command, outfile, self.fofn[r] ] + list(args)
        self.fofn[self.current_run + 1] = outfile
        self.submit(name)
        
    def submit_job(self, name, command, outfile, *args):
        # Initialize a new set of output fofn (if it does not yet exist)
        if len(self.fofn) == self.current_run + 1:
            self.fofn.append([])
        self.current_job = [ command, outfile ] + list(args)
        self.fofn[self.current_run + 1] = outfile 
        self.submit(name)
        
    def file_exists(self, path):
        return(os.path.exists(path))
    
    def submit(self, name):
        # Check if job completed
        if self.file_exists(self.current_job[1]):
            logger.info('Run {} successfully completed in an earlier attempt.'.format(self.current_run + 1))
            self.done()
        # Check if this step is marked "done" in log folder
        elif os.path.isfile(os.path.join(self.logdir, 'run{0}.done'.format(self.current_run + 1))):
            logger.info('Skipping checks for run {0}...'.format(self.current_run + 1))     
        # Submit Spark command
        else:
            # Specify script path
            script_path = os.path.join(
                self.scriptdir,
                "run{}.{}.py".format(self.current_run + 1, name)
            )

            # Copy Python script over if it is a file
            if os.path.isfile(self.current_job[0]):
                shutil.copy2(self.current_job[0], script_path)
            # Write command string as Python script
            else:
                with open(script_path, 'w') as f:
                    f.write(self.header)
                    input_list = self.current_job[2:] + [ self.current_job[1] ]
                    if self.str_format == '%':
                        f.write(self.current_job[0] % tuple(input_list))
                    else:
                        f.write(self.current_job[0].format(*input_list))
            
            # Specify log file
            log_path = os.path.join(self.logdir, "run{}.{}.o".format(self.current_run + 1, name))
            
            try:
                self.spark_submit(script_path, log_path)
            except Exception as e:
                self.sc.notify("run{}.{} has failed.".format(self.current_run + 1, name))
                sys.stderr.write(e)
                sys.exit(1)
            
            self.sc.notify("run{}.{} has finished successfully.".format(self.current_run + 1, name))
            self.done()

        self.current_run += 1
        if self._sig_popr:
            self._sig_popr = False
            self._setr.pop()

        # reset to non-local mode
        self.local = False
    
    def add_pyfile(self, path):
        self.py_files = self.py_files + ",%s" % path

    def quick_submit(self, command):
        temp_py = tempfile.mkstemp(suffix='.py')
        if not os.path.isfile(command):
            with open(temp_py[1], 'w') as f:
                f.write(self.header)
                f.write(command)
        else:
            shutil.copy2(command, temp_py[1])
        self.spark_submit(temp_py[1], False)
        if temp_py is not None:
            os.remove(temp_py[1])
        self.sc.notify("Quick submit has finished successfully.")
        # reset to non-local mode
        self.local = False
            
    # def spark_submit(self, script_path, log_path):
    #     py_files = process_pyfiles(py_files)
    #     cmd = [ 'spark-submit', script_path,
    #             '--files={}'.format(self.hail_jar_path),
    #             '--py-files={}'.format(self.py_files),
    #             '--properties=spark.driver.extraClassPath=./{0},spark.executor.extraClassPath=./{0}'.format(self.hail_jar_base_name),
    #             '--driver-log-levels', 'root=FATAL,is.hail=INFO' ]
    #     execute(cmd, logger = log_path, clean_spark_log = True)
    
    def done(self, abspath = False):
        with open(os.path.join(self.logdir, 'output.fofn'), 'w') as f:
            if abspath:
                fofn = [ os.path.abspath(filename) for filename in self.fofn ]
            else:
                fofn = self.fofn
            f.write('\n'.join(fofn)+'\n')

    def exit(self):
        sys.exit('Exiting script')

    def set_skip(self):
        f = open(os.path.join(self.outdir, 'run{0}.done'.format(self.current_run)), 'w')
        f.write('skip...')
        f.close()

    def reset(self):
        path = self.f
        runner.fofn = self.fofn[0:-1]
        self.current_run -= 1
        return(path)

    @property
    def r(self):
        return(self.current_run)

    @property
    def f(self):
        if len(self.fofn[self.current_run]) == 1:
            return(self.fofn[self.current_run][0])
        return(self.fofn[self.current_run])
    
    @property 
    def popr(self):
        self._sig_popr = True
        return(self._setr[-1])
    
    @property
    def popf(self):
        self._sig_popr = True
        if len(self.fofn[self._setr[-1]]) == 1:
            return(self.fofn[self._setr[-1]][0])
        return(self.fofn[self._setr[-1]])
    
    # should be setter, but it sort of behaves differently
    def pushr(self):
        self._setr.append(self.current_run)

    @property
    def past(self):
        paths = [ path.strip() for path in execute(['cat', os.path.join(self.logdir, 'output.fofn')], 
            return_out = True, silent = True) ]
        return(list(enumerate(paths)))

class HailRunnerGC(HailRunner):
    def __init__(self, instance, version=2, header=None, default_reference='GRCh37', other_files=None, tracker=False, str_format=None, **args):
        hail_jar, pyhail_zip = hail_paths(version = version)      
        header = header if header else get_hail_header(version = version, default_reference = default_reference)
        str_format = '{' if str_format == None and version == 1 else '%'
        super(HailRunnerGC, self).__init__(hail_jar_path = hail_jar, 
                                           pyhail_zip = pyhail_zip, 
                                           header = header, str_format = str_format, 
                                           **args) 
        self.instance = instance 

        if isinstance(other_files, list):
            self.other_files = other_files.join(',') 
        elif isinstance(other_files, str):
            self.other_files = other_files
        else:
            self.other_files = None

        if tracker and os.environ['TRACKER_PATH']:
            if self.other_files:
                self.other_files = f"{self.other_files},{os.environ['TRACKER_PATH']}"
            else:
                self.other_files = f"{os.environ['TRACKER_PATH']}"
            # tracker/db.json as copied to dataproc is in a special nested directory, but can be referred to directly as the current working directory
            self.header += "\nos.environ['TRACKER_PATH'] = 'db.json'\n\n"

    def file_exists(self, path):
        try:
            if re.search(r'\.ht$|\.mt$', path):
                path = os.path.join(path, '_SUCCESS')
            if execute(['gsutil', 'ls', path], return_out=True, silent=True):
                return(True)
        except:
            return(False)

    def spark_submit(self, script_path, log_path, skip_jar = True, add_py_file = None):
        cmd = [ 'gcloud', 'dataproc', 'jobs', 'submit', 'pyspark', script_path, '--cluster', self.instance ]
        
        # Add additional script files to load into working directory
        py_files = self.py_files.split(",")
        if add_py_file:
            if isinstance(add_py_file, list):
                py_files.extend(add_py_file)
            else:
                py_files.append(add_py_file)
        py_files = process_pyfiles(py_files)
        if skip_jar and len(py_files) > 1:
            cmd.extend([ '--py-files={}'.format(",".join(py_files[1:])) ])
        else:
            cmd.extend([ '--py-files={}'.format(",".join(py_files))
                #'--files={}'.format(self.hail_jar_path),
                #'--properties=spark.driver.extraClassPath=./{0},spark.executor.extraClassPath=./{0}'.format(self.hail_jar_base_name),
                #'--p', 'root=FATAL,is.hail=INFO' 
            ])
        if self.other_files:
            cmd.extend([ '--files', self.other_files ])
        # set to local mode here
        cmd = cmd if not self.local else [ 'python',  script_path ]
        execute(cmd, logger = log_path, clean_spark_log = True)
    
    def copy_log(self, target=None):
        if not target:
            target = self.logdir
        cmd = [ 'gcloud', 'compute', 'scp', f'{self.instance}-m:/home/hail/hailrunner.log', target ] #, '--zone', zone ]
        execute(cmd, silent=False)

def process_pyfiles(py_files):
    '''
    py_files is a list of Python files and zipped files.
    process_pyfiles zips all the Python files into a .zip file 
    that will be unpackaged in the PYTHONPATH of the dataproc cluster.
    '''
    return_list = []    
    temp_zip = tempfile.mkstemp(suffix = '.zip', prefix = 'pyfile_')[1]
    zf = zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED)
    for path in py_files:
        if path.endswith('.zip') or path.endswith('.egg'):
            return_list.append(path)
        if path.endswith('.py'):
            zf.write(path, arcname = os.path.basename(path))
        else:
            for root, _, pyfiles_walk in os.walk(path):
                for pyfile in pyfiles_walk:
                    if pyfile.endswith('.py'):
                        zf.write(os.path.join(root, pyfile),
                            os.path.relpath(os.path.join(root, pyfile), os.path.join(path, '..')))
    return_list.append(temp_zip)
    return(return_list)

def get_hail_header(version=2, default_reference='GRCh37', requester_pays=False, tmp_dir=None):
    config_str = [ 'min_block_size=0', f"default_reference='{default_reference}'", "log='/home/hail/hailrunner.log'" ]
    if requester_pays:
        config_str.append("spark_conf={'spark.hadoop.fs.gs.requester.pays.mode': 'AUTO'}")
    if tmp_dir:
        config_str.append(f"tmp_dir='{tmp_dir}'")
    config_str = ', '.join(config_str)
    if version == 1:
        return("""
from hail import *
from hail.expr import *
from hail.representation import *
hc = HailContext(log = "hail.log")

import os
import re
from pprint import pprint
from math import log, isnan

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
""")
    elif version == 2:
        return(
"""
import os
import re
import sys

import hail as hl
hl.init(%s)
from pprint import pprint

import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Default reference: {}'.format(hl.default_reference().name))
""" % config_str)

def get_hail_utils_header():
    return("""
import os
import re
import sys

import hail as hl
from pprint import pprint

import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
""")

def write_hail_utils_header(utils_file, lines_str):
    with open(utils_file, 'w') as f:
        f.write(get_hail_utils_header() + "\n" + lines_str + "\n")

# from IPython.display import Javascript
# Javascript(cwnb) os.path.abspath(notebookName) + './log'

cwnb = """
var kernel = Jupyter.notebook.kernel; 
var command = ["notebookPath = ",
               "'", window.document.body.dataset.notebookPath, "'" ].join('')
//alert(command)
kernel.execute(command)
var command = ["notebookName = ",
               "'", window.document.body.dataset.notebookName, "'" ].join('')
//alert(command)
kernel.execute(command)
"""

# http://mlexplained.com/2017/12/28/creating-custom-magic-commands-in-jupyter/
# https: // github.com/ipython/ipython/issues/11826
@magics_class
class RunnerMagics(Magics):  
    def __init__(self, shell, runner):
        super(RunnerMagics, self).__init__(shell)
        self.runner = runner
        
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', '-n', help='Name.')
    @magic_arguments.argument('--out', '-o', help='Outfile.')
    @magic_arguments.argument('--args', '-a', help='Infile and other arguments, comma-separated.')
    @magic_arguments.argument('--silent', '-q', action = 'store_true', default = False, help = 'Hide results in variable captured.')
    @magic_arguments.argument('--local', '-l', action = 'store_true', default = False, help = 'Run code in local mode using Python.')
    @magic_arguments.argument('--fstring', '-f', action='store_true', default=False, help='Interpret f-strings in code.')
    def submit(self, line, cell):
        args = magic_arguments.parse_argstring(self.submit, line)
        if args.local:
            self.runner.local = True
        if args.fstring:
            cell = cell.format(**self.shell.user_ns)
        if args.silent:
            with capture_output() as runlog:
                if args.args:
                    self.runner.submit_job(args.name, cell, args.out, *args.args.split(","))
                else:
                    self.runner.submit_job(args.name, cell, args.out)
                self.shell.user_ns['runlog'] = runlog
        else:
            if args.args:
                self.runner.submit_job(args.name, cell, args.out, *args.args.split(","))
            else:
                self.runner.submit_job(args.name, cell, args.out)      

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', '-n', help='Name.')
    @magic_arguments.argument('--out', '-o', help='Outfile.')
    @magic_arguments.argument('--args', '-a', help='Infile and other arguments, comma-separated.')
    @magic_arguments.argument('--silent', '-q', action = 'store_true', default = False, help = 'Hide results in variable captured.')
    @magic_arguments.argument('--local', '-l', action = 'store_true', default = False, help = 'Run code in local mode using Python.')
    @magic_arguments.argument('--fstring', '-f', action='store_true', default=False, help='Interpret f-strings in code.')
    def chain(self, line, cell):
        args = magic_arguments.parse_argstring(self.chain, line)
        if args.local:
            self.runner.local = True
        if args.fstring:
            cell = cell.format(**self.shell.user_ns)
        if args.silent:
            with capture_output() as runlog:
                if args.args:
                    self.runner.chain_submit(args.name, cell, args.out, *args.args.split(","))
                else:
                    self.runner.chain_submit(args.name, cell, args.out)
                self.shell.user_ns['runlog'] = runlog
        else:
            if args.args:
                self.runner.chain_submit(args.name, cell, args.out, *args.args.split(","))
            else:
                self.runner.chain_submit(args.name, cell, args.out)         
    
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--args', '-a', help='Infile and other arguments, comma-separated.')
    @magic_arguments.argument('--silent', '-q', action = 'store_true', default = False, help = 'Hide results in variable captured.')
    @magic_arguments.argument('--local', '-l', action = 'store_true', default = False, help = 'Run code in local mode using Python.')
    @magic_arguments.argument('--fstring', '-f', action='store_true', default=False, help='Interpret f-strings in code.')
    def quick(self, line, cell):
        args = magic_arguments.parse_argstring(self.quick, line)
        if args.local:
            logger.info('Run as local mode.')
            self.runner.local = True
        if args.fstring:
            cell = cell.format(**self.shell.user_ns)
        if args.silent:
            with capture_output() as runlog:
                if args.args:
                    self.runner.quick_submit(cell % tuple(args.args.split(",")))
                else:
                    self.runner.quick_submit(cell)
            self.shell.user_ns['runlog'] = runlog
        else:
            if args.args:
                self.runner.quick_submit(cell % tuple(args.args.split(",")))
            else:
                self.runner.quick_submit(cell)
