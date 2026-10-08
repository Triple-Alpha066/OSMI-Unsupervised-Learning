# Methodology

## 1. Analytical objective

The analysis investigates whether the OSMI Mental Health in Tech Survey 2016 contains interpretable respondent groupings that can support organizational mental-health and workplace-support decision-making.

The analysis deliberately distinguishes between a **primary respondent segmentation** based on mental-health experience, disclosure, stigma and work-related impact, and a **secondary workplace-support segmentation** restricted to respondents for whom current-employer questions are applicable. The purpose is not clinical diagnosis or prediction.

## 2. Data preparation

The source survey contains 1,433 respondents and 63 original variables. Categorical survey responses are represented using one-hot encoding. Missing categorical responses are retained as an explicit `Missing/Not reported` category.

Age is treated numerically. Values outside the plausibility range of 18–80 are treated as missing, median-imputed, and standardized. The categorical one-hot features remain binary; the full 58-feature matrix is therefore **not** globally standardized.

Free-text responses, gender, geography and raw multi-response work-position strings are not used as baseline clustering inputs.

## 3. Routing stress test

A broad preliminary representation was evaluated specifically to identify whether survey-routing variables dominated the unsupervised structure. The resulting K=2 solution separated **1,146 non-self-employed respondents from 287 self-employed respondents**, closely reproducing the survey's employment-routing structure. This was treated as a methodological red flag rather than as the substantive target segmentation.

Employer-routing variables were consequently excluded from the primary universal representation.

## 4. Primary representation

The primary representation contains 15 survey variables covering:

- willingness to raise physical and mental-health issues with potential employers;
- perceived career consequences;
- perceived coworker stigma;
- willingness to share with friends and family;
- observed or experienced unsupportive workplace responses;
- whether observed disclosure affects willingness to disclose;
- family history;
- past and current mental-health disorder status;
- professional diagnosis;
- treatment seeking;
- work interference when treated effectively;
- work interference when not treated effectively;
- remote work.

The resulting matrix contains 1,433 respondents and 58 encoded features.

## 5. Clustering methods

### K-Means

K-Means is evaluated for K=2 through K=8. Each K is fitted across 10 random seeds using `n_init=50`. The final deterministic model uses `random_state=42`. Stability is assessed using pairwise Adjusted Rand Index (ARI).

### Gaussian Mixture Models

Gaussian Mixture Models with **diagonal covariance** are evaluated for 2–6 components. AIC and BIC are considered alongside Silhouette Score and Davies–Bouldin Index.

### Hierarchical clustering

Ward hierarchical clustering is used as an independent cross-check for K=2–8 on a PCA-20 representation. Because Ward is evaluated on a different representation, it is treated as corroborative evidence rather than as a directly interchangeable primary model.

## 6. Model evaluation

Model selection considers Silhouette Score, Davies–Bouldin Index, repeated-run ARI, cluster-size balance, independent-method agreement, substantive interpretability and organizational actionability.

For the primary representation, K=2 provides the strongest K-Means internal separation among the tested values and produces large, highly stable groups of 788 and 645 respondents. Its mean pairwise ARI across the 10-seed sweep is 0.9977.

## 7. PCA

PCA is used diagnostically rather than as evidence that the data are inherently two-dimensional. For the primary representation, the first two components explain approximately 28.73% of total variance and the first 20 explain approximately 82.74%.

## 8. Workplace-support analysis

The secondary analysis is restricted to 1,146 non-self-employed respondents. It focuses on current workplace support and stigma variables, including employer-provided mental-health benefits, awareness of available care, formal employer communication, educational resources, anonymity, medical leave, perceived disclosure consequences, coworker/supervisor comfort, employer seriousness toward mental health, and observed negative consequences.

Previous-employer-specific and routing variables are excluded. The substantive survey item asking about an unsupportive or badly handled response in a **current or previous workplace** is retained because it measures a support/stigma experience rather than determining survey routing.

The resulting workplace-support representation contains 45 encoded features. K=2 produces silhouette 0.1021, Davies–Bouldin 2.8210 and mean pairwise ARI 1.0000. Consequently, the groups are interpreted as broad intervention-oriented contrasts rather than sharply separated natural employee types.

## 9. Profiling and diagnostics

Primary cluster profiling is reproduced from the canonical K-Means K=2 labels. The repository generates response-share differences for the key mental-health, disclosure, stigma and work-impact variables, together with cluster-level age summaries. These outputs underpin the case-study tables and differentiator figure.

## 10. Interpretation principles

Clusters are not labelled as “healthy” versus “mentally ill”. Mental-health variables are interpreted as reported survey characteristics rather than clinical diagnoses. The analysis distinguishes statistical structure from organizational usefulness. A cluster can be mathematically stable while still having limited practical separation.

## 11. Limitations

Important limitations include cross-sectional survey design, self-reported responses, possible selection and response bias, structural missingness created by survey routing, modest cluster separation, sensitivity of unsupervised clustering to representation choices, no causal interpretation, no clinical validation, and the limited variance represented by two-dimensional PCA projections.
