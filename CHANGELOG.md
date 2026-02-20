# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-20

### Added

- Composite GitHub Action enforcing maximum file line counts in CI
- Configurable `max_lines` threshold (default: 400)
- Multiple file selection targets: `new`, `changed`, `all`, `explicit`
- Combinable targets with union semantics
- Include/exclude glob pattern filtering
- Auto-detection of base/head SHAs for `pull_request` and `push` events
- Shallow clone handling with safe fetch attempts
- Clear failure output: `path (LINES > MAX)`
- Outputs: `checked_files` and `offenders`
- CI workflow with pass/fail validation scenarios
- Release drafter automation
- Major tag mover workflow

[1.0.0]: https://github.com/BenGlasser/linecap/releases/tag/v1.0.0
