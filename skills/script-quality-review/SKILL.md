---
name: script-quality-review
description: >
  Grade a generated test by what it asserts. A green exit or a verified
  badge is not a pass: skips, status-only 4xx checks, assertions that miss
  the case, unknown routes, and writes with no cleanup all fail. Read-only,
  no signup.
---

# Script Quality Review

A green run is not a real test. Read the script. No signup required.

## Prerequisites

- **None.** Reads the test files directly. No MCP.

## Trigger

- "Are these generated tests real?"
- "Grade this script"
- "Does a green run mean it passed?"

## Workflow

1. Read each test and the case title it claims to cover, if one is nearby.
2. Flag a test that hits any of these. Exit code 0 does not clear a flag.

**Skip counted as a pass** — `pytest.skip`, `@pytest.mark.skip`, `test.skip`, `it.skip`, `xit`, `test.fixme`, or the only path without extra credentials is a skip.

**4xx treated as a block** — success is only `status >= 400`, `status < 500`, or a set that includes 401, 403, or 404. A security test with no credentials that accepts 401 is an auth wall, not a blocked attack.

**Assertion misses the case** — the title's object (the signup, the marker, the named table) is never asserted, or a write is never read back.

**Unknown route** — the path is not in the project's routes or spec, or 404 is treated as success.

**Write with no undo** — a POST, PUT, or PATCH changes state and nothing restores it on failure.

3. For each hit, give `file:line`, the check, and the stronger assertion. Do not edit the file.

4. Output:

```
## Script Quality Review — 12 scripts

**2 skips counted as passes · 3 status-only · 1 misses the case · 1 unknown route · 1 write with no undo**

### Skip counted as a pass
- `test_signup.py:4` — the body is only `pytest.skip(...)`. Delete it or assert the signup guard.

### 4xx treated as a block
- `test_ssrf.py:18` — `status_code >= 400` also passes on 401 and 404. Assert the rejection reason.

**A green exit is not a pass.**
```
