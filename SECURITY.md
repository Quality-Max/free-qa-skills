# Security Policy

`free-qa-skills` is a catalog of read-only diagnostic **skills** (Markdown instructions) for AI coding assistants such as Claude Code. The skills ship no executable package and pull no dependencies — but because they run inside a developer's environment and influence what an AI agent does, their integrity matters. This policy explains our security model and how to report issues.

## The read-only security contract

Every skill in this repository must be **diagnostic and read-only**. A skill must not:

- run destructive or state-changing commands (no `rm -rf`, `git push`, `git commit`, `git reset --hard`, `sudo`, `chmod 777`, piping remote content into a shell, etc.);
- write, modify, or delete the user's code, files, repositories, or sites (skills find and grade problems — they do not fix them);
- exfiltrate data — no sending repository contents, secrets, or scan results to any network destination. Network access is limited to declared browsing of a user-supplied URL and public authoritative sources required for advisory research, without transmitting private target data;
- echo live secrets in full (secret-handling skills must mask matches);
- dump environment variables, secret/configuration files, credentials, provider or deployment logs, or whole configuration objects — inspect only explicitly allowlisted non-sensitive fields and report presence, type, status, or a fully redacted value;
- run active exploits, brute-force attempts, destructive fuzzing, persistence checks, or denial-of-service tests.

**Test skills.** `mr-null` and `scunthorpe-check` are input-testing skills: in website mode they type test cases into real form fields and submit them, then check the client validation, the server response, and the saved value. That changes the environment on purpose, so run them only against a test or staging environment you confirm. They skip payment, delete, credential-change, and outbound-message forms unless you name them, use only inert test values, list the test data they create, and their repository mode stays read-only. Every other rule above still applies.

Security findings must distinguish a risky configuration, an affected and reachable vulnerability, and evidence of exploitation. Advisory claims and affected/fixed version ranges require a primary vendor or maintainer source; social posts and news reports are discovery leads, not proof.

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
