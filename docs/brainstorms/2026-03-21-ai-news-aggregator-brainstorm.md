# Brainstorm: AI News Aggregator
**Date:** 2026-03-21
**Status:** Complete — ready for INITIAL.md

---

## What We're Building

A personal AI news aggregator that ingests from curated RSS feeds, newsletters, and YouTube, filters signal from noise using Claude, clusters stories across sources, and delivers a synthesized daily and weekly digest via a web dashboard.

Built for Michael first. Config-driven from day one so it's portable for others later — designed with a future public release in mind without over-engineering v1.

---

## The Problem

Too much is happening in AI. Newsletters pile up. The important stuff gets buried under noise. You end up either missing things or wasting time reading things that don't matter. The goal is one place to open every day that surfaces what actually matters — with synthesis, not just links.

---

## North Star

*"Help Michael show up as the most informed person in the room on AI."*

Not generic AI news — filtered for an AI PM focused on thought leadership, product craft, and building with AI tools.

---

## Key Decisions

### Output Format
**Web dashboard** — daily view (top 7-10 stories) + weekly view (narrative synthesis of the week's themes). Not email, not Notion. Custom dashboard so it can become public-facing later.

### Cadence
- **Daily:** top 7-10 clustered stories, synthesized, why it matters, source links
- **Weekly:** deeper narrative — "here are the 3 big themes from this week and what they mean"

### Sources (~15 curated)
**AI News & Strategy:**
- AI Daily Brief (Nathaniel Whittemore)
- The Batch (Andrew Ng / deeplearning.ai)
- Stratechery (Ben Thompson)
- The Rundown AI
- TLDR AI
- Hard Fork podcast (NYT) — via transcript/RSS
- Anthropic blog
- OpenAI blog

**AI PM & Product Craft:**
- Lenny's Newsletter
- Akash Gupta
- Aman Khan
- Ben Erez
- How I AI

**Building with AI / Claude Code:**
- Simon Willison's blog
- Ethan Mollick / One Useful Thing
- Sequoia / a16z AI content

**To confirm:** Ben Erez and Aman Khan's exact feed URLs (newsletter vs. LinkedIn vs. podcast — TBD at implementation).

### Ingestion Strategy
- **RSS-first** — most sources have feeds
- **Email forwarding fallback** — dedicated address for newsletters without RSS
- **YouTube transcript ingestion** — several sources are podcast/video format; auto-transcribe if no transcript exists
- **Twitter/X — skip for v1** (API too expensive and unreliable)

### Deduplication
Jaccard similarity on headlines before clustering — compares word overlap between titles, collapses near-duplicates into one story. Prevents the digest filling up with 8 variations of the same GPT-5 launch headline.

### Scoring & Relevance
Claude API scores each item 1-10 for relevance. Scoring prompt reads from `config.yaml` — knows who Michael is, what topics he cares about, what "important" means in his context. Items below threshold are dropped before clustering.

### Synthesis
Claude clusters related items, then synthesizes each cluster into:
- Headline
- 2-3 sentence synthesis
- Why it matters to Michael
- Source links (3-5 per cluster)

### Config-Driven Design
All user-specific data lives in `config.yaml` — sources, topics, name, relevance criteria. Nothing hardcoded. This is the one v1 concession to future multi-user support. Everything else (auth, accounts, onboarding) is v2.

### Scheduler
**GitHub Actions** — free, no server needed, cron in a YAML file. Daily at 6am, weekly on Sunday night.

### Stack
- **Language:** Python
- **LLM:** Claude API (Anthropic SDK)
- **Storage:** SQLite
- **Templates:** Jinja2 (HTML generation)
- **Scheduler:** GitHub Actions
- **Dashboard:** Simple web server (FastAPI + plain HTML/CSS)

---

## What We're NOT Building in V1

- Email delivery
- LinkedIn posting / content generation (→ Content Agent project, separate)
- Learning progress tracker
- Multi-user accounts, auth, onboarding
- Reddit ingestion (noise risk)
- Twitter/X ingestion (API cost)
- "Recap reinforcement" (resurface older items)
- Connection to other agents

---

## V2 Roadmap (parking lot)

- Hosted version with user accounts
- LinkedIn content generation connected to digest (→ Content Agent handoff)
- Reddit as source (r/MachineLearning, r/artificial)
- Recap reinforcement — resurface important older items
- Personalization feedback loop (thumbs up/down → tune scoring prompt)
- Mobile-friendly dashboard

---

## Open Source References

- **[QuantumExecBrief](https://timothyjohnsonsci.com/writing/2026-01-25-building-quantumnews-with-claude-code/)** — closest analog, built with Claude Code, same stack (Python + SQLite + Jinja2 + Claude API + GitHub Actions). Key learnings: prompts are the product, use defusedxml for RSS security, Jaccard for deduplication.
- **[finaldie/auto-news](https://github.com/finaldie/auto-news)** — most feature-complete OSS example. YouTube transcript ingestion pattern worth borrowing.
- **[AKAlSS/AI-News-Aggregator](https://github.com/AKAlSS/AI-News-Aggregator)** — simpler Python RSS → digest pipeline, good reference for ingestion layer.

---

## Architecture Overview

```
config.yaml
    ↓
Ingestion Layer (RSS + email + YouTube transcripts)
    ↓
Raw Items → SQLite
    ↓
Jaccard Deduplication
    ↓
Scoring Agent (Claude) — relevance filter
    ↓
Clustering Agent (Claude) — group related stories
    ↓
Synthesis Agent (Claude) — headline + summary + why it matters
    ↓
Digest stored in SQLite
    ↓
GitHub Actions trigger (6am daily / Sunday weekly)
    ↓
FastAPI + Jinja2 → Web Dashboard
```

---

## Next Step

Fill in `INITIAL.md` for Phase 1 (ingestion pipeline + scoring), then run `/generate-prp`.
