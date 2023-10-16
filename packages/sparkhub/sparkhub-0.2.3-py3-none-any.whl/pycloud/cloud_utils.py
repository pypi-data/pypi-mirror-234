#!/usr/bin/env python

import os
import re
import sys
import subprocess

os.environ["PYTHONUNBUFFERED"] = "1"

def execute(cmd, logger = None, return_out = False, silent = False, 
            return_cmd = False,
            shell = False, clean_spark_log = False):
    if not shell:
        cmd = [ str(c) for c in cmd ]

    if return_cmd:
        return ' '.join(cmd)

    process = subprocess.Popen(cmd,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.STDOUT,
                               bufsize = 0, #1, for buffered
                               universal_newlines = True,
                               shell = shell)
   
    f = open(logger, 'w') if logger else None

    output = []
    clean_flag = 0
    for line in iter(process.stdout.readline, ''):   
        #----
        # writing to screen   
        if not silent:
            sys.stdout.write(line)
            sys.stdout.flush()
    
        #----
        # writing to log
        if f and not clean_spark_log:
            # write everything
            f.write(line)
            f.flush()
        elif f and clean_spark_log:
            if re.search('^Welcome to', line):
                # trigger the start of the Hail run
                clean_flag = 1
                f.write(line)
            elif clean_flag == 1:
                # in the Hail run
                if line == '\n' or line == '' or re.search('^\s+$', line):
                    continue
                elif line[0:7] != '[Stage ':
                    # write non-empty line
                    f.write(line)
                elif line[0:7] == '[Stage ':
                    # Spark stage line, clean up, and write if not empty
                    l = re.sub('\[Stage\s.*\]', '', line)
                    if l != '\n' and l != '' and not re.search('\s+', l):
                        f.write(l)
            else:
                if re.search('^spark\.', line) or re.search('SparkContext', line):
                    f.write(line)
            if re.search('Job.*finished successfully.', line):
                break
            f.flush()
        if return_out:
            output.append(line)

    process.stdout.close()
    
    return_code = process.wait()
    if return_code:
        if silent and return_out:
            sys.stderr.write(''.join(output))
        raise subprocess.CalledProcessError(return_code, cmd)
       
    if return_out:
        return output
