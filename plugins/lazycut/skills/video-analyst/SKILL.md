---
name: video-analyst
description: "Produces a timestamped account of what happens in a video file, read from sampled still frames, plus the facts the creator must confirm. Use when a video or clip needs to be watched, broken down, timestamped, or checked before editing, clipping, or writing a post package."
---

# Video analyst

**Rules that always hold:**

- You do not watch video. You read still frames sampled from it. Be plain about this.
- Sampled frames miss fast action between samples. Never state a count (hits taken, parries, kills) as fact. Propose it with evidence timestamps and ask the creator to confirm.
- You cannot hear audio. You can only measure loudness. Say so if audio matters. Do not describe music, speech, or sound effects.
- Timestamps from a coarse pass are approximate. Refine any timestamp that will be used as a trim point.
- The creator is the source of truth for run quality (no damage, hit counts, first try). If they have not stated it, ask.
- Do not give opinions on whether the video will perform. Report what is there.

Turn a video file into a timestamped account of what happens in it, plus the facts the creator must confirm. Other skills (video-editor, youtube-gaming-seo) build on this output, so accuracy matters more than polish.

## Inputs

- **Video path** (required): the path to the video file. Keep it read-only. If the file is missing or zero-length, say it did not arrive and ask for it again.
- **Output folder** (required from a caller; default `lazycut-out/analysis/<video name>/` in the working directory): where contact sheets, `analysis.json`, and the report are written. It must not be the folder holding the video.
- **Creator-confirmed facts** (optional): run-quality statements such as no damage, hit counts, first try.
- **Requirements**: Python 3 (standard library only) and `ffmpeg` with `ffprobe` on the path. Web search for step 5.

## Process

Run `scripts/analyze.py` (relative to this skill's folder). Run it; do not read it into context. `OUT` below is the output folder.

1. Coarse pass: `python3 scripts/analyze.py VIDEO OUT/`. It prints duration, size, sample rate, dead-time ranges, and writes timestamped contact sheets `OUT/sheet_NN.jpg` (12 frames each) plus `OUT/analysis.json` with a 0.5 s motion track. Read every sheet with the Read tool.
2. Refine pass: for each moment that matters (hook, payoff, any candidate trim point, any claimed count), re-run on a narrow window at higher rate, for example `--start 24 --end 36 --fps 4` into a separate subfolder. Use up to 10 fps on windows of a few seconds.
3. Read on-screen text: `--zoom T X Y W H` writes one enlarged crop (source pixel coordinates). Use it for HUD panels, objective text, prompts, names, and watermarks. Quote game text exactly as shown.
4. For videos longer than about 5 minutes, the coarse pass drops below 1 frame per second. Say so, then refine the windows the motion track marks as high, plus the first 10 seconds and the ending.
5. Research: web-search every proper noun read off the screen (game, mission, boss, character, vehicle, location) for canonical spelling and context. Correct the user's misspellings. Skip thin AI-written guide sites.

## Outputs

Write the report to `OUT/report.md` and report that path back, along with the paths of `OUT/analysis.json` and the contact sheets. Then give the same report in the reply.

Keep the report short and scannable. Lead with a one-line summary of what happens.

- **Basics**: duration, resolution, orientation, whether audio exists, capture quality (direct capture vs phone recording of a screen, watermarks, letterboxing, HUD position).
- **Timeline**: one line per beat, `M:SS-M:SS` then what happens. Mark the peak (the most striking 2 to 3 seconds).
- **On-screen text**: exact text, where it sits, when it appears.
- **Facts to confirm**: each proposed fact with evidence timestamps and `certain` or `uncertain`. Anything that could become a title claim goes here.
- **Dead time**: ranges with little motion, from the script, checked against the frames.
- **Framing**: would a centred 9:16 crop cut off the action or HUD text that the story needs? Name the timestamps.
- **First frame and last frame**: one sentence each.

## Notes

- Contact-sheet images are downscaled when read. For coordinates, work from the source resolution reported by the script, not from the sheet.
- The dead-time threshold (0.08) is tuned loosely. Dark night scenes score low even when things happen, so check flagged ranges against frames before calling them dead.
