# Case Study / Repository Consistency Record

The canonical case-study report is based on the current repository pipeline rather than the earlier model-comparison workbook.

| Item | Canonical result |
|---|---:|
| Respondents | 1,433 |
| Original variables | 63 |
| Primary encoded features | 58 |
| Primary K | 2 |
| Primary cluster sizes | 788 / 645 |
| Primary silhouette | 0.1536 |
| Primary Davies–Bouldin | 2.2557 |
| Primary mean pairwise ARI | 0.9977 |
| Primary PCA first 2 | 28.73% |
| Primary PCA first 20 | 82.74% |
| Workplace-support respondents | 1,146 |
| Workplace-support features | 45 |
| Workplace-support K | 2 |
| Workplace-support silhouette | 0.1021 |
| Workplace-support Davies–Bouldin | 2.8210 |
| Workplace-support mean pairwise ARI | 1.0000 |
| Workplace-support cluster sizes | 670 / 476 |

Methodological wording is synchronized with the implementation: categorical variables are one-hot encoded, age is cleaned to 18–80, median-imputed and standardized, while the binary one-hot features are not globally standardized. GMM uses diagonal covariance. K-Means stability uses 10 random seeds with `n_init=50`.
