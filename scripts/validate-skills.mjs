#!/usr/bin/env node
// Validates every skill in skills/<name>/SKILL.md:
//  - structure: frontmatter name/description, name === dir, title + Trigger + Workflow
//  - the read-only security contract (see SECURITY.md): no destructive, mutating,
//    active-testing, secret-dumping, or unfiltered-log commands in RUNNABLE shell
//    code-blocks (```bash|sh|shell|zsh|console). Detection skills may name these
//    patterns in prose/tables — only commands the agent would actually run are checked.
// Zero dependencies. Exits non-zero on any violation. Run: node scripts/validate-skills.mjs

import { readdirSync, readFileSync, existsSync, statSync } from 'fs';
import { join } from 'path';

const SKILLS_DIR = 'skills';
const CATALOG_PATH = 'skills.sh.json';

// Match an invoked shell command, including a command after a pipeline, separator,
// or command substitution. This avoids flagging a harmless search for the same text.
const commandPattern = (source, flags = 'm') =>
  new RegExp(String.raw`(?:^|[;&|]\s*|\$\()\s*(?:command\s+)?(?:${source})`, flags);

// Tokens that must never appear in a read-only diagnostic skill.
const FORBIDDEN = [
  { re: /\brm\s+-rf\b/, label: 'rm -rf' },
  { re: /\bgit\s+push\b/, label: 'git push' },
  { re: /\bgit\s+commit\b/, label: 'git commit' },
  { re: /\bgit\s+reset\s+--hard\b/, label: 'git reset --hard' },
  { re: /\bsudo\s+/, label: 'sudo' },
  { re: /\bchmod\s+777\b/, label: 'chmod 777' },
  { re: /\bcurl\b[^\n|]*\|\s*(sh|bash)\b/, label: 'curl | sh' },
  { re: /\bwget\b[^\n|]*\|\s*(sh|bash)\b/, label: 'wget | sh' },
  { re: commandPattern(String.raw`(?:env|printenv)\b`), label: 'raw environment dump' },
  { re: commandPattern(String.raw`set\s*(?:$|\n)`), label: 'raw shell state dump' },
  { re: commandPattern(String.raw`(?:cat|head|tail|less|more)\b[^\n]*\.env\b`), label: 'secret file dump' },
  { re: commandPattern(String.raw`railway\s+variables\b`), label: 'Railway variable dump' },
  { re: commandPattern(String.raw`docker\s+inspect\b(?![^\n]*(?:--format(?:=|\s)|-f(?:=|\s)))|(?:docker\s+logs|kubectl\s+logs|railway\s+logs)\b`), label: 'unfiltered provider/container output' },
  { re: commandPattern(String.raw`gcloud\s+secrets\s+versions\s+access\b`), label: 'secret value access' },
  { re: commandPattern(String.raw`kubectl\s+get\s+secrets?\b`), label: 'cluster secret dump' },
  { re: commandPattern(String.raw`(?:heroku|vercel|fly)\s+logs\b|gcloud\s+logging\s+read\b`), label: 'unfiltered provider logs' },
  { re: commandPattern(String.raw`git\s+(?:add|checkout|switch|restore|clean)\b`), label: 'git state change' },
  { re: commandPattern(String.raw`(?:cp|mv|touch|mkdir|truncate|tee)\b`), label: 'filesystem write' },
  { re: commandPattern(String.raw`sed\s+(?:-[A-Za-z]*i[A-Za-z]*\b|--in-place\b)`), label: 'in-place file edit' },
  { re: commandPattern(String.raw`(?:(?:python3?\s+-m\s+)?pip3?|npm|pnpm|yarn|brew|apt|apt-get|dnf|yum)\s+(?:install|add)\b`), label: 'package installation' },
  { re: commandPattern(String.raw`(?:systemctl|service)\s+(?:start|stop|restart|enable|disable)\b`), label: 'service state change' },
  { re: commandPattern(String.raw`curl\b[^\n]*\s(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE)\b`, 'mi'), label: 'state-changing HTTP request' },
  { re: commandPattern(String.raw`(?:sqlmap|msfconsole|hydra|nikto|ffuf|gobuster|wpscan|nuclei)\b`), label: 'active security testing tool' },
  { re: /\s(\d*>>?|&>)\s*\S/, label: 'shell output redirection' },
];

const errors = [];
const fail = (skill, msg) => errors.push(`${skill}: ${msg}`);

// Keep representative guardrails executable so a future regex edit cannot silently
// remove the protections that CI claims to enforce.
const guardrailCases = [
  { command: 'printenv', forbidden: true },
  { command: 'cat ".env.production"', forbidden: true },
  { command: 'docker inspect app', forbidden: true },
  { command: 'docker inspect --format "{{.State.Status}}" app', forbidden: false },
  { command: 'curl --request DELETE https://example.test/item', forbidden: true },
  { command: 'echo result > report.txt', forbidden: true },
  { command: 'git diff --check', forbidden: false },
  { command: 'rg "npm install" .', forbidden: false },
  { command: 'rg "nuclei" skills', forbidden: false },
];

for (const { command, forbidden } of guardrailCases) {
  const matched = FORBIDDEN.some(({ re }) => re.test(command));
  if (matched !== forbidden) fail('validator', `guardrail self-test failed for: ${command}`);
}

// Returns the command lines inside runnable shell fences (```bash|sh|shell|zsh|console),
// skipping blank lines and comments. Detection patterns in prose/tables are ignored.
function shellCommandLines(text) {
  const out = [];
  const fence = /```(bash|sh|shell|zsh|console)\r?\n([\s\S]*?)```/g;
  let m;
  while ((m = fence.exec(text))) {
    const body = m[2].replace(/\\\r?\n/g, ' ');
    for (const raw of body.split('\n')) {
      const line = raw.trim();
      if (!line || line.startsWith('#')) continue;
      out.push(line);
    }
  }
  return out.join('\n');
}

function parseFrontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const block = m[1];
  const out = {};
  // minimal YAML: top-level "key:" or "key: value" (value may continue on folded lines)
  const nameM = block.match(/^name:\s*(.+)$/m);
  const descM = block.match(/^description:\s*([\s\S]*?)(?=^\w+:|\s*$)/m);
  if (nameM) out.name = nameM[1].trim();
  if (descM) out.description = descM[1].trim();
  return out;
}

if (!existsSync(SKILLS_DIR)) {
  console.error(`No ${SKILLS_DIR}/ directory found.`);
  process.exit(1);
}

const dirs = readdirSync(SKILLS_DIR).filter((d) => {
  try { return statSync(join(SKILLS_DIR, d)).isDirectory(); } catch { return false; }
});

if (dirs.length === 0) fail(SKILLS_DIR, 'no skill directories found');

if (!existsSync(CATALOG_PATH)) {
  fail(CATALOG_PATH, 'missing skills.sh catalog');
} else {
  try {
    const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
    const listed = (catalog.groupings ?? []).flatMap((group) => group.skills ?? []);
    const duplicates = listed.filter((name, index) => listed.indexOf(name) !== index);
    for (const name of new Set(duplicates)) fail(CATALOG_PATH, `duplicate skill "${name}"`);
    for (const name of listed) {
      if (!dirs.includes(name)) fail(CATALOG_PATH, `unknown skill "${name}"`);
    }
    for (const dir of dirs) {
      if (!listed.includes(dir)) fail(CATALOG_PATH, `skill "${dir}" is not grouped`);
    }
  } catch (error) {
    fail(CATALOG_PATH, `invalid catalog: ${error.message}`);
  }
}

for (const dir of dirs) {
  const skillPath = join(SKILLS_DIR, dir, 'SKILL.md');
  if (!existsSync(skillPath)) { fail(dir, 'missing SKILL.md'); continue; }
  const text = readFileSync(skillPath, 'utf8');

  const fm = parseFrontmatter(text);
  if (!fm) { fail(dir, 'missing or malformed YAML frontmatter'); }
  else {
    if (!fm.name) fail(dir, 'frontmatter missing "name"');
    else if (fm.name !== dir) fail(dir, `frontmatter name "${fm.name}" != directory "${dir}"`);
    if (!fm.description) fail(dir, 'frontmatter missing "description"');
  }

  if (!/^#\s+\S/m.test(text)) fail(dir, 'missing a "# " title');
  if (!/^##\s+Trigger\b/m.test(text)) fail(dir, 'missing "## Trigger" section');
  if (!/^##\s+Workflow\b/m.test(text)) fail(dir, 'missing "## Workflow" section');

  const runnable = shellCommandLines(text);
  for (const { re, label } of FORBIDDEN) {
    if (re.test(runnable)) fail(dir, `read-only contract violation: runnable command contains "${label}"`);
  }
}

if (errors.length) {
  console.error(`✗ Skill validation failed (${errors.length}):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(`✓ ${dirs.length} skills validated: structure + catalog + read-only security contract OK.`);
