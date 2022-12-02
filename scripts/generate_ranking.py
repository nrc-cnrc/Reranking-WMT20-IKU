#!/usr/bin/env python3

# Produce MT system rankings from human annotations.

# Copyright 2022, National Research Council Canada

import sys
from collections import defaultdict, namedtuple
from scipy import stats
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Produce MT system ranking.")

parser.add_argument("-i", "--input", type=str, nargs="+", help="Input files.", required=True)
parser.add_argument("-s", "--standardize", type=str, choices=["hit", "annotator", "none"], help="Standardize by hit, annotator, or no standardization.", required=True)
parser.add_argument("-z", "--z_score_removal", type=str, nargs="+", help="Remove systems when computing z-score means and standard deviations.", default=[])
parser.add_argument("-f", "--final_removal", type=str, nargs="+", help="Remove systems from final output.", default=[])
parser.add_argument("-b", "--bad_reference_removal", action="store_true", help="Remove 'BAD' ref. when computing z-scores.", default=False)
parser.add_argument("-a", "--annotator_removal", type=str, nargs="+", help="Annotators to remove.", default=[])

args=parser.parse_args()

Score = namedtuple('Score', ['hit', 'system', 'sid', 'score'])

def get_hit(annotator, hitid, standard):
    """
    Use annotator ID if standardizing by annotator; HIT ID otherwise
    """
    if standard == "annotator":
        hit = annotator
    else:
        hit = hitid
    return hit

def keep_score_z(s, segtype, z_removed_systems, remove_bad):
    """
    Determine whether segment should be used for z-score computation
    """
    if s not in z_removed_systems:
        if segtype == "BAD" and remove_bad:
            return False
        else:
            return True
    else:
        return False

def keep_seg(annotator, annotators_removed):
    """
    Determine whether segment should be kept (based on annotator removal)
    """
    if annotator in annotators_removed:
        return False
    else:
        return True

def average_duplicates(system_lst, s):
    """
    Input: the list of all scores (system_lst) for a given system (s)
    Output: lift of scores after averaging scores for duplicate sentence IDs
    """
    sids = set([x.sid for x in system_lst])
    deduped = []
    for sid in sids:
        sid_scores = [x for x in system_lst if x.sid == sid]
        hits = ",".join([x.hit for x in sid_scores])
        deduped.append(Score(hits, s, sid, np.mean([x.score for x in sid_scores])))
    return deduped

def main(args):
    inputdocs = args.input
    standard = args.standardize
    
    z_removed_systems = args.z_score_removal
    final_removed_systems = args.final_removal
    annotators_removed = args.annotator_removal
    remove_bad = args.bad_reference_removal

    all_hit_scores = defaultdict(list)
    scores = []
    zscores = []
    final_scores = []
    sys_scores = defaultdict(list)
    sys_z_scores = defaultdict(list)
    
    for inputdoc in inputdocs:
        with open(inputdoc) as f:
            """
            Extract the raw scores
            """
            for l in f:
                annotator,hitid,system,segid,itemtype,src,tgt,score,docid,docscore,start,end = l.strip().split(",")
                if docscore=="False":
                    # First remove any docscores
                    
                    hit = get_hit(annotator, hitid, standard) # Set HIT to annotator or hitid, as required
                    sid = "-".join([segid,docid])
                    score = float(score)
                    if keep_score_z(system, itemtype, z_removed_systems, remove_bad) and keep_seg(annotator, annotators_removed):
                        # Collect the scores needed to compute z-scores
                        all_hit_scores[hit].append(Score(hit, system, sid, float(score)))
                    if itemtype == "TGT" and keep_seg(annotator, annotators_removed):
                        # Collect all valid (TGT) scores
                        scores.append(Score(hit, system, sid, float(score)))

    # Get the set of "hits" (either annotators or annotation sessions, depending on choice of standardization)
    hits = set([x.hit for x in scores])
    
    # Get the set of systems
    systems = set([x.system for x in scores if x.system not in final_removed_systems])
    
    for hit in hits:
        """
        For each "hit" (annotator or annotation session/hit), get the score information (full_hit)
        And just the raw scores (hit_scores)
        Compute mu and std from all_hit_scores[hit] (may contain "BAD", as required)
        Compute z-scores using mu and std
        Collect all z-scores
        """
        full_hit = [x for x in scores if x.hit == hit]
        hit_scores = [x.score for x in scores if x.hit == hit]
        if standard != "none":
            hs = [x.score for x in all_hit_scores[hit]]
            mu, s = (np.mean(hs), np.std(hs, ddof=1))
            if s != 0 and s == s: #This checks for NaN s
                hit_z_scores = [(x-mu)/s for x in hit_scores]
                zscores += [Score(full_hit[i].hit, full_hit[i].system, full_hit[i].sid, hit_z_scores[i]) for i in range(len(full_hit))]
        else:
            hit_z_scores = [x for x in hit_scores]
            zscores += [Score(full_hit[i].hit, full_hit[i].system, full_hit[i].sid, hit_z_scores[i]) for i in range(len(full_hit))]

    for s in systems:
        """
        For each system s:
        Average any scores (raw or z-score) for segments that have been annotated multiple times
        Compute system averages
        """
        sys_scores[s] = average_duplicates([x for x in scores if x.system == s], s)
        sys_z_scores[s] = average_duplicates([x for x in zscores if x.system == s], s)
        final_scores.append((np.mean([x.score for x in sys_z_scores[s]]), np.mean([x.score for x in sys_scores[s]]), s))
    
    #Sort the systems by z-score
    sorted_systems = sorted(final_scores, reverse=True)

    print("   Ave.   Ave.z  System\n-----------------------------------------")
    for i in range(len(sorted_systems)):
        """
        Produce the ranking table, with significance lines between clusters
        where all systems below a given system are significantly worse than
        the given system.
        """
        z,raw,s = sorted_systems[i]
        print("{:>7.1f}".format(raw), "{:>7.3f}".format(z), s)
        n = 1
        max_sig = 0.0
        z_list = [x.score for x in sys_z_scores[s]]
        while i+n < len(sorted_systems) and max_sig < 0.5:
            next_z_list = [x.score for x in sys_z_scores[sorted_systems[i+n][2]]]
            sig = stats.mannwhitneyu(z_list,next_z_list)[1]
            if sig > max_sig:
                max_sig = sig
            n += 1
        if i+1 < len(sorted_systems):
            if max_sig < 0.001:
                print("----------------------------------------TT (0.001)")
            elif max_sig < 0.01:
                print("-----------------------------------------T (0.01)")
            elif max_sig < 0.05:
                print("-----------------------------------------X (0.05)")

if __name__ == "__main__":
        main(args)
