---
id: ADR-003
date: 2026-03-22
status: accepted
supersedes: ~
---

# Cloud deployment via Render with in-process scheduler

## Context
The V1 pipeline was running entirely locally. To see the dashboard, the server had to be started manually each session. To run the pipeline, a terminal command had to be executed by hand. This was unsustainable for daily use — the digest is only useful if it shows up automatically every morning without any manual steps.

## Options considered
- **Local only** — keep running locally, start the server manually when needed. No cost, but defeats the purpose of a daily digest.
- **Render cron + web service (separate)** — deploy a web service for the dashboard and separate cron services for the pipeline. Simpler in theory, but Render does not share persistent disks between services — the cron would write to a different database than the dashboard reads from.
- **Render web service + APScheduler** — run the pipeline as a scheduled background job inside the same web service process. One service, one persistent disk, no sharing problem. Auto-deploys on every push to main.
- **Turso (hosted SQLite) + Render free tier** — use a cloud SQLite database so pipeline and dashboard can run separately. Clean architecture but required rewriting the entire database layer (different API from sqlite3).

## Decision
Deployed to Render as a single web service (Starter plan, $7/mo) with a persistent disk (1GB, $0.25/mo). APScheduler runs the daily pipeline at 11am UTC and the weekly pipeline at 10pm UTC Sunday inside the web service process, writing to `/data/news.db` on the same disk the dashboard reads from.

Render is connected to the GitHub repo. Every push to main triggers an automatic redeploy.

## Consequences
- Dashboard is accessible from any browser at a permanent URL, no local setup required
- Pipeline runs autonomously every day — no manual intervention
- Code changes deploy automatically on push to main
- Database accumulates history on the persistent disk across deploys
- Pipeline runs in the web server process — if the server restarts mid-pipeline, the run is lost (acceptable for a personal tool)
- APScheduler job failures are silent unless Render logs are monitored — no alerting
- GitHub Actions workflow kept as manual dispatch only for emergency one-off runs (does not write to Render's disk)
