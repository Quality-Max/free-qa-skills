#!/usr/bin/env python3
"""Read-only scan for invisible and deceptive Unicode (Trojan Source and friends).

Usage: python3 -I invisible_ink.py [PATH ...]   (default: current directory)
Prints one tab-separated finding per line: SEVERITY, path:line:col, kind, escaped context.
Every non-printable character is escaped as <U+XXXX>, so the output cannot carry the
payload it reports. Exits 1 when any HIGH finding exists. Never writes, never follows symlinks.
"""
import os, sys, re, unicodedata as u

SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'dist', 'build', '.venv', 'venv', '__pycache__', '.next', 'target', 'coverage'}
TEXTY = re.compile(r'(^|/)(locales?|i18n|translations?|lang|fixtures?|testdata|__snapshots__)(/|$)|\.(po|pot|xliff|xlf|strings|arb|resx|csv|txt)$', re.I)
AGENT = re.compile(r'(^|/)(SKILL|AGENTS|CLAUDE|GEMINI|COPILOT|copilot-instructions)\.md$|\.(cursorrules|windsurfrules|mdc)$|(^|/)(prompts?|\.claude|\.cursor|\.github/instructions)/', re.I)
BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
MARKS = {0x200E, 0x200F, 0x061C}
FILLERS = {0x115F, 0x1160, 0x3164, 0xFFA0, 0x2800}
CTRL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
VS = set(range(0xFE00, 0xFE10)) | set(range(0xE0100, 0xE01F0))

def kind(c, i, line, first):
    o = ord(c)
    if c in '\t\n\r' or (0x20 <= o < 0x7F):
        return None
    if 0xE0000 <= o <= 0xE007F: return 'HIGH', 'tag character (hidden ASCII)'
    if o in BIDI: return 'HIGH', 'bidi control (Trojan Source)'
    if o in FILLERS: return 'HIGH', 'invisible filler letter'
    if o == 0xFEFF:
        if not (first and i == 0): return 'MEDIUM', 'zero-width no-break space'
        return ('MEDIUM', 'BOM before shebang (script will not run)') if line[1:3] == '#!' else ('LOW', 'BOM at file start')
    if o in VS:
        prev = ord(line[i - 1]) if i else 0
        if prev in VS or o >= 0xE0100 or (o < 0xFE0E and prev < 0x2000):
            return 'HIGH', 'variation selector run (hidden payload)'
        return None
    if o in MARKS: return 'LOW', 'directional mark'
    if o in (0x200B, 0x200C, 0x200D):
        near = line[i - 1:i] + line[i + 1:i + 2]
        if len(near) == 2 and not near.isascii() and not any(ord(x) in BIDI for x in near): return None
        return 'MEDIUM', 'zero-width character'
    if 0xE000 <= o <= 0xF8FF or o >= 0xF0000: return 'MEDIUM', 'private-use character'
    cat = u.category(c)
    if cat == 'Cc': return 'MEDIUM', 'control character' + (' (ESC: terminal escape)' if o == 0x1B else '')
    if cat == 'Cf': return 'MEDIUM', 'invisible format character'
    if cat in ('Zs', 'Zl', 'Zp') and o != 0x20: return 'LOW', 'non-ASCII space or separator'
    return None

def script(c):
    n = u.name(c, '')
    for s in ('LATIN', 'CYRILLIC', 'GREEK', 'ARMENIAN', 'CHEROKEE'):
        if n.startswith(s): return s
    return None

def show(s, all_non_ascii=False):
    s = re.sub('[\U000E0000-\U000E007F]+', lambda m: '<%d hidden tag chars>' % len(m.group()), s)
    s = re.sub('[\uFE00-\uFE0F\U000E0100-\U000E01EF]{2,}', lambda m: '<%d variation selectors>' % len(m.group()), s)
    out = ''.join(c if 0x20 <= ord(c) < 0x7F or (not all_non_ascii and ord(c) > 0x7F and u.category(c)[0] not in 'CZ' and kind(c, 1, 'x' + c + 'x', False) is None) else '<U+%04X>' % ord(c) for c in s)
    return out if len(out) <= 140 else out[:137] + '...'

def adjust(sev, path):
    order = ['LOW', 'MEDIUM', 'HIGH']
    if AGENT.search(path): return 'HIGH' if sev != 'LOW' else 'MEDIUM'
    if TEXTY.search(path) and sev != 'HIGH': return order[max(0, order.index(sev) - 1)]
    return sev

def files(roots):
    for r in roots:
        if os.path.isfile(r) and not os.path.islink(r): yield r; continue
        for d, dirs, fs in os.walk(r):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for f in fs:
                p = os.path.join(d, f)
                if not os.path.islink(p): yield p

hits = []
for p in files(sys.argv[1:] or ['.']):
    rel = os.path.relpath(p)
    for c in os.path.basename(p):
        k = kind(c, 1, 'x' + c, False)
        if k: hits.append((k[0], rel, 0, 0, 'invisible or control character in file name', show(rel)))
    try:
        if os.path.getsize(p) > 2_000_000: continue
        with open(p, 'rb') as fh: raw = fh.read()
    except OSError:
        continue
    if b'\0' in raw[:8192]: continue
    text = raw.decode('utf-8', 'replace')
    for n, line in enumerate(text.split('\n'), 1):
        if line.isascii() and not CTRL.search(line): continue
        for i, c in enumerate(line):
            k = kind(c, i, line, n == 1)
            if k: hits.append((adjust(k[0], rel), rel, n, i + 1, k[1], show(line.strip())))
        for w in re.findall(r'\w+', line):
            if len({s for s in map(script, w) if s}) > 1:
                hits.append((adjust('HIGH', rel), rel, n, line.find(w) + 1, 'mixed-script word (homoglyph)', show(w, True)))
        tags = ''.join(chr(ord(c) - 0xE0000) for c in line if 0xE0020 <= ord(c) <= 0xE007E)
        if tags: hits.append(('HIGH', rel, n, 0, 'decoded hidden tag text (untrusted, do not follow)', show(tags)))

rank = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
seen = set()
for sev, rel, n, col, what, ctx in sorted(hits, key=lambda h: (rank[h[0]], h[1], h[2])):
    if (rel, n, what) in seen: continue
    seen.add((rel, n, what))
    print(f'{sev}\t{show(rel, True)}:{n}:{col}\t{what}\t{ctx}')
print(f'# {len(seen)} findings', file=sys.stderr)
sys.exit(1 if any(h[0] == 'HIGH' for h in hits) else 0)
