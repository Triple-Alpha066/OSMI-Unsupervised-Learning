import pandas as pd
from .config import DATA_PATH

def load_osmi_data(path=DATA_PATH):
    """Load the OSMI Mental Health in Tech Survey 2016 dataset."""
    return pd.read_csv(path)

def basic_audit(df):
    """Return basic dataset dimensions and missingness information."""
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
    }
