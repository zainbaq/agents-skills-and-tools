# Data Analyst Sub-Agent

## What It Does

Interprets data and produces plain-language insight narratives for stakeholders. Turns metrics, dashboards, and analytical output into structured findings using a four-layer framework: What → So What → Why → Now What. Calibrates depth by audience — executive summaries vs. analyst-level reports. Flags analysis traps like correlation-causation confusion, cherry-picked timeframes, and vanity metrics.

## When to Invoke

- "What does this data tell us?" (paste data)
- "Write an insight summary of this dashboard for our exec team"
- "Explain why churn spiked in March"
- "What are the key takeaways from these campaign metrics?"
- "Interpret these A/B test results"
- "Build a data narrative for our board update"
- "What's missing from this analysis?"

## How to Install

```bash
# Project-scoped
cp agents/data-analyst/data-analyst.md .claude/agents/data-analyst.md

# User-scoped (available in all projects)
cp agents/data-analyst/data-analyst.md ~/.claude/agents/data-analyst.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the data-analyst agent to interpret the Q2 metrics below and produce
an executive summary for the Monday board call. Focus on the churn trend
and what's driving it.

[paste metrics table]
```

```
Here are our social media analytics from last month. Write a plain-language
insight summary identifying what's working, what's declining, and what to
investigate.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Sufficient for narrative generation from provided data |
| Tools | Read, Glob | Reads data files and reports from the project |
| Memory | project | Retains metric definitions, baselines, and prior period context |
| Color | green | Consistent with data and observability-related agents |

## Important Scope Note

This agent interprets and narrates — it does not perform statistical computation (regression, significance testing). Provide the data or computed metrics; the agent produces the narrative, insight, and recommendation layer.
