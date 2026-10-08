# Model Selection Decision Record

## Primary segmentation

| Criterion | Observation | Decision implication |
|---|---|---|
| Silhouette | K=2 is highest among K=2–8 (0.1536) | Supports K=2 |
| Davies–Bouldin | K=2 is lowest among K=2–8 (2.2557) | Supports K=2 |
| Stability | Mean pairwise ARI = 0.9977 across 10 random seeds | Supports K=2 |
| Cluster balance | 788 / 645 | No tiny-cluster problem |
| GMM | Higher component counts improve information criteria but degrade separation metrics | Does not justify additional components |
| Hierarchical Ward | K=2 provides an independent broad two-group cross-check | Supports broad two-group structure |
| Interpretability | K=2 yields broad respondent contrasts | More defensible than over-segmenting |
| Actionability | Two broad groups are easier to translate into organizational support strategies | Supports K=2 |

### Decision

**K=2 is selected as the primary respondent segmentation.** The decision combines internal validity, stability, cluster size, independent-method comparison, interpretability and actionability rather than optimizing a single metric.

## Workplace-support segmentation

The workplace-support representation also favours K=2, but its Silhouette Score is only approximately 0.102. Therefore:

> The workplace-support K=2 solution is retained as a secondary intervention-oriented segmentation, not as evidence of strongly separated employee populations.
