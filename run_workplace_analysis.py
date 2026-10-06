import sys
from pathlib import Path

import pandas as pd
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.data_loader import load_osmi_data
from src.feature_engineering import build_workplace_support_matrix
from src.clustering import (
    kmeans_stability,
    fit_final_kmeans,
    evaluate_labels,
    compare_gmm,
    hierarchical_on_pca,
)
from src.profiling import cluster_sizes, profile_modes
from src.visualization import plot_pca_clusters
from src.config import FIGURES_DIR, TABLES_DIR

def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_osmi_data()
    subset, X_df, encoder, usable = build_workplace_support_matrix(df)
    X = X_df.to_numpy()

    sweep, _ = kmeans_stability(X, k_values=range(2, 9), seeds=range(10), n_init=50)
    model, labels = fit_final_kmeans(X, k=2, random_state=42, n_init=50)
    metrics = evaluate_labels(X, labels)

    # PCA is diagnostic only. The clustering remains in the encoded feature space.
    pca = PCA(n_components=min(20, X.shape[1]))
    Z = pca.fit_transform(X)

    plot_pca_clusters(
        Z[:, :2],
        labels,
        pca.explained_variance_ratio_,
        FIGURES_DIR / "workplace_support_k2_pca.png",
    )

    cluster_table = cluster_sizes(labels)
    profiles = profile_modes(
        subset[usable].fillna("Missing/Not reported"),
        labels
    )

    sweep.to_csv(TABLES_DIR / "workplace_kmeans_stability.csv", index=False)
    cluster_table.to_csv(TABLES_DIR / "workplace_cluster_sizes.csv", index=False)
    profiles.to_csv(TABLES_DIR / "workplace_cluster_profiles.csv", index=False)
    compare_gmm(
        X, component_values=range(2, 7), random_state=42
    ).to_csv(TABLES_DIR / "workplace_gmm_comparison.csv", index=False)

    hierarchical, _, _, _ = hierarchical_on_pca(
        X, n_components=20, k_values=range(2, 9)
    )
    hierarchical.to_csv(
        TABLES_DIR / "workplace_hierarchical_pca20.csv", index=False
    )

    pd.DataFrame({"Variable": usable}).to_csv(
        TABLES_DIR / "workplace_variables.csv", index=False
    )

    pca_variance = pd.DataFrame({
        "Component": range(1, len(pca.explained_variance_ratio_) + 1),
        "Explained variance ratio": pca.explained_variance_ratio_,
        "Cumulative": pca.explained_variance_ratio_.cumsum(),
    })
    pca_variance.to_csv(
        TABLES_DIR / "workplace_pca_variance.csv", index=False
    )

    print("OSMI Workplace Support Analysis")
    print(f"Respondents: {len(subset)}")
    print(f"Encoded features: {X.shape[1]}")
    print(f"Final K: 2")
    print(f"Silhouette: {metrics['silhouette']:.4f}")
    print(f"Davies-Bouldin: {metrics['davies_bouldin']:.4f}")
    print(cluster_table.to_string(index=False))

if __name__ == "__main__":
    main()
