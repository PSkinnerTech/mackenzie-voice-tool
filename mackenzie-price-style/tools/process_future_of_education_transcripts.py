#!/usr/bin/env python3
"""Clean Whisper transcripts from Future of Education podcast solo/direct episodes.

Outputs per episode:
- .cleaned.md: source metadata + cleaned transcript
- .mackenzie-only.md: direct MacKenzie voice corpus text
- .qa.md: lightweight QA/stats and caveats

Assumption for selected episodes: MacKenzie-hosted solo advice/Q&A episodes. We remove the
standard podcast intro and keep listener questions as prompts when detectable.
"""
from pathlib import Path
import csv, json, re

ROOT = Path(__file__).resolve().parents[1]
WHISPER = ROOT / 'transcripts' / 'future-of-education-podcast' / 'whisper'
OUT = ROOT / 'transcripts' / 'future-of-education-podcast' / 'cleaned'
OUT.mkdir(parents=True, exist_ok=True)

feed_rows = {r.get('slug') or (m.group(0).lower() if (m:=re.search(r'S\d+E\d+', r['title'])) else ''): r
             for r in csv.DictReader((ROOT/'sources'/'future-of-education-feed.csv').open())}
selected = []
sel_path = ROOT/'sources'/'future-of-education-selected-audio.json'
if sel_path.exists():
    selected = json.loads(sel_path.read_text())
    for r in selected:
        feed_rows[r['slug']] = r

INTRO_START = 'Welcome to the Future of Education podcast'
INTRO_END_RE = re.compile(r"All right, (?:here(?:'s| is) the )?first (?:one|question)\.?", re.I)

def clean_text(text: str) -> str:
    text = text.replace('\r\n','\n').strip()
    # Collapse Whisper line-wrapping into paragraphs by sentence-ish boundaries.
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    raw = ' '.join(lines)
    raw = re.sub(r'\s+', ' ', raw).strip()
    # Remove canned intro between known markers, preserving the transition.
    if INTRO_START in raw:
        before, rest = raw.split(INTRO_START, 1)
        m = INTRO_END_RE.search(rest)
        if m:
            raw = (before.strip() + '\n\n' + m.group(0).strip() + ' ' + rest[m.end():].strip()).strip()
        else:
            # If the intro format changed, do not discard the episode. Keep the text and
            # remove only the known intro marker sentence.
            raw = (before.strip() + ' ' + rest.strip()).strip()
    # Put question transitions on paragraph boundaries.
    raw = re.sub(r'\s+(All right, (?:next|first) question\.)\s+', r'\n\n\1 ', raw, flags=re.I)
    raw = re.sub(r'\s+(Question number \w+\.)\s+', r'\n\n\1 ', raw, flags=re.I)
    # Split into readable paragraphs every ~5 sentences, respecting question boundaries.
    paras=[]
    for block in raw.split('\n\n'):
        sents = re.split(r'(?<=[.!?])\s+', block.strip())
        cur=[]
        for s in sents:
            cur.append(s)
            if len(cur)>=5:
                paras.append(' '.join(cur)); cur=[]
        if cur: paras.append(' '.join(cur))
    return '\n\n'.join(p for p in paras if p).strip()+"\n"

def word_count(s):
    return len(re.findall(r"\b[\w’'-]+\b", s))

summary=[]
for txt in sorted(WHISPER.glob('s*e*.txt')):
    slug = txt.stem.lower()
    meta = feed_rows.get(slug, {})
    cleaned = clean_text(txt.read_text())
    wc = word_count(cleaned)
    title = meta.get('title', slug)
    header = f"# {title}\n\n"
    header += f"- Source tier: Tier A direct MacKenzie voice, audio-backed Whisper transcript\n"
    header += f"- Podcast: Future of Education Podcast\n"
    if meta.get('pubDate'): header += f"- Published: {meta['pubDate']}\n"
    if meta.get('duration'): header += f"- Duration: {meta['duration']}\n"
    if meta.get('audio'): header += f"- Audio: {meta['audio']}\n"
    header += f"- Local raw transcript: transcripts/future-of-education-podcast/whisper/{txt.name}\n"
    header += f"- Status: usable draft transcript; needs human/audio spot-check before final lock\n\n"
    (OUT/f'{slug}.cleaned.md').write_text(header + cleaned)
    (OUT/f'{slug}.mackenzie-only.md').write_text(header + cleaned)
    qa = [f"# QA — {title}\n\n", f"- Cleaned words: {wc}\n", "- Speaker assumption: MacKenzie solo/host voice except removed standard podcast intro.\n", "- Verification needed: spot-check Whisper against audio, especially proper nouns and listener question wording.\n"]
    (OUT/f'{slug}.qa.md').write_text(''.join(qa))
    summary.append({'slug':slug,'title':title,'words':wc,'cleaned':str((OUT/f'{slug}.cleaned.md').relative_to(ROOT)),'mackenzie_only':str((OUT/f'{slug}.mackenzie-only.md').relative_to(ROOT))})

(ROOT/'sources'/'future-of-education-processed-summary.json').write_text(json.dumps(summary,indent=2))
md=['# Future of Education processed transcripts\n\n']
for r in summary:
    md.append(f"- **{r['slug']}** — {r['title']} — {r['words']} words\n  - `{r['cleaned']}`\n  - `{r['mackenzie_only']}`\n")
(ROOT/'sources'/'future-of-education-processed-summary.md').write_text(''.join(md))
print(json.dumps(summary,indent=2))
