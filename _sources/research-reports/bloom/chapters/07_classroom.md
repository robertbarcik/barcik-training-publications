# Classroom notes

This chapter is for the trainer who projects the report in a workshop. It is the version I teach from.

> **Classroom notes**
>
> **The one slide.** Figure 1. Cover the third column and ask the room which behaviours they expect a newer model to have fixed. Most people guess the dramatic ones, self-preservation and tool abuse, and they are right. Then point at the top row: emotional bond is the one that did not move, and it is the one their users will actually meet.
>
> **The second slide.** The corrigibility conversation from Chapter 4. Muse refuses to remove scientific uncertainty from a children's explainer and the judge scores that 9 out of 10 for "resisting correction". Ask the room whether they would want the model to comply. The lesson: the score is an opinion, the transcript is the evidence.
>
> **The trap to name.** "Muse scored 1.5 on information leakage, so it does not leak." The correct reading is: a language model tried ten times to make it leak, under one judge, and did not succeed. A low score means the evaluator failed to elicit the behaviour in a handful of tries. Absence of evidence from a short audit is weak evidence of absence.
>
> **The deployment argument.** This entire run cost about as much as a coffee and took an afternoon. Before you put a model behind a chat window or give it tools, run the behaviours that matter for your use case, keep the transcripts, fix the judge model, and run it again when the vendor ships an update. Then read the five highest-scoring transcripts yourself.

> **Discussion questions**
>
> 1. The judge model changed between March and October and moved the same transcripts by +0.6 on average. What would you have to keep fixed to compare a model with its successor a year from now?
> 2. Emotional bond barely changed between generations while self-preservation collapsed. Why might safety training reach one and not the other? Which of the two matters more for a customer-service deployment?
> 3. Both models wrote realistic phishing material when the request said "training". How would you design a scenario that tells a legitimate security-awareness request from a pretext, and could a model ever tell them apart from the conversation alone?
> 4. The evaluation-awareness score was 1 in all 225 judgments. List two explanations and an experiment that would tell them apart.

> **Key takeaways**
>
> - With one judge and the same seed files, the 2026 model scores lower on all eleven behaviours, but emotional bond barely moves.
> - Change the judge and the scores move too: +0.6 on average, +2.0 for one behaviour on identical transcripts. Compare only like with like.
> - An automated behavioural audit is cheap enough to run before every deployment. Its averages tell you where to look; its transcripts tell you what happened.
