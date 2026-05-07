# Level 3 — Memory & Rules (CLAUDE.md)

[Back to Tutorial Index](../README.md) | [Previous: Level 2](../day2/README.md)

---

## What You'll Learn

- How to give Claude persistent instructions that survive between sessions
- What CLAUDE.md is and how to write one
- How to split instructions into focused rule files
- How the loading hierarchy works

---

## Prerequisites

- Completed [Level 2](../day2/README.md) — you understand context and sessions

---

## The Concept: A Persistent Rulebook

In Level 2, you learned that Claude's "whiteboard" gets erased between sessions. But what if you want Claude to *always* follow certain rules — like "always use Celsius for temperature" or "write in British English"?

Think of it like leaving a **laminated instruction card** on someone's desk. Every morning when they sit down (new session), the first thing they see is that card. They read it and follow it — without you having to repeat yourself.

That laminated card is a file called `CLAUDE.md`.

---

## What is CLAUDE.md?

`CLAUDE.md` is a plain text file you put in the root of your project folder. When you start Claude Code in that folder, Claude automatically reads this file first — before you say anything. It's like a briefing document.

Here's a simple example:

```markdown
# CLAUDE.md

## Project Overview
This is a marketing analytics dashboard for the sales team.

## Rules
- Always respond in bullet points, not paragraphs
- Use metric units (Celsius, kilometers, kilograms)
- When creating files, use kebab-case (like-this-name.md)
```

That's it. A text file with instructions. Claude will follow these rules for every conversation in this folder.

### Where does it go?

Put `CLAUDE.md` in the **root of your project** — the top-level folder where you run `claude`:

```
my-project/
  CLAUDE.md          ← Claude reads this automatically
  src/
  docs/
  ...
```

---

## Creating Your First CLAUDE.md

You can write one by hand, or let Claude help you:

### Option A: Let Claude generate it

Run this command inside your project folder:
```
/init
```

Claude will look at your project and generate a CLAUDE.md with sensible defaults. You can then edit it to add your own rules.

### Option B: Write it yourself

Create a file called `CLAUDE.md` in your project root. Write whatever rules you want Claude to follow. Keep it under 200 lines — longer files waste context space (remember Level 2?) and Claude is less likely to follow every instruction if there are too many.

---

## Splitting Rules Into Separate Files

As your rules grow, one big CLAUDE.md file gets unwieldy. Claude Code supports a `.claude/rules/` folder where you can split instructions into focused files:

```
my-project/
  CLAUDE.md                    ← Always loaded (keep short!)
  .claude/
    rules/
      writing-style.md         ← Always loaded (no paths: field)
      data-analysis.md         ← Always loaded
      chart-formatting.md      ← Only loaded when touching chart files
```

Each file in `.claude/rules/` is a small, focused instruction set.

### Always-loaded vs. lazy-loaded rules

By default, every file in `.claude/rules/` is loaded into *every* session (just like CLAUDE.md). But you can make a rule load **only when relevant** by adding a special header:

```markdown
---
paths: "**/*.chart.*"
---

# Chart Formatting Rules

- Always use the company color palette: #2563EB, #7C3AED, #DC2626
- Label all axes
- Include data source attribution
```

The `---` block at the top is called **frontmatter** (think of it as metadata about the file). The `paths:` line tells Claude: "only load this rule when I'm working with files that match `*.chart.*`". This saves context space — why load chart rules when you're editing a text document?

**What is frontmatter?** It's a small section at the very top of a file, surrounded by `---` lines. It contains structured settings in a format called YAML (basically `key: value` pairs). You'll see this pattern in Commands and Skills too (Levels 4-5).

---

## The Loading Hierarchy

Claude Code looks for instructions in multiple places, in this order:

```
1. CLAUDE.md in your project root         (always loaded)
2. .claude/rules/*.md files               (loaded based on paths: filter)
3. CLAUDE.md in parent folders            (if your project is inside another project)
4. ~/.claude/CLAUDE.md                    (your personal global rules)
```

Rules higher in the list take priority. This means:
- Your **project rules** override your personal global rules
- **Specific path-filtered rules** are additive (they add to, not override, the base rules)
- Parent folder CLAUDE.md files provide defaults for sub-projects (useful in large codebases)

---

## Hands-On Exercise

Let's add a rule to the weather example:

**Step 1:** Navigate to this project (or any project folder):
```bash
cd /path/to/your/project
claude
```

**Step 2:** Try asking about weather without any rules:
```
What's the weather in Dubai?
```
Notice Claude might respond in any format — Fahrenheit, Celsius, long paragraphs, etc.

**Step 3:** Exit Claude (`/quit`) and create a CLAUDE.md:

Create a file called `CLAUDE.md` in your project root with this content:
```markdown
# CLAUDE.md

## Rules
- Always report temperatures in Celsius
- Keep responses under 3 sentences
- End weather reports with the data source used
```

**Step 4:** Start Claude again and ask the same question:
```bash
claude
```
```
What's the weather in Dubai?
```
Notice Claude now follows your rules — Celsius, concise, attributes the source.

**Step 5:** Create a path-filtered rule. Make the rules folder:
```
Create a file at .claude/rules/weather-responses.md with this content:

---
paths: "**/weather*"
---

# Weather Response Rules
- Format temperatures as: "24C (feels like 22C)"
- Always include humidity percentage
- Use emoji for conditions (sun, cloud, rain, snow)
```

Ask Claude to create this file for you, or create it manually in your file system.

**Step 6:** Verify it loads only when relevant. Ask Claude:
```
What rules are you following right now?
```

Claude will list the active rules — you should see your CLAUDE.md rules, plus the weather rules only if you're touching weather-related files.

---

## The Weather Thread

In Level 1, Claude's weather answers were unpredictable. Now with CLAUDE.md rules, we've added *consistency* — every response follows the same format. But we're still relying on Claude to figure out *how* to get weather data. In Level 4, we'll create a **command** that standardizes the trigger too.

---

## Best Practices

| Do | Don't |
|----|-------|
| Keep CLAUDE.md under 200 lines | Stuff everything into one file |
| Use `.claude/rules/` for topic-specific rules | Repeat the same rule in multiple places |
| Use `paths:` to avoid loading irrelevant rules | Make every rule always-loaded |
| Write rules as clear imperatives | Write vague suggestions |
| Update rules when you notice Claude misbehaving | Assume Claude will "figure it out" |

---

## Graduation Criteria

You're ready for Level 4 when you can:

- [ ] Create a CLAUDE.md file that Claude follows automatically
- [ ] Explain what happens when Claude starts a new session (it reads CLAUDE.md first)
- [ ] Create a rule file in `.claude/rules/` with `paths:` frontmatter
- [ ] Explain the loading hierarchy (project > parent > global)
- [ ] Keep instructions concise (under 200 lines)

---

## Going Deeper

- [Memory & CLAUDE.md Reference](../../best-practice/claude-memory.md) — full loading mechanics, monorepo patterns
- [This repo's own CLAUDE.md](../../CLAUDE.md) — a real-world example
- [Tips: CLAUDE.md section](../../tips/README.md) — 8 curated tips on writing effective rules

---

## Next Up

[Level 4: Commands](../day4/README.md) — Create reusable shortcuts that trigger specific workflows with a single slash command.
