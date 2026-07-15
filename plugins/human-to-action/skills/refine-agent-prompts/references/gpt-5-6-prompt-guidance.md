# GPT-5.6 prompt-refinement checklist

Source: [OpenAI prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)

This is a distilled operating checklist, not a copy of the article. Fetch the official page before giving current model-specific guidance or citations because it can change.

## Scope

The simplification advice is optimized for GPT-5.6. When the target is older or unknown, preserve working scaffolding unless capability evidence or representative evaluations justify removing it.

## Preserve first

- User-visible outcome and intended audience.
- Relevant domain, current state, prior decisions, and task context.
- Exact values and explicit user choices.
- Success criteria and stopping conditions.
- Safety, business, evidence, permission, cost, and side-effect constraints.
- Required output shape, citations, and validation.
- Personality and collaboration style only when they materially affect the experience.

When the desired value is implicit, name the authoritative source or decision criterion. Do not guess, use keyword maps as a substitute for semantic judgment, or encode broad shortcuts that destroy context.

## Simplify second

- Remove duplicate rules, examples, and style instructions.
- Remove process scaffolding for behavior the target model already performs reliably.
- Remove irrelevant tools and tool descriptions.
- Resolve contradictions before adding detail.
- Prefer decision rules over absolute language for judgment calls.
- Describe the destination and let the agent choose an efficient path.

Keep stable, reusable instructions in a consistent prefix and put variable request context later when cache reuse matters.

## Context and clarification

- Give the agent evidence it cannot infer from training or the visible environment.
- Preserve the artifact, length, structure, genre, terminology, and factual claims.
- Tell the agent when an important ambiguity should trigger a question.
- Ask for the smallest missing field rather than restarting discovery.
- Do not use placeholders for material context unless the requested artifact is a template.
- Do not turn absence of evidence into a factual negative.

## Autonomy and tools

- Separate read, diagnose, plan, implementation, review, and external-coordination authority.
- Authorize local edits only for change, build, fix, or edit requests.
- Stop before destructive, costly, external, or scope-expanding actions without authority.
- Expose task-relevant tools only.
- Discover and validate prerequisites before acting.
- Parallelize independent reads; keep dependent decisions sequential.

Use direct tool calls when approval, citations, native artifacts, semantic judgment, or result-dependent next steps matter. Use programmatic tool calling only for a bounded deterministic reduction stage. If used, specify eligible tools, a compact intermediate schema, retry limit, stop condition, handoff back to the model, and validation of both the program output and final response.

## Retrieval and grounding

- Define what needs support and what counts as enough evidence.
- Cite retrieved sources near supported claims.
- Separate inference from sourced fact.
- State source conflicts.
- Treat empty, partial, or suspiciously narrow results as inconclusive; try one or two meaningful alternate queries or sources.
- Narrow the conclusion or name missing evidence instead of guessing.

## Validation and completion

- Give the agent access to relevant checks and name the checks that matter.
- For code, prefer targeted tests, type or lint checks, affected builds, and a minimal smoke test.
- For visual work, render and inspect the result.
- For plans, cover requirements, named resources, state or data flow, failure behavior, validation, privacy or security, and only material open questions.
- Stop when the core request is complete with useful evidence; do not retrieve again only to improve phrasing or add nonessential detail.

## Optional complex-prompt structure

Use only sections that change behavior:

```text
Role: [function and operating context]

Personality: [tone, if material]

Collaboration: [autonomy and update behavior, if material]

Goal: [user-visible outcome]

Success criteria: [what must be true before completion]

Context: [relevant state, evidence, sources of truth, and exact values]

Constraints: [scope, safety, business, permissions, and side effects]

Tools: [routing, prerequisites, failures, and approval rules]

Output: [artifact, fields, format, length, and tone]

Validation: [checks that must run or be reported]

Stop rules: [when to retry, fallback, ask, abstain, or finish]
```

## Prompt-stack migration

1. Switch to GPT-5.6 while preserving the current working prompt and reasoning effort.
2. Run representative evaluations before changing the prompt.
3. Test the same reasoning effort and one level lower on the same cases.
4. Remove one group of obsolete or repeated instructions at a time.
5. Add the smallest targeted rule that fixes a measured regression.
6. Rerun the same evaluations after each change.

Avoid rewriting a working prompt stack all at once; otherwise behavior changes cannot be attributed reliably.

For long-running prompt stacks:

- preserve assistant phase values when replaying history;
- compact after meaningful milestones rather than every turn;
- keep compacted state opaque and functionally consistent with the original prompt;
- reuse persisted reasoning only while the objective and assumptions remain stable;
- discard stale prior reasoning when the objective or assumptions change;
- request concise updates at major phase transitions rather than every tool call.
