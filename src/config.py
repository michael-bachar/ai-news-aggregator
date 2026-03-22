from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Source:
    name: str
    url: str
    type: str  # rss | youtube | email

    def __post_init__(self) -> None:
        if self.type not in ("rss", "youtube", "email"):
            raise ValueError(f"Unknown source type '{self.type}' for source '{self.name}'")


@dataclass
class Config:
    persona: str
    topics: list[str]
    sources: list[Source]
    relevance_threshold: int = 6
    max_daily_stories: int = 10
    dedup_threshold: float = 0.5
    daily_token_budget: int = 50000


def load_config(path: str | Path | None = None) -> Config:
    if path is None:
        path = Path(os.environ.get("CONFIG_PATH", "config.yaml"))
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open() as f:
        raw = yaml.safe_load(f)

    sources = [Source(**s) for s in raw.get("sources", [])]

    return Config(
        persona=raw["persona"],
        topics=raw.get("topics", []),
        sources=sources,
        relevance_threshold=int(raw.get("relevance_threshold", 6)),
        max_daily_stories=int(raw.get("max_daily_stories", 10)),
        dedup_threshold=float(raw.get("dedup_threshold", 0.5)),
        daily_token_budget=int(raw.get("daily_token_budget", 50000)),
    )
