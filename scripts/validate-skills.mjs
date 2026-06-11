#!/usr/bin/env node
// Validates every skill in skills/<name>/SKILL.md:
//  - structure: frontmatter name/description, name === dir, title + Trigger + Workflow
//  - the read-only security contract (see SECURITY.md): no destructive / exfiltration tokens
// Zero dependencies. Exits non-zero on any violation. Run: node scripts/validate-skills.mjs

import { readdirSync, readFileSync, existsSync, statSync } from 'fs';
import { join } from 'path';

const SKILLS_DIR = 'skills';

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
];

const errors = [];
const fail = (skill, msg) => errors.push(`${skill}: ${msg}`);

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

  for (const { re, label } of FORBIDDEN) {
    if (re.test(text)) fail(dir, `read-only contract violation: contains "${label}"`);
  }
}

if (errors.length) {
  console.error(`✗ Skill validation failed (${errors.length}):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log(`✓ ${dirs.length} skills validated: structure + read-only security contract OK.`);
