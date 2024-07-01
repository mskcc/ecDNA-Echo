'''
This script takes in a FileA manifest document and changes the purity
from pathological to facets called tumor purity for a subset in FileB
'''

import os
import sys
import argparse
import pandas as pd
import math

# TODO: allow for analysisType 2
# Right now only for aType 1

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
# FileA to change
parser.add_argument('--sampleManifest', required=True)
# FileB, list of genes
parser.add_argument('--subsetFile', required=True)
# Path to the output FileA
parser.add_argument('--outputFile', required=True)
# Path to facets report
parser.add_argument('--facetsReport', required=True)
# ID Column
parser.add_argument('--sampleIDColumn', required=True)
# Purity Column
parser.add_argument('--samplePurityColumn', required=True)
# Default purity
parser.add_argument('--defaultPurity', required=True)

args = parser.parse_args()

FileA = args.sampleManifest
FileB = args.subsetFile
IDCol = int(args.sampleIDColumn)
PurityCol = int(args.samplePurityColumn)
outFile = args.outputFile
facetsReport = args.facetsReport
defaultPurity = int(args.defaultPurity)


##################
# Convert Purity #
##################

facets_df = pd.read_csv(facetsReport, sep = '\t', index_col = False)
fileB_df = pd.read_csv(FileB, sep = '\t', index_col = False, header = None)

# get FileA into a dataframe
if is_xlsx(FileA) :
    print("FileA is xlsx")
    fileA_df = pd.read_excel(FileA, engine='openpyxl', header = None)
else :
    print("FileA is tsv")
    fileA_df = pd.read_csv(FileA, sep = '\t', header = None)

# Get the subset of fileA
listOfIDs=fileB_df.iloc[:,0].unique().tolist()
subset_fileA_df=fileA_df[fileA_df.iloc[:,IDCol].isin(listOfIDs)]

facets_df['Facets Purity'] = facets_df['Facets Purity'].fillna(defaultPurity/100)
# Convert purity
facets_df['Facets Purity'] = (facets_df['Facets Purity'] * 100).apply(lambda x: math.ceil(x)).astype(int)

# Check facets complete
if len(subset_fileA_df) != len(facets_df) :
    print("WARNING: Facets not complete, using default where incomplete")

# replace
subset_fileA_df.iloc[:, PurityCol] = defaultPurity

for index, row in facets_df.iterrows() :
    idx = (subset_fileA_df.iloc[:, IDCol] == row['ID']).idxmax()
    subset_fileA_df.at[idx, PurityCol] = row['Facets Purity']
# Export
subset_fileA_df.to_csv(outFile, sep='\t', index = False)