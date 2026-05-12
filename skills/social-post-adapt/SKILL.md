---
name: social-post-adapt
description: >
  Adapt a piece of content (blog post, article, announcement, or existing post)
  into native posts for a specific social media platform. Use when repurposing
  content across channels. Invoke with /social-post-adapt followed by the
  source content and the target platform(s).
allowed-tools: Read
---

When this skill is invoked, adapt the provided source content into platform-native social media posts. Do not summarize or cross-post — rewrite for the platform's audience behavior, algorithm, and cultural norms.

## Before Adapting

1. **Identify the source content type**: Blog post, long-form article, announcement, thread, video script, podcast episode, research finding?
2. **Identify the target platform(s)**: LinkedIn, Instagram, X, TikTok, Threads, Facebook
3. **Identify the brand voice**: Formal/casual, authoritative/peer, technical/accessible
4. **Identify the core message**: What is the single most important point to convey from the source?
5. **Identify the goal**: Awareness, engagement, or driving traffic back to the source?

## Platform Adaptation Rules

### LinkedIn
- Professional but human tone. First line is the hook — it must stand alone before "...more"
- Line breaks after every 1–2 sentences. No walls of text.
- 150–300 words for strong organic reach
- Strong personal perspective or counterintuitive opinion wins over neutral summaries
- 3–5 relevant hashtags at the end
- CTA: ask a question, invite to comment, or point to full article

### Instagram
- Caption supports the visual — assume a striking image or graphic leads
- First sentence hooks without requiring "more" click
- Conversational, personal, or storytelling tone
- Emojis appropriate to brand voice (use sparingly for professional brands)
- 10–15 hashtags mixing niche, mid-range, and broad
- CTA: save, share, comment, or "link in bio"

### X (Twitter)
- 280 characters or a thread. Pick one.
- Single tweet: sharp, specific, opinionated. Cut everything that isn't essential.
- Thread: Hook tweet → 5–8 punchy numbered points → closing tweet with CTA
- No hashtag stuffing — 1–2 max if used at all
- Engage by being specific and taking a stance

### TikTok
- Rewrite as a video script, not a caption
- Hook: First 2 seconds must compel the viewer to stop scrolling (state a problem, make a surprising claim, or ask a jarring question)
- Conversational, authentic tone — sounds like you're talking to a friend
- End with a specific call to action ("comment your answer", "follow for part 2")
- Structure: Hook → Context → Main point → Insight → CTA

### Threads
- Casual, low-friction observations. Short sentences. Like texting a thought.
- Questions work well. Personal takes work well.
- No hashtags needed. No heavy formatting.

## Output Format

```markdown
# Content Adaptation: [Source Title]

**Source summary**: [1 sentence on what the source content is about]
**Core message to convey**: [The single most important point]

---

## LinkedIn Version
[Full caption with line breaks, hashtags, and CTA]

---

## Instagram Version
**Caption**:
[Full caption]
**Hashtags**: [Hashtag set — separate from caption or in first comment]
**Visual direction**: [Brief description of image/graphic that should accompany this]

---

## X (Twitter) Version
**Option A — Single tweet**:
[Tweet under 280 characters]

**Option B — Thread**:
Tweet 1 (hook): [...]
Tweet 2: [...]
[etc.]

---

## TikTok Script
**Hook (0–2 sec)**: [...]
**Context (2–5 sec)**: [...]
**Main content (5–45 sec)**: [...]
**Insight/payoff**: [...]
**CTA**: [...]

---

## Threads Version
[Short, casual take]
```

## Quality Bar

Good adapted content:
- Sounds native to each platform — not like it was copied from somewhere else
- Preserves the core message without losing it in reformatting
- Uses platform-appropriate formatting (line breaks, hashtags, length)
- Has a specific, platform-appropriate CTA on each version
