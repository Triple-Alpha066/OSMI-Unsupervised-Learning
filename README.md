# OSMI Mental Health in Tech 2016 — Unsupervised Learning & Feature Engineering

## Overview

This repository contains the reproducible Python implementation for an unsupervised machine learning case study based on the **OSMI Mental Health in Tech Survey 2016**.

The analysis investigates whether survey respondents can be grouped into interpretable profiles relevant to mental-health stigma, disclosure, work impact, and workplace support.

The project deliberately separates:

- **Primary respondent segmentation** — mental-health experience, stigma, disclosure, and work impact.
- **Secondary workplace-support segmentation** — current workplace-support conditions among non-self-employed respondents.

The analysis is descriptive. It is **not a clinical diagnostic system** and does not make causal claims.

---

## Dataset

The source dataset contains:

- **1,433 respondents**
- **63 original survey variables**

The raw CSV is intentionally excluded from this repository.

Place the file at:

```text
data/mental-heath-in-tech-2016_20161114.csv
```

---

## Analytical workflow

```text
Raw survey data
      ↓
Data audit
      ↓
Feature engineering
      ↓
Categorical encoding + missingness handling
      ↓
Representation stress testing
      ↓
K-Means stability analysis
      ↓
GMM comparison
      ↓
Hierarchical clustering cross-check
      ↓
PCA diagnostic analysis
      ↓
Cluster profiling
      ↓
Interpretation + critical reflection
```

---

## Primary model

The primary representation contains 15 mental-health/stigma/work-impact variables and age.

After feature engineering:

- Respondents: **1,433**
- Encoded features: **58**
- Selected K: **2**
- Silhouette: **0.1536**
- Davies–Bouldin: **2.2557**
- Cluster sizes: **788 / 645**

The first two PCA components explain approximately **28.73%** of total variance.

The relatively modest Silhouette Score is explicitly acknowledged. The clusters are interpreted as broad respondent contrasts rather than sharply separated natural populations.

---

## Workplace-support model

The secondary analysis is restricted to:

- **1,146 non-self-employed respondents**
- **45 encoded features**
- **K=2**

Results:

- Silhouette: **0.1021**
- Davies–Bouldin: **2.8210**
- Cluster sizes: **670 / 476**

The workplace-support clusters are treated as intervention-oriented contrasts because their internal separation is weak.

---

## Methods

The repository implements:

- K-Means clustering
- Gaussian Mixture Models
- Ward hierarchical clustering
- Silhouette Score
- Davies–Bouldin Index
- Adjusted Rand Index
- Principal Component Analysis
- cluster profiling

K-Means is evaluated for K=2–8 using repeated random seeds and `n_init=50`.

Model selection considers multiple criteria rather than optimizing a single metric.

---

## Important methodological decision

A major representation risk was identified during development: employer-related survey variables can contain structural missingness for self-employed respondents.

A preliminary representation produced a cluster split matching self-employment status exactly. This was treated as a methodological red flag.

The final design therefore:

1. excludes problematic employer-routing variables from the primary segmentation; and
2. performs workplace-support analysis separately among non-self-employed respondents.

This makes the analytical pipeline more defensible and more closely aligned with the substantive case objective.

---

## Repository structure

```text
OSMI_Unsupervised_Learning/
├── README.md
├── requirements.txt
├── .gitignore
├── run_all.py
├── run_primary_analysis.py
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

---

## Reproduction

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the source CSV in `data/`.

Run the complete analysis:

```bash
python run_all.py
```

The generated tables are written to:

```text
results/tables/
```

and figures to:

```text
results/figures/
```

---

## Scientific interpretation

The analysis does not claim that K-Means has discovered objectively existing psychological categories.

Instead, the clusters are treated as statistical summaries of response patterns that may support organizational thinking.

The relatively modest internal separation, self-report nature of the survey, cross-sectional design, potential response bias, and sensitivity to feature representation are explicitly considered in the final interpretation.

See:

- `docs/methodology.md`
- `docs/model_selection.md`
- `docs/limitations_and_critical_reflection.md`

for the full methodological rationale.
