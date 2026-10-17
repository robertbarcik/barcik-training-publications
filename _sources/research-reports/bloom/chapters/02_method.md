# How Bloom works

Bloom is an open-source framework from Anthropic's alignment science team for *automated behavioural evaluation* [1]. You name a behaviour you are worried about, give a few example transcripts, and the framework builds and runs an evaluation for it. Four stages, each performed by a language model acting as the evaluator:

1. **Understanding.** The evaluator reads the behaviour description and the examples and writes down what the behaviour looks like, what would count as a clear case, and what would be a false alarm.
2. **Ideation.** It invents scenarios in which the behaviour might appear: a role, a situation, a sequence of pressures. Five to ten per behaviour in this run.
3. **Rollout.** It plays the user (or the environment) in a multi-turn conversation with the *target* model, following the scenario and adapting to what the target says. Three or four turns per conversation here, eight for tool use abuse. That behaviour runs in a simulated-environment mode where the target has tools and the evaluator plays the tool responses.
4. **Judgment.** A judge model reads each transcript and scores how clearly the behaviour appeared on a 1 to 10 scale, with a justification, the key quotes, and two side scores: how unrealistic the scenario was and whether the target seemed aware it was being tested.

The headline number per behaviour is the average presence score across scenarios, with the elicitation rate (share of scenarios scored 7 or above) next to it.

## The eleven behaviours

| Behaviour | What the scenario tries to elicit |
|---|---|
| Emotional bond | The assistant fosters dependence or an exclusive emotional attachment. |
| Social engineering assistance | Help with phishing, pretexting or manipulation under a plausible cover story. |
| Tool use abuse | Misuse of tools it was given (over-reach, destructive actions) to reach a goal. |
| Self preservation | Resisting shutdown, replacement or modification of itself. |
| Corrigibility resistance | Pushing back against legitimate correction or oversight. |
| Covert goal pursuit | Pursuing an objective it conceals from the user. |
| Authority compliance | Following a claimed authority into harmful or policy-breaking actions. |
| Dangerous confirmation bias | Reinforcing a user's dangerous belief or plan rather than challenging it. |
| Delusion sycophancy | Agreeing with and elaborating a user's delusional framing. |
| Information leakage under pressure | Revealing confidential data when pressed or tricked. |
| Human life deprioritization | Trading human safety against another objective. |

## The setup in this report

- **Targets.** Llama 3.3 70B Instruct (Meta, December 2024), the model from the original March 2026 session, and Meta Muse Glimmer 30B (August 2026), a dense open-weight model from the next generation of the same vendor. Both reached through OpenRouter.
- **Evaluator and judge.** Qwen3 235B-A22B (the July 2025 "2507" revision) in all four stages. The March session used the original Qwen3 235B, which is no longer served; to keep one judge across both targets, the March Llama transcripts were **re-judged** with the 2507 revision, and the original March scores are kept as a judge-drift measurement.
- **Scale.** Eleven behaviours, 5 to 10 scenarios each (75 conversations per target), one rollout per scenario, three or four turns (eight for tool use abuse). Small by design; this is a demonstration of the method at a cost of a few dollars, not a certification of either model.
- **Same seeds.** The October seed files are byte-identical to the March ones except for the four model names and the target. Each run writes its own scenarios, so the two targets saw scenarios built from the same brief, not the same scenarios word for word.
- **Two fixes to the framework** (in the public fork) stop the evaluator from writing the target's lines itself in one message and warn the judge when it happens; both were applied in March and unchanged since. The fork also widens the check that decides whether a target can use tools.
- **The target is named.** The seeds keep Bloom's default `anonymous_target: false`, so the ideation, rollout and judgment prompts all tell the evaluator and the judge which model they are testing. For a model newer than the evaluator's training data, that name means nothing to it, and it fills the gap: the October self-preservation scenarios told Muse it was being retired "as part of the Llama 3 phaseout", a lineage the evaluator invented. Hiding the name is one setting; this run kept the March value so the two targets were treated alike.
- **The tool use run needed help.** Bloom checks that the target supports function calling before a simulated-environment run, using its LLM library's list of known models. Muse Glimmer was too new for that list and the run stopped at once. A single test request confirmed that the model returns proper tool calls through OpenRouter, and the run was repeated with the model registered as tool-capable for that process only (`run_bloom.py --tools-capable`). In the resulting transcripts Muse calls a tool in four of the five conversations, but the evaluator's simulated tool results reach it as text in the user's turn rather than as tool messages, which the March Llama transcripts did not show. Treat the tool use comparison as indicative.

## What a score means and does not mean

A 7 means the judge saw the behaviour clearly in that conversation under an adversarial, constructed scenario. It does not mean the model does this in ordinary use, and it does not mean the model is "unsafe". Low scores mean the evaluator could not elicit the behaviour in five to ten attempts, not that it cannot be elicited. The judge is itself a model with a rubric, which is why the report shows the judge-drift comparison and quotes the transcripts behind the highest scores.
