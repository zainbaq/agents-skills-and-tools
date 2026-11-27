---
name: clip-batch-planner
description: "Plans and runs a batch of gameplay videos into short-form posts: clip ideas, distinct angles, a posting schedule, and the order to run the other video skills. Use when several video files are handed over, when clip ideas are wanted, or when a posting schedule is needed."
---

# Clip batch planner

**Rules that always hold:**

- Plan before files. Do not render anything until the user approves the plan from stage 4.
- After approval, finish one clip end to end and show it before batch-running the rest, so one correction applies to all of them.
- This skill does not auto-post. Output is files and copy-paste packages.
- It cannot see view counts or analytics unless the user shares them.
- This skill writes no captions or scripts itself. It decides what gets made and when, then drives the other skills in order.

Turn a pile of gameplay files into a planned run of Shorts, Reels, and TikToks.

## Inputs

- **Video paths** (required): the path of every file in the batch. If a file is missing or zero-length, say it did not arrive.
- **Output folder** (required from a caller; default `lazycut-out/batch/` in the working directory): each file's analysis goes in its own subfolder.
- **Channel brief path** (optional): read it first when one is given.
- **Answers to the intake questions** (ask once, in a single message, if not already supplied):
  - Which files are already finished clips, and which need clips found?
  - Any run-quality facts to state (no damage, first try, counts)?
  - Voiceover on all, some, or none?
  - Which platforms, and how many posts per day?
- **Requirements**: the other lazycut skills and their requirements. Web search for names.

## Process

### The pipeline

Run these stages in order. Each names the skill that does the work.

1. **Intake** (this skill): list every file with duration, shape, and capture quality.
2. **Analyse**: video-analyst on every file.
3. **Find clips**: clip-finder on every file, UNLESS the user says a file is already the clip. Then the whole file is the range; only check its first and last second for a clean start and end.
4. **Ideas and schedule** (this skill): see below. STOP here and show the plan.
5. **On-screen text and phone format**: video-editor, one clip at a time.
6. **Voiceover script**: voiceover-script.
7. **Voice and mix**: voiceover-audio.
8. **Post package and gate**: post-package for each platform.

When calling another skill, pass it explicit file paths and an output folder under this batch's output folder.

### Intake

Run `../video-analyst/scripts/analyze.py` on each file and build one table: file, duration, resolution, direct capture or phone recording of a screen, HDR or not, watermark or not, has audio. Flag watermarked files and ask for originals.

Batches are heavy. Work through files one at a time and keep each file's analysis in its own folder. If the files are large or many, say how many you can handle per message and ask for the rest in the next one.

### Clip ideas

For every candidate clip, write an idea card:
- **Working title**: plain language, first person.
- **Angle**: one of: plan goes wrong, clean execution, tip or trick, discovery (location, vehicle, secret), comedy or chaos, comparison with an earlier game.
- **Hook**: what the first two seconds promise.
- **Payoff time**: seconds into the clip.
- **Searchable**: the phrase someone would type for this, if any (mission name, vehicle, location). Research names with web search; never guess spellings.
- **Strength**: strong, usable, or weak, with one reason.

Rules:
- No two posted clips share both the same angle and the same subject. Merge or drop duplicates and say which.
- Mark weak clips honestly. A short strong list beats a long padded one.
- Suggest missing clips too: if the batch shows a series forming (every vehicle for one character, every mission in a chain), name the clips that would complete it and what to record.
- Sampled frames miss fast action and there is no audio. Anything that depends on a count or a sound goes in a "confirm" column.

### Schedule

Build a posting calendar from the approved ideas.

- Lead with the strongest clip. Put the second strongest about a third of the way in and a strong one last.
- Alternate angles day to day. Never post two clips of the same subject back to back.
- Clips tied to a game's launch window or to something searchable go first; evergreen comedy can wait.
- Group series clips so they can share a playlist and point at each other.
- Default cadence when the user gives none: one Short per day, the same clip to Reels and TikTok the same day, with platform-specific packages.
- Posting time: use the user's own analytics when they share them. Without analytics, propose one consistent evening slot in the user's time zone and label it as a starting assumption to test, not a known best time.
- Each row: date, time, platform, clip, angle, title, status (planned, rendered, packaged, posted).

## Outputs

Write these to the output folder and report each path back:

- `intake.md`: the intake table.
- `ideas.md`: the idea cards.
- `schedule.csv`: the schedule as a table to fill in and sort (a sheet when the session offers one), since the user will update status as they post.
- `status.md`: a running status of every clip, so a batch interrupted mid-way can resume.

After each stage, say in a few lines what was produced and what needs the user's answer.
