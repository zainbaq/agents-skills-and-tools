# Contributing to agents-skills-and-tools

This is a production reference library first. Contributions that add real patterns from real deployments are welcome. Theoretical or speculative additions are not.

## What Makes a Good Contribution

**Sub-agents and skills**: Should be battle-tested in at least one project. Include the tradeoffs in the `SKILL.md` — what the agent does well and where it falls short.

**Azure AI Search configs**: Must be tested against a live Azure AI Search instance. Include the index schema alongside the indexer config so the two can be validated together.

**Power Automate patterns**: Document the authentication approach explicitly. The most common failure mode is auth — don't leave it out.

**ADRs**: Follow the existing format (Status / Context / Decision / Consequences / Alternatives). Include why the alternatives were rejected with specific reasons, not vague ones.

## How to Contribute

### Adding a New Agent

1. Create a directory under `agents/<agent-name>/`
2. Add three files:
   - `<agent-name>.md` — runtime-ready Claude Code agent (YAML frontmatter + system prompt body)
   - `prompt.yml` — YAML specification document
   - `SKILL.md` — human documentation (what it does, when to invoke, install instructions, examples)
3. Follow the existing agent format. Run the agent in Claude Code against a real codebase before opening the PR.

### Adding a New Skill

1. Create a directory under `skills/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter (`name`, `description`, `allowed-tools`) and the full prompt as the body
3. Test the skill by invoking it via `/skill-name` in Claude Code

### Adding an Azure Pattern

1. Place configs/templates in the appropriate subdirectory under `azure-ai-search/`, `power-automate/`, or `copilot-studio/`
2. Include a README or markdown guide that explains the pattern, the auth approach, and a troubleshooting table

## PR Checklist

Before opening a pull request:

- [ ] Tested locally in Claude Code (for sub-agents and skills)
- [ ] No secrets, connection strings, or subscription IDs in any file
- [ ] YAML frontmatter is valid (no syntax errors)
- [ ] JSON files are valid and pretty-printed with 2-space indent
- [ ] `SKILL.md` documents at least one concrete example invocation
- [ ] If adding an ADR, it uses the existing numbering sequence and format

## Issue Labels

| Label | Use for |
|-------|---------|
| `new-agent` | Proposals for new Claude Code sub-agents |
| `new-skill` | Proposals for new Claude Code skills |
| `azure-pattern` | New Azure AI Search, Power Automate, or Copilot Studio patterns |
| `bug` | Something documented here doesn't work as described |
| `docs` | Documentation improvements |

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct.
