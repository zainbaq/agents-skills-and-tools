# UX Designer Sub-Agent

## What It Does

Reviews UI/UX designs for usability, accessibility, and information hierarchy. Audits copy and microcopy for brand voice consistency. Documents component behavior and user flows. Produces prioritized, actionable design feedback rather than vague aesthetic opinions. Built from the failure modes that cause real users to get stuck — not design theory.

## When to Invoke

- "Review this screen for UX issues"
- "Give feedback on the onboarding flow"
- "Audit the copy across these pages for brand voice consistency"
- "Is this microcopy on-brand and clear?"
- "Document the behavior of this component"
- "Review the error messages in the app"
- "Describe this wireframe for developer handoff"

## How to Install

```bash
# Project-scoped
cp agents/ux-designer/ux-designer.md .claude/agents/ux-designer.md

# User-scoped (available in all projects)
cp agents/ux-designer/ux-designer.md ~/.claude/agents/ux-designer.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the ux-designer agent to review the checkout flow screens in /designs/
and produce a prioritized list of UX issues. Focus on clarity and error states.
```

```
Audit the microcopy across all buttons, labels, and error messages in the app
and flag anything that doesn't match our friendly-but-expert brand voice.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Sufficient for design analysis and copy review |
| Tools | Read, WebFetch | Reads design docs and brand guides |
| Memory | project | Retains brand voice profile and design system patterns |
| Color | purple | Distinct from engineering/analysis agents |

## Output Formats

- **UX review**: Prioritized findings (P0–P3) with observation → impact → recommendation
- **Brand voice audit**: Dimension analysis + inconsistencies + suggested rewrites
- **Microcopy review**: Table of Original → Issue → Suggested rewrite
- **Component documentation**: States, usage guidelines, do/don't examples
