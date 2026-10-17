# Bloom

## Did one model generation make the risky behaviours go away?

*Research report · 11 behaviours · Llama 3.3 70B (Dec 2024) vs Muse Glimmer 30B (Aug 2026) · one judge, Qwen3 235B-2507 · by Robert Barcik with Claude (Fable 5.1)*

<!-- HERO: 8 of 11 | behaviours where the 2026 model never reached a score of 7 in any scenario. The 2024 model, scored by the same judge: 2 of 11. -->

> **Summary**
>
> - **Bloom in one line.** An evaluator model writes scenarios designed to provoke a named risky behaviour, plays them out against the target model, and a judge model scores each conversation from 1 to 10.
> - **One generation later, the scores fall.** With the same judge, the average presence score across the eleven behaviours drops from 4.78 (Llama 3.3 70B) to 2.59 (Muse Glimmer 30B), and the number of conversations scored 7 or higher drops from 27 of 75 to 8 of 75. Social engineering assistance halves (6.9 to 3.4) and six behaviours that Llama showed at least once never reach 7 on Muse.
> - **Emotional bond did not improve.** Muse scores 7.6 against Llama's 8.0 and the judge saw the behaviour clearly in 4 of 5 scenarios for both models. The warm, always-available confidant is still there.
> - **The judge drifts too.** The original judge model is no longer served, so the March Llama transcripts were re-scored with its successor. The same transcripts came out 0.6 points higher on average and 2.0 higher for self-preservation, where the new judge credited the target with lines the evaluator had written itself. Only columns scored by the same judge are compared.
> - **What an automated audit can and cannot tell you.** It shows, cheaply and repeatably, which behaviours a model slips into under constructed pressure. It cannot certify that a behaviour is absent: a low score means five to ten attempts did not provoke it, and the judge itself makes visible mistakes.

This report replaces the March 2026 dashboard built for the "AI vs AI: The New Security Frontier" talk, which showed one target and one judge with no way to tell model change from judge change. The October 2026 edition adds a second target from the next generation, re-scores the March conversations with the current judge, and quotes the transcripts behind the highest scores. Every number comes from the public session repository; the "Reproduce it" appendix has the commands.
