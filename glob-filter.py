"""Filter file paths by include/exclude glob patterns via stdin."""
import sys, os, fnmatch

def parse_patterns(env_key):
    val = os.environ.get(env_key, '').strip()
    if not val:
        return []
    return [p.strip() for p in val.splitlines() if p.strip()]

include = parse_patterns('INPUT_INCLUDE')
exclude = parse_patterns('INPUT_EXCLUDE')

print(f"[linecap-filter] python={sys.version_info[:2]} include={include} exclude={exclude}", file=sys.stderr)

lines = list(sys.stdin)
print(f"[linecap-filter] stdin_lines={len(lines)}", file=sys.stderr)

for line in lines:
    f = line.strip()
    if not f:
        continue
    inc_match = not include or any(fnmatch.fnmatch(f, p) for p in include)
    exc_match = exclude and any(fnmatch.fnmatch(f, p) for p in exclude)
    if f.startswith('test/'):
        print(f"[linecap-filter] {f}: inc={inc_match} exc={exc_match}", file=sys.stderr)
    if inc_match and not exc_match:
        print(f)
