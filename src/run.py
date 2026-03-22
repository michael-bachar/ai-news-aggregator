"""CLI entrypoint: python -m src.run --daily | --weekly"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.config import load_config
from src.digest import run_daily, run_weekly

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI News Aggregator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--daily", action="store_true", help="Run daily digest pipeline")
    group.add_argument("--weekly", action="store_true", help="Run weekly synthesis pipeline")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--db", default="data/news.db", help="Path to SQLite database")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except FileNotFoundError as e:
        logger.error("%s — copy config.example.yaml to config.yaml and fill in your sources.", e)
        sys.exit(1)

    db_path = Path(args.db)

    if args.daily:
        entry = run_daily(config, db_path)
        if entry:
            logger.info("Done. %d stories in today's digest.", len(entry.clusters))
    elif args.weekly:
        entry = run_weekly(config, db_path)
        if entry:
            logger.info("Done. %d themes in this week's digest.", len(entry.clusters))
        else:
            logger.info("No weekly digest generated.")


if __name__ == "__main__":
    main()
