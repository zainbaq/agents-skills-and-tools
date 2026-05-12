---
name: design-feedback
description: >
  Generate structured UX/UI design feedback with prioritized findings,
  accessibility checks, and actionable recommendations. Use when reviewing
  screens, flows, or wireframes and need specific, prioritized critique.
  Invoke with /design-feedback followed by a description or paste of the
  design, screen content, or user flow to review.
allowed-tools: Read, WebFetch
---

When this skill is invoked, produce a structured, prioritized UX/UI design review. Your job is to give feedback that helps designers ship better work — not vague aesthetic opinions.

## Before Reviewing

1. Establish context: What is this screen/flow trying to help the user accomplish?
2. Identify the audience: Who is the primary user? What is their technical level?
3. Clarify scope: Are we reviewing the whole flow or a specific screen? Is this early wireframe or high-fidelity?

## Review Dimensions

Evaluate on these dimensions and flag issues by severity:

**Clarity (can users understand the purpose immediately?)**
- Does the user know what this page/screen is for within 3 seconds?
- Is the primary action obvious and labeled clearly?
- Is every label, instruction, and message unambiguous?

**Hierarchy (does visual weight match importance?)**
- Is the most important action the most visually prominent?
- Are secondary options clearly subordinate?
- Is related information grouped together?

**Flow (does the sequence match the user's mental model?)**
- Are there unnecessary steps in the journey?
- Is progress visible where the task takes more than one step?
- Does the back/exit option match user expectations?

**Error handling (are problems actionable?)**
- Do error messages say what went wrong AND what to do next?
- Are inline validation errors specific (not just "required field")?
- Is there a recovery path from every error state?

**Accessibility**
- Would this work for users relying on keyboard navigation?
- Is text contrast sufficient (4.5:1 for body text)?
- Are touch targets at least 44×44px on mobile?
- Is any information communicated by color alone?

**Microcopy**
- Do button labels use verb-noun format (Save draft, Send message)?
- Are empty states helpful rather than just blank?
- Are confirmation dialogs specific about what will be deleted/changed?

## Output Format

```markdown
## Design Review: [Screen/Flow Name]

### Context
[One line on what this screen is meant to accomplish]

### Priority Findings

**P0 — Critical (blocks task completion or causes errors)**
- [Finding]: [Observation] → [Impact on user] → [Specific recommendation]

**P1 — Major (significantly degrades experience)**
- [Finding]: [Observation] → [Impact on user] → [Specific recommendation]

**P2 — Minor (friction or inconsistency)**
- [Finding]: [Observation] → [Impact on user] → [Specific recommendation]

**P3 — Polish (low-impact improvements)**
- [Finding]: [Observation] → [Impact on user] → [Specific recommendation]

### Accessibility Flags
- [Any accessibility issues found, or "No accessibility issues identified"]

### Microcopy Improvements
| Current | Issue | Suggested |
|---------|-------|-----------|
| [text] | [what's wrong] | [better version] |

### What's Working
[2–3 things that are done well — good feedback includes positives]
```

## Quality Bar

A good design review:
- Prioritizes findings so designers know where to start
- Frames every finding from the user's perspective, not design craft theory
- Gives a specific recommendation, not just identifies a problem
- Acknowledges what is working alongside what needs improvement
- Does not redesign — it reviews

## Common Mistakes to Avoid

**Aesthetic feedback without usability grounding**: "The spacing feels off" → useless. "The 8px gap between label and input is below standard, making the form harder to scan" → actionable.

**Flagging everything as equal severity**: If everything is P1, nothing is P1. Prioritize honestly.

**Redesigning when reviewing**: Feedback is "this CTA label is unclear." Redesign is "here's a whole new layout." Stay in feedback mode unless asked for a redesign.
