---
name: competitive-analysis
description: >
  Build a structured competitive analysis with positioning matrix, product
  comparison, and strategic gaps. Use when evaluating competitors before a
  product decision, market entry, or strategic planning cycle. Invoke with
  /competitive-analysis followed by the market or product category and the
  competitors to analyze.
allowed-tools: Read, WebFetch
---

When this skill is invoked, produce a structured competitive analysis that surfaces actionable intelligence about competitor positioning, product reality, and strategic gaps. This is not a feature checklist — it is a tool for identifying where to compete and why.

## Before Analyzing

Gather or clarify:
1. **Competitors to analyze**: List 3–6 specific competitors (not "the market" in general)
2. **Your product/company**: What are you comparing against? What is your current positioning?
3. **Strategic question**: What decision does this analysis support? (New market entry, feature prioritization, pricing change, messaging update?)
4. **Evidence available**: Customer reviews, analyst reports, product demos, pricing pages, job postings?

## Five-Vector Analysis Framework

Analyze each competitor on these five dimensions:

**1. Strategic Positioning**
- How do they define their product category? (They may try to create a new one)
- Who is their stated ICP? What company size, role, and industry do they target?
- What problem do they claim to solve?
- What do they say they are NOT (negative positioning)?

**2. Product Reality**
- What does the product actually do well, based on customer evidence?
- Where does it fall short, based on reviews and customer complaints?
- What features are genuinely differentiated vs. parity with the market?
- What is the implementation complexity and time-to-value?

**3. Go-to-Market Motion**
- Sales model: product-led, sales-led, channel, or hybrid?
- Pricing model: per-seat, usage-based, flat, or enterprise custom?
- ACV tier (if discernible): SMB, mid-market, or enterprise?
- Primary acquisition channels: SEO, paid, events, partnerships, PLG?

**4. Strengths Worth Respecting**
- Genuine competitive moats (network effects, data, switching costs, brand)
- Assets that are expensive or time-consuming to replicate
- Customer segments where they are deeply entrenched

**5. Exploitable Weaknesses**
- Underserved customer segments
- Product gaps backed by review evidence
- Pricing model misalignment with buyer preferences
- GTM limitations (e.g., sales-only in a PLG market)

## Output Format

```markdown
# Competitive Analysis: [Market/Category]

**Date**: [today]
**Strategic question**: [Decision this analysis supports]
**Competitors analyzed**: [List]

---

## Individual Competitor Profiles

### [Competitor Name]

**Positioning**: [How they position themselves — their words]
**ICP**: [Who they target]
**Key message**: [Their core value proposition]

**Product strengths** (evidence-based):
- [Strength 1 — source: G2/Capterra/review/demo/case study]
- [Strength 2]

**Product weaknesses** (evidence-based):
- [Weakness 1 — source]
- [Weakness 2]

**GTM motion**: [PLG / Sales-led / Channel + pricing model + ACV tier]
**Moat**: [What makes them sticky or hard to displace]
**Exploitable gap**: [Where they are vulnerable or underserving customers]

---

[Repeat for each competitor]

---

## Positioning Map

[Describe 2 key axes that differentiate the market — e.g., Simplicity vs. Power, SMB vs. Enterprise]

| Company | Axis 1 | Axis 2 | Positioning Note |
|---------|--------|--------|-----------------|
| [Your co] | [Position] | [Position] | [Brief note] |
| [Competitor A] | [Position] | [Position] | [Brief note] |
...

---

## Feature / Capability Comparison

| Capability | [Your co] | [Comp A] | [Comp B] | [Comp C] |
|-----------|-----------|----------|----------|----------|
| [Feature] | ✓ / ✗ / ~ | ✓ / ✗ / ~ | ... | ... |

*(✓ = strong, ~ = partial/limited, ✗ = not available)*

---

## Strategic Gaps and Opportunities

| Gap | Who is underserved | Why competitors don't address it | Strategic opportunity |
|-----|-------------------|--------------------------------|----------------------|
| [Gap in the market] | [Segment] | [Why existing players don't solve it] | [How this could be a wedge] |

---

## Key Takeaways

1. [Most important competitive finding and its implication]
2. [Second most important finding]
3. [Recommended strategic response based on this analysis]
```

## Quality Bar

A good competitive analysis:
- Distinguishes marketing claims from product reality (using customer evidence)
- Identifies genuinely exploitable weaknesses — not just "they're not as good as us"
- Surfaces the segments and use cases competitors underserve
- Includes a positioning map that reveals white space
- Ends with specific strategic implications, not just descriptions

## Common Mistakes to Avoid

**Feature checklist as strategy**: A table of ✓ and ✗ is useful context but is not competitive analysis. The insight is in understanding why certain capabilities exist and what customer need they serve.

**Dismissing competitors**: "They're overpriced and clunky" is not analysis. Understand why customers buy them despite the issues — that's where the real insight lives.

**Competitor website as source of truth**: Marketing copy describes aspiration, not reality. Always validate against customer reviews, analyst assessments, and product demos.

**Missing the strategic conclusion**: A competitor profile without a "so what" has not done the analysis. Every finding should ladder up to a strategic implication.
