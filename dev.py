#! /usr/local/anaconda/bin/python

# RTI Monitor Controller
# 
# ./monctl.py runs in either of two modes:
# 
# (M1) ./monctl.py start|stop 
#      routine mode to launch and terminate the monitor processs
#      default mode is routine
# 
# (M2) ./monctl.py <ver>
#      release mode
#      - determine which monitors are running (ignore if new_version running)
#      - terminate current monitor processes, 
#        - track and retry termination for multiple processes per instrument
#          - terminate parent first
#            - wait (longer for drp processes)...
#            - if child process(es) do not terminate, terminate them
#      - install new version (what if activating older version?)
#        - if new_ver DNE (reverting to previous or other version)
#          - mkdir <new_ver>
#          - cp -pr cur_ver/ new_ver/
#          - verify with diff
#        - else
#          - unlink default
#          - ln -s ... default
#      - launch new default version of monitors
# 

# included...
# arg0: monctl.py    all defaults, cmd=status
# arg1: cmd          start|stop|[default=status]|[<new ver> sets release mode]
# argx: --svr        test svr (default = k0 = k1 + k2) k1|k2
#
# implement later...
# argx: --skip-start list of instruments to skip re/launch, default=""
# argx: --skip-stop  list of instruments to skip termination, default=""
# argx: --email      send log/notifications to individual or comma separated list

import argparse
import json
import socket

def parse_arguments():
    parser = argparse.ArgumentParser(description = "RTI Monitor Controller")
    parser.add_argument("cmd", type=str, default="status", \
                help="start | stop | [default=status] | \
                      [<new ver> release mode when specified")
    parser.add_argument("--svr", type=str, default="", help="on k0 only, specify k1 | k2")
    parser.add_argument("--skip_start", type=str, default="", help="List of instrument monitors to not launch")        # verify per svr
    parser.add_argument("--skip_stop",  type=str, default="", help="List of instrument monitors to not terminate")     # verify per svr
    parser.add_argument("--email",  type=str, default="", help="List of email recipients to send logs/notifications")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    args = parser.parse_args()
    return args


#import subprocess as sp
#
#fitsFile = '/s/sdata125/hires1/2024nov06/hires0002.fits OUTDIR DATE-OBS INSTRUME'
#cmd = f'/usr/local/home/koarti/bin/fitshead {fitsFile}' 
#proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
#output, error = proc.communicate()
#output = output.decode("ascii").rstrip()
#print(output)



# prep steps
##! /usr/bin/bash
#new_ver = $1
#cd /koa/dep-rti
#mkdir $new_ver
#unlink default
#ln -s $new_ver default
#git status
#git pull
#git status

# if $2 = recycle; then
#     

def display_status():
    print("monctlpy::display_status()")


def start_monitors(): # L0 and DRPs
    print("monctl.py::start_monitors()")


def stop_monitors():  # L0 and DRPs
    print("monctl.py::stop_monitors()")


def process_release(cur_ver, new_ver):
    print("monctl.py::process_release()")


import sys

def main():
    print("monctl.py::main()")
    args = parse_arguments()

    if args.verbose:
        print("Parsed Arguments")
        print(json.dumps(vars(args), indent=4))

    # determine svr
    host = socket.gethostname()

    # move to config.live
    if host == 'vm-koarti':
        svr = 'k1'
    elif host == 'vm-k2koarti':
        svr = 'k2'
    elif host == 'vm-koartibuild':
        svr = 'k0'
        if args.svr:
            svr = args.svr
    else:
        print(f"Invalid server: {host} - RTI server required.")

    print(f"processing svr: {svr} {host}")


    import re
    pattern = r'^\d+\.\d+\.\d+$'
    validVersion = bool(re.match(pattern, cmd))
    if validVersion:
        new_ver = cmd
        cmd = 'rel'

    # determine cmd
    if args.cmd:
       cmd = args.cmd

    if cmd == "status":
        display_status()
        print(f"Processing cmd: {cmd}")
    elif cmd == "start":
        start_monitors() # L0 and DRPs
        print(f"Processing cmd: {cmd}")
    elif cmd == "stop":
        stop_monitors()  # L0 and DRPs
        print(f"Processing cmd: {cmd}")
    elif cmd == "rel";
        cur_ver = ls -l
        #process_release(cur_ver, new_ver) # assumes ...
        #print(f"Processing cmd: {cmd}")
    else:
        print(f"cmd not recognized: {cmd}")
        sys.exit()


if __name__ == "__main__":
    main()
