---
name: meeting-summary
description: >
  Extract a structured summary with key decisions and action items (with owners
  and deadlines) from meeting notes or a transcript. Use after any meeting to
  produce a shareable record. Invoke with /meeting-summary followed by the raw
  notes or transcript.
allowed-tools: Read
---

When this skill is invoked, transform raw meeting notes or a transcript into a structured, shareable summary. A meeting summary is not a transcript — it is a processed record of what was decided, who is doing what, and by when.

## Before Summarizing

1. **Identify the meeting type**: Standup, planning, retrospective, decision meeting, client call, strategy session, or one-on-one?
2. **Identify the participants**: Who was in the room? What are their roles?
3. **Scan for decisions vs. discussions**: Not everything discussed is a decision. Separate what was decided from what was explored.

## Extraction Rules

**Decisions**: A decision was made if someone explicitly stated a choice, the group reached consensus, or a course of action was agreed upon. Vague statements like "we should probably..." are NOT decisions — flag them as open items.

**Action items**: An action item requires:
- A specific, concrete task (not "follow up" or "look into it")
- An owner (a person or role — not "the team")
- A deadline or expected completion timeframe
- If any of these three are missing, flag it as incomplete in the output

**Open questions**: Items that were raised but not resolved. These need a decision process, not just follow-up.

## Output Format

```markdown
# Meeting Summary: [Meeting Name/Type]
**Date**: [date]
**Attendees**: [names or roles]
**Duration**: [if known]

---

## Key Decisions

1. [Decision] — [brief context if needed]
2. [Decision]
[If no decisions were made: "No formal decisions reached — see Open Questions"]

---

## Action Items

| # | Task | Owner | Deadline | Notes |
|---|------|-------|----------|-------|
| 1 | [Specific task] | [Name/Role] | [Date or "EOW", "Next meeting"] | [Any context] |
| 2 | ... | ... | ... | ... |

**Incomplete action items** (flagged — missing owner or deadline):
- [Task as stated] — needs: [what's missing — owner / deadline / clarification]

---

## Open Questions / Unresolved Items

- [Question or issue raised but not decided]
- [Who should resolve it, if named]

---

## Key Discussion Points

[3–5 bullets on the most important topics discussed — for context, not as a transcript]

---

## Next Meeting
**Date**: [if scheduled]
**Agenda items to carry forward**: [items that need to be picked up next time]
```

## Quality Bar

A good meeting summary:
- Distinguishes decisions from discussions — not everything talked about is a decision
- Every action item has an owner and a deadline — vague tasks are flagged
- Open questions are explicit — they don't disappear into "misc"
- Can be read by someone who wasn't in the meeting and understood in under 2 minutes
- Does not require reading the full transcript to understand what happened

## Common Mistakes to Avoid

**Transcription instead of summarization**: A meeting summary is not a cleaned-up transcript. Synthesize — don't just shorten.

**Vague action items**: "John will follow up on the thing we discussed" is not an action item. "John will send the revised proposal to the client by Friday" is.

**Missing owners**: "Someone will..." is not an owner. If ownership was not assigned, flag it as incomplete rather than fabricating an owner.

**Burying the decisions**: The decisions and action items are the highest-value outputs. Put them first, not at the end.
