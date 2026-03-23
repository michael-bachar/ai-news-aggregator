---
date: 2026-03-22
topic: critical evaluation of AI output
---

## Lesson
Interrogation is a skill, not a reflex. Know where to focus it, and know when you're done.

## What happened
After establishing the importance of interrogating AI plans, the next question was: how much is enough? Over-interrogating burns time and delays building. Under-interrogating lets hidden assumptions through. The answer is a combination of knowing which decisions deserve scrutiny and having a clear gate for when interrogation is complete.

## Where to focus interrogation

**Product decisions — interrogate hard, every time.**
What the feature actually does, what counts as success, what's in scope, what's not. Only you know this. The AI will fill these gaps with assumptions that look reasonable but may be wrong for your situation.

**Architecture for your specific system — interrogate carefully.**
The AI knows patterns. You know your constraints, your users, your team. This is where "what are you assuming?" matters most. Bring your context explicitly; don't assume the AI has it.

**Technical implementation — trust more, interrogate less.**
How to structure a function, which library to use, how to handle an error. The AI is usually right here. Reserve your energy for the decisions only you can make.

If you interrogate everything equally, you burn energy on the wrong things.

## The gate: when interrogation is done

**You're done when you can answer three questions in plain English:**
1. What are we building?
2. Why are we building it this way?
3. What are we explicitly not building?

If you or I can't answer all three clearly — the plan isn't ready. Not "the plan is perfect." Perfect doesn't exist. The bar is: you understand it well enough to own it.

This is the moment to build. Not before.

## The trap on the other side
Over-interrogating is real. The annotation cycle is 1-3 rounds, not infinite. At some point you learn more from what breaks during the build than from another round of refinement. Interrogation has diminishing returns — recognize when you're refining out of anxiety rather than necessity.

## LinkedIn draft
Interrogating AI output is important. But there's a trap on the other side.

Over-interrogate and you never build. Under-interrogate and hidden assumptions become bugs.

The answer is knowing *where* to focus:

**Product decisions** — interrogate hard. What it does, what success looks like, what's out of scope. Only you know this. The AI will guess, and it will guess confidently.

**Your specific architecture** — interrogate carefully. The AI knows patterns. You know your constraints. Bring your context explicitly.

**Technical implementation** — trust more. How to structure a function, which library to use. The AI is usually right here. Don't waste scrutiny on decisions it handles well.

And know when you're done. The gate is simple:

Can you explain — in plain English — what you're building, why you're building it this way, and what you're explicitly not building?

If yes: build.
If no: one more round.

Not "is the plan perfect." Perfect doesn't exist. The bar is whether you understand it well enough to own it.

That's the difference between productive interrogation and anxious refinement.
