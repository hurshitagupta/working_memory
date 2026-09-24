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


