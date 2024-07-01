#!/bin/bash

# The file of samples
filename=$1
shift

# The gene
gene=$1
shift

# The data directory
dataDir=$1
shift

# The output directory
outDir=$1

cat "$filename" | while IFS= read -r line; do
    cmd="bsub -n 16 -J facets_${gene} python facets_single.py $line $dataDir ${outDir}/${line}_${gene}.tsv $gene"
    eval "$cmd"
    echo $line
done