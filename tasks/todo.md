# Tasks

## Active
_Nothing in progress._

## Backlog
- [ ] Add ANTHROPIC_API_KEY to GitHub repo secrets for Actions
- [x] Day selector on dashboard (prev/next navigation + available dates from DB)
- [ ] Deploy dashboard to Render — code complete, manual steps remain (see below)
- [ ] ReAct scoring agent (reason + fetch loop for uncertain snippets)
- [ ] Critic loop on synthesis agent

### Render Deployment — Remaining Manual Steps
1. Go to render.com → New → Blueprint → connect GitHub repo
2. Set ANTHROPIC_API_KEY secret when prompted
3. Click Apply/Deploy
4. Once live: Render Shell tab → `python -m src.run --daily --db /data/news.db` to seed DB
5. Reload dashboard URL to verify

## Done
- [x] Set up ingestion pipeline (RSS + YouTube)
- [x] Build Jaccard deduplication
- [x] Build relevance scoring agent (Claude Haiku)
- [x] Build clustering agent (Claude Sonnet)
- [x] Build synthesis agent (Claude Sonnet)
- [x] Build digest orchestrator (daily + weekly)
- [x] SQLite storage layer
- [x] FastAPI + Jinja2 web dashboard (daily + weekly views)
- [x] CLI entrypoint (python -m src.run --daily / --weekly)
- [x] GitHub Actions cron (6am daily + Sunday weekly)
- [x] Unit tests (dedup, config, db) — 13 passing
