#!/bin/bash

# This script submits one job on the cluster for facets gene

CONFIG_FILE=$1
shift
source $CONFIG_FILE

# Directories
dataDir=$dataDirectory
outputDir=$facetsOutputDirectory
flagDir=$facetsFlagDirectory
logDir=$facetsLogDirectory


# Cluster stats
clusterCPUNum=$clusterCPUNum
clusterMemory=$clusterMemory
clusterTime=$clusterTime
if [[ $clusterTime != *:* ]]; then
    clusterTime="${clusterTime}:00"
fi

sampleID=$1
echo "Sample ID: $sampleID"
shift

gene=$1
echo "Gene: $gene"
shift

ts=$(date +%Y%m%d%H%M%S)
outFile="$outputDir/${sampleID}_${gene}.tsv"
rm -rf outFile
# Edit flags
flag_done="${flagDir}/${sampleID}_${gene}.done"
flag_inProcess="${flagDir}/${sampleID}_${gene}.running"
flag_fail="${flagDir}/${sampleID}_${gene}.fail"

rm -rf "$flag_inProcess" && \
rm -rf "$flag_fail" && \
rm -rf "$outFile" &&
touch "$flag_inProcess"

cmd="python3.8 ./facetsApiPull_v2.py ${sampleID} ${gene} ${dataDir} ${outFile}"

echo "$cmd"
if ! eval "$cmd" ; then
    # Command failed
    echo "${sampleID} ${gene} Failed"
    rm "$flag_inProcess" && touch "$flag_fail"
else 
    rm "$flag_inProcess" && touch "$flag_done"
fi
