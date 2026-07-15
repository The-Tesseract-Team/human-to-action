# Privacy

Last updated: 2026-07-15

HumanToAction is a local Codex plugin with a command hook and a bundled skill. It does not operate a separate service.

## Hook data flow

Codex supplies the normal `UserPromptSubmit` lifecycle payload to the local hook subprocess. The hook:

- drains that payload in bounded chunks without retaining its contents;
- emits the same fixed instruction text regardless of the submitted prompt;
- does not echo the prompt;
- does not write files, logs, or local storage;
- does not make network requests or include telemetry; and
- does not initiate an additional model call.

The hook subprocess necessarily receives the payload transiently so it can drain standard input. The plugin cannot change or make guarantees about Codex's own processing, retention, logging, account, or workspace policies.

## Skill data flow

When the bundled skill activates, its instruction text and relevant references can be loaded into the same Codex context used for the task. The skill tells the agent how to preserve user intent and route the result; it does not independently retrieve, store, or transmit user content.

## Dependencies and third parties

The runtime plugin uses only Python's standard library. `PyYAML` is a development-only validation dependency and is not loaded by the hook. GitHub and Codex remain governed by their own policies.

## Reports

Report a suspected privacy or security issue through the private process in [SECURITY.md](SECURITY.md). Do not include sensitive prompt content in a public issue.
