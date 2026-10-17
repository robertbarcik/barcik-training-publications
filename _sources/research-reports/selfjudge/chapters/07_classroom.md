# Classroom notes

This chapter is for the trainer who projects the report in a workshop. It is the version I teach from.

> **Classroom notes**
>
> **The one slide.** Figure 1. Ask the room where they expect the curve to flatten before you show it. Most people guess 14B or higher. The knee at 3B is the surprise and the lesson.
>
> **The second slide.** Figure 4. "Grading a stranger's homework is easier than grading your own." Every model in the set, including the closed one, scores lower on its own output than on the planted set. That is self-leniency, not a lack of skill.
>
> **The trap to name.** 50% on a balanced set is what "always say PASS" scores. A model that passes everything looks confident and is useless. Whenever someone shows you a judge accuracy, ask what the always-PASS baseline was.
>
> **The on-device argument.** If the model you ship is 3B or larger from a 2025 or later generation, it can run a sanity pass on its own output at roughly 93 to 98% accuracy on explicit flaws. Keep a second, independent check for the failures it is lenient about: a rules-based detector for format and safety, and a periodic audit by a bigger model.

> **Discussion questions**
>
> 1. Why is "judging skill" measured on planted answers rather than on the model's own answers? What would go wrong if we only measured the second?
> 2. Self-leniency is positive for every model. Suggest two mechanisms that could cause it, and an experiment that would tell them apart.
> 3. A vendor claims their 1B model "self-verifies every answer." Which figure in this report would you show them, and what question would you ask next?
> 4. The closed model on the chart scores like the best open ones. Why is that *not* an argument for sending the data to the cloud?

> **Key takeaways**
>
> - Judging skill switches on between 1B and 3B and plateaus; bigger is not better past about 4B active parameters.
> - Self-assessment lags judging skill for every model. Plan for self-leniency.
> - A balanced planted set with ground truth by construction is the cheapest honest judge benchmark you can build yourself.
