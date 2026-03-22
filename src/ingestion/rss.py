from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Optional

import feedparser

from src.config import Source
from src.ingestion.base import Item

MAX_ITEM_AGE_HOURS = 48  # Only ingest items published within this window

logger = logging.getLogger(__name__)

# feedparser has its own robust XML sanitization built in.
# defusedxml has no feedparser integration module — importing it here
# would be a no-op and misleading. feedparser's sanitization is sufficient.


def _parse_date(entry: feedparser.FeedParserDict) -> Optional[datetime]:
    # Prefer pre-parsed struct_time (feedparser's published_parsed / updated_parsed)
    # — more reliable than re-parsing the raw string ourselves.
    for attr in ("published_parsed", "updated_parsed"):
        value = entry.get(attr)
        if value:
            try:
                return datetime.fromtimestamp(time.mktime(value), tz=timezone.utc)
            except Exception:
                pass
    # Fall back to raw string parsing
    for attr in ("published", "updated"):
        value = entry.get(attr)
        if value:
            try:
                return parsedate_to_datetime(value)
            except Exception:
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except Exception:
                    pass
    return None


def _extract_content(entry: feedparser.FeedParserDict) -> str:
    # feedparser normalizes <description> to `summary` — no need to check "description"
    if entry.get("content"):
        return entry["content"][0].get("value", "")
    return entry.get("summary", "")


def fetch_rss(source: Source) -> list[Item]:
    """Fetch and parse an RSS/Atom feed. Returns items; logs and returns [] on error."""
    try:
        feed = feedparser.parse(source.url)
    except Exception as e:
        logger.warning("Failed to fetch feed '%s' (%s): %s", source.name, source.url, e)
        return []

    if feed.bozo and feed.bozo_exception:
        logger.warning(
            "Malformed feed '%s': %s — attempting to use partial results",
            source.name,
            feed.bozo_exception,
        )

    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=MAX_ITEM_AGE_HOURS)
    items: list[Item] = []

    for entry in feed.entries:
        url = entry.get("link", "")
        title = entry.get("title", "").strip()
        if not url or not title:
            continue

        content = _extract_content(entry).strip()
        published_at = _parse_date(entry)

        # Skip items older than the cutoff window
        if published_at and published_at < cutoff:
            continue

        items.append(
            Item(
                source=source.name,
                title=title,
                url=url,
                content=content,
                published_at=published_at,
            )
        )

    logger.info("Fetched %d items from '%s'", len(items), source.name)
    return items


def fetch_all_rss(sources: list[Source]) -> list[Item]:
    """Fetch all RSS sources, aggregating results."""
    all_items: list[Item] = []
    for source in sources:
        if source.type == "rss":
            all_items.extend(fetch_rss(source))
    return all_items
