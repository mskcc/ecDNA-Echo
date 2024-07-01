import os
import sys
import argparse
import pandas as pd


parser = argparse.ArgumentParser()

parser.add_argument('--subsetFile', required=False)

parser.add_argument('--sampleManifest', required=True)

parser.add_argument('--outputFile', required=False)

parser.add_argument('--aType', required=True)

parser.add_argument('--sampleIDColumn', required=False)

args = parser.parse_args()

if args.subsetFile is not None:
    subsetFile=args.subsetFile

if args.sampleIDColumn is not None:
    sampleIDColumn=int(args.sampleIDColumn)

sampleTrackerFilePath=args.sampleManifest
outputManifestPath=args.outputFile
analysisType=int(args.aType)

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


if analysisType == 1:

    # df = pd.read_excel(sampleTrackerFilePath, engine='openpyxl')
    # df3=df[df.iloc[:,0].str.contains(regString)==True]
    # df3.to_csv(outputManifestPath, sep='\t', index=False)
    if is_xlsx(sampleTrackerFilePath) :
        print("Tracker is xlsx")
        df = pd.read_excel(sampleTrackerFilePath, engine='openpyxl')
    else :
        print("Tracker is tsv")
        df = pd.read_csv(sampleTrackerFilePath, sep = '\t', header=None, skiprows=[0])

    if is_xlsx(subsetFile) :
        print("Subset is xlsx")
        df_1 = pd.read_excel(subsetFile, engine='openpyxl', header=None)
    else :
        print("Subset is tsv")
        df_1 = pd.read_csv(subsetFile, sep = '\t', header = None)

    listOfIDs=df_1.iloc[:,0].unique().tolist()
    df_filtered=df[df.iloc[:,sampleIDColumn].isin(listOfIDs)]
    # df_filtered_merged=pd.merge(df_filtered, df_1, left_on="DMP Sample ID", right_on="Sample ID")
    df_filtered.to_csv(outputManifestPath, sep='\t', index=False, header = False)
    # df_filtered_merged.to_csv(outputManifestPath, sep='\t', index=False)


elif analysisType == 2:

    if is_xlsx(sampleTrackerFilePath) :
        print("Tracker is xlsx")
        df = pd.read_excel(sampleTrackerFilePath, engine='openpyxl')
    else :
        print("Tracker is tsv")
        df = pd.read_csv(sampleTrackerFilePath, sep = '\t')

    if is_xlsx(subsetFile) :
        print("Subset is xlsx")
        df_1 = pd.read_excel(subsetFile, engine='openpyxl')
    else :
        print("Subset is tsv")
        df_1 = pd.read_csv(subsetFile, sep = '\t')
    
    listOfIDs=df_1.iloc[:,sampleIDColumn].unique().tolist()
    df_filtered=df[df.iloc[:,0].isin(listOfIDs)]
    df_filtered_merged=pd.merge(df_filtered, df_1, left_on="DMP Sample ID", right_on="Sample ID")
    # df_filtered.to_csv(outputManifestPath, sep='\t', index=False)
    df_filtered_merged.to_csv(outputManifestPath, sep='\t', index=False)

# TODO: allow for no subset file