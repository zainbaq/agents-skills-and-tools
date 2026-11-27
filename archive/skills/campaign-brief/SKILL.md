---
name: campaign-brief
description: >
  Generate a complete marketing campaign brief with audience, insight,
  messaging hierarchy, channel mix, and KPIs. Use when planning a new
  campaign, product launch, or marketing initiative. Invoke with
  /campaign-brief followed by the product, launch, or initiative to brief,
  plus any known audience or goal information.
allowed-tools: Read, WebFetch
---

When this skill is invoked, produce a complete marketing campaign brief. A brief is not a list of tactics — it is the strategic foundation that ensures all tactics serve the same goal and audience.

## Before Writing

Gather or clarify these inputs:
1. **What are we promoting?** Product, feature, service, event, or content?
2. **Who is the audience?** Primary ICP, secondary segment. Stage of awareness (unaware → aware → considering → deciding)?
3. **What is the goal?** Brand awareness, lead generation, nurturing, conversion, retention, or re-engagement?
4. **What is the key insight?** The human truth or market observation that makes this campaign relevant and resonant.
5. **What channels are available?** Paid, owned, earned — and which are in scope?
6. **What is the timeline?** Launch date, campaign duration, key milestones.
7. **What is the budget tier?** (If known — shapes channel mix.)

## Brief Format

```markdown
# Campaign Brief: [Campaign Name]

**Date**: [today]
**Campaign type**: [Launch / Awareness / Lead Gen / Nurture / Retention]
**Timeline**: [Start date] → [End date]
**Owner**: [Role or name]

---

## The Audience

**Primary segment**: [Job title, company type, life stage, or demographic]
**Awareness stage**: [Unaware / Problem-aware / Solution-aware / Considering / Deciding]
**Key belief to change or reinforce**: [What does this audience currently believe, and what do we want them to believe after this campaign?]
**Pain points relevant to this campaign**: [2–3 specific frustrations or desires that make this message relevant to them now]

---

## The Insight

[One paragraph. The single human truth, market moment, or cultural observation that makes this campaign timely and resonant. This is not a product feature. It's why people will care. Example: "The average operations manager spends 6 hours a week on status updates — time they could spend on the work that actually requires their judgment."]

---

## The Message

**Core message**: [One sentence — the single most important thing the audience should walk away believing]

**Supporting messages**:
1. [Reason to believe #1 — evidence or proof point]
2. [Reason to believe #2]
3. [Reason to believe #3]

**Tone**: [How should this campaign feel? E.g., urgent, warm, empowering, irreverent, authoritative]

---

## Channel Mix

| Channel | Role in Campaign | Format | Volume/Budget Allocation |
|---------|-----------------|--------|--------------------------|
| [e.g., LinkedIn Ads] | [Awareness / Consideration / Conversion] | [Single image / Video / Carousel] | [%] |
| [e.g., Email] | [Nurture sequence for existing leads] | [3-email sequence] | [%] |
| [e.g., Organic social] | [Amplification and community] | [5 posts] | [%] |

---

## Success Metrics

| KPI | Definition | Target | Timeframe |
|-----|-----------|--------|-----------|
| [Primary KPI — e.g., MQLs] | [How measured] | [Number] | [By when] |
| [Secondary KPI — e.g., CTR] | [How measured] | [Benchmark] | [By when] |
| [Brand/awareness metric] | [How measured] | [Benchmark] | [By when] |

---

## Creative Guardrails

**Must include**: [Brand elements, disclaimers, or messages that are non-negotiable]
**Must avoid**: [Topics, claims, or tones that are off-limits]
**Proof points available**: [Case studies, stats, testimonials that can be used]

---

## Open Questions / Assumptions

[Flag anything that was assumed in this brief that should be validated before production begins]
```

## Quality Bar

A good campaign brief:
- Has a real insight, not a product feature dressed up as an insight
- Specifies awareness stage (this determines the entire message hierarchy)
- Names success metrics that are actually measurable before production begins
- Includes creative guardrails so execution doesn't go off-brief
- Surfaces the assumptions that need validation

## Common Mistakes to Avoid

**Insight = product feature**: "Our product saves time" is not an insight. "Operations leaders are drowning in coordination work that doesn't require their expertise" is an insight.

**"Everyone" as the audience**: Campaigns without a specific primary audience produce generic creative that resonates with no one.

**Missing awareness stage**: A campaign targeting decision-ready buyers needs very different messaging than one targeting awareness-stage audiences. This single variable changes everything.
