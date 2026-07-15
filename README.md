# HumanToAction

A non-commercial open-source Codex plugin maintained as a personal developer hobby project.

This is an independent community project. It is not affiliated with, endorsed by, or an official product of OpenAI.

**Human intent in. Agent-ready action out.**

HumanToAction is an explicit-only skill that helps an agent preserve the user's actual context and choose the right destination for prompt refinement:

- Same task: refine the instruction internally, disclose that once, and continue the work.
- Another agent, new task, handoff, or reusable artifact: return a paste-ready prompt.
- Prompt audit: report consequential findings without silently rewriting the prompt.
- Ordinary work without an explicit HumanToAction invocation: stay completely out of the way.

HumanToAction has no lifecycle hook and does not run automatically. It loads only when you explicitly select `@HumanToAction` in the app or invoke `$human-to-action:refine-agent-prompts` in the prompt. It uses the current model call rather than starting another one.

## Install

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add The-Tesseract-Team/human-to-action --ref main
```

Then install the plugin:

```bash
codex plugin add human-to-action@tesseract-team
```

Restart the ChatGPT desktop app and begin a new task so the bundled skill is discovered.

## Use

HumanToAction never activates from prompt-refinement intent alone. Explicitly select `@HumanToAction` in the app or include `$human-to-action:refine-agent-prompts` in the message.

Same-task refinement:

```text
@HumanToAction Refine this instruction internally and continue: make the border match the attached reference.
```

New-task handoff:

```text
@HumanToAction new task: prepare a paste-ready prompt for another agent to make the border match the attached reference.
```

The phrases `new task`, `new thread`, `new workspace`, and `handoff` select exported-prompt mode when HumanToAction is explicitly invoked. The skill returns the paste-ready handoff and does not execute it.

Direct skill invocation:

```text
Use $human-to-action:refine-agent-prompts to audit this agent prompt without rewriting it.
```

## Privacy and trust

The plugin contains instructions and references only. It has no command hook, executable runtime, network access, persistence, telemetry, or prompt logging.

See [PRIVACY.md](PRIVACY.md) and [SECURITY.md](SECURITY.md) for the complete boundaries and reporting process.

## Repository layout

```text
.agents/plugins/marketplace.json   Marketplace catalog
.codex-plugin/plugin.json          Plugin manifest
skills/refine-agent-prompts/       Bundled refinement skill
evals/cases.json                   Routing cases
tests/                             Deterministic activation and routing tests
scripts/validate.py                Publication and structure checks
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The deterministic tests verify explicit-only activation metadata, handoff routing terms, manifest consistency, marketplace structure, public-path hygiene, and the documented evaluation cases. They do not prove model behavior; semantic routing should also be tested in a new Codex task after installation.

## Inspiration

The bundled checklist is inspired by [OpenAI's prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6). HumanToAction paraphrases and operationalizes selected ideas; it does not reproduce the article or claim official compatibility certification.

## Community and license

- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
- [Trademark guidance](TRADEMARKS.md)

Source is available under the [MIT License](LICENSE).
