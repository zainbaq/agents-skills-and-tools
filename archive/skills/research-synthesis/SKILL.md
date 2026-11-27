---
name: research-synthesis
description: >
  Synthesize findings across multiple research sources into a unified brief
  with themes, conflicts, and implications. Use when combining research from
  multiple documents, reports, or sources into coherent insights. Invoke with
  /research-synthesis followed by the research sources to synthesize.
allowed-tools: Read, WebFetch
---

When this skill is invoked, synthesize the provided research materials into a unified brief. Synthesis is not summarization — it identifies cross-cutting themes, weights evidence by source quality, and explicitly flags where sources conflict.

## Before Synthesizing

1. **Map the sources**: How many sources are there? What type is each (primary research, secondary report, news, expert opinion)?
2. **Identify the research question**: What decision or question should this synthesis help answer?
3. **Note obvious biases or gaps**: Is any major perspective missing from the provided sources?

## Source Quality Hierarchy

Weight findings accordingly when sources conflict:

1. **Primary research** (original surveys, interviews, experiments, first-party data) — highest weight
2. **Peer-reviewed research / industry reports with stated methodology** — high weight
3. **Analyst reports** (Gartner, Forrester, McKinsey) — medium weight; often lag indicators
4. **Journalism and news** — useful for events, low weight for analytical claims
5. **Marketing content / vendor claims** — use for positioning signals only; low weight for factual claims
6. **AI-generated or uncited content** — flag and verify before including

## Synthesis Process

1. **Extract themes**: Read all sources and identify 3–7 cross-cutting themes that appear across multiple sources.

2. **Aggregate evidence per theme**: For each theme, list the supporting evidence from each source. Note agreement and disagreement.

3. **Resolve or flag conflicts**: When sources disagree, do not average the findings. Explain the conflict and assess which finding is more credible — or state that the conflict cannot be resolved with available sources.

4. **Identify gaps**: What important questions remain unanswered? What evidence is missing?

5. **Draw implications**: What does each theme mean for the decision or context this synthesis serves?

## Output Format

```markdown
# Research Synthesis: [Topic]

**Research question**: [What question does this synthesis answer?]
**Sources synthesized**: [List with type and date for each]
**Date**: [today]

---

## Source Map

| Source | Type | Date | Quality Weight | Notes |
|--------|------|------|---------------|-------|
| [Title] | [Primary/Secondary/etc.] | [Year] | High/Med/Low | [Any bias or limitation to note] |

---

## Key Themes

### Theme 1: [Theme Name]

**Finding**: [What the research shows across multiple sources]

**Supporting evidence**:
- [Source A]: [specific finding or quote]
- [Source B]: [specific finding or quote]

**Conflicts**: [If any sources disagree — state both findings and explain]

**Implication**: [What this means for the research question]

---

### Theme 2: [Theme Name]
[Same structure]

---

[Continue for all themes]

---

## Conflicts and Unresolved Questions

| Topic | Finding A | Source A | Finding B | Source B | Assessment |
|-------|-----------|---------|-----------|---------|------------|
| [Topic] | [Finding] | [Source] | [Conflicting finding] | [Source] | [Which is more credible and why, or "unresolved"] |

---

## What the Research Cannot Tell Us

- [Gap 1 — what question remains unanswered and why it matters]
- [Gap 2]

---

## Summary and Implications

[3–5 bullets — the most important actionable conclusions from the synthesis]
```

## Quality Bar

A good research synthesis:
- Identifies themes that span multiple sources — not a sequential summary of each source
- Explicitly states the quality weight of each source type
- Flags conflicts without blending them into false consensus
- Distinguishes what the evidence shows from what it implies
- Ends with what the research cannot tell us — gaps are findings

## Common Mistakes to Avoid

**Source-by-source summary**: "Source A says X. Source B says Y. Source C says Z." This is not synthesis. Synthesis asks: "Across these sources, what do we know about [theme]?"

**False consensus from conflicting data**: "Studies show that 45–72% of buyers..." averaging two different studies is dishonest. State both numbers with their sources.

**Stating inferences as facts**: "This means companies will..." is an inference. "This suggests companies may..." is honest. Label interpretations.

**Ignoring source quality**: Treating a vendor whitepaper with the same weight as peer-reviewed research produces unreliable synthesis.
