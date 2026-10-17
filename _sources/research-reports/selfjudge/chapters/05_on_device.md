# What it means for an on-device deployment

The question that started this was practical: if the model runs on the device, can it be its own judge, so that the deployment does not need a second, larger model on the side? The answer has three parts.

**Yes, for explicit flaws, from 3B up.** A current-generation model with three billion or more active parameters catches planted factual errors, injected instructions, contradictions and tone failures at roughly 95%, and the mixture-of-experts models do it with the memory footprint of a 3B dense model and the speed of one. Bonsai 2 shows that aggressive weight compression does not take this away. For a pipeline that needs a cheap first gate, "ask the same model to grade the answer against the source" is a reasonable design and costs one extra call.

**No, for its own blind spots.** The same models miss a third to four fifths of their own failures while catching the planted ones. A self-judge is weakest exactly where you need it: on the errors the model is prone to make. Self-assessment accuracy of 89 to 98% on the current models looks reassuring until you remember that most of those answers were correct anyway; the "always PASS" baseline in the per-model data is often within a few points.

**So the on-device judge is one layer, not the layer.** A design that follows from the numbers:

1. **The model grades itself against the source**, with the judge prompt from this experiment or one like it, and the verdict is logged. This catches the explicit failures and costs nothing extra in hardware.
2. **A rules-based check runs beside it** for anything that can be checked without a model: output format, length limits, forbidden strings, required citations. Instruction following is the category where small judges are weakest and where rules are strongest.
3. **An independent judge audits a sample.** Not every answer, and not necessarily a frontier model: a *different* small model from another family would already remove the self-preference, since cross-judging in this experiment shows models catching peers' failures they would have waved through in themselves. Run it on a slice in the background and watch the disagreement rate.
4. **Measure your own leniency.** The planted-anchor method is cheap to reproduce for your own domain: write twelve prompts, one good and one bad answer each, and ask your deployed model to grade them blind. If it scores under 90% on your anchors, the first layer is not ready; if it scores 95% on anchors and 70% on its own answers, you have the self-leniency gap and you know how much the audit layer has to carry.

> **Classroom notes**
>
> **The deployment story in one sentence.** The model you ship can be its own first reviewer, never its only reviewer.
>
> **What to show.** Figure 1 for the step, Figure 4 for the gap, then the four-layer design above as a slide.
