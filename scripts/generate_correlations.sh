#!/bin/bash

data_dir="$(dirname $(dirname $(realpath $0)) )/data/metrics"
scripts_dir="$(dirname $(realpath $0))"

bash $scripts_dir/generate_metrics_input.sh
python $scripts_dir/generate_syscorr.py wmt20                                                             > wmt20_syscorr.pearson
python $scripts_dir/generate_syscorr.py hansard   $data_dir/Hansard-ranking.txt                           > Hansard_syscorr.pearson
python $scripts_dir/generate_syscorr.py news      $data_dir/News-ranking.txt                              > News_syscorr.pearson

python $scripts_dir/generate_segcorr.py wmt20                                                             > wmt20_segcorr.kendall
python $scripts_dir/generate_segcorr.py all     < $data_dir/Hansard-metrics.tsv                           > Hansard_segcorr.kendall
python $scripts_dir/generate_segcorr.py all     < $data_dir/News-metrics.tsv                              > News_segcorr.kendall
cat $data_dir/Hansard-metrics.tsv $data_dir/News-metrics.tsv | python generate_segcorr.py all > all_segcorr.kendall
