#!/bin/bash

data_dir="$(dirname $(dirname $(realpath $0)) )/data"
scripts_dir="$(dirname $(realpath $0))"
out_dir=$data_dir/metrics
mkdir -p $out_dir

# Generate Hansard ranking (Table 3):
# Note that the "-b" flag is optional in this case, as the Hansard contains no BAD references
python3 $scripts_dir/generate_ranking.py -i $data_dir/Hansard-A.csv $data_dir/Hansard-B.csv -s annotator -b > $out_dir/Hansard-ranking.txt

python3 $scripts_dir/generate_metrics_input.py -i $data_dir/Hansard-A.csv $data_dir/Hansard-B.csv > $out_dir/Hansard-metrics.tsv

# Generate the News ranking (Table 4), using only annotations of SRPOL for z-score calculations
python3 $scripts_dir/generate_ranking.py -i $data_dir/News-WMT20DocSrcDA.csv $data_dir/News-WMT20DocSrcDA2.csv -s annotator -b -z Human-A.0 CUNI-Transfer.1009 NICT_Kyoto.1219 NRC.715 MultiLingual_Engine_Ubiqus.525 Facebook_AI.1465 Helsinki.992 Groningen.1392 UQAM_TanLe.521 UEDIN.1281 OPPO.722 zlabs-nlp.49 > $out_dir/News-ranking.txt

python3 $scripts_dir/generate_metrics_input.py -i $data_dir/News-WMT20DocSrcDA.csv $data_dir/News-WMT20DocSrcDA2.csv > $out_dir/News-metrics.tsv
