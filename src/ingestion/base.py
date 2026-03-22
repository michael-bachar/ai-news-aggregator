from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    source: str
    title: str
    url: str
    content: str
    published_at: Optional[datetime] = None
