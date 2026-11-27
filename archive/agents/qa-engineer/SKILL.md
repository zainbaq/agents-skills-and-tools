# QA Engineer Sub-Agent

## What It Does

Writes production-quality tests and designs test strategies. Includes AI/RAG-specific test patterns: multi-stage pipeline stage isolation, document chunking edge cases, NLP-to-SQL SQL validity checks, and Azure AI Search response shape validation. Can create and edit test files — the only agent in this library with Write access. Reads existing tests before writing new ones to match project conventions.

## When to Invoke

- "Write unit tests for the extraction service"
- "What test coverage is missing before we release this?"
- "Design the test strategy for the new NLP-to-SQL feature"
- "Review the quality of these tests — are they testing behavior or implementation?"
- "Write integration tests for the Azure AI Search client"

## How to Install

```bash
# Project-scoped
cp agents/qa-engineer/qa-engineer.md .claude/agents/qa-engineer.md

# User-scoped
cp agents/qa-engineer/qa-engineer.md ~/.claude/agents/qa-engineer.md
```

## Example Usage

```
Use the qa-engineer agent to write unit tests for the chunking logic in
backend/services/document_processor.py. Cover the happy path and at least
the empty document, oversized document, and encoding error failure modes.
```

```
QA strategy for the new Copilot Studio hybrid search integration.
What test types do we need and what's explicitly out of scope?
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Test writing is systematic; reasoning depth of opus not needed |
| Tools | Read, Glob, Grep, Write, Edit | Write/Edit access to create and update test files |
| Memory | project | Tracks fixtures, patterns, and known coverage gaps |
| Color | purple | Distinct from the read-only green reviewer |

## Key Distinction from Code Reviewer

The code-reviewer identifies problems; the qa-engineer fixes them by writing tests. If a code review surfaces missing test coverage, use the qa-engineer to fill the gaps.
