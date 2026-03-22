# Tasks

## Active
_Nothing in progress._

## Backlog
- [ ] Populate config.yaml with real RSS feed URLs (copy from config.example.yaml)
- [ ] Confirm Ben Erez + Aman Khan feed URLs
- [ ] Confirm Hard Fork podcast RSS URL
- [ ] Run end-to-end with 2-3 real sources, verify digest renders at localhost:8000
- [ ] Add ANTHROPIC_API_KEY to GitHub repo secrets for Actions

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
