"""Reproduce the survey-routing stress test used in the case study."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.config import DATA_PATH, RESULTS_DIR

SELF = "Are you self-employed?"
AGE = "What is your age?"

def main():
    df = pd.read_csv(DATA_PATH)
    out = RESULTS_DIR / "tables"
    out.mkdir(parents=True, exist_ok=True)
    cols = [c for c in df.columns if c not in {AGE}]
    frame = df[cols].copy()
    # Keep only columns with at least one observed value and encode categoricals.
    frame = frame.fillna("Missing/Not reported").astype(str)
    X = pd.get_dummies(frame, drop_first=False)
    model = KMeans(n_clusters=2, n_init=50, random_state=42)
    labels = model.fit_predict(X)
    counts = pd.Series(labels).value_counts().sort_index()
    self_counts = df[SELF].fillna("Missing/Not reported").astype(str).value_counts()
    result = pd.DataFrame({
        "Cluster": counts.index + 1,
        "N": counts.values,
        "Share": counts.values / len(df),
    })
    result.to_csv(out / "routing_stress_test.csv", index=False)
    pd.DataFrame({"Self-employed response": self_counts.index, "N": self_counts.values}).to_csv(
        out / "self_employment_distribution.csv", index=False
    )
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()
