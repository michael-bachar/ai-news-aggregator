---
date: 2026-03-22
topic: engineering philosophy, architecture, product validation
---

## Lesson
Build the simplest thing that works. Only move to a more complex solution when the simple one actually breaks.

## What happened
When deciding how to deploy the AI news aggregator, the question came up: should we use SQLite or a proper relational database (Postgres, MySQL)? Should we use Render or AWS? The instinct was to think about what a "real" production system would need.

The realization: we're not building a production system yet. We're proving out whether this is worth building at all. The right question isn't "what would this need at scale?" — it's "what's the minimum that lets us find out if this is valuable?"

SQLite is a file. Render is a managed server. Together they took 20 minutes to set up. The alternative — AWS, RDS, VPCs, IAM roles — would have taken days and added complexity that buys nothing until there's a real reason to need it.

## Why it matters
Over-engineering kills products before they prove their value. Every hour spent on infrastructure that isn't needed yet is an hour not spent on the thing that tells you if the product is worth building.

The pattern shows up everywhere in agentic AI work:
- Building a complex multi-agent orchestration when a single LLM call would do
- Adding a vector database before you know what you're searching for
- Designing for 10,000 users before you have 10

The cost of over-engineering is not just time. It's cognitive load — more things to maintain, more things to break, more things to understand before you can change anything.

## The rule
Use the simplest thing that works until it actually breaks. Not until you think it might break. Not until you can imagine a scenario where it breaks. Until it actually breaks.

The signals that it's time to move up:
- **SQLite → Postgres:** Multiple concurrent users writing at the same time, or file locking errors appearing in logs
- **Render → AWS:** You need fine-grained infrastructure control, multi-region, or compliance requirements
- **Single agent → multi-agent:** The single agent is demonstrably hitting a quality ceiling that more agents would solve

Until you see those signals, the simpler thing is the right thing.

## This transfers everywhere
This is not just an infrastructure decision. It's a product philosophy:

- Prove value first. Optimize second.
- Personal use before public launch. Public launch before scale.
- The dashboard running on a $7/mo server that you actually use every day is worth more than a perfectly architected system you never finished building.

The goal of the early stages is not to build something that could scale. It's to find out if there's something worth scaling.

## LinkedIn draft
The most common engineering mistake I see when building with AI:

Over-engineering before you've proven the thing is worth building.

You spend two weeks setting up AWS infrastructure, configuring IAM roles, standing up RDS — and then discover the core idea doesn't work the way you thought.

Meanwhile, the version of that same project built in two days on a $7/mo server would have told you the same thing.

The principle: use the simplest thing that works until it actually breaks. Not until you can imagine it breaking. Until it breaks.

SQLite before Postgres. Render before AWS. One agent before ten.

Every layer of complexity you add before you need it is a tax on every future change. You're not just building the feature — you're maintaining the infrastructure, debugging the infrastructure, and explaining the infrastructure to anyone who touches the code.

Prove value first. Scale second. The early job is not to build something that could work for 10,000 users. It's to find out if it's worth building for 10.
