# INITIAL.md — AI News Aggregator

Use this file to describe a feature before running `/generate-prp`.
Fill in all four sections, then run: `/generate-prp INITIAL.md`

---

## FEATURE

**AI News Aggregator — Full Pipeline (Ingestion → Scoring → Clustering → Synthesis → Dashboard)**

A personal AI news aggregator that ingests from curated RSS feeds, newsletters, and YouTube transcripts, filters and scores items for relevance using Claude, clusters related stories across sources, and delivers a synthesized daily and weekly digest via a web dashboard.

### What It Does

1. **Ingestion** — Pulls raw items from ~15 curated sources on a schedule (GitHub Actions cron: 6am daily, Sunday weekly). Sources: RSS feeds (primary), email forwarding for newsletters without RSS, YouTube transcript ingestion for podcast/video sources.

2. **Storage** — Persists raw items to SQLite. Schema tracks source, title, URL, content, timestamp, relevance score, cluster ID, and digest inclusion status.

3. **Deduplication** — Jaccard similarity on headlines before scoring. Collapses near-duplicate items (e.g., 8 outlets covering the same GPT-5 launch) into one before passing to Claude.

4. **Scoring Agent** — Claude API scores each deduplicated item 1–10 for relevance using a prompt that reads persona + topic priorities from `config.yaml`. Items below threshold (default: 6) are dropped.

5. **Clustering Agent** — Claude groups surviving items into thematic clusters (e.g., "OpenAI's new model," "AI regulation in EU," "Agentic AI frameworks"). Each cluster = one story in the digest.

6. **Synthesis Agent** — For each cluster, Claude produces:
   - Headline
   - 2–3 sentence synthesis
   - "Why it matters" framing (personalized to persona in config)
   - 3–5 source links

7. **Digest Storage** — Daily digest (top 7–10 stories) and weekly digest (3 big themes + narrative) stored in SQLite.

8. **Web Dashboard** — FastAPI server renders digests via Jinja2 templates. Daily view and weekly view. Simple, clean HTML/CSS — no JS framework. Config-driven so it's portable for future public release.

### Who Triggers It and How

- **Automatically** — GitHub Actions cron job triggers the full pipeline daily at 6am and weekly on Sunday night.
- **Manually** — Can be triggered locally by running the pipeline script directly for testing.

### Expected Output

- **Daily digest:** 7–10 story clusters, each with headline, 2–3 sentence synthesis, "why it matters," and source links.
- **Weekly digest:** 3 thematic narratives summarizing the week — "here are the 3 big themes from this week and what they mean."
- **Dashboard:** Web UI at localhost (dev) or hosted URL (prod) with daily and weekly tabs.

### What Success Looks Like

- Opens every morning to a clean digest with 7–10 stories — no duplicates, no noise.
- Every item passed Claude's relevance filter: it's about AI strategy, AI product craft, or building with AI tools.
- Each cluster synthesis is accurate and the "why it matters" framing is specific to an AI PM focused on thought leadership and building with AI — not generic.
- Weekly view tells a coherent narrative, not just a list.
- Pipeline runs end-to-end without manual intervention. GitHub Actions logs show success.
- Zero cost surprises — Claude API calls are batched and token-efficient. Config sets a daily token budget.

---

## EXAMPLES

- `examples/__init__.py` — placeholder only, no patterns yet.

**Closest reference implementations to follow:**
- **QuantumExecBrief** — same stack (Python + SQLite + Jinja2 + Claude API + GitHub Actions). Key patterns: prompts are the product, use `defusedxml` for RSS parsing security, Jaccard for deduplication. Blog post: https://timothyjohnsonsci.com/writing/2026-01-25-building-quantumnews-with-claude-code/
- **finaldie/auto-news** (GitHub) — most feature-complete OSS reference. YouTube transcript ingestion pattern worth borrowing.
- **AKAlSS/AI-News-Aggregator** (GitHub) — simpler Python RSS → digest pipeline, good reference for ingestion layer structure.

---

## DOCUMENTATION

- **Anthropic Python SDK:** https://github.com/anthropics/anthropic-sdk-python
- **Claude API Messages:** https://docs.anthropic.com/en/api/messages
- **feedparser (RSS/Atom parsing):** https://feedparser.readthedocs.io/
- **defusedxml (secure XML parsing):** https://pypi.org/project/defusedxml/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Jinja2:** https://jinja.palletsprojects.com/
- **youtube-transcript-api:** https://pypi.org/project/youtube-transcript-api/
- **GitHub Actions cron syntax:** https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule

---

## OTHER CONSIDERATIONS

**Config-driven design is non-negotiable for v1.**
All user-specific data lives in `config.yaml`: sources (name, feed URL, type), persona description, topic priorities, relevance threshold, token budget. Nothing hardcoded. This is the one v1 concession to future multi-user support — makes the project portable without building accounts or auth.

**Stack:**
- Python
- Claude API via Anthropic SDK
- SQLite (single-file DB, no Postgres needed for v1)
- Jinja2 for HTML templating
- FastAPI for the dashboard server
- GitHub Actions for scheduling

**What NOT to build in v1:**
- Email delivery
- LinkedIn content generation (that's the Content Agent project — separate)
- Multi-user accounts, auth, onboarding
- Reddit or Twitter/X ingestion (noise risk + API cost)
- Personalization feedback loop (thumbs up/down)
- Connection to other agents

**Rate limits and cost:**
- Claude API calls are the main cost driver. Batch scoring calls — don't call per item individually.
- Target: full daily pipeline under $0.10 in API costs.
- Use `haiku` model for scoring (cost-efficient); use `sonnet` for synthesis (quality matters there).

**Edge cases to handle:**
- RSS feeds that are down or malformed — log and skip, don't crash the pipeline.
- Duplicate ingestion across runs — check URL against SQLite before inserting.
- YouTube transcripts unavailable — fall back to title + description only.
- Empty digest day (all items scored below threshold) — render a "quiet day" state, don't crash.
- `defusedxml` required for RSS parsing — prevents XML injection attacks from untrusted feeds.

**Sources to confirm before implementation:**
- Ben Erez and Aman Khan feed URLs (newsletter vs. LinkedIn vs. podcast — TBD at implementation).
- Hard Fork podcast RSS URL (NYT-hosted, may require workaround).
