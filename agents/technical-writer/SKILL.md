# Technical Writer Sub-Agent

## What It Does

Writes and edits technical documentation, SOPs, user guides, runbooks, and knowledge base articles. Knows the difference between documentation that actually gets read and followed versus documentation that looks complete but confuses users. Enforces standards that prevent the most common documentation failures: implicit prerequisites, passive voice without ownership, and audience-inappropriate depth.

## When to Invoke

- "Write an SOP for our onboarding process"
- "Document how to set up the development environment"
- "Improve this user guide — it's confusing"
- "Write a runbook for the deployment process"
- "Create a knowledge base article about [feature]"
- "Review this documentation for completeness"
- "Build a style guide for our documentation"

## How to Install

```bash
# Project-scoped
cp agents/technical-writer/technical-writer.md .claude/agents/technical-writer.md

# User-scoped (available in all projects)
cp agents/technical-writer/technical-writer.md ~/.claude/agents/technical-writer.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the technical-writer agent to write an SOP for our client onboarding
process. The audience is account managers. Steps involve Salesforce, Slack,
and our internal project management tool.
```

```
Review the existing documentation in /docs/ and produce a prioritized
improvement plan. Flag accuracy issues, missing prerequisites, and
audience mismatches.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Good balance of quality and speed for documentation work |
| Tools | Read, Glob, Grep | Reads existing docs to match conventions |
| Memory | project | Retains documentation conventions, audience profiles, and style |
| Color | blue | Consistent with knowledge/advisory agents |

## Key Distinctions

This agent will write documentation that actually enables action — not documentation that describes systems in abstract terms. Every SOP gets a purpose statement, scope boundary, prerequisites, and numbered steps with expected results. It will always ask what task a user is trying to complete before writing.
