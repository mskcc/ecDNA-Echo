#!/bin/bash

CONFIG_FILE=$1
source $CONFIG_FILE

mkdir -p $echoLogDirectory 2>/dev/null

clusterCPUNum=$clusterCPUNum
clusterMemory=$clusterMemory
clusterTime=$clusterTime

if [[ $clusterTime != *:* ]]; then
    clusterTime="${clusterTime}:00"
fi

ts=$(date +%Y%m%d%H%M%S)

cmd="bsub \
    -W ${clusterTime} \
    -n ${clusterCPUNum} \
    -R 'rusage[mem=${clusterMemory}]' \
    -J 'call_submit_on_cluster' \
    -o '${echoLogDirectory}/call_submit_on_cluster.${ts}.stdout' \
    -e '${echoLogDirectory}/call_submit_on_cluster.${ts}.stderr' \
    sh submit_on_cluster.sh $CONFIG_FILE"
echo "$cmd"
eval $cmd