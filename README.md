# agents-skills-and-tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Commit](https://img.shields.io/github/last-commit/zainbaq/agents-skills-and-tools)](https://github.com/zainbaq/agents-skills-and-tools/commits/main)
[![Azure AI](https://img.shields.io/badge/Azure-AI%20Search-0078D4?logo=microsoftazure)](https://azure.microsoft.com/en-us/products/ai-services/ai-search)
[![Claude Code](https://img.shields.io/badge/Claude-Code-D97757?logo=anthropic)](https://claude.ai/code)

> A production reference library of Claude Code sub-agents, skills, Azure AI Search indexer configs, Power Automate flow patterns, and Copilot Studio deployment guides — built from real enterprise AI engineering work.

This repo is a byproduct of shipping production AI systems. Everything here has been deployed, debugged, and iterated on in live environments. Nothing is theoretical.

## What's Inside

| Directory | Contents |
|-----------|----------|
| `agents/` | 5 Claude Code sub-agents: architect, code-reviewer, security-auditor, integration-validator, qa-engineer |
| `skills/` | 3 Claude Code slash-command skills: implementation-planning, adr-writing, api-design |
| `tools/` | Standalone scripts and utilities for AI engineering workflows |
| `azure-ai-search/` | Hybrid semantic search indexer configs, field mapping guides, chunking strategies |
| `power-automate/` | Flow patterns for RAG pipelines and private Azure Function connectors |
| `copilot-studio/` | Agent templates and dev-to-prod deployment guides via Power Platform pipelines |
| `docs/` | Architecture Decision Records and environment setup guides |

## Who This Is For

- AI engineers building RAG pipelines on Azure
- Teams adopting Claude Code as an engineering workflow tool
- Architects evaluating Copilot Studio for enterprise deployment
- Anyone debugging the gap between Azure AI documentation and production reality

## Using the Claude Code Sub-Agents

Sub-agents are `.md` files with YAML frontmatter that Claude Code reads from your `.claude/agents/` directory. Each sub-agent in this repo includes a runtime-ready `<agent-name>.md` file you can copy directly.

```bash
# Clone the repo
git clone https://github.com/zainbaq/agents-skills-and-tools.git
cd agents-skills-and-tools

# Install a single sub-agent (project-scoped — checked into your repo)
cp agents/architect/architect.md .claude/agents/architect.md

# Or install all agents globally (available in every project)
mkdir -p ~/.claude/agents
cp agents/architect/architect.md ~/.claude/agents/
cp agents/code-reviewer/code-reviewer.md ~/.claude/agents/
cp agents/security-auditor/security-auditor.md ~/.claude/agents/
cp agents/integration-validator/integration-validator.md ~/.claude/agents/
cp agents/qa-engineer/qa-engineer.md ~/.claude/agents/
```

Restart Claude Code after copying files for the agents to be available.

## Using the Skills

Skills are slash commands you invoke inside Claude Code with `/skill-name`. Copy the `SKILL.md` files to your `.claude/skills/` directory:

```bash
mkdir -p ~/.claude/skills
cp skills/implementation-planning/SKILL.md ~/.claude/skills/implementation-planning.md
cp skills/adr-writing/SKILL.md ~/.claude/skills/adr-writing.md
cp skills/api-design/SKILL.md ~/.claude/skills/api-design.md
```

Then invoke them in Claude Code:
```
/implementation-planning Add OAuth2 login to the API
/adr-writing auth pattern selection
/api-design extraction-jobs resource
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
