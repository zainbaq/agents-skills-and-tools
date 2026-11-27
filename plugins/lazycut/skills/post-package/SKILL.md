---
name: post-package
description: "Writes the per-platform post package for a short-form clip (title, description, hashtags, pinned comment, cover) and runs a scripted pre-publish gate on any YouTube, Shorts, Reels, or TikTok package. Use when a post package is wanted for a Short, Reel, or TikTok, or when any package needs checking against the channel rules before posting."
---

# Post package

**Rules that always hold:**

- Every package goes through the gate script before it is delivered. A **block** means the field is not delivered as written.
- Use only facts the creator has confirmed or the channel brief records. If run quality is unstated, ask before writing a title.
- Put only creator-confirmed facts in the package's `facts` field.
- Research the subject fresh with web search. Never guess spellings.
- A clip is one continuous range.

Write the per-platform package for a short-form clip and run the pre-publish gate on every package, long-form included. Long-form YouTube metadata itself comes from the youtube-gaming-seo skill; this skill adds the extras and the gate.

## Inputs

- **Clip path or package path** (required): the clip to write a package for, or an existing package to check.
- **Analysis folder** (required when writing a package): the video-analyst output folder for the clip, so the package matches what is on screen.
- **Platforms** (required): any of `youtube`, `shorts`, `reels`, `tiktok`.
- **Channel brief path** (required when writing a package): the source of truth for handle, links, playlists, templates, and run-quality history. A blank template is at [references/channel-brief.example.md](references/channel-brief.example.md). If no brief is given, ask for one; do not invent channel facts.
- **Creator-confirmed facts** (optional): no damage, hit count, first try, final boss, and similar.
- **Output folder** (required from a caller; default `lazycut-out/packages/<clip name>/` in the working directory).
- **Requirements**: Python 3 (standard library only) for the gate. Web search.

## Process

### Before writing

1. Facts: list every claim the package might make (no damage, hit count, first try, final boss). Use only what the creator has confirmed or the brief records. If run quality is unstated, ask before writing a title.
2. Research the subject fresh with web search: canonical spelling, real names, questline or mission, mechanics. Correct misspellings and say so.
3. Know what is on screen. Use the video-analyst report; the tip in a description must pay off during the clip.

### Packages

Every copyable field goes in its own code block. Tag each recommendation with the goal it serves: click-through, retention, session watch time, engagement, or funnel.

**Shorts**
- Title: short, first-person, one emoji, game hashtag.
- Description, in this order: hook line; one tip in 2 sentences that pays off in the clip; link to the full video or playlist (channel subscribe link only when no long-form exists); 5 hashtags including #Shorts.
- For boss fights the hook line is the hit-count hook ("1 hit. That's all Benkei got."). For other content it is the "what went wrong" or "what I pulled off" hook.

**Reels**
- On-screen text in plain language, no niche jargon.
- Caption: what happens, the niche term explained in one line, a question, a pointer to the full video on YouTube, 5 hashtags.
- End text pointing to YouTube.

**TikTok**
- Start from the Reel package and shorten it. Same fields, 5 hashtags.

**Every short-form package also gets**
- A pinned comment: a question that splits opinion or invites stories.
- A cover frame timestamp and a 2 to 4 word cover word that does not repeat the title.

**Long-form extras** (added to the youtube-gaming-seo output)
- Retention hook: first 1 to 2 description sentences, plus what moment to open the video on.
- Pinned-comment question.
- End-screen target: a specific next video, never the channel page.
- The Short to cut: exact moment, title, description.
- A community post idea for the day before or after.
- Thumbnail word, frame choice, and 2 to 3 A/B options when the upload matters.
- Chapters with real timestamps from the analyst report, not 0:00 placeholders.

### The gate

Write each package as JSON in the output folder and run `python3 scripts/check.py package.json` (path relative to this skill's folder). Run the script; do not read it into context. Put only creator-confirmed facts in `facts`.

Package fields: `platform` (`youtube`, `shorts`, `reels`, or `tiktok`), `topic`, `subject`, `handle` (the channel handle from the brief, with the @), `title`, `alternates`, `description`, `tags`, `thumbnail_word`, `captions` (each with `t0`, `t1`, `text`), `facts` (for example `{"no_damage": true, "final_boss": false}`), `strategy` (`search_first` or `hook_first`), and `true_tags` (genre tags confirmed true for this game).

- A **block** means the field is not delivered as written. Fix the text or get the fact confirmed, then re-run. The script exits with code 1 if anything blocks.
- A **warn** is delivered with the warning stated in one line.

Rules the script cannot check; apply them by hand:
- Spelling of the subject matches the research.
- The same boss or subject is not already covered without a distinct angle (check the brief's content history). If it is, give this one a different angle or suggest a compilation.
- No epithets or names sourced only from thin AI-written guide sites.
- A clip is one continuous range.
- A true small count ("Only 2 Hits Taken") is a hook and is allowed.

## Outputs

Written to the output folder, with each path reported back:

- `package-<platform>.json`: one per platform, the file the gate was run on.
- `package.md`: every package with each copyable field in its own code block.
- `gate-report.md`: the gate output for each package.

In the reply, report the gate result to the creator as a short list: what passed, what was fixed, what still needs their confirmation.

## Notes

- The link-back rule accepts a YouTube link, the words "on YouTube", or the channel handle given in the package's `handle` field. Always set `handle` from the channel brief.
- Platform character limits change. Re-check them with a web search about once a year.
- When the channel moves from search-first to hook-first titles, set `"strategy": "hook_first"` and update the brief.
