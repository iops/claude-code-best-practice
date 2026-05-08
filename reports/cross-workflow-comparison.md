# Cross-Workflow Comparison: Superpowers vs Spec Kit vs gstack

![Last Updated](https://img.shields.io/badge/Last_Updated-May%2008%2C%202026-white?style=flat&labelColor=555)

A side-by-side analysis of three of the most-starred Claude Code workflow repos — what each optimizes for, where they conflict, and how to combine the best moves from each on top of Anthropic's foundational [Explore → Plan → Code → Commit](../best-practice/claude-explore-plan-code-commit.md) pattern.

<table width="100%">
<tr>
<td><a href="../">← Back to Claude Code Best Practice</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

---

## At a Glance

| | [Superpowers](https://github.com/obra/superpowers) | [Spec Kit](https://github.com/github/spec-kit) | [gstack](https://github.com/garrytan/gstack) |
|---|---|---|---|
| **★ Stars** | 175k | 92k | 88k |
| **Author** | Jesse Kriss (obra) | GitHub | Garry Tan |
| **Agents** | 5 | 0 | 0 |
| **Commands** | 3 | 9 | 0 |
| **Skills** | 14 | 0 | 43 |
| **Primary primitive** | Subagents + skills | Commands (artifacts) | Skills (persona prompts) |
| **Failure mode it fights** | Regression / integration bugs | Ambiguity | Strategic misalignment |
| **Source of truth** | The test suite | The spec doc | The stakeholder review |
| **Loop discipline** | Sub-loops (TDD, review) | Forward-only (waterfall-ish) | Forward with QA gate |
| **Ceremony cost** | High throughout | High upfront, low later | Medium, persona-driven |

---

## Superpowers — *Parallelism + tests catch what reviews miss*

**Pattern:** `brainstorming → using-git-worktrees → writing-plans → subagent-driven-development → TDD → requesting-code-review → finishing-a-development-branch`

### What's distinctive

- **Git worktrees as a first-class phase.** Each task gets its own isolated working directory, so multiple subagents can work in parallel without stepping on each other.
- **Subagent-driven development** is its own phase — explicitly orchestrating specialist subagents rather than one monolithic Claude.
- **TDD as a mandatory sub-loop** (the yellow tag in the README workflow table). You can't enter the implement phase without a failing test.
- **Code review as a sub-loop.** Review is iterative, not a single end-of-stream gate.

### Best for

Complex features that benefit from parallelism and need strong correctness guarantees. The ceremony cost buys you reduced regression risk.

### Weak when

Tasks are small or sequential — the worktree + subagent overhead dominates. Steep on-ramp for users new to git worktrees.

---

## Spec Kit — *Most failures are spec failures. Eliminate ambiguity before code*

**Pattern:** `/speckit.constitution → /speckit.clarify → /speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement`

### What's distinctive

- **`/speckit.constitution`** — project-level principles (your "north star": what the system must always do). No other workflow has this.
- **`/speckit.clarify`** — explicit ambiguity-removal phase. Claude is forced to surface every uncertain interpretation *before* speccing.
- **Pure command-based.** No agents, no skills. Each step produces a written artifact (constitution, spec, plan, task list) that stays in the repo. Auditable.
- **Waterfall-ish on purpose.** You don't loop back without reopening the prior artifact.

### Best for

Greenfield features, multi-stakeholder projects, regulated environments where traceability matters. The spec *is* the deliverable as much as the code.

### Weak when

Rapid prototyping or research code — you spend more time speccing than building. No built-in review or QA gate after implement.

---

## gstack — *Different stakeholders catch different blind spots. Simulate the team*

**Pattern:** `/office-hours → /plan-ceo-review → /plan-eng-review → /plan-design-review → implement → /review → /qa → /ship → /land-and-deploy`

### What's distinctive

- **Three parallel plan reviews** by personas — CEO (business value), Engineering (feasibility), Design (UX). gstack's signature move; no other major workflow does multi-perspective planning natively.
- **`/office-hours`** — YC-style ideation phase, where Claude plays advisor.
- **`/ship` and `/land-and-deploy` as separate phases.** Most workflows treat shipping as commit + push; gstack splits "ship" (release-ready) from "land-and-deploy" (in production).
- **All 43 skills, zero commands, zero agents.** Heaviest reliance on Claude's auto-discovery — Garry's bet that natural-language triggers beat explicit slash commands at scale.

### Best for

Startup-style product teams where you'd actually have CEO/Eng/Design reviews. Catches "this is technically right but strategically wrong" issues other workflows miss.

### Weak when

Solo work or low-stakes changes — the persona overhead is theatrical for a typo fix. Persona quality only as good as the prompt files behind them.

---

## Where They Overlap, Where They Collide

All three have a **Plan phase** and an implicit **Explore** before it — they all shadow the [Explore → Plan → Code → Commit](../best-practice/claude-explore-plan-code-commit.md) base pattern.

The conflicts are *philosophical*, not mechanical:

| Conflict point | Spec Kit's answer | Superpowers' answer | gstack's answer |
|----------------|-------------------|---------------------|-----------------|
| What's the source of truth? | The spec | The tests | The stakeholder review |
| How do you validate? | Re-read the spec | Run the tests | Persona critique |
| What's the unit of work? | A task in the task list | A subagent's worktree | A skill invocation |
| When is it done? | All tasks implemented | All tests pass | `/qa` and `/ship` clean |

The most direct collision is **Spec Kit's `/speckit.tasks`** vs **Superpowers' subagent decomposition** — both produce a task breakdown but in incompatible formats. You'd pick one or the other.

---

## Can They Be Combined Into a Superset?

**Yes, partially — but not by installing all three wholesale.**

Installing the full skill/command sets gives you 14 + 9 + 43 = 66 specialized triggers plus 5 Superpowers agents. That's not a workflow; that's a buffet your future self can't navigate. Auto-discovery starts misfiring when there are too many similarly-named skills competing for the same prompt.

The smarter approach: **pick the signature move from each** and drop redundant phases — because they all sit on top of Explore → Plan → Code → Commit anyway, you can swap in specialized phases without breaking coherence.

### A pragmatic combined workflow

```
EXPLORE  (base pattern — read first)
   │
   ├─→ /speckit.constitution     [Spec Kit] — once per project
   ├─→ /speckit.clarify          [Spec Kit] — for genuinely ambiguous specs
   │
PLAN
   │
   ├─→ /plan-eng-review          [gstack] — feasibility check
   ├─→ /plan-ceo-review          [gstack] — for product features only
   ├─→ using-git-worktrees       [Superpowers] — for parallel/risky work
   │
CODE
   │
   ├─→ test-driven-development   [Superpowers] — mandatory for shipping code
   ├─→ subagent-driven-dev       [Superpowers] — for parallelizable tasks
   ├─→ /qa                       [gstack] — pre-ship gate
   │
COMMIT  (base pattern — focused commits per project rules)
   │
   └─→ /ship  →  /land-and-deploy [gstack] — explicit release/deploy split
```

### What's deliberately dropped

| Dropped phase | Reason |
|---------------|--------|
| gstack's `/office-hours` | Overlaps with base Explore |
| Spec Kit's `/speckit.specify` and `/speckit.plan` | Overlaps with base Plan + Plan Mode |
| gstack's `/plan-design-review` | Keep only if you have a UI surface |
| Superpowers' `brainstorming` and `writing-plans` | Overlaps with base Plan |
| Spec Kit's `/speckit.tasks` and `/speckit.implement` | Overlaps with base Code |

The principle: **one phase, one chosen specialization.** Don't run three different "plan review" gates back-to-back. Pick the one that fights *your* dominant failure mode for *this* task type.

---

## When To Use What

| Task type | Recommended combination |
|-----------|------------------------|
| One-line bug fix | Just Explore → Plan → Code → Commit. Skip everything else. |
| Routine feature | Base pattern + `test-driven-development` (Superpowers) |
| Greenfield service | Spec Kit's `constitution` + `clarify`, then Superpowers' TDD + worktrees |
| Product feature with stakeholders | gstack's three plan reviews + Superpowers' TDD + base commit/ship |
| Refactor across many files | Superpowers' worktrees + subagent-driven-development |
| Compliance-heavy change | Full Spec Kit (audit trail matters) + Superpowers' TDD |

---

## The Honest Answer

There is no single superset because the *cost* of running all three in series exceeds the cost of being wrong on most tasks. The right framing:

> **Explore → Plan → Code → Commit is the superset.** Everything else is a context-specific specialization you opt into when the failure mode it fights is your actual risk for *this* task.

That's also why this repo's [`development-workflows/rpi/`](../development-workflows/rpi/rpi-workflow.md) ships as a single specialization rather than a megaworkflow — RPI maps directly onto the base pattern (Research = Explore, Plan = Plan, Implement = Code + Commit) and adds specialist agents for one specific failure mode. Same logic should apply when you're choosing what to install from Superpowers, Spec Kit, or gstack.

---

## See Also

- [Explore → Plan → Code → Commit](../best-practice/claude-explore-plan-code-commit.md) — the foundational pattern
- [DEVELOPMENT WORKFLOWS table](../README.md#-development-workflows) — full list of community workflows with phase breakdowns
- [RPI Workflow](../development-workflows/rpi/rpi-workflow.md) — this repo's implementation of a base-pattern specialization
- [Cross-Model Workflow](../development-workflows/cross-model-workflow/cross-model-workflow.md) — multi-model validation pattern
