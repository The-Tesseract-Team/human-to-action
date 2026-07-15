#!/usr/bin/env python3
"""Validate the public marketplace and HumanToAction bundle without a model call."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_REL = Path("plugins/human-to-action")
PLUGIN_ROOT = REPO_ROOT / PLUGIN_REL
PLUGIN_NAME = "human-to-action"
SKILL_NAME = "refine-agent-prompts"
NAMESPACED_SKILL = f"{PLUGIN_NAME}:{SKILL_NAME}"
MARKETPLACE_NAME = "tesseract-agent-extensions"
REPOSITORY_URL = "https://github.com/The-Tesseract-Team/agent-extensions"

REQUIRED_REPO_PATHS = (
    ".agents/plugins/marketplace.json",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug-report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature-request.yml",
    ".github/dependabot.yml",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PRIVACY.md",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "TRADEMARKS.md",
    "evals/human-to-action/cases.json",
    "requirements-dev.txt",
    "scripts/validate.py",
    "skills/README.md",
    "tests/test_human_to_action_hook.py",
)

REQUIRED_PLUGIN_PATHS = (
    ".codex-plugin/plugin.json",
    "hooks/hooks.json",
    "hooks/human-to-action.py",
    "skills/refine-agent-prompts/SKILL.md",
    "skills/refine-agent-prompts/agents/openai.yaml",
    "skills/refine-agent-prompts/references/gpt-5-6-prompt-guidance.md",
)

TEXT_SUFFIXES = {"", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}
EXCLUDED_PARTS = {".git", ".venv", "__pycache__"}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
PRIVATE_PATH_PATTERNS = (
    re.compile("/" + r"Users/[^/\s]+/"),
    re.compile("/" + r"home/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\" + r"Users\\[^\\\s]+\\"),
)
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"gh" + r"[opsu]_[A-Za-z0-9]{20,}"),
    "OpenAI key": re.compile(r"sk-" + r"[A-Za-z0-9_-]{20,}"),
    "private key": re.compile(r"BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "AWS access key": re.compile(r"AKIA" + r"[A-Z0-9]{16}"),
}
STALE_IDENTITIES = (
    "context-" + "first-prompting",
    "Context-" + "First Prompting",
    "Local " + "developer",
)


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise AssertionError(f"invalid JSON at {relative(path)}") from None


def load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        raise AssertionError(f"invalid YAML at {relative(path)}") from None


def iter_public_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        assert not path.is_symlink(), f"symlink requires review: {relative(path)}"
        if path.is_file():
            files.append(path)
    return sorted(files)


def validate_required_paths() -> None:
    missing = [path for path in REQUIRED_REPO_PATHS if not (REPO_ROOT / path).is_file()]
    missing.extend(
        str(PLUGIN_REL / path)
        for path in REQUIRED_PLUGIN_PATHS
        if not (PLUGIN_ROOT / path).is_file()
    )
    assert not missing, f"missing required public files: {', '.join(missing)}"


def validate_public_text_surface() -> None:
    for path in iter_public_files():
        rel = relative(path)
        assert path.suffix != ".pyc", f"compiled Python found: {rel}"
        assert path.suffix.lower() in TEXT_SUFFIXES, f"unreviewed binary or file type: {rel}"
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise AssertionError(f"non-UTF-8 public file: {rel}") from None

        for pattern in PRIVATE_PATH_PATTERNS:
            assert not pattern.search(text), f"private absolute path found in {rel}"
        for category, pattern in SECRET_PATTERNS.items():
            assert not pattern.search(text), f"potential {category} found in {rel}"
        for stale_identity in STALE_IDENTITIES:
            assert stale_identity not in text, f"stale private plugin identity found in {rel}"


def validate_serialized_files() -> None:
    for path in iter_public_files():
        if path.suffix.lower() == ".json":
            load_json(path)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            load_yaml(path)


def validate_manifest() -> None:
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin/plugin.json")
    assert isinstance(manifest, dict), "plugin manifest must be an object"
    assert manifest.get("name") == PLUGIN_NAME
    assert PLUGIN_ROOT.name == manifest.get("name"), "plugin folder and manifest name differ"
    assert SEMVER.fullmatch(str(manifest.get("version", ""))), "invalid plugin version"
    assert manifest.get("description")
    assert manifest.get("skills") == "./skills/"
    assert manifest.get("license") == "MIT"
    assert manifest.get("repository") == REPOSITORY_URL
    assert "hooks" not in manifest, "hooks must use default discovery, not manifest metadata"

    author = manifest.get("author")
    assert author == {
        "name": "Benny Ebere",
        "url": "https://github.com/tesseractT",
    }

    interface = manifest.get("interface")
    assert isinstance(interface, dict)
    assert interface.get("displayName") == "HumanToAction"
    assert interface.get("developerName") == "The Tesseract Team"
    assert interface.get("category") == "Productivity"
    assert interface.get("privacyPolicyURL") == f"{REPOSITORY_URL}/blob/main/PRIVACY.md"
    prompts = interface.get("defaultPrompt")
    assert isinstance(prompts, list) and 1 <= len(prompts) <= 3
    assert all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts)


def validate_marketplace() -> None:
    marketplace = load_json(REPO_ROOT / ".agents/plugins/marketplace.json")
    assert isinstance(marketplace, dict)
    assert marketplace.get("name") == MARKETPLACE_NAME
    assert marketplace.get("interface") == {"displayName": "Tesseract Agent Extensions"}
    plugins = marketplace.get("plugins")
    assert isinstance(plugins, list) and len(plugins) == 1
    entry = plugins[0]
    assert entry.get("name") == PLUGIN_NAME
    assert entry.get("source") == {
        "source": "local",
        "path": "./plugins/human-to-action",
    }
    assert entry.get("policy") == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    assert entry.get("category") == "Productivity"


def validate_ci() -> None:
    workflow = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "permissions:\n  contents: read" in workflow
    assert "persist-credentials: false" in workflow
    assert "runs-on: ubuntu-24.04" in workflow
    assert "timeout-minutes: 10" in workflow
    action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s]+)", workflow)
    assert action_refs, "CI has no pinned actions"
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in action_refs), (
        "every CI action must use an immutable commit SHA"
    )
    assert (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8") == (
        "PyYAML==6.0.3\n"
    )


def validate_hook() -> None:
    hook_path = PLUGIN_ROOT / "hooks/human-to-action.py"
    hooks = load_json(PLUGIN_ROOT / "hooks/hooks.json")
    handlers = hooks["hooks"]["UserPromptSubmit"]
    assert isinstance(handlers, list) and len(handlers) == 1
    command_hooks = handlers[0]["hooks"]
    assert isinstance(command_hooks, list) and len(command_hooks) == 1
    assert command_hooks[0] == {
        "type": "command",
        "command": '/usr/bin/python3 "$PLUGIN_ROOT/hooks/human-to-action.py"',
        "timeout": 5,
    }

    tree = ast.parse(hook_path.read_text(encoding="utf-8"), filename=str(hook_path))
    imports = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    assert imports <= {"sys"}, "hook imports an unreviewed module"
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"open", "exec", "eval"}
        for node in ast.walk(tree)
    ), "hook uses an unreviewed file or code-execution primitive"

    marker = "DO_NOT_ECHO_THIS_PROMPT_MARKER"
    outputs: list[str] = []
    for prompt in (marker, "different prompt"):
        payload = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": prompt})
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            cwd=REPO_ROOT,
            input=payload,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        assert result.returncode == 0, "hook smoke test failed"
        assert not result.stderr, "hook wrote to stderr"
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1], "hook output depends on submitted prompt"
    assert marker not in outputs[0], "hook echoed the submitted prompt"
    assert NAMESPACED_SKILL in outputs[0]
    assert "another agent" in outputs[0]


def validate_skill() -> None:
    skill_path = PLUGIN_ROOT / "skills/refine-agent-prompts/SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    assert skill_text.startswith("---\n"), "SKILL.md frontmatter is missing"
    _, frontmatter_text, _ = skill_text.split("---", 2)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        raise AssertionError("invalid skill frontmatter") from None
    assert isinstance(frontmatter, dict)
    assert frontmatter.get("name") == SKILL_NAME
    assert isinstance(frontmatter.get("description"), str)

    agent = load_yaml(PLUGIN_ROOT / "skills/refine-agent-prompts/agents/openai.yaml")
    assert isinstance(agent, dict)
    assert f"${NAMESPACED_SKILL}" in agent["interface"]["default_prompt"]
    assert agent["policy"]["allow_implicit_invocation"] is True


def validate_evals() -> None:
    cases = load_json(REPO_ROOT / "evals/human-to-action/cases.json")
    assert isinstance(cases, dict)
    positive = cases.get("positive")
    negative = cases.get("negative")
    assert isinstance(positive, list) and isinstance(negative, list)
    assert {case.get("id") for case in positive} == {
        "current-task-refinement",
        "other-agent-export",
        "audit-without-rewrite",
        "gpt-5-6-migration",
        "visual-reference-handoff",
    }
    assert {case.get("id") for case in negative} == {
        "ordinary-task",
        "casual-chat",
        "general-copy-editing",
    }
    exported = next(case for case in positive if case.get("id") == "other-agent-export")
    assert f"${NAMESPACED_SKILL}" in exported.get("prompt", "")


def validate_markdown_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in iter_public_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            target = target.strip().strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#", "codex:")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            assert resolved.is_relative_to(REPO_ROOT.resolve()), (
                f"Markdown link escapes repository in {relative(path)}"
            )
            assert resolved.exists(), f"broken Markdown link in {relative(path)}"


def main() -> int:
    checks = (
        validate_required_paths,
        validate_public_text_surface,
        validate_serialized_files,
        validate_manifest,
        validate_marketplace,
        validate_ci,
        validate_hook,
        validate_skill,
        validate_evals,
        validate_markdown_links,
    )
    try:
        for check in checks:
            check()
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print("repository checks passed: structure, metadata, hook behavior, and redacted pattern scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
