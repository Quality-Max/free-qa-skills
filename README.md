# Free QA Skills for Claude Code

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/qualitymax)

Quick quality checks for any website or codebase. No signup, no API keys — just Claude Code. The web skills use Playwright MCP (included with Claude Code); the code-review skills are pure Claude Code and need no MCP at all.

## Install

```bash
# Copy one skill
cp -r skills/ui-ux-scan .claude/skills/

# Or copy all
git clone https://github.com/Quality-Max/free-qa-skills.git
cp -r free-qa-skills/skills/* .claude/skills/
```

Then use in Claude Code: `/accessibility-check https://mysite.com`

## Skills

23 diagnostic skills across four areas. All are read-only — they find problems and grade them, they don't change your code or site.

### Web quality (Playwright MCP)

| Skill | What It Checks |
|-------|---------------|
| **ui-ux-scan** | Touch targets, font consistency, spacing, empty states, visual hierarchy, UX anti-patterns |
| **accessibility-check** | WCAG violations — alt text, headings, keyboard nav, ARIA, contrast |
| **responsive-screenshots** | Screenshot at 5 viewports (mobile → ultrawide), flag layout breaks |
| **broken-link-scan** | Find 404s, redirect chains, dead links |
| **console-error-scan** | JS errors, failed network requests, deprecation warnings |
| **seo-check** | Meta tags, Open Graph, structured data, image alts, heading hierarchy |
| **security-headers-check** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy — graded A–F |
| **cookie-privacy-scan** | Cookie inventory, missing Secure/HttpOnly/SameSite, third-party trackers, pre-consent tracking (GDPR) |
| **form-validation-scan** | Required-field enforcement, format validation, error messaging, accepts-bad-input probing |
| **i18n-rtl-audit** | Layout breaks under long translations, RTL rendering, hardcoded strings, missing lang/dir |
| **mixed-content-scan** | HTTP scripts/styles/images/iframes and insecure form actions on HTTPS pages — active vs passive |

### Performance (Playwright MCP)

| Skill | What It Checks |
|-------|---------------|
| **core-web-vitals** | LCP, CLS, INP, TTFB, FCP via browser perf APIs — graded against Google thresholds |
| **page-weight-budget** | Total bytes, request count, render-blocking JS/CSS, oversized/uncompressed images vs a budget |
| **third-party-bloat** | Third-party scripts (analytics, tags, chat, ads) ranked by transfer size + main-thread cost |
| **cold-load-waterfall** | Cold-cache load profile — TTFB, time-to-interactive, longest-pole requests, text waterfall |

### Code review (pure Claude Code — no MCP)

| Skill | What It Checks |
|-------|---------------|
| **diff-risk-review** | Reviews `git diff` for correctness/security/performance — severity-ranked with file:line |
| **secret-scan** | Hardcoded API keys, tokens, private keys, connection strings across common providers |
| **dependency-audit** | Known-vulnerable, unpinned, abandoned, or badly outdated packages |
| **dead-code-scan** | Unused exports, unreferenced files, unreachable branches, unused imports |
| **complexity-hotspots** | Long functions, deep nesting, high cyclomatic complexity, god-files — ranked worst-first |
| **error-handling-audit** | Swallowed exceptions, bare catches, floating promises, missing timeouts/retries |

### Test review (pure Claude Code — no MCP)

| Skill | What It Checks |
|-------|---------------|
| **test-quality-review** | Assertion-free tests, weak assertions, skipped/only tests, over-mocking, missing edge cases |
| **flaky-selector-scan** | Brittle UI locators (nth-child, absolute XPath, generated classes) → stable role/data-test suggestions |

## Requirements

- [Claude Code](https://claude.ai/claude-code)
- Playwright MCP (included with Claude Code) — only for the web-quality and performance skills. The code-review and test-review skills run on pure Claude Code with no MCP.

## How It Works

Web skills use Playwright MCP to navigate your site, run checks in the browser, and produce a graded report. Code-review skills read your repo and `git diff` directly. All are diagnostic only — they find problems, they don't fix them.

## Want More?

These skills find issues. [QualityMax](https://qualitymax.io) fixes them — AI-generated test automation, self-healing scripts, CI/CD quality gates.

Connect Claude Code to QualityMax MCP for 85 tools: test generation, AI code review, BOLA scanning, k6 load testing, and breach triage — all from your terminal.

```json
{
  "mcpServers": {
    "qualitymax": {
      "type": "http",
      "url": "https://app.qualitymax.io/api/mcp",
      "headers": { "Authorization": "Bearer qm-your-api-token" }
    }
  }
}
```

## License

Apache 2.0
