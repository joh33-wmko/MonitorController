#! /usr/bin/bash

# Monitor Controller - Routine Mode

# Execute on an RTI ops or test server as koarti
#   koarti@vm-koarti (k1), koarti@vm-k2koarti (k2), or koarti@vm-koartibuild (k0)
#   servers are auto-detected
 
# Usage:
#   $ ./monctl.sh [cmd] [svr]                    full command with args
#                                                     - cmd start|stop|[status], where status is default
#                                                       for all servers
#                                                     - svr [k1|k2|k0] where k0 is vm-koartibuild (k1 + k2)
#                                                       for test server, only
#   $ cd to script location
#   $ ./monctl.sh start|stop|[status]            full command with args
#   $ ./monctl.sh                                assumes status command on respective server
#   $ ./monctl.sh status                         default, same as previous
#   $ ./monctl.sh start|start                    on test server, specify k1|k2
#                                                     otherwise, k0 for k1+k2 is default

# Note(s):
# (1) On test server: 
#     Running all (k0 default, k1+k2) vs specific server (start|stop|status k1|k2)
#   $ ./monctl.sh                                all: compares running processes to sum of k1 + k2
#   $ ./monctl.sh status                         same as all
#   $ ./monctl.sh start|stop                     runs on all k1 and k2 servers
#
#   $ ./monctl.sh start|stop k1|k2        specific: runs for specified k1 or k2 server
#                                         bug: status k1|k2 is not specific, refers to all

# Known Issues(s):
# - multiple monitors running per instrument
#   - does not currently track so additional processes continue to run after terminating parent process
#   - workaround: run status and stop until all terminated if child processes do not terminate on thier own
# - test server needs to separate k1|k2 when requesting for status (start and stop operate as expected)

# ToDo(s):
# - start should only launch processes that are not already running (currently restarts everything)
# - implement skip-* lists (add ESI as default on k2?)
# - hostnames to config.live
# - push to wmko koa repo
# - report missing (not running) L0 and DRP monitors
# - track number of monitors per instrument (track, wait or terminate, verify)
# - separate status k1|k2 on test server (uses all, but start|stop are separate)
# - (opt) track number of processes per server (on vm-koartibuild k0-1 and k0-2)
# - (opt) convert to Python 3

## ===== k1 monitors =====
k1InstList=( "guiderk1" "hires" "kpf" "lris_blue" "lris_red" "mosfire" "osiris_img" "osiris_spec" )
k1InstDrpList=( "kpf" "mosfire" "osiris" )

## ===== k2 monitors =====
k2InstList=( "deimos_fcs" "deimos_spec" "esi" "guiderk2" "kcwi_blue" "kcwi_fcs" "kcwi_red" "nirc2_unp" "nirc2" "nires_img" "nires_spec" "nirspec_scam" "nirspec_spec" )
k2InstDrpList=( "kcwi" "deimos" "esi" "nirc2" "nires" )

## ===== k0 (all) monitors =====
k0InstList=("${k1InstList[@]}" "${k2InstList[@]}")
k0InstDrpList=("${k1InstDrpList[@]}" "${k2InstDrpList[@]}")

echo

hostname=`hostname -s`
case ${hostname} in
  "vm-koarti") svr="k1" ;;
  "vm-k2koarti") svr="k2" ;;
  "vm-koartibuild") svr="k0" ;;
  *) echo -e "\nInvalid server ${hostname}\n"; exit ;;
esac

case "$#" in
  0) cmd="status" ;;
  1) cmd=$1 ;;
  2) cmd=$1;
     if [[ ${svr} -eq "k0" ]]; then
       svr=$2
     fi
     ;;
  *) echo -e "\nInvalid number of arguments : start|stop|[status] k0|k1|k2\n"; exit ;;
esac

case $svr in
  "k1")
    #echo "Server vm-koarti"
    instList=("${k1InstList[@]}")
    instDrpList=("${k1InstDrpList[@]}")
    ;;
  "k2")
    #echo "Server vm-k2koarti"
    instList=("${k2InstList[@]}")
    instDrpList=("${k2InstDrpList[@]}")
    ;;
  "k0")
    #echo "Server vm-koartibuild"
    instList=("${k0InstList[@]}")
    instDrpList=("${k0InstDrpList[@]}")
    ;;
  *)
    echo -e "Invalid server arg: ${svr}\n"
    exit
    ;;
esac

case $cmd in

  "status")
    ;;

  "start")
    echo "Launching $svr Monitors"
    for instr in "${instList[@]}"; do
      echo "Starting: Monitor for ${instr}"
      /usr/local/koa/dep-rti/default/src/monitor.sh ${instr}
      echo "Started: `ps -ef | grep ${instr} | grep -v grep | grep -v _drp | awk -F " " '{print $2" "$9" "$10}' | sort`"
      echo -e "Sleeping 10...\n"
      #sleep 10   # ops
      sleep 5    # test
    done

    echo "Launching $svr DRP Monitors"
    for instr in "${instDrpList[@]}"; do
      echo "Starting: DRP Monitor for ${instr}"
      /usr/local/koa/dep-rti/default/src/monitor_drp.sh ${instr}
      echo "Started: `ps -ef | grep ${instr} | grep -v grep | grep _drp | awk -F " " '{print $2" "$9" "$10}' | sort`"
      echo -e "Sleeping 30...\n"
      #sleep 30   # ops
      sleep 10   # test
    done
    ;;

  "stop")
    echo "Terminating $svr Monitors"
    for instr in ${instList[@]}; do
      echo "Stopping Monitor for ${instr}"
      ps -ef | grep monitor | grep -v _drp | grep -v grep | grep ${instr}
      pid=`ps -ef | grep monitor | grep -v _drp | grep -v grep | grep ${instr} | awk -F " " '{print $2}'`
      if [ ! -z ${pid} ]; then
        kill -15 $pid
        echo "Stopped PID=$pid"
      else
        echo "${instr} Monitor is not running"
      fi
      #echo -e "If [monitor_drp.py] <defunct>, run again...\n"   # refine to auto search, sleep, recheck, stop
    done

    echo "Terminating $svr DRP Monitors"
    for instr in ${instDrpList[@]}; do
      echo "Stopping DRP Monitor for ${instr}"
      ps -ef | grep monitor_drp | grep -v grep | grep ${instr}
      pid=`ps -ef | grep monitor_drp | grep -v grep | grep ${instr} | awk -F " " '{print $2}'`
      if [ ! -z ${pid} ]; then
        kill -15 $pid
        echo "Stopped PID=$pid"
      else
        echo -e "${instr} DRP Monitor is not running\n"
      fi
    done
    ;;

  *)
    echo -e "\nInvalid command arg: ${cmd}\n"
    exit
    ;;
esac

echo -e "Current Monitor Processes Running on ${hostname} (${svr}):\n"

mon_procs_lst=`ps -ef | grep monitor | grep -v grep | sort | grep -v _drp`
mon_procs_cnt=`ps -ef | grep monitor | grep -v grep | sort | grep -v _drp | wc -l`
echo -e "L0 (Raw) Monitors ${mon_procs_cnt} of ${#instList[@]} [${instList[@]}]\n"
echo -e "${mon_procs_lst[@]}"

drp_procs_lst=`ps -ef | grep monitor | grep -v grep | sort | grep _drp`
drp_procs_cnt=`ps -ef | grep monitor | grep -v grep | sort | grep _drp | wc -l`
echo -e "\nDRP Monitors ${drp_procs_cnt} of ${#instDrpList[@]} [${instDrpList[@]}]\n"
echo -e "${drp_procs_lst[@]}"

#echo -e "If [monitor_drp.py] <defunct>, run again...\n"   # refine to auto search, sleep, recheck, stop
echo
