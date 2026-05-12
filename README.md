# agents-skills-and-tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Commit](https://img.shields.io/github/last-commit/zainbaq/agents-skills-and-tools)](https://github.com/zainbaq/agents-skills-and-tools/commits/main)
[![Azure AI](https://img.shields.io/badge/Azure-AI%20Search-0078D4?logo=microsoftazure)](https://azure.microsoft.com/en-us/products/ai-services/ai-search)
[![Claude Code](https://img.shields.io/badge/Claude-Code-D97757?logo=anthropic)](https://claude.ai/code)

> A reusable library of Claude Code sub-agents and slash-command skills covering software engineering, design, marketing, social media, strategy, and daily productivity — built from production use and research into what actually works.

## What's Inside

| Directory | Contents |
|-----------|----------|
| `agents/` | 11 Claude Code sub-agents across engineering, design, marketing, research, and strategy |
| `skills/` | 21 Claude Code slash-command skills for daily work |
| `tools/` | Standalone scripts and utilities for AI engineering workflows |
| `msft/` | Azure AI Search configs, Power Automate patterns, Copilot Studio deployment guides |
| `docs/` | Architecture Decision Records and environment setup guides |

## Who This Is For

- Developers and teams using Claude Code as a daily workflow tool
- Designers, marketers, and strategists who want reusable AI workflows
- AI engineers building RAG pipelines and agent systems on Azure
- Anyone who wants to encode expertise into reusable, team-shareable prompts

## Agents

Sub-agents are `.md` files with YAML frontmatter that Claude Code reads from your `.claude/agents/` directory. Each agent includes a runtime-ready file you can copy directly.

### Engineering Agents

| Agent | What it does |
|-------|-------------|
| `architect` | System design, ADRs, Azure architecture review, RAG pipeline design |
| `code-reviewer` | Code quality, correctness, security, performance, test coverage |
| `security-auditor` | OWASP Top 10, secret scanning, auth bypass, CVE analysis |
| `integration-validator` | API contracts, Azure service integration, resilience patterns |
| `qa-engineer` | Test design, test writing, coverage analysis |

### Design, Marketing & Strategy Agents

| Agent | What it does |
|-------|-------------|
| `content-strategist` | Social media calendars, platform-native copy, campaign content |
| `ux-designer` | UX/UI critique, brand voice auditing, microcopy review, design system docs |
| `research-analyst` | Multi-source synthesis, competitive intelligence, research briefs |
| `data-analyst` | Metric interpretation, insight narratives, dashboard analysis |
| `technical-writer` | SOPs, user guides, runbooks, documentation audits |
| `business-strategist` | SWOT analysis, business cases, competitive positioning (uses Opus) |

### Install an Agent

```bash
# Clone the repo
git clone https://github.com/zainbaq/agents-skills-and-tools.git
cd agents-skills-and-tools

# Project-scoped (checked into your repo's version control)
cp agents/architect/architect.md .claude/agents/architect.md

# User-scoped (available in every project on your machine)
mkdir -p ~/.claude/agents
cp agents/content-strategist/content-strategist.md ~/.claude/agents/
cp agents/ux-designer/ux-designer.md ~/.claude/agents/
cp agents/research-analyst/research-analyst.md ~/.claude/agents/
# ... repeat for any agents you want
```

Or install all agents at once:

```bash
mkdir -p ~/.claude/agents
for agent in agents/*/; do
  name=$(basename "$agent")
  cp "$agent$name.md" ~/.claude/agents/
done
```

Restart Claude Code after copying for agents to be available.

## Skills

Skills are slash commands invoked inside Claude Code with `/skill-name`. Each skill is a single `SKILL.md` file with a YAML frontmatter and a prompt body.

### Engineering Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `implementation-planning` | `/implementation-planning` | Break a feature into sequenced implementation steps |
| `adr-writing` | `/adr-writing` | Generate an Architecture Decision Record |
| `api-design` | `/api-design` | Design a RESTful or GraphQL API with OpenAPI spec |

### Design Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `design-feedback` | `/design-feedback` | Prioritized UX/UI critique with accessibility checks |
| `brand-voice-audit` | `/brand-voice-audit` | Audit copy for brand voice consistency |

### Marketing Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `campaign-brief` | `/campaign-brief` | Full marketing campaign brief with audience, insight, KPIs |
| `email-sequence` | `/email-sequence` | Multi-email sequence with subject lines and CTAs |
| `landing-page-copy` | `/landing-page-copy` | Conversion-focused landing page copy from a brief |

### Social Media Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `social-calendar` | `/social-calendar` | 30-day multi-platform content calendar |
| `social-post-adapt` | `/social-post-adapt` | Adapt content to a specific platform natively |
| `hashtag-strategy` | `/hashtag-strategy` | Tiered hashtag strategy (niche + mid + broad) |

### Productivity Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `meeting-summary` | `/meeting-summary` | Key decisions and action items (owner + deadline) from notes |
| `follow-up-email` | `/follow-up-email` | Post-meeting follow-up email for attendees |
| `status-report` | `/status-report` | Project status report with RAG status, blockers, and next steps |

### Writing & Daily Work Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `exec-summary` | `/exec-summary` | Executive summary surfacing decisions and risks |
| `research-synthesis` | `/research-synthesis` | Synthesize findings across multiple sources |
| `sop-create` | `/sop-create` | Standard operating procedure with steps and troubleshooting |
| `proofread` | `/proofread` | Grammar, clarity, tone, and consistency editing pass |

### Strategy & Analysis Skills

| Skill | Invoke with | What it does |
|-------|-------------|-------------|
| `swot-analysis` | `/swot-analysis` | Evidence-grounded SWOT with strategic synthesis |
| `competitive-analysis` | `/competitive-analysis` | Competitor positioning matrix with gaps and opportunities |
| `data-insights` | `/data-insights` | Plain-language insight narrative from metrics or dashboard data |

### Install Skills

```bash
mkdir -p ~/.claude/commands

# Install individual skills
cp skills/meeting-summary/SKILL.md ~/.claude/commands/meeting-summary.md
cp skills/design-feedback/SKILL.md ~/.claude/commands/design-feedback.md
cp skills/campaign-brief/SKILL.md ~/.claude/commands/campaign-brief.md
# ... repeat for any skills you want
```

Or install all skills at once:

```bash
mkdir -p ~/.claude/commands
for skill in skills/*/; do
  name=$(basename "$skill")
  cp "${skill}SKILL.md" ~/.claude/commands/${name}.md
done
```

Then invoke them in Claude Code:

```
/meeting-summary [paste your meeting notes]
/design-feedback [describe the screen or paste copy]
/campaign-brief Q3 product launch targeting operations managers
/swot-analysis our current market position vs. competitors
/exec-summary [paste the report or document]
/social-calendar B2B SaaS brand, LinkedIn + Instagram, 4x/week
```

## About

**Syed Zain Ali Baquar** — Senior AI Engineer at [HSO](https://www.hso.com). Principal at [Promethean Labs](https://promethean.ai).

I build production AI systems using Azure AI Search, Copilot Studio, Claude Code, Power Automate, and Microsoft Fabric. This repo documents the patterns, decisions, and configurations that actually work in enterprise environments.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://linkedin.com/in/zainbaq)
[![X](https://img.shields.io/badge/X-Follow-000000?logo=x)](https://x.com/zainbaq)

Interested in working together? Reach out via [LinkedIn](https://linkedin.com/in/zainbaq) or the [Promethean Labs consulting page](https://promethean.ai).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
