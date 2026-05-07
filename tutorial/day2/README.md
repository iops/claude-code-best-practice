# Level 2 — Context Management

[Back to Tutorial Index](../README.md) | [Previous: Level 1](../day1/README.md)

---

## What You'll Learn

- What the "context window" is and why it matters
- How to check how much space you've used
- When and how to clear, compact, or start fresh
- How to resume a previous conversation

---

## Prerequisites

- Completed [Level 1](../day1/README.md) — you can have a conversation with Claude Code

---

## The Concept: Claude's Working Memory

Think of Claude's context window like a **whiteboard in a meeting room**. Everything you say, everything Claude reads, every file it looks at — it all gets written on this whiteboard. The whiteboard is large (about 1 million tokens, roughly 750,000 words), but it's not infinite.

Here's the problem: as the whiteboard fills up, things get crowded. Claude has to scan through more and more content to find what's relevant. Research shows that quality starts to degrade around **40% full** — not because Claude "forgets," but because there's too much noise competing for attention.

### The Three Zones

```
┌─────────────────────────────────────────────┐
│  0-40%    FRESH ZONE                        │
│           Claude is sharp, focused           │
├─────────────────────────────────────────────┤
│  40-70%   DRIFT ZONE                        │
│           Quality subtly degrades            │
│           Claude may "forget" early context  │
├─────────────────────────────────────────────┤
│  70-100%  COMPRESSION ZONE                  │
│           System auto-compacts older msgs    │
│           Significant quality loss           │
└─────────────────────────────────────────────┘
```

### What fills up context?

- Every message you type
- Every message Claude responds with
- Every file Claude reads (a 500-line file uses ~500 lines of context)
- Tool calls and their results (searches, terminal commands)
- System instructions (CLAUDE.md, rules — we'll cover these in Level 3)

---

## Your Toolkit for Managing Context

Claude Code gives you several tools to manage your whiteboard:

### `/context` — Check the whiteboard

Type `/context` during a conversation to see how full your context is. It shows a percentage and a visual bar. This is your dashboard — check it periodically, especially during long sessions.

### `/compact` — Summarize and clear

When your whiteboard is getting full, `/compact` tells Claude to summarize the conversation so far, then wipe the board and write just the summary. You keep the key points without all the noise.

**Pro tip**: You can give `/compact` a focus hint — `/compact focus on the weather API work` — and it will prioritize keeping that information in the summary.

### `/clear` — Start fresh

If you want a completely clean slate (empty whiteboard), use `/clear`. This removes everything — the conversation is gone. Use this when you're switching to a completely different task.

### `/rewind` — Undo the last exchange

Made a mistake? Asked something that produced a huge, unhelpful response that ate up context? `/rewind` removes the last exchange (your message + Claude's response) from the whiteboard.

### Starting a new session

You can also exit Claude Code entirely (type `/quit` or press `Ctrl+D`) and start a fresh session. Each new session starts with a clean whiteboard.

---

## Resuming Previous Work

Sometimes you want to come back to where you left off. Claude Code can do this:

### `claude --continue`

Opens your most recent conversation exactly where you left off. The entire history is back on the whiteboard. Useful when you stepped away but weren't done.

### `claude --resume`

Shows you a list of recent sessions and lets you pick which one to continue. Helpful when you've had several conversations and want to return to a specific one.

### When to resume vs. start fresh

| Situation | Best choice |
|-----------|-------------|
| Stepped away for lunch, same task | `--continue` |
| Want to reference yesterday's work | `--resume` and pick the session |
| Starting a completely new task | Fresh session (just type `claude`) |
| Context was >50% when you left | Fresh session + re-explain briefly |

---

## Hands-On Exercise

Let's see context management in action using the weather example:

**Step 1:** Start a new Claude Code session:
```bash
claude
```

**Step 2:** Ask Claude to read a few files (this fills context):
```
Read the files in this project's tutorial directory and summarize what each one covers
```

**Step 3:** Check your context usage:
```
/context
```
Notice how much space those file reads consumed.

**Step 4:** Now compact with a focus:
```
/compact focus on the weather system
```
Claude summarizes the conversation, keeping weather-related info. Notice the context usage drops.

**Step 5:** Verify the summary kept what matters:
```
What do you remember about the weather system?
```
Claude should recall the weather-related content but may have lost unrelated details. That's the trade-off — space for relevance.

**Step 6:** Exit and resume:
```
/quit
```
Then in your terminal:
```bash
claude --continue
```
You're back where you left off.

---

## The Weather Thread

Remember from Level 1 — you asked Claude "what's the weather?" and got an unpredictable answer? Now imagine asking that same question 50 times in one session. Each question and answer fills the whiteboard. By the 30th time, Claude is in the "drift zone" — its responses might become less focused or start repeating itself.

This is why, in later levels, we'll build a **command** that triggers a focused workflow rather than relying on repeated prompting. Better architecture means less context waste.

---

## Graduation Criteria

You're ready for Level 3 when you can:

- [ ] Explain what the context window is (in your own words)
- [ ] Use `/context` to check how full your session is
- [ ] Use `/compact` to summarize and free up space
- [ ] Use `/clear` to start a clean slate
- [ ] Resume a previous session with `claude --continue`
- [ ] Explain why long sessions degrade quality

---

## Going Deeper

- [CLI Startup Flags](../../best-practice/claude-cli-startup-flags.md) — all session flags (`--continue`, `--resume`, `--print`)
- [Usage & Rate Limits](../../reports/claude-usage-and-rate-limits.md) — understanding `/usage` and plan limits
- [Tips: Context section](../../tips/README.md) — 5 curated tips on context management
- [Tips: Session management](../../tips/README.md) — 6 tips on session workflows

---

## Next Up

[Level 3: Memory & Rules](../day3/README.md) — Give Claude a persistent rulebook that survives between sessions.
