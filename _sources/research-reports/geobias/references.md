# Related work

A short reading list, not a survey. Every title below was checked against its arXiv abstract page on 2026-10-17.

1. Santurkar, S. et al. (2023). *Whose Opinions Do Language Models Reflect?* arXiv:2303.17548. <https://arxiv.org/abs/2303.17548>. Introduces OpinionQA and the method of asking whose demographic opinions a model's answers resemble.
2. Durmus, E. et al. (2023). *Towards Measuring the Representation of Subjective Global Opinions in Language Models.* arXiv:2306.16388. <https://arxiv.org/abs/2306.16388>. Anthropic's country-level version of the same question; the closest ancestor of GeoBias's origin-by-topic matrix.
3. Naseh, A. et al. (2025). *R1dacted: Investigating Local Censorship in DeepSeek's R1 Language Model.* arXiv:2505.12625. <https://arxiv.org/abs/2505.12625>. Measures censorship in locally run weights, the "is it in the weights or in the API?" question GeoBias asks of smaller models.
4. Qiu, P. et al. (2025). *Information Suppression in Large Language Models: Auditing, Quantifying, and Characterizing Censorship in DeepSeek.* arXiv:2506.12349. <https://arxiv.org/abs/2506.12349>. A larger audit of politically sensitive topics on one Chinese-origin model.
5. Deng, Y. et al. (2024). *Multilingual Jailbreak Challenges in Large Language Models.* ICLR 2024, arXiv:2310.06474. <https://arxiv.org/abs/2310.06474>. Safety behaviour changes with the prompt language; the reason GeoBias includes a language-quality category.
6. Verga, P. et al. (2024). *Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models.* arXiv:2404.18796. <https://arxiv.org/abs/2404.18796>. The case for a panel of judges from different families; GeoBias's three-origin evaluator panel follows it.
7. Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv:2306.05685. <https://arxiv.org/abs/2306.05685>. The founding LLM-as-a-judge paper and its catalogue of judge biases, which the evaluator-leniency check is designed to catch.
