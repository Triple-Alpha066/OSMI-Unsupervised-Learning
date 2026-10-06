import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    adjusted_rand_score,
)

def kmeans_stability(X, k_values=range(2, 9), seeds=range(10), n_init=50):
    """Evaluate K-Means stability across K and random seeds."""
    rows = []
    best_labels = {}

    for k in k_values:
        labels_runs, silhouettes, dbs = [], [], []

        for seed in seeds:
            model = KMeans(n_clusters=k, n_init=n_init, random_state=seed)
            labels = model.fit_predict(X)
            labels_runs.append(labels)
            silhouettes.append(silhouette_score(X, labels))
            dbs.append(davies_bouldin_score(X, labels))

        aris = [
            adjusted_rand_score(labels_runs[i], labels_runs[j])
            for i in range(len(labels_runs))
            for j in range(i + 1, len(labels_runs))
        ]

        best_idx = int(np.argmax(silhouettes))
        sizes = np.bincount(labels_runs[best_idx])
        best_labels[k] = labels_runs[best_idx]

        rows.append({
            "k": k,
            "Silhouette mean": np.mean(silhouettes),
            "Silhouette SD": np.std(silhouettes),
            "Davies-Bouldin mean": np.mean(dbs),
            "Pairwise ARI mean": np.mean(aris),
            "Min cluster": sizes.min(),
            "Max cluster": sizes.max(),
            "Best-run cluster sizes": ",".join(map(str, sorted(sizes))),
        })

    return pd.DataFrame(rows), best_labels

def fit_final_kmeans(X, k=2, random_state=42, n_init=50):
    """Fit the selected deterministic K-Means model."""
    model = KMeans(n_clusters=k, n_init=n_init, random_state=random_state)
    labels = model.fit_predict(X)
    return model, labels

def evaluate_labels(X, labels):
    return {
        "silhouette": silhouette_score(X, labels),
        "davies_bouldin": davies_bouldin_score(X, labels),
    }

def compare_gmm(X, component_values=range(2, 7), random_state=42):
    rows = []
    for n in component_values:
        model = GaussianMixture(
            n_components=n,
            covariance_type="diag",
            random_state=random_state,
        )
        labels = model.fit_predict(X)
        rows.append({
            "components": n,
            "AIC": model.aic(X),
            "BIC": model.bic(X),
            "silhouette": silhouette_score(X, labels),
            "davies_bouldin": davies_bouldin_score(X, labels),
        })
    return pd.DataFrame(rows)

def compare_hierarchical(X, k_values=range(2, 9)):
    rows = []
    for k in k_values:
        model = AgglomerativeClustering(n_clusters=k, linkage="ward")
        labels = model.fit_predict(X)
        sizes = np.bincount(labels)
        rows.append({
            "k": k,
            "silhouette": silhouette_score(X, labels),
            "davies_bouldin": davies_bouldin_score(X, labels),
            "min_cluster": sizes.min(),
            "max_cluster": sizes.max(),
        })
    return pd.DataFrame(rows)


def hierarchical_on_pca(X, n_components=20, k_values=range(2, 9)):
    """Evaluate Ward hierarchical clustering on a PCA representation."""
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    pca = PCA(n_components=min(n_components, X.shape[1], X.shape[0]))
    Z = pca.fit_transform(X)

    rows = []
    labels_by_k = {}
    for k in k_values:
        model = AgglomerativeClustering(n_clusters=k, linkage="ward")
        labels = model.fit_predict(Z)
        sizes = np.bincount(labels)
        rows.append({
            "k": k,
            "silhouette": silhouette_score(Z, labels),
            "davies_bouldin": davies_bouldin_score(Z, labels),
            "min_cluster": sizes.min(),
            "max_cluster": sizes.max(),
        })
        labels_by_k[k] = labels
    return pd.DataFrame(rows), labels_by_k, pca, Z

