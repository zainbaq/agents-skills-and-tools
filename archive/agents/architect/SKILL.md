# Architect Sub-Agent

## What It Does

Reviews architecture, designs systems, evaluates trade-offs, and produces ADRs. Specializes in Azure cloud-native patterns, RAG pipeline design, agentic system architecture, and Power Platform deployment patterns. Built from production experience shipping AI systems — it knows the failure modes that only surface after go-live. Read-only — the architect observes and advises, never modifies files.

## When to Invoke

- "Review the architecture of this service"
- "Design a RAG pipeline for document search"
- "Write an ADR for our auth strategy"
- "What's the right Azure service for this queue pattern?"
- "Should this be multi-agent or a single-agent pipeline?"
- "Why is the Copilot Studio agent returning inconsistent results?"
- "How do I connect Power Automate to a private Azure Function?"
- "Design an NLP-to-SQL agent over this Fabric schema"

## How to Install

```bash
# Project-scoped (checked into version control)
cp agents/architect/architect.md .claude/agents/architect.md

# User-scoped (available in all projects)
cp agents/architect/architect.md ~/.claude/agents/architect.md
```

Restart Claude Code after copying.

## Example Usage

```
Use the architect agent to review the RAG pipeline design in /backend/services/
and produce an ADR for the chunking strategy decision.
```

```
Review the authentication architecture across the API and flag any
privilege escalation risks.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Good balance of reasoning depth and speed for design work |
| Tools | Read, Glob, Grep, WebFetch | Read-only — architect advises, never modifies |
| Memory | project | Accumulates codebase-specific patterns across sessions |
| Color | blue | Visually distinct in the Claude Code task list |

## Output Formats

The architect produces:
- **Architecture review reports** with `[RISK]`-tagged findings
- **ADRs** in Status / Context / Decision / Consequences / Alternatives format
- **Mermaid diagrams** for system topology
- **Azure service recommendations** with SKU tiers at the described scale
