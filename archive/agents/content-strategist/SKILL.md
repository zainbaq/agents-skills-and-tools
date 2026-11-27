# Content Strategist Sub-Agent

## What It Does

Plans and produces social media content, multi-platform content calendars, campaign copy, and brand voice guidance. Understands the algorithmic and cultural differences between LinkedIn, Instagram, X, TikTok, and Threads — never recommends cross-posting identical content. Built from the patterns that actually drive engagement, not just content creation theory.

## When to Invoke

- "Build a 30-day content calendar for our LinkedIn and Instagram"
- "Adapt this blog post into posts for each platform"
- "Write 5 LinkedIn posts about our product launch"
- "What should we post this week?"
- "Create a social media campaign brief for our Q3 launch"
- "Audit our content strategy and suggest improvements"
- "Write captions for these product photos"

## How to Install

```bash
# Project-scoped
cp agents/content-strategist/content-strategist.md .claude/agents/content-strategist.md

# User-scoped (available in all projects)
cp agents/content-strategist/content-strategist.md ~/.claude/agents/content-strategist.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the content-strategist agent to build a 30-day LinkedIn content calendar
for a B2B SaaS company targeting operations leaders. Content pillars are:
thought leadership, product education, and social proof. Post 4x per week.
```

```
Take this blog post [paste content] and adapt it into native posts for
LinkedIn, Instagram, and X. Keep our brand voice casual but expert.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Fast enough for high-volume content production |
| Tools | Read, WebFetch | Reads brand guides; fetches competitor content for reference |
| Memory | project | Accumulates brand voice, content pillar, and audience patterns |
| Color | orange | Distinct from technical agents in the Claude Code task list |

## Key Distinctions

The content-strategist understands **platform-native behavior** — not just formatting differences, but what each platform's algorithm rewards, what its culture expects, and how audiences behave there. It will refuse to produce identical content for multiple platforms and will always ask about brand voice before writing at scale.
