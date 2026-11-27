---
name: follow-up-email
description: >
  Draft a professional post-meeting follow-up email summarizing key decisions,
  action items, and next steps for all attendees. Use immediately after a
  meeting to send a structured recap. Invoke with /follow-up-email followed
  by the meeting notes, summary, or transcript.
allowed-tools: Read
---

When this skill is invoked, produce a clear, professional follow-up email ready to send to meeting attendees. This email is not a transcript — it is a confirmation document that aligns everyone on what was decided and who is doing what.

## Before Drafting

1. **Identify the meeting context**: What was this meeting for? What was the relationship between participants (team internal, client, executive, cross-functional)?
2. **Identify the tone**: Internal team meeting → direct and efficient. Client meeting → professional and warm. Executive meeting → concise and decision-focused.
3. **Identify the sender**: Who is sending this? (Affects "I" vs "we" framing and sign-off style)
4. **Identify key outputs**: Decisions made, actions assigned, next steps confirmed.

## Email Principles

**Subject line sets expectations**: The subject line should make the meeting's output immediately clear. "Follow-up: [Meeting Name] — [Date]" works for recurring meetings. "[Decision made]: Next steps from [Meeting Name]" works for decision meetings.

**Lead with decisions, not summary**: Attendees don't need a narrative recap — they were there. Lead with what was decided and who's doing what.

**Action items need specificity**: "We agreed John would send the proposal" is too vague. "John will send the revised proposal to the client by EOD Friday, March 14" creates accountability.

**Segment by recipient where needed**: If different attendees have different action items, make it obvious who owns what. Nobody should have to search to find their tasks.

**End with a clear next step**: What happens next? When is the next meeting? What should people do if they have questions?

## Output Format

```markdown
**Subject**: Follow-up: [Meeting Name] — [Date]

Hi [Name / Team / All],

Thanks for joining today's [meeting type]. Here's a recap of what we covered and agreed on.

---

**Decisions Made**

- [Decision 1 — stated clearly and specifically]
- [Decision 2]
[If no formal decisions: "We covered [topic] and will finalize the decision by [date/trigger]."]

---

**Action Items**

| Owner | Task | Due Date |
|-------|------|----------|
| [Name] | [Specific task] | [Date] |
| [Name] | [Specific task] | [Date] |

---

**Open Items / Next Steps**

- [Question or item that still needs resolution — and who is responsible for resolving it]

---

**Next Meeting**

[Date and time if scheduled, or "TBD — I'll send a calendar invite once [condition is met]"]

---

Let me know if I've missed anything or if there are any corrections.

[Sign-off],
[Sender name]
```

## Tone Variations

**Internal team**: Casual, first names, can be bullet-heavy without pleasantries.

**Client-facing**: Warm opening, professional framing, confirm next steps clearly, offer to answer questions.

**Executive-level**: Lead with the decision or key outcome in the first line. Executives read the first sentence and skim the rest. Be the most concise version of this email.

**Cross-functional / stakeholder**: Name each team's action items separately so ownership is unambiguous across group boundaries.

## Quality Bar

A good follow-up email:
- Can be read in under 60 seconds
- Every action item has a named owner and a specific deadline
- Decisions are stated as decisions, not as things that "might" happen
- Recipients can immediately identify their own responsibilities
- Ends with a clear next step or trigger for what happens next

## Common Mistakes to Avoid

**Meeting narrative**: "We started by discussing X, then moved to Y" — nobody needs to re-read the meeting. Lead with outcomes.

**Passive ownership**: "It was agreed that the report would be sent" — who sends it? Name the owner.

**Endless pleasantries**: "Thank you so much for taking the time to join us today, it was wonderful to connect..." — people read this on their phone between meetings. Get to the point in sentence 1.

**Missing deadlines**: "Soon" and "ASAP" are not deadlines. Name a date or a clear trigger event.
