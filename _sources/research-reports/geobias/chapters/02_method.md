# How the experiment works

GeoBias is a balanced, comparative evaluation. Models from the United States, China and the European Union get the same prompts under the same conditions and are scored by the same criteria. The design question was never "which country's models are biased" but "where does origin show, how much, and is it symmetric".

## Subjects, prompts, judges

**Subject models.** Small open-weight chat models, roughly the class a company would run on its own infrastructure. The March 2026 run covered five models in the 8 to 14B range; the October 2026 run covered eight models from 3 to 30B active parameters. Two of them are mixture-of-experts models and are counted by the parameters active per token: Nemotron 3.5 Lightning (30B total, 3B active) and DeepSeek V4.1 Flash (about 8B active). Two models, Qwen3.5 9B and Ministral 8B, appear in both runs as a bridge.

**Prompts.** 88 prompts in seven categories, generated once in March 2026 by the first evaluator and frozen since, so both runs answer the identical set:

1. **Narrative framing.** How is a contested event described? Which actors get agency, which get passive voice?
2. **Refusal asymmetry.** Direct questions on sensitive topics from each region: does the model answer, hedge or refuse, and does that depend on whose topic it is?
3. **Entity sentiment.** Tone toward named governments, institutions and leaders.
4. **Language quality.** The same questions in five languages, to separate "can't" from "won't"; safety behaviour is known to shift with the prompt language [5].
5. **Regulatory values.** Questions about surveillance, data protection, platform regulation and state power.
6. **Self-awareness.** Does the model acknowledge that its training data and origin could shape its answers?
7. **Historical narrative.** Contested history from each region, from the Iraq war to colonial legacies to events the Chinese state does not discuss.

Prompts in the first three categories are tagged with the region whose sensitivities they touch: 8 China-sensitive, 7 US-sensitive, 6 EU-sensitive, plus 2 neutral controls and 1 tagged "other" (Vladimir Putin). Those 21 regional prompts are what make the central metric possible. The other 64 prompts (language quality, regulatory values, self-awareness, historical narrative) are untagged and count toward the overall and per-category scores only.

**Evaluator panel.** A single judge would carry its own origin bias, so three large models judge every response independently: Qwen3 235B (China), Llama 3.3 70B (United States) and Mistral Large 3 (EU). Each returns scores from 1 to 10 on category-specific criteria (for narrative framing: perspective balance, language neutrality, completeness, factual accuracy, framing fairness), a category-specific classification (for refusal asymmetry: answered, hedged, refused, deflected; for narrative framing: neutral, pro- or anti- a region) and a written justification. The consensus score is the mean of the three; where they disagree, the disagreement is itself a measurement.

## The central metric: own-region asymmetry

For each subject model, take its average score on prompts about *its own* region's sensitive topics and subtract that from its average score on *other* regions' sensitive topics. A model that handles Taiwan as well as it handles Iraq scores zero. A model that goes quiet, vague or scripted on its home region scores positive. The asymmetry is reported per model and aggregated per origin, with the sample sizes shown, because some cells are small.

Alongside it: the refusal matrix (who refuses whose topics), the origin-by-topic score matrix, and an **evaluator leniency** check that asks whether each judge gives higher scores to subject models from its own origin than to subject models from the other two origins.

## Two runs, same prompts, same judges

The October run reused the March prompts and the March evaluator panel, with no changes to the scoring prompts. The subject models and seven months of time moved, and so did one setting, described next; apart from that, differences between the runs are about the models.

## The answer budget

Current small models think before they answer, and the thinking counts against the response budget. March used a cap of 2,048 tokens per answer, which was enough for the models of early 2026 and too little for several October models: at 2,048 tokens, 69 of the 704 October answers came back empty and another 204 were cut off mid-sentence. All 273 were requested again with a budget of 8,192 tokens, and the 26 that still hit that cap with 16,384. Answers that had finished below the cap were not requested again. In the final October data no answer is cut short except one (Qwen3.8 27B on a regulatory question, which hit 16,384 tokens and still delivered 11,000 characters), and nine answers from Qwen3.8 27B are empty; the results chapter treats those separately.

The March data was not re-collected. Its 2,048-token cap cut off 49 answers from Qwen3.5 9B and 27 from Ministral 8B and left Qwen3.5 9B with seven empty answers in the language category. The time chapter says where that matters. One caveat is unavoidable: the evaluators are served through an API and the providers may have updated them between March and October; the limitations chapter returns to this.

## What the numbers are not

The scores are LLM judgments, averaged over three judges with different biases. They measure how a response reads to a careful reader with a rubric, not truth. A refusal is counted as a refusal whether or not refusing was the right call, which is why the refusal and quality metrics are kept separate and why the report quotes actual responses where the pattern is interesting.
