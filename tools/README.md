# Tools

Reusable scripts, utilities, and helper code for AI engineering workflows. These are standalone tools you can drop into a project or run directly — not Claude Code sub-agents or slash commands, but executable code that solves recurring operational problems.

## Planned

The following tools are actively used in production and will be open-sourced here as time allows:

| Tool | Language | What it does |
|------|----------|-------------|
| `chunk-and-index` | Python | Sentence-level chunking + Azure AI Search indexing pipeline with progress tracking |
| `search-eval` | Python | Evaluate retrieval quality against a Q&A test set (citation recall, answer accuracy) |
| `connection-ref-mapper` | Python | Map Power Platform connection references across environments for solution import |
| `ase-dns-validator` | Bash | Validate private DNS resolution for ILB ASE hostnames from within a VNet |
| `fabric-schema-gen` | Python | Generate NLP-to-SQL example queries from a Microsoft Fabric star schema |

## Contributing a Tool

A tool belongs in this directory if it:
- Is a standalone script that can be run with minimal setup
- Solves a problem that appears repeatedly across different AI engineering projects
- Has no equivalent in existing Azure tooling, Power Platform, or Claude Code itself

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the PR checklist.
