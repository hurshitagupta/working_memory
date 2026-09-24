import pytest

from store_recall.store_recall import MemoryStore


def test_store_and_recall_memory():
    store = MemoryStore()

    store.store(content="User prefers concise examples.",memory_type="long_term",consent=True)

    store.store(content="Discussed working memory module.",memory_type="short_term")

    results = store.recall("concise")

    assert len(results) == 1
    assert results[0].content == "User prefers concise examples."


def test_empty_recall_query_is_rejected():
    store = MemoryStore()

    with pytest.raises(ValueError, match="Recall query cannot be empty"):
        store.recall("")