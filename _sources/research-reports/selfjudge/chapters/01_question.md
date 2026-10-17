# The question

Small language models are the ones that end up on real hardware: a laptop, a phone, a branch-office server, a factory PC with no internet. They are cheap, private and fast. They also fail, and somebody has to notice.

The textbook answer is a second, larger model that reads every output and grades it. In the cloud that is normal practice. On the edge it defeats the purpose: if a 3B model needs a 70B judge, the deployment is a 73B deployment with extra steps.

So the practical question is simple to state. **If a small model runs on the device, can the same model be its own judge?** Can it read its own answer and say, reliably, "this is wrong"?

That question splits into three measurements, and the split is the point of the whole experiment.

1. **Judging skill.** Given a response whose correctness is known for certain, does the model grade it correctly? This has nothing to do with whose response it is.
2. **Self-assessment.** Given its *own* response, does the model grade it correctly? Now the ground truth is noisier and the response is familiar.
3. **Self-leniency.** Does the model miss its own failures more often than it misses identical-looking failures written by someone else?

A model can be a competent judge and still a useless self-judge, because the second and third measurements can fail while the first succeeds. The literature on self-preference bias in large judges says exactly this [2][3]. SelfJudge checks whether the same thing happens at one to thirty billion parameters, where it matters for the people who have to ship a device.

> **Key takeaways**
>
> - "Can it judge?" and "can it judge *itself*?" are different questions with different answers.
> - Judging skill is measured on planted answers with ground truth by construction. Self-assessment is measured on the model's own answers.
> - The gap between the two is the honest number for anyone planning an on-device quality gate.
