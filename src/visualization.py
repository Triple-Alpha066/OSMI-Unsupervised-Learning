import matplotlib.pyplot as plt

def plot_pca_clusters(Z, labels, explained_variance, output_path):
    """Save a two-dimensional PCA diagnostic plot."""
    plt.figure(figsize=(9, 7))

    for cluster in sorted(set(labels)):
        mask = labels == cluster
        plt.scatter(
            Z[mask, 0],
            Z[mask, 1],
            s=18,
            alpha=0.55,
            label=f"Cluster {cluster + 1} (n={mask.sum()})",
        )

    plt.xlabel(f"PC1 ({explained_variance[0] * 100:.1f}% variance)")
    plt.ylabel(f"PC2 ({explained_variance[1] * 100:.1f}% variance)")
    plt.title("OSMI Clustering — K-Means K=2 (PCA diagnostic)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=220)
    plt.close()
