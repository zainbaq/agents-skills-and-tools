---
name: clip-finder
description: "Picks short-form clip candidates out of an analysed video and returns ranked, frame-snapped time ranges ready to render. Use when Shorts, Reels, or TikTok clips need to be picked out of a longer video, when the best moments are wanted, or when a clip is described by prompt and has to be found."
---

# Clip finder

**Rules that always hold:**

- Never propose ranges from a guess. Work only from a video-analyst report. If there is none, run video-analyst first.
- One continuous range per clip, minimum 3 s, inside the video bounds. Never stitch ranges.
- Sampled frames miss fast action. Do not promise a count ("8 parries") in a clip name or note without the creator's confirmation.
- There is no audio awareness: a clip may cut a line of dialogue or a music hit. Say so when the video has audio.

Pick clip candidates from an analysed video and hand the chosen one to the video-editor skill. This covers the step between "here is what happens in the video" and "render this range".

## Inputs

- **Video path** (required): the source video file.
- **Analysis folder** (required): the video-analyst output folder for that video, holding `report.md` and `analysis.json`. If it does not exist, run video-analyst first.
- **Output folder** (required from a caller; default `lazycut-out/clips/<video name>/` in the working directory).
- **Prompt** (optional): the creator's request in plain language ("longest counter chain", "the finisher", "best 30 seconds"). If none is given, use the saved prompts for the content type below.
- **Target platform and length** (optional): default 20 to 45 s for Shorts and Reels.
- **Requirements**: the video-analyst script at `../video-analyst/scripts/analyze.py` and its requirements (Python 3, `ffmpeg`).

Saved prompts:
- Boss fights: longest clean exchange, phase change, finisher, the one hit taken.
- Open-world or story games: the plan going wrong, the chase, the escape, the payoff.
- Anything else: best 30 seconds, opening, ending.

## Process

1. Work from the analyst's timeline, dead-time ranges, peak, and framing notes. Pick 3 to 5 candidate ranges that answer the prompt.
2. Snap every candidate with these rules:
   - One continuous range, minimum 3 s, inside the video bounds. Never stitch ranges.
   - Start 0.5 s before the first event in the range (a beat before the first clash).
   - End 0.5 s after the result lands, before any dissolve, menu, or loading screen.
3. Refine the edges: run `../video-analyst/scripts/analyze.py` on a 4 s window around each start and end at 5 to 10 fps and move the edge to the exact frame of the cue. Coarse timestamps are not good enough for a trim point.
4. For each candidate compute and report:
   - `payoff_t`: seconds from clip start to the payoff.
   - Dead time inside the range, from the analyst's dead-time list.
   - Crop warning if any beat in range is not safe for a centred 9:16 crop.
   - Counted events, marked as needing the creator's confirmation.
5. Give each candidate its own angle. Clips from one video that show the same thing read as repeats when posted together; say which to post and which to drop.
6. Write one analysis note per candidate, chosen by rule:
   - First event lands more than 1.0 s after the start: start later.
   - Payoff later than 7 s in: the first on-screen text must promise it.
   - More than 2 s of dead time inside: say where, and offer a shorter range.
   - Otherwise: say what makes it loop or land cleanly.

## Outputs

Write the candidates to `candidates.md` and `candidates.json` in the output folder and report both paths back. Then give the list in the reply.

A numbered list, strongest first. Per candidate: name, `M:SS.s-M:SS.s` in source time, length, why it works in one line, payoff time, dead time, crop warning, the analysis note.

Then ask which to cut. The creator can nudge by saying "2, start half a second earlier". Apply nudges in 0.5 s steps (0.1 s if asked), restate the new range, update the files, and pass the final range to video-editor.
