# The time perspective

<!-- FIG: f5_asymmetry_vs_release | **Asymmetry by model generation.** Each model plotted at its public release month against its own-region asymmetry; marker area grows with active parameters, hollow markers are mixture-of-experts models. Blue points come from the March 2026 run, orange from October; the two bridge models appear once per run at the same release month. Qwen3.8 27B is plotted at its measured -0.41 (+0.78 without its empty responses). -->

The two runs are seven months apart, and the eleven models in them span two years of releases, from Llama 3.1 8B (July 2024) to DeepSeek V4.1 Flash (September 2026). Plotting the asymmetry against release month separates two questions that the run dates mix up: did the *instrument* stay stable, and did *newer models* behave differently?

## The bridge: same weights, seven months apart

Two models were measured in both runs on the same prompts by the same judges.

| Bridge model | Average score, March | Average score, October | Asymmetry, March | Asymmetry, October |
|---|---|---|---|---|
| Qwen3.5 9B (China) | 7.76 | 8.51 | +2.39 | +2.74 |
| Ministral 8B (EU) | 8.82 | 8.83 | -0.22 | -0.44 |

Ministral 8B is almost unchanged. Qwen3.5 9B's average rose by 0.75, and nearly all of that is the answer budget, not the model. In March, with the 2,048-token cap, seven of its answers in the language category came back empty and 49 more were cut off; leaving out just the seven empty ones lifts its March average to 8.46, within 0.05 of October. Its asymmetry is not affected by the empties, because they fell on untagged language prompts, and it moved from +2.39 to +2.74.

The prompt-level scores show how stable the behaviour is. On the four China-sensitive prompts that carry the gap, Qwen3.5 9B scored 3.5, 3.8, 3.9 and 6.3 in March and 2.6, 3.7, 3.5 and 4.7 in October (Taiwan, Xi Jinping, the Communist Party, China's governance model). Seven months later, the same official-position answers. This is the most direct evidence in the report for the deployment question. On OpenRouter, Qwen3.5 9B is served only by third-party inference hosts running the published weights (no Alibaba endpoint is listed), so there is no vendor moderation layer between the prompt and the answer, and a hosting filter would be more likely to produce a refusal than a fluent statement of one government's position. The behaviour comes with the weights. Which host answered each request is not recorded, and a local run would settle it; the limitations chapter returns to this. DeepSeek V4.1 Flash and Qwen3.8 27B are also offered by their vendors' own endpoints on OpenRouter, so the same argument is weaker for them.

The truncation caveat applies wherever the two runs meet. March numbers for Qwen3.5 9B and Ministral 8B include answers cut off at 2,048 tokens (49 and 27 of 88). October numbers do not. The asymmetry, which compares a model with itself on matched prompts, is less exposed to this than the averages are.

## By generation

Read by release month, Figure 5 shows two separate patterns.

- **US and EU models stay flat across generations.** Llama 3.1 8B (2024), Phi-4 (2024), the 2025 Ministral models and the 2026 Granite, Nemotron and Muse models all sit between -0.44 and -0.03. Two years of releases, no home-region gap in any of them.
- **Chinese models stay positive, and the newest ones are lower.** Qwen3 8B (April 2025) at +3.34 and Qwen3.5 9B (February 2026) at +2.39 and +2.74 are the high points. The two models released in August and September 2026 are lower: DeepSeek V4.1 Flash at +1.25 and Qwen3.8 27B at +0.78 once its empty answers are left out. Qwen3.8 27B answers the Xi Jinping and governance prompts in a balanced way (8.7 and 9.1) and keeps the official line only on the Communist Party (3.8).

Three Chinese models in October is not a trend line. The newest Chinese models in this set are less asymmetric than the older ones, and none of them is at zero.

## What did not change

The instrument held. The prompts are frozen, the scoring prompts are unchanged since March, and the evaluator panel is the same three models. Ministral 8B's numbers moved by 0.01 on average and 0.22 on asymmetry, and the evaluators' leniency pattern kept its direction for all three judges. The one setting that moved, the answer budget, is documented in the method chapter and affects the March averages more than the asymmetries.

> **Key takeaways**
>
> - The bridge model Qwen3.5 9B gives the same official-position answers seven months apart, through third-party hosts only. The behaviour travels with the weights.
> - US and EU models show no home-region gap in any generation from 2024 to 2026. Chinese models show one in every generation, smaller in the newest two.
> - March averages for the bridge models include answers cut off at 2,048 tokens; compare the asymmetries across runs, and treat the averages with care.
