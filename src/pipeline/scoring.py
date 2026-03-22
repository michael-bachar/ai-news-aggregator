from __future__ import annotations

import json
import logging
from typing import Optional

import anthropic

from src.config import Config
from src.models import RawItem

logger = logging.getLogger(__name__)

SCORING_MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 20

SYSTEM_PROMPT = """You are a relevance scoring assistant for a personal AI news digest.

Your job is to score each news item 1-10 based on how relevant and important it is to the reader's specific persona and interests.

Scoring guide:
- 9-10: Must-read. High-signal, directly relevant to the reader's work and interests.
- 7-8: Worth reading. On-topic and useful.
- 5-6: Marginally relevant. Tangentially related.
- 3-4: Low relevance. Loosely related but not useful.
- 1-2: Not relevant. Off-topic or noise.

You must return ONLY a valid JSON array with one object per item in the same order as provided.
Each object must have: {"index": <int>, "score": <int 1-10>, "reason": "<one sentence>"}

Do not include any other text."""


def _build_user_prompt(config: Config, items: list[RawItem]) -> str:
    topics_str = "\n".join(f"- {t}" for t in config.topics)
    items_str = "\n\n".join(
        f"[{i}] Title: {item.title}\nSource: {item.source}\nContent snippet: {item.content[:300]}"
        for i, item in enumerate(items)
    )
    return f"""Persona: {config.persona}

Topics of interest:
{topics_str}

Score the following {len(items)} news items:

{items_str}"""


def _strip_code_fence(text: str) -> str:
    """Strip ```json ... ``` or ``` ... ``` wrappers Claude sometimes adds."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]  # drop opening fence line
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


def _parse_scores(response_text: str, count: int) -> list[Optional[int]]:
    """Parse the JSON scores array from Claude's response."""
    try:
        scores_data = json.loads(_strip_code_fence(response_text))
        result: list[Optional[int]] = [None] * count
        for item in scores_data:
            idx = item.get("index")
            score = item.get("score")
            if idx is not None and score is not None and 0 <= idx < count:
                result[idx] = int(score)
        return result
    except Exception as e:
        logger.warning("Failed to parse scoring response: %s\nResponse: %s", e, response_text[:500])
        return [None] * count


def score_items(
    client: anthropic.Anthropic,
    config: Config,
    items: list[RawItem],
) -> list[RawItem]:
    """
    Score items using Claude Haiku. Items below config.relevance_threshold are dropped.
    Returns only items that pass the threshold, with relevance_score set.
    """
    if not items:
        return []

    scored_items: list[RawItem] = []
    total_input_tokens = 0
    total_output_tokens = 0

    for batch_start in range(0, len(items), BATCH_SIZE):
        batch = items[batch_start : batch_start + BATCH_SIZE]

        try:
            response = client.messages.create(
                model=SCORING_MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": _build_user_prompt(config, batch)}],
            )
            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

            scores = _parse_scores(response.content[0].text, len(batch))  # type: ignore[union-attr]

        except Exception as e:
            logger.error("Scoring API call failed for batch starting at %d: %s", batch_start, e)
            scores = [None] * len(batch)

        for item, score in zip(batch, scores):
            if score is None:
                logger.warning("No score returned for '%s' — skipping", item.title)
                continue
            item.relevance_score = score
            if score >= config.relevance_threshold:
                scored_items.append(item)
            else:
                logger.debug("Dropped '%s' (score %d)", item.title, score)

    # Rough cost estimate: Haiku input ~$0.80/M tokens, output ~$4/M tokens
    est_cost = (total_input_tokens / 1_000_000 * 0.80) + (total_output_tokens / 1_000_000 * 4.0)
    logger.info(
        "Scoring complete: %d/%d items passed threshold %d | tokens: %d in / %d out | est. cost: $%.4f",
        len(scored_items),
        len(items),
        config.relevance_threshold,
        total_input_tokens,
        total_output_tokens,
        est_cost,
    )

    return scored_items
