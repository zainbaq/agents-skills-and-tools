---
name: sop-create
description: >
  Write a complete Standard Operating Procedure (SOP) with purpose, scope,
  prerequisites, numbered steps, and troubleshooting guidance. Use when
  documenting a repeatable process for a team. Invoke with /sop-create
  followed by the process to document and the intended audience.
allowed-tools: Read
---

When this skill is invoked, produce a complete, actionable Standard Operating Procedure. An SOP is not a description of a process — it is a procedure executable by someone following it for the first time without needing to ask for help.

## Before Writing

Gather or clarify:
1. **Process name**: What is being documented?
2. **Audience**: Who will execute this? What is their technical level and role?
3. **Purpose**: What outcome does this process produce? Why does it exist?
4. **Scope**: What triggers this SOP? What is NOT covered by this SOP?
5. **Prerequisites**: What must be true or complete before step 1? Access, tools, prior steps?
6. **Known edge cases**: What commonly goes wrong? What variations exist?

## SOP Writing Rules

**Each step = one action**: If a step has "and" in it, consider splitting it.

**Action verbs lead every step**: "Click Settings" not "Settings should be clicked" or "You will want to go to Settings."

**Include expected outcomes**: After steps where something visually changes or a confirmation appears, tell the reader what they should see. This is how they know they did it right.

**Prerequisites are not step 1**: Prerequisites belong in their own section before the procedure. A reader who doesn't have the required access should know before they start — not after step 7.

**Warnings before the step**: If a step has a risk of data loss, irreversibility, or common error, put the warning directly before the step — not after.

## Output Format

```markdown
# SOP: [Process Name]

**Version**: 1.0
**Last reviewed**: [today]
**Owner**: [Role — not a specific person, who may change]
**Audience**: [Who executes this]

---

## Purpose

[One sentence: what outcome does this process produce and why it matters]

## Scope

**In scope**: [What this SOP covers]
**Out of scope**: [What this SOP explicitly does not cover — prevents confusion]
**Trigger**: [What initiates this process — an event, schedule, or request]

---

## Prerequisites

Before beginning, ensure you have:
- [ ] [Access or permission required — with instructions on how to get it if non-obvious]
- [ ] [Tool or system required — with version or configuration note if relevant]
- [ ] [Prior process or step that must be completed first]

---

## Procedure

### Step 1 — [Short descriptive name]
[Action verb + specific instruction]

> **Expected result**: [What the user should see or confirm after this step]

---

### Step 2 — [Short descriptive name]
[Action verb + specific instruction]

> ⚠️ **Warning**: [If this step is irreversible or error-prone, state the risk here]

[Action details]

> **Expected result**: [Confirmation of success]

---

[Continue for all steps]

---

## Edge Cases and Troubleshooting

| Situation | Cause | Resolution |
|-----------|-------|------------|
| [Error message or unexpected outcome] | [Why this happens] | [How to fix it] |
| [Common variation from standard path] | [Why it occurs] | [How to handle it] |

---

## Escalation

If you cannot complete this process or encounter a situation not covered above:
- **First contact**: [Role or team and how to reach them]
- **Escalation path**: [Who to escalate to if first contact cannot resolve]

---

## Related Documents

- [Links to related SOPs, runbooks, or reference documents]

---

## Revision History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | [today] | Initial version | [Name/Role] |
```

## Quality Bar

A good SOP:
- Can be executed by a qualified new hire without asking anyone a question
- Every step starts with an action verb
- Every risky or irreversible step has a warning immediately before it
- Expected results are included for steps where the outcome is visible
- Troubleshooting table covers the 3–5 most common failure modes

## Common Mistakes to Avoid

**Implicit prerequisites**: The first step of many SOPs secretly requires prior setup that is never documented. Ask: "What must be true before someone can do step 1?"

**"Just" and "simply"**: Remove these words. They signal you've forgotten what it's like to not know the process.

**No expected results**: Without expected outputs at each step, users don't know if they're on the right path or silently doing something wrong.

**One SOP for multiple audiences**: A developer SOP and an end-user SOP for the same process should be separate documents. Merge them and you get something neither audience can follow.
