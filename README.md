# OSMI Mental Health in Tech 2016 — Unsupervised Learning & Feature Engineering

## Overview

This repository contains the reproducible Python implementation for an unsupervised-machine-learning case study based on the **OSMI Mental Health in Tech Survey 2016**.

The analysis investigates whether survey respondents can be grouped into interpretable profiles relevant to mental-health history, disclosure, stigma, work impact and workplace support.

The project deliberately separates:

- **Primary respondent segmentation** — mental-health experience, disclosure, stigma and work impact.
- **Secondary workplace-support segmentation** — current workplace-support conditions among non-self-employed respondents.

The analysis is descriptive. It is **not a clinical diagnostic system** and does not make causal claims.

## Dataset

The source dataset contains **1,433 respondents** and **63 original survey variables**. The raw CSV is intentionally excluded from the repository. Place it at:

```text
data/mental-heath-in-tech-2016_20161114.csv
```

## Analytical workflow

```text
Raw survey data
      ↓
Data audit
      ↓
Routing stress test
      ↓
Feature engineering
      ↓
Categorical encoding + explicit missingness handling
      ↓
K-Means stability analysis
      ↓
GMM comparison
      ↓
Ward hierarchical cross-check
      ↓
PCA diagnostic analysis
      ↓
Cluster profiling + age diagnostics
      ↓
Figures + tables
      ↓
Interpretation + critical reflection
```

## Primary representation

The primary representation contains **15 respondent-level survey variables plus age**. The 15 categorical variables cover mental-health history/status, diagnosis, treatment, disclosure, stigma, work interference, family history and remote work. Employer-routing variables are excluded because a preliminary broad representation reproduced the self-employed versus non-self-employed survey pathway.

Categorical variables are one-hot encoded. Missing categorical responses are represented explicitly as `Missing/Not reported`. Age is treated separately: values outside **18–80** are treated as missing, median-imputed and standardized. **The complete 58-feature matrix is not globally standardized; only age is standardized.** Free-text responses, gender, geography and raw multi-response work-position strings are not used as baseline clustering inputs.

The resulting representation contains **58 encoded features**. Approximately 72.41% of the encoded entries are zero-valued, reflecting the categorical and sparse response structure.

## Primary model

K-Means is evaluated for K=2–8 using **10 random seeds** and `n_init=50`. The retained deterministic model uses `random_state=42`.

Final K=2 results:

- Respondents: **1,433**
- Encoded features: **58**
- Cluster sizes: **788 / 645**
- Silhouette: **0.1536**
- Davies–Bouldin: **2.2557**
- Mean pairwise ARI across the 10-seed stability runs: **0.9977**
- First two PCA components: **28.73%** of variance
- First 20 PCA components: **82.74%** of variance

The relatively modest Silhouette Score is explicitly acknowledged. The clusters are interpreted as broad respondent contrasts rather than sharply separated natural populations.

## Alternative models

Gaussian Mixture Models with **diagonal covariance** are evaluated for 2–6 components using AIC, BIC, Silhouette and Davies–Bouldin metrics. Ward hierarchical clustering is evaluated for K=2–8 on a PCA-20 representation as an independent structural cross-check.

## Workplace-support model

The secondary analysis is restricted to **1,146 non-self-employed respondents** and uses **13 workplace-support/stigma variables**, producing **45 encoded features**. Previous-employer-specific and routing variables are excluded, while the substantive item concerning an unsupportive response in a current or previous workplace is retained because it measures an outcome rather than routing structure.

Results:

- K=2
- Silhouette: **0.1021**
- Davies–Bouldin: **2.8210**
- Mean pairwise ARI: **1.0000**
- Cluster sizes: **670 / 476**

The workplace-support clusters are treated as intervention-oriented contrasts because their internal separation is weak.

## Reproducibility outputs

The repository includes the analytical outputs needed to audit the case study, including:

- K-Means stability tables
- GMM comparison tables
- Ward/PCA comparison tables
- primary and workplace cluster profiles
- routing stress-test output
- age summary statistics
- primary cluster differentiator table and figure
- PCA cluster figures
- K-Means validation figure

The raw survey CSV remains excluded because it is the supplied source dataset rather than a distributable project artefact.

## Repository structure

```text
OSMI_Unsupervised_Learning/
├── README.md
├── requirements.txt
├── .gitignore
├── run_all.py
├── run_routing_stress_test.py
├── run_primary_analysis.py
├── run_profile_diagnostics.py
├── run_workplace_analysis.py
│
├── data/
│   └── README.md
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── clustering.py
│   ├── evaluation.py
│   ├── profiling.py
│   └── visualization.py
│
├── notebooks/
│   └── 01_osmi_reproducible_analysis.ipynb
│
├── results/
│   ├── figures/
│   └── tables/
│
└── docs/
    ├── methodology.md
    ├── model_selection.md
    └── limitations_and_critical_reflection.md
```

## Reproduction

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the source CSV in `data/`, then run:

```bash
python run_all.py
python run_routing_stress_test.py
python run_profile_diagnostics.py
```

The scripts write tables to `results/tables/` and figures to `results/figures/`.

## Scientific interpretation

The analysis does not claim that K-Means has discovered objectively existing psychological categories. The clusters are statistical summaries of response patterns that may support organizational thinking. Stable assignments do not imply strong substantive separation. Cluster membership must not be used for recruitment, promotion, termination, performance ranking, clinical diagnosis or automated psychological intervention.
