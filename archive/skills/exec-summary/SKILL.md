---
name: exec-summary
description: >
  Generate an executive summary from a longer document, report, or set of
  findings. Surfaces key decisions, risks, and recommended actions for
  decision-makers. Use when a detailed document needs a one-page leadership
  summary. Invoke with /exec-summary followed by the document content or
  key findings to summarize.
allowed-tools: Read
---

When this skill is invoked, produce an executive summary from the provided source material. An executive summary is not a compression of the full document — it is a decision-enabling document written for people who will act on the findings without reading the full source.

## Before Writing

1. **Identify the audience**: Who is the executive or decision-maker? What decisions do they need to make? What do they already know?
2. **Identify the document type**: Report, research findings, project proposal, audit, strategic plan?
3. **Identify the key decisions or actions**: What should the reader do differently after reading this? If nothing, the summary has no purpose.
4. **Identify the most critical risk or finding**: What is the single most important thing the reader must not miss?

## Executive Summary Principles

**Lead with the conclusion**: Executives read the first paragraph. The most important finding, decision, or recommendation goes first — not last.

**Decision-forcing, not informing**: Every paragraph should either inform a decision or support a recommendation. Background context earns its place only if the decision cannot be understood without it.

**One-page discipline**: An executive summary that requires scrolling has failed. If there are more than 5 key points, the summary is a document — not a summary.

**Acknowledge risk**: Leadership needs to know what could go wrong, not just what the plan is. Surface the top risks honestly.

**Avoid jargon from the source**: The executive summary is often read by people outside the domain of the full document. Write for a smart generalist.

## Output Format

```markdown
# Executive Summary: [Document Title]

**Date**: [date]
**Source document**: [Title or description]
**Prepared for**: [Audience/role]

---

## Situation

[1–2 sentences on the context or problem that prompted this document. Why does it exist? What decision or event created it?]

---

## Key Findings

1. **[Finding headline]** — [1–2 sentence explanation of the finding and why it matters]
2. **[Finding headline]** — [1–2 sentence explanation]
3. **[Finding headline]** — [1–2 sentence explanation]
[Maximum 5 findings — if there are more, prioritize the ones that inform the recommendation]

---

## Recommendation

[One clear recommendation. Who should do what, and by when. If there are options, state the recommendation and acknowledge the alternative in one sentence.]

---

## Key Risks

- **[Risk]**: [Brief impact statement and mitigation if one exists]
- **[Risk]**: [Brief impact statement]

---

## Decisions Required

[What does the reader need to decide or approve? State each decision explicitly with a deadline if applicable.]

[If no decisions required: "No decisions required — this summary is for information."]

---

## Next Steps

1. [Specific action — owner — timeframe]
2. [Specific action — owner — timeframe]
```

## Quality Bar

A good executive summary:
- Can be read in under 3 minutes
- The most important finding is the first thing the reader sees
- Does not require reading the full document to act on
- Contains exactly one clear recommendation
- Surfaces risks alongside the recommendation — not separate from it
- Ends with unambiguous next steps

## Common Mistakes to Avoid

**Building up to the recommendation**: Start with the answer, then support it. Never make the executive read to the end to find out what you recommend.

**Comprehensive instead of selective**: An executive summary of a 50-page report should not have 40 bullet points. Select the 3–5 most important findings and leave the rest in the full document.

**Passive tense obscuring ownership**: "It is recommended that..." → "We recommend that the CFO approve the budget reallocation by May 20."

**Missing the "so what"**: A finding without an implication is just information. "Conversion rate dropped 12% MoM" is a finding. "Conversion rate dropped 12% MoM, which puts Q2 revenue target at risk unless we address the checkout abandonment issue identified in Section 3" is an insight.
