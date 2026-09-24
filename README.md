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

---

## Task 3 — Relevance Limits

Task 3 adds relevance-based recall and result limits to the working memory module.

It reuses the `MemoryStore` created in Task 2 and ranks stored memories based on how many query words match the memory content.

### Implementation

The task introduces two functions:

* `relevance_score()` — calculates a simple relevance score using word overlap.
* `recall_relevant()` — returns only relevant memories, sorted by score and restricted by a result limit.

Before comparing words, punctuation is removed so values such as `examples` and `examples.` are treated as the same word.

The higher-scoring memory is returned first.

### Limit Handling

The `limit` argument controls the maximum number of memories returned.

For example:

```python
recall_relevant(store=store,query="Python examples",limit=1)
```

returns only the highest-ranked matching memory.

A limit of `0` or less is rejected with a `ValueError`.

## Success Path

Relevant memories are scored, ranked, and limited successfully.


## Failure Path

An invalid limit is rejected.


## Run Task 3

Run the relevance limits demonstration:

```bash
python -m relevance_limits.relevance_limits
```

## Run Automated Tests

```bash
pytest tests/test_relevance_limits.py -v
```

## Evidence

The automated tests verify:

**Success case:**

* Relevant memories are ranked correctly.
* Higher-scoring memories are returned first.
* The requested result limit is respected.

**Failure case:**

* Invalid limits are rejected.

The output also provides observable measurements through:

* Relevance score
* Number of results returned

## Reuse from Previous Tasks

Task 3 imports and reuses:

```python
from store_recall import MemoryStore
```

This means memory creation and validation continue to use the logic already implemented in Tasks 1 and 2.

## Guardrails

The following safeguards apply:

* **Validation:** Empty queries and invalid limits are rejected.
* **Relevance boundary:** Memories with a relevance score of `0` are not returned.
* **Result limit:** Recall results are capped using the requested limit.
* **Consent:** Long-term memory still follows the consent rules from Task 1.
* **Secret hygiene:** No secrets or credentials are included in the implementation.

Retries and timeouts are not applicable because this task uses only local in-memory processing and does not make external calls.

---

## Task 4 — Privacy Lifecycle

Task 4 implements privacy and lifecycle controls for the working memory module.

The assessment specifically states that durable memory requires:

* Consent
* Retention
* Deletion
* Access rules

This task reuses the previous memory store and adds these lifecycle behaviors without duplicating earlier validation logic.

### Implementation

The `PrivacyMemoryStore` class extends `MemoryStore` from Task 2.

It adds:

* `delete_memory()` — removes a stored memory.
* `clear_expired_short_term()` — removes short-term memories that exceed the retention period.
* `access_memories()` — controls whether long-term memories can be accessed.

Consent for long-term memory is already enforced by the memory schema from Task 1.

### Consent

Long-term memory still requires explicit consent.

Because Task 4 inherits the previous memory implementation, this rule remains active:

```python
store.store(
    content="User prefers concise examples.", memory_type="long_term", consent=True)
```

A long-term memory without consent is rejected before storage.

### Retention

Short-term memories can be removed after a configured retention period.

The implementation checks the creation time of short-term memories and removes those older than the configured retention window.

Invalid retention values such as `0` or negative values are rejected.

### Deletion

Stored memories can be explicitly deleted.

The method returns `True` when a matching memory is successfully removed.

### Access Rules

Long-term memory is not automatically exposed to every caller.

Example:

```python
store.access_memories(allow_long_term=False)
```

When long-term access is disabled, only allowed memories are returned.

This demonstrates that storing information and accessing information are treated as separate operations.

## Success Path

The implementation demonstrates:

* Memories are stored successfully.
* Long-term memories can be restricted from access.
* A stored memory can be deleted.
* Remaining memory counts can be observed.

## Failure Path

An invalid retention period is rejected.

## Run Task 4

Run the privacy lifecycle demonstration:

```bash
python -m privacy_lifecycle.privacy_lifecycle
```

## Run Automated Tests

```bash
pytest tests/test_privacy_lifecycle.py -v
```

## Evidence

The implementation demonstrates the required privacy lifecycle controls:

* **Consent** — long-term memory continues to require consent from Task 1.
* **Retention** — short-term memory can be removed using a retention rule.
* **Deletion** — stored memory can be explicitly removed.
* **Access rules** — long-term memory can be hidden when access is not allowed.

## Reuse from Previous Tasks

Task 4 imports and reuses the earlier memory implementation:

```python
from store_recall import MemoryStore
```

This means memory creation, validation, storage, recall, and consent rules remain centralized.

## Guardrails

The following safeguards apply:

* **Validation:** Invalid retention values are rejected.
* **Consent:** Long-term memory requires explicit consent.
* **Retention:** Short-term memory follows a defined retention window.
* **Deletion:** Stored memories can be removed.
* **Access control:** Long-term memory access can be restricted.
* **Secret hygiene:** No credentials or secrets are stored in source code.

Retries and timeouts are not applicable because this task uses only local in-memory operations and does not call external services.

---

## Task 5 — Memory Test

Task 5 performs an end-to-end test of the working memory module.

It reuses the implementations from the previous tasks and verifies that storage, relevance-based recall, access control, deletion, validation, and measurement work together correctly.

### Implementation

Task 5 uses:

```python
from privacy_lifecycle.privacy_lifecycle import PrivacyMemoryStore
from relevance_limits.relevance_limits import recall_relevant
```

This avoids duplicating earlier logic.

The workflow is:

1. Store valid memories.
2. Recall the most relevant memory.
3. Apply access restrictions.
4. Delete a stored memory.
5. Record execution measurements.

A `safe_store()` function is also added to reject obvious sensitive information before it enters memory.

### Sensitive Data Protection

The assessment states that secrets or sensitive information should not be stored merely because they are mentioned.

The implementation checks for obvious sensitive terms such as:

```text
password
api key
secret key
token
```

If detected, the memory is rejected before storage.


### Step Limit

The complete workflow uses a hard step limit:

```python
MAX_STEPS = 5
```

The current workflow completes in four steps.

This provides a simple safeguard against unexpectedly long execution flows.

### Measurement

Execution time is measured using `perf_counter()`.

The final result reports:

* Steps completed
* Memories stored
* Relevant memories recalled
* Accessible memories
* Deletion status
* Remaining memories
* Execution latency

### Success Path

The successful workflow performs:

```text
Store
→ Recall
→ Access Control
→ Delete
```

### Failure Path

Sensitive information is rejected before it is stored.

The automated test also confirms that the memory store remains empty after rejection.

## Run Task 5

Run the complete memory test:

```bash
python -m memory_test.memory_test
```

## Run Automated Tests

```bash
pytest tests/test_memory_test.py -v
```


## Evidence

The automated tests verify:

**Success case:**

* Memories are stored successfully.
* Relevant memory is recalled.
* Access rules are applied.
* A memory is deleted successfully.
* Memory counts are correct.
* Execution latency is recorded.

**Failure case:**

* Sensitive information is rejected.
* Rejected sensitive information is not added to memory.


## Guardrails

The following safeguards are demonstrated:

* **Step limit:** The workflow has a hard maximum number of execution steps.
* **Validation:** Invalid and sensitive memory writes are rejected.
* **Consent:** Long-term memory continues to require consent.
* **Relevance limit:** Recall results remain limited and relevance-based.
* **Privacy lifecycle:** Access and deletion rules are applied.
* **Secret hygiene:** Sensitive information is rejected before memory storage.
* **Measurement:** Execution latency and memory counts are recorded.

Retries and external-operation timeouts are not required because this implementation uses only local in-memory operations and does not perform external service calls.




