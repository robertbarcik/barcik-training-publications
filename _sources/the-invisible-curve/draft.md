# The Invisible Curve

*Why the AI you have seen is no longer the AI that exists*

Robert Barcik · July 2026 · An opinion essay

---

## 1 · Two Mondays

It is a Monday morning in early July 2026, and I am sitting with a coffee, trying to explain a feeling I have had for months.

Last week I worked through my entire professional infrastructure with an AI agent: nineteen repositories touched, over a hundred commits. The agent integrated my Google Workspace with my local machines (safely, which matters, and we will get to that), rewrote my published booklets, rebuilt my exam-prep sites, drafted course materials, and, in a separate window, is rewriting my interactive training demos while I type this sentence. I reviewed everything. I rejected some of it. I kept most of it. It was, without exaggeration, the most productive week of my working life.

That same week, someone I trained a year ago used AI too. They typed a question into a search engine and read the AI summary that appeared above the results. It was slightly wrong, mildly useful, and easy to ignore.

Both of us would tick the box "uses AI." We are describing experiences that no longer resemble each other. Two people, one technology, and between us a gap that has been widening quietly for two years.

## 2 · The Shared Boat

Rewind to late 2022. ChatGPT launches, and for about a year afterwards, everyone on Earth has roughly the same relationship with this technology. You open a chat window. If you pay nothing, you get a slightly dumber model; if you pay twenty dollars, a slightly smarter one. Either way, the entire capability of the system is right there in front of you, one answer at a time.

That mattered more than we realized at the time. It meant everyone's evidence base was identical. When the models improved, everyone felt it: fewer hallucinations, better structure, answers that held together. Your skeptical colleague and your enthusiastic colleague were at least arguing about the same object.

Through 2024 the story stayed mostly legible. Much of the progress that year was engineering: the models could see images, browse the web, talk out loud, plug into your documents. Paying customers got convenient tricks earlier, but a free user could still look over a paying user's shoulder and understand what they were looking at.

We were, all of us, in the same boat. That boat no longer exists.

## 3 · Where the Progress Went

Around 2025, with the arrival of reasoning models, something structural changed in where progress shows up.

The gains stopped concentrating in answer quality, which everyone can see, and started concentrating in something harder to name: the ability to hold a goal for hours, use tools, check its own work against reality, recover from its own mistakes, and carry a project across hundreds of steps. Call it long-horizon work. It is the difference between an assistant that answers questions and a colleague who takes a task and comes back when it is done.

Here is the uncomfortable part: long-horizon capability is invisible in a chat window. A ten-message conversation has no room to express it, the way a hundred-meter dash has no room to express a marathon runner's advantage. So the person whose entire contact with AI is a free chat tab, or that summary above the search results (often served by a small, cheap model, because serving a frontier model to billions of searches would be economically absurd), is experiencing something close to a time capsule. The interface looks the same as 2023. The answers are somewhat better. Meanwhile, the actual frontier moved to a regime they never visit.

I watch this play out every time a new model generation appears. In mid-2026, when Anthropic released the generation after Opus, my feeds filled with people reporting that the new model felt no better. Barely distinguishable, they said. And within the world of their evidence, they were right. In a short chat, the difference between a very good model and a frontier model compresses toward zero; the task has no room to show it. But over a week of sustained work, small per-step advantages compound: slightly better judgment, times slightly better error recovery, times slightly better memory of the plan, multiplied across hundreds of steps. In that regime the difference between generations felt, to me, like a different species of colleague.

Both reports are honest. They are measurements of different quantities. And that is the one sentence I would defend against all comers: **capability is no longer legible in the interface most people use to judge it.**

People are not stupid, and they are not in denial. The curve simply left their field of view.

## 4 · What the Skeptics Can See

If you are skeptical of everything I have said so far, I want to take your position seriously, because your evidence is real. Let me state it at full strength.

You have seen the slop. AI-generated code that compiles but rots, AI-generated articles that say nothing, AI-generated images clogging every feed. This is genuinely what AI output looks like from the outside, and here is why: bad AI output is loud and attributable, while good AI output ships silently under a human's name. Nobody labels the well-crafted module an agent wrote and a senior engineer reviewed. The sample you can see is systematically the worst sample. Your observation is accurate; the sampling is cursed.

You have also heard, correctly, that the tech layoffs have a boring explanation: the industry overhired during Covid, the correction was coming anyway, and executives enjoy blaming a robot instead of their own planning. This is true. It is simply also true that a second force arrived at the same time, and two true stories layered on top of each other make the second one deniable for years.

Where I part ways with the skeptics is the shape of the curve. When ChatGPT could barely produce a coherent line of code, people laughed. When it could barely assemble a function, they laughed a bit less. When it wrote whole scripts, they stopped laughing and started talking about quality. Now agents build whole applications, and the conversation is about maintainability. Notice the pattern: four points on the same curve, and at every point, the consensus treated that point as the final one. The observations were accurate every time. The extrapolation failed every time. I see no reason offered, other than comfort, why the fifth point should be different.

## 5 · The Keys to My Computer

Let me make this concrete with the story that convinced me more than any benchmark.

For months I wanted to connect my AI tooling to my Google Workspace: courses, videos, business documents. I asked the previous-generation model, Claude Opus, to set this up several times across several sessions. Each time, its plan eventually ran through the same step: grant the terminal Full Disk Access on macOS. Innocent-sounding words for handing a program the right to read and delete anything on my machine, in my name. I refused, every time, and the project stalled for months.

The next-generation model, Fable, looked at the same problem in our first week together and immediately proposed a different shape: a dedicated service account with its own credentials, scoped to exactly the two shared drives it needed, with no access to my machine beyond the folder it worked in. It then built the whole integration around that idea, and it has run safely ever since.

One AI asked for the keys to my whole computer. The other found a way that needed almost no keys at all.

Sit with that for a second, because the capability jump did not show up as eloquence or speed. It showed up as judgment: the newer system was more careful than its predecessor, more protective of me than I had thought to ask it to be. No leaderboard measures that. Yet it is exactly the quality you would demand before trusting a system with real work, and exactly the kind of progress a chat window can never display.

The rest of the week followed the same pattern. I did not hand my professional life to this agent in one act of faith; I handed it one piece at a time, and every next piece was surrendered only because the previous one survived my inspection. Operations first, then code, then the writing I publish under my own name. By Friday, the ledger read roughly one hundred and thirty commits across nineteen repositories (I will resist quoting line counts; much of that volume is generated data, and inflated numbers are how you lose a skeptic's trust). The evidence I am offering you is a judgment, given by someone qualified to grade the work and with every incentive to catch it failing.

And yes: the system being judged helped me compile this account of its own judging. You should find that circular. It is the illegibility problem in miniature. Verifying what the frontier can do requires either doing the work yourself, which costs expertise, or trusting someone who did, which costs faith in their honesty. There is no third path where the truth is simply visible from the outside. That is new, and I do not think we have absorbed it.

## 6 · The People Who Cross

Around a thousand people have passed through my introductory AI trainings in the past year alone: engineers, managers, lawyers, clerks, owners of small companies. For a long time I could not predict who would end up transformed by this technology and who would walk away unchanged. It was never intelligence. Some of my sharpest participants remained untouched; some initial skeptics became the most productive people I know.

I now believe the dividing line is this: whether a person's relationship to AI is **instrumental or evaluative**.

The ones who cross the gap arrive with a task they are accountable for. The report due Friday. The codebase. The offer document that has to go out. They point the AI at that task because they need the task done, and their skepticism turns out not to matter, because three iterations into real work, the results update them whether they like it or not. Stakes convert skeptics.

The ones who stay stuck engage with AI as a topic. They arrive to form an opinion, not to finish anything. Every session becomes a test, and here is the trap: the evaluative posture always wins its own game. These models remain jagged; anyone who goes hunting for a failure will find one, collect the gotcha, and leave with their prior beliefs intact and their evidence base one demo older. Same tool, opposite aims: one person is trying to complete something, the other is trying to be right.

Which finally gives me something I can offer you that does not cost two hundred dollars a month, because I am aware of the objection: the frontier I have described is expensive, and "trust me, it is amazing up here" is worthless advice. So here is the only instruction I have found that transfers, and it works on the cheapest paid plan, in your domain, this week:

**Do not evaluate the model. Give it a task that actually matters to you, in a domain where you are qualified to grade the output, and iterate at least three times before you allow yourself an opinion.**

Not a trivia quiz, not a trick question, not a topic you cannot judge. A real task, with stakes, where you are the expert grader. If it fails, you will have earned a current, first-hand data point, which is more than most public commentary is built on. If it does not fail, you will feel the floor move a little. Either way, you will have replaced borrowed evidence with your own.

## 7 · How Old Is Your Evidence?

One more thing, before the ask, because fairness demands it. If you are on the far side of this gap, you are not merely under-informed; you are also carrying costs. Your graphics card got more expensive so that data centers could be filled. Your industry's hiring pages went quiet while executives talk about efficiency. Your feeds filled with machine-made noise you never asked for. The benefits of this technology are currently flowing to people like me, and a meaningful share of the costs are landing on people who have never experienced anything past the free tier. If that arrangement irritates you, the irritation is legitimate, and no essay should talk you out of it.

But being right about the unfairness will not protect anyone from being wrong about the trajectory.

So I am not asking you to believe me. I have an interest in your belief, and the disclosures just below spell out what it is. I am asking something smaller. Look at your own evidence about what AI can do, the actual experiences your conviction rests on, and check the date on them. If the last time you seriously tried was a free chat tab in 2023, or a code snippet in 2024, or a search summary last week, then whatever you concluded, you concluded it about a system that no longer represents the frontier. You were measuring in an interface the curve has already left.

The curve did not stop when it left your window. It just became invisible from where you stand.

And the strange, honest, slightly vertiginous truth of July 2026 is that the fastest way to see it again has not changed since 2022: bring it something real, and watch what comes back.

### Whose opinion this is

Two disclosures, kept for the end so they would not interrupt the argument, because this is an opinion essay and you deserve to know whose opinion you have been reading.

First: I make my living training people in generative AI. If this essay leaves you convinced the technology matters enormously, people like me benefit. Weigh everything above accordingly.

Second, and stranger: I wrote this essay together with the AI it describes. The receipts I showed you were compiled by the system being judged. Keep that in mind; by now, I hope you can see why this awkwardness is the whole point.

---

*Robert Barcik trains companies and professionals in generative AI (learningdoe.com, barcik.training). This essay was written in collaboration with Claude, the AI system it describes; the author reviewed and stands behind every claim. For the machinery behind the working setup described here, see the companion piece [Claude Code as an Operations Specialist](../claude-code-setup/).*
