---
name: status-report
description: >
  Generate a structured project status report with progress, blockers, risks,
  and next steps. Use for weekly team updates, stakeholder reports, or
  executive briefings. Invoke with /status-report followed by the project
  updates, current state, and any blockers or risks to surface.
allowed-tools: Read
---

When this skill is invoked, produce a structured status report that tells stakeholders exactly what they need to know: what's on track, what's at risk, what's blocked, and what's next. A status report is not a journal — it is a decision-support document.

## Before Writing

Gather or clarify:
1. **Project/initiative name and goal**: What are we trying to accomplish?
2. **Reporting period**: What timeframe does this cover?
3. **Audience**: Engineering team, project manager, executive sponsor, client?
4. **Status inputs**: What work was completed? What is in progress? What is blocked?
5. **RAG status**: Red (blocked/at risk of missing milestone), Amber (at risk, can recover), Green (on track)?

## Status Report Structure

```markdown
# Status Report: [Project Name]
**Period**: [e.g., Week of May 12, 2026]
**Prepared by**: [Name/Role]
**Audience**: [Team / Leadership / Client]

---

## Overall Status: [🟢 Green / 🟡 Amber / 🔴 Red]

**One-line summary**: [What is the most important thing to know about this project's current state?]

---

## Progress This Period

**Completed**:
- [Specific deliverable or milestone — not "worked on X"]
- [Be concrete: "Shipped v1.2 to staging" not "did some backend work"]

**In Progress**:
- [What is currently underway — with expected completion if relevant]
- [% complete if meaningful]

---

## Blockers

| Blocker | Impact | Owner of Resolution | Target Resolution Date |
|---------|--------|--------------------|-----------------------|
| [Specific blocker] | [What it blocks, and severity] | [Who needs to act] | [Date] |

[If no blockers: "No current blockers."]

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Specific mitigation in place or planned] |

[If no material risks: "No new risks identified this period."]

---

## Next Period Plan

- [Planned work for the next reporting period]
- [Key milestone or decision coming up]

---

## Decisions Needed

[Any decisions that stakeholders or leadership need to make to unblock progress. Be specific about what is needed and when.]

[If no decisions needed: "No decisions required at this time."]

---

## Key Metrics

| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| [e.g., Sprint velocity] | [n] | [n] | ↑ / → / ↓ |

[Include only if meaningful metrics are available. Skip section if not.]
```

## RAG Status Criteria

**Green**: On track to meet milestones. No active blockers. Known risks are mitigated.

**Amber**: At risk of missing a milestone, but recovery is possible without major scope/timeline change. Blockers exist but have owners and resolution paths.

**Red**: Milestone will be missed without intervention. Blocker has no current resolution path or requires stakeholder decision to unblock.

## Audience Calibration

**Engineering/team report**: Include task-level detail, technical blockers, velocity metrics.

**Executive/leadership report**: Lead with overall status and one-line summary. Focus on milestone risks and decisions needed. Skip implementation detail.

**Client report**: Focus on outcomes and milestones, not internal process. Frame blockers in terms of impact on deliverables. Be honest about Amber status — surprises are worse than proactive transparency.

## Quality Bar

A good status report:
- States the overall status first — readers shouldn't have to read to the end to know if there's a problem
- Distinguishes completed work from in-progress work clearly
- Every blocker has an owner and a resolution target
- Every risk has a stated mitigation (even "monitoring" is better than blank)
- Decisions needed are explicit — not buried in narrative

## Common Mistakes to Avoid

**Activity ≠ progress**: "Spent the week on API development" is activity. "Completed authentication endpoint — API is now feature-complete" is progress.

**Burying bad news**: If the project is Red, it should be Red in the header — not Green in the RAG status with a "we're a bit behind" buried in paragraph 4.

**Vague blockers**: "Waiting on legal" is not a blocker entry. "Legal review of data processing agreement not yet started — blocks deployment to EU region, currently targeting resolution by May 20" is a blocker entry.

**No decisions needed when decisions are needed**: If a project is stalled waiting for a choice, that choice must appear in the "Decisions Needed" section with a clear deadline.
