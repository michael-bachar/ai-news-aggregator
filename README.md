# AI News Aggregator

An agentic news aggregator that pulls from RSS feeds, newsletters, and email to surface what's actually worth reading in AI.

Filters signal from noise. Synthesizes key developments. Delivers a ranked digest on your schedule.

## The Problem

Too much is happening in AI. Newsletters pile up. Twitter threads disappear. The important stuff gets buried. You end up either missing things or wasting time reading things that don't matter.

## What This Does

- Ingests from RSS feeds, newsletters, and (v2) Gmail
- Scores each item for relevance using Claude
- Synthesizes a ranked daily digest with key takeaways
- Highlights what matters for AI product work specifically

## Stack

- **Agents:** Python, Claude API (Anthropic SDK)
- **Storage:** SQLite (local) → Postgres (prod)
- **Scheduler:** APScheduler / cron
- **Delivery:** CLI → email/Slack (v2)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python -m src.main
```

## Project Structure

```
src/
├── ingestion/    # RSS, newsletter, email readers
├── scoring/      # Relevance scoring agent
├── synthesis/    # Digest generation agent
├── delivery/     # CLI, email, Slack output
└── storage/      # DB models and queries
```

## Status

🟡 In progress — v1 (RSS + newsletter → digest)
