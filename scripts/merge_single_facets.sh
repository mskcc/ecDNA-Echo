#!/bin/bash

# Directory containing your files
directoryToMerge=$1
shift
mergedFile=$1

if [ -f "$file" ]; then
    rm $mergedFile
fi

echo -e "sample\tgene\tgene_start\tgene_end\tseg_start\tseg_end\tseg_length\tcf\ttcn\tlcn\tcn_state\tfilter\ttsg\tseg\tmedian_cnlr_seg\tsegclust\tmcn\tgenes_on_seg\tgene_snps\tgene_het_snps\tspans_segs" > $mergedFile

# Iterate over each file in the directory
for file in "$directoryToMerge"/*; do
    # Skip directories
    if [ -f "$file" ]; then
        # Append content of each file, ignoring the first line
        cat "$file" >> "$mergedFile"
    fi
done
