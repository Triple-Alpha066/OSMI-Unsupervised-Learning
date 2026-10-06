# Methodology

## 1. Analytical objective

The analysis investigates whether the OSMI Mental Health in Tech Survey 2016 contains interpretable respondent groupings that can support organizational mental-health and workplace-support decision-making.

The analysis deliberately distinguishes between:

1. a **primary respondent segmentation**, based on mental-health experience, disclosure, stigma and work-related impact; and
2. a **secondary workplace-support segmentation**, restricted to respondents for whom current-employer questions are applicable.

The purpose is not clinical diagnosis or prediction. Clusters are descriptive analytical segments.

## 2. Data preparation

The source survey contains 1,433 respondents and 63 original variables.

Categorical survey responses are represented using one-hot encoding. Missing categorical responses are retained as an explicit `Missing/Not reported` category rather than silently discarded.

Age is treated numerically. Values outside the plausibility range of 18–80 are treated as missing, median-imputed, and standardized.

Free-text responses, gender, geography, and raw multi-response work-position strings are not used as baseline clustering inputs. This reduces the risk that high-cardinality text or demographic/geographic structure dominates the unsupervised representation.

## 3. Primary representation

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

Employer-routing variables that could create structural missingness are excluded from the primary representation.

The resulting matrix contains 1,433 respondents and 58 encoded features.

## 4. Clustering methods

Three unsupervised approaches are considered:

### K-Means

K-Means is evaluated for K=2 through K=8. Each K is fitted repeatedly using 10 random seeds with `n_init=50`.

Stability is assessed using pairwise Adjusted Rand Index (ARI).

### Gaussian Mixture Models

Gaussian Mixture Models with diagonal covariance are evaluated for 2–6 components. AIC and BIC are considered alongside Silhouette Score and Davies–Bouldin Index.

### Hierarchical clustering

Ward hierarchical clustering is used as an independent cross-check. A PCA-20 representation is used for the Ward comparison to reduce dimensionality while retaining most of the structured variation.

## 5. Model evaluation

Model selection does not rely on one metric.

The analysis considers:

- Silhouette Score — higher is preferable;
- Davies–Bouldin Index — lower is preferable;
- repeated-run ARI — higher indicates greater stability;
- cluster-size balance;
- agreement with an independent clustering method;
- substantive interpretability;
- organizational actionability.

The primary K=2 solution provides the strongest internal separation among the tested K values, while also producing stable and reasonably sized groups.

The resulting primary clusters contain 788 and 645 respondents.

## 6. PCA

PCA is used as a diagnostic representation rather than as evidence that the data are inherently two-dimensional.

For the primary representation, the first two principal components explain approximately 28.73% of total variance.

Therefore, a PCA scatter plot is interpreted as a visual aid, not as proof of sharply separated natural populations.

## 7. Workplace-support analysis

The secondary analysis is restricted to 1,146 non-self-employed respondents.

It focuses on current workplace support and stigma variables, including employer-provided mental-health benefits, awareness of available care, formal employer communication, educational resources, anonymity, medical leave, perceived disclosure consequences, coworker/supervisor comfort, employer seriousness toward mental health, and observed negative consequences.

Previous-employer variables, self-employment routing variables, employer-type classification, and completely missing variables are excluded from the final representation.

The resulting workplace-support representation contains 45 encoded features.

K=2 again provides the strongest tested internal solution, but the Silhouette Score is only approximately 0.102. Consequently, these groups are interpreted as broad intervention-oriented contrasts rather than sharply separated natural employee types.

## 8. Interpretation principles

Clusters are not labelled as “healthy” versus “mentally ill”.

Mental-health variables are interpreted as reported survey characteristics rather than clinical diagnoses.

The analysis distinguishes statistical structure from organizational usefulness. A cluster can be mathematically stable while still having limited practical separation.

The results therefore support cautious segmentation and targeted organizational support, not individual clinical decisions.

## 9. Limitations

Important limitations include:

- cross-sectional survey design;
- self-reported responses;
- possible selection and response bias;
- structural missingness created by survey routing;
- modest cluster separation;
- sensitivity of unsupervised clustering to representation choices;
- no causal interpretation;
- no clinical validation;
- PCA explains only part of the total variation in its first two dimensions.

These limitations are incorporated into the final interpretation rather than hidden from the reader.
