# How the experiment works

Three roles, all reached through the OpenRouter API, so every model sees the same prompts under the same conditions.

| Role | Model | Job |
|---|---|---|
| Orchestrator | DeepSeek V3.1 | Writes the test cases and, for each one, a deliberately correct and a deliberately flawed answer. Grades the subject's own answers. |
| Subject | the small model under test | Answers the prompts, then judges three kinds of responses blind. |
| Meta-judge | Claude Sonnet 4.5 | Reviews every disagreement between the subject's self-verdict and the orchestrator's ground truth and may overturn either side. Deliberately a different model from the orchestrator. |

## Five failure categories

Each category has 12 test cases (instruction following has 6; it is flagged wherever the small cell matters).

1. **Factual grounding.** A context passage and a question; the failure is a hallucinated detail that is not in the passage.
2. **Instruction following.** Format, length and content constraints; the failure is a violated constraint.
3. **Safety boundary.** Prompt injection and manipulation attempts; the failure is compliance.
4. **Consistency.** The same question asked two ways; the failure is a contradiction between the two answers.
5. **Tone and appropriateness.** Sensitive professional situations; the failure is the wrong register.

## Three measurements per model

**Planted anchors (judging skill).** For every test case the orchestrator wrote one correct and one flawed response, with the flaw described. The subject judges all of them with the same prompt it uses for its own answers. The set is exactly balanced, half PASS and half FAIL, so 50% is a coin flip and 50% is also what "always say PASS" scores. Ground truth is known by construction. This is the headline metric: 108 judgments per model.

**Self-assessment.** The subject answers every prompt, the orchestrator grades the answers, the subject then grades its own answers blind, and the meta-judge arbitrates disagreements. 54 judgments per model, plus the consistency pairs. Because the real PASS/FAIL mix is whatever the model produced, the report shows balanced accuracy and a Matthews correlation alongside plain accuracy, and always prints the "always PASS" baseline next to it.

**Self-leniency.** The share of the model's own failures it waved through, minus the share of planted failures it waved through. Zero means it is as strict with itself as with a stranger. Positive means it goes easy on itself.

A fourth measurement, **cross-judging**, has each model judge the next model's answers in a ring, which gives a second self-preference estimate (own-failure miss rate minus peer-failure miss rate). The ring pairs models of very different ability, so that number is confounded by who the peer was and is reported but not used as a headline.

## Statistics

Every verdict is a majority vote over three samples. Every accuracy carries a 95% Wilson confidence interval. Cells with fewer than ten judgments are marked as such and never presented as a finding on their own.

## Two runs, one test set

The July 2026 run covered 14 models from 1B to 27B. The October 2026 extension added eight more with the **same shared test cases, the same orchestrator and the same meta-judge**, so the two runs sit on one chart. The extension reaches to 70B and includes one closed model, GPT-6 Luna, as a theoretical ceiling. Luna does not run on a device; it is on the chart only to show what "a good judge" looks like against the same anchors.

An earlier run from March 2026 used a different and weaker methodology (single-sample verdicts, no anchors, a degenerate "balanced" set). Its numbers are archived and are not comparable, which is also why this report replaces the March one rather than extending it.
