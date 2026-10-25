---
name: railway-exposure-audit
description: >
  Audit a Railway deployment's public domains, TCP proxies, private networking,
  service bindings, trust boundaries, and repository configuration for accidental
  exposure without dumping variables, logs, credentials, or provider configuration.
---

# Railway Exposure Audit

Map what a Railway deployment exposes and whether each boundary is intentional and protected. Public reachability, weak protection, vulnerability, and compromise are separate conclusions.

## Prerequisites

- A local repository and, when available, a user-supplied Railway project or deployment view.
- Current access to Railway's official networking documentation for platform semantics.
- Optional read-only provider access. The repository-only path must still produce useful results and explicit verification gaps.

## Trigger

- "Audit our Railway exposure"
- "Is our Railway database or Redis public?"
- "Check Railway domains, TCP proxies, and private networking"
- "Review this app's Railway deployment security"

## Workflow

1. **Define the boundary.** Record the project/environment/services in scope and the observation time. Start from local deployment files, Dockerfiles, application bindings, framework settings, and documentation. Treat names and URLs as potentially sensitive; do not reproduce internal identifiers unnecessarily.

2. **Build a service exposure map.** For each service, record only the minimum non-sensitive facts:

   - role and protocol;
   - Railway-provided or custom public HTTP domain present/absent;
   - public TCP proxy present/absent and exposed protocol/port;
   - private-network endpoint expected/present;
   - application listen address and port source;
   - authentication boundary and intended callers;
   - health, metrics, debug, admin, database, cache, queue, and object-storage surfaces.

   Prefer presence/status checks over full objects. Never retrieve all variables or logs. Do not use provider commands or views that return secrets or whole configurations.

3. **Verify Railway networking semantics.** Use current official documentation to distinguish:

   - public HTTP domains routed through Railway's edge;
   - TCP proxies that publicly expose non-HTTP services;
   - project/environment-isolated private networking through `railway.internal`;
   - application-layer controls that Railway edge TLS does not supply, such as authorization, safe proxy trust, abuse controls, and workload-specific rate limiting.

   Do not assume a service is private because the application also has a private endpoint, or protected because TLS terminates at the edge.

   Re-check Railway's current [networking overview](https://docs.railway.com/networking), [TCP proxy documentation](https://docs.railway.com/networking/tcp-proxy), [private networking documentation](https://docs.railway.com/networking/private-networking), and [public networking specifications](https://docs.railway.com/networking/public-networking/specs-and-limits) during every audit.

4. **Trace local configuration to the boundary.** Check for:

   - databases, Redis, queues, admin consoles, dashboards, or debug servers behind public domains or TCP proxies;
   - services listening on the wrong interface/port or bypassing expected framework security;
   - unauthenticated health/metrics endpoints disclosing internals;
   - permissive CORS, host validation, forwarded-header, or trusted-proxy settings;
   - debug/development mode, verbose errors, default credentials, or management routes in production paths;
   - secrets placed in client-visible variables, build arguments, images, generated static assets, or repository files;
   - cross-service traffic using public endpoints where private networking is intended;
   - mutable images, over-privileged containers, weak health checks, or missing environment separation that magnify exposure.

   A reference to a variable is not its value. Report the variable name and risky use only; never resolve or print a secret.

5. **Validate externally only within the supplied scope.** For a user-supplied public URL, passive browser/header checks may confirm reachability and visible controls. Do not enumerate unrelated subdomains, probe ports, attempt authentication bypass, fuzz endpoints, or connect to databases/caches. A TCP proxy's existence is enough to flag an exposure for owner verification without touching the service.

6. **Classify every conclusion.** Use:

   - **Publicly reachable** — a public domain or TCP proxy is evidenced.
   - **Risky exposure/configuration** — reachability or a weak boundary is unnecessary or insufficiently protected.
   - **Confirmed vulnerability** — a concrete, reproducible failure path is evidenced without intrusive testing.
   - **Verification gap** — provider or runtime evidence required to decide was unavailable.
   - **Evidence of compromise** — concrete indicators support exploitation; never infer it from exposure alone.

7. **Report an exposure matrix.** Include service role, public HTTP, public TCP, private path, authentication, evidence source, state, severity, confidence, smallest useful mitigation, and safe validation. End with explicit provider-side checks the owner should perform for gaps, phrased as narrow presence/status queries rather than secret/configuration dumps.

## Safety Boundary

- This skill is diagnostic and read-only. Do not add/remove domains or TCP proxies, change variables, redeploy services, rotate credentials, or modify firewall/networking settings.
- Never dump Railway variables, environment files, credentials, provider/deployment logs, database URLs, private endpoints, tokens, whole configuration objects, or container inspection output.
- Inspect only an explicit allowlist of non-sensitive fields and report presence, type, or status—not secret values.
- Do not perform port scanning, exploit attempts, authentication bypass, brute force, destructive fuzzing, denial-of-service testing, or database/cache handshakes.
- Do not claim that edge TLS supplies application authorization or a web application firewall. Do not claim compromise from public reachability alone.
