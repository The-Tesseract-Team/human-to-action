from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins/human-to-action"
HOOK = PLUGIN_ROOT / "hooks/human-to-action.py"


def run_hook(prompt: str) -> subprocess.CompletedProcess[str]:
    payload = {
        "hook_event_name": "UserPromptSubmit",
        "prompt": prompt,
    }
    return subprocess.run(
        [sys.executable, str(HOOK)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )


def run_configured_hook(prompt: str) -> subprocess.CompletedProcess[str]:
    payload = {
        "hook_event_name": "UserPromptSubmit",
        "prompt": prompt,
    }
    return subprocess.run(
        ["/usr/bin/python3", str(HOOK)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )


class HookTests(unittest.TestCase):
    def test_source_compiles_without_writing_bytecode(self) -> None:
        compile(HOOK.read_text(encoding="utf-8"), str(HOOK), "exec")

    def test_hook_returns_fixed_context_without_echoing_prompt(self) -> None:
        marker = "DO_NOT_ECHO_THIS_PROMPT_MARKER"
        first = run_hook(marker)
        second = run_hook("a different request")

        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stderr, "")
        self.assertEqual(first.stdout, second.stdout)
        self.assertNotIn(marker, first.stdout)

    @unittest.skipUnless(Path("/usr/bin/python3").is_file(), "configured interpreter unavailable")
    def test_configured_interpreter_executes_hook(self) -> None:
        result = run_configured_hook("verify configured hook command")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("human-to-action:refine-agent-prompts", result.stdout)

    def test_hook_describes_both_destination_modes(self) -> None:
        result = run_hook("revamp this instruction")

        self.assertIn(
            "human-to-action:refine-agent-prompts",
            result.stdout,
        )
        self.assertIn("continue without returning a prompt", result.stdout)
        self.assertIn("another agent", result.stdout)


if __name__ == "__main__":
    unittest.main()
