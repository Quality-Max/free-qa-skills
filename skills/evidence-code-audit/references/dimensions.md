# Audit dimensions

Use relevant rows for a focused or incremental audit. A full audit considers all
26 rows; an absent surface is **Not assessed — not applicable**, not a clean score.
These are investigation prompts, not automatic finding rules. Follow the failure
path and check protections before reporting a defect.

| Dimension | Trace and verify |
|-----------|------------------|
| Security | Authentication and object ownership from entry point through data access; untrusted input into SQL, shell, paths, and HTML; actual authorization guards. |
| Stability | Expected invalid input, partial failures, cancellation, and resource cleanup; whether errors reach callers instead of becoming false success. |
| Performance | Hot-path I/O, query count, pagination, allocations, and input bounds; connect an alleged bottleneck to actual workload evidence. |
| Architecture | Ownership and dependency boundaries; conflicting sources of truth or incompatible contracts that cause a concrete failure. |
| Maintainability | Duplicated business rules or opaque control flow that already produce divergent behavior; avoid size-only findings. |
| Testing | Critical behavior asserted, negative paths and fixtures; whether the test would fail if that behavior broke. |
| Testing authenticity | Skips and early returns counted as success, assertion-free runs, status-only failures, unknown routes/selectors, mocks hiding the claimed behavior. |
| Documentation | Public examples and setup guidance against implemented contracts; identify a specific broken instruction or promise. |
| Design | Business invariants and state transitions; invalid combinations that the model or workflow permits. |
| Code consistency | Similar handlers implementing the same contract differently; distinguish intentional policy differences from defects. |
| Dependency weight | Dependencies loaded on critical paths and duplicate implementations; avoid speculative size or latency claims. |
| Comment coverage | Undocumented non-obvious invariants or misleading comments linked to an actual misuse; missing comments alone are not findings. |
| Type safety | Nullability, unchecked parsing, casts, and interface assumptions at boundaries; trace a reachable invalid value. |
| AI safety | Untrusted retrieved content into prompts, model output into tools, server-owned authorization, bounded steps/cost, and output validation. |
| Fallback behavior | Timeout/retry exhaustion and degraded paths; no silent success, weaker authorization, or repeated side effects. |
| Backend API | Request validation, tenant scope, response contracts, pagination, and idempotency across routes and callers. |
| Frontend state | Async response ordering, stale caches, optimistic rollback, and visible error states; compare UI assumptions to API behavior. |
| Observability | A specific failure can be detected and attributed without sensitive payloads; distinguish missing evidence from proof of healthy operation. |
| Configuration | Required non-sensitive settings, defaults, precedence, and web/worker parity; inspect named keys without dumping configuration. |
| Supply chain | Lockfile/manifests alignment, untrusted build hooks, artifact provenance, and provided advisory evidence; no network scans or package installation. |
| Release | Code, schema, and artifact compatibility, migration ordering, rollback assumptions, and existing release-check evidence; do not deploy. |
| Data integrity | Tenant-safe queries, transactions, nullable values, cursor ordering, uniqueness, durable writes before acknowledgments, and repeat-call invariants. |
| Privacy | Collection, retention, access, and logging of personal data; report paths and behavior without copying user data. |
| Accessibility | Source-level semantics, labels, keyboard/focus behavior, and error announcements; runtime contrast or interaction remains unassessed without supplied evidence. |
| Cost | Input, retry, job, and model/tool budgets; runaway work or billing duplication tied to reachable paths, without invented pricing. |
| Concurrency | Shared state across workers, lock scope, races, cancellation, deadlocks, and idempotency under overlapping requests. |

## Coverage example

| Dimension | Coverage | Evidence inspected | Limits |
|-----------|----------|--------------------|--------|
| Data integrity | High | Submit handler, storage transaction, queue consumer, duplicate-delivery test assertions | Source review; no database or runtime execution |
| Concurrency | Medium | Worker state ownership and retry paths | Deployment worker count not available |
| Accessibility | Not assessed | None | Outside this backend audit |

High source-review coverage does not establish runtime success. A passed command
or empty error window supplied by the user only supports what it actually checked.

## Finding example

**F-001 — Acknowledgment precedes durable storage**

- **Severity / confidence:** High / High (source-traced).
- **Evidence:** `routes/submit.py:48` acknowledges the accepted item before
  `repositories/items.py:77` persists it; the exception path drops the item.
- **Trigger and impact:** storage fails after the acknowledgment; the caller
  believes the item was accepted, and a retry is suppressed despite lost work.
- **Minimal fix:** persist successfully before acknowledging; return the existing
  retryable failure response if storage fails.
- **Regression scenario:** inject a storage failure and assert a retryable response
  with no success acknowledgment; retry successfully and assert one durable item.

This is a fictional example, not a finding about the repository being audited.

## Provenance

Adapted from [XiNian-dada/Fuck_My_Shit_Mountain](https://github.com/XiNian-dada/Fuck_My_Shit_Mountain/tree/8354e7bfb27e3647cbb74068304a0fe25c0f856e),
particularly its audit dimensions, evidence rubric, and separation of severity,
finding confidence, and coverage confidence.

The adaptation removes mandatory intake questions, numeric scoring, fixed report
templates, audit-file writes, and executable helpers. It adds merge-base branch
scope, impact-based finding thresholds, prompt-injection boundaries, and complete
credential redaction. Concurrency is included in the full checklist.

Files under `skills/evidence-code-audit/` retain the upstream MIT terms in
[LICENSE](../LICENSE). The collection's other files retain their existing licenses.
