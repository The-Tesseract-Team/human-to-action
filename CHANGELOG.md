# Changelog

All notable user-visible changes are recorded here.

## Unreleased

### Added

- Added a high-resolution README walkthrough showing explicit same-task refinement and new-task handoff behavior.

## 0.2.0 - 2026-07-15

### Changed

- Renamed the public repository to `human-to-action`.
- Moved the plugin manifest and bundled skill to the repository root.
- Replaced the Agent Extensions marketplace identity with `tesseract-team`.
- Removed the automatic `UserPromptSubmit` hook and its Python runtime.
- Disabled implicit skill invocation; HumanToAction now runs only through explicit selection or `$human-to-action:refine-agent-prompts`.
- Made explicit `new task`, `new thread`, `new workspace`, and `handoff` requests return paste-ready handoffs.

## 0.1.0 - 2026-07-15

### Added

- HumanToAction as an independent Codex plugin.
- Fixed `UserPromptSubmit` context guidance without prompt-dependent output or another model call. This behavior was removed in `0.2.0` in favor of explicit invocation.
- Destination-aware `refine-agent-prompts` skill for same-task execution, exported prompts, audits, and measured migrations.
- Deterministic hook tests, routing cases, publication validation, CI, privacy documentation, and community policies. Hook tests were removed with the hook in `0.2.0`.

### Limitations

- Semantic agent behavior remains model-dependent and cannot be guaranteed by deterministic tests.
