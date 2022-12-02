#!/usr/bin/env python3

# Generate metrics input (tab-separated System name, metrics ID, and DA score) from DA annotation files.

# Copyright 2022, National Research Council Canada

import sys
import argparse

parser = argparse.ArgumentParser(description="Produce system+metrics id+DA score input for metric correlations.")

parser.add_argument("-i", "--input", type=str, nargs="+", help="Input files.", required=True)

args=parser.parse_args()

inputdocs = args.input

iddict={}

with open("../data/segment_id_mapping.tsv") as f:
    for line in f:
        _,_,_,d,s,m=line.strip().split()
        iddict[(d,s)]=int(m)

for inpdoc in inputdocs:
    with open(inpdoc) as f:
        for l in f:
            annotator,hitid,system,segid,itemtype,src,tgt,score,docid,docscore,start,end = l.strip().split(",")
            if itemtype=="TGT" and docscore=="False":
                metricsid=str(iddict[(docid,segid)])
                print("\t".join([system, metricsid, score]))
