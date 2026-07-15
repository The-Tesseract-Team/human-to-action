# Changelog

All notable user-visible changes are recorded here.

## 0.1.0 - 2026-07-15

### Added

- HumanToAction as the first Tesseract Agent Extensions plugin.
- Fixed `UserPromptSubmit` context guidance without prompt-dependent output or another model call.
- Destination-aware `refine-agent-prompts` skill for same-task execution, exported prompts, audits, and measured migrations.
- Deterministic hook tests, routing cases, publication validation, CI, privacy documentation, and community policies.

### Limitations

- The command hook currently supports macOS and Linux environments with `/usr/bin/python3`.
- Semantic agent behavior remains model-dependent and cannot be guaranteed by deterministic tests.
