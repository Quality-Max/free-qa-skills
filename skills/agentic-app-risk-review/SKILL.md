---
name: agentic-app-risk-review
description: >
  Defensive review of an LLM/agent application for OWASP-LLM-style risks —
  prompt injection, unsafe tool calls, excessive agency, and PII/secret
  leakage. Reads your code, flags issues with file:line. Pure Claude Code, no signup.
---

# Agentic App Risk Review

Find the security weaknesses in your own LLM or agent app before users — or attackers — do. Read-only: it flags risks, it doesn't change your code.

## Prerequisites

- **None.** Pure Claude Code — reads your repository directly, no MCP required.

## Trigger

- "Review my agent app for prompt injection"
- "Security review of my LLM integration"
- "Is my chatbot safe against jailbreaks / tool abuse?"

## Workflow

1. Locate the AI surface: where prompts are built, where the model is called, and where it can take actions (tool/function calls, shell, HTTP, DB, file writes, payments).
2. Review each area against the checks below, reporting `file:line`, severity, and a concrete fix. Treat all model input and tool output as untrusted.

### What to flag

| Risk | What to look for |
|------|------------------|
| **Prompt injection** | Untrusted input (user text, web/RAG content, file contents) concatenated into the prompt without delineation or instruction-hardening |
| **Indirect injection** | Fetched pages, emails, or documents fed to the model that can carry instructions the agent then follows |
| **Unsafe tool calls** | Tools that run commands, write files, send money, or call APIs with no allowlist, schema validation, or argument sanitization |
| **Excessive agency** | Destructive/irreversible tools exposed with no human-in-the-loop confirmation |
| **Unbounded loops** | Agent/tool loops with no max-step or cost/timeout limit (DoS / runaway spend) |
| **Output not validated** | Model output used directly in shell, SQL, HTML, or `eval` without checking |
| **PII / secret leakage** | Secrets, keys, or personal data placed into prompts, tool args, or logs/traces |
| **Over-broad system prompt** | Secrets or privileged instructions in the system prompt that injection could exfiltrate |
| **No rate / cost limits** | Per-user or per-session limits absent on model and tool calls |

3. Output a severity-ranked report:

```
## Agentic App Risk Review

**2 high, 1 medium**

### HIGH
- agent/tools.py:40 — shell tool runs model-provided strings with no allowlist
  or validation (command injection via tool abuse). Restrict to a fixed command
  set and validate arguments.
- chat/prompt.py:22 — user message concatenated straight into the system prompt
  (prompt injection). Separate untrusted input from instructions and harden.

### MEDIUM
- agent/loop.py:15 — tool loop has no max-step limit (runaway spend / DoS).
  Add a step and cost ceiling.
```

This review is diagnostic only. **Want continuous adversarial testing of your agent in CI?** See QualityMax — qualitymax.io
