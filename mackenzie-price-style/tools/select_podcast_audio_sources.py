#!/usr/bin/env python3
from pathlib import Path
import csv, re, urllib.request, ssl, hashlib, json
root=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'sources'/'future-of-education-feed.csv').open()))
# Prioritize MacKenzie-forward solo/Q&A/editorial episodes, short first for fast transcription.
patterns=[
    r"MacKenzie's Advice Column",
    r"Audience Q\+A",
    r"Debating My Haters",
    r"Does Alpha Go Too Far",
    r"Why We Don't Say the Pledge",
    r"The Secret to Solving Behavioral Issues",
    r"The Wealthy Student Myth",
    r"Why We Treat Every Student",
    r"The 5 Strategies",
    r"Debunking the Nonprofit Fantasy",
]
selected=[]
for pat in patterns:
    for r in rows:
        if re.search(pat, r['title'], re.I) and r not in selected:
            selected.append(r)
# Start with two Advice Column episodes.
selected=selected[:2]
outdir=root/'raw'/'future-of-education-podcast'/'audio'; outdir.mkdir(parents=True, exist_ok=True)
manifest=[]
ctx=ssl._create_unverified_context()
for r in selected:
    eid=re.search(r'S\d+E(\d+)', r['title'])
    slug=(eid.group(0).lower() if eid else hashlib.sha1(r['title'].encode()).hexdigest()[:8])
    path=outdir/f'{slug}.mp3'
    if not path.exists():
        print('downloading', r['title'])
        data=urllib.request.urlopen(urllib.request.Request(r['audio'],headers={'User-Agent':'Mozilla/5.0'}),timeout=120,context=ctx).read()
        path.write_bytes(data)
    manifest.append({**r,'local_audio':str(path.relative_to(root)),'slug':slug})
(root/'sources'/'future-of-education-selected-audio.json').write_text(json.dumps(manifest,indent=2))
for m in manifest:
    print(m['slug'], m['duration'], m['title'], m['local_audio'], Path(root/m['local_audio']).stat().st_size)
