import tempfile
from pathlib import Path
from datetime import datetime


from src.db import db, init_db, upsert_item, get_unscored_items, update_item_score
from src.models import RawItem


def temp_db() -> Path:
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    f.close()
    return Path(f.name)


def _item(url: str = "https://example.com/1") -> RawItem:
    return RawItem(
        source="Test",
        title="Test headline",
        url=url,
        content="Some content",
        published_at=datetime(2026, 3, 21),
    )


def test_init_and_upsert():
    path = temp_db()
    init_db(path)
    with db(path) as conn:
        row_id = upsert_item(conn, _item())
    assert row_id is not None


def test_upsert_duplicate_returns_none():
    path = temp_db()
    init_db(path)
    with db(path) as conn:
        first = upsert_item(conn, _item())
        second = upsert_item(conn, _item())
    assert first is not None
    assert second is None


def test_get_unscored_items():
    path = temp_db()
    init_db(path)
    with db(path) as conn:
        upsert_item(conn, _item("https://example.com/unscored"))
        items = get_unscored_items(conn, since_hours=1)
    assert any(i.url == "https://example.com/unscored" for i in items)


def test_update_score():
    path = temp_db()
    init_db(path)
    with db(path) as conn:
        row_id = upsert_item(conn, _item())
        update_item_score(conn, row_id, 8)
        items = get_unscored_items(conn, since_hours=1)
    # After scoring, item should not appear in unscored list
    assert not any(i.relevance_score is None for i in items if i.id == row_id)
