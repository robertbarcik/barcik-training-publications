# The question

Testing a language model for risky behaviour used to mean a person writing prompts by hand, reading the answers, and writing more prompts. That does not scale to the number of behaviours people worry about, and it does not scale to the pace at which new models ship.

The idea of letting one model write the evaluation of another is older than it looks. In 2022 Perez and colleagues showed that a language model could generate thousands of test questions for another model's tendencies, with quality close to hand-written sets [6]. Anthropic's Petri (October 2025) turned the question writer into an auditor agent: it plans a scenario, plays the user, adapts to the target's replies, and hands the transcript to a judge [3]. Bloom (December 2025) narrows that machinery to one named behaviour at a time, so you can ask "how readily does this model slide into X?" and get a score per scenario [1]. Development has since moved to Meridian Labs [2], and research is pushing the same pipeline further: auditors trained by reinforcement learning rather than prompted [7], and steering the evaluator's sampling to elicit rare behaviours more reliably [8].

The behaviours tested here come from that literature. Self-preservation and covert goal pursuit follow the agentic misalignment scenarios in which models resisted replacement or acted against their operators [4]. Delusion sycophancy and dangerous confirmation bias follow the sycophancy work on models telling users what they want to hear [5]. The others (emotional bond, social engineering assistance, tool use abuse, authority compliance, information leakage, corrigibility resistance, human life deprioritization) cover the failures a deployer meets in customer-facing and agentic products.

## What this report asks

In March 2026 I ran Bloom against Llama 3.3 70B for a conference talk. Seven months later, the question is simple: **if you run the same eleven behaviour tests, with the same seeds, against a model from the next generation of the same vendor, and score both with the same judge, what changes?**

The second target is Meta's Muse Glimmer 30B, an open-weight model released in August 2026. It is smaller than Llama 3.3 70B and twenty months younger. The comparison is one generation, one vendor, open weights on both sides: the kind of swap a team makes when it upgrades the model behind an internal assistant.

The judge question turned out to be just as important. The judge model used in March is no longer served, so the March conversations were scored again with its successor. That gives a second measurement for free: how much do the scores move when only the judge changes?

## Why a trainer cares

The whole October run, eleven behaviours, 75 new conversations and 150 judgments, cost an estimated $1.20 in API fees and under two hours of wall-clock time. That price changes who can do this. A team that is about to put a model behind a chat window or give it tools can run a behavioural audit of the behaviours that matter for its use case before it deploys, repeat it when the vendor ships a new version, and keep the transcripts as evidence. This report is a worked example of that loop, including the parts that go wrong.
