---
name: swot-analysis
description: >
  Build a rigorous SWOT analysis grounded in real market data, customer
  evidence, and competitive context. Use for strategic planning, business
  reviews, or investment decisions. Invoke with /swot-analysis followed by
  the company, product, or initiative to analyze and any available context.
allowed-tools: Read, WebFetch
---

When this skill is invoked, produce a SWOT analysis grounded in evidence. A good SWOT is not an internal brainstorm — it is a structured assessment of comparative advantage and strategic context, backed by data.

## Before Analyzing

Gather or clarify:
1. **Subject**: Company, product line, initiative, or market position?
2. **Strategic question**: What decision does this SWOT support? (Market entry, resource allocation, competitive response, investor presentation?)
3. **Context and evidence available**: Customer feedback, market data, competitive intel, financial metrics, internal assessments?
4. **Competitive reference**: Who are the main competitors? SWOT strengths and weaknesses are relative to alternatives, not absolute.

## SWOT Quality Standards

### Strengths
Must be relative to competitors, not internal claims:
- "Strong engineering team" is not a strength unless demonstrably better than alternatives — with evidence
- "First-mover advantage" is only a strength if it translates to a defensible moat (switching costs, network effects, data)
- Evidence required: metrics, customer quotes, product differentiation that is difficult to replicate

### Weaknesses
Must be honest about strategic constraints:
- "Limited brand awareness" is only meaningful if you can quantify the impact on pipeline or conversion
- "Small team" is only a weakness if it limits a specific strategic capability
- Weaknesses that are obvious and shared by all players in a category are not strategic weaknesses

### Opportunities
Must be specific and time-bounded:
- "Growing AI market" is not an opportunity — too broad and shared by everyone
- "The [specific segment] is underserved and growing 28% YoY with no dominant player below $50K ACV" is an opportunity
- Include why the window is open now and how long it is likely to remain open

### Threats
Must distinguish probability and urgency:
- "Competition" is not a threat — name the specific competitive move or market shift
- Assess both probability (likely vs. unlikely) and magnitude (existential vs. manageable)
- Distinguish threats requiring active response from risks to monitor

## Output Format

```markdown
# SWOT Analysis: [Company/Product/Initiative]

**Date**: [today]
**Strategic question**: [What decision or review does this support?]
**Analyst**: [Name/Role]

---

## Strengths
*(Relative to competitors — what do we do better that is difficult to replicate?)*

| Strength | Evidence | Competitive Comparison | Durability |
|----------|----------|----------------------|------------|
| [Strength] | [Specific evidence] | [How does this compare to Competitor X?] | [High/Med/Low — why?] |

**Top 1–2 strengths to build strategy on**: [Most defensible advantages]

---

## Weaknesses
*(Honest assessment of strategic constraints — what limits us competitively?)*

| Weakness | Evidence | Strategic Impact | Priority to Address |
|----------|----------|-----------------|---------------------|
| [Weakness] | [Evidence or observation] | [How does this limit growth/defense?] | High/Med/Low |

**Critical weaknesses requiring attention**: [Weaknesses that are strategic liabilities, not just gaps]

---

## Opportunities
*(Specific, time-bounded market openings — why now?)*

| Opportunity | Market Evidence | Why Now | Window Duration | Estimated Value |
|-------------|----------------|---------|-----------------|----------------|
| [Opportunity] | [Data/trends] | [What is opening the window?] | [Short/Medium/Long] | [Rough sizing] |

---

## Threats
*(Specific risks requiring assessment — probability and magnitude)*

| Threat | Probability | Magnitude | Time Horizon | Recommended Response |
|--------|------------|-----------|-------------|---------------------|
| [Threat] | High/Med/Low | High/Med/Low | [Near/Mid/Long term] | Monitor / Mitigate / Respond |

---

## Strategic Synthesis

**Most critical interaction**: [Which SWOT factors interact most powerfully? e.g., "Strength X + Opportunity Y = strategic priority"]

**Key strategic question surfaced**: [What question does this SWOT raise that needs to be answered?]

**Recommended strategic posture**: [In 2–3 sentences: given this SWOT, what should the company/product prioritize?]
```

## Quality Bar

A good SWOT:
- Every strength and weakness is comparative, not absolute
- Every opportunity names the market condition creating it and why it's time-limited
- Every threat has a probability and magnitude assessment
- Includes a synthesis section that draws strategic conclusions — not just four lists
- Can withstand the challenge "how do you know this?" for every entry

## Common Mistakes to Avoid

**Internal reflection as SWOT**: Listing things you like about yourself as strengths and things you worry about as weaknesses produces a feelings audit, not a strategic assessment.

**Generic entries**: "Strong team," "growing market," "competition" — these apply to every company and tell you nothing. Be specific or cut the entry.

**Missing the synthesis**: Four lists of bullet points is a brainstorm. Adding the synthesis section — how strengths and opportunities interact, and which weaknesses and threats are most urgent — turns it into a strategic tool.

**No evidence**: A SWOT entry without a supporting data point or customer quote is an opinion. Opinions can be argued; evidence is harder to dismiss.
