---
date: 2026-03-22
topic: critical evaluation of AI output
---

## Lesson
You are the editor, not the author. Never accept an AI output you can't fully explain.

## What happened
When building workflow automations and reviewing AI-generated plans, I noticed that when things didn't work consistently, it was usually because I had accepted a plan without fully understanding the decisions inside it. The AI wrote with confidence, I approved it, and the hidden assumptions only surfaced when something broke.

The realization: I was evaluating AI output by whether it *looked* right, not whether I could explain *why* every decision was made. If I can't explain a decision, I don't own it — the AI does.

## Why it matters
The AI fills gaps with assumptions. It makes architectural choices, picks libraries, handles edge cases — and presents all of it with the same confidence as the things you explicitly asked for. The tells:
- **Unexplained choices** — it picked something without saying why
- **Scope expansion** — the plan does more than you asked
- **Missing edge cases** — happy path is clear, failure cases aren't addressed
- **Confident language about uncertain things** — "this will scale" without proof

The fix is not more prompting upfront. It's interrogation at the plan stage, before anything gets built.

## The questions to ask every time

**To surface hidden assumptions:**
- "What are you assuming that I haven't told you?"
- "What did you have to guess because I didn't specify it?"

**To find the riskiest decisions:**
- "What's the riskiest decision in this plan?"
- "What would break first if this goes wrong?"

**To check scope:**
- "What did you add that I didn't explicitly ask for?"
- "What would you cut if you had to?"

**To stress-test the approach:**
- "If we had twice as long, how would you build this differently?"
- "What cases are you not handling?"
- "What input would break this?"

**The final check before building:**
- "Explain what you're about to build in plain English — not the plan, just what you're doing and why."
  If the explanation isn't clear, the plan isn't ready.

## The mental checklist (before accepting any AI output)
- Does this make sense to me?
- Do I understand what's about to happen?
- Am I blindly accepting something I don't fully understand?
- Did I interrogate enough?
- Did I ask the AI to interrogate itself?
- Do I have control — could I explain this to someone else?

If any of these is no: don't proceed. Ask the question first.

## This transfers everywhere
This posture — editor, not author — applies to any AI output at work: analysis, writing, strategy, code. The people who get the most out of AI are not the ones who write the best prompts. They're the ones who read output critically and know what questions to make it better.

Stop evaluating AI output by whether it looks right. Evaluate it by whether you can explain why every decision was made.

## LinkedIn draft
The most important skill in working with AI isn't prompting.

It's editing.

When AI gives you a plan, a design, a piece of code — that's a first draft. Your job is to read it the way a good editor reads a manuscript: not to admire it, but to find where the logic is weak, where assumptions snuck in, where the author took shortcuts they hoped you wouldn't notice.

The AI writes with confidence. It doesn't flag its guesses. It'll make an architectural decision and present it as the obvious choice — because in its training, it often was. But "obvious in training data" is not the same as "right for your situation."

The questions that surface what's hidden:
- "What are you assuming I didn't tell you?"
- "What's the riskiest decision in this plan?"
- "What did you add that I didn't ask for?"
- "If we had more time, how would you build this differently?"

And before anything gets built: "Explain what you're about to do in plain English." If the explanation isn't clear, the plan isn't ready.

The shift: stop evaluating AI output by whether it *looks* right. Evaluate it by whether you can *explain* why every decision was made.

If you can't explain a decision, you don't own it. The AI does.

That's the difference between using AI and being used by it.
