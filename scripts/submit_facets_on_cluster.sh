#!/bin/bash

# config file
CONFIG_FILE=$1
source $CONFIG_FILE

################################
# set up using the config file #
################################

# Directories
dataDir=$dataDirectory
inputDir=$inputDirectory
manifestDir=$manifestDirectory
logDir=$facetsLogDirectory
outputDir=$facetsOutputDirectory
flagDir=$facetsFlagDirectory

mkdir -p "$flagDir" 2>/dev/null
mkdir -p "$logDir" 2>/dev/null
mkdir -p "$outputDir" 2>/dev/null

if [[ $clusterTime != *:* ]]; then
    clusterTime="${clusterTime}:00"
fi

#################################

echoReportFile=${mergedOutputDirectory}/merged.ECHO_results.csv
ts=$(date +%Y%m%d%H%M%S)

if [ -f "$echoReportFile" ]; then

    cmd="bsub \
        -W ${clusterTime} \
        -n ${clusterCPUNum} \
        -R 'rusage[mem=${clusterMemory}]' \
        -J 'facets_driver' \
        -o '${logDir}/facets_multiple_call_${ts}.stdout' \
        -e '${logDir}/facets_multiple_call_${ts}.stderr' \
        sh submit_facets_multipleSamples.sh ${CONFIG_FILE}"
    echo "$cmd"
    eval $cmd

else
    echo "Generate merged ECHO report first. Aborting"
fi


