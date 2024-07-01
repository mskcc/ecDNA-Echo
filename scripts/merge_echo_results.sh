#!/bin/bash

# config file
CONFIG_FILE=$1
source $CONFIG_FILE


dataDir=$dataDirectory
outputDir=${mergedOutputDirectory}
mergedFile=${outputDir}/merged.ECHO_results.csv
echoOutputDir=${echoOutputDirectory}

mkdir -p $outputDir 2>/dev/null

echo "Scanning ${echoFlagDirectory}"
countFail=$(find ${echoFlagDirectory} -type f -name "*.fail" | wc -l)
echo "Number of fail files found: $countFail"
countRunning=$(find ${echoFlagDirectory} -type f -name "*.running" | wc -l)
echo "Number of running files found: $countRunning"

if [ -f "$mergedFile" ]; then
  rm $mergedFile
fi

count=0

for i in "$echoOutputDir"/*/*/*.csv; do

  [[ -e "$i" ]] || break

  if [[ "$count" == 0 ]]; 
  then
    cat "$i" > ${mergedFile}
  else
    < "$i" tail -n+2 >> ${mergedFile}
  fi

 count=$((count+1))

done

echo "Total Files Found = $count"
