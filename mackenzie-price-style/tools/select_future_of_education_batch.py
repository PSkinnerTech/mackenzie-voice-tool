#!/usr/bin/env python3
"""Select and download the next curated Future of Education audio batch.

This batch prioritizes MacKenzie-forward solo/editorial/Q&A episodes where the RSS
metadata indicates MacKenzie is the primary speaker. We avoid obvious guest/interview
episodes unless deliberately added later with diarization.
"""
from pathlib import Path
import csv, hashlib, json, re, ssl, urllib.request

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT / 'sources' / 'future-of-education-feed.csv'
OUTDIR = ROOT / 'raw' / 'future-of-education-podcast' / 'audio'
OUTDIR.mkdir(parents=True, exist_ok=True)

# Curated first expansion set. S2E307/S2E308 are already processed.
TARGETS = [
    'S2E285',  # Audience Q+A
    'S2E286',  # Debunking the Nonprofit Fantasy
    'S2E290',  # 11 Things Your Kid's Brain Actually Needs
    'S2E291',  # Brain-Based Principles Part 2
    'S2E296',  # Parent survey results
    'S2E331',  # Non-partisan education / pledge
]

def slug_for(title: str) -> str:
    m = re.search(r'S\d+E\d+', title, re.I)
    if m:
        return m.group(0).lower()
    return hashlib.sha1(title.encode()).hexdigest()[:8]

rows = list(csv.DictReader(FEED.open()))
by_slug = {slug_for(r['title']).upper(): r for r in rows}
ctx = ssl._create_unverified_context()
manifest = []
for target in TARGETS:
    r = by_slug.get(target.upper())
    if not r:
        raise SystemExit(f'Missing target in feed: {target}')
    slug = slug_for(r['title'])
    path = OUTDIR / f'{slug}.mp3'
    if not path.exists():
        print('downloading', target, r['title'])
        req = urllib.request.Request(r['audio'], headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=180, context=ctx).read()
        path.write_bytes(data)
    manifest.append({**r, 'local_audio': str(path.relative_to(ROOT)), 'slug': slug})

# Preserve prior selected entries and merge by slug.
sel_path = ROOT / 'sources' / 'future-of-education-selected-audio.json'
prior = []
if sel_path.exists():
    prior = json.loads(sel_path.read_text())
merged = {m['slug']: m for m in prior}
for m in manifest:
    merged[m['slug']] = m
sel_path.write_text(json.dumps(list(merged.values()), indent=2))

batch_path = ROOT / 'sources' / 'future-of-education-selected-audio-batch-v0.2.json'
batch_path.write_text(json.dumps(manifest, indent=2))

for m in manifest:
    p = ROOT / m['local_audio']
    print(m['slug'], m['duration'], m['title'], m['local_audio'], p.stat().st_size)
