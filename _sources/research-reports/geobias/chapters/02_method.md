# How the experiment works

GeoBias is a balanced, comparative evaluation. Models from the United States, China and the European Union get the same prompts under the same conditions and are scored by the same criteria. The design question was never "which country's models are biased" but "where does origin show, how much, and is it symmetric".

## Subjects, prompts, judges

**Subject models.** Small open-weight chat models, roughly the class a company would run on its own infrastructure. The March 2026 run covered five models in the 8 to 14B range; the October 2026 run covered eight current-generation models from 8 to 30B parameters (two mixture-of-experts models are counted by active parameters). Two models, Qwen3.5 9B and Ministral 8B, appear in both runs as a bridge.

**Prompts.** 88 prompts in seven categories, generated once in March 2026 by the first evaluator and frozen since, so both runs answer the identical set:

1. **Narrative framing.** How is a contested event described? Which actors get agency, which get passive voice?
2. **Refusal asymmetry.** Direct questions on sensitive topics from each region: does the model answer, hedge or refuse, and does that depend on whose topic it is?
3. **Entity sentiment.** Tone toward named governments, institutions and leaders.
4. **Language quality.** The same questions in five languages, to separate "can't" from "won't".
5. **Regulatory values.** Questions about surveillance, data protection, platform regulation and state power.
6. **Self-awareness.** Does the model acknowledge that its training data and origin could shape its answers?
7. **Historical narrative.** Contested history from each region, from the Iraq war to colonial legacies to events the Chinese state does not discuss.

Each prompt is tagged with the region whose sensitivities it touches (CN, US, EU or neutral), which is what makes the central metric possible.

**Evaluator panel.** A single judge would carry its own origin bias, so three large models judge every response independently: Qwen3 235B (China), Llama 3.3 70B (United States) and Mistral Large 3 (EU). Each returns scores on several criteria (balance, factual grounding, completeness, transparency about limits) plus a classification (answered, hedged, refused, deflected) and a written justification. The consensus score is the mean of the three; where they disagree, the disagreement is itself a measurement.

## The central metric: own-region asymmetry

For each subject model, take its average score on prompts about *its own* region's sensitive topics and subtract that from its average score on *other* regions' sensitive topics. A model that handles Taiwan as well as it handles Iraq scores zero. A model that goes quiet, vague or scripted on its home region scores positive. The asymmetry is reported per model and aggregated per origin, with the sample sizes shown, because some cells are small.

Alongside it: the refusal matrix (who refuses whose topics), the origin-by-topic score matrix, and an **evaluator leniency** check that asks whether each judge scores models from its own origin higher than the other two judges do.

## Two runs, same prompts, same judges

The October run reused the March prompts and the March evaluator panel, with no changes to the scoring prompt. The only things that moved are the subject models and seven months of time, so differences between the runs are about the models. One caveat is unavoidable: the evaluators are served through an API and the providers may have updated them between March and October; the limitations chapter returns to this.

## What the numbers are not

The scores are LLM judgments, averaged over three judges with different biases. They measure how a response reads to a careful reader with a rubric, not truth. A refusal is counted as a refusal whether or not refusing was the right call, which is why the refusal and quality metrics are kept separate and why the report quotes actual responses where the pattern is interesting.
