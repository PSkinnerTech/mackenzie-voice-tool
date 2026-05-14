# MacKenzie Price / Alpha Voice Project

Purpose: build a source-backed, reviewable drafting system for MacKenzie/Alpha-style copy.

Safety/product framing: this project should create drafts for review in a MacKenzie-inspired Alpha founder voice, not deceptive impersonation or unsupervised sending.


## Current corpus version

Status: **v0.2, expanded usable draft but not locked**.

The v0.2 Tier A corpus contains **41,395 words** from **9 sources**, representing approximately **234 total minutes** of video/audio transcript material:

- Modern Wisdom #981 video/podcast: 71 minutes
- Future of Education podcast selected episodes: 163 minutes

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
