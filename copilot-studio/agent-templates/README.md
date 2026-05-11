# Copilot Studio Agent Templates

Reference configurations and design patterns for enterprise Copilot Studio agents. Each template documents the architecture, topic design, integration approach, and known failure modes for a common enterprise AI use case.

---

## Template 1: RAG-Powered Knowledge Base Agent

### What It Does

Answers questions against a private document corpus using Azure AI Search hybrid semantic search. Returns answers with citation links to source documents. Suitable for compliance, policy lookup, technical documentation, and internal knowledge bases.

### Architecture

```
User Question
    │
    ▼
Copilot Studio — Generative Answers action
    │
    ├── [Option A: Native knowledge source]
    │   └── Azure AI Search data source (max 5 results — limited)
    │
    └── [Option B: Power Automate action — recommended for production]
        └── Hybrid Search Flow (see power-automate/hybrid-semantic-search-flow/)
            ├── Azure OpenAI: generate query embedding
            ├── Azure AI Search: hybrid query (50–100 results)
            └── Return citations array to Copilot Studio
```

For production deployments serving compliance or research use cases, use Option B. The native knowledge source's 5-result cap is insufficient when the relevant answer may be in document 12 of 10,000.

### Key Configuration

**Authentication**: Configure the Power Automate connection with Managed Identity. Do not use API keys — they cannot be rotated without updating every agent that references them.

**Generative Answers node settings**:
- Enable content moderation for enterprise context
- Set "No answer found" fallback to a specific topic that escalates or directs the user to a human contact
- Configure citations to display `file_name` and `page_number` (not just the raw blob URL)

**System prompt for the generative answers node**:
```
You are a compliance assistant. Answer questions using only the retrieved document excerpts provided.
If the answer is not found in the excerpts, say "I could not find this in the provided documents."
Always include the document name and page number when citing a source.
Do not speculate beyond what the documents say.
```

### Topic Design

**When to use Topics vs Generative Answers**:
- Use Topics for structured, multi-step flows (collect information → submit a form → confirm)
- Use Generative Answers for open-ended questions against a knowledge base
- Combine both: Topics as the entry point for intent disambiguation, Generative Answers for the lookup

**Out-of-scope handling**: Every Generative Answers agent needs an explicit "I don't know" path. Configure the fallback to say "This question is outside my knowledge area" and route to a handoff topic that captures the question for human review.

**Escalation pattern**:
```
Topic: Escalate to Human
Condition: User requests human, or Generative Answers returns no result twice
Action: Send Teams adaptive card to a support channel OR transfer to Omnichannel
```

### Testing Checklist

Before go-live:
- [ ] Test with 20+ representative questions, verify citations resolve to correct documents
- [ ] Test with out-of-scope questions — confirm graceful fallback, not hallucination
- [ ] Test with ambiguous questions — confirm clarification prompt triggers
- [ ] Verify authentication works for all user groups (not just the builder's account)
- [ ] Confirm telemetry is flowing to Application Insights or Dataverse Analytics

---

## Template 2: Process Automation Agent

### What It Does

Guides users through a multi-step business process by collecting information conversationally and triggering Power Automate flows at each decision point. Examples: document submission, approval requests, leave requests, IT ticket creation.

### Architecture

```
User Intent
    │
    ▼
Copilot Studio Topic (slot-filling conversation)
    │
    ├── Collect structured data (entity extraction)
    │   ├── Name, date, category, etc.
    │   └── Validate each input before proceeding
    │
    ├── Confirmation step ("Submit this request?")
    │
    └── Power Automate HTTP action
        ├── Create record in Dataverse / SharePoint / ServiceNow
        └── Send notification to approver
```

### Key Design Patterns

**Slot filling**: Use entities (prebuilt or custom) to extract structured data from natural language. Define entities for categories, dates, amounts — not free-text fields where validation is important.

**Confirmation before action**: Always ask for confirmation before triggering an irreversible action. Present a summary card ("You are about to submit a leave request from May 15 to May 20. Confirm?") and require an affirmative response.

**Error handling for Power Automate failures**: Check the HTTP response status from the flow action. On error, surface a user-friendly message ("Something went wrong. Your request was not submitted. Please try again or contact support."). Log the error with the conversation ID for debugging.

**Draft-and-edit pattern**: For complex forms, allow users to review and edit individual fields before final submission rather than restarting from scratch.

### Sample Topic Flow

```
Trigger: "submit leave request", "request time off", "vacation request"
    │
    ├── Ask: Start date (validate: is in the future, is a workday)
    ├── Ask: End date (validate: is after start date)
    ├── Ask: Leave type (entity: Annual / Sick / Personal)
    ├── Ask: Reason (optional)
    │
    ├── Show confirmation card
    │   ├── [Yes] → Trigger Power Automate flow → Success message
    │   └── [No]  → "What would you like to change?" → Branch back
    │
    └── On flow error: Error topic (log + user message)
```

---

## Template 3: Enterprise Helpdesk Agent

### What It Does

First-line IT or HR helpdesk agent that handles common requests (password reset, VPN access, software installation, policy questions) and escalates to ServiceNow or a ticketing system when it cannot resolve the request.

### Architecture

```
User Issue
    │
    ▼
Copilot Studio — Intent classification
    │
    ├── Self-service resolution topics (cover 70–80% of volume)
    │   ├── Password reset → AAD Self-Service Password Reset flow
    │   ├── VPN setup → Knowledge base lookup (RAG template above)
    │   ├── Software request → Approval flow (Process Automation template above)
    │   └── Policy question → Document search
    │
    └── Escalation topic (remaining 20–30%)
        ├── Capture: issue description, urgency, user details
        ├── Create ServiceNow ticket via Power Automate
        └── Confirm: ticket number to user
```

### Deflection Measurement

The primary KPI for a helpdesk agent is deflection rate — the percentage of sessions resolved without human escalation. Set up Dataverse or Application Insights logging from day one to track:
- Sessions started vs escalated
- Top escalation reasons (unresolved intents, repeated failures)
- Resolution time for self-service vs escalated tickets

Target 60–70% deflection in the first 90 days, increasing as new resolution topics are added based on escalation patterns.

### Agent Design Principles

**Keep topics focused**: Each topic should resolve one specific intent. Avoid "mega-topics" that try to handle multiple issue types with complex branching.

**Always provide an exit**: Every topic must have a path to "talk to a human." Remove this and users get frustrated and lose trust in the agent.

**Measure, then expand**: Launch with the 5–10 highest-volume issues. Add topics based on actual escalation data, not assumptions about what users will ask.

**Don't fake knowledge**: If the agent doesn't know the answer, it should say so and escalate — never hallucinate a policy or procedure.
