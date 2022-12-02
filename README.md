## MT System Rankings for WMT20 English-Inuktitut
This repository contains code and data for replicating rankings and correlations in the paper [Test Set Sampling Affects System Rankings: Expanded Human Evaluation of WMT20 English-Inuktitut Systems](https://www.statmt.org/wmt22/pdf/2022.wmt-1.8.pdf) by Rebecca Knowles and Chi-kiu Lo.

## Requirements
This code relies on SciPy (https://www.scipy.org), NumPy (https://numpy.org/), and MT Metrics Eval (https://github.com/google-research/mt-metrics-eval). Please follow the libraries' instructions for installation. For MT Metrics Eval, please also follow the instruction to download the database.

## Data
The data in this repository includes News data annotations (already publicly available from [WMT20](https://www.statmt.org/wmt20/results.html)) as well as additional annotations of Hansard data.
For details, see the [DATA-README](data/DATA-README.md).

## Code

### System Rankings
To reproduce the system rankings shown in Tables 3 and 4 of the paper, run `scripts/generate_rankings.sh`. The result should match the contents of the file `scripts/example_rankings.txt`. To match the clusterings exactly, you may need to use scipy version <=1.6.2 (note that this differs from the metric correlations code, which may run with newer versions of scipy).

### Metric Correlations
To reproduce the metrics correlation shown in Tables 6 and 7 of the paper, run `scripts/generate_correlations.sh`. The result should match the contents of the files `scripts/*.pearson` and `scripts/*.kendall`.

## Copyright
Multilingual Text Processing / Traitement multilingue de textes

Digital Technologies Research Centre / Centre de recherche en technologies numériques

National Research Council Canada / Conseil national de recherches Canada

Copyright 2022, Sa Majesté le Roi du Chef du Canada / His Majesty the King in Right of Canada

Published under the GPL v3.0 License (see [LICENSE](LICENSE)).

## Cite
If you use this code, you may wish to cite:

```
@InProceedings{knowles-lo:2022:WMT,
  author    = {Knowles, Rebecca  and  Lo, Chi-kiu},
  title     = {Test Set Sampling Affects System Rankings: Expanded Human Evaluation of {WMT20} {E}nglish-{I}nuktitut Systems},
  booktitle      = {Proceedings of the Seventh Conference on Machine Translation},
  month          = {December},
  year           = {2022},
  address        = {Abu Dhabi},
  publisher      = {Association for Computational Linguistics},
  pages     = {140--153},
  url       = {https://aclanthology.org/2022.wmt-1.8}
}
```
