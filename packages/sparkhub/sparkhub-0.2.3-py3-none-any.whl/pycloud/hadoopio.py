#!/usr/bin/python

from pycloud.cloud_utils import execute

def execute_hdfs_cmd(options):
    cmd = [ 'hadoop', 'fs' ] + options
    execute(cmd)

def ls(path):
    execute_hdfs_cmd(['-ls', '-h', path])

def lsr(path):
    execute_hdfs_cmd(['-ls', '-h', '-R', path])

def du(path):
    execute_hdfs_cmd([ '-du', '-s', '-h', path ])
    
def cp(from_path, to_path):
    execute_hdfs_cmd(['-cp', from_path, to_path])

def mv(from_path, to_path):
    execute_hdfs_cmd(['-mv', from_path, to_path])

    
def chmod(path, code = '700', recursive = False):
    options = [ '-chmod', code ]
    if recursive:
        options.append('-r')
    execute_hdfs_cmd(options + path)

def rm(path, recursive = False, force = False, quiet = False):
    options = [ '-rm' ]
    if recursive:
        options.append('-r')
    if force:
        options.append('-f')
    execute_hdfs_cmd(options + [ path ])
        
def rmdir(path):
    execute_hdfs_cmd([ '-rmdir', path ])        

def mkdir(path):
    execute_hdfs_cmd([ '-mkdir', '-p', path ])
    
def get(remote_path, local_path):
    """Retrieve files from hdfs/Spark file system.
    
    Specify the file or directory on the hdfs and the path to the local directory
    to copy it to.
    
    Parameters
    ----------
    remote_path : {str}
        Should start with `/user/` for the Broad system
    local_path : {str}
        Should start with file:///psych/genetics_data/tsingh/projects/sczexomes/analysis/ for the Broad system
    """
    execute_hdfs_cmd(['-get', remote_path, local_path])

def put(local_path, remote_path):
    """Copy files to the hdfs/Spark file system.
    
    Specify the file or directory on the local system to the hdfs.
    
    Parameters
    ----------
    local_path : {str}
        Should start with file:///psych/genetics_data/tsingh/projects/sczexomes/analysis/ for the Broad system
    remote_path : {str}
        Should start with `/user/` for the Broad system
    """
    execute_hdfs_cmd(['-put', local_path, remote_path])
    
def put_directory(local_dir, remote_dir):
    execute_hdfs_cmd([ '-copyFromLocal', local_dir, remote_dir ])

def get_directory(remote_dir, local_dir):
    execute_hdfs_cmd([ '-copyToLocal', remote_dir, local_dir ])

def glob(path):
    lines = execute([ 'hadoop', 'fs', '-ls', path], return_out = True, silent = True)
    return([ line.split()[-1] for line in lines[1:] ])
