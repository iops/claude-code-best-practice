# Claude Code: Zero to Hero

A self-paced learning path that takes you from first install to building orchestrated AI workflows. Each level builds on the last, using a single running example — a **weather reporter** — that evolves from a bare question into a fully automated system.

---

## Who This Is For

You're technically minded but not necessarily a software engineer. Maybe you're a product manager, data analyst, designer, or content strategist. You're comfortable using a computer but terms like "YAML frontmatter" or "subagent" might be new. That's perfect — we'll explain everything as we go.

---

## The Learning Path

| Level | Title | What You'll Build | Time |
|-------|-------|-------------------|------|
| 0 | [Install & Authenticate](day0/README.md) | Claude Code running on your machine | 10 min |
| 1 | [First Conversation](day1/README.md) | Your first chat with Claude | 15 min |
| 2 | [Context Management](day2/README.md) | Understanding Claude's "working memory" | 15 min |
| 3 | [Memory & Rules](day3/README.md) | A persistent rulebook (CLAUDE.md) | 15 min |
| 4 | [Commands](day4/README.md) | A reusable `/get-weather` shortcut | 15 min |
| 5 | [Skills](day5/README.md) | An auto-triggered weather fetcher | 15 min |
| 6 | [Agents](day6/README.md) | A specialist weather reporter | 15 min |
| 7 | [Orchestration](day7/README.md) | A full Command + Agent + Skill pipeline | 20 min |
| 8 | [Hooks & Automation](day8/README.md) | Automatic actions on lifecycle events | 15 min |
| 9 | [Production Workflows](day9/README.md) | Agent teams, scheduling, and integrations | 20 min |

---

## The Weather Reporter Story

Throughout this guide, you'll build a weather reporting system one layer at a time:

```
Level 1:  "Hey Claude, what's the weather?"     → unpredictable answer
Level 4:  /get-weather                          → consistent trigger
Level 5:  skill auto-discovers intent           → reliable API data
Level 6:  agent runs in isolation               → clean, focused work
Level 7:  command orchestrates everything       → SVG card output
Level 9:  scheduled to run every morning        → fully automated
```

By the end, you'll understand not just *how* to build this, but *when* to use each layer — and how to apply the same patterns to your own workflows.

---

## How to Use This Guide

1. **Go in order.** Each level assumes you completed the previous one.
2. **Do the exercises.** Reading isn't enough — the hands-on steps are where learning happens.
3. **Check the graduation criteria.** Each level has a checklist. If you can tick every box, move on.
4. **Go deeper when curious.** Each level links to reference docs for those who want more detail.

---

## Quick Reference

Once you've completed the guide, these are your go-to references:

| Topic | Reference |
|-------|-----------|
| Commands | [best-practice/claude-commands.md](../best-practice/claude-commands.md) |
| Skills | [best-practice/claude-skills.md](../best-practice/claude-skills.md) |
| Agents | [best-practice/claude-subagents.md](../best-practice/claude-subagents.md) |
| Settings | [best-practice/claude-settings.md](../best-practice/claude-settings.md) |
| Memory | [best-practice/claude-memory.md](../best-practice/claude-memory.md) |
| MCP Servers | [best-practice/claude-mcp.md](../best-practice/claude-mcp.md) |
| Tips (83 curated) | [tips/README.md](../tips/README.md) |
