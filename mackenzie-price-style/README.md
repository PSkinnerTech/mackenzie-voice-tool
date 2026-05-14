# MacKenzie Price / Alpha Voice Project

Purpose: build a source-backed, reviewable drafting system for MacKenzie/Alpha-style copy.

Safety/product framing: this project should create drafts for review in a MacKenzie-inspired Alpha founder voice, not deceptive impersonation or unsupervised sending.

## Corpus tiers

- Tier A: direct MacKenzie voice (`direct-authored`, `spoken-transcript`, `approved-internal`)
- Tier B: MacKenzie-adjacent (`quoted`, `profile-about`, `event-description`)
- Tier C: Alpha brand/context (`brand-copy`, `unknown-author`, `third-party-about-alpha`)

## Folders

- `raw/` — untouched downloaded source material
- `sources/` — source tracker + inventories
- `processed/` — cleaned text and extracted MacKenzie utterances
- `transcripts/` — transcripts, speaker-labeled where possible
- `voice-guide/` — evolving style guide and rubrics
- `training/` — graded examples and preference calibration records
- `tools/` — local scripts for collection/classification
