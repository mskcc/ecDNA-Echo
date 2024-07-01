#!/bin/bash

# config file
CONFIG_FILE=$1
source $CONFIG_FILE

dataDir=$dataDirectory
outputDir=${mergedOutputDirectory}
flagDirFacets=${facetsFlagDirectory}
mergedFile=${outputDir}/merged.FACETS_gene_results.tsv

echo "Scanning ${facetsFlagDirectory}"
countFail=$(find ${facetsFlagDirectory} -type f -name "*.fail" | wc -l)
echo "Number of fail files found: $countFail"
countRunning=$(find ${facetsFlagDirectory} -type f -name "*.running" | wc -l)
echo "Number of running files found: $countRunning"

# Rewrite merged file
if [ -f "$mergedFile" ]; then
    rm -rf $mergedFile
fi
count=0

# Start of file
echo -e "sample\tgene\tgene_start\tgene_end\tseg_start\tseg_end\tseg_length\tcf\ttcn\tlcn\tcn_state\tfilter\ttsg\tseg\tmedian_cnlr_seg\tsegclust\tmcn\tgenes_on_seg\tgene_snps\tgene_het_snps\tspans_segs" > $mergedFile
# Iterate and add the first line
for file in $facetsOutputDirectory/*.tsv; do

    first_line=$(head -n 1 $file)
    if [[ $first_line == "" ]]; then

        to_write=${file##*/}
        to_write="${to_write//_/	}"
        to_write="${to_write%.tsv}"
        to_write="${to_write}																			"
        echo "$to_write" >> $mergedFile

    else
        cat $file >> $mergedFile
    fi

    count=$((count+1))

done
echo "Total files merged: $count"

line_count_facets=$(wc -l < $mergedFile)
echo "Number of lines in merged facets: $line_count_facets"

line_count_echo=$(wc -l < ${outputDir}/merged.ECHO_results.csv)
echo "Number of lines in merged echo: $line_count_echo"
