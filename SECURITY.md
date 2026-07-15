# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 0.2.x | Yes |
| 0.1.x | No |
| Earlier or modified copies | No |

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/The-Tesseract-Team/human-to-action/security/advisories/new). Do not open a public issue for a suspected vulnerability, private prompt content, credential, or personal data.

This is a volunteer, non-commercial project with no guaranteed response time. Reports will be acknowledged and handled on a best-effort basis. Include the affected version, platform, reproduction steps, impact, and the smallest safe evidence needed.

## Trust boundaries

- Version 0.2.0 contains no lifecycle hook or executable plugin runtime.
- The skill is configured for explicit invocation only and has no network, persistence, telemetry, or file-writing behavior.
- The plugin does not guarantee that an agent will interpret or follow every instruction correctly.
- Codex, GitHub, operating-system logging, and modified distributions are outside this repository's control.
- No binary release is distributed. Users inspect and run source.

Security fixes may change behavior when preserving the vulnerable behavior would be unsafe.
