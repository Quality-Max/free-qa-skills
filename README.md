# Free QA Skills for Claude Code

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/qualitymax)

Quick quality checks for any website. No signup, no API keys — just Claude Code + Playwright MCP.

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

| Skill | What It Checks |
|-------|---------------|
| **ui-ux-scan** | Touch targets, font consistency, spacing, empty states, visual hierarchy, UX anti-patterns |
| **accessibility-check** | WCAG violations — alt text, headings, keyboard nav, ARIA, contrast |
| **responsive-screenshots** | Screenshot at 5 viewports (mobile → ultrawide), flag layout breaks |
| **broken-link-scan** | Find 404s, redirect chains, dead links |
| **console-error-scan** | JS errors, failed network requests, deprecation warnings |
| **seo-check** | Meta tags, Open Graph, structured data, image alts, heading hierarchy |
| **security-headers-check** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy — graded A–F |

## Requirements

- [Claude Code](https://claude.ai/claude-code)
- Playwright MCP (included with Claude Code)

## How It Works

Each skill uses Playwright MCP to navigate your site, run checks in the browser, and produce a graded report. Diagnostic only — finds problems, doesn't fix them.

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
