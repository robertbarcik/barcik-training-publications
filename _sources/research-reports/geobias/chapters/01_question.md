# The question

A European company wants to run a language model on its own servers. The open-weight models that fit on one or two GPUs come from three places: China (Qwen, DeepSeek), the United States (Llama, Granite, Nemotron, Phi, Muse) and the EU (Mistral). The Chinese models are often the strongest per parameter and the cheapest to run, and the first question in the room is always the same.

**If I deploy a Chinese-origin model on EU infrastructure, will it behave differently on politically sensitive topics than a US or European model? And is that behaviour in the weights, or only in the vendor's API?**

The second half matters for the deployment decision. A filter in a vendor's hosted API disappears the moment you download the weights and run them yourself. A behaviour trained into the weights comes with you. Audits of DeepSeek's R1 found censorship that survives when the weights run locally [3] and characterised what the model suppresses [4].

The question also has a symmetric version that is asked less often and deserves the same treatment. US models may treat US foreign policy more gently than Chinese policy; EU models may lean toward EU regulatory values. Earlier work on whose opinions language models reflect found that models carry identifiable national and demographic perspectives [1][2]. GeoBias was built to measure all three directions with the same instrument, never treating one origin as the neutral baseline.

## What March 2026 found

The first run, in March 2026, compared five models of 8 to 14B parameters: Qwen3 8B and Qwen3.5 9B from China, Llama 3.1 8B and Phi-4 from the United States, Ministral 8B from the EU. The result was lopsided. Both Chinese models scored 2.4 to 3.3 points lower (on a 10-point scale) on China-sensitive topics than on other regions' topics, the US and EU models showed no comparable gap, and Qwen3 8B answered both prompts about Xinjiang with a scripted Chinese sentence saying it "hasn't learned how to answer this question yet", and returned nothing at all on Xi Jinping and the Communist Party (the March dashboard is archived at [/reports/geobias-7b/](/reports/geobias-7b/)).

## Why run it again in October

Seven months is a full generation in open-weight models. Between March and October 2026 new releases arrived from almost every family in the set: Qwen3.8 and DeepSeek V4.1 Flash from China, Granite 4.2, Nemotron 3.5 Lightning and Muse Glimmer from the United States. Mistral's Ministral line, released in December 2025, is represented by its 8B and 14B models. Two practical questions follow.

1. **Did the new generation change the picture?** If the asymmetry was a property of one model family's training in 2025, it may have moved. If it is a stable policy, it should still be there.
2. **Is the March measurement stable?** Two models from March, Qwen3.5 9B and Ministral 8B, were kept in the October run as a bridge. If their numbers stay put, differences between the two runs are about the new models, not about noise in the instrument.

The October run therefore reuses the March prompts and the March evaluator panel unchanged, with eight subject models from 8 to 30B parameters: the two bridge models plus six new ones, three from China, three from the United States and two from the EU in total.

> **Key takeaways**
>
> - The deployment question has two halves: does origin show, and does it travel with the weights.
> - GeoBias measures all three origins in both directions with one instrument.
> - October 2026 repeats March on identical prompts and judges, with a new generation of models and two bridge models.
