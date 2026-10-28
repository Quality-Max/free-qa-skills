#!/usr/bin/env python3
"""Read-only scan for invisible and deceptive Unicode (Trojan Source and friends).

Usage: python3 -I invisible_ink.py [PATH ...]   (default: current directory)
Prints one tab-separated finding per line: SEVERITY, path:line:col, kind, context.
Context is a short window around the hit with every invisible, control, and combining
character escaped as <U+XXXX> and secret-looking values redacted, so the output carries
neither the payload nor a credential. Sensitive files (.env, keys, credentials) get no
context at all. Exits 1 when any HIGH finding exists. Never writes, never follows symlinks.
"""
import os, sys, re, unicodedata as u

SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'dist', 'build', '.venv', 'venv', '__pycache__', '.next', 'target', 'coverage'}
TEXTY = re.compile(r'(^|/)(locales?|i18n|translations?|lang|fixtures?|testdata|__snapshots__)(/|$)|\.(po|pot|xliff|xlf|strings|arb|resx|csv|txt)$', re.I)
AGENT = re.compile(r'(^|/)(SKILL|AGENTS|CLAUDE|GEMINI|COPILOT|copilot-instructions)\.md$|\.(cursorrules|windsurfrules|mdc)$|(^|/)(prompts?|\.claude|\.cursor|\.github/instructions)/', re.I)
SENSITIVE = re.compile(r'(^|/)(\.env[^/]*|\.npmrc|\.pypirc|\.netrc|\.git-credentials|\.htpasswd|credentials[^/]*|secrets?\.[^/]+|id_(rsa|dsa|ecdsa|ed25519)[^/]*)$|\.(pem|key|p12|pfx|jks|keystore|kdbx|tfvars|tfstate)$', re.I)
SECRET_VALUES = [
    (re.compile(r'(?i)((?:pass(?:word|wd)?|secret|token|api[_-]?key|auth|credential|private[_-]?key|access[_-]?key|bearer)[\w.-]*["\']?\s*[:=]\s*)\S+'), r'\1<redacted>'),
    (re.compile(r'://[^/\s:@]+:[^/\s@]+@'), '://<redacted>@'),
    (re.compile(r'AKIA[0-9A-Z]{16}|(?<![\w+/-])(?=[\w+/-]*\d)(?=[\w+/-]*[A-Za-z])[\w+/-]{24,}={0,2}'), '<redacted>'),
]

BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
MARKS = {0x200E, 0x200F, 0x061C}
FILLERS = {0x115F, 0x1160, 0x3164, 0xFFA0, 0x2800}
JOINERS = {0x200C, 0x200D, 0x034F} | set(range(0x180B, 0x1810))
VS = set(range(0xFE00, 0xFE10)) | set(range(0xE0100, 0xE01F0))
IGNORABLE = ({0x00AD, 0x034F, 0x061C, 0x115F, 0x1160, 0x17B4, 0x17B5, 0x3164, 0xFEFF, 0xFFA0}
             | set(range(0x180B, 0x1810)) | set(range(0x200B, 0x2010)) | BIDI | set(range(0x2060, 0x2070))
             | VS | set(range(0xFFF0, 0xFFF9)) | set(range(0x1BCA0, 0x1BCA4)) | set(range(0x1D173, 0x1D17B)))
CTRL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

def emoji(o):
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or 0x2B00 <= o <= 0x2BFF or o == 0xFE0F

def non_latin_letter(c):
    return u.category(c)[0] in 'LM' and not c.isascii() and not u.name(c, '').startswith('LATIN')

def kind(c, i, line, first):
    o = ord(c)
    if c in '\t\n\r' or (0x20 <= o < 0x7F):
        return None
    prev = line[i - 1] if i else ''
    nxt = line[i + 1] if i + 1 < len(line) else ''
    if 0xE0000 <= o <= 0xE007F: return 'HIGH', 'tag character (hidden ASCII)'
    if o in BIDI: return 'HIGH', 'bidi control (Trojan Source)'
    if o in FILLERS: return 'HIGH', 'invisible filler letter'
    if o == 0xFEFF:
        if not (first and i == 0): return 'MEDIUM', 'zero-width no-break space'
        return ('MEDIUM', 'BOM before shebang (script will not run)') if line[1:3] == '#!' else ('LOW', 'BOM at file start')
    if o in VS:
        p = ord(prev) if prev else 0
        if p in VS: return 'HIGH', 'variation selector run (hidden payload)'
        if o >= 0xE0100:  # ideographic variation sequence: one selector after a CJK ideograph
            return None if u.name(prev, '').startswith('CJK') else ('HIGH', 'variation selector run (hidden payload)')
        if o < 0xFE0E and p < 0x2000: return 'HIGH', 'variation selector run (hidden payload)'
        return None
    if o in MARKS: return 'LOW', 'directional mark'
    if o == 0x200B: return 'MEDIUM', 'zero-width space'
    if o in JOINERS:
        if o == 0x200D and prev and nxt and emoji(ord(prev)) and emoji(ord(nxt)): return None
        if prev and nxt and non_latin_letter(prev) and non_latin_letter(nxt): return None
        return 'MEDIUM', 'zero-width joiner or invisible mark'
    if 0xE000 <= o <= 0xF8FF or o >= 0xF0000: return 'MEDIUM', 'private-use character'
    cat = u.category(c)
    if cat == 'Cc': return 'MEDIUM', 'control character' + (' (ESC: terminal escape)' if o == 0x1B else '')
    if cat == 'Cf' or o in IGNORABLE: return 'MEDIUM', 'invisible format character'
    if cat in ('Zs', 'Zl', 'Zp') and o != 0x20: return 'LOW', 'non-ASCII space or separator'
    return None

def script(c):
    n = u.name(c, '')
    for s in ('LATIN', 'CYRILLIC', 'GREEK', 'ARMENIAN', 'CHEROKEE'):
        if n.startswith(s): return s
    return None

def safe_char(c, all_non_ascii):
    o = ord(c)
    if 0x20 <= o < 0x7F: return True
    if all_non_ascii or o < 0xA0 or o in IGNORABLE or 0xE0000 <= o <= 0xE0FFF: return False
    return u.category(c)[0] not in 'CZM'

RUNS = re.compile('([\U000E0000-\U000E007F]+)|([\uFE00-\uFE0F\U000E0100-\U000E01EF]{2,})')

def show(s, all_non_ascii=False):
    """Redact secret-looking values, then escape everything that is not plainly visible."""
    for pattern, repl in SECRET_VALUES:
        s = pattern.sub(repl, s)
    esc = lambda t: ''.join(c if safe_char(c, all_non_ascii) else '<U+%04X>' % ord(c) for c in t)
    out, pos = [], 0
    for m in RUNS.finditer(s):
        out += [esc(s[pos:m.start()]), '<%d %s>' % (len(m.group()), 'hidden tag chars' if m.group(1) else 'variation selectors')]
        pos = m.end()
    out = ''.join(out) + esc(s[pos:])
    return out if len(out) <= 140 else out[:137] + '...'

def window(line, i, width=40):
    lo, hi = max(0, i - width), min(len(line), i + width)
    return ('...' if lo else '') + line[lo:hi].strip() + ('...' if hi < len(line) else '')

def adjust(sev, what, path):
    if AGENT.search(path):
        return 'MEDIUM' if what in ('BOM at file start', 'non-ASCII space or separator') else 'HIGH'
    if TEXTY.search(path):
        return {'HIGH': 'MEDIUM', 'MEDIUM': 'LOW', 'LOW': 'LOW'}[sev]
    return sev

def files(roots):
    for r in roots:
        if os.path.islink(r):
            print(f'# skipped symlink root: {show(r, True)}', file=sys.stderr); continue
        if os.path.isfile(r): yield r; continue
        for d, dirs, fs in os.walk(r):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not os.path.islink(os.path.join(d, x))]
            for f in fs:
                p = os.path.join(d, f)
                if not os.path.islink(p): yield p

hits = []
def add(sev, what, rel, n, col, ctx):
    hits.append((adjust(sev, what, rel), rel, n, col, what, ctx))

for p in files(sys.argv[1:] or ['.']):
    rel = os.path.relpath(p)
    hidden = SENSITIVE.search(rel)
    name = os.path.basename(p)
    for j, c in enumerate(name):
        k = kind(c, j, name, False)
        if k:
            add(k[0], 'invisible or control character in file name', rel, 0, 0, show(rel, True)); break
    try:
        if os.path.getsize(p) > 2_000_000: continue
        with open(p, 'rb') as fh: raw = fh.read()
    except OSError:
        continue
    if b'\0' in raw[:8192]: continue
    text = raw.decode('utf-8', 'replace')
    for n, line in enumerate(text.split('\n'), 1):
        if line.isascii() and not CTRL.search(line): continue
        seen = set()
        for i, c in enumerate(line):
            k = kind(c, i, line, n == 1)
            if k and k[1] not in seen:
                seen.add(k[1])
                add(k[0], k[1], rel, n, i + 1, '(context withheld: sensitive file)' if hidden else show(window(line, i)))
        for m in re.finditer(r'\w+', line):
            if len({s for s in map(script, m.group()) if s}) > 1:
                add('HIGH', 'mixed-script word (homoglyph)', rel, n, m.start() + 1,
                    '(context withheld: sensitive file)' if hidden else show(m.group(), True))
                break
        tags = ''.join(chr(ord(c) - 0xE0000) for c in line if 0xE0020 <= ord(c) <= 0xE007E)
        if tags:
            add('HIGH', 'decoded hidden tag text (untrusted, do not follow)', rel, n, 0,
                '(context withheld: sensitive file)' if hidden else show(tags))

rank = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
for sev, rel, n, col, what, ctx in sorted(hits, key=lambda h: (rank[h[0]], h[1], h[2], h[3])):
    print(f'{sev}\t{show(rel, True)}:{n}:{col}\t{what}\t{ctx}')
print(f'# {len(hits)} findings', file=sys.stderr)
sys.exit(1 if any(h[0] == 'HIGH' for h in hits) else 0)
