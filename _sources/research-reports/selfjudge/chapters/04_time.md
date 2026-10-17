# The time perspective

<!-- FIG: f2_skill_vs_release | **Judging skill by model generation.** Each model plotted at its public release month; marker area grows with parameter count, hollow markers are mixture-of-experts models, the diamond is the closed ceiling. -->

The two runs are three months apart, but the models in them span two years of releases, from Llama 3.2 (September 2024) to LFM2.5 (October 2026). Plotting judging skill against release month instead of size tells a cleaner story than Figure 1.

- **2024 generation.** The three small models from 2024 are the three lowest scores in the whole set below 7B: Llama 3.2 1B at 47%, Llama 3.2 3B at 77%, and Qwen 2.5 7B at 94% (the first to reach the plateau). Llama 3.3 70B, from December 2024, is on the plateau at 98%, but it needed 70B to get there.
- **2025 generation.** Eight models from 85% (Granite 4.0 Micro) to 98% (Nemotron 3 Nano). The spread is wide, and the mixture-of-experts models are at the top of it.
- **2026 generation.** Ten models, all between 95 and 98%, from 2.45B active parameters to 30B, dense and sparse, from five vendors on three continents. The spread has closed.

The plain reading is that judging skill, as this test measures it, became a standard property of small models during 2025 and was universal by 2026. What took 70B parameters at the end of 2024 took 3B active parameters by the end of 2025 and is now the floor. Size still matters for other things; for grading an explicit flaw it stopped mattering about a year ago.

Two cautions. Release month is a coarse proxy for training recipe, which is what actually changed. And the test cases were written in July 2026 by DeepSeek V3.1; a model trained after that date could, in principle, have seen similar material, though the planted answers are specific to this run and are not public anywhere else.

## What did not change between July and October

The three-month gap between the runs is too short for a trend and was not meant to show one. Its value is methodological: the October models were judged by the same orchestrator and meta-judge against the same 54 test cases and the same 108 planted anchors, so the two runs sit on one chart without adjustment. The March 2026 run cannot join them; its methodology was replaced and its numbers are archived.

> **Key takeaways**
>
> - By release month: 2024 small models below the plateau, 2025 models spread across it, 2026 models all on it.
> - What needed 70B in late 2024 needs 3B active parameters now.
> - Release month is a proxy for training recipe, and the test set postdates most of the models; read the chart as a pattern, not a causal claim.
