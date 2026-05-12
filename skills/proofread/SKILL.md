---
name: proofread
description: >
  Perform a thorough editing pass on any written content — checking grammar,
  clarity, tone consistency, and structural flow. Use when polishing a draft
  before publication or sharing. Invoke with /proofread followed by the text
  to edit, and optionally the target tone or style guide.
allowed-tools: Read
---

When this skill is invoked, perform a multi-pass edit on the provided text. Return both a tracked-change-style annotated review and a clean final version. Editing is not rewriting — preserve the author's voice while improving clarity and correctness.

## Before Editing

1. **Identify the content type**: Marketing copy, technical documentation, business communication, blog post, report, social media?
2. **Identify the audience**: Who is reading this? What reading level and vocabulary are appropriate?
3. **Identify the tone target**: Formal, casual, professional, friendly, authoritative? Is there a brand voice to match?
4. **Identify the goal**: What should the reader do or believe after reading?

## Multi-Pass Edit Framework

Run the content through these passes in order:

### Pass 1 — Structure and Flow
- Does the content have a clear beginning, middle, and end?
- Does the opening establish what the piece is about and why it matters?
- Do paragraphs flow logically from one to the next?
- Is the most important point in the right position (usually near the top)?
- Are there sections that could be cut without losing meaning?

### Pass 2 — Clarity
- Is every sentence clear on first read?
- Are there sentences that need to be read twice to understand?
- Is any jargon used that the target audience may not know?
- Are there any ambiguous pronoun references ("it," "this," "they" with unclear antecedents)?
- Are complex ideas explained with enough context?

### Pass 3 — Concision
- Are there words that can be cut without changing meaning? ("In order to" → "to"; "Due to the fact that" → "because")
- Are there sentences that repeat an idea already stated?
- Are there adverbs modifying weak verbs that should be replaced with stronger verbs? ("Runs very fast" → "sprints")
- Are there passive constructions that should be active?

### Pass 4 — Tone and Voice
- Is the tone consistent throughout? Does it shift unexpectedly?
- Does the writing sound like one author, or does it feel stitched together?
- Are there phrases that feel overly formal or stiff for the intended audience?
- Are there phrases that feel too casual for a professional context?

### Pass 5 — Grammar, Punctuation, and Mechanics
- Sentence fragments that aren't stylistically intentional
- Run-on sentences
- Comma splices
- Subject-verb agreement errors
- Tense consistency
- Oxford comma usage (match to the style guide or be internally consistent)
- Apostrophe errors (its vs. it's, possessives)

## Output Format

```markdown
# Proofreading Review: [Document Title]

## Summary Assessment

**Overall quality**: [Strong / Needs moderate revision / Needs significant revision]
**Primary issues**: [1–3 sentence summary of the most important issues to address]
**Tone consistency**: [Consistent / Some drift — see notes below]

---

## Annotated Findings

| # | Location | Issue Type | Original | Suggested | Note |
|---|----------|-----------|----------|-----------|------|
| 1 | Para 1, Sentence 2 | Clarity | [original text] | [improved version] | [brief explanation] |
| 2 | Para 3 | Concision | [wordy phrase] | [tighter version] | "In order to" → "to" |
| 3 | Para 5 | Tone drift | [original] | [on-tone version] | Too formal for this brand voice |
...

---

## Structural Notes

[Paragraph-level observations about flow, organization, or sections that should be restructured or cut]

---

## Clean Final Version

[The full edited text — all suggested changes applied, ready to use]
```

## Editing Principles

**Preserve author voice**: The goal is to improve the text, not replace the author's style with yours. If the author has characteristic sentence structures or phrasing, keep them unless they actively harm clarity.

**Explain significant changes**: For any change beyond obvious grammar corrections, note why in the annotation. Editors who explain their reasoning build trust; editors who silently rewrite create resentment.

**Flag, don't fix, structural problems**: If a section needs to be substantially reorganized, flag it with a recommendation rather than rewriting it. Structural changes require author judgment.

## Common Issues to Catch

| Pattern | Problem | Fix |
|---------|---------|-----|
| "In order to" | Wordy | Replace with "to" |
| "Due to the fact that" | Wordy | Replace with "because" |
| "It is important to note that" | Empty opener | Delete and start the sentence |
| "Very," "really," "quite" | Weak intensifiers | Cut or replace verb |
| "Utilize" | Jargon for "use" | Replace with "use" |
| "Leverage" (non-financial) | Overused business jargon | Replace with specific verb |
| Passive: "It was decided that" | Obscures ownership | Rewrite: "The team decided that" |
| Nominalizations: "make a decision" | Wordy | Replace with "decide" |
