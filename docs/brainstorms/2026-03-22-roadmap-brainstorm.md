# Roadmap Brainstorm: V1 Polish → Agentic Patterns → V2 Vision
**Date:** 2026-03-22 (consolidated from 2026-03-21 V2 brainstorm and 2026-03-22 V1 improvements brainstorm)
**Status:** Active

---

## Core Insight

Aggregation is table stakes. The real problem is:

> You read something, it feels useful, and then it disappears. A week later you can't recall it. You can't talk about it. You can't apply it.

Even a well-designed digest can recreate the original problem — just organized differently. Instead of scrolling an email inbox, you scroll a dashboard. The noise is reduced but the depth isn't there.

What's missing is the path from **exposure → understanding → retention → application**.

The full loop we're building toward:

```
Ingest → Filter → Synthesize → Reflect → Retain → Apply
```

V1 covers the first three. The layers below map to where we are and where we're going.

---

## Current Pipeline (What's Built)

Three LLM calls chained in a fixed pipeline — not true agents, just structured inference:

| Step | Type | Model | What it does |
|---|---|---|---|
| Ingest | Deterministic | — | RSS + YouTube transcript fetch |
| Dedup | Deterministic | — | Jaccard similarity on headlines |
| Score | LLM call | Haiku | 1–10 relevance against persona + topics |
| Cluster | LLM call | Sonnet | Groups items into thematic clusters |
| Synthesize | LLM call | Sonnet | Headline + synthesis + why it matters per cluster |

None of these have tool calls, reasoning loops, or the ability to gather more information. They get a fixed input and return structured JSON. The pipeline is fixed — no step can decide to re-run or adapt based on results.

---

## Layer 1: V1 Polish (Tactical — implement now)

Three concrete gaps surfaced from the first real run on live data.

### 1.1 Day Selector on Dashboard

**Problem:** Dashboard defaults to today. No way to navigate to previous days in the UI. The backend already supports `?date=YYYY-MM-DD` but it's not surfaced.

**What to build:** Prev/next day navigation in the daily template, plus a date picker or dropdown showing available digest dates pulled from the DB.

**Notes:**
- Only show dates that have a digest in the DB (not all calendar dates)
- Prev/next arrows are the minimum; a dropdown of available dates is nicer
- Route already works — this is purely a template change

### 1.2 Relevance Scoring Criteria

**Current state:** Haiku uses a 1–10 scale with these descriptions:
- 9-10: Must-read. High-signal, directly relevant to the reader's work and interests.
- 7-8: Worth reading. On-topic and useful.
- 5-6: Marginally relevant. Tangentially related.
- 3-4: Low relevance. Loosely related but not useful.
- 1-2: Not relevant. Off-topic or noise.

It receives `persona` and `topics` from config.yaml as the only context. No deeper rubric.

**Levers:**
- Tuning `persona` in config.yaml is the highest-impact change
- Tuning `topics` to be more specific drives better signal
- `relevance_threshold` (currently 6) controls the cutoff — raise to 7 for stricter filtering
- The scoring prompt itself could be expanded with negative examples ("do NOT score highly if...")

**Open question:** Should we expose scores in the dashboard so the user can see why something made the cut?

### 1.3 Hosted Dashboard (No Local Setup)

**Problem:** Currently requires running `python3 -m src.run --daily` locally and `uvicorn` locally to see anything. Not sustainable.

**Option A — Hosted dashboard (Fly.io / Railway / Render)**
- Deploy FastAPI app as always-on service
- Run pipeline as a scheduled job (cron on the same host, or GitHub Actions writing to a hosted DB)
- Accessible from any browser
- Cheapest options: Render free tier, Railway ~$5/mo, Fly.io ~$3/mo

**Option B — Push delivery (email or Slack)**
- Pipeline runs on GitHub Actions (already planned for 6am daily)
- Formats digest and sends via email (SendGrid/Resend) or Slack webhook
- No hosting needed — just an API key
- Less interactive but zero infrastructure

**Option C — Both**
- GitHub Actions runs pipeline + sends email
- Dashboard also deployed for browsing history

**Leaning toward:** Option A or C — the dashboard view is valuable for browsing history, which push delivery doesn't solve. Render or Fly.io are the simplest deploys.

---

## Layer 2: Agentic Pattern Improvements (V1 Quality — demonstrate real agent design)

The current pipeline makes uninformed decisions because each step gets a fixed input with no ability to gather more information. These patterns introduce real agentic properties — tool calls, reasoning loops, feedback cycles — that improve output quality and demonstrate advanced agent design.

### 2.1 ReAct Scoring Agent (Reason + Act loop)

**Problem:** The scoring agent gets 300 characters of content and makes a relevance judgment. A lot of articles can't be judged from a snippet — weak snippets cause false negatives (relevant articles dropped) and strong headlines cause false positives (low-quality articles that pass).

**Pattern:** ReAct — Reason + Act loop

**How it works:**
1. Read title + snippet
2. Reason: "Can I judge relevance from this? Do I need more?"
3. If uncertain: call fetch tool to retrieve full article
4. Re-evaluate with full content
5. Return informed score with reasoning trace

**Why it fits:** Most natural entry point for tool use in the existing pipeline. Solves a concrete, measurable problem. Canonical ReAct pattern with a clear before/after.

### 2.2 Critic / Self-Reflection Loop on Synthesis

**Problem:** The synthesis agent writes summaries with no quality check. Generic "why it matters" framing, summaries that restate rather than synthesize, no feedback mechanism.

**Pattern:** Writer + Critic feedback loop

**How it works:**
1. Synthesis agent writes cluster summary
2. Critic agent evaluates: "Is this insightful or just a restatement? Does the why-it-matters connect to the persona? Is the headline specific or generic?"
3. If critique fails: synthesis agent revises with critic feedback
4. Loop until quality threshold met or max iterations reached

**Why it fits:** Demonstrates agent feedback loops and self-correction. Directly improves the most user-facing output in the system.

### 2.3 Orchestrator + Subagents

**Problem:** The pipeline in `digest.py` is a fixed sequence. If too few items pass scoring, it doesn't adapt. If a cluster is too large or incoherent, it doesn't re-cluster. Every run follows the same path regardless of what the data looks like.

**Pattern:** Orchestrator agent coordinating specialist subagents

**How it works:**
- Orchestrator receives ingested items and decides the execution path
- Calls scoring subagent, evaluates results ("only 3 items passed — lower threshold and re-score?")
- Calls clustering subagent, evaluates ("one cluster has 40 items — re-cluster with tighter constraints?")
- Calls synthesis subagent per cluster
- Makes adaptive decisions at each step rather than executing a fixed sequence

**Why it fits:** Most architecturally significant pattern. Shows multi-agent coordination and adaptive pipelines. Makes the system genuinely resilient to varying data volumes.

### 2.4 Source Discovery Agent

**Pattern:** Autonomous tool use for expanding the system's own inputs

**How it works:**
- Runs weekly
- Looks at what scored highest over the past week
- Uses web search tools to find new RSS feeds and sources in those topic areas
- Evaluates source quality and relevance
- Proposes additions to config.yaml for user approval

**Why it fits:** Demonstrates autonomous decision-making and tool use outside the main pipeline. The system improves its own inputs over time.

---

## Layer 3: V2 Vision (Strategic — parked until V1 is solid)

### The Connection Layer

The missing piece is not a new tool — it's a bridge between the news aggregator and the existing knowledge base.

Today they're two silos:
- News aggregator surfaces what's happening
- Personal knowledge base stores what you know
- Nothing connects them

The V2 layer bridges: "today I read X → this connects to what I already know about Y → here's what it suggests you're missing → here's how you'd use it in an interview answer."

### Digest Enhancement
- Top-of-digest synthesis: "From today's content, here are 3 key themes and why they matter to you specifically as an AI PM interviewing at big tech"
- Gap identification: "Based on what came in today, here's a concept you should understand better"

### Reflection Interface
- After reading, ability to chat with the digest — interrogate ideas, ask follow-up questions
- Not passive reading but active engagement
- An agent that can read the digest, query your knowledge base, and answer "what does this mean for me?"

### Knowledge Base Integration
- User adds existing notes/knowledge into the system
- New articles build on and connect to what you already know
- Surfaces "you already know X — today's articles extend that with Y"
- Agent with retrieval tools (search notes, search prior digests) — the *decision about what to look up* is the agentic part

### Retention Layer
- Save insights from digests
- Spaced repetition surfaces old insights at the right time
- Knowledge compounds visibly over time

### Open V2 Questions (parked)
- How does the reflection interface work — chat UI in the dashboard, or something else?
- How does the knowledge base integration work — does the aggregator read from personal-os files, or does the user paste knowledge in?
- What does "saving an insight" look like — a note, a card, a tag?
- Spaced repetition mechanism — built-in or integrate with existing tool (Anki, Readwise)?
- Does V2 stay local (personal tool) or become multi-user (public product)?

---

## Layer 4: V3 / North Star

- Interview prep mode: "based on what you've been reading this month, here's a practice question"
- Pattern recognition across weeks: "this is the third time agents have come up — here's the emerging story" — a longitudinal agent that queries digest history, identifies recurring themes, and surfaces trend narratives
- Export to personal OS / notes
- Multi-user hosted product

---

## Competitive Landscape (Summate.io — researched 2026-03-21)

**What Summate does well:**
- Hierarchical custom AI instructions (account → digest → source block level)
- Pre-built digest templates for cold-start onboarding
- Credit transparency (1 credit per article)
- Clean scheduling and delivery
- Active product development cadence

**Summate's gaps = our opportunity:**
- No relevance scoring — summarizes everything indiscriminately (we have this)
- No deduplication across sources (we have this)
- No reflection or interrogation layer
- No knowledge compounding or spaced repetition
- No connection to existing personal knowledge
- English-only, no mobile app, browser extension paused
- No Reddit, Twitter/X, podcast sources

**Our differentiators already built in V1:**
- Claude relevance scoring filters before summarizing
- Jaccard deduplication across sources
- Clustering to group related stories

---

## The Differentiated Vision

**"An AI learning companion that aggregates what's happening in AI, connects it to what you already know, surfaces your knowledge gaps, and helps you compound understanding over time."**

Nobody does this end-to-end. Summate does aggregation. Readwise does retention. Nobody connects them with a personalization layer that knows your context (AI PM, interviewing at big tech, building products).

The product arc:
- **V1:** One place to see everything important in AI today
- **V2:** One place to understand what it means for you
- **V3:** One place where your AI knowledge compounds over time

---

## What V1 Needs to Be Rock Solid First

Before any V2 work, V1 must be genuinely solid:

- [ ] More sources in config.yaml — need enough volume to feel the real synthesis value
- [ ] Dashboard rendering cleanly across different content volumes
- [ ] Scoring and clustering feeling accurate on real diverse data
- [ ] GitHub Actions running reliably on schedule
- [ ] End-to-end feeling genuinely useful daily, not just technically working

**The test:** after one week of daily use, does the digest feel worth reading every morning and actually worth retaining? If yes, V1 is solid. If not, fix V1 first.

---

## Next Steps (ordered)

**Layer 1 — V1 Polish:**
- [ ] Implement day selector in dashboard template
- [ ] Decide on hosting target (Fly.io vs Render vs Railway)
- [ ] Deploy pipeline + dashboard to chosen host
- [ ] Optionally: expose relevance scores in dashboard UI

**Layer 2 — Agentic Patterns:**
- [ ] ReAct scoring agent (start here — most contained, clearest ROI)
- [ ] Critic loop on synthesis
- [ ] Orchestrator + subagents
- [ ] Source discovery agent

**Layer 3+ — defer until V1 is solid and agentic patterns are in place**
