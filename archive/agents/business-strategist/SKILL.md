# Business Strategist Sub-Agent

## What It Does

Produces rigorous strategic analysis: competitive intelligence, SWOT assessments grounded in market evidence, business cases with options and trade-offs, and market opportunity evaluation. Applies the same analytical rigor used in management consulting engagements — every claim requires evidence, every recommendation comes with its costs acknowledged, every assumption is surfaced. Uses Opus for deeper reasoning on high-stakes decisions.

## When to Invoke

- "Build a business case for entering this market"
- "Do a SWOT analysis of our current position"
- "Analyze the competitive landscape for our product category"
- "Evaluate whether we should build, buy, or partner for this capability"
- "Write a strategic brief for the board on our 2026 priorities"
- "Compare these three strategic options and recommend one"
- "What are the biggest threats to our current strategy?"

## How to Install

```bash
# Project-scoped
cp agents/business-strategist/business-strategist.md .claude/agents/business-strategist.md

# User-scoped (available in all projects)
cp agents/business-strategist/business-strategist.md ~/.claude/agents/business-strategist.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the business-strategist agent to produce a competitive analysis of the
top 3 players in the workflow automation space. We are evaluating whether
to compete directly or find a complementary positioning.
```

```
Build a business case for expanding into the enterprise segment.
Current ACV is $8K targeting SMBs. Include market sizing, investment
required, and three scenario outcomes.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | opus | Complex strategic reasoning benefits from Opus-level depth |
| Tools | Read, WebFetch | Reads internal docs; fetches competitor and market data |
| Memory | none | Fresh analysis each session — no carry-over of prior strategic context |
| Color | red | High-stakes decisions; visually prominent in task list |

## Key Distinctions

Uses **Opus** rather than Sonnet because strategic analysis requires deeper reasoning across complex trade-offs. Memory is intentionally **none** — each strategic engagement should be grounded in current reality, not cached assumptions from prior sessions. Every business case produced includes explicit scenarios (best/base/downside) and names the assumptions that must be true for the recommendation to hold.
