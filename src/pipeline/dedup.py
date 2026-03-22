from __future__ import annotations

import re
from src.models import RawItem


def _tokenize(text: str) -> set[str]:
    """Lowercase, strip punctuation, split on whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.split())


def jaccard(a: str, b: str) -> float:
    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a and not tokens_b:
        return 1.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def deduplicate(items: list[RawItem], threshold: float = 0.5) -> list[RawItem]:
    """
    Remove near-duplicate items using Jaccard similarity on titles.
    When duplicates are found, keeps the item with the longest content.
    """
    kept: list[RawItem] = []

    for item in items:
        is_duplicate = False
        for i, existing in enumerate(kept):
            if jaccard(item.title, existing.title) >= threshold:
                # Keep whichever has more content
                if len(item.content) > len(existing.content):
                    kept[i] = item
                is_duplicate = True
                break
        if not is_duplicate:
            kept.append(item)

    return kept
