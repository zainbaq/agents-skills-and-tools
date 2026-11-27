---
name: implementation-planning
description: >
  Walk through a structured implementation plan for any feature or system change.
  Use when asked to plan an implementation, before starting a complex task, or
  when you need to break down a requirement into ordered engineering steps with
  clear acceptance criteria.
allowed-tools: Read, Glob, Grep, WebFetch
---

When this skill is invoked, guide through a complete implementation plan. Read the relevant codebase first — never plan in the abstract when you can see the actual code.

## Step 1: Understand the Requirements

Identify or ask for:
- What is the user-visible behavior being added or changed?
- What are the acceptance criteria — how do we know it's done?
- What are the constraints? (performance targets, backward compatibility, security requirements, deployment window)

## Step 2: Map the Affected Surface

Read existing files to identify:
- Which files will be created or modified?
- What database schema changes are needed (and how will existing data be migrated)?
- What API contracts change — and are there consumers that need to be notified or versioned?
- What configuration or environment variables are added?
- What external services or dependencies are involved?

Use Glob and Grep to discover the actual file structure before listing affected files.

## Step 3: Design the Implementation

Produce a numbered, ordered list of implementation steps. Each step must:
- Be independently completable and testable
- Specify the file(s) to be created or modified
- Include the test or verification that confirms the step is complete
- Call out dependencies on prior steps explicitly

**Sequence steps so the system is always in a deployable state.** Incomplete features should be unreachable until the final step. For Power Platform deployments (Copilot Studio agents, Power Automate flows), plan solution export/import steps as discrete checkpoints between dev, UAT, and production — not as an afterthought.

## Step 4: Identify Risks

List risks in this format: `[RISK]` Description → Mitigation

Common risks specific to AI engineering projects:

- **Auth pattern mismatch between environments**: if dev uses API keys and production uses managed identity, this won't surface until production deployment. Plan auth validation as a step, not an assumption.
- **Context window budget not validated**: a RAG pipeline that works with 10 test documents may fail silently when retrieving 50 results from a 10,000-document corpus. Include a context window size check in the implementation plan.
- **Power Platform connection references**: when a solution moves between environments, all connection references must be mapped to target-environment connections before import. Add this as an explicit pre-deployment step.
- **Python package version compatibility on Windows**: PyO3-dependent packages (pydantic-core, cryptography) are compiled against a specific Python minor version. Plan for explicit Python version pinning in `pyproject.toml` or `.python-version` if the team includes Windows developers.
- **Azure AI Search semantic tier requirement**: semantic reranking requires S1 tier or higher. If the plan involves adding semantic search to an existing Basic-tier search service, tier upgrade is a prerequisite step.
- Breaking changes to public APIs (requires versioning or deprecation notice)
- Data migrations on large tables (requires estimated duration and rollback plan)

## Step 5: Complexity Estimate

Rate each step:
- **S** — under 2 hours (single function or config change)
- **M** — 2–8 hours (a feature with tests)
- **L** — 1–3 days (a subsystem or new integration)
- **XL** — over 3 days (break it down further before starting)

## Output Format

```markdown
## Implementation Plan: [Feature Name]

[One-paragraph summary of what is being built and why]

### Affected Files
- `path/to/file.py` — description of change
- `path/to/new_file.py` — new file, purpose

### Steps

1. [S] Step description
   - Files: `path/to/file.py`
   - Done when: specific, observable acceptance criterion

2. [M] Step description
   - Files: `path/to/file.py`, `tests/test_feature.py`
   - Depends on: step 1
   - Done when: specific criterion

### Risks
- [RISK] Description → Mitigation

### Out of Scope
- Explicit list of related things not included in this plan
```
