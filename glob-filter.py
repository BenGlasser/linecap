"""Filter file paths by include/exclude glob patterns via stdin."""
import sys, re, os

def glob_to_regex(pattern):
    i, parts = 0, []
    while i < len(pattern):
        c = pattern[i]
        if c == '*' and i + 1 < len(pattern) and pattern[i + 1] == '*':
            if i + 2 < len(pattern) and pattern[i + 2] == '/':
                parts.append('(.*/)?')
                i += 3
            else:
                parts.append('.*')
                i += 2
        elif c == '*':
            parts.append('[^/]*')
            i += 1
        elif c == '?':
            parts.append('[^/]')
            i += 1
        elif c in r'.+^${}()|\\[]':
            parts.append('\\' + c)
            i += 1
        else:
            parts.append(c)
            i += 1
    return re.compile('^' + ''.join(parts) + '$')

def parse_patterns(env_key):
    val = os.environ.get(env_key, '').strip()
    if not val:
        return []
    return [glob_to_regex(p.strip()) for p in val.splitlines() if p.strip()]

include = parse_patterns('INPUT_INCLUDE')
exclude = parse_patterns('INPUT_EXCLUDE')

for line in sys.stdin:
    f = line.strip()
    if not f:
        continue
    if include and not any(r.match(f) for r in include):
        continue
    if exclude and any(r.match(f) for r in exclude):
        continue
    print(f)
