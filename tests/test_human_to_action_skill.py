import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin/plugin.json"
SKILL = ROOT / "skills/refine-agent-prompts/SKILL.md"
AGENT = ROOT / "skills/refine-agent-prompts/agents/openai.yaml"
EVALS = ROOT / "evals/cases.json"
NAMESPACED_SKILL = "$human-to-action:refine-agent-prompts"


class ExplicitActivationTests(unittest.TestCase):
    def test_plugin_has_no_hook_runtime(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(manifest["version"], "0.2.0")
        self.assertNotIn("hooks", manifest)
        self.assertFalse((ROOT / "hooks").exists())

    def test_implicit_skill_invocation_is_disabled(self) -> None:
        agent = yaml.safe_load(AGENT.read_text(encoding="utf-8"))

        self.assertIs(agent["policy"]["allow_implicit_invocation"], False)
        self.assertIn(NAMESPACED_SKILL, agent["interface"]["default_prompt"])

    def test_skill_documents_explicit_activation_and_handoff_routes(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")

        self.assertIn("## Activation gate", skill)
        self.assertIn("@HumanToAction", skill)
        self.assertIn(NAMESPACED_SKILL, skill)
        for destination in ("new task", "new thread", "new workspace", "handoff"):
            self.assertIn(destination, skill)

    def test_eval_cases_separate_invoked_and_uninvoked_prompts(self) -> None:
        cases = json.loads(EVALS.read_text(encoding="utf-8"))

        for case in cases["positive"]:
            prompt = case["prompt"]
            self.assertTrue(
                "@HumanToAction" in prompt or NAMESPACED_SKILL in prompt,
                case["id"],
            )
        for case in cases["negative"]:
            prompt = case["prompt"]
            self.assertNotIn("@HumanToAction", prompt, case["id"])
            self.assertNotIn(NAMESPACED_SKILL, prompt, case["id"])


if __name__ == "__main__":
    unittest.main()
