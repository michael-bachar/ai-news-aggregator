from __future__ import annotations

import json
import logging

import anthropic

from src.pipeline.scoring import _strip_code_fence

from src.config import Config
from src.models import ClusterSummary, RawItem

logger = logging.getLogger(__name__)

SYNTHESIS_MODEL = "claude-sonnet-4-6"

DAILY_SYSTEM_PROMPT = """You are a synthesis assistant for a personal AI news digest.

For each story cluster, produce:
1. A sharp, informative headline (not clickbait)
2. A 2-3 sentence synthesis of what happened
3. A "why it matters" framing tailored to the reader's persona and interests
4. A list of the best source links from the cluster (max 5)

Return ONLY valid JSON. No other text.

Format:
{
  "headline": "...",
  "synthesis": "...",
  "why_it_matters": "...",
  "sources": [{"name": "...", "url": "..."}]
}"""

WEEKLY_SYSTEM_PROMPT = """You are a synthesis assistant for a weekly AI news digest.

You will receive a list of story clusters from the past week.
Identify the 3 biggest themes and write a narrative paragraph for each.

Return ONLY valid JSON. No other text.

Format:
[
  {"cluster_id": "theme-1", "headline": "Theme title", "synthesis": "2-3 sentence narrative of what happened this week on this theme", "why_it_matters": "Why this matters for the reader", "sources": [{"name": "...", "url": "..."}]},
  ...
]"""


def _build_cluster_prompt(config: Config, cluster_id: str, items: list[RawItem]) -> str:
    items_str = "\n\n".join(
        f"Source: {item.source}\nTitle: {item.title}\nURL: {item.url}\nContent: {item.content[:500]}"
        for item in items
    )
    return f"""Persona: {config.persona}

Cluster: {cluster_id}
Items ({len(items)} sources covering this story):

{items_str}"""


def synthesize_cluster(
    client: anthropic.Anthropic,
    config: Config,
    cluster_id: str,
    items: list[RawItem],
) -> ClusterSummary:
    """Synthesize a single cluster into a digest entry."""
    try:
        response = client.messages.create(
            model=SYNTHESIS_MODEL,
            max_tokens=1024,
            system=DAILY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_cluster_prompt(config, cluster_id, items)}],
        )
        data = json.loads(_strip_code_fence(response.content[0].text))  # type: ignore[union-attr]
        return ClusterSummary(
            cluster_id=cluster_id,
            headline=data["headline"],
            synthesis=data["synthesis"],
            why_it_matters=data["why_it_matters"],
            sources=data.get("sources", []),
        )
    except Exception as e:
        logger.error("Synthesis failed for cluster '%s': %s", cluster_id, e)
        # Graceful fallback — use first item's title and URL
        first = items[0]
        return ClusterSummary(
            cluster_id=cluster_id,
            headline=first.title,
            synthesis="Synthesis unavailable.",
            why_it_matters="",
            sources=[{"name": first.source, "url": first.url}],
        )


def synthesize_all(
    client: anthropic.Anthropic,
    config: Config,
    clusters: dict[str, list[RawItem]],
    max_stories: int,
) -> list[ClusterSummary]:
    """Synthesize all clusters, limited to max_stories."""
    # Sort clusters by average relevance score (descending) to prioritize top stories
    def avg_score(items: list[RawItem]) -> float:
        scores = [i.relevance_score for i in items if i.relevance_score is not None]
        return sum(scores) / len(scores) if scores else 0.0

    sorted_clusters = sorted(clusters.items(), key=lambda kv: avg_score(kv[1]), reverse=True)
    top_clusters = sorted_clusters[:max_stories]

    summaries: list[ClusterSummary] = []
    for cluster_id, items in top_clusters:
        summary = synthesize_cluster(client, config, cluster_id, items)
        summaries.append(summary)
        logger.info("Synthesized cluster '%s': %s", cluster_id, summary.headline)

    return summaries


def synthesize_weekly(
    client: anthropic.Anthropic,
    config: Config,
    all_summaries: list[ClusterSummary],
) -> list[ClusterSummary]:
    """
    Take the week's daily summaries and produce 3 overarching weekly themes.
    """
    if not all_summaries:
        return []

    items_str = "\n\n".join(
        f"Headline: {s.headline}\nSynthesis: {s.synthesis}"
        for s in all_summaries
    )
    prompt = f"""Persona: {config.persona}

Here are this week's top stories ({len(all_summaries)} clusters):

{items_str}

Identify the 3 biggest themes of the week and write a narrative synthesis for each."""

    try:
        response = client.messages.create(
            model=SYNTHESIS_MODEL,
            max_tokens=2048,
            system=WEEKLY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        themes = json.loads(_strip_code_fence(response.content[0].text))  # type: ignore[union-attr]
        return [
            ClusterSummary(
                cluster_id=t["cluster_id"],
                headline=t["headline"],
                synthesis=t["synthesis"],
                why_it_matters=t["why_it_matters"],
                sources=t.get("sources", []),
            )
            for t in themes
        ]
    except Exception as e:
        logger.error("Weekly synthesis failed: %s", e)
        return all_summaries[:3]
