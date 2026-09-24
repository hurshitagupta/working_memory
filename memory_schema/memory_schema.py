from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryItem:
    content: str
    memory_type: str
    created_at: str
    consent: bool = False

    def validate(self) -> None:
        """Validate a memory before it is stored."""

        if not self.content.strip():
            raise ValueError("Memory content cannot be empty.")

        if self.memory_type not in {"short_term", "long_term"}:
            raise ValueError("memory_type must be 'short_term' or 'long_term'.")

        if self.memory_type == "long_term" and not self.consent:
            raise ValueError("Consent is required for long-term memory.")


def create_memory(content: str,memory_type: str = "short_term",consent: bool = False) -> MemoryItem:
    """Create and validate a memory item."""

    memory = MemoryItem(content=content,memory_type=memory_type,created_at=datetime.now().isoformat(timespec="seconds"),consent=consent)

    memory.validate()
    return memory


if __name__ == "__main__":
    print("=== MEMORY SCHEMA DEMO ===")

    print("\nHappy path:")

    memory = create_memory(content="User prefers concise examples.",memory_type="long_term",consent=True)

    print(memory)
    print("Status: accepted")

    print("\nFailure path:")

    try:
        create_memory(content="User prefers Python.",memory_type="long_term",consent=False)

    except ValueError as error:
        print(f"Status: rejected")
        print(f"Reason: {error}")