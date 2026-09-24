import pytest

from memory_schema.memory_schema import create_memory


def test_valid_long_term_memory():
    memory = create_memory(content="User prefers concise examples.",memory_type="long_term",consent=True)

    assert memory.content == "User prefers concise examples."
    assert memory.memory_type == "long_term"
    assert memory.consent is True


def test_long_term_memory_without_consent_is_rejected():
    with pytest.raises( ValueError, match="Consent is required for long-term memory"):
        create_memory(content="User prefers Python.",memory_type="long_term",consent=False)