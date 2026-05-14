#!/usr/bin/env python3
"""Print the compact context pack for MacKenzie voice drafting/review."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
files = [
    ROOT/'voice-guide'/'mackenzie-voice-guide-v0.1.md',
    ROOT/'training'/'grading-schema.md',
    ROOT/'training'/'feedback'/'2026-05-13-sales-director-feedback.md',
    ROOT/'training'/'feedback'/'rachel-doc'/'alignment-review-2026-05-13.md',
    ROOT/'processed'/'mackenzie-tier-a-master-corpus-v0.2.qa.md',
]
print('# MacKenzie Voice Context Pack\n')
for f in files:
    if f.exists():
        print(f'\n--- FILE: {f.relative_to(ROOT)} ---\n')
        print(f.read_text().strip())
manifest = ROOT/'processed'/'mackenzie-tier-a-master-corpus-v0.2.manifest.json'
if manifest.exists():
    print('\n--- CORPUS MANIFEST ---\n')
    print(json.dumps(json.loads(manifest.read_text()), indent=2))
