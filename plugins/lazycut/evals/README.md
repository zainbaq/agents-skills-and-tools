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

These cases have not been run yet. Treat the first run as a check of the cases themselves as much as of the skills.
