---
name: youtube-gaming-seo
description: "Generates complete, copy-paste-ready YouTube SEO metadata for a gaming video (titles, description, tags, thumbnail guidance, and a pre-publish checklist) from a game name and a rough video title, researching the game and subject for accuracy first. Use when YouTube titles, descriptions, tags, chapters, or thumbnails are wanted for a gaming video, when a gaming video is about to be posted or uploaded to YouTube, or when one or more game and title pairs are handed over, even if the word SEO is never used."
---

# YouTube Gaming SEO Metadata

**Rules that always hold:**

- Research the game and subject fresh every time. Never fill in names, phases, or questlines from memory. A wrong boss name in a title is an embarrassing, permanent mistake.
- Never put a difficulty claim (`No Hit`, `No Damage`, `Flawless`) in a recommended title unless the run truly is one. Do not silently assume the run is flawless.
- Tag the game's real genre. No false "soulslike" label on a game that is not one.
- Channel facts (name, handle, tagline, links, size) come only from the channel brief. Do not invent them.
- If a game is given with no subject, ask for the subject before proceeding. Do not invent one.

Turn a bare game name + rough video title into a full, publish-ready YouTube metadata package. The two things that make the output good are (1) **factual accuracy about the game** and (2) **consistent, search-first SEO conventions**. This skill splits those: it makes you research the facts fresh, and it hands you the SEO conventions so you don't have to re-derive them.

## Inputs

1. **Game name** (required): for example "Ghost of Yotei", "Elden Ring", "Sekiro".
2. **Rough video title / subject** (required): for example "Lord Saito fight", "Malenia no hit", "the Spider Lily General", "Genichiro Ashina". This tells you *what the video is about* (usually a boss, but it can be a level, a challenge run, a full-game segment, etc.).
3. **Channel brief path** (required): the file holding the channel name, handle, subscribe link, tagline and positioning, channel size, and title strategy. A blank template is at [references/channel-brief.example.md](references/channel-brief.example.md). If no brief is given, ask for the handle and tagline before writing; everything else in the workflow stays the same.
4. **Output path** (required from a caller; default `lazycut-out/seo/<Channel>_<Game>_YouTube_SEO.md` in the working directory, or the session's outputs folder when it has one).

You can receive **one** game and title pair or a **list** of pairs. If it's a list (for example four bosses from one game), process every item and produce a metadata block for each, but only do the shared research (game overview, channel context) once.

**Requirements**: web search and web fetch.

## Process

### Why "search-first" (the single most important strategic choice)

A small channel does **not** get meaningful reach from the browse/suggested feed yet. Its discovery comes almost entirely from **people searching** for the exact thing they want to watch: `"[game] [boss] boss fight"`. So the primary title must **front-load the exact phrase a viewer would type**, and only add the skill/curiosity hook *after* that. Cleverness that buries the search phrase costs views. As a channel grows and the suggested feed kicks in, curiosity-gap titles can move up front. Default to search-first unless the channel brief sets a different title strategy.

### Step 1 — Research the game and subject (do this fresh, every time)

Accuracy is the whole edge here. Big guide channels are sloppy with real character names and questline details; getting them *right* is how a channel's videos get found by superfans and don't look amateur. Never fill these in from memory — games and their wikis change, and a wrong boss name in a title is an embarrassing, permanent mistake.

For each subject, use web search (and web fetch on a good result) to confirm:

- **The exact canonical name** of the boss/subject, including the character's *real name* if they have a nickname (for example "The Dragon" = *Ukichi Saito*; "Malenia" = *Malenia, Blade of Miquella*). Both go in the tags/description — the nickname people search, and the real name superfans search.
- **Context that makes the description credible**: what questline/area the fight is in, the number of phases, the signature mechanic (a weapon, a gimmick, a phase transition). One or two accurate specifics make the description read like it was written by someone who actually beat the fight.
- **The correct genre of the game.** This governs the tags. Be honest: if the game is a samurai action-adventure, don't tag it "soulslike" just because the channel's niche is Souls. Mislabeling pulls in the wrong audience who click and bounce, which *hurts* ranking. Capture the skill-showcase crowd with accurate cross-tags instead (for example "no damage", "parry", "boss fight") rather than a false genre label.

If you're unsure whether the game is current/real or spelled correctly, search — don't guess.

Optionally, if the brief gives little context on the channel, you can web fetch the channel's videos page (the URL is in the brief) once to confirm positioning. Usually the brief is enough.

### Step 2 — Read the difficulty framing from the rough title (be honest about it)

The biggest click-through lever in this niche is a **truthful** difficulty claim: `No Hit`, `No Damage`, `Flawless`. But a false claim tanks retention (viewers leave the second they see a hit land), and retention is what actually ranks the video — so a lie here is self-defeating.

- If the rough title already contains "no hit" / "no damage" / "flawless" / "deathless", treat that as confirmed and use it in the recommended title.
- If it doesn't, produce a **neutral recommended title** plus a clearly-labeled no-hit/no-damage *variant*, and tell the user to use the variant **only if the run truly is one**. Don't silently assume the run is flawless.
- When in genuine doubt, ask the user one question: "Is this run actually no-hit / no-damage, or just a clean run?" It changes which variant is recommended.

### Step 3 — Build the metadata for each video

Use the SEO conventions in [references/seo-playbook.md](references/seo-playbook.md) (title-pattern library, description template, tag-construction recipe, thumbnail guidance). Read that file now if you haven't — it has the exact patterns and a worked example. Fill its channel placeholders from the channel brief.

For each video produce:
- **1 recommended title** + **3 alternate titles** (one search-max, one no-hit/no-damage variant, one on-brand variant built on the channel's tagline).
- **1 description** following the template: keyword-rich first two lines (this is what shows in search), the channel's tagline line, playlist + subscribe links, a CHAPTERS block with placeholder `0:00` timestamps (first chapter MUST be `0:00`), a plain boss/game credit line, and 3 hashtags.
- **1 tags line** (~18–20 comma-separated tags) built from the recipe: game name + variants, subject nickname + real name, "boss fight", honest difficulty terms, accurate genre/mechanic terms, related-game piggyback, and the channel name.

### Step 4 — Assemble one copy-paste file and add the extras

Put everything into a **single Markdown file** with each copyable field in its own fenced code block (so the user gets a clean copy button per field and exact plaintext — no smart quotes). Structure:

1. A short **strategy notes** section at the top (why these choices, tuned to the channel's size).
2. One section **per video** with TITLE / ALTERNATES / DESCRIPTION / TAGS blocks.
3. A **thumbnail guidance** section (from the playbook), with a suggested punchy word per video.
4. A **pre-publish checklist**.

### Step 5 — Close with the honest-framing check

After presenting, briefly (a few sentences, not a wall) surface the 2–3 judgment calls you made: the difficulty variant to pick honestly, why you led with search phrases, and any genre-tagging decision. If difficulty is still unconfirmed, ask the single clarifying question so they can lock the recommended variant.

### Batch handling

For a list of videos from the same game: do Step 1's game-level research once, then loop Steps 2–3 per subject (each subject still needs its own name/context lookup). Always recommend making one **playlist** ("<Game> — All Boss Fights") and linking it in every description — multiple videos feeding each other's watch time is worth more than any single tag, and it's the highest-leverage move for a small channel.

## Outputs

One Markdown file at the output path, with a descriptive filename like `<Channel>_<Game>_YouTube_SEO.md`. Report the path back, and present the file with the session's file-presenting tool when it has one.

What good output looks like:

- Titles a viewer would actually type into search, with the game and subject name intact and correctly spelled.
- Descriptions that read like they were written by someone who beat the fight, not scraped from a wiki.
- Tags that mix the searched nickname, the real name, honest difficulty terms, and the accurate genre — no false "soulslike" labels on non-souls games.
- Everything in clean, per-field code blocks the user can paste straight into YouTube Studio.
