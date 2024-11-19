#! /usr/bin/bash

# requires user koarti@vm-koarti, koarti@vm-k2koarti, or koarti@vm-koartibuild
#   $ cd to script location
#   $ bash ./mon_control.sh start|stop|status k1|k2

# ToDo
# - (opt) convert to Python 3

## ===== k1 monitors =====
k1InstList=( "guiderk1" "hires" "kpf" "lris_blue" "lris_red" "mosfire" "osiris_img" "osiris_spec" )
k1InstDrpList=( "kpf" "mosfire" "osiris" )

## ===== k2 monitors =====
k2InstList=( "deimos_fcs" "deimos_spec" "guiderk2" "kcwi_blue" "kcwi_fcs" "kcwi_red" "nirc2" "nirc2_unp" "nires_img" "nires_spec" "nirspec_scam" "nirspec_spec" )
k2InstDrpList=( "kcwi" "deimos" "nirc2" "nires" )

echo

if [[ "$#" -eq 2 ]]; then
  cmd=$1
  svr=$2
else
  echo -e "Requires two arguments: command server\n"
  exit
fi

case $svr in
  "k1")
    echo "Server vm-koarti"
    instList=("${k1InstList[@]}")
    instDrpList=("${k1InstDrpList[@]}")
    ;;
  "k2")
    echo "Server vm-k2koarti"
    instList=("${k2InstList[@]}")
    instDrpList=("${k2InstDrpList[@]}")
    ;;
  *)
    echo -e "Invalid server arg: ${svr}\n"
    exit
    ;;
esac

if [[ "${svr}" == @(k1|k2) ]]; then
  echo "L0 Monitors [${#instList[@]}]: ${instList[@]}"
  echo "L0 DRP Monitors [${#instDrpList[@]}]: ${instDrpList[@]}"
fi

case $cmd in

  "status")
    ;;

  "start")
    echo "Launching $svr Monitors"
    for instr in "${instList[@]}"; do
      echo "Starting: Monitor for ${instr}"
      /usr/local/koa/dep-rti/default/src/monitor.sh ${instr}
      echo "Started: `ps -ef | grep ${instr} | grep -v grep | grep -v _drp | awk -F " " '{print $2" "$9" "$10}' | sort`"
      echo "Sleeping 10..."
      #sleep 10
      sleep 5
      echo
    done

    echo "Launching $svr DRP Monitors"
    for instr in "${instDrpList[@]}"; do
      echo "Starting: DRP Monitor for ${instr}"
      /usr/local/koa/dep-rti/default/src/monitor_drp.sh ${instr}
      echo "Started: `ps -ef | grep ${instr} | grep -v grep | grep _drp | awk -F " " '{print $2" "$9" "$10}' | sort`"
      echo "Sleeping 30..."
      #sleep 30
      sleep 10
      echo
    done
    ;;

  "stop")
    # if [monitor_drp.py] <defunct>, run again...
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
      echo
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
        echo "${instr} DRP Monitor is not running"
      fi
      echo
    done
    ;;

  *)
    echo -e "\nInvalid command arg: ${cmd}\n"
    exit
    ;;
esac

# show monitor processes and amount(s)
#   monitors and DRP monitors
#   running vs not running (list)
echo -e "\nCurrent Monitor Processes Running:\n"
ps -ef | grep monitor | grep -v grep | sort
