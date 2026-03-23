from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.config import load_config
from src.db import db, get_available_dates, get_digest, get_latest_digest
from src.digest import run_daily, run_weekly

TEMPLATES_DIR = Path(__file__).parent / "templates"
DB_PATH = Path(os.environ.get("DB_PATH", "data/news.db"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    config = load_config()
    db_path = Path(os.environ.get("DB_PATH", "data/news.db"))
    scheduler = BackgroundScheduler()

    def _run_daily() -> None:
        try:
            run_daily(config, db_path)
        except Exception as e:
            print(f"[scheduler] daily job failed: {e}", flush=True)

    def _run_weekly() -> None:
        try:
            run_weekly(config, db_path)
        except Exception as e:
            print(f"[scheduler] weekly job failed: {e}", flush=True)

    scheduler.add_job(_run_daily, "cron", hour=11, minute=0)
    scheduler.add_job(_run_weekly, "cron", day_of_week="sun", hour=22, minute=0)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="AI News Digest", lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _domain_from_url(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception:
        return ""


templates.env.filters["domain"] = _domain_from_url


@app.get("/", response_class=HTMLResponse)
async def daily(request: Request, date: Optional[str] = None):
    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    with db(DB_PATH) as conn:
        entry = get_digest(conn, date, "daily")
        if entry is None:
            entry = get_latest_digest(conn, "daily")
        available_dates = get_available_dates(conn, "daily")

    return templates.TemplateResponse(
        "daily.html",
        {"request": request, "entry": entry, "date": date, "available_dates": available_dates},
    )


@app.get("/weekly", response_class=HTMLResponse)
async def weekly(request: Request):
    with db(DB_PATH) as conn:
        entry = get_latest_digest(conn, "weekly")

    return templates.TemplateResponse(
        "weekly.html",
        {"request": request, "entry": entry},
    )
