# MacKenzie Content Collection Plan

## Goal
Build a source-backed corpus that separates MacKenzie Price's direct voice from Alpha brand voice and third-party descriptions. The drafting tool should learn from direct voice and approved edits, while using brand/context sources only for factual grounding.

## Source hierarchy

### Tier A — direct MacKenzie voice
Use for voice modeling.

- Direct-authored essays/articles/posts.
- Podcast/video/interview transcripts where MacKenzie is speaking.
- Event talks/webinars/live streams with MacKenzie as speaker.
- Internal samples explicitly approved by MacKenzie.
- Human-edited before/after drafts from calibration sessions.

### Tier B — MacKenzie-adjacent
Use for claims, quotes, and context; do not overfit style.

- Profiles about MacKenzie with direct quotes.
- Press articles where she is interviewed/quoted.
- Event pages where she is listed as speaker.
- Bio/founder pages.

### Tier C — Alpha brand/context
Use for factual grounding and Alpha positioning only.

- Alpha website/blog/news copy with unknown authorship.
- 2 Hour Learning pages not explicitly authored by MacKenzie.
- Third-party coverage about Alpha where MacKenzie is not directly quoted.

## Active collection tracks

### Track 1 — Public web discovery
Status: started.

Artifacts:
- `raw/alpha_llms_full.txt` — downloaded Alpha full site corpus.
- `sources/alpha-discovered-sources.csv` — 238 Alpha-discovered candidates.
- `sources/web-search-discovered.csv` — 37 web-search candidates from DuckDuckGo fallback.
- `sources/curated-source-tracker.csv` — current high-signal seed tracker.

### Track 2 — Transcript extraction
Status: started.

Priority targets:
1. Modern Wisdom #981: MacKenzie Price — Alpha School: A New Approach To Education.
   - YouTube: https://www.youtube.com/watch?v=enXA7xepu2U
   - Singju transcript fetched and speaker-labeled.
   - Podscripts transcript fetched but needs speaker-label cleanup.
2. Johnathan Bi interview transcript.
   - Preview found; likely paywalled.
   - Needs approved access/export.
3. NYT Hard Fork: A.I. School Is in Session.
   - Discovered through Alpha corpus.
   - Needs transcript/access.
4. Alpha Future of School live stream.
   - Alpha page lists MacKenzie as co-founder speaker.
   - Need video/transcript source.

### Track 3 — Direct-authored writing
Status: not enough evidence yet.

Targets:
- Forbes Technology Council articles under MacKenzie Price, if any.
- LinkedIn posts/articles by MacKenzie.
- 2 Hour Learning / Future of Education posts explicitly authored by her.
- Internal approved emails/articles from MacKenzie.

### Track 4 — Internal calibration set
Status: pending human/MacKenzie input.

Ask MacKenzie for:
- 5–10 emails that sound exactly like her.
- 5–10 articles/posts she is proud of.
- 5–10 examples that are close but wrong, with notes.
- 3–5 before/after edits where her revision changed tone materially.

## Attribution rules

- Never mark a source Tier A unless MacKenzie is the author or speaker.
- If the source is a transcript mirror, preserve the original URL and mark confidence lower until verified against audio/video.
- If a source contains direct quotes but is written by a journalist, mark Tier B, not Tier A.
- Alpha website/blog copy defaults to Tier C unless explicit author attribution exists.

## Next operational steps

1. Clean and speaker-label the Modern Wisdom transcript.
2. Search for direct-authored MacKenzie articles/posts.
3. Locate Future of Education podcast feed and episode archive.
4. Find transcript/access route for NYT Hard Fork and Johnathan Bi interview.
5. Prepare a lightweight intake form for MacKenzie-approved internal samples.
