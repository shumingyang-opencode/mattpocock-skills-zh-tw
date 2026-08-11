## The Missing Manual: How To Write Great Skills

This guide distills Matt Pocock's talk **"Building Great Agent Skills: The Missing Manual"** (AI Engineer World's Fair) into a four-gate checklist you can run against any skill you write — or any skill you download. The same checklist is encoded, machine-readable, in the [`writing-for-agents`](writing-for-agents/SKILL.html) skill.

## Skill hell — collecting is not using

We developers seem to be pretty talented at finding different forms of hell for ourselves. A few years ago we had **tutorial hell** — go into a bunch of tutorials, never piece it together. Then **framework hell** — a new JavaScript framework announced every ten minutes. And now we have another one: **skill hell**.

Skill hell is where you have all these skills freely available — download them, contribute to them, figure them out on your own — but you can't tell a good skill from a bad one. You can't see how the pieces all work together, and you don't get the results the skills themselves promise. Bad skills are worse than no skills: they burn your tokens, steal the agent's attention, and steal your trust.

## The checklist — four gates

What's missing is a shared rubric: a way to look at a skill and say "these are the good things, these are the bad things." Here it is. Four gates, in order: **Trigger** (how the skill gets invoked), **Structure** (how the skill is composed), **Steering** (how you get the agent to do what you want), **Pruning** (how you make the skill as small as possible).

## ① Trigger — decide: user-invoked or model-invoked

A skill can be invoked two ways. **Model-invoked** skills carry a description that sits in the agent's context window; the agent reads it and decides to pull the `SKILL.md` in. That description is a **context pointer**. **User-invoked** skills hide the pointer — the description only shows to the user (`disable-model-invocation: true`), so the agent can't trigger them on its own.

Model-invoked sounds strictly better — more flexible, the model can grab it when appropriate. But every model-invoked skill adds **context load**: another description costing tokens on every single request, plus another thing for the agent to think about. A hundred model-invoked skills is a hundred descriptions sitting in context.

User-invoked skills push the cost the other way — **cognitive load** on you. The more user-invoked skills you have, the more you have to keep in your head about which to call when.

The two philosophies map onto real skill sets: **Superpowers** is primarily model-invoked (give the agent superpowers); Matt prefers being in full control — user-invoked keeps the agent's context load small and removes an entire class of problem: "is my skill being called at the right time?" There's no free lunch — pick based on whether you want control or flexibility.

## ② Structure — steps + reference, and a small SKILL.md

A skill is composed of two main units. **Steps** are the step-by-step procedure the skill walks through. **Reference** is any supporting information that helps it walk through those steps. Skills can be all steps, all reference, or both — thinking of them this way makes them much easier to break down and write from scratch.

Then the hard constraint: **make the main `SKILL.md` file as small as possible.** Smaller skills are easier to maintain, easier to audit, and every word you shave is a token shaved from your skills cost, on every request.

The technique for keeping it small is **progressive disclosure**: think about the branches of the skill — the different ways it can be used. Reference material that only matters for one branch is a candidate for removal from the main file. Point the main file at it with a **context pointer** — an external reference file bundled alongside the skill that the agent pulls in only when it needs that branch.

## ③ Steering — leading words and legwork

This is the highest-leverage gate. Agents often don't do what you want because you're not using **leading words** — compact concepts already in the model's pre-training that pack a lot of meaning into a small space. Put the leading word in the skill text; the agent repeats it back to itself in its reasoning, and because it keeps re-emphasizing that word, its behavior follows.

Classic example: agents code **layer by layer** — all the database, then all the schemas, then all the API, then the front end. You could write a paragraph begging them to build something small and working first. Or you put in the leading word **"vertical slice"** — a well-known development term that triggers the agent's priors. You can even verify it worked: watch the reasoning traces, and you'll see the agent muttering "we'll do this as a thin vertical slice."

The second lever is **legwork** — the agent skimps on a step when it can see the finish line. The classic case is plan mode: "ask clarifying questions" never gets enough effort because the agent sees the ultimate goal (create a plan) and rushes toward it. Matt's solution: split the planning into its **own skill** so the agent only sees one step at a time. Hiding the future goal forces focus on the current step. Sometimes giving less information is what makes the work deeper.

## ④ Pruning — no repetition, no sediment, no no-ops

A massive skill is usually a symptom of another failure mode. Run three checks:

**Don't repeat yourself.** Every part should have a single source of truth — one authoritative place, so changing behavior is one edit in one place. Watch for duplication across reference material too.

**Watch for sediment.** When people work on the same shared docs and nobody feels brave enough to delete or modify anyone else's, you end up with a huge pile of often-irrelevant material. If added material isn't relevant for all branches, move it into the right branches — or kill it.

**Hunt no-ops.** These are the classic agent-written-skill disease: things that appear to do something but don't actually influence the agent's behavior. The test is a **deletion test**: delete the paragraph and ask whether the agent's behavior changes. If it doesn't, that paragraph was a no-op. Delete the whole sentence, not trimmed words — and judge disagreements by running the skill, not by debating.

## Where this lives now

All of this was encoded into a skill in Matt's repo — originally called `writing-great-skills`, renamed in v1.1 to [`writing-for-agents`](writing-for-agents/SKILL.html). It's the reference for writing any agent-facing document: skills, `AGENTS.md`/`CLAUDE.md`, specs, tickets. The skill-specific mechanics (frontmatter, model- vs user-invoked, router skills) live in [`SKILL-MECHANICS.md`](writing-for-agents/SKILL-MECHANICS.html). Run this four-gate checklist over any skill you're about to install — or over the SOP that nobody follows.
