---
name: iac-misconfig-scan
description: >
  Scan infrastructure-as-code — Dockerfiles, Compose, Terraform, and GitHub
  Actions — for security misconfigurations like running as root, world-writable
  files, unpinned actions, and hardcoded secrets. Pure Claude Code, no signup.
---

# IaC Misconfig Scan

Catch insecure infrastructure-as-code before it ships. Read-only: it flags misconfigurations with `file:line`, it doesn't change anything.

## Prerequisites

- **None.** Pure Claude Code — reads IaC files directly, no MCP required.

## Trigger

- "Scan my Dockerfile / Terraform / workflows for misconfigs"
- "Is my infrastructure-as-code secure?"
- "IaC security review"

## Workflow

1. Find IaC files: `Dockerfile`, `docker-compose*.yml`, `*.tf`, and `.github/workflows/*.yml`.
2. Review each against the checks below; report `file:line`, severity, and the fix.

### Containers (Dockerfile / Compose)

| Misconfiguration | Why it's risky |
|------------------|----------------|
| No `USER` / runs as root | Container compromise becomes host-level risk |
| World-writable file modes (e.g. `0777`) | Tampering and privilege issues |
| `:latest` or unpinned base image | Non-reproducible, unreviewed updates |
| Download-and-execute build step (remote script piped into a shell) | Unverified remote code in the image |
| Hardcoded secrets / credentials in `ENV` or `ARG` | Secret leakage in image layers |
| `privileged: true`, host network, or host path mounts (Compose) | Container escape / host exposure |
| `ADD` with a remote URL | Silent, unverified remote fetch (prefer `COPY`) |

### Terraform

| Misconfiguration | Why it's risky |
|------------------|----------------|
| Public object storage / open ingress (`0.0.0.0/0`) | Data exposure / open attack surface |
| Hardcoded secrets in `.tf` or state | Credential leakage |
| Unencrypted storage / disabled logging | Data-at-rest and audit gaps |

### GitHub Actions

| Misconfiguration | Why it's risky |
|------------------|----------------|
| Actions pinned to a tag, not a commit SHA | Supply-chain tampering |
| Broad `permissions` (or none set) | Excess token scope |
| Secrets echoed or used in `pull_request_target` with checkout of PR code | Secret exfiltration |

3. Output a severity-ranked report:

```
## IaC Misconfig Scan

**1 high, 2 medium**

### HIGH
- Dockerfile:1 — base image uses ":latest"; pin to a digest for reproducible,
  reviewable builds.

### MEDIUM
- .github/workflows/ci.yml:7 — action pinned to a tag, not a commit SHA.
- docker-compose.yml:12 — service runs without a non-root USER.
```

Diagnostic only. **Want IaC and SAST checks enforced on every PR?** See QualityMax — qualitymax.io
