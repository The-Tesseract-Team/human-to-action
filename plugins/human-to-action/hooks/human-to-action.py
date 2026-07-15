#!/usr/bin/env python3
"""Inject HumanToAction's fixed context preflight on each user turn."""

import sys


def main() -> None:
    # Codex provides the submitted hook payload to this local subprocess. Drain
    # it in bounded chunks without retaining, echoing, persisting, or transmitting
    # its contents.
    while sys.stdin.read(8192):
        pass
    sys.stdout.write(
        "Use the current request, relevant conversation, project instructions and files, "
        "supplied artifacts, and evidence as one context. Preserve explicit values, scope, "
        "authority, and unrelated behavior; validate the result. For visual work, follow "
        "the latest approved reference and inspect the result. If the user refines the "
        "current task instruction, briefly say that "
        "`human-to-action:refine-agent-prompts` was applied internally, then "
        "continue without returning a prompt. Return "
        "a prompt only for another agent, a new task, handoff, reuse, or an explicit "
        "copyable artifact."
    )


if __name__ == "__main__":
    main()
