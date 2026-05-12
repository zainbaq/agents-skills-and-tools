---
name: email-sequence
description: >
  Write a multi-email sequence with subject lines, preview text, body copy,
  and CTAs for a specific goal and audience. Use for welcome sequences,
  nurture campaigns, onboarding flows, re-engagement campaigns, or
  post-event follow-ups. Invoke with /email-sequence followed by the goal,
  audience, and number of emails needed.
allowed-tools: Read
---

When this skill is invoked, produce a complete email sequence. Each email in the sequence must serve a specific purpose within the journey — no filler emails that exist only to maintain cadence.

## Before Writing

Clarify or gather:
1. **Sequence type**: Welcome / Onboarding / Nurture / Re-engagement / Post-event / Sales follow-up
2. **Audience**: Who is receiving this? What do they know about the brand at this point?
3. **Goal**: What should the reader do or believe after completing the sequence?
4. **Number of emails**: How many? What is the cadence (daily, every 2 days, weekly)?
5. **Brand voice**: Formal or casual? Personal (from a person) or brand? Warm or efficient?
6. **CTA type**: What is each email asking the reader to do?

## Sequence Architecture Principles

**Every email needs one job.** Multi-CTA emails are confusing. Each email in a sequence should have exactly one primary call to action.

**Sequence logic**: Each email should build on the previous one. Reader should feel a coherent journey, not a series of unrelated messages.

**Subject line is half the battle.** The best body copy is useless if no one opens. Write 2 subject line options per email.

**Preview text is the second subject line.** Don't waste it by repeating the subject line or leaving it blank.

**Email 1 sets the contract.** The first email in any sequence tells the reader what to expect. Violate those expectations and unsubscribes follow.

## Output Format

```markdown
# Email Sequence: [Name]
**Type**: [Welcome / Nurture / etc.]
**Audience**: [Who receives this]
**Goal**: [What success looks like]
**Cadence**: [e.g., Day 0, Day 2, Day 5, Day 8]

---

## Email 1 — [Purpose of this email]
**Send time**: [Day 0 / Immediately after trigger]
**Job**: [One sentence on what this email must accomplish]

**Subject line A**: [Option 1]
**Subject line B**: [Option 2 — different angle or hook]
**Preview text**: [35–90 characters — the line under the subject in the inbox]

---

[Body copy — in the brand's voice. Use short paragraphs (2–4 lines max).
Include a clear, single CTA.]

**CTA**: [Button text or link text] → [Where it goes / what it does]

---

## Email 2 — [Purpose]
[Same format]

---
[Continue for all emails in the sequence]

---

## Sequence Notes
- **Personalization hooks**: [Variables to swap in, e.g., first name, company, product used]
- **Branch logic** (if applicable): [What happens if someone clicks CTA in Email 2 — do they skip Email 3?]
- **Exit trigger**: [What action removes someone from this sequence — e.g., books a demo, makes a purchase]
```

## Subject Line Formulas That Work

- **Curiosity gap**: "You're missing [X]" / "Why [unexpected thing] works"
- **Direct value**: "[Specific outcome] in [timeframe]"
- **Question**: "Is your [thing] doing [problem]?"
- **Personal/relatable**: "I was wrong about [X]"
- **Social proof**: "How [Company] achieved [result]"

## Quality Bar

A good email sequence:
- Has a clear arc — readers feel they're moving toward something
- Each email has one job and one CTA
- Subject lines create genuine curiosity or communicate clear value (not both at once)
- Body copy is scannable (short paragraphs, occasional bold for key phrases)
- Uses the reader's perspective ("you'll be able to..." not "we built...")

## Common Mistakes to Avoid

**Sequence without arc**: Sending 5 emails about 5 different topics is a newsletter cadence, not a sequence. Define the journey before writing.

**Pitch in every email**: Nurture sequences that sell in every email exhaust subscribers. Use 80% value, 20% CTA.

**Generic subject lines**: "Check out our latest update" will be ignored. Be specific about the value or create genuine curiosity.

**Long paragraphs**: Emails are read on phones between meetings. Write like that. 3 lines, white space, scan-friendly.
