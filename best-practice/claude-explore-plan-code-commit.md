# Explore → Plan → Code → Commit

![Last Updated](https://img.shields.io/badge/Last_Updated-May%2007%2C%202026-white?style=flat&labelColor=555)

The foundational Claude Code workflow from Anthropic's official [best practices guide](https://www.anthropic.com/engineering/claude-code-best-practices). Every community workflow listed in [DEVELOPMENT WORKFLOWS](../README.md#-development-workflows) is a specialization of this four-phase pattern.

<table width="100%">
<tr>
<td><a href="../">← Back to Claude Code Best Practice</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

---

## The Pattern

| Phase | Goal | What Claude does | How to enforce |
|-------|------|------------------|----------------|
| **Explore** | Build context. No edits. | Reads files, runs `grep`/`find`, gathers facts. | Say "do not write code yet" or delegate to the [`Explore`](https://code.claude.com/docs/en/sub-agents) subagent. |
| **Plan** | Design before doing. | Proposes an approach you can critique. | [Plan Mode](https://code.claude.com/docs/en/permission-modes#plan-mode) (`Shift+Tab` twice), or `/ultraplan`. |
| **Code** | Execute the approved plan. | Edits files according to the plan. | Switch out of Plan Mode only after the plan is reviewed. |
| **Commit** | Capture the change cleanly. | Creates focused, reviewable commits. | One commit per file (see [project rule](../CLAUDE.md#git-commit-rules)). |

---

## Why It Works

The failure mode it prevents: Claude reads two files, infers a pattern, writes 200 lines, then discovers it misunderstood — now you have a half-correct diff to untangle.

Splitting `Explore` and `Plan` from `Code` makes that misunderstanding visible **before** code exists. The user reviews a plan (cheap to revise) instead of a diff (expensive to revise).

Two of the global behavioral guidelines in [`~/.claude/CLAUDE.md`](https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md) map directly onto the first two phases:

- **§1 Think Before Coding** = Explore + Plan
- **§4 Goal-Driven Execution** = Plan defines verifiable success criteria before Code starts

---

## How This Repo Already Implements It

Each phase has tooling built into this repo's configuration:

| Phase | Built-in support |
|-------|-----------------|
| Explore | [`Explore` subagent](https://code.claude.com/docs/en/sub-agents) (parallelizable — spawn multiple in one message for independent searches) |
| Plan | [Plan Mode](https://code.claude.com/docs/en/permission-modes#plan-mode), [`/ultraplan`](https://code.claude.com/docs/en/ultraplan), [`EnterPlanMode`](https://code.claude.com/docs/en/cli-reference) tool |
| Code | Default mode; `Auto Mode` for less prompting |
| Commit | [Per-file commit rule](../CLAUDE.md#git-commit-rules), [Checkpointing](https://code.claude.com/docs/en/checkpointing) for safe rewinds |

---

## Variations

- **TDD variant:** Explore → Plan → **Test** → Code → Commit. Write a failing test after Plan; Code runs until tests pass. Common in the [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock](https://github.com/mattpocock/skills) workflows.
- **Visual iteration variant:** For UI work, add screenshots after Code. Use the [Playwright MCP](https://code.claude.com/docs/en/mcp) or `agent-browser` skill.
- **Cross-model review variant:** Add a second-model review between Plan and Code (see [cross-model workflow](../development-workflows/cross-model-workflow/cross-model-workflow.md)).
- **Parallel Explore:** Spawn multiple `Explore` subagents in one message for independent searches — recommended in the [Agent tool docs](https://code.claude.com/docs/en/sub-agents).

---

## Anti-Patterns

| Anti-pattern | What goes wrong |
|--------------|-----------------|
| Skip Explore — start in Code | Claude infers structure from filenames, gets it wrong, edits the wrong file. |
| Skip Plan — bundle Explore + Code | You review a 200-line diff instead of a 5-line plan. Expensive to revise. |
| One giant commit at the end | Lost reviewability. Hard to bisect. Violates this repo's [per-file rule](../CLAUDE.md#git-commit-rules). |
| Re-Explore mid-Code | Context bloats. Use [`/compact`](https://code.claude.com/docs/en/interactive-mode) with a hint or [`/rewind`](https://code.claude.com/docs/en/checkpointing) instead. |

---

## See Also

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) — original Anthropic post
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) — official docs
- [DEVELOPMENT WORKFLOWS](../README.md#-development-workflows) — community workflows that extend this pattern
- [`tips/claude-boris-13-tips-03-jan-26.md`](../tips/claude-boris-13-tips-03-jan-26.md) — Boris Cherny on plan mode discipline
