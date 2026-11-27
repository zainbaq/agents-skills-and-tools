# lazycut trigger evals

Each skill has six cases: three prompts that should load it and three that should not.

| Case folder | What it checks |
| --- | --- |
| `<skill>-trigger-1` to `-3` | The prompt loads the skill. Grader: `graders/skill-fired.md`. |
| `<skill>-no-trigger-1` to `-3` | The prompt does not load the skill. Grader: `graders/must-not-fire.md`. |

The first two "no trigger" prompts for each skill are near misses that belong to a sibling skill in the pod. The third is unrelated to the pod.

The files named in the prompts (for example `footage/boss_fight_01.mp4`) do not exist. These cases test only whether the skill is chosen, not what it produces.

## Running them

Running evals makes real model calls and spends tokens. Nothing here runs automatically.

One skill, one arm, with a spending cap:

```bash
claude plugin eval plugins/lazycut --case "clip-finder-*" --ablation none --max-cost-usd 2
```

Every case:

```bash
claude plugin eval plugins/lazycut --ablation none
```

Each case runs three times by default. Results are written to `evals/results/`, which is listed in `.gitignore`.

## Last run

Run on 2026-11-27 against version 0.1.0, one arm (`--ablation none`):

| Skills | Runs per case | Result |
| --- | --- | --- |
| `clip-finder` | 3 | 6 of 6 cases passed |
| `youtube-gaming-seo` | 3 | 6 of 6 cases passed, after its description was widened to cover "posting to YouTube" requests |
| The other seven skills | 1 | 42 of 42 cases passed |

A single run per case is a weak signal. Rerun with three runs before relying on a result.
