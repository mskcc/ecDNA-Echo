import sys
import os
import pandas as pd
import numpy as np

# #change this to wherever the facetsAPI is stored
# sys.path.insert(1, '/juno/work/ccs/pricea2/pipelines/facetsAPI')
# # sys.path.insert(1, '/juno/work/ccs/orgeraj/facetsAPI')

from facetsAPI import *


# def get_sample_report(useSingleRun, allowDefaults, sampleList, sampleReport, dataDir):
#     clinical_sample_file= dataDir + "/input/data_clinical_sample.oncokb.txt"
#     facets_dir="/work/ccs/shared/resources/impact/facets/all/"

#     #Initialize FacetsMeta. This will build all relevant metadata we need going forward.
#     prepared_metadata = FacetsMeta(clinical_sample_file, facets_dir, "purity")
    
#     #We just want to look at a single run per sample, looking for best/acceptable fits. Default is acceptable if not.
#     prepared_metadata.setSingleRunPerSample(useSingleRun,allowDefaults)
    
#     #Read in the list of IDs we are selecting from a file. One sample per line.
#     prepared_metadata.selectSamplesFromFile(sampleList)
    
#     #Build our FacetsMeta Object.
#     prepared_metadata.buildFacetsMeta()

#     #Build our FacetsDataset Object and write a report to file.
#     test_dataset = FacetsDataset(prepared_metadata)
#     test_dataset.buildFacetsDataset()

#     test_dataset.writeReport(sampleReport)

def get_selected_genes(useSingleRun, allowDefaults, target_sample_id, target_gene_list, geneReport, dataDir):
    clinical_sample_file= dataDir + "/input/data_clinical_sample.oncokb.txt"
    facets_dir="/work/ccs/shared/resources/impact/facets/all/"

    prepared_metadata = FacetsMeta(clinical_sample_file, facets_dir, "hisens")
    prepared_metadata.setSingleRunPerSample(useSingleRun,allowDefaults)
    prepared_metadata.build_from_file_listing = True
    prepared_metadata.samples_from_file.append(target_sample_id)
    prepared_metadata.buildFacetsMeta()

    target_dataset = FacetsDataset(prepared_metadata)
    target_dataset.buildFacetsDataset()

    found_runs = []
    for facets_run in target_dataset.runList:
        found_runs.append(facets_run.id)

    for target_sample in prepared_metadata.samples_from_file:
        if target_sample not in found_runs:
            print("Missing: " + target_sample)


    #Loop over our gene objects and print out what we want.
    with open(geneReport, 'a') as outfile:
        for cur_run in target_dataset.runList:
            #print(cur_run.id)
            for cur_gene in cur_run.genes:
                if cur_gene.gene in target_gene_list:
                    outfile.write(str(cur_run.id) + "\t")
                    outfile.write(str(cur_gene.gene) + "\t")
                    outfile.write(str(cur_gene.gene_start) + "\t")
                    outfile.write(str(cur_gene.gene_end) + "\t")
                    outfile.write(str(cur_gene.seg_start) + "\t")
                    outfile.write(str(cur_gene.seg_end) + "\t")
                    outfile.write(str(cur_gene.seg_length) + "\t")
                    outfile.write(str(cur_gene.cf) + "\t")
                    outfile.write(str(cur_gene.tcn) + "\t")
                    outfile.write(str(cur_gene.lcn) + "\t")
                    outfile.write(str(cur_gene.cn_state) + "\t")
                    outfile.write(str(cur_gene.filter) + "\t")
                    outfile.write(str(cur_gene.tsg) + "\t")
                    outfile.write(str(cur_gene.seg) + "\t")
                    outfile.write(str(cur_gene.median_cnlr_seg) + "\t")
                    outfile.write(str(cur_gene.segclust) + "\t")
                    outfile.write(str(cur_gene.mcn) + "\t")
                    outfile.write(str(cur_gene.genes_on_seg) + "\t")
                    outfile.write(str(cur_gene.gene_snps) + "\t")
                    outfile.write(str(cur_gene.gene_het_snps) + "\t")
                    outfile.write(str(cur_gene.spans_segs) + "\t")
                    outfile.write("\n")


if __name__ == '__main__':


    # sampleList="/home/sumans/Projects/Project_BoundlessBio/data/facetsAPI_testing/FileB_export_ecDNATracker_records_230818160357.txt"
    # echoReportFile="/home/sumans/Projects/Project_BoundlessBio/data/facetsAPI_testing/merged.ECHO_results.csv"
    # sampleReport="/home/sumans/Projects/Project_BoundlessBio/data/facetsAPI_testing/sample_report_final_1.txt"
    # geneReport="/home/sumans/Projects/Project_BoundlessBio/data/facetsAPI_testing/gene_report_final_2.txt"


    sampleList=sys.argv[1]
    echoReportFile=sys.argv[2]
    sampleReport=sys.argv[3]
    geneReport=sys.argv[4]
    dataDir=sys.argv[5]
    # get_sample_report(True, True, sampleList, sampleReport, dataDir)

    with open(geneReport, 'w') as outfile:
        outfile.write("sample\tgene\tgene_start\tgene_end\tseg_start\tseg_end\tseg_length\tcf\ttcn\tlcn\tcn_state\tfilter\ttsg\tseg\tmedian_cnlr_seg\tsegclust\tmcn\tgenes_on_seg\tgene_snps\tgene_het_snps\tspans_segs" + "\n")


    df=pd.read_csv(echoReportFile, header=0)
    df2 = df.replace(np.nan, '', regex=True)
    for index, row in df2.iterrows():
        sampleID='-'.join(x.strip() for x in row['sample_id'].split('-')[:4])
        gene=row['gene']
        print(sampleID, gene)

        if gene:

            # get_selected_genes(True, True,"P-0001631-T03-IM6",["TP53"])
            get_selected_genes(True, True, sampleID, gene, geneReport, dataDir)