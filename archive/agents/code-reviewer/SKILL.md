# Code Reviewer Sub-Agent

## What It Does

Conducts production-grade code reviews covering correctness, security, performance, maintainability, and test coverage — in that priority order. Includes Azure SDK-specific checks (client instantiation, `DefaultAzureCredential` usage, embedding batch patterns, pydantic v1/v2 mixing) that standard linters miss. Read-only. Builds memory of recurring patterns in the codebase so it can surface them proactively at the start of future reviews.

## When to Invoke

- "Review the changes in `backend/api/v1/extract.py`"
- "Do a pre-PR review of everything I've changed"
- "Is this implementation correct?"
- "Check the error handling in the indexer service"
- "What am I missing before I open this PR?"

## How to Install

```bash
# Project-scoped
cp agents/code-reviewer/code-reviewer.md .claude/agents/code-reviewer.md

# User-scoped
cp agents/code-reviewer/code-reviewer.md ~/.claude/agents/code-reviewer.md
```

## Example Usage

```
Use the code-reviewer agent to review the changes in backend/services/extraction.py
before I open the PR.
```

```
Code review the authentication middleware — focus on security.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Sufficient for systematic rule-based review |
| Tools | Read, Glob, Grep | Read-only — reviewer never modifies files |
| Memory | project | Tracks recurring issues; surfaces patterns proactively |
| Color | green | "Go / review" association |

## Output Structure

Reviews are structured as: Summary → Must Fix (blocking, with concrete fixes) → Should Fix → Consider → Approved Patterns. Every Must Fix item includes a suggested fix — not just identification.
