# Level 7 — Orchestration

[Back to Tutorial Index](../README.md) | [Previous: Level 6](../day6/README.md)

---

## What You'll Learn

- How commands, agents, and skills wire together into a pipeline
- The two skill patterns: preloaded vs. directly invoked
- How to trace a complete flow end-to-end
- How to build your own orchestration

---

## Prerequisites

- Completed [Level 6](../day6/README.md) — you can create agents with preloaded skills

---

## The Concept: Assembly Line

In the previous levels you built individual pieces:
- **Command** — the button you press (Level 4)
- **Skill** — the training manual (Level 5)
- **Agent** — the specialist worker (Level 6)

Now it's time to connect them into an **assembly line**:

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   COMMAND   │ ───→ │    AGENT    │ ───→ │    SKILL    │
│  (trigger)  │      │  (worker)   │      │  (output)   │
│             │      │             │      │             │
│ /weather    │      │ fetches     │      │ creates     │
│ orchestrator│      │ temperature │      │ SVG card    │
└─────────────┘      └─────────────┘      └─────────────┘
     YOU                 ISOLATED              RESULT
   press this          context work         beautiful output
```

Think of it like a **restaurant**:
- **Command** = the menu item you order ("Pasta Carbonara")
- **Agent** = the chef (works in the kitchen, out of your sight)
- **Skill** = the recipe (precise instructions the chef follows)

You order from the menu. The chef follows the recipe. Your plate arrives beautifully presented. You never see the messy kitchen.

---

## The Weather System: A Complete Example

This repository has a working orchestration you can run. Here are the four components:

### 1. The Command (entry point)

File: `.claude/commands/weather-orchestrator.md`

```
/weather-orchestrator
```

This is what you type. The command's instructions tell Claude to:
1. Ask you: Celsius or Fahrenheit?
2. Dispatch to the weather-agent
3. Take the result and invoke the weather-svg-creator skill

### 2. The Agent (isolated worker)

File: `.claude/agents/weather-agent.md`

The agent has `weather-fetcher` preloaded as a skill. It:
1. Reads the preloaded skill instructions
2. Calls the Open-Meteo API for Dubai
3. Returns the temperature to the command

### 3. The Preloaded Skill (agent knowledge)

File: `.claude/skills/weather-fetcher/SKILL.md`

This skill is preloaded into the agent via the `skills:` frontmatter field. It never runs independently — it's baked into the agent's context as reference material. It tells the agent *exactly* which API to call and how.

### 4. The Invoked Skill (output creator)

File: `.claude/skills/weather-svg-creator/SKILL.md`

This skill is invoked *after* the agent returns. The command tells Claude to invoke it directly (using the Skill tool). It takes the temperature data and creates a beautiful SVG weather card.

---

## Two Skill Patterns

This example demonstrates both ways skills can be used:

| Pattern | Example | How it works |
|---------|---------|-------------|
| **Preloaded** (agent skill) | weather-fetcher | Listed in agent's `skills:` field. Loaded automatically into agent context. Never invoked separately. |
| **Directly invoked** (skill) | weather-svg-creator | Called explicitly via the Skill tool during the workflow. Runs in its own turn. |

**When to use which:**
- **Preloaded**: When the agent needs the knowledge to do its job (like a reference card)
- **Directly invoked**: When a distinct step needs to happen after the agent finishes (like rendering output)

---

## The Flow (Step by Step)

Here's exactly what happens when you type `/weather-orchestrator`:

```
1. You type: /weather-orchestrator
2. Command loads → asks: "Celsius or Fahrenheit?"
3. You answer: "Celsius"
4. Command dispatches to weather-agent (Agent tool)
   └→ Agent starts in ISOLATED context
   └→ Agent reads preloaded weather-fetcher skill
   └→ Agent calls Open-Meteo API
   └→ Agent returns: "34" (temperature)
5. Command receives result from agent
6. Command invokes weather-svg-creator skill (Skill tool)
   └→ Skill creates SVG weather card
   └→ Skill writes to orchestration-workflow/weather.svg
   └→ Skill updates orchestration-workflow/output.md
7. Command reports success to you
```

Total context used on YOUR whiteboard: your command + the final result. All the API work happened in the agent's isolated context.

---

## Hands-On Exercise

**Step 1:** Run the real orchestration. Start Claude in this project:
```bash
cd /path/to/claude-code-best-practice
claude
```

**Step 2:** Invoke the weather orchestrator:
```
/weather-orchestrator
```

When asked, choose Celsius. Watch the flow happen — you'll see Claude dispatch to the agent, receive the result, and then create the SVG.

**Step 3:** Check the output:
```
Read orchestration-workflow/output.md
```

You should see the formatted weather report and a reference to the generated SVG file.

**Step 4:** Trace the flow. Read each component in order:
```
Read .claude/commands/weather-orchestrator.md
```
```
Read .claude/agents/weather-agent.md
```
```
Read .claude/skills/weather-fetcher/SKILL.md
```
```
Read .claude/skills/weather-svg-creator/SKILL.md
```

For each one, identify: What triggers it? What does it produce? Where does the output go?

**Step 5:** Read the architecture documentation:
```
Read orchestration-workflow/orchestration-workflow.md
```

This shows the complete flow diagram and design decisions.

**Step 6 (Challenge):** Build your own mini-orchestration. Think of a workflow like:
- `/daily-brief` → agent fetches 3 data points → skill formats them as a summary
- `/project-status` → agent reads git log → skill creates a status report
- `/meeting-prep` → agent gathers agenda items → skill formats talking points

Pick one and sketch out what your command, agent, and skill would look like. You don't need to build the whole thing — just write the markdown files and test.

---

## Common Orchestration Patterns

| Pattern | Command does | Agent does | Skill does |
|---------|-------------|-----------|-----------|
| **Fetch & Render** | Asks user preferences | Fetches data from APIs | Renders output (SVG, PDF, etc.) |
| **Research & Report** | Accepts a topic | Searches, reads, analyzes | Formats as a report |
| **Review & Fix** | Accepts a file path | Reads code, finds issues | Applies fixes, writes PR description |
| **Collect & Summarize** | Accepts a time range | Gathers entries from multiple sources | Creates a digest |

---

## The Weather Thread: Complete!

The full progression:

| Level | What we added | Result |
|-------|--------------|--------|
| 1 | Just asked Claude | Unpredictable |
| 3 | CLAUDE.md rules | Consistent format |
| 4 | `/get-weather` command | Consistent trigger |
| 5 | weather-fetcher skill | Consistent method |
| 6 | weather-agent | Clean context |
| **7** | **Orchestration** | **Full pipeline: trigger → work → beautiful output** |

You've built the complete weather reporting system. The next levels add *operational* capabilities: automation that triggers without you being present.

---

## Graduation Criteria

You're ready for Level 8 when you can:

- [ ] Run `/weather-orchestrator` and see it complete end-to-end
- [ ] Explain the three layers: command (trigger), agent (worker), skill (knowledge/output)
- [ ] Distinguish preloaded skills from directly invoked skills
- [ ] Trace the flow from command → agent → skill → output
- [ ] Identify where context isolation happens in the pipeline

---

## Going Deeper

- [Orchestration Docs](../../orchestration-workflow/orchestration-workflow.md) — complete system documentation with flow diagram
- [Why Harness Matters](../../reports/why-harness-is-important.md) — architectural rationale for this pattern
- [Agent Teams](../../implementation/claude-agent-teams-implementation.md) — multiple agents coordinating (Level 9 preview)

---

## Next Up

[Level 8: Hooks & Automation](../day8/README.md) — Add automatic actions that fire on lifecycle events, like sounds, logging, or safety checks.
