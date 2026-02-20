# LineCap

**Enforce maximum file line counts in CI.**

LineCap is a GitHub Action that checks files against a configurable line limit and fails your build when any file exceeds it. Keep your codebase manageable by catching oversized files before they merge.

## Quickstart

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0

- uses: BenGlasser/linecap@v1
```

That's it. By default, LineCap checks **newly added files** against a **400-line limit**.

## Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `max_lines` | Maximum lines allowed per file | `400` |
| `targets` | Comma-separated: `new`, `changed`, `all`, `explicit` | `new` |
| `explicit_files` | Newline-separated file paths (required when targets includes `explicit`) | |
| `include` | Newline-separated glob patterns to include | *(all files)* |
| `exclude` | Newline-separated glob patterns to exclude | |
| `diff_base` | Base ref/SHA for diff | *(auto-detected)* |
| `diff_head` | Head ref/SHA for diff | *(auto-detected)* |
| `fail_on_no_git` | Fail if git history is unavailable | `true` |

### Targets

| Target | Description |
|--------|-------------|
| `new` | Files added in the diff (PR or push) |
| `changed` | Files added, modified, renamed, or copied in the diff |
| `all` | All tracked files in the repository |
| `explicit` | Files listed in `explicit_files` input |

Targets are **combinable** — the file set is the **union** of all selected targets. After computing the union, `include` globs filter first, then `exclude` globs remove matches.

## Outputs

| Output | Description |
|--------|-------------|
| `checked_files` | Newline-separated list of files that were checked |
| `offenders` | Newline-separated list of files exceeding the limit |

## Examples

### Check newly added files (default)

```yaml
- uses: BenGlasser/linecap@v1
```

### Check new files + specific files

```yaml
- uses: BenGlasser/linecap@v1
  with:
    targets: new,explicit
    explicit_files: |
      src/legacy/big-module.ts
      src/legacy/old-controller.ts
```

### Check all tracked files with include/exclude

```yaml
- uses: BenGlasser/linecap@v1
  with:
    max_lines: '300'
    targets: all
    include: |
      src/**/*.ts
      src/**/*.tsx
    exclude: |
      src/**/*.test.ts
      src/**/*.generated.ts
```

### Check changed files in a PR

```yaml
- uses: BenGlasser/linecap@v1
  with:
    targets: changed
    max_lines: '500'
```

### Print offenders on failure

```yaml
- uses: BenGlasser/linecap@v1
  id: linecap
  continue-on-error: true

- if: steps.linecap.outputs.offenders != ''
  run: |
    echo "These files are too long:"
    echo "${{ steps.linecap.outputs.offenders }}"
```

### Full workflow example

```yaml
name: Lint
on:
  pull_request:
  push:
    branches: [main]

jobs:
  linecap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: BenGlasser/linecap@v1
        with:
          max_lines: '400'
          targets: changed
```

## Troubleshooting

### "Cannot resolve base commit"

LineCap needs git history to compute diffs for `new` and `changed` targets. Make sure you use `fetch-depth: 0` in your checkout step:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

### Shallow clones

If you can't use `fetch-depth: 0`, LineCap will attempt to fetch the required commits automatically. If that fails and `fail_on_no_git` is `true` (default), the action will error. Set `fail_on_no_git: false` to skip diff-based targets when history is unavailable:

```yaml
- uses: BenGlasser/linecap@v1
  with:
    fail_on_no_git: 'false'
    targets: all
```

### Base/head missing

For `pull_request` events, base and head are read from the event payload. For `push` events, base is `event.before` and head is `GITHUB_SHA`. You can override both:

```yaml
- uses: BenGlasser/linecap@v1
  with:
    diff_base: ${{ github.event.pull_request.base.sha }}
    diff_head: ${{ github.event.pull_request.head.sha }}
```

### Permissions

LineCap only needs read access to the repository contents. The default `GITHUB_TOKEN` permissions are sufficient. No additional permissions are required.

### No files checked

If LineCap reports 0 files checked:
- Verify your `targets` setting matches your use case
- Check that `include`/`exclude` patterns aren't filtering out all files
- For `new`/`changed` targets, ensure there are actual file changes in the diff
- For `explicit` targets, verify the file paths exist in the repository

## License

[MIT](LICENSE)
