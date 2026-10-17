# Related work

A short reading list, not a survey. Every arXiv title below was checked against its abstract page on 2026-10-17; the Anthropic pages were opened the same day.

1. Gupta, A. et al. (2025). *Bloom: an open source tool for automated behavioral evaluations.* Anthropic Alignment Science blog, 19 December 2025. <https://alignment.anthropic.com/2025/bloom-auto-evals/>. The framework this report uses: understanding, ideation, rollout and judgment stages. Code: <https://github.com/safety-research/bloom>.
2. Meridian Labs (2026). *Bloom: Automated Behavioral Evaluations for LLMs.* <https://meridianlabs-ai.github.io/petri_bloom/>. The current home of Bloom and Petri after the original repository was frozen; the successor to the version used here.
3. Anthropic Alignment Science (2025). *Petri: An open-source auditing tool to accelerate AI safety research.* 6 October 2025. <https://alignment.anthropic.com/2025/petri>. Bloom's sibling: an auditor agent that probes a target over many scenarios; Bloom specialises it to one named behaviour at a time.
4. Lynch, A. et al. (2025). *Agentic Misalignment: How LLMs Could Be Insider Threats.* arXiv:2510.05179. <https://arxiv.org/abs/2510.05179>. The study behind the self-preservation and covert-goal behaviours tested here.
5. Sharma, M. et al. (2023). *Towards Understanding Sycophancy in Language Models.* arXiv:2310.13548. <https://arxiv.org/abs/2310.13548>. The sycophancy literature behind the delusion-sycophancy and confirmation-bias behaviours.
6. Perez, E. et al. (2022). *Discovering Language Model Behaviors with Model-Written Evaluations.* arXiv:2212.09251. <https://arxiv.org/abs/2212.09251>. The ancestor of letting a model write the evaluation of another model.
7. Rosu, A. and Wang, Y. (2026). *Training Alignment Auditors via Reinforcement Learning.* arXiv:2608.25460. <https://arxiv.org/abs/2608.25460>. Where automated auditing is heading: auditor models trained for the job rather than prompted.
8. Skapars, A. and Manino, E. (2026). *BLOOM-WILT: Logit Tilting for Behaviour Elicitation in Automated LLM Auditing.* arXiv:2608.31105. <https://arxiv.org/abs/2608.31105>. Builds directly on the Bloom pipeline to elicit behaviours more reliably.
