# Brainstorm: V1 Dashboard & Infrastructure Improvements
**Date:** 2026-03-22
**Status:** Active — items to implement

---

## Context

V1 ran end-to-end on live data. Three improvements surfaced from the first real run:
1. No way to browse previous days in the dashboard
2. Relevance scoring criteria could be more explicit
3. No hosted environment — requires local run to view output

---

## 1. Day Selector on Dashboard

**Problem:** The dashboard defaults to today. No way to navigate to previous days in the UI. The backend already supports `?date=YYYY-MM-DD` but it's not surfaced.

**What to build:** Prev/next day navigation in the daily template, plus a date picker or dropdown showing available digest dates pulled from the DB.

**Notes:**
- Only show dates that have a digest in the DB (not all calendar dates)
- Prev/next arrows are the minimum; a dropdown of available dates is nicer
- Route already works — this is purely a template change

---

## 2. Relevance Scoring Criteria

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

---

## 3. Hosted Dashboard (No Local Setup)

**Problem:** Currently requires running `python3 -m src.run --daily` locally and `uvicorn` locally to see anything. Not sustainable.

**Decision needed:** Push digest to user (email/Slack) vs. hosted web dashboard the user visits.

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

## Next Steps

- [ ] Implement day selector in dashboard template
- [ ] Decide on hosting target (Fly.io vs Render vs Railway)
- [ ] Deploy pipeline + dashboard to chosen host
- [ ] Optionally: expose relevance scores in dashboard UI
