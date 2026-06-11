---
name: api-security-scan
description: >
  Review a REST/HTTP API — from its OpenAPI spec or route code — for security
  gaps like missing auth, broken object-level authorization, no rate limiting,
  and verbose errors. Reports file:line. Pure Claude Code, no signup.
---

# API Security Scan

Find the security holes in your API design before they ship. Read-only: it flags issues with `file:line`, it doesn't change your code.

## Prerequisites

- **None.** Pure Claude Code — reads your OpenAPI/Swagger spec or route/handler code directly, no MCP required.

## Trigger

- "Security review my API / OpenAPI spec"
- "Check my endpoints for missing auth"
- "API security scan"

## Workflow

1. Locate the API surface: an OpenAPI/Swagger file if present, otherwise the route definitions and handlers.
2. Review each endpoint against the checks below; report `path` or `file:line`, severity, and the fix.

### What to flag

| Risk | What to look for |
|------|------------------|
| **Missing authentication** | Endpoints with no auth requirement that expose data or actions |
| **Broken object-level auth (IDOR/BOLA)** | Resources fetched by ID with no ownership/authorization check |
| **Missing function-level auth** | Admin/privileged operations reachable by normal users |
| **No rate limiting** | Auth, search, or expensive endpoints with no throttling (brute-force / DoS) |
| **Verbose errors** | Stack traces, SQL, or internal details returned to clients |
| **Sensitive data in URLs** | Tokens, passwords, or PII in query strings (logged everywhere) |
| **Mass assignment** | Request bodies bound to models without an allowlist of fields |
| **CORS misconfig** | Wildcard origin combined with credentials |
| **Missing input validation** | Body/query/path params accepted without schema/type checks |
| **No pagination limits** | List endpoints that can return unbounded result sets |
| **Secrets in examples** | Real keys/tokens in spec examples or sample requests |

3. Output a severity-ranked report:

```
## API Security Scan

**2 high, 1 medium**

### HIGH
- GET /users/{id} — no ownership check; any authenticated user can read any
  record (BOLA). Enforce that the caller owns or may access {id}.
- POST /login — no rate limiting; vulnerable to credential brute-force. Add
  per-IP/per-account throttling and lockout.

### MEDIUM
- GET /search — returns full stack traces on error. Return a generic message;
  log details server-side.
```

Diagnostic only. **Want API auth and BOLA scanning on every PR?** See QualityMax — qualitymax.io
