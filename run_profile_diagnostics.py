"""Reproduce primary cluster profile statistics and differentiator table/figure."""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import DATA_PATH, RESULTS_DIR
from src.feature_engineering import build_universal_core_matrix
from src.clustering import fit_final_kmeans

KEY_VARIABLES = [
    "Have you had a mental health disorder in the past?",
    "Do you currently have a mental health disorder?",
    "Have you been diagnosed with a mental health condition by a medical professional?",
    "Have you ever sought treatment for a mental health issue from a mental health professional?",
    "Do you have a family history of mental illness?",
    "If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?",
    "If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?",
    "Do you feel that being identified as a person with a mental health issue would hurt your career?",
    "Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?",
    "How willing would you be to share with friends and family that you have a mental illness?",
    "Would you bring up a mental health issue with a potential employer in an interview?",
    "Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?",
]

def main():
    df = pd.read_csv(DATA_PATH)
    frame, X_df, _, _ = build_universal_core_matrix(df)
    _, labels = fit_final_kmeans(X_df.to_numpy(), k=2, random_state=42, n_init=50)
    labels_s = pd.Series(labels, index=df.index)
    rows = []
    for col in KEY_VARIABLES:
        if col not in frame.columns:
            continue
        values = frame[col].fillna("Missing/Not reported").astype(str)
        shares = pd.crosstab(values, labels_s, normalize="columns")
        for response in shares.index:
            c1 = float(shares.loc[response].get(0, 0.0))
            c2 = float(shares.loc[response].get(1, 0.0))
            rows.append({"Variable": col, "Response": response, "Cluster 1 share": c1, "Cluster 2 share": c2, "Absolute difference": abs(c1-c2)})
    result = pd.DataFrame(rows).sort_values("Absolute difference", ascending=False)
    out = RESULTS_DIR / "tables"
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / "primary_profile_differences.csv", index=False)

    age = pd.to_numeric(df["What is your age?"], errors="coerce").where(lambda s: s.between(18,80))
    age_summary = pd.DataFrame({
        "Cluster": [1,2],
        "N": [int((labels_s==0).sum()), int((labels_s==1).sum())],
        "Mean age": [float(age[labels_s==0].mean()), float(age[labels_s==1].mean())],
        "Median age": [float(age[labels_s==0].median()), float(age[labels_s==1].median())],
        "SD age": [float(age[labels_s==0].std()), float(age[labels_s==1].std())],
    })
    age_summary.to_csv(out / "primary_age_summary.csv", index=False)

    top = result.drop_duplicates("Variable").sort_values("Absolute difference", ascending=False).head(10).iloc[::-1]
    plt.figure(figsize=(8,5.2))
    plt.barh([v[:55] for v in top["Variable"]], top["Absolute difference"])
    plt.xlabel("Absolute difference in response share")
    plt.ylabel("Survey variable")
    plt.title("Strongest differentiators of the primary two-cluster solution")
    plt.tight_layout()
    fig = RESULTS_DIR / "figures" / "primary_cluster_differentiators.png"
    fig.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig, dpi=220, bbox_inches="tight")
    plt.close()
    print(age_summary.to_string(index=False))
    print(result.head(15).to_string(index=False))

if __name__ == "__main__":
    main()
