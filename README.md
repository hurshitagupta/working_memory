#  Build a Working Memory Module

This project implements the core concepts of a working memory module, including memory schema, storing and recalling memories, relevance limits, privacy, and lifecycle controls.

## Task 1 — Memory Schema

Task 1 defines the structure of a memory item and validates whether a memory is allowed to be created.

Each memory contains:

* `content` — the actual information stored in memory
* `memory_type` — either `short_term` or `long_term`
* `created_at` — timestamp showing when the memory was created
* `consent` — whether permission was given for durable memory storage

The implementation also validates memory before it is accepted.

### Validation Rules

The following checks are applied:

* Memory content cannot be empty.
* Memory type must be either `short_term` or `long_term`.
* Long-term memory requires explicit consent.

A long-term memory without consent is rejected instead of being stored.

## Run Task 1

Run the memory schema demonstration:

```bash
python -m memory_schema.memory_schema
```

## Run Automated Tests

```bash
pytest tests/test_memory_schema.py -v
```

## Evidence

The implementation demonstrates both required paths:

**Success case:**
A valid long-term memory with consent is successfully created.

**Failure case:**
A long-term memory without consent is rejected with a `ValueError`.

Automated tests verify both behaviors.

## Guardrails

Task 1 includes the following safeguards:

* **Validation:** Invalid memory content and unsupported memory types are rejected.
* **Consent:** Long-term memory cannot be created without explicit consent.
* **Privacy boundary:** Information is not automatically converted into durable memory.
* **Secret hygiene:** No credentials or secrets are stored in the source code.

Step limits, retries, and timeouts are not required for this task because the implementation does not contain loops, external API calls, retries, or blocking operations.

---

## Task 2 — Store/Recall

Task 2 implements the basic memory storage and recall behavior.

It reuses the memory schema created in Task 1 instead of defining a new schema.

### Implementation

The `MemoryStore` class provides two main operations:

* `store()` — creates, validates, and stores a memory.
* `recall()` — searches stored memories using a text query.

The `store()` method uses the `create_memory()` function from Task 1, so all existing validation rules still apply before a memory is stored.

The `recall()` method performs a simple case-insensitive text search across stored memories.

### Success Path

A valid memory is stored and successfully recalled using a matching query.

### Failure Path

An empty recall query is rejected with a `ValueError`.

This prevents invalid recall requests from being processed.

## Run Task 2

Run the store/recall demonstration:

```bash
python -m store_recall.store_recall
```

## Run Automated Tests

```bash
pytest tests/test_store_recall.py -v
```

## Evidence

The implementation demonstrates both required paths:

**Success case:**
A valid memory is stored and recalled successfully.

**Failure case:**
An empty recall query is rejected.

The output also provides basic observable measurements:

* Total number of memories stored
* Number of matching memories recalled

## Reuse from Task 1

Task 2 imports and reuses:

```python
from memory_schema import MemoryItem, create_memory
```

This ensures that memory validation remains centralized and is not duplicated across tasks.

## Guardrails

The following safeguards apply:

* **Validation:** Memory validation from Task 1 is applied before storage.
* **Recall validation:** Empty recall queries are rejected.
* **Consent:** Long-term memories still require consent because Task 2 uses the Task 1 schema.
* **Secret hygiene:** No credentials or secrets are stored in the source code.

Step limits, retries, and timeouts are not applicable here because this task uses only local in-memory operations and does not contain loops, external API calls, or blocking operations.


