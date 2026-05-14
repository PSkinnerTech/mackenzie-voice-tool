#!/usr/bin/env python3
from pathlib import Path
import re, json
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / 'processed'
OUTDIR.mkdir(exist_ok=True)
SOURCES = [
    {
        'id': 'modern-wisdom-981',
        'title': 'Modern Wisdom #981 — MacKenzie Price: Alpha School: A New Approach To Education',
        'tier': 'Tier A direct MacKenzie voice; transcript mirror cleaned and speaker-labeled',
        'status': 'usable draft corpus; verify against YouTube/audio before final lock',
        'path': ROOT / 'transcripts' / 'modern-wisdom-981' / 'modern-wisdom-981.mackenzie-only.md',
    },
    {
        'id': 'future-of-education-s2e307',
        'title': "Future of Education S2E307 — MacKenzie's Advice Column: Answering Your Questions (Part 1)",
        'tier': 'Tier A direct MacKenzie voice; audio-backed Whisper transcript',
        'status': 'usable draft corpus; needs audio spot-check before final lock',
        'path': ROOT / 'transcripts' / 'future-of-education-podcast' / 'cleaned' / 's2e307.mackenzie-only.md',
    },
    {
        'id': 'future-of-education-s2e308',
        'title': "Future of Education S2E308 — MacKenzie's Advice Column: Answering Your Questions (Part 2)",
        'tier': 'Tier A direct MacKenzie voice; audio-backed Whisper transcript',
        'status': 'usable draft corpus; needs audio spot-check before final lock',
        'path': ROOT / 'transcripts' / 'future-of-education-podcast' / 'cleaned' / 's2e308.mackenzie-only.md',
    },
]

def strip_header(text):
    lines=text.splitlines()
    if lines and lines[0].startswith('# '):
        i=1
        while i < len(lines) and (not lines[i].strip() or lines[i].startswith('- ')):
            i+=1
        return '\n'.join(lines[i:]).strip()
    return text.strip()

def wc(s):
    return len(re.findall(r"\b[\w’'-]+\b", s))

parts=[]; manifest=[]
for src in SOURCES:
    if not src['path'].exists():
        raise SystemExit(f"Missing {src['path']}")
    body=strip_header(src['path'].read_text())
    words=wc(body)
    manifest.append({k: (str(v.relative_to(ROOT)) if k=='path' else v) for k,v in src.items()} | {'words': words})
    parts.append(f"## SOURCE: {src['id']}\n\n"
                 f"- Title: {src['title']}\n"
                 f"- Attribution: {src['tier']}\n"
                 f"- Status: {src['status']}\n"
                 f"- Source file: {src['path'].relative_to(ROOT)}\n"
                 f"- Word count: {words}\n\n"
                 f"{body}\n")

total=sum(m['words'] for m in manifest)
header = "# MacKenzie Price Tier A Master Corpus v0.1\n\n"
header += "This corpus is for drafting/review support and voice analysis, not deceptive impersonation. Outputs built from it should be framed as drafts for human review.\n\n"
header += "Status: usable but not locked. Modern Wisdom should be verified against original audio/video; Future of Education Whisper transcripts need spot-checks for proper nouns and listener-question wording.\n\n"
header += f"Sources: {len(manifest)}\nTotal words: {total}\n\n"
header += "## Source manifest\n\n"
for m in manifest:
    header += f"- **{m['id']}** — {m['words']} words — `{m['path']}`\n"
header += "\n---\n\n"
master = header + "\n---\n\n".join(parts)
(OUTDIR/'mackenzie-tier-a-master-corpus-v0.1.md').write_text(master)
(OUTDIR/'mackenzie-tier-a-master-corpus-v0.1.txt').write_text('\n\n'.join(strip_header((ROOT/m['path']).read_text()) for m in manifest) + '\n')
(OUTDIR/'mackenzie-tier-a-master-corpus-v0.1.manifest.json').write_text(json.dumps({'version':'v0.1','total_words':total,'sources':manifest}, indent=2))
qa = ["# QA — MacKenzie Price Tier A Master Corpus v0.1\n\n", f"- Sources: {len(manifest)}\n", f"- Total words: {total}\n"]
for m in manifest:
    qa.append(f"- {m['id']}: {m['words']} words\n")
qa.append("\n## Caveats\n\n- Usable but not locked.\n- Modern Wisdom source came from transcript mirror and needs original audio/video verification.\n- Future of Education transcripts are local Whisper outputs and need spot-checking.\n")
(OUTDIR/'mackenzie-tier-a-master-corpus-v0.1.qa.md').write_text(''.join(qa))
print(json.dumps({'total_words':total,'sources':manifest}, indent=2))
