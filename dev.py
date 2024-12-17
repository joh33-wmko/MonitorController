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
import subprocess as sp
import sys


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


def run_cmd(cmdstr):
    # move path to config.live
    proc = sp.Popen(cmdstr, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    output, error = proc.communicate()
    output = output.decode("ascii").rstrip()
    return output

# these commands need to be run via ssh as koabld@vm-[k2]|koarti[build]

def apply_update(cur_ver, new_ver):
    print('monctl.py::apply_update()')

    print(f"      svr     is {svr}")
    print(f"      host     is {host}")
    print(f"      cur_ver is {cur_ver}")
    print(f"      new_ver is {new_ver}")

    #test
    cmd_str = 'ls -l; date'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    # ssh from koarti@vm-koarti|vm-k2koarti|vm-koartibuild to user koartibld
    #   so use absolute paths...
    #
    #cd execution dir
    #cmd_str = 'cd /koa/dep_rti/'
    #print(cmd_str)
    #resp = run_cmd(cmd_str)
    #print(resp)

    #mkdir $new_ver
    cmd_str = 'mkdir new_ver'
    #cmd_str = f'ssh koartibld@vm-koartibuild mkdir /koa/dep-rti/{new_ver}'
    #cmd_str = f'ssh koartibld@vm-koartibuild mkdir /usr/local/koa/dep-rti/${new_ver}'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #cp -pr $cur_ver $new_ver
    cmd_str = 'cp -pr {cur_ver} {new_ver}'
    #cmd_str = f'ssh koartibld@vm-koartibuild cp -pr /koa/dep-rti/{cur_ver} /koa/dep-rti/{new_ver}'
    #cmd_str = f'ssh koartibld@vm-koartibuild cp -pr /koa/dep-rti/${cur_ver} /koa/dep-rti/${new_ver}'
    #cmd-str = f'ssh koartibld@vm-koartibuild cp -pr /usr/local/koa/dep-rti/${cur_ver} /usr/local/koa/dep-rti/${new_ver}'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #unlink default
    cmd_str = 'unlink default'
    #cmd_str = f'ssh koartibld@vm-koartibuild unlink /koa/dep-rti/default'
    print(cmd_str)
    #resp = run_cmd(cmd_str)
    print(resp)

    #ln -s $new_ver default
    #cmd_str = 'ln -s new_ver default2'
    #cmd_str = f'ssh koartibld@vm-koartibuild ln -s /koa/dep-rti/2.6.0 /koa/dep-rti/default'
    #cmd_str = f'ssh koartibld@vm-koartibuild ln -s /koa/dep-rti/${new_ver} /koa/dep-rti/default'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #git status
    cmd_str = 'git status'
    cmd_str = f'ssh koartibld@vm-koartibuild cd /koa/koa-rti/{cur_ver}; git status'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #git pull
    cmd_str = 'git pull'
    #cmd_str = f'ssh koartibld@vm-koartibuild cd /koa/koa-rti/{new_ver}; git pull'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #git status
    cmd_str = 'git status'
    cmd_str = f'ssh koartibld@vm-koartibuild cd /koa/koa-rti/{new_ver}; git status'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    #git diff contents of curr and new dirs
    cmd_str = 'git diff cur_ver new_ver'
    #cmd_str = f'ssh koartibld@vm-koartibuild git diff /koa/dep-rti/2.5.0 /koa/dep-rti/2.6.0'
    #cmd_str = f'ssh koartibld@vm-koartibuild git diff /koa/dep-rti/{cur_ver} /koa/dep-rti/{new_ver}'
    print(cmd_str)
    resp = run_cmd(cmd_str)
    print(resp)

    # restart new version of monitors
    print('monctl.sh::stop_monitors()')
    #stop_monitors()
    print('monctl.sh::start_monitors()')
    #start_monitors()

    return


def display_status():
    print("monctl.py::display_status()")


def start_monitors(): # L0 and DRPs
    print("monctl.py::start_monitors()")


def stop_monitors():  # L0 and DRPs
    print("monctl.py::stop_monitors()")


def process_release(cur_ver, new_ver):
    print("monctl.py::process_release()")
    apply_update(cur_ver,new_ver)
    
    return


def main():
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

    print(f"Server: {svr} {host}")
    print("monctl.py::main()")


    # determine cmd
    if args.cmd:
       cmd = args.cmd
    #else:
        #pass

    #import re
    #pattern = r'^\d+\.\d+\.\d+$'
    #validVersion = bool(re.match(pattern, cmd))
    #if validVersion:
    #    new_ver = cmd
    #    cmd = 'rel'

    # accept without checking for now...
    if cmd not in ("start", "stop", "status"):
        new_ver = cmd

        cmd_str = "ls -l /koa/dep-rti/default | awk '{print $11}'"
        cur_ver = run_cmd(cmd_str)
        cmd = 'rel'

    if cmd == "status":
        print(f"   Processing cmd: {cmd}")
        display_status()
    elif cmd == "start":
        print(f"   Processing cmd: {cmd}")
        start_monitors() # L0 and DRPs
    elif cmd == "stop":
        print(f"   Processing cmd: {cmd}")
        stop_monitors()  # L0 and DRPs
    elif cmd == "rel":
        print(f"   Processing cmd: {cmd}")
        process_release(cur_ver, new_ver) # assumes ...
    else:
        print(f"cmd not recognized: {cmd}")
        sys.exit()


if __name__ == "__main__":
    main()
