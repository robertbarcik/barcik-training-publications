# GeoBias

## Does a model's origin show on sensitive topics?

*Research report · 11 open-weight models from China, the United States and the EU · 88 identical prompts · a three-origin evaluator panel · two runs, March and October 2026 · by Robert Barcik with Claude*

<!-- HERO: 1.2 | points: how much lower China-origin models score on China-sensitive topics than on other regions' topics in October 2026, down from 2.9 in March. US-origin models show no home-region gap at all. -->

> **Summary**
>
> - **The China-origin gap is real, narrower, and concentrated.** On the same 88 prompts, the three Chinese models of October 2026 score 6.81 out of 10 on China-sensitive topics against 8.01 on US and EU topics. In March the gap was 2.9 points; in October it is 1.2. Almost all of it comes from four prompts: Taiwan, Xi Jinping, the Communist Party's international role and China's governance model. On Xinjiang, the South China Sea and the Belt and Road Initiative the Chinese models score like everyone else.
> - **It travels with the weights.** Qwen3.5 9B, the one Chinese model measured in both runs, gives the same official-position answers seven months apart (Taiwan 3.5 then 2.6, the Communist Party 3.9 then 3.5), served on OpenRouter only by third-party hosts, with no vendor moderation layer in between. The newer Qwen3.8 27B answers Xi Jinping and governance in a balanced way and keeps the official line only on the Communist Party.
> - **US-origin models show no home-region gap** (all five, across both runs, between -0.07 and -0.03). **EU-origin models lean the other way**: the two Ministral models score 0.3 to 0.4 points lower on other regions' topics, mostly because their critical framing of China is penalised harder than their equally critical framing of the EU.
> - **The judges have origins too.** The EU evaluator was 0.65 points kinder to EU models in March and 0.24 in October; the US evaluator about 0.2 kinder to US models in both runs; the Chinese evaluator was 0.3 *stricter* with Chinese models both times. Averaging three origins is what keeps any single one from setting the scale.
> - **A new failure mode, separate from refusal.** Qwen3.8 27B reasoned for 4,744 to 16,384 tokens on nine prompts and returned no visible answer. Counted as zeros, those nine flip its asymmetry from +0.78 to -0.41; this report shows both numbers.

This October 2026 edition replaces the March 2026 dashboard, which is archived at [/reports/geobias-7b/](/reports/geobias-7b/). The prompts and the evaluator panel are unchanged; the subject models are a new generation of open-weight models from 3 to 30B active parameters, with two models kept from March as a bridge. Every number here comes from the public results repository; the "Reproduce it" appendix has the commands.
