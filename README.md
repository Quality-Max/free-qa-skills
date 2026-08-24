# Free QA Skills for AI Coding Agents

[![validate-skills](https://github.com/Quality-Max/free-qa-skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/Quality-Max/free-qa-skills/actions/workflows/validate-skills.yml)
[![GitHub Agent Skills](https://img.shields.io/badge/GitHub-Agent%20Skills-181717?logo=github)](https://github.com/Quality-Max/free-qa-skills/releases/latest)
[![skills.sh installs](https://skills.sh/b/quality-max/free-qa-skills)](https://www.skills.sh/quality-max/free-qa-skills)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/qualitymax)

Quick QA, accessibility, performance, security, SEO, privacy, and test-review skills for any website or codebase. No signup or API keys required. The web skills use browser automation such as Playwright MCP; the code-review skills work directly with local repository files and need no MCP at all.

Use these skills when you need a fast audit for Core Web Vitals, WCAG accessibility, broken links, responsive screenshots, console errors, security headers, cookies and trackers, mixed content, dependency risk, leaked secrets, flaky selectors, dead code, API security, IaC misconfigurations, or LLM/agent app risk.

**Directory page:** [skills.sh/quality-max/free-qa-skills](https://www.skills.sh/quality-max/free-qa-skills)

## Install

### GitHub Agent Skills

Install all 27 skills with the GitHub CLI:

```bash
gh skill install Quality-Max/free-qa-skills
```

Install one skill and pin it to the current release:

```bash
gh skill install Quality-Max/free-qa-skills accessibility-check --pin v1.0.0
```

See the [latest GitHub Agent Skills release](https://github.com/Quality-Max/free-qa-skills/releases/latest).

### skills.sh

Install from skills.sh with the official skills CLI. This records the install correctly for the public skills directory.

```bash
# Install all 27 QA skills
npx skills add Quality-Max/free-qa-skills

# Or install one focused skill
npx skills add Quality-Max/free-qa-skills/accessibility-check
npx skills add Quality-Max/free-qa-skills/core-web-vitals
npx skills add Quality-Max/free-qa-skills/diff-risk-review
```

Then use the skill in your coding agent:

```bash
/accessibility-check https://mysite.com
/core-web-vitals https://mysite.com
/diff-risk-review
```

Manual copying still works for local development, but `npx skills add` is the recommended install path because it keeps the skills visible on [skills.sh](https://www.skills.sh/).

## Skills

27 diagnostic skills across five areas. All are read-only — they find problems and grade them, they don't change your code or site.

### Web quality (browser automation)

| Skill | What It Checks | Install |
|-------|---------------|---------|
| **ui-ux-scan** | Touch targets, font consistency, spacing, empty states, visual hierarchy, UX anti-patterns | `npx skills add Quality-Max/free-qa-skills/ui-ux-scan` |
| **accessibility-check** | WCAG violations — alt text, headings, keyboard nav, ARIA, contrast | `npx skills add Quality-Max/free-qa-skills/accessibility-check` |
| **responsive-screenshots** | Screenshot at 5 viewports (mobile → ultrawide), flag layout breaks | `npx skills add Quality-Max/free-qa-skills/responsive-screenshots` |
| **broken-link-scan** | Find 404s, redirect chains, dead links | `npx skills add Quality-Max/free-qa-skills/broken-link-scan` |
| **console-error-scan** | JS errors, failed network requests, deprecation warnings | `npx skills add Quality-Max/free-qa-skills/console-error-scan` |
| **seo-check** | Meta tags, Open Graph, structured data, image alts, heading hierarchy | `npx skills add Quality-Max/free-qa-skills/seo-check` |
| **security-headers-check** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy — graded A–F | `npx skills add Quality-Max/free-qa-skills/security-headers-check` |
| **cookie-privacy-scan** | Cookie inventory, missing Secure/HttpOnly/SameSite, third-party trackers, pre-consent tracking (GDPR) | `npx skills add Quality-Max/free-qa-skills/cookie-privacy-scan` |
| **form-validation-scan** | Required-field enforcement, format validation, error messaging, accepts-bad-input probing | `npx skills add Quality-Max/free-qa-skills/form-validation-scan` |
| **i18n-rtl-audit** | Layout breaks under long translations, RTL rendering, hardcoded strings, missing lang/dir | `npx skills add Quality-Max/free-qa-skills/i18n-rtl-audit` |
| **mixed-content-scan** | HTTP scripts/styles/images/iframes and insecure form actions on HTTPS pages — active vs passive | `npx skills add Quality-Max/free-qa-skills/mixed-content-scan` |

### Performance (browser automation)

| Skill | What It Checks | Install |
|-------|---------------|---------|
| **core-web-vitals** | LCP, CLS, INP, TTFB, FCP via browser perf APIs — graded against Google thresholds | `npx skills add Quality-Max/free-qa-skills/core-web-vitals` |
| **page-weight-budget** | Total bytes, request count, render-blocking JS/CSS, oversized/uncompressed images vs a budget | `npx skills add Quality-Max/free-qa-skills/page-weight-budget` |
| **third-party-bloat** | Third-party scripts (analytics, tags, chat, ads) ranked by transfer size + main-thread cost | `npx skills add Quality-Max/free-qa-skills/third-party-bloat` |
| **cold-load-waterfall** | Cold-cache load profile — TTFB, time-to-interactive, longest-pole requests, text waterfall | `npx skills add Quality-Max/free-qa-skills/cold-load-waterfall` |

### Code review (local repository — no MCP)

| Skill | What It Checks | Install |
|-------|---------------|---------|
| **diff-risk-review** | Reviews `git diff` for correctness/security/performance — severity-ranked with file:line | `npx skills add Quality-Max/free-qa-skills/diff-risk-review` |
| **secret-scan** | Hardcoded API keys, tokens, private keys, connection strings across common providers | `npx skills add Quality-Max/free-qa-skills/secret-scan` |
| **dependency-audit** | Known-vulnerable, unpinned, abandoned, or badly outdated packages | `npx skills add Quality-Max/free-qa-skills/dependency-audit` |
| **dead-code-scan** | Unused exports, unreferenced files, unreachable branches, unused imports | `npx skills add Quality-Max/free-qa-skills/dead-code-scan` |
| **complexity-hotspots** | Long functions, deep nesting, high cyclomatic complexity, god-files — ranked worst-first | `npx skills add Quality-Max/free-qa-skills/complexity-hotspots` |
| **error-handling-audit** | Swallowed exceptions, bare catches, floating promises, missing timeouts/retries | `npx skills add Quality-Max/free-qa-skills/error-handling-audit` |

### Test review (local repository — no MCP)

| Skill | What It Checks | Install |
|-------|---------------|---------|
| **test-quality-review** | Assertion-free tests, weak assertions, skipped/only tests, over-mocking, missing edge cases | `npx skills add Quality-Max/free-qa-skills/test-quality-review` |
| **flaky-selector-scan** | Brittle UI locators (nth-child, absolute XPath, generated classes) → stable role/data-test suggestions | `npx skills add Quality-Max/free-qa-skills/flaky-selector-scan` |

### Security & compliance (local repository — no MCP)

| Skill | What It Checks | Install |
|-------|---------------|---------|
| **agentic-app-risk-review** | LLM/agent apps — prompt injection, unsafe tool calls, excessive agency, PII/secret leakage (OWASP-LLM-style) | `npx skills add Quality-Max/free-qa-skills/agentic-app-risk-review` |
| **iac-misconfig-scan** | Dockerfiles, Compose, Terraform, GitHub Actions — root containers, world-writable files, unpinned actions, hardcoded secrets | `npx skills add Quality-Max/free-qa-skills/iac-misconfig-scan` |
| **api-security-scan** | REST / OpenAPI — missing auth, broken object-level authorization (IDOR/BOLA), no rate limiting, verbose errors | `npx skills add Quality-Max/free-qa-skills/api-security-scan` |
| **license-compliance-scan** | Dependency licenses vs. your project's — copyleft conflicts, AGPL, unknown/unlicensed packages | `npx skills add Quality-Max/free-qa-skills/license-compliance-scan` |

## Requirements

- An AI coding agent supported by the [skills CLI](https://skills.sh/)
- A browser-automation integration such as Playwright MCP — only for the web-quality and performance skills. The repository-review skills need no MCP.

## How It Works

Web skills use the agent's browser-automation integration to navigate your site, run checks in the browser, and produce a graded report. Code-review skills read your repo and `git diff` directly. All are diagnostic only — they find problems, they don't fix them.

## Want More?

These skills find issues. [QualityMax](https://qualitymax.io) fixes them — AI-generated test automation, self-healing scripts, CI/CD quality gates.

Connect your agent to QualityMax MCP for 67 OAuth-protected tools: test generation, AI code review, BOLA scanning, k6 load testing, and breach triage.

Open [QualityMax MCP on Smithery](https://smithery.ai/servers/qualitymax/qualitymax-mcp), connect it to your agent, and complete the hosted OAuth authorization flow. No API token needs to be copied into client configuration.

## Security & contributing

Every skill is **diagnostic and read-only** — it finds and grades problems, it never changes your code or site, and it doesn't exfiltrate data. This read-only contract is enforced in CI by [`scripts/validate-skills.mjs`](scripts/validate-skills.mjs).

- Report a vulnerability: see [SECURITY.md](SECURITY.md).
- Add or improve a skill: see [CONTRIBUTING.md](CONTRIBUTING.md) (run `node scripts/validate-skills.mjs` before opening a PR).
- Be excellent to each other: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Apache 2.0
