# Security Policy

`free-qa-skills` is a catalog of read-only diagnostic **skills** (Markdown instructions) for AI coding assistants such as Claude Code. The skills ship no executable package and pull no dependencies — but because they run inside a developer's environment and influence what an AI agent does, their integrity matters. This policy explains our security model and how to report issues.

## The read-only security contract

Every skill in this repository must be **diagnostic and read-only**. A skill must not:

- run destructive or state-changing commands (no `rm -rf`, `git push`, `git commit`, `git reset --hard`, `sudo`, `chmod 777`, piping remote content into a shell, etc.);
- write, modify, or delete the user's code, files, repositories, or sites (skills find and grade problems — they do not fix them);
- exfiltrate data — no sending repository contents, secrets, or scan results to any network destination beyond the explicitly declared Playwright MCP browsing of a user-supplied URL;
- echo live secrets in full (secret-handling skills must mask matches).

This contract is **enforced in CI** by `scripts/validate-skills.mjs` (see [CONTRIBUTING.md](CONTRIBUTING.md)). A change that violates it is a security defect.

## What we consider a vulnerability

- A skill that could cause data loss, unwanted writes, or execution of destructive/remote commands.
- A skill that could exfiltrate code, secrets, or results.
- A secret-handling skill that prints unmasked credentials.
- Instructions that can be hijacked by malicious content in the target under test (e.g., a page or diff that injects commands the agent then follows) to escape the read-only contract.

## Reporting a vulnerability

Please report privately — do **not** open a public issue for a security problem.

- Preferred: GitHub **Security Advisories** → "Report a vulnerability" on this repository.
- Or email **contact@qualitymax.io** with `SECURITY: free-qa-skills` in the subject.

Include the affected skill, the impact, and steps to reproduce. We aim to acknowledge within **5 business days** and to agree on a disclosure timeline with you. We credit reporters who wish to be named.

## Supported versions

Skills are rolling; the latest commit on the default branch is the supported version. Fixes ship to the default branch.
