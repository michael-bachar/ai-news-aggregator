from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from src.models import ClusterSummary, DigestEntry, RawItem

DB_PATH = Path("data/news.db")


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db(db_path: Path = DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: Path = DB_PATH) -> None:
    with db(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS raw_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                content TEXT,
                published_at TEXT,
                ingested_at TEXT NOT NULL,
                relevance_score INTEGER,
                cluster_id TEXT,
                included_in_digest INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS digest_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                clusters_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(date, type)
            );

            CREATE INDEX IF NOT EXISTS idx_raw_items_url ON raw_items(url);
            CREATE INDEX IF NOT EXISTS idx_raw_items_ingested ON raw_items(ingested_at);
            CREATE INDEX IF NOT EXISTS idx_digest_date ON digest_entries(date, type);
        """)


def upsert_item(conn: sqlite3.Connection, item: RawItem) -> Optional[int]:
    """Insert item if URL not seen before. Returns row id or None if duplicate."""
    existing = conn.execute(
        "SELECT id FROM raw_items WHERE url = ?", (item.url,)
    ).fetchone()

    if existing:
        return None

    now = datetime.utcnow().isoformat()
    published = item.published_at.isoformat() if item.published_at else None

    cursor = conn.execute(
        """INSERT INTO raw_items (source, title, url, content, published_at, ingested_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (item.source, item.title, item.url, item.content, published, now),
    )
    return cursor.lastrowid


def update_item_score(conn: sqlite3.Connection, item_id: int, score: int) -> None:
    conn.execute(
        "UPDATE raw_items SET relevance_score = ? WHERE id = ?", (score, item_id)
    )


def update_item_cluster(conn: sqlite3.Connection, item_id: int, cluster_id: str) -> None:
    conn.execute(
        "UPDATE raw_items SET cluster_id = ?, included_in_digest = 1 WHERE id = ?",
        (cluster_id, item_id),
    )


def get_unscored_items(conn: sqlite3.Connection, since_hours: int = 25) -> list[RawItem]:
    """Fetch recently ingested items that haven't been scored yet."""
    rows = conn.execute(
        """SELECT * FROM raw_items
           WHERE relevance_score IS NULL
           AND ingested_at >= datetime('now', ?)
           ORDER BY ingested_at DESC""",
        (f"-{since_hours} hours",),
    ).fetchall()
    return [_row_to_raw_item(r) for r in rows]


def get_scored_items(conn: sqlite3.Connection, min_score: int, since_hours: int = 25) -> list[RawItem]:
    """Fetch recently ingested items at or above the score threshold."""
    rows = conn.execute(
        """SELECT * FROM raw_items
           WHERE relevance_score >= ?
           AND ingested_at >= datetime('now', ?)
           ORDER BY relevance_score DESC""",
        (min_score, f"-{since_hours} hours"),
    ).fetchall()
    return [_row_to_raw_item(r) for r in rows]


def save_digest(conn: sqlite3.Connection, entry: DigestEntry) -> None:
    clusters_json = json.dumps([
        {
            "cluster_id": c.cluster_id,
            "headline": c.headline,
            "synthesis": c.synthesis,
            "why_it_matters": c.why_it_matters,
            "sources": c.sources,
        }
        for c in entry.clusters
    ])
    now = datetime.utcnow().isoformat()
    conn.execute(
        """INSERT INTO digest_entries (date, type, clusters_json, created_at)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(date, type) DO UPDATE SET clusters_json=excluded.clusters_json, created_at=excluded.created_at""",
        (entry.date, entry.type, clusters_json, now),
    )


def get_digest(conn: sqlite3.Connection, date: str, digest_type: str) -> Optional[DigestEntry]:
    row = conn.execute(
        "SELECT * FROM digest_entries WHERE date = ? AND type = ?", (date, digest_type)
    ).fetchone()

    if not row:
        return None

    clusters_data = json.loads(row["clusters_json"])
    clusters = [
        ClusterSummary(
            cluster_id=c["cluster_id"],
            headline=c["headline"],
            synthesis=c["synthesis"],
            why_it_matters=c["why_it_matters"],
            sources=c["sources"],
        )
        for c in clusters_data
    ]
    return DigestEntry(
        id=row["id"],
        date=row["date"],
        type=row["type"],
        clusters=clusters,
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def get_available_dates(conn: sqlite3.Connection, digest_type: str) -> list[str]:
    """Return all dates that have a digest of the given type, sorted descending."""
    rows = conn.execute(
        "SELECT date FROM digest_entries WHERE type = ? ORDER BY date DESC",
        (digest_type,),
    ).fetchall()
    return [row["date"] for row in rows]


def get_latest_digest(conn: sqlite3.Connection, digest_type: str) -> Optional[DigestEntry]:
    row = conn.execute(
        "SELECT date FROM digest_entries WHERE type = ? ORDER BY date DESC LIMIT 1",
        (digest_type,),
    ).fetchone()
    if not row:
        return None
    return get_digest(conn, row["date"], digest_type)


def _row_to_raw_item(row: sqlite3.Row) -> RawItem:
    return RawItem(
        id=row["id"],
        source=row["source"],
        title=row["title"],
        url=row["url"],
        content=row["content"] or "",
        published_at=datetime.fromisoformat(row["published_at"]) if row["published_at"] else None,
        ingested_at=datetime.fromisoformat(row["ingested_at"]) if row["ingested_at"] else None,
        relevance_score=row["relevance_score"],
        cluster_id=row["cluster_id"],
        included_in_digest=bool(row["included_in_digest"]),
    )
