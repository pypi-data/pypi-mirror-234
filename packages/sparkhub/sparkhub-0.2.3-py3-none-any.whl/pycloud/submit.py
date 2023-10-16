#!/usr/bin/python

import os
import sys
import subprocess
import re
import tempfile
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute(cmd, logger = None, return_out = False, silent = False, return_cmd = False, shell = False):
    if not shell:
        cmd = [ str(c) for c in cmd ]    

    if return_cmd:
        return(' '.join(cmd))

    process = subprocess.Popen(cmd, 
                               stdout = subprocess.PIPE, 
                               stderr = subprocess.STDOUT,
                               bufsize = 1,
                               universal_newlines = True,
                               shell = shell)
    
    f = open(logger, 'w') if logger else None
    
    output = []
    for line in iter(process.stdout.readline, ''):
        if not silent:
            sys.stdout.write(line)
            sys.stdout.flush()
        if f:
            f.write(line)
        if return_out:
            output.append(line)

    process.stdout.close()
    
    return_code = process.wait()
    if return_code:
        if silent and return_out:
            sys.stderr.write(''.join(output))
        raise subprocess.CalledProcessError(return_code, cmd)
        
    if return_out:
        return(output)

def unix_cmd(cmd, return_out = False, silent = False, shell = True,
             basic = True, huge_mem = False, print_error = False, # old options that aren't used
             strict = False, return_error = False):
    ''
    execute(cmd, return_out = return_out, silent = silent, shell = shell)

def archive(outdir, infile, code = 0o550):
    filename = os.path.basename(infile)
    outfile = os.path.join(outdir, filename)
    make_dir(outfile)
    shutil.copy2(infile, outdir)
    os.chmod(outfile, code)

def make_dir(outfile):
    """ make_dir checks if directory for outfile exists and creates it if necessary """
    outdir = os.path.dirname(os.path.abspath(outfile))
    try:
        os.makedirs(outdir)
    except OSError:
        if not os.path.isdir(outdir):
            raise
    return(outdir)

def rename(outfile):
    """ complete checks for existence of an outfile.part and renames it to outfile if it exists. """
    if os.path.isfile("{0}.part".format(outfile)):
        os.rename("{0}.part".format(outfile), outfile)
    else:
        raise Exception("Did not find {0}.part...".format(outfile))

def rename_ext(root, ext):
    os.rename("{0}.part.{1}".format(root, ext), "{0}.{1}".format(root, ext))

def add_tag(filelist, tag, dirname = None):
    if isinstance(filelist, str):
        return(__add_tag(filelist, tag, dirname))
    else:
        return([__add_tag(f, tag, dirname) for f in filelist])

def add_tag_chrom(filelist, tag, dirname, chrom_sep = ':'):
    if isinstance(filelist, str):
        filelist = [ filelist ]
    fofn = []
    for f in filelist:
        chrom = get_region(f, chrom = True, chrom_sep = chrom_sep)
        fofn.append(__add_tag(f, tag, os.path.join(dirname, chrom)))
    if len(fofn) == 1:
        fofn = fofn[0]
    return(fofn)       

def __add_tag(filepath, tag, dirname = None):
    filename = os.path.basename(filepath)
    if not dirname:
        dirname = os.path.dirname(filepath)
    filename_list = filename.split('.')
    filename_list.insert(1,tag)
    return(os.path.join(dirname, ".".join(filename_list)))

def change_ext(filelist, newext, oldext, dirname = None):
    if isinstance(filelist, str):
        return(__change_ext(filelist, newext, oldext, dirname))
    else:
        return([__change_ext(f, newext, oldext, dirname) for f in filelist])

def change_ext_chrom(filelist, newext, oldext, dirname, chrom_sep = ':'):
    if isinstance(filelist, str):
        filelist = [ filelist ]
    fofn = []
    for f in filelist:
        chrom = get_region(f, chrom = True, chrom_sep = chrom_sep)
        fofn.append(__change_ext(f, newext, oldext, os.path.join(dirname, chrom)))
    if len(fofn) == 1:
        fofn = fofn[0]
    return(fofn)       

def __change_ext(filepath, newext, oldext, dirname = None):
    filename = os.path.basename(filepath)
    if not dirname:
        dirname = os.path.dirname(filepath)
    filename_new = re.sub(r"{0}$".format(oldext), r"{0}".format(newext), filename)
    return(os.path.join(dirname, filename_new))

def add_ext(filelist, newext, dirname = None):
    if isinstance(filelist, str):
        return(__add_ext(filelist, newext, dirname))
    else:
        return([__add_ext(f, newext, dirname) for f in filelist])

def add_ext_chrom(filelist, newext, dirname, chrom_sep = ':'):
    if isinstance(filelist, str):
        filelist = [ filelist ]
    fofn = []
    for f in filelist:
        chrom = get_region(f, chrom = True, chrom_sep = chrom_sep)
        fofn.append(__add_ext(f, newext, os.path.join(dirname, chrom)))
    if len(fofn) == 1:
        fofn = fofn[0]
    return(fofn)       

def __add_ext(filepath, newext, dirname = None):
    filename = os.path.basename(filepath)
    if not dirname:
        dirname = os.path.dirname(filepath)
    return(os.path.join(dirname, filename+newext))

def change_outdir(filelist, dirname):
    if isinstance(filelist, str):
        return(__change_outdir(filelist, dirname))
    else:
        return([__change_outdir(f, dirname) for f in filelist])

def __change_outdir(filepath, dirname):
    filename = os.path.basename(filepath)
    return(os.path.join(dirname, filename))

def reset_tag(filelist, dirname = None, ext = None):
    if isinstance(filelist, str):
        return(__reset_tag(filelist, ext, dirname))
    else:
        return([__reset_tag(f, ext, dirname) for f in filelist])

def reset_tag_chrom(filelist, dirname, ext = None, chrom_sep = ':'):
    if isinstance(filelist, str):
        filelist = [ filelist ]
    fofn = []
    for f in filelist:
        chrom = get_region(f, chrom=True, chrom_sep = chrom_sep)
        fofn.append(__reset_tag(f, ext, os.path.join(dirname, chrom)))
    if len(fofn) == 1:
        fofn = fofn[0]
    return(fofn)       

def __reset_tag(filepath, ext = None, dirname = None, chrom_sep = ':'):
    """ ext must have a . """
    region = get_region(filepath, chrom_sep = chrom_sep)
    if not dirname:
        dirname = os.path.dirname(filepath)
    if not ext:
        ext = os.path.splitext(filepath)[1]
    return(os.path.join(dirname, region + ext))

def get_region(filepath, split = False, chrom = False, chrom_sep = ':'):
    filename = os.path.basename(filepath)
    regexp = re.compile("(?P<chrom>[0-9XY]{1,2})" + '\{0}'.format(chrom_sep) + "(?P<start>[0-9]+)\-(?P<end>[0-9]+)")
    match = regexp.search(filename)
    if match and split:
        return(match.group("chrom"), match.group("start"), match.group("end"))
    elif match and chrom:
        return(match.group("chrom"))
    else:
        filename_list = filename.split('.')
        return(filename_list[0])

def add_region(filelist, newregion, dirname):
    if isinstance(filelist, str):
        return(__add_region(filelist, newregion, dirname))
    else:
        return([__add_region(f, newregion, dirname) for f in filelist])

def __add_region(filepath, newregion, dirname = None):
    filename = os.path.basename(filepath)
    if not dirname:
        dirname = os.path.dirname(filepath)
    return(os.path.join(dirname, newregion + '.' + filename))

def replace_region(filepath, newregion, dirname = None):
    filename = os.path.basename(filepath)
    if not dirname:
        dirname = os.path.dirname(filepath)
    filename_lst = filename.split('.')
    filename_lst[0] = newregion
    return(os.path.join(dirname, '.'.join(filename_lst)))

def mktemp(outdir, suffix):
    return(outdir + tempfile.mktemp(suffix))

def decode_string(s):
    try:
        s.decode('ascii')
        return(s)
    except:
        logger.info('Replacing "%s" with "%s"', s, re.sub(r'[^\x00-\x7f]',r'', s))
        return(re.sub(r'[^\x00-\x7f]',r'', s))
