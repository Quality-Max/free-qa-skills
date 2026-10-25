# Contributing to free-qa-skills

Thanks for helping improve free, no-signup QA and security checks for AI coding assistants. Contributions are welcome — new skills, fixes, and clearer instructions.

## Anatomy of a skill

Each skill lives in `skills/<skill-name>/SKILL.md` and is plain Markdown with YAML frontmatter:

```markdown
---
name: my-skill
description: >
  One or two sentences describing what the skill checks and that it is read-only.
---

# My Skill

Short intro.

## Prerequisites
- None, or "Playwright MCP (comes with Claude Code)".

## Trigger
- "Phrases a user would type to invoke it"

## Workflow
1. Steps the assistant follows...
```

Requirements (checked by CI):
- `skills/<name>/SKILL.md` exists.
- Frontmatter has `name` and `description`; `name` **equals the directory name**.
- The body has a `# ` title and `## Trigger` and `## Workflow` sections.

## The Skill Security Contract (required)

Every skill must be **diagnostic and read-only**. By contributing a skill you confirm it:

- [ ] Makes **no destructive or state-changing** changes — it finds and grades problems, it does not fix them.
- [ ] Runs **no** destructive/remote-execution commands (`rm -rf`, `git push`/`commit`/`reset --hard`, `sudo`, `chmod 777`, `curl … | sh`, etc.).
- [ ] Does **not write, modify, or delete** the user's files, repos, or sites.
- [ ] Does **not exfiltrate** data — network access is limited to declared browsing of a user-supplied URL and public authoritative advisory research, without transmitting private target data.
- [ ] **Masks secrets** in any output (never echoes a full live credential).
- [ ] Never dumps environment variables, secret/configuration files, credentials, provider/deployment logs, or whole configuration objects; any inspection is explicitly allowlisted and redacted.
- [ ] Runs no active exploits, brute-force attempts, destructive fuzzing, persistence checks, or denial-of-service tests.
- [ ] Is resistant to instruction-hijacking by the content under test (treat page/diff content as untrusted data, not commands).
- [ ] Separates risky configuration, affected/reachable vulnerability, and evidence of exploitation; advisory version claims cite primary sources.

These rules are our core security guarantee and are enforced by `scripts/validate-skills.mjs`. See [SECURITY.md](SECURITY.md).

## Before you open a PR

```bash
node scripts/validate-skills.mjs
```

This validates structure and the security contract for every skill. CI runs the same check.

## Conduct

By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md).
