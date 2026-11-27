---
name: adr-writing
description: >
  Generate a complete Architecture Decision Record (ADR). Use when a significant
  technical decision has been made or needs to be documented. Invoke with
  /adr-writing followed by the decision topic.
allowed-tools: Read, Glob, Grep
---

When this skill is invoked, produce a complete Architecture Decision Record. Read existing ADRs in `docs/architecture-decisions/` first to use the next sequential number and match conventions.

## Before Writing

1. Read existing ADRs to identify the next number in sequence
2. Read relevant config files, infrastructure-as-code, or existing implementations to understand technical context accurately
3. Identify the decision-makers (roles if names are unknown)

## ADR Format

```markdown
# ADR-[NNN]: [Decision Title]

**Date**: [today's date in YYYY-MM-DD]
**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Deciders**: [roles or names]

## Context

[2–4 paragraphs describing the situation that requires a decision. Include:
what problem is being solved, what constraints exist, what has been tried
or evaluated. Write in past tense — this is the state of the world AT THE
TIME of the decision, not general background.]

## Decision

[One clear sentence stating what was decided. Then 2–3 paragraphs explaining
the implementation approach. Be specific: name the Azure service tier, the
auth flow, the data format, the exact configuration. No vague language like
"a more scalable approach."]

## Consequences

### Positive
- [Specific, measurable benefit]

### Negative
- [Specific trade-off or cost accepted — be honest]

### Neutral
- [Changes to workflows or operations that are neither clearly good nor bad]

## Alternatives Considered

### Alternative: [Name]
[1–2 sentences: what it is and the specific reason it was rejected.
"Too expensive" alone is not enough — how much more, and why doesn't
the benefit justify that cost?]
```

## Quality Bar

A good ADR:
- Can be read by someone joining the team in 6 months and understood without prior context
- Documents the **why**, not just the **what** — the what is in the code
- Acknowledges trade-offs honestly — future readers need to know what was accepted
- Uses past tense for Context and present/future for Decision and Consequences
- Includes at least two alternatives with specific rejection reasons

## Real Examples of Context Done Right

These are the kinds of specific, situation-grounded context paragraphs that make an ADR useful:

> "Copilot Studio's built-in Azure AI Search knowledge source caps retrieval at 5 results. For a corpus of 10,000 documents where the relevant passage may not be in the top 5, this produces incorrect or incomplete answers without any error signal — the agent simply presents the best 5 results as if they are sufficient."

> "The Copilot Studio agent was using Entra ID delegated authentication to call the backend API. In production, every new user was prompted for OAuth consent on first use. With hundreds of daily users, this was unacceptable from a UX standpoint and created a support burden."

> "The Azure Function extraction job takes 45–90 seconds to process a large document. Power Automate's HTTP action has a 120-second timeout, which was being hit intermittently on large files, causing the flow to fail with no result — not an error the user could act on."

> "The development environment used Python 3.11 and the CI pipeline used Python 3.12. pydantic-core is compiled against a specific Python minor version. Tests passed in CI but failed on developer machines with a `ModelMetaclass` import error that was non-obvious to diagnose."

## Common Mistakes to Avoid

**Context as general background**: "Azure AI Search is a cloud search service that supports hybrid search..." — This describes the product, not the situation. The context should describe *your* problem, not the documentation.

**Consequences that restate the decision**: "We will use managed identity, so authentication will use managed identity." A consequence is an effect of the decision, not a restatement of it.

**Vague rejection reasons**: "Too complex" → what specifically makes it too complex, and for whom? "The client team does not have Kubernetes expertise to operate a Qdrant cluster" is a specific rejection reason.
