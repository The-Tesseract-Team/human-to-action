# Privacy

Last updated: 2026-07-15

HumanToAction is a local Codex plugin containing a bundled skill and reference material. It does not operate a separate service or include a command hook.

## Skill data flow

The bundled skill activates only through explicit selection or invocation. Its instruction text and relevant references can then be loaded into the same Codex context used for the task. The skill tells the agent how to preserve user intent and route the result; it does not independently retrieve, store, or transmit user content.

## Dependencies and third parties

The plugin has no executable runtime dependency. `PyYAML` is used only by repository validation and tests. GitHub and Codex remain governed by their own policies.

## Reports

Report a suspected privacy or security issue through the private process in [SECURITY.md](SECURITY.md). Do not include sensitive prompt content in a public issue.
