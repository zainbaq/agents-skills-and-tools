---
name: voiceover-script
description: "Writes a timed, natural-sounding voiceover script for a short gameplay clip, separate from the on-screen text. Use when a script, narration, commentary, or voiceover lines are wanted for a clip."
---

# Voiceover script

**Rules that always hold:**

- Show the script and wait for approval before any voice is generated. Voice generation can cost credits.
- Do not write lines for moments you have not seen in the frames. Work from a video-analyst timeline for the clip.
- Only state what the frames show or the user confirmed. No "first try", "no damage", or counts without confirmation.
- Never read a caption aloud. The voice and the on-screen text must not be the same words.
- Verify game facts (payouts, names, mechanics) with a web search before putting them in a line.
- There is no audio awareness: if the clip may contain dialogue or music the voice would talk over, say so.

Write what a person would say while watching their own clip back, timed to the action. The script feeds the voiceover-audio skill.

## Inputs

- **Clip path** (required): the rendered clip the voice will sit on. All times are seconds from the start of this clip.
- **Analysis folder** (required): a video-analyst output folder covering the clip. If it does not exist, run video-analyst on the clip first.
- **Caption list** (required when the clip has on-screen text): the `plan.json` from video-editor, or the captions with their times.
- **Output folder** (required from a caller; default `lazycut-out/voiceover/<clip name>/` in the working directory).
- **Channel brief path** (optional): the source for the channel's tagline and tone.
- **Creator-confirmed facts** (optional).
- **Requirements**: web search, for checking game facts.

## Process

### Voice and text do different jobs

The on-screen text is a signpost: short, readable with the sound off. The voiceover is a person talking: reaction, context, a bit of personality. They must not be the same words.

- Never read a caption aloud. If the caption says "No tracker. $1,850 from Moses.", the voice says something like "No tracker on it, which means Moses will actually buy this thing."
- The voice can carry what text cannot: why something matters, what the player was thinking, the joke.
- When a voiceover exists, cut the on-screen text down. Keep the hook, any number or name the viewer needs to see, and the closing tagline. Return the trimmed caption list with the script.

### How to make it sound like a person

- First person, present tense, contractions. "I'm", "that's", "gonna" where it fits the channel.
- React before explaining. "Oh, he's leaving with it" lands better than a description of a tow truck.
- One thought per line. Vary line length; follow a long line with a short one.
- Allow one aside or dry joke per clip. Do not force more.
- No announcer phrases: "in this video", "let's dive in", "watch what happens next", "wait for it".
- No filler praise of the game, and no asking for likes inside the clip.
- Use the channel's tagline only as the last line, and only when it fits the clip.

### Timing rules

- Budget 2.4 words per second. A 4 second slot holds about 9 words. Stay under the budget; speech that fills every gap is tiring.
- The first line starts within 0.3 s and is the hook.
- Each line starts 0.2 to 0.5 s after the beat it talks about begins, never before the viewer can see it.
- Leave at least 0.5 s of air between lines, and let the peak moment play with no voice, or with three words at most.
- A tip must finish before its payoff appears on screen.
- Total speech should cover roughly 40 to 60 percent of the clip.

### Writing for a synthetic voice

- Spell numbers the way they should be said: "eighteen hundred and fifty dollars", not "$1,850".
- Avoid abbreviations, symbols, and all caps. Write "GTA six" if the voice reads "6" oddly.
- Flag names the voice may mispronounce and offer a phonetic respelling.
- Use commas for short pauses and full stops for longer ones. Do not use ellipses or stage directions.

## Outputs

Write these to the output folder and report each path back, then show the script in the reply:

1. `script.md`: a table with line number, start time, slot length in seconds, the line, word count. It also holds one alternate for the hook line and one for the closing line.
2. `lines.json`: the same lines as JSON for voiceover-audio:
```json
[{"id": 1, "t0": 0.2, "slot": 3.7, "text": "..."}]
```
   `t0` is seconds from the start of the output clip. `slot` is the time until 0.5 s before the next line starts.
3. `captions-trimmed.json`: the trimmed on-screen text list with times.

Show the script and wait for approval before any voice is generated.
