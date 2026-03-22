import tempfile
from pathlib import Path

import pytest
import yaml

from src.config import load_config


VALID_CONFIG = {
    "persona": "AI PM focused on building with AI",
    "topics": ["AI strategy", "LLMs"],
    "relevance_threshold": 7,
    "max_daily_stories": 8,
    "dedup_threshold": 0.5,
    "daily_token_budget": 40000,
    "sources": [
        {"name": "Test Feed", "url": "https://example.com/feed", "type": "rss"},
    ],
}


def write_config(data: dict) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    yaml.dump(data, f)
    f.close()
    return Path(f.name)


def test_load_valid_config():
    path = write_config(VALID_CONFIG)
    config = load_config(path)
    assert config.persona == "AI PM focused on building with AI"
    assert config.relevance_threshold == 7
    assert len(config.sources) == 1
    assert config.sources[0].name == "Test Feed"
    assert config.sources[0].type == "rss"


def test_missing_config_raises():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")


def test_invalid_source_type_raises():
    bad = {**VALID_CONFIG, "sources": [{"name": "Bad", "url": "https://x.com", "type": "twitter"}]}
    path = write_config(bad)
    with pytest.raises(ValueError, match="Unknown source type"):
        load_config(path)
