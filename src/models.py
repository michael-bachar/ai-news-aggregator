from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RawItem:
    source: str
    title: str
    url: str
    content: str
    published_at: Optional[datetime]
    id: Optional[int] = None
    ingested_at: Optional[datetime] = None
    relevance_score: Optional[int] = None
    cluster_id: Optional[str] = None
    included_in_digest: bool = False


@dataclass
class ClusterSummary:
    cluster_id: str
    headline: str
    synthesis: str
    why_it_matters: str
    sources: list[dict]  # [{"name": str, "url": str}]


@dataclass
class DigestEntry:
    date: str           # YYYY-MM-DD
    type: str           # daily | weekly
    clusters: list[ClusterSummary]
    id: Optional[int] = None
    created_at: Optional[datetime] = None
