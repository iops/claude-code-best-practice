# Level 8 — Hooks & Automation

[Back to Tutorial Index](../README.md) | [Previous: Level 7](../day7/README.md)

---

## What You'll Learn

- What hooks are and how they differ from commands/skills
- The lifecycle events you can hook into
- How to create your first hook
- Practical use cases: sounds, logging, safety guards

---

## Prerequisites

- Completed [Level 7](../day7/README.md) — you understand the orchestration pipeline

---

## The Concept: Tripwires and Sensors

Everything you've built so far requires a *decision*: you choose to type a command, or Claude decides to use a skill. But what about things that should happen **automatically**, every single time, without anyone deciding?

Think of **hooks** like the sensors in a smart home:
- Motion sensor at the front door → light turns on (you didn't flip a switch)
- Smoke detector → alarm sounds (you didn't press a button)
- Thermostat drops below 20C → heating starts (nobody decided)

Hooks in Claude Code work the same way. They're scripts that **automatically run** when specific events happen — before a tool runs, after a session ends, when Claude is about to execute a command, etc.

### The key difference from skills and commands

| | Command | Skill | Hook |
|--|---------|-------|------|
| **Trigger** | You type it | Claude's judgment | Lifecycle event (automatic) |
| **Code type** | Markdown prompt | Markdown prompt | Shell script (real code) |
| **Runs where** | Claude's context | Claude's context | Your computer (outside Claude) |
| **Can block actions?** | No | No | Yes! |

Hooks are **deterministic code** — they always run the same way, unlike Claude which has creative variability. They run *outside* Claude, on your actual computer.

---

## Lifecycle Events

Claude Code has events throughout its lifecycle that you can hook into:

| Event | When it fires | Common use |
|-------|--------------|-----------|
| `PreToolUse` | Before Claude uses any tool | Block dangerous tools, log actions |
| `PostToolUse` | After a tool finishes | Play sounds, validate output |
| `Stop` | When Claude finishes responding | Notification sounds, summaries |
| `Notification` | When Claude sends a notification | Desktop alerts |
| `UserPromptSubmit` | When you press Enter | Validate input, track time |
| `SessionStart` | When a session begins | Set up environment |
| `SessionEnd` | When a session ends | Clean up, log session |
| `SubagentStart` | When an agent is dispatched | Track agent usage |
| `SubagentStop` | When an agent finishes | Log results |

There are 16 total events — these are the most commonly used.

---

## How Hooks Are Configured

Hooks live in your `.claude/settings.json` file. Here's a minimal example:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'A file was written!' >> /tmp/claude-log.txt"
          }
        ]
      }
    ]
  }
}
```

Let's break this down:

- **`PostToolUse`** — the event (after a tool finishes)
- **`matcher: "Write"`** — only fire when the *Write* tool was used (not every tool)
- **`command`** — the shell command to run on your computer

### Matchers (filtering events)

Not every event needs to trigger your hook. Matchers let you filter:

```json
{
  "matcher": "Write",
  "hooks": [...]
}
```

This hook only fires when the Write tool is used. Without a matcher, it fires for *every* tool.

You can also use pattern matching:
- `"Bash"` — only Bash tool
- `"Edit"` — only file edits
- `"*"` — everything (same as no matcher)

---

## Your First Hook: A Simple Logger

Let's create a hook that logs every tool Claude uses:

**Step 1:** Open or create `.claude/settings.json` in your project. If it doesn't exist, create it:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): Tool used\" >> /tmp/claude-tool-log.txt"
          }
        ]
      }
    ]
  }
}
```

**Step 2:** Start a session and do something that uses tools:
```bash
claude
```
```
List the files in this directory
```

**Step 3:** Check the log:
```bash
cat /tmp/claude-tool-log.txt
```

You should see entries for each tool Claude used (Glob, Bash, etc.).

---

## Practical Use Cases

### 1. Safety guard — block destructive commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'BLOCKED: rm -rf is not allowed' >&2; exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

When a `PreToolUse` hook exits with code 1 (error), Claude is **blocked** from using that tool. This prevents accidental `rm -rf` commands.

### 2. Sound notification when done

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ]
  }
}
```

On macOS, this plays a sound when Claude finishes a response. Useful when you're working in another window and want to know when Claude is done.

### 3. Auto-format after file writes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

Automatically runs a code formatter after Claude writes a file.

---

## This Repository's Hook System

This project has a sophisticated hook setup you can study:

```
.claude/
  hooks/
    scripts/hooks.py       ← Main hook handler (Python)
    config/hooks-config.json    ← Shared config
    config/hooks-config.local.json  ← Personal overrides (git-ignored)
    sounds/                ← Audio files for different events
      stop/
      notification/
      pretooluse-git-committing/
```

It plays different sounds for different events — a chime when Claude finishes, a specific sound when a git commit happens, notification sounds for alerts. It's configured in `.claude/settings.json` and processes events through a Python script.

---

## Disabling Hooks

Sometimes hooks get in the way (especially while debugging). You can disable them:

**Disable all hooks** — add to `.claude/settings.local.json`:
```json
{
  "disableAllHooks": true
}
```

**Disable a specific hook** — set its `disabled` field in the hooks config.

---

## Hands-On Exercise

**Step 1:** Create a simple Stop hook. Add to your `.claude/settings.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '✓ Claude finished at '$(date '+%H:%M:%S') >> /tmp/claude-sessions.txt"
          }
        ]
      }
    ]
  }
}
```

**Step 2:** Start a session, ask Claude something, and check the log:
```bash
claude
```
```
What is 2 + 2?
```
```
/quit
```
```bash
cat /tmp/claude-sessions.txt
```

**Step 3:** Add a PreToolUse guard. Add this to your hooks config:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm|delete|drop'; then echo 'BLOCKED: destructive command' >&2; exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

**Step 4:** Test the guard:
```bash
claude
```
```
Run the command: rm -rf /tmp/test
```

Claude should be blocked from executing this.

**Step 5:** Study this repo's hook system:
```
Read .claude/hooks/scripts/hooks.py and explain the main event handling logic
```

---

## The Weather Thread

Adding hooks to our weather system:
- **PostToolUse hook** on the weather agent → logs every weather fetch with timestamp
- **Stop hook** after the orchestrator completes → plays a notification sound
- **PreToolUse hook** → prevents the weather agent from accidentally writing to files other than `orchestration-workflow/`

Hooks are the "operational layer" — they don't change *what* the system does, but add safety, observability, and polish.

---

## Graduation Criteria

You're ready for Level 9 when you can:

- [ ] Explain what hooks are (automatic scripts triggered by lifecycle events)
- [ ] Configure a hook in `.claude/settings.json`
- [ ] Create a Stop hook that logs when Claude finishes
- [ ] Create a PreToolUse hook that blocks a specific command
- [ ] Explain how hooks differ from skills (deterministic code vs. AI-guided)
- [ ] Know how to disable hooks when they get in the way

---

## Going Deeper

- [Hooks README](../../.claude/hooks/HOOKS-README.md) — comprehensive reference with all 16 events
- [Settings Reference](../../best-practice/claude-settings.md) — full hooks configuration options
- [Tips: Hooks section](../../tips/README.md) — 5 curated tips on hook design

---

## Next Up

[Level 9: Production Workflows](../day9/README.md) — Agent teams, scheduled tasks, MCP servers, and real-world workflow patterns.
