# Security Auditor Sub-Agent

## What It Does

Conducts adversarial security audits covering OWASP Top 10, Azure-specific risks, secret management, authentication bypass paths, and dependency CVEs. Has specific experience with the auth patterns that fail in Copilot Studio and Power Platform deployments — particularly the difference between user-delegated and application-level auth, and why it matters in production. Uses `claude-opus-4-5` — adversarial reasoning benefits from the highest-capability model. No memory, by design — each audit should be fresh.

## When to Invoke

- "Security audit the authentication flow in `backend/app/api/v1/auth.py`"
- "Audit the entire API for OWASP Top 10 vulnerabilities"
- "Is there any hardcoded secret in this codebase?"
- "Pre-deployment security review"
- "Check if managed identity permissions are appropriately scoped"
- "Why are Copilot Studio users being prompted for OAuth consent?"
- "Review this Entra ID app registration for over-permissions"

## How to Install

```bash
# Project-scoped
cp agents/security-auditor/security-auditor.md .claude/agents/security-auditor.md

# User-scoped
cp agents/security-auditor/security-auditor.md ~/.claude/agents/security-auditor.md
```

## Example Usage

```
Use the security-auditor agent to audit the authentication and authorization
implementation across the entire backend API. Flag anything that could allow
privilege escalation or auth bypass.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | opus | Adversarial reasoning requires the highest-capability model |
| Tools | Read, Glob, Grep | Read-only — auditor never modifies files |
| Memory | none | Audits should be unbiased by prior sessions |
| Color | red | "Alert / danger" visual signal |

## What Makes This Agent Different from Code Reviewer

The code-reviewer is a peer reviewer looking for bugs and quality issues. The security-auditor is an adversary looking for exploitable vulnerabilities. The security-auditor explicitly traces attack paths, checks for auth bypass, and thinks about how a real attacker would abuse the system — not just whether the code is correct.
