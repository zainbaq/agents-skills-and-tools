# Contributing

This repository is a Claude plugin marketplace of pods. A pod is a small group of skills that serve one specific job and run roughly in order on one piece of work. Contributions are welcome when they meet the two admission rules below.

## Admission rules

1. **A skill is added only after the task has been done by hand three times.** A skill records a way of working that has already proved itself. If the task has not been done by hand three times, it is too early to know what the skill should say.
2. **A pod needs at least three skills serving one job.** A collection of unrelated skills is not a pod. If the skills do not share one job and one piece of work, they do not ship together.

## Repository layout

| Path | What it is |
| --- | --- |
| `.claude-plugin/marketplace.json` | Lists every pod, and any external plugin. |
| `plugins/<pod>/` | One pod. Installing a pod copies only this folder. |
| `plugins/<pod>/.claude-plugin/plugin.json` | The pod's manifest. Its `name` must equal the folder name and the marketplace entry. |
| `plugins/<pod>/skills/<skill>/` | One skill: `SKILL.md`, plus `scripts/` and `references/` when needed. |
| `plugins/<pod>/evals/` | Trigger prompts for each skill, in the layout `claude plugin eval` expects. |
| `scripts/` | Repository checks. Not part of any pod. |
| `archive/` | Old content. Not installed, not maintained. Do not add to it. |
| `msft/`, `docs/`, `tools/` | Reference material, separate from the marketplace. |

A pod cannot reference a file outside its own folder, because installing copies only that folder.

## Rules for every skill in a pod

Skills must work in the Claude app, in Claude Code, and when called by a subagent that has no conversation history.

**Frontmatter**

- Only `name` and `description`. Other keys are rejected outside Claude Code.
- `name`: lowercase letters, numbers and hyphens, at most 64 characters, the same as the folder name.
- `description`: third person, at most 1,024 characters. Say what the skill does first, then when to use it.

**Body**

- Critical rules go in the first lines, before anything else. Only the start of a skill survives a long conversation being compacted.
- Then three headings in this order: `## Inputs`, `## Process`, `## Outputs`.
- Inputs are explicit: a file path or stated values, never "the video we discussed".
- Outputs are files written to a path the caller gives, with the path reported back.
- Keep the file under 500 lines. Move long reference material into a file one level down and link to it.

**Scripts**

- Scripts live in `scripts/` inside the skill folder and are referred to by relative path.
- The skill tells Claude to run the script, not to read it.
- Standard library first. If a script needs anything else (ffmpeg, a pip package), the skill lists it under Inputs.
- Anything that must hold every time is enforced by a script the skill runs, not by a sentence.

**Content**

- No channel-specific or organisation-specific facts. Where a skill needs them, it reads a brief the caller points to.
- No client, employer or personal names. No table names, endpoints or credentials.

## Checks to run before a push

Run these from the repository root. All three must pass.

```bash
python scripts/lint_skills.py
```

Checks frontmatter keys, name and description limits, the three headings, the 500-line limit, and that every referenced script exists. This also runs in GitHub Actions on every push and pull request.

```bash
python scripts/scrub_check.py
```

Fails if a blocked term appears in any file that could be pushed. The terms come from a file named `.scrub-blocklist` in the repository root, which you create yourself: one term per line, with client names, employer names and anything else that must never appear here. That file is listed in `.gitignore` and must never be committed. With no blocklist file the script prints a warning and passes, so it only protects you once the file exists. Run it before every push.

```bash
claude plugin validate .
```

Checks the marketplace manifest and each pod's `plugin.json`. This is a local step and is not run in GitHub Actions.

## Pull request checklist

- [ ] The two admission rules are met, and the pull request says how.
- [ ] `lint_skills.py`, `scrub_check.py` and `claude plugin validate .` all pass.
- [ ] Every new skill has three prompts that should trigger it and three that should not, under `plugins/<pod>/evals/`.
- [ ] No secrets, connection strings, names or internal identifiers in any file.
- [ ] Nothing in `msft/`, `docs/`, `tools/` or `archive/` was changed as a side effect.

## Code of conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct.
