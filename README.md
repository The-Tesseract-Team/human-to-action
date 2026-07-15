# Tesseract Agent Extensions

A non-commercial collection of open-source agent skills and plugins maintained as personal developer and hobby projects.

This is an independent community project. It is not affiliated with, endorsed by, or an official product of OpenAI.

## Catalog

### HumanToAction

**Human intent in. Agent-ready action out.**

HumanToAction helps an agent preserve the user's actual context and choose the right destination for prompt refinement:

- Same task: refine the instruction internally, disclose that once, and continue the work.
- Another agent, new task, handoff, or reusable artifact: return a paste-ready prompt.
- Prompt audit: report consequential findings without silently rewriting the prompt.
- Ordinary work: stay out of the way of the relevant domain workflow.

The automatic `UserPromptSubmit` hook emits the same fixed context on every turn. It does not dynamically inspect or rewrite the submitted prompt, and it does not make another model call. The bundled `human-to-action:refine-agent-prompts` skill supplies the semantic refinement workflow when relevant.

## Install

HumanToAction currently supports macOS and Linux environments that provide `/usr/bin/python3`. Windows is not supported in version 0.1.0.

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add The-Tesseract-Team/agent-extensions --ref main
```

Then install the plugin:

```bash
codex plugin add human-to-action@tesseract-agent-extensions
```

Review the `UserPromptSubmit` command hook when Codex asks for trust. Do not bypass that review. Restart the ChatGPT desktop app and begin a new task so newly installed skills and hooks are discovered.

## Use

You do not need a trigger phrase for ordinary automatic context guidance. Ask for prompt refinement only when that is what you want.

Same-task refinement:

```text
Refine this instruction internally and continue: make the border match the attached reference.
```

Reusable prompt for another agent:

```text
Use $human-to-action:refine-agent-prompts to write a paste-ready prompt for another agent to make the border match the attached reference.
```

Audit without rewriting:

```text
Audit this agent prompt for contradictions and missing completion criteria. Do not rewrite it.
```

## Privacy and trust

The local hook receives the normal lifecycle payload from Codex, drains it without retaining it, and emits fixed guidance. It contains no network, file-writing, telemetry, or logging code. Installing a command hook still creates a trust boundary: inspect the source and approve only the version you intend to run.

See [PRIVACY.md](PRIVACY.md) and [SECURITY.md](SECURITY.md) for the complete boundaries and reporting process.

## Repository layout

```text
.agents/plugins/marketplace.json   Marketplace catalog
plugins/human-to-action/           Installable HumanToAction plugin
skills/                            Future standalone skills
evals/                             Routing cases
tests/                             Deterministic hook tests
scripts/validate.py                Publication and structure checks
```

Bundled skills stay inside their plugin. The top-level `skills/` directory is reserved for standalone skills so the same workflow is not duplicated.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The deterministic tests verify fixed hook output, prompt non-echoing, namespace routing, manifest consistency, marketplace structure, public-path hygiene, and the documented evaluation cases. They do not prove model behavior; semantic routing should also be tested in a new Codex task after installation.

## Inspiration

The bundled checklist is inspired by [OpenAI's prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6). HumanToAction paraphrases and operationalizes selected ideas; it does not reproduce the article or claim official compatibility certification.

## Community and license

- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
- [Trademark guidance](TRADEMARKS.md)

Source is available under the [MIT License](LICENSE).
