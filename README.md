# agents-skills-and-tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Lint skills](https://github.com/zainbaq/agents-skills-and-tools/actions/workflows/lint.yml/badge.svg)](https://github.com/zainbaq/agents-skills-and-tools/actions/workflows/lint.yml)

> A Claude plugin marketplace of pods: small groups of skills that each do one job from start to finish.

## What a pod is

A pod is a small group of skills that serve one specific job and run roughly in order on one piece of work. Each pod is a separate plugin, so you install only the one you need.

A general-purpose collection of unrelated skills is not a pod and does not ship here.

## Pods available

| Pod | Job | Skills |
| --- | --- | --- |
| [`lazycut`](plugins/lazycut/) | Takes raw gameplay footage to a published short-form post. | 9 |

### lazycut

The skills, in the order they usually run:

| Skill | What it does |
| --- | --- |
| `video-analyst` | Produces a timestamped account of a video from sampled frames, plus the facts the creator must confirm. |
| `clip-finder` | Picks clip candidates from an analysed video and returns exact ranges to cut. |
| `clip-batch-planner` | Plans a batch of videos into clip ideas and a posting schedule, and drives the other skills. |
| `video-editor` | Renders one uncut range as a vertical clip with burned-in on-screen text. |
| `voiceover-script` | Writes a timed voiceover script that is separate from the on-screen text. |
| `voiceover-audio` | Generates the voice, places each line on the clip, and ducks the original audio. |
| `post-package` | Writes the per-platform post package and runs a scripted pre-publish gate. |
| `video-research` | Researches competing videos, overlap with past uploads, and thumbnail direction. |
| `youtube-gaming-seo` | Generates YouTube titles, description, tags and a pre-publish checklist for a gaming video. |

**What it needs on your machine:** Python 3 and `ffmpeg`. `video-editor` also needs the `Pillow` package. The local voice route in `voiceover-audio` needs `kokoro-onnx`, `soundfile` and `numpy`, and downloads a voice model of about 350 MB. Each skill lists its own requirements under Inputs.

**Channel brief:** the skills contain no channel names, handles or links. Copy [`channel-brief.example.md`](plugins/lazycut/skills/youtube-gaming-seo/references/channel-brief.example.md), fill it in for your channel, and give its path to the skills that ask for one. Keep the filled-in copy out of public repositories.

## Install

The marketplace is named `zainbaq-pods`.

### In Claude Code

Add the marketplace:

```
/plugin marketplace add zainbaq/agents-skills-and-tools
```

Install one pod:

```
/plugin install lazycut@zainbaq-pods
```

The same two steps from a shell:

```bash
claude plugin marketplace add zainbaq/agents-skills-and-tools
```

```bash
claude plugin install lazycut@zainbaq-pods
```

### In the Claude app

1. Open the **Customize** menu in the left sidebar and go to the **Plugins** tab. In Cowork, open the **Cowork** tab first, then **Customize**.
2. Click **Add**, then **Add marketplace**.
3. Under **Add from a repository**, enter `zainbaq/agents-skills-and-tools`.
4. Open the **Discover** tab, select `lazycut`, and click **Add**.

## Talos

The marketplace also lists `promethean-talos`. It lives in its own repository, [zainbaq/promethean-talos](https://github.com/zainbaq/promethean-talos), and none of its files are in this one. Listing it here means it installs from the same marketplace:

```
/plugin install promethean-talos@zainbaq-pods
```

## Security

- Installing a pod lets Claude run that pod's scripts on your machine. Read the scripts in `plugins/<pod>/skills/*/scripts/` before you install; they are short.
- The lazycut scripts call `ffmpeg` on files you point them to and write only to the output folder you give. Two skills suggest downloads when you choose to use them: a caption font in `video-editor` and a voice model in `voiceover-audio`.
- `promethean-talos` is fetched from a different repository. Review that repository separately.
- This repository contains no credentials. If you find something sensitive, please open an issue.

## Repository layout

| Path | What it is |
| --- | --- |
| `.claude-plugin/marketplace.json` | The marketplace manifest. |
| `plugins/` | One folder per pod. |
| `plugins/lazycut/evals/` | Trigger prompts for each lazycut skill. |
| `scripts/` | Repository checks: `lint_skills.py` and `scrub_check.py`. |
| `archive/` | Older content. See below. |
| `msft/` | Azure AI Search, Copilot Studio and Power Automate reference files. |
| `docs/` | Architecture Decision Records and a Windows setup guide. |
| `tools/` | Standalone utilities. |

`msft/`, `docs/` and `tools/` are reference material. They are not part of the marketplace and are not installed by any pod.

## The archive

[`archive/`](archive/) holds the 22 general-purpose skills and 11 agents this repository used to offer. They are kept for reference, with their history. They are not installed by the marketplace and are not maintained. See [archive/README.md](archive/README.md).

## About

**Syed Zain Ali Baquar** — Senior AI Engineer at a Microsoft solutions partner. Principal at [Promethean Labs](https://promethean.ai).

I build production AI systems using Azure AI Search, Copilot Studio, Claude Code, Power Automate, and Microsoft Fabric.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://linkedin.com/in/zainbaq)
[![X](https://img.shields.io/badge/X-Follow-000000?logo=x)](https://x.com/zainbaq)

Interested in working together? Reach out via [LinkedIn](https://linkedin.com/in/zainbaq) or [Promethean Labs](https://promethean.ai).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). A skill is added only after the task has been done by hand three times, and a pod needs at least three skills serving one job.

## License

MIT — see [LICENSE](LICENSE).
