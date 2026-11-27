---
name: video-research
description: "Researches what already exists for a game, boss, or topic: competing videos, overlap with the channel's own uploads, what to make next, and thumbnail direction. Use when asked what competing videos exist, what to make next, whether an idea overlaps an earlier upload, or which thumbnail frames and words to use."
---

# Video research

**Rules that always hold:**

- Be honest about data limits. Search results often omit view counts and subscriber numbers. Never estimate them. If the numbers matter, ask the creator for a screenshot of the YouTube search results page and read it.
- Cite sources. Skip thin AI-written guide sites for facts.
- Any thumbnail claim word (NO DAMAGE, 1 HIT TAKEN) needs the creator's confirmation.
- Use only the creator's own footage for thumbnails. Push back if a source image looks like another creator's thumbnail.

Four jobs that all depend on knowing what already exists: competitor research, overlap with the channel's own uploads, what to make next, and thumbnail direction.

## Inputs

- **Job** (required): one or more of competitor research, overlap check, what to make next, thumbnail direction.
- **Game and subject** (required): the game, and the boss, topic, or idea in question.
- **Channel brief path** (required for the overlap check, optional otherwise): read it first when given. Its content history is the library of past uploads.
- **Video path and analysis folder** (required for thumbnail direction): the video and its video-analyst output folder. If there is no analysis, run `../video-analyst/scripts/analyze.py` on the video.
- **Analytics** (optional): figures or screenshots the creator shares.
- **Output folder** (required from a caller; default `lazycut-out/research/<subject>/` in the working directory).
- **Requirements**: web search. For thumbnail frames, `ffmpeg` and the video-analyst script's requirements.

## Process

### 1. Competitor research

Goal: find the angle nobody has claimed, and judge demand against competition.

1. Build the search phrase a viewer would type. Boss fights: `[game] [boss] boss fight`. Other content: `[game] [subject]` plus the task word (location, guide, how to).
2. Web-search that phrase and 2 or 3 variants (no damage, how to beat, location). Collect the top videos: title, channel, and age, plus views and channel size where the results show them.
3. Be honest about data limits, as in the rules above.
4. Report:
   - Shared title patterns across the top results.
   - Common thumbnail words.
   - The unclaimed angle (a run quality, a method, a mechanic, a format nobody used).
   - Demand versus competition in one line: many searches and weak videos, or crowded with large channels.
   - Launch-window status: how new the game is and whether coverage is still thin.
5. Cite sources. Skip thin AI-written guide sites for facts.

### 2. Overlap with past uploads

1. Match the proposed subject against the brief's content history, allowing for spelling variants and nicknames versus real names.
2. If it is already covered, list the existing videos and their angles, then either give the new one a distinct angle (encounter, location, method, run quality) or suggest a compilation.
3. Pick the end-screen target: the specific next video in the playlist order, never the channel page.
4. When a new upload is finished, tell the creator the line to add to the brief's content history, including run quality.

### 3. What to make next

Rank ideas in this order: games in their launch window, subjects with high search demand and weak competing videos, series that can become a playlist. For each idea give the search phrase, the competition read, and the playlist it would join. If the creator shares analytics, diagnose those first and tie the ranking to the numbers.

### 4. Thumbnail direction

1. Frame choice: propose 3 timestamps that read at phone size: a big face or figure, two rivals squared off, or a transformation or impact moment. Use the analyst script's `--zoom` on each to check sharpness and that no menu or subtitle covers the subject. Export full-resolution frames with ffmpeg and send them.
2. Result word: 2 to 4 words that say why to click and do not repeat the title. Any claim word (NO DAMAGE, 1 HIT TAKEN) needs the creator's confirmation.
3. Styling: white text with a heavy black outline by default; gold only for confirmed no-damage runs; no red text in fire-heavy scenes; text in the emptiest dark area, never over a face or weapon. Keep one template across a series.
4. Give 2 to 3 A/B options when the upload matters, and a ready-to-paste image prompt that erases all HUD and text, enhances for phone-size readability, and adds the result word with exact styling.
5. Use only the creator's own footage. Push back if a source image looks like another creator's thumbnail.
6. After generation, remind the creator to check faces, hands, leftover HUD, and text placement.

Follow the session's own instructions for which image tool and models to use.

## Outputs

Written to the output folder, with each path reported back:

- `research.md`: the findings for each job that was run, with sources.
- `frames/`: the exported full-resolution thumbnail frames, when thumbnail direction was run.

Give the findings in the reply as well, and send the frames.
