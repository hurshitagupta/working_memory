from datetime import datetime, timedelta

from store_recall.store_recall import MemoryStore


class PrivacyMemoryStore(MemoryStore):
    def delete_memory(self, content: str) -> bool:
        """Delete a memory matching the given content."""

        for memory in self.memories:
            if memory.content == content:
                self.memories.remove(memory)
                return True

        return False

    def clear_expired_short_term(self,retention_minutes: int = 60,) -> int:
        """Remove short-term memories older than the retention period."""

        if retention_minutes <= 0:
            raise ValueError("Retention period must be greater than 0.")

        cutoff = datetime.now() - timedelta(minutes=retention_minutes)

        original_count = len(self.memories)

        self.memories = [memory for memory in self.memories
            if not ( memory.memory_type == "short_term" and datetime.fromisoformat(memory.created_at) < cutoff)
        ]

        return original_count - len(self.memories)

    def access_memories(self,allow_long_term: bool = False,) -> list[str]:
        """Return memories based on access permission."""

        results = []

        for memory in self.memories:
            if memory.memory_type == "long_term" and not allow_long_term:
                continue

            results.append(memory.content)

        return results


if __name__ == "__main__":
    print("=== PRIVACY LIFECYCLE DEMO ===")

    store = PrivacyMemoryStore()

    store.store(content="User prefers concise examples.",memory_type="long_term",consent=True)

    store.store(content="Discussed working memory today.",memory_type="short_term")

    print("\nMemories stored:")
    print(f"Total memories: {len(store.memories)}")

    print("\nAccess without long-term permission:")

    results = store.access_memories( allow_long_term=False)

    for result in results:
        print(f"Accessible: {result}")

    print(f"Accessible memories: {len(results)}")

    print("\nDeletion:")

    deleted = store.delete_memory("User prefers concise examples.")

    print(f"Memory deleted: {deleted}")
    print(f"Remaining memories: {len(store.memories)}")

    print("\nFailure path:")

    try:
        store.clear_expired_short_term(retention_minutes=0)

    except ValueError as error:
        print("Status: rejected")
        print(f"Reason: {error}")