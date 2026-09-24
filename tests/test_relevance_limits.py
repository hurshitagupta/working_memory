import pytest

from store_recall.store_recall import MemoryStore
from relevance_limits.relevance_limits import recall_relevant


def test_relevant_memories_are_ranked_and_limited():
    store = MemoryStore()

    store.store(content="User prefers concise Python examples.",memory_type="long_term",consent=True)

    store.store(content="User likes Python programming.",memory_type="short_term")

    store.store(content="Discussed working memory concepts.",memory_type="short_term")

    results = recall_relevant(store=store,query="Python examples",limit=1)

    assert len(results) == 1
    assert results[0][0] == "User prefers concise Python examples."
    assert results[0][1] == 2


def test_invalid_limit_is_rejected():
    store = MemoryStore()

    with pytest.raises(ValueError,match="Limit must be greater than 0"):
        recall_relevant(store=store, query="Python", limit=0)