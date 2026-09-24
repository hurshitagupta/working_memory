from store_recall.store_recall import MemoryStore
import string

def relevance_score(query: str, text: str) -> int:
    """Calculate relevance using simple word overlap."""

    query = query.lower().translate(str.maketrans("", "", string.punctuation))

    text = text.lower().translate(str.maketrans("", "", string.punctuation))

    query_words = set(query.split())
    text_words = set(text.split())

    return len(query_words & text_words)


def recall_relevant( store: MemoryStore,query: str,limit: int = 3,) -> list[tuple[str, int]]:
    """Recall the most relevant memories up to the given limit."""

    if not query.strip():
        raise ValueError("Recall query cannot be empty.")

    if limit <= 0:
        raise ValueError("Limit must be greater than 0.")

    scored_memories = []

    for memory in store.memories:
        score = relevance_score(query, memory.content)

        if score > 0:
            scored_memories.append((memory.content, score))

    scored_memories.sort( key=lambda item: item[1],reverse=True)

    return scored_memories[:limit]


if __name__ == "__main__":
    print("=== RELEVANCE LIMITS DEMO ===")

    store = MemoryStore()

    store.store(content="User prefers concise Python examples.",memory_type="long_term",consent=True)

    store.store(content="User likes Python programming.",memory_type="short_term")

    store.store(content="Discussed working memory concepts.",memory_type="short_term")

    print("\nHappy path:")

    results = recall_relevant(store=store,query="Python examples",limit=2)

    print(f"Results returned: {len(results)}")

    for content, score in results:
        print(f"Memory: {content}")
        print(f"Relevance score: {score}")

    print("\nFailure path:")

    try:
        recall_relevant(store=store,query="Python",limit=0)

    except ValueError as error:
        print("Status: rejected")
        print(f"Reason: {error}")