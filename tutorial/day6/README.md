# Level 6 — Agents

[Back to Tutorial Index](../README.md) | [Previous: Level 5](../day5/README.md)

---

## What You'll Learn

- What agents are and why isolation matters
- How to create a specialist agent
- How agents preload skills
- How agent memory persists between sessions

---

## Prerequisites

- Completed [Level 5](../day5/README.md) — you can create skills with auto-discovery

---

## The Concept: Specialist Workers

Imagine you're managing a project. You *could* do everything yourself at your desk — research, writing, design, data analysis — but your desk gets cluttered. Papers pile up. You lose track of what's what.

Now imagine you have a **specialist** in a separate office. You say "go research X and bring me a summary." They go to their office (their own clean desk), do all the messy work — reading 20 documents, trying 5 approaches, hitting dead ends — and come back with just the clean result. Your desk stays tidy.

That's what an **agent** (also called a "subagent") does in Claude Code. It works in its own **isolated context window** — its own whiteboard — so all the messy intermediate work stays there. Only the final result comes back to your main conversation.

### Why this matters

Remember Level 2? Context fills up. If Claude reads 15 files and runs 8 searches to answer your question, all of that lands on *your* whiteboard. With an agent:

```
Your whiteboard:  "Get me the weather report"  →  [agent works]  →  "Dubai: 34C, Clear"
Agent's whiteboard: [reads API docs, tries 3 endpoints, handles an error, formats result]
```

The agent's messy work stays in the agent's context. You only see the clean answer.

---

## Creating an Agent

Agents live as markdown files in `.claude/agents/`:

```
my-project/
  .claude/
    agents/
      weather-reporter.md      ← Agent definition
      file-analyzer.md         ← Another agent
```

### A simple agent

```markdown
---
name: weather-reporter
description: "PROACTIVELY use when the user asks about weather or temperature"
model: haiku
skills:
  - weather-fetcher
---

You are the Weather Reporter. Your job:
1. Use your weather-fetcher skill to get current temperature data
2. Format the result clearly: City, Temperature (Celsius), Conditions
3. Keep your response to 2 lines maximum
```

Let's break down what's new here:

### Key frontmatter fields

| Field | What it does | Example |
|-------|-------------|---------|
| `name` | Agent identifier | `weather-reporter` |
| `description` | When to invoke (use "PROACTIVELY" for auto-dispatch) | See above |
| `model` | Which AI model the agent uses | `haiku` (fast), `sonnet`, `opus` (powerful) |
| `skills` | Skills preloaded into the agent's context | `- weather-fetcher` |
| `tools` | Which tools the agent can use | `Bash, Read, Glob` |
| `maxTurns` | How many steps the agent can take before stopping | `10` |
| `memory` | Whether the agent remembers across sessions | `project`, `user`, `local` |

### The `skills:` field — preloading knowledge

This is powerful. When you list skills in an agent's frontmatter, those skills are loaded into the agent's context *before* it starts working. It's like giving the specialist their training manual before they walk into their office.

The weather-reporter agent has `weather-fetcher` preloaded — so it already knows the exact API, coordinates, and format to use.

### The `tools:` field — limiting access

You can restrict what an agent is allowed to do. A `weather-reporter` agent doesn't need to write files or edit code — it just needs to make API calls:

```yaml
tools: Bash, Read
```

This prevents the agent from accidentally modifying your project.

---

## How Agents Get Invoked

There are two ways:

### 1. Automatic dispatch (via description)

If the description says "PROACTIVELY use when..." — Claude's main session will automatically dispatch work to this agent when the situation matches. You don't type anything special.

### 2. Explicit reference

You can mention the agent by name: "Ask the weather-reporter to check Dubai's temperature." Claude will dispatch to it.

---

## Agent Memory

Agents can remember things between sessions. Set `memory: project` in the frontmatter, and the agent gets a persistent memory file at `.claude/agent-memory/<agent-name>/MEMORY.md`.

What does this look like in practice?

```
You: "Ask the weather reporter for Dubai's weather"
Agent: "Dubai: 34C, Clear. (Noted: user prefers Dubai.)"
         ↓ saves to memory

[next session]
You: "Get me the usual weather report"
Agent: [reads memory] "Dubai: 31C, Partly cloudy."
         (Remembered that "usual" means Dubai!)
```

The agent builds up contextual knowledge over time — learning your preferences, common queries, and patterns.

---

## The Context Isolation Benefit

Here's a real scenario showing why isolation matters:

**Without an agent** (everything on your whiteboard):
```
You: "What's the weather in Dubai?"
Claude: [reads API docs... 500 lines of context]
        [tries endpoint... error, 200 more lines]
        [tries different parameters... 300 more lines]
        [finally succeeds... 100 more lines]
        "Dubai: 34C"

Your context used: ~1100 lines for one answer
```

**With an agent** (work happens in isolated context):
```
You: "What's the weather in Dubai?"
[agent dispatched → works in its own context]
Agent returns: "Dubai: 34C, Clear"

Your context used: ~20 lines (your question + the answer)
```

Same result. 98% less context consumed in your main conversation.

---

## Hands-On Exercise

**Step 1:** Study the real weather-agent in this repo:
```
Read .claude/agents/weather-agent.md and explain each frontmatter field
```

**Step 2:** Create a simple agent. Ask Claude:
```
Create a file at .claude/agents/file-summarizer.md with:

---
name: file-summarizer
description: "PROACTIVELY use when the user asks to summarize, analyze, or describe files in the project"
model: haiku
tools: Read, Glob, Grep
maxTurns: 5
memory: project
---

You are the File Summarizer. Your job:
1. Find the requested files using Glob or Grep
2. Read their contents
3. Provide a concise summary (3-5 bullet points per file)
4. Note the total line count and last modified date if relevant

Remember: you work in isolation. Keep your summaries focused and return only the final result.
```

**Step 3:** Start a fresh session and test it:
```bash
claude
```
```
Summarize the tutorial files in this project
```

Claude should dispatch to the file-summarizer agent. Watch the output — you'll see an indicator that an agent is working.

**Step 4:** Check that isolation worked — your context should be lean (just your question + the summary), not bloated with all the file reads.

**Step 5:** Test memory persistence. Ask:
```
Summarize any new files since last time
```

If the agent has memory enabled, it will reference what it knew from the previous run.

---

## The Weather Thread

Our system is almost complete:
- **Level 1**: Unpredictable answers
- **Level 3**: Consistent format (CLAUDE.md rules)
- **Level 4**: Consistent trigger (`/get-weather`)
- **Level 5**: Consistent method (weather-fetcher skill)
- **Level 6**: Clean context (weather-agent works in isolation, preloads the skill)

But right now these pieces exist independently. The command and the agent aren't wired together. In Level 7, we'll connect them into a single pipeline: command triggers agent, agent uses skill, result flows back cleanly.

---

## Graduation Criteria

You're ready for Level 7 when you can:

- [ ] Create an agent in `.claude/agents/`
- [ ] Explain what context isolation means (own whiteboard)
- [ ] Use the `skills:` field to preload a skill into an agent
- [ ] Restrict an agent's tools with the `tools:` field
- [ ] Enable `memory: project` and observe persistence
- [ ] Explain when to use an agent vs. a command vs. a skill

---

## Going Deeper

- [Agents Reference](../../best-practice/claude-subagents.md) — all 16 frontmatter fields, 5 official agent types
- [Agents Implementation](../../implementation/claude-subagents-implementation.md) — working examples
- [Agent Memory](../../reports/claude-agent-memory.md) — deep dive on persistence
- [Agent vs Command vs Skill](../../reports/claude-agent-command-skill.md) — decision tree
- [Tips: Agents section](../../tips/README.md) — 4 curated tips

---

## Next Up

[Level 7: Orchestration](../day7/README.md) — Wire commands, agents, and skills into a single end-to-end pipeline.
