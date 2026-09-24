from memory_schema.memory_schema import MemoryItem, create_memory


class MemoryStore:
    def __init__(self) -> None:
        self.memories: list[MemoryItem] = []

    def store(self,content: str,memory_type: str = "short_term",consent: bool = False) -> MemoryItem:
        """ Create, validate, and store a memory."""

        memory = create_memory(content=content,memory_type=memory_type, consent=consent)

        self.memories.append(memory)
        return memory

    def recall(self, query: str) -> list[MemoryItem]:
        """Return memories containing the query text."""

        if not query.strip():
            raise ValueError("Recall query cannot be empty.")

        query_lower = query.lower()

        return [memory for memory in self.memories if query_lower in memory.content.lower()]


if __name__ == "__main__":
    print("=== STORE / RECALL DEMO ===")

    store = MemoryStore()

    print("\nStoring memories...")

    store.store(content="User prefers concise examples.",memory_type="long_term",consent=True)

    store.store(content="Discussed working memory module.",memory_type="short_term")

    print(f"Total memories stored: {len(store.memories)}")

    print("\nHappy path:")

    results = store.recall("concise")

    for memory in results:
        print(f"Recalled: {memory.content}")

    print(f"Matches found: {len(results)}")

    print("\nFailure path:")

    try:
        store.recall("")
    except ValueError as error:
        print("Status: rejected")
        print(f"Reason: {error}")