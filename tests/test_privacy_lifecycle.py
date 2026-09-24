import pytest

from privacy_lifecycle.privacy_lifecycle import PrivacyMemoryStore


def test_delete_memory_and_access_rules():
    store = PrivacyMemoryStore()

    store.store(content="User prefers concise examples.", memory_type="long_term",consent=True)

    store.store(content="Discussed working memory today.", memory_type="short_term")

    accessible = store.access_memories( allow_long_term=False)

    assert "User prefers concise examples." not in accessible

    assert "Discussed working memory today." in accessible

    deleted = store.delete_memory( "User prefers concise examples.")

    assert deleted is True
    assert len(store.memories) == 1


def test_invalid_retention_period_is_rejected():
    store = PrivacyMemoryStore()

    with pytest.raises(ValueError, match="Retention period must be greater than 0"):
        store.clear_expired_short_term( retention_minutes=0)