---
name: brand-voice-audit
description: >
  Audit copy or content for brand voice consistency. Use when reviewing
  marketing copy, UI text, documentation, or any written content against
  a brand's established voice and tone. Invoke with /brand-voice-audit
  followed by the content to audit and (optionally) brand voice guidelines
  or sample content that represents the correct voice.
allowed-tools: Read
---

When this skill is invoked, perform a systematic brand voice audit of the provided content. Your job is to identify where the writing drifts from the established voice and recommend specific improvements.

## Before Auditing

1. **Establish the voice profile**: If brand guidelines are provided, extract the key voice dimensions. If not, infer them from sample content. Document the dimensions before auditing.

2. **Define the voice dimensions** on these axes:
   - Formality: Formal ↔ Casual
   - Authority: Expert/Authoritative ↔ Peer/Conversational
   - Tone: Serious ↔ Playful
   - Complexity: Technical ↔ Accessible
   - Warmth: Professional ↔ Personal
   - Directness: Direct ↔ Nuanced

3. **Identify voice markers**: Specific vocabulary preferences, sentence length tendencies, CTA style, use of humor, and personality signals.

## Audit Checklist

**Vocabulary consistency**
- Are synonyms used consistently? (help vs. assist, use vs. utilize, get vs. obtain)
- Is jargon level consistent throughout?
- Are brand-specific terms used correctly and consistently?

**Formality drift**
- Does the register shift between sections without reason?
- Are there formal constructions in content meant to feel casual?
- Are there casualisms in content meant to feel authoritative?

**Personality markers**
- If the brand uses humor, does it appear where expected?
- If the brand is warm, are error messages and confirmations equally warm?
- If the brand is direct, are there hedged or wishy-washy statements?

**Active vs. passive voice**
- Does passive voice appear in ways that feel evasive for this brand?
- Are there passive constructions that obscure ownership or action?

**CTA style**
- Do calls to action match the brand's energy? (Get started vs. Let's go vs. Begin your journey)
- Are CTAs consistent in style across the content?

## Output Format

```markdown
## Brand Voice Audit: [Content Name/Type]

### Voice Profile
**Established dimensions:**
- Formality: [position on scale with evidence]
- Authority: [position on scale with evidence]
- Tone: [position on scale with evidence]
- Complexity: [position on scale with evidence]
- Warmth: [position on scale with evidence]

### Summary
[2–3 sentence overall assessment. Is the voice consistent? Where is the biggest drift?]

### Findings

| # | Location | Issue | Current Text | Suggested Rewrite |
|---|----------|-------|-------------|-------------------|
| 1 | [section/line] | [voice drift type] | [original] | [on-brand version] |
| 2 | ... | ... | ... | ... |

### Vocabulary Flags
**Inconsistent synonyms found:**
- [word A] used in [location] vs. [word B] used in [location] → standardize to: [preferred]

### Patterns to Address
[2–3 systemic patterns across the content that indicate a broader issue, not just individual instances]

### What's Working
[Strong examples of on-brand writing from the content]
```

## Quality Bar

A good voice audit:
- Establishes the voice dimensions before auditing against them
- Finds systemic patterns, not just individual word swaps
- Provides rewrites that sound natural, not just technically correct
- Distinguishes intentional style choices from accidental drift
- Doesn't impose a voice — audits against the brand's own established voice
