"""Filter file paths by include/exclude glob patterns via stdin."""
import sys, os, fnmatch

def parse_patterns(env_key):
    val = os.environ.get(env_key, '').strip()
    if not val:
        return []
    return [p.strip() for p in val.splitlines() if p.strip()]

include = parse_patterns('INPUT_INCLUDE')
exclude = parse_patterns('INPUT_EXCLUDE')

for line in sys.stdin:
    f = line.strip()
    if not f:
        continue
    inc_match = not include or any(fnmatch.fnmatch(f, p) for p in include)
    exc_match = exclude and any(fnmatch.fnmatch(f, p) for p in exclude)
    if inc_match and not exc_match:
        print(f)
