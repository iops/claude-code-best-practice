# Level 5 — Skills

[Back to Tutorial Index](../README.md) | [Previous: Level 4](../day4/README.md)

---

## What You'll Learn

- What skills are and how they differ from commands
- How Claude automatically discovers and uses skills
- How to create a skill with supporting files
- When to use skills vs. commands

---

## Prerequisites

- Completed [Level 4](../day4/README.md) — you can create and run custom commands

---

## The Concept: Training Manuals

In Level 4, you built a `/get-weather` command — a shortcut *you* trigger. But what if Claude could figure out *on its own* when to use a particular capability?

Think of it like this: A **command** is giving someone a walkie-talkie and saying "when I radio you, do this." A **skill** is handing them a training manual and saying "whenever you encounter *this kind of situation*, follow these instructions."

You don't have to radio them — they recognize the situation and know what to do.

### The key difference

| | Command | Skill |
|--|---------|-------|
| **Who triggers it?** | You (type `/name`) | Claude (auto-discovers by intent) |
| **Where does it live?** | `.claude/commands/name.md` | `.claude/skills/name/SKILL.md` |
| **When is it used?** | Only when you invoke it | Whenever the situation matches |
| **Structure** | Single file | Folder (can include reference files) |

---

## How Auto-Discovery Works

When Claude starts a session, it sees a list of available skills — specifically their `name` and `description`. It's like seeing a bookshelf with labeled spines. Claude reads the spine (description), and when your request matches, it pulls the book off the shelf and follows it.

This means the `description` field is critical. It's the trigger — the thing that tells Claude "this skill is relevant right now."

```markdown
---
name: weather-fetcher
description: "Use when the user asks about current weather or temperature for any city"
---

Instructions here...
```

With that description, if you say "What's the temperature in Tokyo?", Claude recognizes the match and loads the skill — without you typing any command.

---

## Creating Your First Skill

Skills live in folders under `.claude/skills/`:

```
my-project/
  .claude/
    skills/
      weather-fetcher/
        SKILL.md              ← The main instructions (required)
        reference.md          ← Extra details Claude can consult (optional)
        examples.md           ← Example inputs/outputs (optional)
```

### The SKILL.md file

Here's a minimal skill:

```markdown
---
name: weather-fetcher
description: "Use when the user asks about current weather, temperature, or forecast"
---

# Weather Fetcher

## Instructions

To get current weather data:

1. Use the Open-Meteo API (free, no API key needed)
2. Endpoint: https://api.open-meteo.com/v1/forecast
3. Parameters:
   - latitude and longitude of the city
   - current=temperature_2m,relative_humidity_2m
4. Report temperature in Celsius
5. Format: "City: 24C, Humidity: 65%"
```

Now when anyone asks "how hot is it in Dubai?", Claude auto-discovers this skill, loads the instructions, and follows the exact method every time. No command needed — no `/` prefix.

---

## Supporting Files

Skills can include additional files that provide context:

### reference.md — Technical details

```markdown
# Weather API Reference

## City Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Dubai | 25.276987 | 55.296249 |
| London | 51.507351 | -0.127758 |
| Tokyo | 35.689487 | 139.691711 |

## API Response Format

The API returns JSON with `current.temperature_2m` and `current.relative_humidity_2m`.
```

### examples.md — Input/Output samples

```markdown
# Examples

## Input: "What's the weather in Dubai?"
Output: "Dubai: 34C, Humidity: 45%, Clear skies"

## Input: "Temperature in London"
Output: "London: 12C, Humidity: 78%, Overcast"
```

These files help Claude be more precise without cramming everything into a single SKILL.md.

---

## Frontmatter Fields

Skills support several configuration options:

| Field | What it does | Example |
|-------|-------------|---------|
| `name` | Display name and slash command | `weather-fetcher` |
| `description` | When to auto-invoke (the trigger!) | `"Use when user asks about weather"` |
| `user-invocable` | Whether it shows in the `/` menu | `true` (default) or `false` |
| `allowed-tools` | Tools allowed without permission prompts | `Bash, Read` |
| `model` | AI model to use | `haiku`, `sonnet` |
| `context` | Run in isolated context? | `fork` |

### `user-invocable: false`

Sometimes you want a skill that Claude uses automatically but that *you* never need to trigger directly. Setting `user-invocable: false` hides it from the `/` menu. This is useful for skills that only agents need (we'll cover agents in Level 6).

---

## Skills vs. Commands: When to Use Which

| Scenario | Use a... | Why |
|----------|----------|-----|
| "I want to type a shortcut" | Command | Explicit trigger |
| "Claude should just know how to do this" | Skill | Auto-discovery |
| "The team needs a consistent workflow" | Command | Everyone types the same `/name` |
| "I want to embed knowledge Claude can tap into" | Skill | Triggered by intent, not muscle memory |
| "I want to pass arguments each time" | Command | Commands handle `$ARGUMENTS` naturally |
| "This should always work the same way" | Skill | Description ensures consistent matching |

In practice, many workflows use **both**: a command as the entry point, with skills providing the know-how.

---

## Hands-On Exercise

**Step 1:** Create a skill folder:
```bash
mkdir -p .claude/skills/greeting-generator
```

**Step 2:** Ask Claude to create the skill file:
```
Create a file at .claude/skills/greeting-generator/SKILL.md with:

---
name: greeting-generator
description: "Use when the user asks for a greeting, welcome message, or ice-breaker"
---

# Greeting Generator

Generate creative, contextual greetings. Rules:
1. Match the tone to the context (formal for business, casual for friends)
2. Include the current day of the week
3. Keep it to 2 sentences maximum
4. Never use generic phrases like "I hope this finds you well"
```

**Step 3:** Start a fresh session and test auto-discovery:
```bash
claude
```
```
I need a welcome message for my team's Monday morning Slack channel
```

Claude should auto-discover the greeting-generator skill (the description matches your intent) and follow its rules — without you typing any command.

**Step 4:** Now test that it *doesn't* trigger when irrelevant:
```
What files are in this directory?
```

The greeting skill shouldn't activate for this request — the description doesn't match.

**Step 5:** Add a reference file for extra context:
```
Create .claude/skills/greeting-generator/examples.md with 3 example greetings for different contexts (Monday morning, Friday wrap-up, new team member)
```

**Step 6:** Study a real skill. Read the weather-fetcher in this repo:
```
Read .claude/skills/weather-fetcher/SKILL.md and explain how it works
```

---

## The Weather Thread

Our progression so far:
- **Level 1**: Unpredictable answers
- **Level 3**: Consistent format (CLAUDE.md rules)
- **Level 4**: Consistent trigger (`/get-weather`)
- **Level 5**: Consistent method (skill with exact API instructions)

The weather-fetcher skill ensures Claude always uses the Open-Meteo API with the right coordinates and format. But it still runs in your main conversation — filling your whiteboard with API call details. In Level 6, we'll wrap it in an **agent** that works in its own isolated context.

---

## Graduation Criteria

You're ready for Level 6 when you can:

- [ ] Create a skill in `.claude/skills/name/SKILL.md`
- [ ] Write a `description` that triggers auto-discovery
- [ ] Test that the skill activates on matching intent
- [ ] Add supporting files (reference.md, examples.md)
- [ ] Explain the difference between skills and commands

---

## Going Deeper

- [Skills Reference](../../best-practice/claude-skills.md) — all 15 frontmatter fields, 6 official skills
- [Skills Implementation](../../implementation/claude-skills-implementation.md) — working examples
- [Skills in Monorepos](../../reports/claude-skills-for-larger-mono-repos.md) — discovery in large projects
- [Tips: Skills section](../../tips/README.md) — 9 curated tips on skill design

---

## Next Up

[Level 6: Agents](../day6/README.md) — Create specialist workers that operate in their own isolated context, keeping your main conversation clean.
