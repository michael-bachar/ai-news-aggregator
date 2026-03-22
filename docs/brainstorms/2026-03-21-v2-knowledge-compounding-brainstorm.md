# Brainstorm 2: Beyond Aggregation — Knowledge Compounding
**Date:** 2026-03-21
**Status:** Parked — return after V1 is solid

---

## Context

This brainstorm came out of a competitive review of Summate.io and a reflection on what the real problem is. V1 (ingest → filter → synthesize → dashboard) is built and has run end-to-end on live data. The question was: what comes next, and is V1 actually solving the right problem?

---

## The Core Insight

Aggregation is table stakes. The real problem is:

> You read something, it feels useful, and then it disappears. A week later you can't recall it. You can't talk about it. You can't apply it.

Even a well-designed digest can recreate the original problem — just organized differently. Instead of scrolling an email inbox, you scroll a dashboard. The noise is reduced but the depth isn't there.

What's missing is the path from **exposure → understanding → retention → application**.

---

## The Full Loop (What We're Actually Building Toward)

```
Ingest → Filter → Synthesize → Reflect → Retain → Apply
```

V1 covers the first three. V2+ covers the last three.

| Stage | What It Means | Status |
|---|---|---|
| Ingest | Pull from RSS, YouTube, newsletters | Built |
| Filter | Score and deduplicate by relevance | Built |
| Synthesize | Cluster, summarize, generate digest | Built |
| Reflect | Interrogate the content — "what does this mean for me?" | Not built |
| Retain | Store insights, surface them over time (spaced repetition) | Not built |
| Apply | Connect to interview prep, real conversations, actual use | Not built |

---

## The Differentiated Vision

**"An AI learning companion that aggregates what's happening in AI, connects it to what you already know, surfaces your knowledge gaps, and helps you compound understanding over time."**

Nobody does this end-to-end. Summate does aggregation. Readwise does retention. Nobody connects them with a personalization layer that knows your context (AI PM, interviewing at big tech, building products).

The secret weapon: Michael already has a personal knowledge base (personal OS in Claude Code). Most people building news aggregators have no knowledge base to connect to. This one does.

---

## Competitive Landscape (Summate.io Key Findings)

Researched 2026-03-21. Full notes below.

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

**Our differentiators (already built in V1):**
- Claude relevance scoring filters before summarizing
- Jaccard deduplication across sources
- Clustering to group related stories

---

## V2 Product Vision

### The Connection Layer
The missing piece is not a new tool — it's a bridge between the news aggregator and the existing knowledge base.

Today they're two silos:
- News aggregator surfaces what's happening
- Personal OS stores what you know
- Nothing connects them

The V2 layer bridges: "today I read X → this connects to what I already know about Y → here's what it suggests you're missing → here's how you'd use it in an interview answer."

### What V2 Looks Like

**Digest enhancement:**
- Top-of-digest synthesis: "From today's content, here are 3 key themes and why they matter to you specifically as an AI PM interviewing at big tech"
- Gap identification: "Based on what came in today, here's a concept you should understand better"

**Reflection interface:**
- After reading, ability to chat with the digest — interrogate ideas, ask follow-up questions
- Not passive reading but active engagement

**Knowledge base integration:**
- User can add existing notes/knowledge into the system
- New articles build on and connect to what you already know
- Surfaces "you already know X — today's articles extend that with Y"

**Retention layer:**
- Save insights from digests
- Spaced repetition surfaces old insights at the right time
- Knowledge compounds visibly over time

### V3 Vision
- Interview prep mode: "based on what you've been reading this month, here's a practice question"
- Pattern recognition across weeks: "this is the third time agents have come up — here's the emerging story"
- Export to personal OS / notes

---

## What V1 Needs to Be Rock Solid First

Before any V2 work, V1 must be genuinely solid:

- [ ] More sources in config.yaml — need enough volume to feel the real synthesis value
- [ ] Dashboard rendering cleanly across different content volumes
- [ ] Scoring and clustering feeling accurate on real diverse data
- [ ] GitHub Actions running reliably on schedule
- [ ] End-to-end feeling genuinely useful daily, not just technically working

**The test:** after one week of daily use, does Michael find himself reading the digest every morning and actually retaining something? If yes, V1 is solid. If not, fix V1 first.

---

## Decisions Parked for V2

- How does the reflection interface work — chat UI in the dashboard, or something else?
- How does the knowledge base integration work — does the aggregator read from personal-os files, or does the user paste knowledge in?
- What does "saving an insight" look like — a note, a card, a tag?
- Spaced repetition mechanism — built-in or integrate with existing tool (Anki, Readwise)?
- Does V2 stay local (personal tool) or become multi-user (public product)?

---

## North Star

A one-stop shop for AI knowledge that doesn't just surface information — it helps you understand, internalize, and apply it. Built for Michael first. Designed to be shareable later.

The product arc:
- **V1:** One place to see everything important in AI today
- **V2:** One place to understand what it means for you
- **V3:** One place where your AI knowledge compounds over time
