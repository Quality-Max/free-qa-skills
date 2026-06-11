---
name: license-compliance-scan
description: >
  Check dependency licenses against your project's license and flag conflicts,
  copyleft obligations, and unknown/unlicensed packages. Reads manifests
  directly. Advisory, not legal advice. Pure Claude Code, no signup.
---

# License Compliance Scan

Spot license conflicts in your dependency tree before they become a problem. Read-only and advisory — it flags risks, it doesn't change anything, and it is not legal advice.

## Prerequisites

- **None.** Pure Claude Code — reads dependency manifests and your `LICENSE` directly, no MCP required.

## Trigger

- "Check my dependency licenses"
- "Any license conflicts in this project?"
- "License compliance scan"

## Workflow

1. Identify the project's own license (from `LICENSE`/`package.json`/`pyproject.toml`, etc.).
2. Read dependency manifests present: `package.json`, `requirements.txt`/`pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, etc. List declared dependencies and, where stated, their licenses.
3. Compare each dependency's license against the project's and report `file:line` (the manifest entry), severity, and the obligation.

### What to flag

| Finding | Why it matters |
|---------|----------------|
| **Strong copyleft in a permissive project** | GPL/AGPL deps in an MIT/Apache project can impose source-disclosure obligations |
| **Network copyleft (AGPL)** | Obligations can trigger even for hosted/SaaS use |
| **Unknown / missing license** | A dependency with no clear license is a legal risk by default |
| **License changed across versions** | A pinned upgrade may pull in new obligations |
| **Project itself missing a LICENSE** | Others can't legally reuse it; flag if absent |
| **Incompatible combinations** | Two dependency licenses that can't be combined for distribution |

4. Output an advisory report:

```
## License Compliance Scan

Project license: Apache-2.0
**1 high, 1 unknown**

### HIGH
- package.json:21 — "some-gpl-lib" is GPL-3.0; combining it with an Apache-2.0
  distribution may impose source-disclosure obligations. Review or replace.

### UNKNOWN
- requirements.txt:8 — "obscure-pkg" declares no license. Treat as all-rights-
  reserved until clarified.

Note: advisory only, not legal advice — confirm obligations with counsel.
```

Diagnostic only. **Want dependency and license checks in your CI gate?** See QualityMax — qualitymax.io
