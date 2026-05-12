---
name: hashtag-strategy
description: >
  Build a tiered hashtag strategy for a brand, account, or content topic on
  a specific social platform. Use when building a hashtag library for ongoing
  content or optimizing reach for a specific post or campaign. Invoke with
  /hashtag-strategy followed by the brand/topic and the target platform.
allowed-tools: WebFetch
---

When this skill is invoked, produce a structured hashtag strategy organized by tier. Generic hashtag lists don't work — effective hashtag strategy uses a mix of niche, mid-range, and broad tags to maximize both relevance and reach.

## Before Building

Gather or clarify:
1. **Brand/topic**: What is the account about? Industry, niche, content type?
2. **Platform**: Instagram, LinkedIn, TikTok, X? Each platform has different hashtag conventions.
3. **Audience**: Who are you trying to reach? Job titles, interests, community affiliations?
4. **Content pillars**: What topics does the account regularly cover?
5. **Goal**: Discovery by new audiences, community engagement, or topic authority?

## Hashtag Tier Logic

**Tier 1 — Niche (under 100K uses)**
High relevance, low competition. Your posts have a real chance of ranking in these hashtags. Attracts smaller but highly targeted audiences who are specifically interested in this topic. These are the most valuable for community-building.

**Tier 2 — Mid-range (100K–1M uses)**
Balanced reach and competition. Active communities without being overwhelmed by content volume. Strong for engagement and discovery.

**Tier 3 — Broad (1M+ uses)**
High reach, high competition. Posts get buried quickly. Use sparingly — 1–2 per post for association with the category, not for discovery. Do not overload on these.

## Platform-Specific Guidelines

**Instagram**:
- Optimal: 10–15 hashtags per post (first comment or end of caption)
- Mix: 4–5 Tier 1 + 4–5 Tier 2 + 2–3 Tier 3
- Create 3–4 sets for rotation — using the same set on every post signals spam to the algorithm

**LinkedIn**:
- Optimal: 3–5 hashtags (end of post or integrated naturally)
- Mix: 2 Tier 1/2 + 1–2 Tier 3
- Over-hashtagging on LinkedIn looks amateur and reduces reach

**TikTok**:
- Hashtags matter less than audio and content signals
- Use 3–5: 1–2 niche, 1–2 content-type, 1 broad
- Always include #fyp or trending sounds separately from hashtag strategy

**X (Twitter)**:
- 1–2 hashtags max. More looks like spam.
- Only use when the hashtag is an active conversation (trending topic, industry event)

## Output Format

```markdown
# Hashtag Strategy: [Brand/Topic]
**Platform**: [Platform]
**Niche**: [Industry/topic area]

---

## Core Hashtag Sets

### Set A — [Theme, e.g., Industry/Expertise]
**Tier 1 (Niche)**: #[tag] #[tag] #[tag] #[tag] #[tag]
**Tier 2 (Mid)**: #[tag] #[tag] #[tag] #[tag]
**Tier 3 (Broad)**: #[tag] #[tag]

### Set B — [Theme, e.g., Audience/Role]
**Tier 1 (Niche)**: #[tag] #[tag] #[tag] #[tag] #[tag]
**Tier 2 (Mid)**: #[tag] #[tag] #[tag] #[tag]
**Tier 3 (Broad)**: #[tag] #[tag]

### Set C — [Theme, e.g., Content Format/Type]
[Same structure]

### Set D — [Theme, e.g., Community/Event]
[Same structure]

---

## Usage Instructions

- **Rotate sets**: Use Set A on Monday, Set B on Wednesday, Set C on Friday, etc.
- **Mix and match**: Pull Tier 1 from Set A with Tier 2 from Set B for variety
- **Refresh quarterly**: Hashtag volumes change. Re-audit every 90 days.
- **Never repeat the exact same set twice in a row** on Instagram

---

## Tags to Avoid

| Tag | Reason |
|-----|--------|
| #[tag] | [Over-saturated / flagged as spam / irrelevant to niche] |

---

## Pillar-Specific Tags

| Content Pillar | Recommended Tags |
|---------------|-----------------|
| [Pillar 1] | #[tag] #[tag] #[tag] |
| [Pillar 2] | #[tag] #[tag] #[tag] |
```

## Quality Bar

A good hashtag strategy:
- Has tags that are genuinely relevant to the content (not just popular)
- Includes enough Tier 1 tags to enable real niche discovery
- Provides multiple rotation sets to avoid algorithm spam flags
- Includes instructions for how and when to use each set
- Flags tags known to be overused or algorithmically penalized
