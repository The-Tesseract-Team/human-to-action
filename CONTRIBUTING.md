# Contributing

Contributions that keep the repository small, inspectable, and privacy-preserving are welcome.

## Before changing code

- Open or reference an issue for material behavior changes.
- Keep the plugin manifest, bundled skill, and references at the repository root; do not reintroduce a multi-plugin wrapper.
- Do not add telemetry, network access, prompt logging, or persistence without an explicit proposal and privacy review.
- Do not add an automatic hook or enable implicit skill invocation without an explicit behavior and privacy review.
- Never commit credentials, private prompts, personal data, generated caches, or absolute local paths.

## Validate locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

If prompt-routing semantics change, update the relevant case under `evals/` and test the installed plugin in a new Codex task. State what was verified deterministically and what was observed through model behavior.

## Pull requests

Keep changes focused. Explain the user-visible outcome, privacy and security impact, validation performed, and any limitation that remains. Contributors agree that submitted code is licensed under the repository's MIT License and that their public Git metadata will be visible.
