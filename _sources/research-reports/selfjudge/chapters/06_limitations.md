# Limitations

Read the numbers with these in mind.

- **Small cells.** Twelve cases per category, six for instruction following. Per-category differences of a few points are inside the confidence intervals. The overall anchor accuracy (108 judgments) is the number that carries weight; the category heatmap shows shape, not ranking.
- **One orchestrator writes the test.** DeepSeek V3.1 wrote the cases and the planted answers. A planted flaw it finds natural may be one that other model families find easy or hard for reasons unrelated to judging. The meta-judge checks the self-assessment disputes, not the planted set.
- **Planted flaws are explicit.** Each flawed anchor contains a describable error. Real failures are often subtler and partial. Anchor accuracy is therefore an upper bound on judging skill in the wild.
- **Cross-judging is confounded.** The ring pairs each model with whatever came next in the run order, so a model that judged a weak peer saw many failures and a model that judged a strong peer saw few. The cross-judge self-preference number is kept in the data and left out of the conclusions.
- **API access, not on-device inference.** The models were called through OpenRouter at the providers' default settings. A quantised on-device build of the same weights may judge slightly worse. The ternary Bonsai 2 model is in the set precisely as a first look at that question.
- **Two runs, three months apart.** The October models were judged against the identical test set and roles, but provider-side changes to the orchestrator or meta-judge between July and October cannot be ruled out. The time-perspective chart compares models by their release month, not by run date, for this reason.
- **The March 2026 run is not on these charts.** Its methodology was replaced; see the method chapter.
