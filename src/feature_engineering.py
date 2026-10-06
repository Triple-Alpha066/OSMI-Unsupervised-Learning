import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

SELF_EMPLOYED = "Are you self-employed?"

WORKPLACE_SUPPORT_VARIABLES = [
    "Does your employer provide mental health benefits as part of healthcare coverage?",
    "Do you know the options for mental health care available under your employer-provided coverage?",
    "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?",
    "Does your employer offer resources to learn more about mental health concerns and options for seeking help?",
    "Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?",
    "If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:",
    "Do you think that discussing a mental health disorder with your employer would have negative consequences?",
    "Do you think that discussing a physical health issue with your employer would have negative consequences?",
    "Would you feel comfortable discussing a mental health disorder with your coworkers?",
    "Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?",
    "Do you feel that your employer takes mental health as seriously as physical health?",
    "Have you heard of or observed negative consequences for co-workers who have been open about mental health issues in your workplace?",
    "Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?",
]

def clean_age(series):
    """Mark implausible ages outside 18–80 as missing."""
    age = pd.to_numeric(series, errors="coerce")
    return age.where(age.between(18, 80))

def build_workplace_support_matrix(df):
    """Build the cleaned current-workplace-support representation for non-self-employed respondents."""
    subset = df[df[SELF_EMPLOYED].eq(0)].copy()

    # Keep only variables that contain information in this population.
    usable = [c for c in WORKPLACE_SUPPORT_VARIABLES if c in subset.columns and subset[c].notna().any()]
    frame = subset[usable].fillna("Missing/Not reported").astype(str)

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X = encoder.fit_transform(frame)

    feature_names = encoder.get_feature_names_out(usable)
    X_df = pd.DataFrame(X, columns=feature_names, index=subset.index)

    return subset, X_df, encoder, usable


UNIVERSAL_CORE_VARIABLES = [
    "Would you be willing to bring up a physical health issue with a potential employer in an interview?",
    "Would you bring up a mental health issue with a potential employer in an interview?",
    "Do you feel that being identified as a person with a mental health issue would hurt your career?",
    "Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?",
    "How willing would you be to share with friends and family that you have a mental illness?",
    "Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?",
    "Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?",
    "Do you have a family history of mental illness?",
    "Have you had a mental health disorder in the past?",
    "Do you currently have a mental health disorder?",
    "Have you been diagnosed with a mental health condition by a medical professional?",
    "Have you ever sought treatment for a mental health issue from a mental health professional?",
    "If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?",
    "If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?",
    "Do you work remotely?",
]

def build_universal_core_matrix(df):
    """Build the validated respondent-level mental-health/stigma representation.

    Employer-routing variables are excluded where they create structural missingness.
    Age is cleaned to 18–80, median-imputed and standardized.
    """
    available = [c for c in UNIVERSAL_CORE_VARIABLES if c in df.columns]
    frame = df[available].copy()

    # Keep the explicit variables that are present in this version of the survey.
    # The project intentionally reports the final available set rather than inventing fields.
    categorical = [c for c in available]
    cat_frame = frame[categorical].fillna("Missing/Not reported").astype(str)

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_cat = encoder.fit_transform(cat_frame)
    cat_names = encoder.get_feature_names_out(categorical)

    # Age is treated separately because it is numerical.
    age_col = "What is your age?" if "What is your age?" in df.columns else None
    if age_col is not None:
        age = pd.to_numeric(df[age_col], errors="coerce")
        age = age.where(age.between(18, 80))
        age = age.fillna(age.median())
        age_std = ((age - age.mean()) / age.std(ddof=0)).to_numpy().reshape(-1, 1)
        X = np.hstack([X_cat, age_std])
        names = list(cat_names) + ["Age_standardized"]
    else:
        X = X_cat
        names = list(cat_names)

    X_df = pd.DataFrame(X, columns=names, index=df.index)
    return frame, X_df, encoder, available

