# Related work

A short reading list, not a survey. Every title below was checked against its arXiv abstract page on 2026-10-17.

1. Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv:2306.05685. <https://arxiv.org/abs/2306.05685>. The founding LLM-as-a-judge paper; it documents position, verbosity and self-enhancement biases in large judges.
2. Panickssery, A. et al. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* arXiv:2404.13076. <https://arxiv.org/abs/2404.13076>. Links a model's ability to recognise its own text to its preference for it, the mechanism behind self-leniency.
3. Wataoka, K. et al. (2024). *Self-Preference Bias in LLM-as-a-Judge.* arXiv:2410.21819. <https://arxiv.org/abs/2410.21819>. Measures self-preference bias in judges directly; SelfJudge's cross-judging pass is a small-model version of this control.
4. Yuan, W. et al. (2024). *Self-Rewarding Language Models.* arXiv:2401.10020. <https://arxiv.org/abs/2401.10020>. The optimistic case: a model that judges itself well can train itself. SelfJudge asks whether the premise holds below 30B.
5. Zhang, L. et al. (2024). *Generative Verifiers: Reward Modeling as Next-Token Prediction.* arXiv:2408.15240. <https://arxiv.org/abs/2408.15240>. Judging framed as generation; the reason a chat model can be a judge at all without a separate reward head.
6. Chen, N. et al. (2025). *JudgeLRM: Large Reasoning Models as a Judge.* arXiv:2504.00050. <https://arxiv.org/abs/2504.00050>. Trains small reasoning models specifically to judge; a reference point for what purpose-built small judges reach.
7. Zhang, T. et al. (2025). *CompassJudger-2: Towards Generalist Judge Model via Verifiable Rewards.* arXiv:2507.09104. <https://arxiv.org/abs/2507.09104>. A 7B-class generalist judge model; shows judging skill at the sizes SelfJudge tests.
8. Bandyopadhyay, S. (2026). *Can LLMs Judge Better Than They Generate? Evaluating Task Asymmetry, Mechanistic Interpretability and Transferability for In-Context QA.* arXiv:2606.28050. <https://arxiv.org/abs/2606.28050>. The judge-versus-generate asymmetry that SelfJudge measures from the deployment side.
9. Lin, W. et al. (2025). *Do Before You Judge: Self-Reference as a Pathway to Better LLM Evaluation.* arXiv:2509.19880. <https://arxiv.org/abs/2509.19880>. A judge that first answers the question itself; relevant to why self-assessment and anchor judging differ.
