import pytest

from memory_test.memory_test import run_memory_test, safe_store
from privacy_lifecycle.privacy_lifecycle import PrivacyMemoryStore


def test_complete_memory_workflow():
    result = run_memory_test()

    assert result["steps"] == 4
    assert result["stored_before_delete"] == 2
    assert result["recalled_count"] == 1
    assert result["accessible_count"] == 1
    assert result["deleted"] is True
    assert result["remaining_memories"] == 1
    assert result["latency_ms"] >= 0


def test_sensitive_memory_is_rejected():
    store = PrivacyMemoryStore()

    with pytest.raises( ValueError, match="Sensitive information cannot be stored",):
        safe_store(store,content="My password is abc123", memory_type="long_term", consent=True)

    assert len(store.memories) == 0