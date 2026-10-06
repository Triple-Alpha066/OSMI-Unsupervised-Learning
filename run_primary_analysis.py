import sys
from pathlib import Path
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import FIGURES_DIR, TABLES_DIR
from src.data_loader import load_osmi_data
from src.feature_engineering import build_universal_core_matrix
from src.clustering import (
    kmeans_stability,
    fit_final_kmeans,
    evaluate_labels,
    compare_gmm,
    hierarchical_on_pca,
)
from src.profiling import cluster_sizes, profile_modes
from src.visualization import plot_pca_clusters

def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_osmi_data()
    frame, X_df, encoder, used_variables = build_universal_core_matrix(df)
    X = X_df.to_numpy()

    # K-Means stability and final model.
    sweep, _ = kmeans_stability(X, k_values=range(2, 9), seeds=range(10), n_init=50)
    model, labels = fit_final_kmeans(X, k=2, random_state=42, n_init=50)
    metrics = evaluate_labels(X, labels)

    # GMM comparison.
    gmm = compare_gmm(X, component_values=range(2, 7), random_state=42)

    # Independent Ward cross-check on PCA-20.
    hierarchical, h_labels, pca20, Z20 = hierarchical_on_pca(X, n_components=20)

    # PCA diagnostic on the encoded representation.
    # Age is standardized during feature engineering; one-hot variables remain binary.
    pca = PCA(n_components=min(30, X.shape[1]))
    Z = pca.fit_transform(X)

    plot_pca_clusters(
        Z[:, :2],
        labels,
        pca.explained_variance_ratio_,
        FIGURES_DIR / "primary_k2_pca.png",
    )

    sizes = cluster_sizes(labels)
    profiles = profile_modes(frame.fillna("Missing/Not reported"), labels)

    # Record PCA variance.
    pca_variance = pd.DataFrame({
        "Component": range(1, len(pca.explained_variance_ratio_) + 1),
        "Explained variance ratio": pca.explained_variance_ratio_,
        "Cumulative": pca.explained_variance_ratio_.cumsum(),
    })

    pd.DataFrame({"Variable": used_variables}).to_csv(
        TABLES_DIR / "primary_variables.csv", index=False
    )
    sweep.to_csv(TABLES_DIR / "primary_kmeans_stability.csv", index=False)
    gmm.to_csv(TABLES_DIR / "primary_gmm_comparison.csv", index=False)
    hierarchical.to_csv(TABLES_DIR / "primary_hierarchical_pca20.csv", index=False)
    sizes.to_csv(TABLES_DIR / "primary_cluster_sizes.csv", index=False)
    profiles.to_csv(TABLES_DIR / "primary_cluster_profiles.csv", index=False)
    pca_variance.to_csv(TABLES_DIR / "primary_pca_variance.csv", index=False)

    print("OSMI Primary Unsupervised ML Analysis")
    print(f"Respondents: {len(df)}")
    print(f"Encoded features: {X.shape[1]}")
    print(f"Variables used: {len(used_variables)}")
    print(f"Final K: 2")
    print(f"Silhouette: {metrics['silhouette']:.4f}")
    print(f"Davies-Bouldin: {metrics['davies_bouldin']:.4f}")
    print(sizes.to_string(index=False))

if __name__ == "__main__":
    main()
