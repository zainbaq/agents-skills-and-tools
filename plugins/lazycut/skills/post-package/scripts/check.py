#!/usr/bin/env python3
"""Deterministic pre-publish gate for one post package.
usage: check.py PACKAGE.json   (exit code 1 if anything blocks)

PACKAGE = {
  "platform": "youtube" | "shorts" | "reels" | "tiktok",
  "topic": "GTA 6", "subject": "Yosemite 1500",
  "handle": "@yourchannel",                             # optional: counts as a link back on short-form
  "title": "...", "alternates": ["..."], "description": "...", "tags": ["..."],
  "thumbnail_word": "...", "captions": [{"t0": 0, "t1": 3, "text": "..."}],
  "facts": {"no_damage": true, "final_boss": false},   # ONLY facts the creator confirmed
  "strategy": "search_first" | "hook_first",
  "true_tags": ["soulslike"]                            # genre tags confirmed true for this game
}
"""
import json, re, sys

CLAIMS = {  # phrase -> confirmed fact it needs
    "no hit": "no_damage", "no damage": "no_damage", "hitless": "no_damage", "flawless": "no_damage",
    "untouched": "no_damage", "final boss": "final_boss", "first boss": "first_boss",
    "first try": "first_try", "deathless": "no_deaths", "no death": "no_deaths", "no deaths": "no_deaths",
    "world record": "world_record", "world first": "world_first",
}
HASHTAGS = {"youtube": 3, "shorts": 5, "reels": 5, "tiktok": 5}
LIMITS = {"youtube": {"title": 100, "description": 5000}, "shorts": {"title": 100, "description": 5000},
          "reels": {"description": 2200}, "tiktok": {"description": 2200}}   # re-verify yearly
BANNED_UNLESS_TRUE = ["soulslike", "souls-like", "souls like"]

def check(p):
    out = []
    add = lambda rule, sev, field, msg: out.append({"rule": rule, "severity": sev, "field": field, "message": msg})
    plat, facts = p["platform"], p.get("facts", {})
    desc, title = p.get("description", ""), p.get("title", "")
    fields = {"title": title, "description": desc, "thumbnail_word": p.get("thumbnail_word", "")}
    fields.update({f"alternate {i + 1}": t for i, t in enumerate(p.get("alternates", []))})
    fields.update({f"caption {i + 1}": c["text"] for i, c in enumerate(p.get("captions", []))})

    for name, text in fields.items():
        for phrase, fact in CLAIMS.items():
            if re.search(rf"\b{re.escape(phrase)}\b", text, re.I) and facts.get(fact) is not True:
                add("claim_needs_fact", "block", name, f'"{phrase}" needs the creator to confirm {fact}')

    tags_found = re.findall(r"#\w+", desc)
    if len(tags_found) != HASHTAGS[plat]:
        add("hashtag_count", "block", "description", f"{len(tags_found)} hashtags, {plat} takes exactly {HASHTAGS[plat]}")
    if plat == "shorts" and not any(t.lower() == "#shorts" for t in tags_found):
        add("hashtag_count", "block", "description", "#Shorts is missing")

    for field, limit in LIMITS[plat].items():
        n = len(p.get(field, ""))
        if n > limit:
            add("length_limits", "block", field, f"{n} characters, limit {limit}")

    if plat == "youtube":
        topic, subject = p.get("topic", ""), p.get("subject", "")
        if p.get("strategy", "search_first") == "search_first":
            head = title[:len(topic) + len(subject) + 12].lower()
            if not (title.lower().startswith(topic.lower()[:6]) and subject.lower() in head):
                add("search_first_title", "warn", "title", "game and subject should lead the title")
        stamps = [int(m) * 60 + int(s) for m, s in re.findall(r"^(\d+):(\d\d)\b", desc, re.M)]
        if len(stamps) < 3 or stamps[0] != 0 or any(b - a < 10 for a, b in zip(stamps, stamps[1:])):
            add("chapters_valid", "block", "description", "chapters need 0:00 first, at least 3, each 10+ s apart")
        if re.search(r"^0:00.*\n0:00", desc, re.M):
            add("chapters_valid", "block", "description", "placeholder 0:00 timestamps are still in")
        tags = p.get("tags", [])
        if not 15 <= len(tags) <= 25:
            add("tags_count", "warn", "tags", f"{len(tags)} tags, aim for about 20")
        if len(", ".join(tags)) > 500:
            add("length_limits", "block", "tags", "tags exceed 500 characters in total")
        for t in tags:
            if t.lower() in BANNED_UNLESS_TRUE and t.lower() not in [x.lower() for x in p.get("true_tags", [])]:
                add("false_genre_tag", "block", "tags", f'"{t}" is not confirmed true for this game')
    else:
        handle = "|" + re.escape(p["handle"]) if p.get("handle") else ""   # channel handle from the brief
        if not re.search(r"youtube\.com|youtu\.be|on youtube" + handle, desc, re.I):
            add("link_back", "block", "description", "no link or pointer back to the full video or channel")
        caps = p.get("captions", [])
        if caps and caps[0]["t0"] > 0.3:
            add("hook_at_zero", "warn", "caption 1", "first on-screen text should start at 0.0 s")
        for i, c in enumerate(caps):
            if c["t1"] - c["t0"] < 2.5:
                add("caption_duration", "warn", f"caption {i + 1}", "on screen under 2.5 s")
            if len(c["text"].split()) > 9:
                add("caption_length", "warn", f"caption {i + 1}", "over 9 words")
        if re.search(r"[\U0001F300-\U0001FAFF]", title) is None and plat == "shorts":
            add("short_title_style", "warn", "title", "Short titles carry one emoji by convention")
    return out

if __name__ == "__main__":
    res = check(json.load(open(sys.argv[1])))
    for r in res:
        print(f'{r["severity"].upper():5} {r["rule"]:20} {r["field"]:14} {r["message"]}')
    blocks = sum(r["severity"] == "block" for r in res)
    print(f"{blocks} block(s), {len(res) - blocks} warning(s)" if res else "PASS: no blocks, no warnings")
    sys.exit(1 if blocks else 0)
