---
name: video-editor
description: "Renders one uncut range of a video as a ready-to-post clip, cropped or fitted to vertical with burned-in on-screen text, and returns the video file and its edit plan. Use when a clip needs to be cut, cropped to vertical, or given on-screen text for Shorts, Reels, or TikTok."
---

# Video editor

**Rules that always hold:**

- **One continuous range.** Never join two ranges or cut inside the clip. Uncut footage is the proof of skill. If the best moments are far apart, propose separate clips.
- **No false claims.** No Hit, No Damage, First Try, Final Boss and similar go on screen only when the creator has confirmed them. A true small count ("Only 2 hits taken") is a hook.
- Do not choose trim points or write text from a guess about what is on screen. Work from a video-analyst report; run video-analyst first if there is none.
- **Start** a beat before the first action. **End** on the result, before any dissolve or menu.
- Flag source problems before rendering: another platform's watermark, a phone recording of a screen, letterboxing. Platforms suppress watermarked reposts, so ask for the original file. Rendering a labelled test from a flawed source is fine.
- This skill does not add music, voiceover, transitions, or effects.

Produce a ready-to-post clip from a video file: one uncut range, the right vertical layout, and burned-in on-screen text. Deliver the rendered file and the edit plan behind it.

## Inputs

- **Video path** (required): the source video file.
- **Analysis folder** (required): the video-analyst output folder for that video. If it does not exist, run video-analyst first.
- **Range** (required): start and end in source time, from clip-finder or stated by the creator.
- **Output folder** (required from a caller; default `lazycut-out/render/<clip name>/` in the working directory).
- **Creator-confirmed facts** (optional): the only source for claims that go on screen.
- **Captions** (optional): on-screen text supplied by the caller. Otherwise write them by the rules below.
- **Requirements**: Python 3 with the `Pillow` package (`pip install pillow`), and `ffmpeg` with `ffprobe` on the path. A bold font: Anton if present; the script falls back to a system bold font.

## Process

### On-screen text rules

- The first caption starts at 0.0 s and is the hook, in plain language a non-player understands.
- If the payoff lands after about second 7, the first caption must promise it.
- Each caption: 7 words or fewer where possible, on screen at least 2.5 s, wraps to 2 lines at most.
- A tip caption must pay off on screen while it is showing.
- Leave gaps. Text during every second reads as noise; let the peak moment play clean or with a 2 to 3 word caption.
- White with a heavy black outline is the default. Gold is reserved for confirmed no-damage results and the closing tagline.
- Emoji are stripped from burned-in text (the caption font has none). Keep emoji for titles and captions written in the post package.
- Verify every fact in a caption (payouts, names, mechanics) against the frames or a web search.

### Layout choice

- `fit`: whole frame over a blurred fill, text in the band above the footage. Use when HUD panels or action at the frame edges carry the story. Add `fg_aspect` (for example 1.333 or 1.0) to trim the sides and make the footage bigger when the edges are not needed.
- `crop`: fills the 9:16 frame. Use when the action stays near one horizontal position; set `focus_x` to it. Check the analyst's framing notes first.
- `none`: keep the original shape, for long-form or already-vertical sources.
- `screen` pre-crops the source, for borders or the room around a recorded screen.

Text always stays out of the top 12% and bottom 15% of a vertical frame, where platform UI sits.

### Steps

1. Write the plan as `plan.json` in the output folder. The schema is printed in the docstring at the top of `scripts/render.py`; the fields are `source`, `out`, `start`, `end`, `layout`, `screen`, `focus_x`, `fg_aspect`, and `captions` (each with `t0`, `t1`, `text`, `pos`, `color`). Caption times are seconds from the start of the output clip, not the source.
2. Fonts: use Anton if present. If not, try `curl -sSL -o ~/fonts/Anton-Regular.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf`. The script falls back to a system bold font.
3. Run `python3 scripts/render.py plan.json` (path relative to this skill's folder). Run the script; do not read it into context. A 50 s clip takes about a minute.
4. Check the result before sending: grab one frame from the middle of each caption, tile them, and read the image. Confirm wrapping, placement, timing against the action, and that nothing covers key gameplay. Replace the frame numbers with the middle frame of each caption (seconds x 30):

```bash
ffmpeg -v error -y -i out.mp4 -vf "select='eq(n,45)+eq(n,570)+eq(n,960)',scale=450:-1,tile=3x1" -vsync 0 -frames:v 1 -update 1 check.jpg
```

## Outputs

Written to the output folder, with each path reported back:

- The rendered clip (the `out` path in the plan).
- `plan.json`: the edit plan behind it.
- `check.jpg`: the tiled caption check.

Send the video file with the session's file-sending tool when it has one. In the reply, list the captions with their times so the creator can ask for changes by number, and say what to check (text timing, leftover HUD or watermark, crop).

## Notes

- Output is H.264, 30 fps, AAC audio, 1080x1920 for vertical layouts. A 50 s clip lands around 45 MB.
- If the layout is `none` and the source is large, expect a longer render.
