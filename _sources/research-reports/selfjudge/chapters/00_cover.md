# SelfJudge

## Can a small language model judge its own outputs?

*Research report · 21 open-weight models from 1B to 70B plus one closed ceiling · two runs on one test set, July and October 2026 · by Robert Barcik with Claude (Fable 5.1)*

<!-- HERO: ~3B | is where judging skill switches on. Above it, size stops mattering and generation takes over. -->

> **Summary**
>
> - **Judging skill is a step, not a slope.** On a balanced set of planted answers with ground truth by construction, a 1B model scores at chance (47%). Above 3B, 20 of the 21 open models score 85 to 98%; the one exception is the 2024-era Llama 3.2 3B at 77%. The 70B model (98%) is no better than the best 2.5B-active mixture-of-experts (98%).
> - **Generation beats size.** Every 2026-generation model, from 2.45B active parameters to 30B, sits at 95 to 98%. The closed GPT-6 Luna, included only as a ceiling, scores 93.5% on the same anchors, below 15 of the 21 open models.
> - **Self-assessment lags.** Nineteen of the 22 models score lower on their own answers than on planted ones, by up to 26 points; three current models are within a point either way.
> - **Every model is lenient with itself.** Each one waves through more of its own failures than of identical-looking planted failures. Among the 12 models with ten or more own failures to judge, the average gap is 49 points; the strongest models fail so rarely that their leniency rests on three to six cases and is shown as unreliable.
> - **What this means on device:** a current-generation model of 3B active parameters or more can run a sanity pass on its own output and catch explicit flaws at roughly 95%. It cannot be trusted with the failures it is lenient about; pair it with a rules-based check and an occasional independent audit.

This report replaces the March 2026 SelfJudge report, whose methodology (single-sample verdicts, no planted anchors, a degenerate "balanced" set) produced the opposite conclusion, "you need more than 27B". The July 2026 methodology fixed that, and this October edition extends it with eight more models, a 70B rung, a closed ceiling and the time perspective. Every number here comes from the public results repository; the "Reproduce it" appendix has the commands.
