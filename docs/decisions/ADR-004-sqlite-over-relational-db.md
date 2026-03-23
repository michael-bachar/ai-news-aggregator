---
id: ADR-004
date: 2026-03-22
status: accepted
supersedes: ~
---

# SQLite over Postgres, MySQL, or DynamoDB

## Context
When building the storage layer for the AI news aggregator, a decision was needed on what database to use. The options ranged from SQLite (a local file) to fully managed cloud databases (Postgres on RDS, MySQL, DynamoDB). The natural instinct was to ask "what would a production system need?" — but that was the wrong question at this stage.

## Options considered
- **SQLite** — a file on disk, no server required, built into Python's standard library. Zero setup, zero cost, zero operational overhead. Limitation: locks on writes, not suited for multiple concurrent writers.
- **Postgres (e.g. RDS, Supabase, Render Postgres)** — proper relational database with concurrent reads/writes, point-in-time recovery, and production-grade reliability. Adds cost (~$7–25/mo minimum), requires connection management, and introduces a network hop on every query.
- **MySQL** — similar trade-offs to Postgres. No meaningful advantage for this use case.
- **DynamoDB** — NoSQL, AWS-native, scales to massive throughput. Entirely wrong abstraction for a structured digest dataset with relational queries. Requires AWS ecosystem buy-in.

## Decision
SQLite. The pipeline runs once per day in a single process. The dashboard serves one user. There is no concurrent write problem to solve. SQLite is the right tool for the actual problem, not the imagined future problem.

The migration signal is clear: if multiple users are hitting the dashboard simultaneously and write contention appears, or if the pipeline needs to run in parallel processes, migrate to Postgres. That signal has not appeared.

## Consequences
- Zero database operational overhead — no connection strings to manage, no server to provision, no backups to configure (Render's persistent disk handles the file)
- Queries are instant — no network hop, everything is local to the process
- The entire database is a single file that can be inspected, copied, or migrated trivially
- Concurrent write limitation: if two pipeline runs fire simultaneously, the second will fail with a lock error — acceptable for a single-user daily digest
- Migration to Postgres when needed is straightforward: SQLite and Postgres share the same SQL dialect for the queries used here; the main change would be the connection layer in `src/db.py`
- **Revisit if:** multiple users, concurrent pipeline runs, or data volume that strains a single file
