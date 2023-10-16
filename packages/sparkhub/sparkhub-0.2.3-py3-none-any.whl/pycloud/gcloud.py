#!/usr/bin/env python

import os
import sys
import re
import subprocess
import shutil
import tempfile
import yaml
from .cloud_utils import execute
from .slackconnector import SlackConnector

class GCloud():
    def __init__(self, account, project = None, local = True):
        self.account = account
        self.project = project
        if local:
            self.login()
            if project:
                self.set_project()
        
    def login(self):
        execute(['gcloud', 'auth', 'login', self.account])
        
    def logout(self):
        execute(['gcloud', 'auth', 'revoke'])
    
    def set_project(self):
        execute(['gcloud', 'config', 'set', 'project', self.project])
    
    def change_project(self, project):
        execute(['gcloud', 'config', 'set', 'project', self.project])
        self.project = project
    
    def ls(self, path, detailed = False, bucket = False):
        cmd = ['gsutil', 'ls']
        if detailed:
            cmd.append('-L')
        else:
            cmd.append('-l')
        if bucket:
            cmd.append('-b')
        cmd.append(path)
        execute(cmd)

    def cp(self, from_path, to_path, recursive = False, multithreaded = False, return_cmd = False, quiet = False):
        cmd = ['gsutil']
        if multithreaded:
            cmd.append('-m')
        if quiet:
            cmd.append('-q')
        cmd.append('cp')
        if recursive:
            cmd.append('-r')
        cmd.extend([from_path, to_path])
        if return_cmd:
            return(' '.join(cmd))
        else:
            execute(cmd)
    
    def cpi(self, paths, to_path, quiet = False):
        cmd = ['gsutil', '-m']
        if quiet:
            cmd.append('-q')
        cmd.append('cp')
        cmd.extend(paths)
        cmd.append(to_path)
        execute(cmd)
    
    def mv(self, from_path, to_path, keep_permissions = False, 
           multithreaded = False):
        cmd = ['gsutil', 'mv']
        if keep_permissions:
            cmd.append('-p')
        if multithreaded:
            cmd.append('-m')
        cmd.extend([from_path, to_path])
        execute(cmd)
        
    def du(self, path, total = True, human = True):
        cmd = ['gsutil', 'du', '-c']
        if human:
            cmd.append('-h')
        if total:
            cmd.append('-s')
        cmd.append(path)
        execute(cmd) 
    
    def create_bucket(self, path,
                      storage_class = 'regional', 
                      location = 'us-central1'):
        '''Storage classes: 
        https://cloud.google.com/storage/docs/storage-classes#regional
        '''
        cmd = ['gsutil', 'mb'] 
        cmd.append('-c {}'.format(storage_class))
        cmd.append('-l {}'.format(location))
        cmd.append('-p {}'.format(self.project))
        cmd.append(path)
        execute(cmd)
    
    def delete_bucket(self, path):
        '''Bucket must be empty first. Equivalent to rmdir'''
        execute(['gsutil', 'rb', path])
        
    def rm(self, path, recursive = False, force = False, quiet = False, multithreaded = False):
        '''* remove all objects in subdirectory. 
           ** removes all objects in subdirectory and those under them'''
        cmd = ['gsutil']
        if multithreaded:
            cmd.append('-m')
        cmd.append('rm')
        if recursive:
            cmd.append('-r')
        if force:
            cmd.append('-f')
        cmd.append(path)
        execute(cmd)
    
    def describe_project(self, path):
        execute(['gcloud', 'projects', 'get-iam-policy', self.project])
        execute(['gcloud', 'projects', 'describe', self.project])
    
    def list_projects(self):
        execute(['gcloud', 'projects', 'get-iam-policy', self.project])
    
    def rsync(self, from_path, to_path, 
              delete_too = False, recursive = False,
              multithreaded = False):
        cmd = ['gsutil', 'rsync'] 
        if delete_too:
            cmd.append('-d')
        if recursive:
            cmd.append('-r')
        if multithreaded:
            cmd.append('-m')
        cmd.extend([from_path, to_path])
        execute(cmd)
                
    def get_permission(self, path, recursive = False):
        cmd = ['gsutil', 'acl', 'get']
        if recursive:
            cmd.append('-r')
        cmd.append(path)
        execute(cmd)  
    
    def chmod(self, path, entity, 
              permission = None, 
              is_user = True, 
              is_group = False,
              is_project = False,
              add_modify = True, 
              remove = False,
              recursive = False, 
              multithreaded = False):
        ''' 
        Role must be: R, W, O.

        Sample uses:

        Everyone on the internet. 
        -g AllUsers:R 
        -g AllAuth:R

        Individual user:
        -u john.doe@example.com:W

        Group:
        -g admins@example.com:O
        -g broadinstitute.org:R # all Broad users

        Owners of example project:
        -p owners-example-project:W
        -p owners-12345:W # project number   
        '''
        cmd = ['gsutil']
        if multithreaded:
            cmd.append('-m')
        cmd.append('acl ch')
        if recursive:
            cmd.append('-r')
        if remove:
            cmd.extend(['-d', entity])
            cmd.append(path)
        else:
            if is_user:
                cmd.append('-u')
            elif is_group:
                cmd.append('-g')
            elif is_project:
                cmd.append('-p')
            cmd.append('{}:{}'.format(entity, permission))
        execute(cmd)
    
    def ComputeEngine(self):
        return(ComputeEngine(self.account, self.project))
    
class ComputeEngine():
    def __init__(self, account, project):
        self.account = account
        self.project = project
        self.instances = None
        self.get_instances(True)
        return
    
    def list_images(self):
        execute(['gcloud', 'compute', 'images', 'list'])
    
    def list_instances(self):
        execute(['gcloud', 'compute', 'instances', 'list'])
    
    def get_instances(self, silent = False):
        instances = {}
        output = execute(['gcloud', 'compute', 'instances', 'list'], return_out = True, silent = True)
        for instance in output[1:]:
            if instance == '':
                continue
            instance = instance.split()
            instances[instance[0]] = {'zone': instance[1], 'machine_type': instance[2], 'status': instance[-1] }
        self.instances = instances
        if not silent:
            print(instances)
    
    def ComputeEngineInstance(self, name):
        if name in self.instances:
            return(ComputeEngineInstance(instance = name,
                                         project = self.project,
                                         machine_type = self.instances[name]['machine_type'],
                                         zone = self.instances[name]['zone'], create = False))
        else:
            return(None)
                                                   
    def _list_machine_types(self):
        # g1-small: 1 cpu, 1.7 GB
        machine_types = ['f1-micro', 'g1-small']
        # n1-standard-x: x cpus, 3.75 GB per CPU
        machine_types.extend(['n1-standard-{}'.format(i) for i in [1, 2, 4, 8, 17, 32, 64]])
        # n1-highmem-x: x cpus, 6.5 GB per CPU
        machine_types.extend(['n1-highmem-{}'.format(i) for i in [2, 4, 8, 17, 32, 64]])
        # n1-highcpu-x: x cpus, 0.9 GB per CPU
        machine_types.extend(['n1-highcpu-{}'.format(i) for i in [2, 4, 8, 17, 32, 64]])
        self.machine_types = machine_types
    
    def show_machine_types(self):
        _list_machine_types()
        print(self.machine_types)
        
class ComputeEngineInstance():
    def __init__(self, instance, project,
                 zone = 'us-central1-a', 
                 machine_type = 'n1-highmem-4', 
                 create = True,
                 image = 'debian-8', # can be user image as well
                 boot_disk_size = None, 
                 description = None,
                 preemptible = False):
        '''
        https://cloud.google.com/compute/docs/images
        '''
        self.instance = instance
        self.project = project
        self.zone = zone
        self.machine_type = machine_type
        self.image = image
        self.boot_disk_size = None
        self.description = None
        self.preemptible = None
        if create:
            self.create_instance()
            
    def create_instance(self):
        cmd = ['gcloud', 'compute', 'instances', 'create']
        cmd.extend([self.instance])
        cmd.extend(['--zone', self.zone])
        cmd.extend(['--image {}'.format(self.image)])
        cmd.extend(['--machine-type', self.machine_type])
        if self.boot_disk_size:
            cmd.extend(['--boot-disk-size', self.boot_disk_size])
        if self.description:
            cmd.extend(['--description', self.description])
        if self.preemptible:
            cmd.extend(['--preemptible'])
        execute(cmd)
    
    def start(self):
        execute(['gcloud', 'compute', 'instances', 'start', self.instance, '--zone', self.zone])
        
    def stop(self):
        execute(['gcloud', 'compute', 'instances', 'stop', self.instance, '--zone', self.zone])
    
    def delete(self):
        execute(['gcloud', 'compute', 'instances', 'delete', self.instance, '--zone', self.zone])
        
    def reset(self):
        execute(['gcloud', 'compute', 'instances', 'reset', self.instance, '--zone', self.zone])
    
    def describe(self):
        output = execute(['gcloud', 'compute', 'instances', 'describe', 
                          self.instance, '--zone', self.zone],
                         silent = True, return_out = True)
        return(yaml.safe_load(''.join(output)))
    
    def ssh(self):
        '''Connecting securely
        https://cloud.google.com/solutions/connecting-securely'''
        cmd = ['gcloud', 'compute', '--project', self.project, self.zone, self.instance]
        print(' '.join(cmd))
        
    def tunnel(self, port = 2708, silent = False):
        cmd = ['gcloud', 'compute', 'ssh', self.instance]
        cmd.extend(['--project', self.project])
        cmd.extend(['--zone', self.zone])
        if silent:
            cmd.extend(['--ssh-flag=-f', '--ssh-flag=-N'])
        cmd.extend(['--ssh-flag=-L'])
        cmd.extend(['--ssh-flag={0}:localhost:{0}'.format(port)])
        print(' '.join(cmd))  
        
class DataProc():
    def __init__(self, account, project):
        self.account = account
        self.project = project
        self.instances = None
        self.get_instances(True)
        return
    
    def list_instances(self):
        execute(['gcloud', 'dataproc', 'clusters', 'list'])
    
    def get_instances(self, silent = False):
        instances = {}
        output = execute(['gcloud', 'dataproc', 'clusters', 'list'], return_out = True, silent = True)
        for instance in output[1:]:
            if instance == '':
                continue
            instance = instance.split()
            instances[instance[0]] = {'zone': instance[-1], 'worker_count': instance[1], 'status': instance[2] }
        self.instances = instances
        if not silent:
            print(instances)
    
    def describe_instance(self, instance):
        output = execute(['gcloud', 'dataproc', 'clusters', 'describe', instance], 
                         silent = True, return_out = True)
        return(yaml.safe_load(''.join(output)))
    
    def DataProcInstance(self, name):
        self.get_instances(True)
        if name in self.instances:
            desc = self.describe_instance(name)
            dpi = DataProcInstance(name,
                                    self.account,
                                    self.project,
                                    zone = desc['config']['gceClusterConfig']['zoneUri'].split('/')[-1],
                                    initialization_actions = ','.join([ ia['executableFile'] for ia in desc['config']['initializationActions'] ]),
                                    master_machine_type = desc['config']['masterConfig']['machineTypeUri'].split('/')[-1],
                                    master_boot_disk_size = desc['config']['masterConfig']['diskConfig']['bootDiskSizeGb'],
                                    n_workers = desc['config']['workerConfig']['numInstances'],
                                    worker_machine_type = desc['config']['workerConfig']['machineTypeUri'].split('/')[-1],
                                    n_worker_local_ssds = desc['config']['workerConfig']['diskConfig']['numLocalSsds'] if 'numLocalSsds' in desc['config']['workerConfig']['diskConfig'] else 0,
                                    worker_boot_disk_size = desc['config']['workerConfig']['diskConfig']['bootDiskSizeGb'],
                                    n_pre_workers = desc['config']['secondaryWorkerConfig']['numInstances'],
                                    #preworker_boot_disk_size = desc['config']['secondaryWorkerConfig']['diskConfig']['bootDiskSizeGb']
                                    version = desc['config']['softwareConfig']['imageVersion'],
                                    properties = desc['config']['softwareConfig']['properties'], 
                                  create = False)         
            return(dpi)
        else:
            return(None)
    
    def DataProcHailInstance(self, name):
        dpi = self.DataProcInstance(name)
        dpi.__class__ = DataProcHailInstance
        return(dpi)
    
    def _list_machine_types(self):
        # g1-small: 1 cpu, 1.7 GB
        machine_types = ['f1-micro', 'g1-small']
        # n1-standard-x: x cpus, 3.75 GB per CPU
        machine_types.extend(['n1-standard-{}'.format(i) for i in [1, 2, 4, 8, 17, 32, 64]])
        # n1-highmem-x: x cpus, 6.5 GB per CPU
        machine_types.extend(['n1-highmem-{}'.format(i) for i in [2, 4, 8, 17, 32, 64]])
        # n1-highcpu-x: x cpus, 0.9 GB per CPU
        machine_types.extend(['n1-highcpu-{}'.format(i) for i in [2, 4, 8, 17, 32, 64]])
        self.machine_types = machine_types
    
    def show_machine_types(self):
        _list_machine_types()
        print(self.machine_types)

def set_actions(hail = True, hail01 = False, jupyter = True, vep = False, vep_reference = 'GRCh37', repos = False, r = False):
    # /Users/tsingh/conda3/lib/python3.7/site-packages/hailctl/deploy.yaml
    actions = []
    if hail:
        actions.append('gs://hail-common/hail-init.sh')
        actions.append('gs://dataproc-initialization-actions/conda/bootstrap-conda.sh')
    if jupyter: # now default
        #if not hail01:
        #   actions.append('gs://hail-common/hailctl/dataproc/0.2.16/init_notebook.py')
        #else:
        actions.append('gs://hail-common/cloudtools/init_notebook-0.1-4.py') # actions.append('gs://hail-common/cloudtools/init_notebook1.py')
    if vep:
        if hail01:
            #actions.append('gs://tsingh/bin/vep85-init.sh')
            actions.append('gs://hail-common/vep/vep/vep85-init.sh')
        else:
            actions.append('gs://hail-common/vep/vep/vep{vep_version}-loftee-1.0-{vep_ref}-init-docker.sh'.format(
                vep_version = 85 if vep_reference == 'GRCh37' else 95,
                vep_ref = vep_reference))
    if repos:
        actions.append('gs://tsingh/bin/init_repos.sh')
    if r: 
        actions.append('gs://gnomad-public/tools/inits/master-init.sh')
    return(actions) 

def hail_paths(version = 2):
    hail_version = '0.1' if version == 1 else '0.2'
    spark_version = '2.0.2' if version == 1 else '2.4.0' # goes with image version 1.1

    hail_bucket = 'gs://hail-common/builds/{}'.format(hail_version)    
    hail_hash_path = '{}/latest-hash-spark-{}.txt'.format(hail_bucket, spark_version) if hail_version == '0.1' \
        else '{}/latest-hash/cloudtools-5-spark-{}.txt'.format(hail_bucket, spark_version)
    hail_hash = execute(['gsutil', 'cat', hail_hash_path], return_out = True, silent = True)[0].strip()
    hail_jar = '{0}/jars/hail-{1}-{2}-Spark-{3}.jar'.format(hail_bucket, hail_version, hail_hash, spark_version)
    pyhail_zip = '{0}/python/hail-{1}-{2}.zip'.format(hail_bucket, hail_version, hail_hash)
    
    if version == 1:
        pyhail_zip = 'gs://hail-common/builds/0.1/python/hail-0.1-5a6778710097.zip'
        hail_jar = 'gs://hail-common/builds/0.1/jars/hail-0.1-5a6778710097-Spark-2.0.2.jar'
    return(hail_jar, pyhail_zip)

class DataProcInstance():
    def __init__(self, instance, account, project,               
                 zone = 'us-central1-a',
                 master_machine_type = 'n1-highmem-8', 
                 master_boot_disk_size = 100, 
                 n_workers = 2, 
                 worker_machine_type = 'n1-standard-8', # 'n1-highmem-8' for VEP
                 n_worker_local_ssds = 1,
                 worker_boot_disk_size = 75, # 40
                 n_pre_workers = 2, 
                 version = 2, 
                 properties = {'spark:spark.driver.extraJavaOptions': '-Xss4M',
                               'spark:spark.executor.extraJavaOptions': '-Xss4M',
                               'spark:spark.driver.memory': '45g', 
                               'spark:spark.driver.maxResultSize': '30g',
                               'spark:spark.task.maxFailures': '20',
                               'spark:spark.kryoserializer.buffer.max': '1g',
                               'hdfs:dfs.replication': '1',
                               'dataproc:dataproc.logging.stackdriver.enable': 'false',
                               'dataproc:dataproc.monitoring.stackdriver.enable': 'false'},
                 initialization_actions = [ 'gs://hail-common/hail-init.sh' ],
                 packages = '',
                 hail_jar_path = None, hail_zip_path = None,
                 create = True,
                 dry_run = False):
        
        # Store variables
        self.account = account
        self.instance = instance
        self.project = project
        self.zone = zone
        self.master_machine_type = master_machine_type
        self.master_boot_disk_size = master_boot_disk_size
        self.n_workers = n_workers
        self.worker_machine_type = worker_machine_type
        self.n_worker_local_ssds = n_worker_local_ssds
        self.worker_boot_disk_size = worker_boot_disk_size
        self.n_pre_workers = n_pre_workers
        self.version = version
        self.image_version = '1.1.121-debian9' if version == 1 else '1.4-debian9' # froze the Hail 0.1 # 1.1.73 used to work...
        self.properties = ','.join([ '{}={}'.format(key, properties[key]) for key in properties ])
        self.initialization_actions = ','.join(initialization_actions)

        hail_jar, pyhail_zip = hail_paths(version = version)

        if hail_jar_path and hail_zip_path:
            hail_jar = hail_jar_path
            pyhail_zip = hail_zip_path

        # prepare metadata values
        self.metadata = 'JAR={0},ZIP={1}'.format(hail_jar, pyhail_zip)

        #self.packages = 'numpy<2|pandas>0.22,<0.2 4|bokeh>1.1,<1.3|parsimonious<0.9|ipykernel<5|decorator<5|requests>=2.21.0,<2.21.1|gcsfs==0.2.1|hurry.filesize==0.9|scipy>1.2,<1.4|'
        self.packages = packages # self.packages + 

        if version == 1:
            self.metadata = self.metadata + ',MINICONDA_VARIANT=2'
        else:
            self.metadata = self.metadata + ',MINICONDA_VERSION=4.4.10'
        
        #if self.packages:
        #   self.metadata = self.metadata + '|||PKGS="{}"'.format('|'.join(self.packages.strip('|').split("|")))
            
        # Create dataproc instance]
        cmd = self.create_instance_01() if version == 1 else self.create_instance()

        self.sc = SlackConnector('PyCloud')

        if create:
            print(cmd)
            execute([ str(c) for c in cmd ])
            self.sc.notify('Cluster %s has been created.' % self.instance)
        
    def create_instance(self):
        cmd = [ 
            'hailctl', 'dataproc', 'start', self.instance, 
            '--project', self.project,
            '--zone', self.zone,
            '--master-machine-type', self.master_machine_type,
            '--master-memory-fraction', 0.8,
            '--master-boot-disk-size', self.master_boot_disk_size,
            '--num-master-local-ssds', 0,
            '--num-preemptible-workers', self.n_pre_workers,
            '--num-worker-local-ssds', self.n_worker_local_ssds,
            '--num-workers', self.n_workers,
            '--preemptible-worker-boot-disk-size', 40,
            '--worker-boot-disk-size', self.worker_boot_disk_size, 
            '--worker-machine-type', self.worker_machine_type,
            '--properties', self.properties,
            '--metadata', self.metadata,
            '--init', self.initialization_actions,
        ]
        return(cmd)

    def create_instance_01(self):
        cmd = ['gcloud', 'dataproc', 'clusters','create', 
               self.instance,
               '--project', self.project,
               '--zone', self.zone,
               '--master-machine-type', self.master_machine_type,
               '--master-boot-disk-size', self.master_boot_disk_size,
               '--num-workers', self.n_workers,
               '--worker-machine-type', self.worker_machine_type,
               '--worker-boot-disk-size', self.worker_boot_disk_size, 
               '--num-worker-local-ssds', self.n_worker_local_ssds,
               '--num-preemptible-workers', self.n_pre_workers,
               '--image-version', self.image_version,
               '--initialization-actions', self.initialization_actions,
               '--properties', self.properties,
               '--metadata', self.metadata
              ]      
        return(cmd)

    def describe(self):
        output = execute(['gcloud', 'dataproc', 'clusters', 'describe', self.instance], 
                         silent = True, return_out = True)
        return(yaml.safe_load(''.join(output)))
        
    def diagnose(self):
        execute(['gcloud', 'dataproc', 'clusters', 'diagnose', self.instance])
    
    def refresh(self):
        dp = DataProc(self.account, self.project)
        self.__dict__ = dp.DataProcInstance(self.instance).__dict__
    
    def update(self, n_workers = None, n_pre_workers = None):
        cmd = [ 'gcloud', 'dataproc', 'clusters', 'update', self.instance ] 
        if n_workers:
            cmd.extend(['--num-workers', n_workers])
            self.n_workers = n_workers
        if n_pre_workers:
            cmd.extend(['--num-preemptible-workers', n_pre_workers])
            self.n_pre_workers = n_pre_workers
        execute(cmd)
        self.sc.notify('Cluster %s has been updated.' % self.instance)

    def time_warning(self):
        return
    
    def delete(self):
        execute(' '.join(['yes', '|', 'gcloud', 'dataproc', 'clusters', 'delete', self.instance ]), shell = True)
        self.sc.notify('Cluster %s has been deleted.' % self.instance)
        self.instance = None

        return
    
    def ssh(self):
        cmd = ['gcloud', 'compute', 'ssh',
               '{}-m'.format(self.instance),
               '--zone={}'.format(self.zone),
               '--ssh-flag="-D 10000 -N -f -n"'
               '> /dev/null 2>&1 &']
        print(execute(cmd, return_cmd = True))
    
    def connect(self, port):
        browser_exec = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
        cmd = [ browser_exec,
                'http://localhost:{}'.format(port),
                '--proxy-server="socks5://localhost:10000"',
                '--host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost"',
                '--user-data-dir=/tmp/',
                '> /dev/null 2>&1 &' ]
        
        print(execute(cmd, return_cmd = True))
    
    def notebook(self):
        self.connect(8123)
        
    def sparkui(self):
        self.connect(4040)
    
    def list_jobs(self, return_out = False):
        cmd = [ 'gcloud', 'dataproc', 'jobs', 'list']
        cmd.append("--cluster={}".format(self.instance))
        cmd.append("--state-filter=active")
        if not return_out:
            execute(cmd)
        else:
            output = execute(cmd, return_out = return_out, silent = True)
            return(output)
        
    def number_of_active_jobs(self):
        return(len([ 0 for line in self.list_jobs(return_out = True) if re.search('RUNNING', line) ]))