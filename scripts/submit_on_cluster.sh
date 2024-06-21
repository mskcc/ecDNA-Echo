#!/bin/bash

# config file
CONFIG_FILE=$1
source $CONFIG_FILE

################################
# set up using the config file #
################################

# Directories
dataDir=$dataDirectory
manifestDir=$manifestDirectory
inputDir=$inputDirectory
sampleFacetsLogDir=$sampleFacetsLogDirectory

mkdir -p $sampleFacetsLogDir 2>/dev/null
mkdir -p $sampleFacetsDirectory 2>/dev/null
mkdir -p $echoLogDirectory 2>/dev/null

# Analysis type
aType=$aType

# Manifest doc
sampleTrackerFile=$sampleTracker
subsetFile=$sampleSubset
facetsPurity=$useFacetsPurity
defaultPurity=$defaultPurity

# Column numbers
sampleIDColumn=$sampleIDColumn
tumorPurityColumn=$tumorPurityColumn
somaticStatusColumn=$somaticStatusColumn

# Cluster stats
clusterCPUNum=$clusterCPUNum
clusterMemory=$clusterMemory
clusterTime=$clusterTime
if [[ $clusterTime != *:* ]]; then
    clusterTime="${clusterTime}:00"
fi

# Sample facets location
sampleReportFacetsName="${sampleFacetsDirectory}/sample_report_facets.txt"


################################

ts=$(date +%Y%m%d%H%M%S)

# Create manifest if necessary
if [[ -f "$sampleTrackerFile" ]]; then
    echo "Manifest FileA Found"
    echo
else 
    echo "Manifest FileA Not Found, Creating..."
    cmd="bsub \
        -W ${clusterTime} \
        -n ${clusterCPUNum} \
        -R 'rusage[mem=${clusterMemory}]' \
        -J 'create_manifest' \
        -o '${echoLogDirectory}/make_manifest.${ts}.stdout' \
        -e '${echoLogDirectory}/make_manifest.${ts}.stderr' \
        python3.8 ./cBioPortalApiPull.py /home/yuk3/cbioportal_data_access_token.txt $subsetFile $sampleTrackerFile $defaultPurity"
    echo "$cmd"
    eval $cmd
    echo

    while [[ ! -f "$sampleTrackerFile" ]]; do
        echo
        echo "Waiting for job to finish... Feel free to quit and rerun when job is finished..."
        bjobs
        sleep 4
    done
    echo "Manifest Created, Continuing"
    sleep 1
fi

# child directory paths
outputManifest="sampleManifest_${ts}_${aType}.txt"
outputManifestPath=${manifestDir}/${outputManifest}

if [[ $subsetFile == *.xlsx ]]; then
    echo "Converting Sample List to txt"
    txt_name="${subsetFile%.xlsx}.txt"
    xlsx2csv "${subsetFile}" | sed '/^""$/d' > "${txt_name}"
    subsetFile=$txt_name

fi

# Create facets sample document
echo "Creating facets sample"
cmd="bsub \
      -W ${clusterTime} \
      -n ${clusterCPUNum} \
      -R 'rusage[mem=${clusterMemory}]' \
      -J 'Facets_sample' \
      -o '${sampleFacetsLogDir}/facets_sample.${ts}.stdout' \
      -e '${sampleFacetsLogDir}/facets_sample.${ts}.stderr' \
      python3.8 generateFacetsSampleReport.py --subsetFile $subsetFile --outputFile $sampleReportFacetsName --dataDirectory $dataDir"
echo "$cmd"
eval "$cmd"
echo

# If using facets purity change
if [[ $facetsPurity == True ]]; then
    while [[ ! -f "$sampleReportFacetsName" ]]; do
        echo
        echo "Waiting for facets report... feel free to quit and rerun when job is finished..."
        bjobs
        sleep 4
    done

    echo "Using facets purity"
    echo "New File location: ${sampleTrackerFile}.facets.tsv"
    newManifest="${sampleTrackerFile}.facets.tsv"
    cmd="python3.8 generateFacetsManifest.py --sampleManifest $sampleTrackerFile --subsetFile $subsetFile --outputFile $newManifest --facetsReport $sampleReportFacetsName --sampleIDColumn $sampleIDColumn --samplePurityColumn $tumorPurityColumn --defaultPurity $defaultPurity"
    echo "$cmd"
    eval "$cmd"
    echo

    sampleTrackerFile=$newManifest
fi

if [[ ! -f $outputManifest ]]; then
    cmd="python3.8 generateManifest_v2.py --sampleManifest $sampleTrackerFile --outputFile $outputManifestPath --subsetFile $subsetFile --aType $aType --sampleIDColumn $sampleIDColumn"
    echo "$cmd"
    eval "$cmd"
    echo

fi

# Counts the number of jobs
count=0;

mkdir -p $echoLogDirectory 2>/dev/null
for i in $(cat "$outputManifestPath" | awk -F "\t" -v sampleIDColumn=$(expr $sampleIDColumn + 1) -v tumorPurityColumn=$(expr $tumorPurityColumn + 1) -v somaticStatusColumn=$(expr $somaticStatusColumn + 1) '{print $sampleIDColumn"_"$tumorPurityColumn"_"$somaticStatusColumn}'); do

  sampleID_Tumor=$(echo "$i" | awk -F'_' '{print $1}')

  cmd="bsub \
  -W ${clusterTime} \
  -n ${clusterCPUNum} \
  -R 'rusage[mem=${clusterMemory}]' \
  -J 'echo.${sampleID_Tumor}' \
  -o '${echoLogDirectory}/${sampleID_Tumor}.${ts}.stdout' \
  -e '${echoLogDirectory}/${sampleID_Tumor}.${ts}.stderr' \
  ./preProcess_multipleSamples_v2.sh ${CONFIG_FILE} \
  $seqType \
  $i"

    echo "Sample=$sampleID_Tumor"
    echo "$cmd"
    echo "submitting Job for Sample=$sampleID_Tumor"
    eval "$cmd"
    echo

    count=$((count+1))
  
done


echo "Total Samples Found = $count"
