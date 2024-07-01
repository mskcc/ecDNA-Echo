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

echoReportFile=${mergedOutputDirectory}/merged.ECHO_results.csv

ts=$(date +%Y%m%d%H%M%S)

if [[ $clusterTime != *:* ]]; then
    clusterTime="${clusterTime}:00"
fi

# Read each line of file
while IFS=, read -r sample_id _ gene _; do
    IFS='-' read -ra parts <<< "$sample_id"
    sampleID=""
    for ((i=0; i<4 && i<${#parts[@]}; i++)); do
        sampleID+="${parts[i]}-"
    done
    sampleID=${sampleID%-} 

    
    # Remove NA
    if [[ $sampleID == "NA" ]]; then
        sampleID=""
    fi

    if [[ $gene != "gene" ]]; then
        flag_done="${flagDir}/${sampleID}_${gene}.done"

        if [[ ! -f $flag_done ]]; then

            # Run sample
            if [[ $gene != "gene" ]]; then
                cmd="bsub \
                    -W ${clusterTime} \
                    -n ${clusterCPUNum} \
                    -R 'rusage[mem=${clusterMemory}]' \
                    -J 'facets_api_pull' \
                    -o '${logDir}/facets_api_pull_${sampleID}_${gene}_${ts}.stdout' \
                    -e '${logDir}/facets_api_pull_${sampleID}_${gene}_${ts}.stderr' \
                    sh submit_one_facets.sh ${CONFIG_FILE} ${sampleID} ${gene}"
                echo "$cmd"
                eval $cmd

            fi
        fi      
    fi

done < "$echoReportFile"