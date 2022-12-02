import sys
from mt_metrics_eval import data
import statistics
import math

mode = sys.argv[1]

evs = data.EvalSet('wmt20', 'en-iu', read_stored_metric_scores=True)

human_scores = dict()
hs=[]
if (mode == "wmt20"):
    human_scores = evs.Scores('sys', 'wmt-z')
    for sc in human_scores:
        hs.append(human_scores[sc][0])
else:
    rankings = sys.argv[2]
    RNK = open(rankings,"r")
    lines = RNK.readlines()
    for line in lines[1:]:
        f = line.strip().split(" ")
        if (len(f) > 2) and (f[-1] not in ["Human-A.0", "zlabs-nlp.49"]):
            human_scores[f[-1]]=[float(f[-2])]
            hs.append(float(f[-2]))
            
qm_sys = set(human_scores) - evs.human_sys_names

#determin outliers
med = statistics.median(hs)
mad = 1.483 * statistics.median([math.fabs(s-med) for s in hs])

outliers=set()
for s in qm_sys:
    if (math.fabs(human_scores[s][0]-med)/mad) > 2.5:
        outliers.add(s)

qm_out = qm_sys - outliers

metric_scores=dict()
print("Metrics\t    all   -out")
for m in sorted(evs.metric_names):
    if evs.Scores('seg', scorer=m) is not None:
        for s in qm_sys:
            seg_scores=[]
            if (mode == "hansard"):
                seg_scores = evs.Scores('seg', scorer=m)[s][0:1566]
            elif (mode == "news" or mode == "wmt20"):
                seg_scores = evs.Scores('seg', scorer=m)[s][1566:]
            else:
                for sid in annotated[s]:
                    seg_scores.append(evs.Scores('seg', scorer=m)[s][sid])
            metric_scores[s]=[sum(seg_scores)/len(seg_scores)]
        syscorr = evs.Correlation(human_scores, metric_scores, qm_sys)
        noout   = evs.Correlation(human_scores, metric_scores, qm_out)
        print(m, "\t", "{:>7.3f}".format(syscorr.Pearson()[0]), "{:>7.3f}".format(noout.Pearson()[0]))
