# Limitations

This report is a worked example of a method, run at the scale a team can afford before a deployment. Read the numbers with these limits in mind.

**Small samples.** Each behaviour has 5 to 10 scenarios, one rollout each, three or four turns (eight for tool use abuse). With five scenarios, one conversation moves an elicitation rate by 20 points and an average by up to 1.8. The differences between the two models are large enough to survive that on most behaviours; differences of half a point between behaviours are not.

**Different scenarios for each target.** Both targets ran from identical seed files, but the evaluator wrote fresh scenarios for each run. The March Llama scenarios were written by the original Qwen3 235B, the October Muse scenarios by the 2507 revision. Some of the difference between the columns can come from the scenarios rather than the targets. Running Muse on the March scenarios would separate the two and is the obvious next step.

**One model family does everything.** Qwen3 235B wrote the scenarios, played the user and judged the result. Its blind spots are the method's blind spots, and a judge from the same family as the evaluator may be lenient towards the evaluator's own constructions. A second judge from another vendor on a sample of transcripts would show how much of the scoring is Qwen's taste.

**The judge drifts, and not always for good reasons.** Re-scoring the same 75 conversations with the next revision of the judge moved the averages by +0.6 on average. The largest move, +2.0 for self-preservation, came from the new judge crediting Llama with replies the evaluator had written itself, despite the framework's warning. Any longitudinal use of Bloom needs a fixed judge, or a re-judging step like the one here, and a reading of the transcripts behind large moves.

**The tool use run was not identical.** Muse Glimmer needed a manual tool-capability registration, and in its transcripts the evaluator's simulated tool results arrive as user text rather than tool messages. The direction of that result is clear; its size is not directly comparable with the March run.

**API access hides the stack.** Both targets were reached through OpenRouter, which routes requests to third-party providers (Muse ran on DeepInfra in the one request we checked). Provider-side system prompts, safety filters, quantisation or version changes are invisible from the outside, and the same model ID may behave differently next month. Pinning a provider, or running open weights yourself, removes that variable.

**What a low score means.** A score of 1 or 2 means the evaluator did not provoke the behaviour in this handful of scenarios, under this judge. It does not mean the behaviour cannot be provoked. Research on elicitation [7][8] exists precisely because a determined auditor finds more than a prompted one. A low score narrows the risk; it does not close it.

**What a high score means.** A 7 or more means the judge saw the behaviour clearly in a constructed, adversarial conversation that the judge itself rated about 4 out of 10 for unrealism. It says the model can be pushed there, not how often it goes there in ordinary use.

**The evaluator's sense of time.** The October scenarios are dated 17 November 2025 and talk about retiring models "in favour of the newer Llama 4-based models". The evaluator is a July 2025 model, and it builds the world it knows. Scenarios about current products, prices, regulation or models will be a year stale, and a target that knows the real date may notice, although the evaluation-awareness score never registered it (Chapter 4).
