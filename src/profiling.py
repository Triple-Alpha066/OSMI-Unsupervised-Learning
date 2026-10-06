import pandas as pd

def cluster_sizes(labels):
    counts = pd.Series(labels).value_counts().sort_index()
    return pd.DataFrame({
        "Cluster": counts.index + 1,
        "N": counts.values,
        "Share": counts.values / len(labels),
    })

def profile_modes(frame, labels):
    rows = []
    labels = pd.Series(labels, index=frame.index)
    for column in frame.columns:
        for cluster in sorted(labels.unique()):
            values = frame.loc[labels.eq(cluster), column]
            counts = values.value_counts(normalize=True)
            rows.append({
                "Variable": column,
                "Cluster": int(cluster) + 1,
                "N": int(values.shape[0]),
                "Modal response": counts.index[0],
                "Modal share": float(counts.iloc[0]),
            })
    return pd.DataFrame(rows)
