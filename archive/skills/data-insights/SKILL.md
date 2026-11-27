---
name: data-insights
description: >
  Generate a plain-language insight narrative from data, metrics, or a
  dashboard. Produces findings layered by What, So What, Why, and Now What.
  Use when turning raw numbers into stakeholder-ready insights. Invoke with
  /data-insights followed by the data, metrics, or dashboard values to interpret.
allowed-tools: Read
---

When this skill is invoked, produce a structured insight narrative from the provided data. This skill interprets data — it does not compute statistics. Provide the numbers; this skill produces the meaning.

## Before Analyzing

1. **Identify what the data represents**: What metrics are these? What do they measure?
2. **Identify the audience**: Executive (headlines + decision), analyst (full evidence + methodology), or operational team (what to do now)?
3. **Identify the context**: What time period? What is the comparison point (prior period, target, benchmark)?
4. **Identify the business question**: What decision or question should this data help answer?

## Four-Layer Analysis Framework

Work through every data set in this order:

**Layer 1 — What** (observation)
State the facts cleanly and specifically. No interpretation yet. Include absolute numbers, rates, and trends. Example: "Conversion rate dropped from 4.2% to 3.1% between February and March — a 26% relative decline."

**Layer 2 — So What** (significance)
What is notable about this? Is this above or below expectation? Is this trend accelerating or decelerating? How does it compare to target, benchmark, or prior period? Example: "This is the lowest conversion rate in the past 12 months and puts Q2 revenue target at risk if the trend continues."

**Layer 3 — Why** (hypothesis)
What is the most likely business explanation? What events, changes, or patterns could explain this? Label this as hypothesis, not fact — unless the cause is confirmed. Example: "The decline coincides with the checkout flow redesign deployed March 3rd — this is a likely cause requiring investigation."

**Layer 4 — Now What** (action)
What should be done or investigated? What decision does this data support? What would confirm or refute the hypothesis? Example: "Run A/B analysis comparing conversion rates pre/post redesign. Pause rollout to new regions until root cause is identified."

## Analysis Integrity Rules

**Correlation ≠ causation**: When two metrics move together, state correlation — do not imply causation without a mechanism or confirmation.

**Always include rates, not just counts**: "1,200 users clicked" is less useful than "1,200 users clicked (5.8% of page visitors, up from 4.1% last month)."

**Name vanity metrics and flag them**: If a metric looks good but doesn't connect to business outcomes (total impressions, follower count without engagement rate), say so.

**State what the data cannot tell you**: If the available metrics don't explain a trend, say what additional data would be needed to understand it.

**Specify timeframes and comparison bases**: "Up 15%" compared to what? Prior week, prior month, prior year, or target? Always name the comparison.

## Output Format

```markdown
# Data Insights: [Report/Dashboard Name]

**Data period**: [Timeframe covered]
**Prepared for**: [Audience]
**Date**: [today]

---

## Overall Status

[One sentence: is this data telling a good story, a concerning story, or a mixed story?]

---

## Key Insights

### [Metric or Theme Name]

**What**: [Specific numbers — rates, absolutes, trends]
**So what**: [Why this is notable — comparison to target, trend direction, benchmark]
**Why**: [Most likely explanation — label as hypothesis if not confirmed]
**Now what**: [Recommended action or investigation]

---

[Repeat for each key insight — typically 3–5]

---

## Notable Anomalies

| Metric | Expected | Actual | Likely Cause | Recommended Action |
|--------|---------|--------|-------------|-------------------|
| [Metric] | [target/baseline] | [actual] | [hypothesis] | [action] |

---

## What This Data Cannot Tell Us

- [Gap 1 — what additional data would be needed to explain this trend or answer this question]
- [Gap 2]

---

## Summary for [Executive / Team] Audience

[2–4 bullets — if executive: headlines + one recommendation. If team: findings + what to investigate + what to do]
```

## Audience Calibration

**Executive summary**: Lead with the most important finding. 3–5 bullets maximum. One clear recommendation. One key risk or watch item. No methodology detail.

**Analyst/team report**: Full four-layer analysis per metric. Include anomaly table. Flag data gaps and open questions. Include recommended investigations.

**Operational report**: Focus on "Now What" layer. What should the team start, stop, or change based on this data? What is blocked?

## Common Mistakes to Avoid

**Numbers without context**: "CTR is 2.8%" means nothing without a benchmark. "CTR is 2.8%, down from 3.4% last month and below the 3.0% industry benchmark" is a finding.

**Correlation presented as causation**: "Revenue went up the same week we launched the feature" requires the word "coincides with," not "because of."

**Reporting activity instead of outcomes**: "We sent 12,000 emails" is activity. "The email campaign generated 340 MQLs, a 2.8% conversion rate" is an outcome.

**Insight-free summary**: Restating what the dashboard shows is not analysis. Every section should include an interpretation — the "so what" — not just the observation.
