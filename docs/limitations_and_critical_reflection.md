# Limitations and Critical Reflection

The analysis demonstrates useful but modest unsupervised structure.

The most important methodological risk was structural missingness. Several employer-related variables were not applicable to self-employed respondents. A preliminary broad representation produced a 1,146 versus 287 split corresponding to non-self-employed versus self-employed survey pathways. This indicated that the model could learn questionnaire-routing structure rather than the intended mental-health construct.

The representation was therefore redesigned. The primary model excludes employer-routing variables, while the workplace-support analysis is explicitly restricted to non-self-employed respondents.

A second limitation is cluster separation. The primary K=2 Silhouette Score is approximately 0.154 and the mean pairwise ARI across the stability sweep is 0.9977. The result is therefore highly stable but not evidence of strongly separated natural populations. It is better interpreted as a broad tendency in respondent profiles.

The workplace-support model has an even lower Silhouette Score of approximately 0.102. It is consequently used as a practical contrast for organizational intervention rather than a definitive taxonomy.

A third limitation concerns feature representation. The primary matrix combines binary one-hot features with one standardized age feature and remains approximately 72.41% zero-valued. Distance-based clustering can therefore be sensitive to encoding choices and the relative contribution of variables.

A fourth limitation concerns PCA. The first two principal components explain approximately 28.73% of the primary representation's variance, while the first 20 explain approximately 82.74%. The PCA plot therefore cannot be interpreted as a complete map of the data.

Finally, survey responses are self-reported and cross-sectional. The clusters do not establish causality, clinical status or individual risk. Any organizational application should operate at an aggregate level and should not be used for individual employment or clinical decisions.
