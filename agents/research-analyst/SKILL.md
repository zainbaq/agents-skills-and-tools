# Research Analyst Sub-Agent

## What It Does

Synthesizes research across multiple sources into clear, actionable intelligence. Performs competitive analysis, builds research briefs, and produces audience-calibrated summaries. Knows how to weight different source types, surface conflicts between findings, and separate facts from inferences. Read-only — the analyst interprets, never modifies source documents.

## When to Invoke

- "Synthesize these three market reports into a single brief"
- "Analyze the competitive landscape for our product category"
- "Summarize the key findings from these customer interviews"
- "What are the gaps in our current market research?"
- "Build a competitive comparison of these five vendors"
- "Write an executive summary of this research"
- "What do these user reviews tell us about the biggest pain points?"

## How to Install

```bash
# Project-scoped
cp agents/research-analyst/research-analyst.md .claude/agents/research-analyst.md

# User-scoped (available in all projects)
cp agents/research-analyst/research-analyst.md ~/.claude/agents/research-analyst.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the research-analyst agent to synthesize the three market reports in
/docs/research/ and produce an executive brief for our board meeting.
Focus on competitive positioning and market sizing.
```

```
Analyze G2 and Capterra reviews for [Competitor A] and [Competitor B] and
identify the top 5 unmet customer needs we could address.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Strong reasoning for multi-source analysis |
| Tools | Read, Glob, Grep, WebFetch | Reads local docs; fetches external sources |
| Memory | project | Retains key findings and source map across sessions |
| Color | blue | Consistent with analytical/advisory agents |

## Key Distinctions

This agent **synthesizes, does not summarize**. It identifies themes across sources, weights evidence by source quality, and explicitly flags when sources conflict. It will never blend contradictory findings into a false consensus — a gap or contradiction in the research is treated as a finding, not a problem to paper over.
