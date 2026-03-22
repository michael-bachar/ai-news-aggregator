from __future__ import annotations

import json
import logging
import uuid

import anthropic

from src.pipeline.scoring import _strip_code_fence

from src.config import Config
from src.models import RawItem

logger = logging.getLogger(__name__)

CLUSTERING_MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are a news clustering assistant. Group a list of news items into thematic clusters.

Rules:
- Each cluster should represent one coherent story or theme.
- Only merge items into the same cluster if they cover the SAME specific event, announcement, or topic. Different aspects of AI (e.g. evals, coding tools, embeddings, strategy) are NOT the same cluster.
- When in doubt, keep items in separate clusters. Splitting is always better than merging.
- A single item with no close match should be its own cluster.
- Minimum clusters: at least 1 per 3 items. For 10 items expect 5-8 clusters.
- Return ONLY a valid JSON array, no other text.

Each object in the array must have:
{"cluster_id": "<short-slug>", "title": "<cluster theme title>", "item_indices": [<list of 0-based indices>]}"""


def _build_prompt(items: list[RawItem]) -> str:
    items_str = "\n\n".join(
        f"[{i}] {item.title} (source: {item.source})\n    {item.content[:150].strip()}"
        for i, item in enumerate(items)
    )
    return f"Cluster the following {len(items)} news items:\n\n{items_str}"


def cluster_items(
    client: anthropic.Anthropic,
    config: Config,
    items: list[RawItem],
) -> dict[str, list[RawItem]]:
    """
    Group items into thematic clusters.
    Returns a dict mapping cluster_id → list of RawItems.
    """
    if not items:
        return {}

    try:
        response = client.messages.create(
            model=CLUSTERING_MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_prompt(items)}],
        )
        clusters_data = json.loads(_strip_code_fence(response.content[0].text))  # type: ignore[union-attr]
    except Exception as e:
        logger.error("Clustering failed: %s — putting all items in one cluster", e)
        fallback_id = str(uuid.uuid4())[:8]
        return {fallback_id: items}

    clusters: dict[str, list[RawItem]] = {}
    assigned = set()

    for cluster in clusters_data:
        cluster_id = cluster.get("cluster_id", str(uuid.uuid4())[:8])
        indices = cluster.get("item_indices", [])
        cluster_items_list = []
        for idx in indices:
            if 0 <= idx < len(items):
                cluster_items_list.append(items[idx])
                assigned.add(idx)
        if cluster_items_list:
            clusters[cluster_id] = cluster_items_list

    # Any items not assigned get their own cluster
    for idx, item in enumerate(items):
        if idx not in assigned:
            fallback_id = f"misc-{idx}"
            clusters[fallback_id] = [item]

    logger.info("Clustered %d items into %d clusters", len(items), len(clusters))
    return clusters
