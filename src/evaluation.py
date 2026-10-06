import numpy as np
from sklearn.metrics import adjusted_rand_score

def pairwise_ari(label_runs):
    """Return all pairwise adjusted Rand indices for repeated clusterings."""
    return np.array([
        adjusted_rand_score(label_runs[i], label_runs[j])
        for i in range(len(label_runs))
        for j in range(i + 1, len(label_runs))
    ])
