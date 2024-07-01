import os
import sys
import pandas as pd



keyFile=sys.argv[1]
#print(keyFile)

bamMirrorPath=sys.argv[2]


sampleID=sys.argv[3]
#print(sampleID)

sampleType=sys.argv[4]


df=pd.read_csv(keyFile, header=None)

if sampleType == "T":
    try: 
        bamID=df[df.iloc[:,0].str.contains(sampleID)].iloc[:,1].values[0]
    except :
        print(f"Error: bamID not found for {sampleID}", file = sys.stderr)
        sys.exit(1)
    #print(bamID)

elif sampleType == "N":

    ID=sampleID.split('-')
    ID[2]='N..'
    ID_N='-'.join(ID)

    try :
        bamID=df[df.iloc[:,0].str.contains(ID_N)].iloc[:,1].values[0]
    except :
        print(f"Error: bamID not found for {ID_N}", file = sys.stderr)
        sys.exit(1)
    #print(bamID)

bamFilePath=os.path.join(bamMirrorPath,bamID[0],bamID[1],bamID + ".bam")
print(bamFilePath)
