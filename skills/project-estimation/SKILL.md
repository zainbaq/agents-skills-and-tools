---
name: project-estimation
description: >
  Create a well-informed project effort estimate from requirements, discovery notes,
  architecture decisions, or a proposed solution. Use when asked to estimate delivery
  effort, staffing, timeline, sprint plan, week-by-week allocation, or Excel-ready
  project estimates. Produces padded, stakeholder-ready estimates with activities,
  assumptions, in-scope/out-of-scope items, risks, and role-by-role hour allocation.
allowed-tools: Read, Glob, Grep, WebFetch, Bash
---

When this skill is invoked, produce a practical delivery estimate that a project manager, solution architect, or client stakeholder can use for planning and commercial discussion. The estimate should be grounded in the provided requirements and, when relevant, the actual repository or technical artifacts. Do not estimate in the abstract when documents, code, or architecture notes are available.

The goal is not to produce the lowest possible number. The goal is to produce a credible, padded estimate that accounts for discovery gaps, integration risk, testing, review, deployment, and project overhead.

## When to Use This Skill

Use this skill for requests like:

- "Estimate how long this project will take."
- "Break this solution into activities and hours."
- "Create a week-by-week effort plan for two developers."
- "Turn this architecture into an implementation estimate."
- "Create an Excel estimation workbook."
- "Estimate MVP, phase 2, and optional scope."
- "Build a client-ready estimate from this requirements document."

## Step 1: Understand Inputs and Constraints

Before estimating, identify:

1. **Project objective**: What business problem is being solved?
2. **Delivery scope**: What is included in phase 1 / MVP?
3. **Known exclusions**: What has been deferred or explicitly ruled out?
4. **Team model**: Number of developers, roles, hours per week, expected availability.
5. **Timeline constraints**: Hard deadlines, pilot dates, stakeholder review windows.
6. **Technical stack**: Cloud provider, frameworks, databases, AI services, integration points.
7. **Artifacts available**: Requirements docs, architecture diagrams, sample data, repo code, designs.
8. **Output format**: Markdown estimate, CSV, Excel workbook, project plan, or SOW-ready text.

If the user provided explicit constraints, honor them exactly. For example, if they say two developers at 20 hours/week each, calculate weekly capacity as 40 hours/week total and do not assume full-time availability.

## Step 2: Read Relevant Material First

Use available tools to inspect:

- Requirements documents
- Architecture notes
- Existing codebase structure
- README / deployment docs
- Data model or API contracts
- Prior estimates or implementation plans

When the estimate depends on current platform capabilities, use `WebFetch` to verify official documentation. Prefer official vendor documentation over blogs, especially for Azure, Microsoft, AWS, GCP, Salesforce, OpenAI, or framework-specific capabilities.

## Step 3: Define Estimation Assumptions

Every estimate must include assumptions. At minimum, state:

- Number of developers and weekly availability
- Total weekly capacity
- Whether hours are engineering hours only or include PM/QA/design
- Whether infrastructure is already available
- Whether sample data and test users are available on time
- Whether security reviews, procurement, and compliance approvals are included
- Whether production support / hypercare is included
- Padding approach, such as 15-30% built into activity estimates

Use generous padding for:

- AI/RAG systems
- Data ingestion and document parsing
- Authentication and environment setup
- Search quality tuning
- Evaluation and testing
- Client review cycles
- Unknown data quality issues
- Deployment permissions and enterprise network constraints

## Step 4: Break Work into Activities

Create activity groups that are concrete, testable, and tied to deliverables. For software/AI projects, a good structure is:

1. Discovery validation and backlog refinement
2. Solution architecture and technical design
3. Environment setup and DevOps foundation
4. Data model and storage design
5. Ingestion pipeline implementation
6. Document parsing and normalization
7. Search / indexing / retrieval setup
8. AI prompt and orchestration design
9. Core backend/API development
10. Frontend or user interface development
11. Structured output/report generation
12. Security, auth, and RBAC
13. Evaluation, test harnesses, and quality tuning
14. User acceptance testing support
15. Deployment and release readiness
16. Documentation and handoff
17. Project management, demos, and stakeholder reviews
18. Contingency / stabilization buffer

Adjust these to the project. Do not include irrelevant activities just to make the plan look complete.

## Step 5: Allocate Hours by Role or Developer

For each activity, provide:

- Activity name
- Description / deliverable
- Dev A hours
- Dev B hours
- Total hours
- Notes / assumptions

When assigning hours:

- Put architecture, backend, DevOps, data modeling, and integration-heavy tasks primarily on Dev A if no other roles are specified.
- Put frontend, UX flow, testing support, documentation, and report formatting primarily on Dev B if no other roles are specified.
- Share cross-cutting tasks like testing, UAT, tuning, and deployment.
- Do not exceed each developer's weekly capacity in the week-by-week plan.
- Include review/demo/project coordination time unless a PM is explicitly provided separately.

## Step 6: Build a Week-by-Week Plan

Create a weekly allocation that respects capacity constraints.

For each week, include:

- Week number
- Main focus
- Dev A hours
- Dev B hours
- Total hours
- Major activities
- Expected deliverables / checkpoint

Rules:

- Do not exceed stated weekly capacity per developer.
- Preserve realistic sequencing. For example, do not schedule UAT before the first usable build exists.
- Include overlap between development and testing once the first slice is ready.
- Include stakeholder review checkpoints at natural milestones.
- Include stabilization near the end.

## Step 7: State In-Scope and Out-of-Scope Clearly

Include a dedicated **In Scope** section with the activities included in the estimate.

Also include an **Out of Scope / Not Included** section. Examples:

- Production support beyond hypercare
- Advanced analytics or model fine-tuning
- Pricing optimization
- Complex integrations not named in requirements
- Full data migration from legacy systems
- Security remediation outside the application boundary
- Mobile app support
- Ongoing managed services

This prevents the estimate from being interpreted as unlimited scope.

## Step 8: Include Risks and Estimate Drivers

Include a short risk table:

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data quality issues | More parsing and tuning time | Use representative sample documents early |
| Auth/environment access delays | Blocks development and deployment | Validate access in week 1 |
| Search quality below expectations | Additional tuning needed | Build evaluation set and feedback loop |

Also include major estimate drivers, such as:

- Number and complexity of integrations
- Number of document formats
- Quality of sample data
- Security and compliance review depth
- Need for production-grade observability
- Complexity of UI workflow

## Step 9: Excel Workbook Output Requirements

When the user asks for Excel, create a workbook with clear tabs. Recommended tabs:

1. **Summary**
   - Project name
   - Estimate date
   - Team assumptions
   - Total hours
   - Total weeks
   - Weekly capacity
   - High-level notes

2. **Activity Estimate**
   - Activity ID
   - Workstream
   - Activity
   - Description
   - Dev A Hours
   - Dev B Hours
   - Total Hours
   - Dependencies
   - Notes

3. **Weekly Plan**
   - Week
   - Focus
   - Dev A Hours
   - Dev B Hours
   - Total Hours
   - Activities
   - Deliverables / checkpoint

4. **Scope & Assumptions**
   - In-scope activities
   - Out-of-scope items
   - Assumptions
   - Constraints

5. **Risks**
   - Risk
   - Probability
   - Impact
   - Mitigation

6. **Sources**
   - Requirements files reviewed
   - Architecture docs reviewed
   - Official documentation referenced

Excel formatting standards:

- Bold header rows
- Freeze top row on tabular sheets
- Auto-size columns where possible
- Use numeric formats for hours
- Include totals at the bottom or top of relevant sheets
- Keep text wrapped for long descriptions
- Avoid over-styling; make it client-readable

If creating the Excel file with Python, use `openpyxl` or an equivalent library. Do not rely on screenshots or manual formatting. Validate that the workbook saves correctly.

## Step 10: Output a Clear Summary

After creating the estimate, summarize:

- Total hours
- Total weeks
- Weekly capacity assumption
- Number of developers
- Major included workstreams
- Key caveats
- Link to the generated file if one was created

## Output Format for Markdown Estimates

When not exporting to Excel, use this structure:

```markdown
# Project Effort Estimate: [Project Name]

## Summary

| Item | Estimate |
|------|----------|
| Team | [e.g., 2 developers] |
| Availability | [e.g., 20 hrs/week each] |
| Weekly Capacity | [e.g., 40 hrs/week] |
| Total Estimated Effort | [hours] |
| Estimated Duration | [weeks] |
| Padding Included | [yes/no and approach] |

## In Scope

- [Activity]
- [Activity]

## Assumptions

- [Assumption]
- [Assumption]

## Activity Estimate

| ID | Workstream | Activity | Dev A | Dev B | Total | Notes |
|----|------------|----------|------:|------:|------:|-------|
| 1 | Discovery | Requirements validation | 8 | 4 | 12 | Includes stakeholder review |

## Week-by-Week Plan

| Week | Focus | Dev A | Dev B | Total | Deliverable |
|------|-------|------:|------:|------:|-------------|
| 1 | Discovery + architecture | 20 | 20 | 40 | Validated backlog |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

## Out of Scope

- [Excluded item]
```

## Quality Bar

A good estimate:

- Is traceable to actual requirements or architecture
- Respects stated capacity constraints
- Includes padded hours, not optimistic best-case hours
- Separates activity estimates from calendar schedule
- Includes in-scope and out-of-scope items
- Names assumptions clearly
- Includes testing, UAT, deployment, documentation, and stabilization
- Is understandable to both technical and non-technical stakeholders

## Common Mistakes to Avoid

**Mistake: Only estimating coding time.**
Include discovery, setup, testing, review, deployment, documentation, and handoff.

**Mistake: Ignoring part-time capacity.**
If developers have 20 hours/week, do not schedule them as if they are full-time.

**Mistake: Treating AI tools as eliminating engineering effort.**
AI tools can speed up coding and drafting, but they do not remove integration, testing, security, review, and debugging work. Use AI acceleration as a reason to improve throughput, not to remove padding.

**Mistake: Hiding uncertainty.**
Call out unknowns and include a contingency buffer.

**Mistake: Over-precision.**
Do not pretend an estimate is exact. Use ranges when appropriate, but provide a planning number when the user needs one.

**Mistake: No acceptance checkpoints.**
Each major phase should have a tangible checkpoint or deliverable.
