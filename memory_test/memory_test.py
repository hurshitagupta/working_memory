from time import perf_counter

from privacy_lifecycle.privacy_lifecycle import PrivacyMemoryStore
from relevance_limits.relevance_limits import recall_relevant


MAX_STEPS = 5


def safe_store( store: PrivacyMemoryStore, content: str, memory_type: str = "short_term", consent: bool = False) -> None:
    """Store memory only if it does not contain obvious sensitive data."""

    sensitive_words = {"password", "api key","secret key","token"}

    content_lower = content.lower()

    for word in sensitive_words:
        if word in content_lower:
            raise ValueError("Sensitive information cannot be stored in memory.")

    store.store(content=content, memory_type=memory_type, consent=consent)


def run_memory_test() -> dict:
    """Run an end-to-end test of the working memory module."""

    store = PrivacyMemoryStore()
    steps = 0

    start_time = perf_counter()

    # Step 1: Store memories
    steps += 1
    if steps > MAX_STEPS:
        raise RuntimeError("Step limit exceeded.")

    safe_store(store,content="User prefers concise Python examples.",memory_type="long_term", consent=True)

    safe_store(store,content="Discussed working memory module.", memory_type="short_term")

    # Step 2: Recall relevant memory
    steps += 1
    if steps > MAX_STEPS:
        raise RuntimeError("Step limit exceeded.")

    recalled = recall_relevant(store=store,query="Python examples", limit=1)

    # Step 3: Apply access rule
    steps += 1
    if steps > MAX_STEPS:
        raise RuntimeError("Step limit exceeded.")

    accessible = store.access_memories(allow_long_term=False)

    # Step 4: Delete long-term memory
    steps += 1
    if steps > MAX_STEPS:
        raise RuntimeError("Step limit exceeded.")

    deleted = store.delete_memory("User prefers concise Python examples.")

    elapsed_ms = (perf_counter() - start_time) * 1000

    return {
        "steps": steps,
        "stored_before_delete": 2,
        "recalled_count": len(recalled),
        "accessible_count": len(accessible),
        "deleted": deleted,
        "remaining_memories": len(store.memories),
        "latency_ms": round(elapsed_ms, 3),
    }


if __name__ == "__main__":
    print("=== MEMORY TEST ===")

    print("\nHappy path:")

    result = run_memory_test()

    print(f"Steps completed: {result['steps']}")
    print(f"Memories stored: {result['stored_before_delete']}")
    print(f"Relevant memories recalled: {result['recalled_count']}")
    print(f"Accessible memories: {result['accessible_count']}")
    print(f"Memory deleted: {result['deleted']}")
    print(f"Remaining memories: {result['remaining_memories']}")
    print(f"Execution latency: {result['latency_ms']} ms")

    print("\nFailure path:")

    store = PrivacyMemoryStore()

    try:
        safe_store(store, content="My password is abc123", memory_type="long_term", consent=True)

    except ValueError as error:
        print("Status: rejected")
        print(f"Reason: {error}")