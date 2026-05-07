# Level 4 — Commands

[Back to Tutorial Index](../README.md) | [Previous: Level 3](../day3/README.md)

---

## What You'll Learn

- What slash commands are and why they're useful
- How to create your own custom commands
- How to configure commands with frontmatter
- The difference between built-in and custom commands

---

## Prerequisites

- Completed [Level 3](../day3/README.md) — you understand CLAUDE.md and rules

---

## The Concept: Reusable Shortcuts

You know how on your phone you can set up a shortcut — tap one button and it runs a whole sequence of actions? That's what a **command** is in Claude Code.

Instead of typing "get me the weather for Dubai, use the Open-Meteo API, report in Celsius, keep it to 3 sentences" every single time, you create a command called `/get-weather` and it does all of that with one slash.

Think of it like **speed dial** — you're still making the same call, but you've saved the number.

---

## Built-In Commands

Claude Code comes with many commands already. You've used some:

| Command | What it does |
|---------|-------------|
| `/help` | Shows available commands |
| `/context` | Shows context usage (Level 2!) |
| `/compact` | Compresses context |
| `/clear` | Clears the conversation |
| `/init` | Generates a CLAUDE.md |
| `/doctor` | Diagnoses problems |
| `/quit` | Exits Claude Code |
| `/model` | Switches AI model |

Type `/` during a conversation and you'll see the full list pop up — there are 75+ built-in commands.

---

## Creating Your Own Commands

Custom commands live as markdown files in a `.claude/commands/` folder inside your project:

```
my-project/
  .claude/
    commands/
      get-weather.md       ← This becomes /get-weather
      summarize-doc.md     ← This becomes /summarize-doc
      daily-standup.md     ← This becomes /daily-standup
```

The filename becomes the command name. `get-weather.md` → `/get-weather`.

### Your simplest command

Create a file at `.claude/commands/greet.md`:

```markdown
Say hello to the user, tell them today's date, and wish them a productive day.
```

That's a complete command. One sentence of instructions. When you type `/greet` in a conversation, Claude reads this file and follows the instructions.

---

## Adding Frontmatter (Optional Settings)

Remember frontmatter from Level 3? (The `---` block at the top of a file.) Commands support it too, for extra configuration:

```markdown
---
description: Greet the user with today's date
model: haiku
allowed-tools: Bash
---

Say hello to the user. Run a terminal command to get today's date and include it.
Wish them a productive day.
```

### Key frontmatter fields

| Field | What it does | Example |
|-------|-------------|---------|
| `description` | Shows in the `/` menu to explain the command | `"Fetch Dubai weather"` |
| `model` | Which AI model to use (faster or smarter) | `haiku`, `sonnet`, `opus` |
| `allowed-tools` | What tools Claude can use without asking | `Bash, Read, Write` |
| `arguments` | Accept input from the user | (see below) |

### Commands with arguments

You can make a command accept input. Use `$ARGUMENTS` as a placeholder:

```markdown
---
description: Get weather for a city
argument-hint: "[city name]"
---

Get the current weather for $ARGUMENTS using a web search.
Report in Celsius, keep it to 2 sentences.
```

Now `/get-weather Dubai` passes "Dubai" into the command.

---

## Why Commands Over Plain Prompting?

You might wonder: "Why not just type my prompt each time?" Here's why commands win:

| Plain prompting | Commands |
|----------------|----------|
| You type it fresh each time | One slash and done |
| Slight variations each time | Identical every time |
| Only you know the "recipe" | Your team can use it too (it's a file in the project) |
| Fills context with the full prompt | Fills context the same way, but you don't have to remember it |
| Can't enforce a specific model | Can lock to `haiku` for speed or `opus` for quality |

Commands are especially powerful for **team workflows**. Since they're files in your project, anyone on the team can use `/daily-standup` or `/review-code` without knowing the prompt recipe behind it.

---

## Hands-On Exercise

**Step 1:** Create the commands folder in your project:
```bash
mkdir -p .claude/commands
```

**Step 2:** Create a simple greeting command. Ask Claude:
```
Create a file at .claude/commands/greet.md with this content:
---
description: Greet me and show today's date
model: haiku
---

Say hello! Tell me today's date and day of the week. Keep it to one cheerful sentence.
```

**Step 3:** Start a new Claude session (so it picks up the new file):
```bash
claude
```

**Step 4:** Type `/` and look for your command in the list. Select `/greet` and run it.

**Step 5:** Now create a weather command. Ask Claude:
```
Create a file at .claude/commands/get-weather.md with this content:
---
description: Get current weather for a city
argument-hint: "[city]"
allowed-tools: Bash
---

Get the current weather for $ARGUMENTS.
Use a web search or API call.
Report: city name, temperature in Celsius, conditions, humidity.
Keep it to 3 lines maximum.
```

**Step 6:** Test it:
```
/get-weather Dubai
```

You should get a concise, consistent weather report — same format every time.

**Step 7:** Study a production command. Read the weather orchestrator in this repo:
```
Read the file .claude/commands/weather-orchestrator.md and explain what it does
```

This is a preview of Level 7 — a command that orchestrates an entire workflow.

---

## The Weather Thread

We've now gone from:
- **Level 1**: "What's the weather?" → unpredictable
- **Level 3**: CLAUDE.md rules → consistent format
- **Level 4**: `/get-weather Dubai` → consistent trigger + consistent format

But there's still a gap: the command tells Claude *what* to do, but not *exactly how*. Claude might use different methods each time (web search, cached data, API). In Level 5, we'll create a **skill** with precise instructions for *how* to fetch weather data.

---

## Graduation Criteria

You're ready for Level 5 when you can:

- [ ] Create a custom command in `.claude/commands/`
- [ ] Invoke it using the `/` menu
- [ ] Add frontmatter (description, model, allowed-tools)
- [ ] Create a command that accepts arguments with `$ARGUMENTS`
- [ ] Explain why commands are better than repeating prompts

---

## Going Deeper

- [Commands Reference](../../best-practice/claude-commands.md) — all 15 frontmatter fields, 75 built-in commands
- [Commands Implementation](../../implementation/claude-commands-implementation.md) — real-world examples
- [Tips: Commands section](../../tips/README.md) — 3 curated tips on command design

---

## Next Up

[Level 5: Skills](../day5/README.md) — Create capabilities that Claude discovers and uses automatically, without you typing a command.
