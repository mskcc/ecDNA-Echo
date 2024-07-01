'''
This script generates a FACETS sample report
'''

import os
import sys
import argparse
import pandas as pd
import math



'''
Checks if file is an xlsx file
'''
def is_xlsx(file) :
    with open(file, 'rb') as f :
        try : 
            magic_number = f.read(4) # finds magic number if it exists
            return magic_number == b'\x50\x4B\x03\x04'
        except :
            return False

###################
# Parse arguments #
###################

parser = argparse.ArgumentParser()

# FileB, list of genes (subset)
parser.add_argument('--subsetFile', required=True)
# full list of genes
parser.add_argument('--fullFile', required=True)
# output 
parser.add_argument('--outputFile', required=True)
# full output
parser.add_argument('--outputFileFull', required=True)
# data directory
parser.add_argument('--dataDirectory', required=True)
# full cbioportal info
parser.add_argument('--fullInfo', required=True)
# subset cbioportal info
parser.add_argument('--subsetInfo', required=True)
# merged full file
parser.add_argument('--mergedOutputFull', required=True)
# merged subset file
parser.add_argument('--mergedOutput', required=True)

args = parser.parse_args()

FileB = args.subsetFile
fullFileB = args.fullFile
outFile = args.outputFile
outFileFull = args.outputFileFull
dataDir = args.dataDirectory
FileA = args.subsetInfo
fullFileA = args.fullInfo
merged = args.mergedOutput
mergedFull = args.mergedOutputFull


###################
# Generate Facets #
###################

from facetsAPI import *

clinical_sample_file= dataDir + "/input/data_clinical_sample.oncokb.txt"
facets_dir="/work/ccs/shared/resources/impact/facets/all/"

prepared_metadata = FacetsMeta(clinical_sample_file, facets_dir, "purity")
prepared_metadata.setSingleRunPerSample(True,True)
prepared_metadata.selectSamplesFromFile(fullFileB)

prepared_metadata.buildFacetsMeta()
test_dataset = FacetsDataset(prepared_metadata)
test_dataset.buildFacetsDataset()

# Write a report
test_dataset.writeReport(outFileFull)

#######################
# Make FACETS reports #
#######################

# Facets report
fullOut = pd.read_csv(outFileFull, sep = '\t', index_col = False)
# List of all samples
allSamples = pd.read_csv(fullFileB, sep = '\t', header = None, index_col = False, names = ['sampleId'])
fullOut = fullOut.merge(allSamples, how = 'right', left_on = 'ID', right_on = 'sampleId')

# Create subset
sampleList = pd.read_csv(FileB, sep = '\t', header = None, names = ['sampleId'])
toRunDict = set(sampleList['sampleId'].unique())
subsetOut = fullOut[fullOut['sampleId'].isin(toRunDict)]
subsetOut.to_csv(outFile, index = False, sep = '\t')
fullOut.to_csv(outFileFull, index = False, sep = '\t')

#########################
# Merge with cBioPortal #
#########################

fullCbio = pd.read_csv(fullFileA, sep = '\t', index_col = False)
subsetCbio = pd.read_csv(FileA, sep = '\t', index_col = False)

mergedFullDF = fullOut.merge(fullCbio, how = 'right', left_on = 'ID', right_on = 'sampleId')
mergedFullDF.drop(["TumorPurity", 'Cancer Type', 'Cancer Type Detail'], axis = 1, inplace = True)
cols = mergedFullDF.columns.tolist()
cols = ['ID'] + [col for col in cols if col != 'ID']
mergedFullDF = mergedFullDF[cols]
mergedFullDF.to_csv(mergedFull, sep = '\t', index = False)

mergedSubsetDF = subsetOut.merge(subsetCbio, how = 'right', left_on = 'ID', right_on = 'sampleId')
mergedSubsetDF.drop(["TumorPurity", 'Cancer Type', 'Cancer Type Detail'], axis = 1, inplace = True)
cols = mergedSubsetDF.columns.tolist()
cols = ['ID'] + [col for col in cols if col != 'ID']
mergedSubsetDF = mergedSubsetDF[cols]
mergedSubsetDF.to_csv(merged, sep = '\t', index = False)
