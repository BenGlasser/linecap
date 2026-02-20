# Contributing to LineCap

Thanks for your interest in contributing to LineCap!

## Development

1. Fork the repo and clone it locally
2. Make your changes in a feature branch
3. Test your changes against the fixture files in `test/fixtures/`
4. Open a pull request with a clear description

### PR Labels

Use these labels on your PRs for automatic release note categorization:

| Label | Category |
|-------|----------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `chore` | Maintenance |
| `refactor` | Code refactoring |
| `test` | Tests |
| `ci` | CI/CD changes |

## Testing Locally

You can test the core logic locally using bash:

```bash
# Check a single file
wc -l path/to/file.txt

# Simulate the action's file discovery
git diff --name-only --diff-filter=A origin/main..HEAD
```

The CI workflow runs two scenarios against test fixtures:
- **Pass scenario**: Files under the line limit
- **Fail scenario**: Files over the line limit (expected failure)

## Releasing

### Creating a Release

1. **Tag the release:**

   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **Create a GitHub Release:**
   - Go to [Releases](https://github.com/BenGlasser/linecap/releases)
   - Click "Draft a new release" (or use the draft from release-drafter)
   - Select the tag you just pushed
   - Review and publish

3. **Move the major tag** using one of these methods:

   **Option A: Manual CLI**

   ```bash
   git tag -fa v1 -m "Move v1 to v1.0.0"
   git push origin v1 --force
   ```

   **Option B: GitHub Workflow**

   - Go to [Actions > Move Major Tag](https://github.com/BenGlasser/linecap/actions/workflows/move-major-tag.yml)
   - Click "Run workflow"
   - Enter the version tag (e.g., `v1.0.0`)
   - The workflow will verify the tag exists and move `v1` to that commit

### Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes to action inputs/outputs/behavior
- **MINOR**: New features, new inputs (backwards compatible)
- **PATCH**: Bug fixes, documentation

Consumers reference `BenGlasser/linecap@v1` which always points to the latest `v1.x.x` release.

## Code of Conduct

Be kind. Be constructive. We're all here to make better tools.
