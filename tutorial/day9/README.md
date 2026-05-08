# Level 9 — Production Workflows

[Back to Tutorial Index](../README.md) | [Previous: Level 8](../day8/README.md)

---

## What You'll Learn

- How to run multiple Claude sessions as a team
- How to schedule recurring tasks
- What MCP servers are and how to connect external tools
- Real-world workflow patterns used in production

---

## Prerequisites

- Completed [Level 8](../day8/README.md) — you understand hooks and automation

---

## The Concept: From Single Player to Multiplayer

Everything until now has been one Claude session doing one thing at a time. But real workflows often need:

- **Parallel work** — two specialists working simultaneously
- **Recurring tasks** — something that runs every morning without you
- **External integrations** — Claude talking to Slack, Gmail, databases, or browsers

This level covers the patterns that take Claude Code from a personal assistant to a **production system**.

---

## Part 1: Agent Teams

### What are agent teams?

Agent teams are multiple Claude Code sessions running simultaneously, coordinating through a shared task list. Think of it like a **project team** where each person has their own desk (context) but they share a Kanban board.

```
┌──────────────────────┐   ┌──────────────────────┐
│  Claude Session 1    │   │  Claude Session 2    │
│  "Frontend Agent"    │   │  "Backend Agent"     │
│                      │   │                      │
│  Working on: UI      │   │  Working on: API     │
│  components          │   │  endpoints           │
└──────────┬───────────┘   └──────────┬───────────┘
           │                          │
           └──────────┬───────────────┘
                      │
              ┌───────┴───────┐
              │  Shared Task  │
              │     List      │
              └───────────────┘
```

### How to set up agent teams

You can use tmux (a terminal multiplexer) to run multiple sessions side by side:

```bash
# Split your terminal into two panes
tmux new-session -d -s agents
tmux split-window -h
tmux send-keys -t agents:0.0 'claude --agent-name "Frontend" --task-file shared-tasks.md' Enter
tmux send-keys -t agents:0.1 'claude --agent-name "Backend" --task-file shared-tasks.md' Enter
tmux attach -t agents
```

Each session picks tasks from the shared file, works on them independently, and marks them done. They don't step on each other's toes because each works in its own context.

### When to use agent teams

| Scenario | Single session | Agent team |
|----------|---------------|-----------|
| Write one feature | Yes | Overkill |
| Refactor frontend + backend simultaneously | Too slow | Yes |
| Research + implementation in parallel | Yes (but messy) | Cleaner |
| Review code while writing tests | Can't multitask | Yes |

---

## Part 2: Scheduled Tasks

### What are scheduled tasks?

Scheduled tasks are Claude Code sessions that run on a timer — like a cron job, but powered by AI. No human triggers them.

### The `/loop` skill

The simplest way to schedule recurring work:

```
/loop 5m check if any new issues have been created in this repo
```

This tells Claude to check every 5 minutes. The task keeps running in the background.

### The `/schedule` skill

For more formal scheduling (like "every morning at 9am"):

```
/schedule "0 9 * * *" generate a daily status report from yesterday's git commits
```

The format `"0 9 * * *"` is cron syntax:
- `0` — minute 0
- `9` — hour 9
- `* * *` — every day of month, every month, every day of week

Common patterns:
| Schedule | Cron | Meaning |
|----------|------|---------|
| Every morning at 9 | `0 9 * * *` | Daily standup prep |
| Every hour | `0 * * * *` | Health checks |
| Monday mornings | `0 9 * * 1` | Weekly summaries |
| Every 30 minutes | `*/30 * * * *` | Frequent monitoring |

### Practical scheduled task examples

```
/schedule "0 9 * * 1-5" summarize the git log from yesterday and post to #dev-updates
/schedule "0 8 * * *" check the weather in Dubai and save to orchestration-workflow/weather.svg
/loop 10m check if the deploy pipeline has finished and notify me
```

---

## Part 3: MCP Servers (External Integrations)

### What is MCP?

MCP stands for **Model Context Protocol**. It's a way to give Claude access to external tools and data sources. Think of it like installing **plugins** that let Claude talk to the outside world.

Without MCP, Claude can only:
- Read/write files in your project
- Run terminal commands
- Search the web (if configured)

With MCP, Claude can additionally:
- Browse websites and click buttons (Playwright)
- Read your Google Drive documents
- Search Slack messages
- Query databases
- Interact with any API that has an MCP server

### How to configure MCP

MCP servers are configured in `.mcp.json` at your project root:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-playwright"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

Each entry:
- **Key** (`playwright`) — the server name
- **command** — how to start it
- **args** — arguments to pass

### Popular MCP servers

| Server | What it does | Use case |
|--------|-------------|----------|
| Playwright | Browser automation | Test web apps, fill forms, screenshot pages |
| Context7 | Library documentation | Look up API docs for any framework |
| Google Drive | Read/search docs | Access team documents |
| Slack | Read/send messages | Check channels, post updates |
| PostgreSQL | Query databases | Analyze data, check records |

### Setting up your first MCP server

The easiest to start with is **Context7** (library documentation). Create `.mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

Now when you ask Claude about any library ("how do I use React hooks?"), it can fetch the *latest* documentation rather than relying on training data.

---

## Part 4: Development Workflows

### The Foundational Workflow: Explore → Plan → Code → Commit

Before any of the more elaborate workflows below, there's the **base pattern** every Claude Code workflow extends — Anthropic's official four-phase methodology:

```
EXPLORE   →   PLAN   →   CODE   →   COMMIT
(read)        (design)   (do)       (capture)
```

| Phase | What you do | How you trigger it |
|-------|-------------|--------------------|
| **Explore** | Ask Claude to read files / research — *no edits yet* | "Read X, don't write code" or use the `Explore` subagent |
| **Plan** | Get a written approach to critique before any code is touched | `Shift+Tab` twice to enter Plan Mode, or `/ultraplan` |
| **Code** | Execute the approved plan | Exit Plan Mode after reviewing the plan |
| **Commit** | Capture the change in focused, reviewable commits | One commit per logical change (or per file, per project rules) |

**Why this matters:** The most expensive Claude mistakes happen when you skip Explore and Plan. Reviewing a 200-line diff is much harder than reviewing a 5-line plan. Catching the misunderstanding *before* code exists is the entire point.

Full reference: [Explore → Plan → Code → Commit](../../best-practice/claude-explore-plan-code-commit.md).

The workflows below are all **specializations** of this base pattern.

### The RPI Workflow (Research → Plan → Implement)

RPI is essentially Explore → Plan → Code → Commit with Explore renamed to Research and Code+Commit collapsed into Implement — plus dedicated specialist agents per phase. This repository ships RPI as a complete workflow:

```
/rpi:research   → Agent researches the problem, gathers context
/rpi:plan       → Agent creates a detailed implementation plan
/rpi:implement  → Agent executes the plan step by step
```

Each phase has specialized agents:
- **Research**: technical-cto-advisor, documentation-analyst
- **Plan**: product-manager, senior-software-engineer
- **Implement**: code-reviewer (validates after each step)

This is a "training wheels" workflow — it prevents Claude from jumping into code before understanding the problem.

### The Cross-Model Workflow

A pattern that uses different AI models for different strengths:

```
PLAN (Claude Opus — best reasoning)
  → QA REVIEW (GPT-5 — different perspective)
  → IMPLEMENT (Claude Opus — best coding)
```

Using multiple models catches blind spots — one model reviews another's work.

### Choosing a workflow

| Your task | Recommended workflow |
|-----------|---------------------|
| Small bug fix | Explore → Plan → Code → Commit (the base pattern, lightweight) |
| New feature | RPI (research first, then plan, then build) |
| Large refactor | Agent teams (parallel work) |
| Recurring report | Scheduled task |
| Multi-model validation | Cross-model workflow |

---

## Hands-On Exercise

**Step 1:** Set up Context7 MCP. Create `.mcp.json` in your project:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

Start Claude and ask: "Using context7, look up the latest React useEffect documentation." Claude should fetch live docs.

**Step 2:** Try a recurring task:
```
/loop 2m tell me the current time
```

Watch it execute twice (it will fire every 2 minutes). Then cancel it when you're satisfied it works.

**Step 3:** Explore the RPI workflow in this repo:
```
Read development-workflows/rpi/rpi-workflow.md and explain the three phases
```

**Step 4:** Explore the agent teams documentation:
```
Read implementation/claude-agent-teams-implementation.md and summarize how coordination works
```

**Step 5 (Advanced):** If you have tmux installed, try running two Claude sessions side by side:
```bash
tmux new-session -d -s team
tmux split-window -h -t team
tmux send-keys -t team:0.0 'claude' Enter
tmux send-keys -t team:0.1 'claude' Enter
tmux attach -t team
```

Give each session a different task in the same project and watch them work in parallel.

---

## The Weather Thread: Full Circle

Our weather system now has every layer:

| Level | Layer | What it adds |
|-------|-------|-------------|
| 1 | Prompting | "What's the weather?" |
| 3 | Rules | Consistent format (CLAUDE.md) |
| 4 | Command | `/get-weather` shortcut |
| 5 | Skill | Exact API method |
| 6 | Agent | Isolated context |
| 7 | Orchestration | Full pipeline |
| 8 | Hooks | Sound notifications, logging |
| **9** | **Scheduling** | **`/schedule "0 8 * * *"` — runs every morning automatically** |

From "hey what's the weather?" to a fully automated, orchestrated, monitored weather reporting system — built entirely from markdown files and configuration.

---

## Graduation Criteria

You've completed the Zero to Hero journey when you can:

- [ ] Explain agent teams and when parallel sessions make sense
- [ ] Use `/loop` or `/schedule` to create a recurring task
- [ ] Configure an MCP server in `.mcp.json`
- [ ] Describe the foundational Explore → Plan → Code → Commit workflow and how RPI extends it
- [ ] Choose the right pattern for a given task size/complexity
- [ ] Explain the full stack: CLAUDE.md → Commands → Skills → Agents → Hooks → Orchestration

---

## Going Deeper

- [Agent Teams Implementation](../../implementation/claude-agent-teams-implementation.md) — full coordination patterns
- [Scheduled Tasks](../../implementation/claude-scheduled-tasks-implementation.md) — recurring task setup
- [MCP Reference](../../best-practice/claude-mcp.md) — all MCP configuration options
- [Explore → Plan → Code → Commit](../../best-practice/claude-explore-plan-code-commit.md) — Anthropic's foundational workflow that all others extend
- [RPI Workflow](../../development-workflows/rpi/rpi-workflow.md) — complete workflow with 8 specialized agents
- [Cross-Model Workflow](../../development-workflows/cross-model-workflow/cross-model-workflow.md) — multi-model validation
- [Settings Reference](../../best-practice/claude-settings.md) — 60+ settings, permissions, sandbox config

---

## What's Next?

You've completed the full learning path. Here's where to go from here:

1. **Build your own workflow** — Pick a repetitive task in your work and automate it using the patterns from Levels 4-9.
2. **Explore the tips** — [83 curated tips](../../tips/README.md) organized by topic, from creators and community experts.
3. **Study real implementations** — The `implementation/` folder has production-ready examples.
4. **Watch expert sessions** — The `videos/` folder has transcripts from Claude Code creators and power users.
5. **Join the community** — Share your workflows, learn from others, contribute back.

Congratulations — you've gone from zero to hero.
