import sys
import os
import pandas as pd
import numpy as np

from facetsAPI import *

sampleID = sys.argv[1]
gene = sys.argv[2]
dataDir = sys.argv[3]
outFile = sys.argv[4]

def get_selected_genes(useSingleRun, allowDefaults, target_sample_id, target_gene_list, dataDir):
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
    to_write = ''
    for cur_run in target_dataset.runList:

        for cur_gene in cur_run.genes:
            if cur_gene.gene in target_gene_list:

                to_write += str(cur_run.id) + "\t"
                to_write += str(cur_gene.gene) + "\t"
                to_write += str(cur_gene.gene_start) + "\t"
                to_write += str(cur_gene.gene_end) + "\t"
                to_write += str(cur_gene.seg_start) + "\t"
                to_write += str(cur_gene.seg_end) + "\t"
                to_write += str(cur_gene.seg_length) + "\t"
                to_write += str(cur_gene.cf) + "\t"
                to_write += str(cur_gene.tcn) + "\t"
                to_write += str(cur_gene.lcn) + "\t"
                to_write += str(cur_gene.cn_state) + "\t"
                to_write += str(cur_gene.filter) + "\t"
                to_write += str(cur_gene.tsg) + "\t"
                to_write += str(cur_gene.seg) + "\t"
                to_write += str(cur_gene.median_cnlr_seg) + "\t"
                to_write += str(cur_gene.segclust) + "\t"
                to_write += str(cur_gene.mcn) + "\t"
                to_write += str(cur_gene.genes_on_seg) + "\t"
                to_write += str(cur_gene.gene_snps) + "\t"
                to_write += str(cur_gene.gene_het_snps) + "\t"
                to_write += str(cur_gene.spans_segs)
                to_write += "\n"

    return to_write



if gene != "NA" :
    to_write = get_selected_genes(True, True, sampleID, [gene], dataDir)

    print("To write:")
    print(to_write)
    if to_write == '' :
        print("Is empty")
        to_write = str(sampleID) + "\t" + gene + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n"
        print(to_write)
    with open(outFile, 'a') as outfile:
        outfile.write(to_write)
else :
    with open(outFile, 'a') as outfile:
        outfile.write(sampleID + "\tNo_genes_above_ECHO_amplification_threshold\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n")


