import sys
from mt_metrics_eval import data

mode = sys.argv[1]

evs = data.EvalSet('wmt20', 'en-iu', read_stored_metric_scores=True)
n = len(evs.Scores('seg', 'wmt-raw')['NRC.715'])

human_scores = dict()
if (mode == "wmt20"):
    human_scores = evs.Scores('seg', 'wmt-raw')
else:
    for line in sys.stdin:
        f = line.strip().split("\t")
        if f[0] not in ["Human-A.0", "zlabs-nlp.49"]:
            if f[0] not in human_scores:
                segid = int(f[1])
                human_scores[f[0]]=[[] for i in range(n)]
                human_scores[f[0]][segid]=[float(f[2])]
            else:
                human_scores[f[0]][int(f[1])].append(float(f[2]))
    for s in human_scores:
        for i in range(n):
            if len(human_scores[s][i]) > 0:
                human_scores[s][i] = sum(human_scores[s][i]) / len(human_scores[s][i])
            else:
                human_scores[s][i] = None
    

qm_sys = set(human_scores) - evs.human_sys_names

metric_scores=dict()
for m in sorted(evs.metric_names):
    if evs.Scores('seg', scorer=m) is not None:
        for s in qm_sys:
            metric_scores[s] = evs.Scores('seg', scorer=m)[s]
        wmt = evs.Correlation(human_scores, metric_scores, qm_sys)
        print(m, "\t", "{:>7.3f}".format(wmt.KendallLike()[0]))
