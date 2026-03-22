from __future__ import annotations

import logging
import re
from typing import Optional

from src.config import Source
from src.ingestion.base import Item

logger = logging.getLogger(__name__)


def _extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/|shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def _fetch_transcript(video_id: str) -> Optional[str]:
    try:
        from youtube_transcript_api import (
            NoTranscriptFound,
            RequestBlocked,
            TranscriptsDisabled,
            YouTubeTranscriptApi,
        )

        # Instance-based API (current as of v0.6+)
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id)
        return " ".join(snippet.text for snippet in fetched.snippets)
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        logger.warning("Transcript not available for video %s: %s", video_id, e)
        return None
    except RequestBlocked:
        # Common on cloud IPs (GitHub Actions, AWS, etc.) — YouTube blocks them
        logger.warning(
            "YouTube blocked transcript request for video %s — "
            "this is expected on cloud infrastructure. "
            "Consider running ingestion locally or via a proxy.",
            video_id,
        )
        return None
    except Exception as e:
        logger.warning("Could not fetch transcript for video %s: %s", video_id, e)
        return None


def _fetch_video_metadata(video_id: str) -> dict:
    """Fetch basic metadata via oembed — no API key required."""
    try:
        import urllib.request
        import json

        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310
            return json.loads(resp.read())
    except Exception as e:
        logger.warning("Could not fetch metadata for video %s: %s", video_id, e)
        return {}


def fetch_youtube(source: Source) -> list[Item]:
    """Fetch transcript (or fallback to description) for a YouTube source."""
    video_id = _extract_video_id(source.url)
    if not video_id:
        logger.warning("Could not extract video ID from URL: %s", source.url)
        return []

    metadata = _fetch_video_metadata(video_id)
    title = metadata.get("title", source.name)

    transcript = _fetch_transcript(video_id)
    if transcript:
        content = transcript
    else:
        # Fall back to title only — still worth scoring
        content = f"{title}. (Transcript unavailable.)"
        logger.info("Using title-only fallback for '%s'", source.name)

    return [
        Item(
            source=source.name,
            title=title,
            url=source.url,
            content=content,
            published_at=None,
        )
    ]


def fetch_all_youtube(sources: list[Source]) -> list[Item]:
    all_items: list[Item] = []
    for source in sources:
        if source.type == "youtube":
            all_items.extend(fetch_youtube(source))
    return all_items
