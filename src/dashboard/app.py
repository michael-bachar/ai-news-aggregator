from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.db import db, get_available_dates, get_digest, get_latest_digest

TEMPLATES_DIR = Path(__file__).parent / "templates"
DB_PATH = Path(os.environ.get("DB_PATH", "data/news.db"))

app = FastAPI(title="AI News Digest")
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
