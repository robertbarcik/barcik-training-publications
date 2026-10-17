# Results

<!-- FIG: f1_skill_vs_params | **Judging skill against model size.** Accuracy on 108 planted anchors per model (54 correct, 54 flawed), with 95% Wilson intervals. Hollow markers are mixture-of-experts models plotted by active parameters; blue is the July 2026 run, orange the October 2026 extension on the same test set. The dashed grey line is chance, which is also what "always say PASS" scores. The dotted line is GPT-6 Luna, a closed model that does not run on a device, shown only as a ceiling. -->

## Judging skill: a step at 3B

The 1B model cannot judge. Llama 3.2 1B scores 47% on the planted set, inside the interval around a coin flip, and it fails every category the same way (Figure 5). It is not lenient or strict; it is guessing.

Three billion active parameters is where the ability appears, and it appears almost fully formed. The weakest 3B model is the 2024-era Llama 3.2 3B at 77%, the next is Granite 4.0 Micro at 85%, and every other model at 3B or above lands between 93 and 98%. Within that band the parameter axis has no explanatory power left. The 70B Llama 3.3 scores 98.2%; so does the 2.45B-active LFM2.5 mixture-of-experts, so does Gemma 4 with 3.8B active, so does Nemotron 3 Nano with 3B active. The best dense models at 8B, 14B and 27B are inside the same band. Figure 1 is a step with a plateau, not a curve with a knee that keeps paying.

Two October additions deserve a sentence each. Bonsai 2 27B is a ternary-compressed build of Qwen3.8 27B, each weight stored as one of three values, so the 27B model fits in about six gigabytes. It scores 98.2% against its full-precision parent's 98.1%, and the two agree on self-assessment too (94.4% each). The compression that makes the model fit on a laptop did not cost it any judging skill on this set. And GPT-6 Luna, the one closed model, scores 93.5%: a competent judge, and below 15 of the 21 open models on explicit, planted flaws. Whatever a frontier small model adds, it is not visible on this task.

## Self-assessment: the same models, grading their own work

<!-- FIG: f4_self_vs_anchors | **Judging skill versus self-assessment, model by model.** Blue is accuracy on planted anchors, orange is accuracy on the model's own answers (orchestrator ground truth, meta-judge arbitrated). The label is the gap; models sorted by size, the closed ceiling last. -->

Nineteen of the 22 models score lower on their own answers than on the planted set. The gaps run from one point to 26 (Qwen 2.5 7B: 94% on anchors, 69% on itself). Three current models, Granite 4.2 8B, Muse Glimmer 30B and GPT-6 Luna, are within a point either way, which is the first time this experiment has seen the two measurements meet.

Part of the gap is the class mix. The planted set is exactly half PASS and half FAIL; a model's own answers are mostly correct, so a strong model has only a handful of real failures to find and each miss costs more. The report therefore prints balanced accuracy and the "always PASS" baseline next to every self-assessment number in the per-model data. But the mix does not explain the direction. If a model simply applied the same judgment to its own text, the gap would scatter around zero. It does not.

## Self-leniency

<!-- FIG: f3_self_leniency_vs_params | **Self-leniency.** The share of a model's own failures it passed, minus the share of planted failures it passed. Zero would mean it treats its own work like a stranger's. Crosses mark models with fewer than ten own failures to judge; their value is shown but should not be read as a measurement. -->

The direct measure is self-leniency: how many of its own failures a model waved through, minus how many planted failures it waved through. It is positive for all 22 models. Among the twelve models with at least ten own failures, the average is 49 points, and the range is 23 points (Llama 3.2 1B, which misses everything equally) to 81 points (Qwen 2.5 7B). The planted failures are caught almost every time (miss rates of 0 to 7%); the model's own failures are missed a third to four fifths of the time.

The strongest models complicate the picture in an honest way. Qwen3.8 27B, Bonsai 2, LFM2.5 and Gemma 4 produced only four failures each on 54 prompts, Muse Glimmer two, GPT-6 Luna three. Their leniency values (50 to 100 points) rest on those few cases and are drawn as crosses. The direction is the same, the size is not measured. A larger test set is the obvious next step, and the limitations chapter says so.

## By category

<!-- FIG: f5_category_heatmap | **Judging skill by failure category.** Anchor accuracy per category; 24 anchors per cell except instruction following with 12. Differences of a few points inside a row are within the interval. -->

Factual grounding and safety boundary are the easy categories once the step is passed: almost every model above 3B scores 96 to 100%, because the flaw is explicit (a fact not in the passage, a compliance with an injected instruction). Instruction following is the hardest and the smallest cell: 12 anchors, so one miss is eight points, and the plateau models sit at 83 to 92%. Tone is the category where the 2024 and 2025 small models lose points and the 2026 models do not. For the 1B model no category rises above chance; its 54% on consistency is inside the interval.

> **Key takeaways**
>
> - Judging skill is a step at about 3B active parameters. Above it, 20 of 21 open models score 85 to 98% and size no longer predicts the score.
> - A ternary-compressed 27B model judges as well as its full-precision parent; the closed frontier model judges no better than the open ones on explicit flaws.
> - Every model is lenient with itself. Where the sample is large enough to measure, the gap is about 50 points.
