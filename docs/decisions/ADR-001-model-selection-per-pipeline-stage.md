---
id: ADR-001
date: 2026-03-21
status: accepted
supersedes: ~
---

# Use different Claude models per pipeline stage based on task complexity

## Context
The pipeline runs daily and makes many Claude API calls — one scoring call per article (potentially 50–100/day), one clustering call per run, one synthesis call per cluster. Cost and latency compound quickly if the same model is used everywhere. But quality matters differently at each stage: a mis-scored article gets dropped silently; a bad synthesis ships to the dashboard.

## Options considered
- **Same model everywhere (Sonnet)** — Consistent quality, simpler config. But expensive for high-volume, low-complexity tasks like per-article scoring.
- **Same model everywhere (Haiku)** — Cheaper, faster. But synthesis quality degrades noticeably — summaries become thin and generic.
- **Per-stage model selection** — Match model capability to task complexity. Higher cost to reason about, but better cost/quality ratio overall.

## Decision
Use **Haiku** for scoring (high volume, binary judgment — is this relevant or not?) and **Sonnet** for clustering and synthesis (low volume, requires reasoning and writing quality).

Scoring is a classification task: given a relevance threshold of 6/10, Haiku performs comparably to Sonnet at a fraction of the cost. Clustering and synthesis require understanding relationships between articles and producing coherent, well-written output — Sonnet is worth the cost there.

## Consequences
- Daily API cost is substantially lower than all-Sonnet
- Scoring latency is faster, which matters when processing 50–100 articles
- If scoring quality degrades (wrong articles passing the threshold), Haiku is the first thing to revisit
- Model selection is currently hardcoded per agent — if we want to make it configurable, it needs to move to config.yaml
- This pattern should apply to Layer 2 agents: ReAct scoring agent stays on Haiku; Critic Loop on synthesis stays on Sonnet
