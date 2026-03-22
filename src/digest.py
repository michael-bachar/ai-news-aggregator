from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import anthropic

from src.config import Config
from src.db import (
    db,
    get_scored_items,
    init_db,
    save_digest,
    update_item_cluster,
    update_item_score,
    upsert_item,
)
from src.ingestion.rss import fetch_all_rss
from src.ingestion.youtube import fetch_all_youtube
from src.models import DigestEntry, RawItem
from src.pipeline.clustering import cluster_items
from src.pipeline.dedup import deduplicate
from src.pipeline.scoring import score_items
from src.pipeline.synthesis import synthesize_all, synthesize_weekly

logger = logging.getLogger(__name__)


def _ingestion_to_raw(item) -> RawItem:

    return RawItem(
        source=item.source,
        title=item.title,
        url=item.url,
        content=item.content,
        published_at=item.published_at,
    )


def run_daily(config: Config, db_path: Path = Path("data/news.db")) -> DigestEntry | None:
    """Run the full daily pipeline. Returns the DigestEntry or None on quiet day."""
    init_db(db_path)
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.utcnow().strftime("%Y-%m-%d")

    logger.info("=== Daily digest: %s ===", today)

    # 1. Ingest
    rss_items = fetch_all_rss(config.sources)
    yt_items = fetch_all_youtube(config.sources)
    ingested = rss_items + yt_items
    logger.info("Ingested %d raw items", len(ingested))

    # 2. Persist new items to DB (skip duplicates)
    raw_items: list[RawItem] = []
    with db(db_path) as conn:
        for item in ingested:
            raw = _ingestion_to_raw(item)
            row_id = upsert_item(conn, raw)
            if row_id is not None:
                raw.id = row_id
                raw_items.append(raw)

    logger.info("%d new items after deduplication against DB", len(raw_items))

    if not raw_items:
        logger.info("No new items today — quiet day.")
        return _quiet_day_digest(today, "daily")

    # 3. Deduplicate by headline similarity
    deduped = deduplicate(raw_items, threshold=config.dedup_threshold)
    logger.info("%d items after Jaccard deduplication", len(deduped))

    # 4. Score
    scored = score_items(client, config, deduped)

    # Persist scores
    with db(db_path) as conn:
        for scored_item in deduped:
            if scored_item.id and scored_item.relevance_score is not None:
                update_item_score(conn, scored_item.id, scored_item.relevance_score)

    if not scored:
        logger.info("No items passed relevance threshold — quiet day.")
        return _quiet_day_digest(today, "daily")

    # 5. Cluster
    clusters = cluster_items(client, config, scored)

    # 6. Synthesize
    summaries = synthesize_all(client, config, clusters, config.max_daily_stories)

    # Persist cluster assignments
    with db(db_path) as conn:
        for cluster_id, cluster_items_list in clusters.items():
            for clustered_item in cluster_items_list:
                if clustered_item.id:
                    update_item_cluster(conn, clustered_item.id, cluster_id)

    # 7. Save digest
    entry = DigestEntry(date=today, type="daily", clusters=summaries)
    with db(db_path) as conn:
        save_digest(conn, entry)

    logger.info("Daily digest complete: %d stories", len(summaries))
    return entry


def run_weekly(config: Config, db_path: Path = Path("data/news.db")) -> DigestEntry | None:
    """
    Run the weekly synthesis. Pulls this week's daily digest items and synthesizes 3 themes.
    """
    init_db(db_path)
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    today = datetime.utcnow()
    week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    week_date = today.strftime("%Y-%m-%d")

    logger.info("=== Weekly digest: week of %s ===", week_start)

    # Pull all scored items from the past 7 days
    with db(db_path) as conn:
        recent_items = get_scored_items(conn, config.relevance_threshold, since_hours=7 * 24)

    if not recent_items:
        logger.info("No items this week — skipping weekly digest.")
        return None

    # Cluster and synthesize the whole week
    clusters = cluster_items(client, config, recent_items)
    daily_summaries = synthesize_all(client, config, clusters, max_stories=30)
    weekly_themes = synthesize_weekly(client, config, daily_summaries)

    entry = DigestEntry(date=week_date, type="weekly", clusters=weekly_themes)
    with db(db_path) as conn:
        save_digest(conn, entry)

    logger.info("Weekly digest complete: %d themes", len(weekly_themes))
    return entry


def _quiet_day_digest(date: str, digest_type: str) -> DigestEntry:
    from src.models import ClusterSummary

    return DigestEntry(
        date=date,
        type=digest_type,
        clusters=[
            ClusterSummary(
                cluster_id="quiet-day",
                headline="Quiet day — nothing made the cut",
                synthesis="No items passed the relevance threshold today. Check back tomorrow.",
                why_it_matters="",
                sources=[],
            )
        ],
    )
