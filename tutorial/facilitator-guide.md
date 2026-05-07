# Facilitator Guide: Teaching Claude Code over Zoom

[Back to Tutorial Index](README.md)

---

## Overview

A 3-session live teaching plan for onboarding a non-developer power user to Claude Code. Each session is 45-60 minutes over Zoom with homework between sessions.

**Your pupil**: Technically minded but not a software engineer (PM, analyst, designer, content strategist). Comfortable using a computer but new to terminals and AI coding tools.

**Your goal**: By the end of Session 3, they can build their own Command → Agent → Skill pipeline for a workflow relevant to their actual job.

---

## Before You Start

### Pre-requisites (send 24 hours before Session 1)

Send your pupil these instructions:

> **Prep for our Claude Code session (10 min)**
>
> 1. Install Claude Code: follow the guide for your OS
>    - Mac: `brew install --cask claude-code`
>    - Windows/Linux: see tutorial/day0/
> 2. Run `claude --version` in your terminal — confirm it shows a version number
> 3. Log in: run `claude` and follow the auth prompts
> 4. Think of one repetitive task in your work you'd love to automate
>
> If you get stuck on any step, just note where you got stuck — we'll fix it together.

### Your setup (facilitator)

- [ ] Have this repo open and ready to demo
- [ ] Test that `/weather-orchestrator` runs successfully
- [ ] Have Zoom screen-sharing set up with terminal visible
- [ ] Open a shared note (Google Doc, Notion, or HackMD) for the pupil to reference later
- [ ] Optional: have Excalidraw or Zoom whiteboard ready for Level 7 diagramming

---

## Session 1: Foundation

**Duration**: 50 minutes
**Levels covered**: 1, 2, 3
**Theme**: "Understanding how Claude thinks"

---

### Opening: The Magic Trick (5 min)

**You drive. They watch.**

> "Before we learn how any of this works, let me show you what's possible."

1. Share your screen
2. Run `/weather-orchestrator`
3. Choose Celsius when prompted
4. Show the SVG output in a browser

**Talking point**: "That was one slash command. Behind it: a command triggered an agent, which used a skill to call a weather API, then another skill rendered this SVG. You'll build something like this for your own workflow by Session 3."

**Transition**: "But first — let's start at the very beginning."

---

### Block 1: First Conversation (15 min)

**They drive. You guide.**

Ask them to share their screen.

**Script:**

> "Open your terminal and type `claude`. That's it — you're now talking to an AI coding assistant."

Walk them through:

1. Ask something simple: "What day of the week is it?"
2. Ask something about a file: "What files are in this folder?"
3. Ask something Claude can't reliably do: "What's the weather in Dubai right now?"

**Key teaching moment** (after the weather question):

> "Notice Claude gave you an answer — but did it check a real weather source? Maybe, maybe not. It's unpredictable. We'll fix that over the next sessions."

**Show them essential commands:**
- Type `/help` — see what's available
- Type `/quit` — exit cleanly
- Mention `Ctrl+C` to cancel a response mid-stream

**Check-in question**: "Any questions about what just happened?"

---

### Block 2: Context — The Whiteboard (10 min)

**You drive. They watch.**

> "Claude has a working memory called the *context window*. Think of it like a whiteboard in a meeting room. Everything gets written on it — your messages, Claude's responses, files it reads. Let me show you."

1. Start a fresh session
2. Ask Claude to read 3-4 files: "Read the files in the tutorial/ directory"
3. Run `/context` — show the percentage
4. Point out: "See? Just reading a few files used X% of the whiteboard"
5. Run `/compact` — show the number drop
6. Explain: "It summarized everything and wiped the board. The key info stays, the noise is gone."

**Analogy to reinforce:**

> "Imagine writing notes on a whiteboard for 6 hours straight. Eventually it's so cluttered you can't find anything. `/compact` is like erasing the board and writing just the summary. `/clear` is wiping it completely."

**Quick mention** (don't demo, just tell):
- `claude --continue` resumes your last session
- `claude --resume` lets you pick from recent sessions

---

### Block 3: CLAUDE.md — The Rulebook (15 min)

**They drive. You guide.**

> "Right now, Claude forgets everything between sessions. But what if you want it to *always* follow certain rules? That's what CLAUDE.md does — it's a file Claude reads automatically at the start of every session. Like a laminated card on someone's desk."

**Together:**

1. Have them navigate to one of their real project folders
2. Create a CLAUDE.md together:

> "What are 3 rules you'd want Claude to always follow in this project?"

Help them brainstorm. Prompt if stuck:
- "Should responses be formal or casual?"
- "Are there terms specific to your work it should know?"
- "Any format preferences — bullet points? Short sentences?"

3. Write the file together (they type, you dictate/suggest):

```markdown
# CLAUDE.md

## About This Project
[One sentence about what the project is]

## Rules
- [Rule 1 they chose]
- [Rule 2 they chose]
- [Rule 3 they chose]
```

4. Start Claude, test a rule:
   - "Ask Claude something that would trigger one of your rules. Does it follow it?"

5. Briefly show `.claude/rules/` exists (don't create one yet — that's homework):

> "As your rules grow, you can split them into separate files in a `.claude/rules/` folder. Each file can load only when you're working on matching files. We'll try that in your homework."

---

### Closing & Homework (5 min)

**Recap in shared doc:**
- Context = whiteboard (use `/context`, `/compact`, `/clear`)
- CLAUDE.md = laminated rule card (always loaded)
- Commands we learned: `/help`, `/quit`, `/context`, `/compact`

**Homework** (write in shared doc):

> 1. Use Claude for 3 real tasks this week (anything — don't overthink it)
> 2. Add 2 more rules to your CLAUDE.md as you discover preferences
> 3. Create `.claude/rules/reports.md` (or whatever matches your work) with a `paths:` header
> 4. Bonus: run `/context` periodically and notice how different tasks consume space differently

**Preview**: "Next session we'll build shortcuts that automate your repetitive tasks — commands, skills, and agents."

---

## Session 2: Building Blocks

**Duration**: 55 minutes
**Levels covered**: 4, 5, 6
**Theme**: "Three ways to extend Claude"

---

### Opening: Check-in (5 min)

- "How did the homework go?"
- "Show me your CLAUDE.md — what rules did you add?"
- Troubleshoot any issues they hit
- "Did you notice context filling up?"

---

### Block 1: Commands — Speed Dial (15 min)

**They drive. You guide.**

> "You know how on your phone you can set up shortcuts? One tap and it runs a whole sequence? That's a command. Instead of typing your prompt each time, you save it as a slash command."

**Together — build THEIR command (not the weather one):**

1. Ask: "What's something you do repeatedly? Weekly report? Standup prep? Document review?"
2. Help them design it. Example prompts:
   - PM: "Summarize yesterday's git commits as bullet points for my standup"
   - Analyst: "Read the latest CSV file and give me the top 5 trends"
   - Designer: "Review my component and suggest accessibility improvements"

3. Create the file together:
```bash
mkdir -p .claude/commands
```

4. Write their command (they type):
```markdown
---
description: [What it does — one line]
---

[Their instructions — 2-4 sentences]
```

5. Start Claude, type `/` — find their command in the list
6. Run it. Celebrate when it works.

**Teaching moment:**

> "See how that's now a single `/` away? And because it's a file in your project, you could share this with teammates. They'd get the same command."

**Quick extension** — show `$ARGUMENTS`:

> "You can also make it accept input." Add `argument-hint: "[topic]"` and use `$ARGUMENTS` in the body. Demo once.

---

### Block 2: Skills — The Training Manual (15 min)

**You drive first, then they try.**

> "Commands are shortcuts YOU trigger. But what if Claude could figure out on its own when to use something? That's a skill — it auto-activates when the situation matches."

**Demo the difference (you drive):**

1. Show a skill file — the key is the `description` field:

> "This description is like a label on a reference book's spine. Claude scans these at the start of every session. When your request matches a description, it pulls the book off the shelf."

2. Create a demo skill live:
```
.claude/skills/date-formatter/SKILL.md
```
```markdown
---
name: date-formatter
description: "Use when the user mentions dates, deadlines, or scheduling"
---

# Date Formatter

When formatting dates:
1. Always use format: "Monday, 5 May 2026"
2. Always include the day of the week
3. If a deadline is mentioned, calculate days remaining
```

3. Test it: "My report is due next Friday" — Claude should auto-format the date without you typing any command.

**Now they try:**

4. Ask: "What's something Claude should just *know how to do* in your project without you asking?"
5. Help them create a skill for it. Common ones:
   - "Always format currency as $X,XXX.XX"
   - "When reviewing text, check for brand voice guidelines"
   - "When I mention a client name, look up their info in clients.md"

**Key teaching moment:**

> "Notice you didn't type `/date-formatter`. You just talked naturally, and Claude matched your intent to the skill. That's the difference — commands are buttons, skills are intuition."

---

### Block 3: Agents — The Specialist (15 min)

**You drive the demo. They build after.**

> "Here's the final building block. An agent is a specialist that works in its own separate workspace. It does all the messy research in its own context, then brings back only the clean result."

**Visual explanation (draw or describe):**

> "Imagine your whiteboard (context). If Claude reads 15 files to answer your question, all 15 files go on YOUR whiteboard. But with an agent — it reads those 15 files on ITS whiteboard. You only see the 3-sentence summary it brings back."

**Demo (you drive):**

1. Show before: ask something file-heavy, run `/context` — note the percentage
2. Now show an agent doing the same work — point out context barely changed

**They build:**

3. Together, create an agent for their workflow:
```markdown
---
name: [their-agent-name]
description: "PROACTIVELY use when [their trigger]"
model: haiku
tools: Read, Glob, Grep
maxTurns: 5
---

You are the [Role Name]. Your job:
1. [What to find/analyze]
2. [How to format the result]
3. Keep your response concise — 3-5 bullet points max.
```

4. Test it together. Observe it working.

---

### Closing & Homework (5 min)

**Recap in shared doc:**
- Command = speed dial (you trigger with `/`)
- Skill = training manual (Claude triggers by intent)
- Agent = specialist (isolated context, clean results)

**Homework:**

> 1. Create one more command for a different repetitive task
> 2. Try triggering your skill in 3 different ways — see if the description catches all of them
> 3. Read through `.claude/commands/weather-orchestrator.md` in the tutorial repo — we'll dissect it next time
> 4. Bonus: try adding `memory: project` to your agent and use it twice — does it remember?

**Preview**: "Next time we wire everything together — one command that triggers an agent that uses a skill. The full pipeline."

---

## Session 3: Power User

**Duration**: 55 minutes
**Levels covered**: 7, 8, 9
**Theme**: "Putting it all together"

---

### Opening: Show & Tell (5 min)

- "Show me what you built this week!"
- Have them demo their command, skill, and agent
- Praise what works, gently correct what doesn't
- Quick fix for any issues

---

### Block 1: Orchestration — The Pipeline (20 min)

**Whiteboard first, then code.**

> "You've built the three pieces separately. Now let's see how they chain together."

**Draw the pipeline** (Zoom whiteboard or Excalidraw):

```
[/command] ──triggers──→ [agent] ──uses──→ [skill]
   YOU                   ISOLATED           KNOWLEDGE
 press this            does the work       knows the method
```

**Walk through the weather system (you drive, they follow along):**

1. Open `.claude/commands/weather-orchestrator.md` — "This is the entry point"
2. Open `.claude/agents/weather-agent.md` — "This is the worker"
3. Open `.claude/skills/weather-fetcher/SKILL.md` — "This is the agent's training manual"
4. Open `.claude/skills/weather-svg-creator/SKILL.md` — "This creates the output"

For each file, ask: "What does this do? Where does the output go next?"

**Design THEIR orchestration (whiteboard):**

5. Ask: "What's a workflow in your job that has these three steps: trigger, work, output?"

Help them sketch it:
- What would the command say?
- What would the agent do?
- What knowledge (skill) does the agent need?

Common examples:
- PM: `/sprint-report` → agent reads Jira/Linear → skill formats as executive summary
- Analyst: `/data-check` → agent queries data → skill creates chart description
- Marketer: `/competitor-scan` → agent researches → skill formats comparison table

6. If time: start building the command file together (they can finish as homework)

---

### Block 2: Hooks — The Safety Net (15 min)

**You drive. Fun demo focus.**

> "Everything so far requires a decision — you or Claude choosing to do something. Hooks are different. They're automatic tripwires — code that runs every time a specific event happens."

**Demo 1: The sound hook (fun)**

1. Show `.claude/settings.json` with the Stop hook
2. Run a query — they hear the sound when Claude finishes
3. "Useful when you're multitasking — you know Claude is done without watching"

**Demo 2: The safety guard (impressive)**

1. Add a PreToolUse hook that blocks `rm`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm'; then echo 'BLOCKED' >&2; exit 1; fi"}]
      }
    ]
  }
}
```

2. Ask Claude to delete something — show it getting BLOCKED
3. "This is your safety net. Even if you accidentally ask Claude to do something destructive, the hook catches it."

**Their takeaway:**

> "You probably won't write hooks today. But know they exist. When you think 'I wish something would automatically happen when X' — that's a hook."

---

### Block 3: What's Beyond (10 min)

**You drive. Awareness tour.**

Quick tour of production patterns — no hands-on, just show-and-tell:

**Agent teams** (2 min):
> "You can run multiple Claude sessions in parallel. One works on frontend, one on backend. They share a task list."

Show the tmux split-pane if you have it set up (or show the screenshot/doc).

**Scheduled tasks** (2 min):
> "You can schedule Claude to run without you."

Demo: `/loop 2m tell me the time` — show it fire twice, then cancel.

**MCP servers** (3 min):
> "MCP lets Claude connect to external tools — browsers, databases, Slack, Google Drive."

Show `.mcp.json` briefly. Mention Context7 as the easy starter.

**Workflows** (3 min):
> "There are pre-built workflow systems — like RPI (Research → Plan → Implement) — that give you a structured approach to bigger tasks."

Show the `development-workflows/rpi/` folder briefly.

---

### Closing: The Full Picture (5 min)

**Draw the complete stack:**

```
┌─────────────────────────────────────────┐
│  Level 9: Scheduling, Teams, MCP        │  ← production
├─────────────────────────────────────────┤
│  Level 8: Hooks (automatic actions)     │  ← safety/polish
├─────────────────────────────────────────┤
│  Level 7: Orchestration (pipeline)      │  ← architecture
├─────────────────────────────────────────┤
│  Level 6: Agents (isolated workers)     │  ← delegation
├─────────────────────────────────────────┤
│  Level 5: Skills (auto-triggered)       │  ← knowledge
├─────────────────────────────────────────┤
│  Level 4: Commands (manual trigger)     │  ← shortcuts
├─────────────────────────────────────────┤
│  Level 3: CLAUDE.md (rules)             │  ← consistency
├─────────────────────────────────────────┤
│  Level 2: Context (working memory)      │  ← awareness
├─────────────────────────────────────────┤
│  Level 1: Prompting (just ask)          │  ← foundation
└─────────────────────────────────────────┘
```

> "You don't need all of these for every task. Simple question? Level 1. Repeating yourself? Level 4. Need isolation? Level 6. Full pipeline? Level 7. Start simple, add layers only when you feel the pain."

**Assign "graduation project":**

> "Your final homework: build one real orchestration (command + agent + skill) for something you actually do at work. Next time we talk, show me."

**Share resources:**
- Link to this tutorial repo
- Link to the tips/ folder (83 tips)
- Offer async support: "Ping me if you get stuck"

---

## Facilitator Cheat Sheet

### If they're confused

| Signal | Response |
|--------|----------|
| Glazed eyes during context explanation | Skip the zones diagram. Just say: "Long sessions = worse answers. /compact fixes it." |
| "Why not just use ChatGPT?" | "ChatGPT is a chat box. Claude Code runs in your project — it reads your files, writes code, runs commands. It's an assistant sitting inside your actual work." |
| Can't think of a use case | Offer: standup prep, weekly summary, document review, data formatting, email drafting |
| Frustrated by terminal | Slow down. Type commands for them. Come back to it. |
| "This is too much" | Skip Levels 8-9 entirely. Focus on getting one command + one skill working. That alone is transformative. |

### If they're ahead of schedule

| Signal | Response |
|--------|----------|
| Built homework before the call | Jump ahead — go straight to orchestration |
| Asking about MCP/teams already | Show briefly, then say "Let's nail the foundations first — these will make more sense after" |
| Already writing code | Lean into agents + isolation — that's where their developer instincts add value |

### Timing adjustments

| Scenario | Cut | Keep |
|----------|-----|------|
| Running 10 min over | Cut homework review | Keep hands-on building |
| They're struggling | Cut Level 8-9 awareness tour | Keep their custom command working |
| They're flying | Cut basic explanations | Add the "build your own orchestration" exercise |

---

## After All 3 Sessions

### Follow-up (1 week later)

Send a message:

> "Hey! How's Claude Code going? Have you finished your orchestration project? Happy to do a 15-min check-in if you want to show me what you've built or troubleshoot anything."

### Signs of success

- They've created at least one command they use daily
- They can explain commands vs skills vs agents without your help
- They've customized CLAUDE.md for their real project
- They ask questions like "Could I use a skill for this?" (thinking in patterns)

### Common sticking points at this stage

| Problem | Solution |
|---------|----------|
| "My skill doesn't auto-trigger" | Description doesn't match their phrasing — help them rewrite it |
| "My agent takes forever" | Add `maxTurns: 5` and `model: haiku` |
| "Context fills up too fast" | Show them `/compact` with focus hints, suggest shorter agent responses |
| "I don't know when to use what" | Point to `reports/claude-agent-command-skill.md` decision tree |
