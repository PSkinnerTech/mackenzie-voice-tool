#!/usr/bin/env python3
"""Append a MacKenzie voice review entry to training/examples/feedback-ledger.jsonl.

Usage:
  python tools/capture_mackenzie_feedback.py --artifact-id miami-email-v1 \
    --reviewer MacKenzie --draft-path path.md --notes-file notes.txt \
    --accepted-revision-file accepted.md --sounds-like 4 --clarity 5 ...
"""
from pathlib import Path
import argparse, json, datetime
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--artifact-id', required=True)
parser.add_argument('--reviewer', default='MacKenzie')
parser.add_argument('--draft-path', default='')
parser.add_argument('--notes-file', default='')
parser.add_argument('--accepted-revision-file', default='')
for k in ['sounds-like','clarity','conviction','parent-resonance','alpha-accuracy','not-generic']:
    parser.add_argument(f'--{k}', type=int)
parser.add_argument('--too-salesy', action='store_true')
parser.add_argument('--too-corporate', action='store_true')
parser.add_argument('--forbidden-phrase', action='append', default=[])
parser.add_argument('--keeper-phrase', action='append', default=[])
args = parser.parse_args()
def read_optional(p):
    return Path(p).read_text().strip() if p and Path(p).exists() else ''
entry = {
    'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'artifact_id': args.artifact_id,
    'reviewer': args.reviewer,
    'draft_path': args.draft_path,
    'scores': {
        'sounds_like_mackenzie': args.sounds_like,
        'clarity': args.clarity,
        'conviction': args.conviction,
        'parent_resonance': args.parent_resonance,
        'alpha_accuracy': args.alpha_accuracy,
        'not_generic': args.not_generic,
    },
    'too_salesy': args.too_salesy,
    'too_corporate': args.too_corporate,
    'forbidden_phrases': args.forbidden_phrase,
    'keeper_phrases': args.keeper_phrase,
    'reviewer_notes_verbatim': read_optional(args.notes_file),
    'accepted_revision': read_optional(args.accepted_revision_file),
}
out = ROOT/'training'/'examples'/'feedback-ledger.jsonl'
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('a') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
print(out)
