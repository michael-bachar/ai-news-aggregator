from src.models import RawItem
from src.pipeline.dedup import deduplicate, jaccard


def _item(title: str, content: str = "") -> RawItem:
    return RawItem(source="test", title=title, url=f"https://example.com/{title}", content=content, published_at=None)


def test_jaccard_identical():
    assert jaccard("hello world", "hello world") == 1.0


def test_jaccard_disjoint():
    assert jaccard("hello world", "foo bar") == 0.0


def test_jaccard_partial():
    score = jaccard("openai releases gpt5", "openai announces gpt5 launch")
    assert 0 < score < 1.0


def test_dedup_removes_near_duplicate():
    items = [
        _item("OpenAI releases GPT-5", content="short"),
        _item("OpenAI announces GPT-5 launch", content="much longer content here"),
        _item("Anthropic releases Claude 4", content="different story"),
    ]
    result = deduplicate(items, threshold=0.4)
    assert len(result) == 2
    # Should keep the item with longer content
    gpt_item = next(i for i in result if "GPT" in i.title)
    assert gpt_item.content == "much longer content here"


def test_dedup_keeps_distinct_items():
    items = [
        _item("OpenAI releases GPT-5"),
        _item("Anthropic releases Claude 4"),
        _item("Google releases Gemini 3"),
    ]
    result = deduplicate(items, threshold=0.5)
    assert len(result) == 3


def test_dedup_empty():
    assert deduplicate([]) == []
