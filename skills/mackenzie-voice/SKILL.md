---
name: mackenzie-voice
version: 0.1.0
description: |
  Draft and critique MacKenzie Price voice artifacts from a source-backed Tier A corpus, then capture MacKenzie/user feedback as training data. Use for emails, short blogs, announcements, and review-loop calibration where the target voice is MacKenzie Price only.
triggers:
  - "MacKenzie voice"
  - "draft as MacKenzie"
  - "MacKenzie Price draft"
  - "review MacKenzie output"
  - "train MacKenzie voice"
tools:
  - read
  - write
  - edit
  - exec
mutating: true
---

# MacKenzie Voice

## Contract

This skill guarantees:

- Target voice is **MacKenzie Price only**. Never draft in Rachel Goodlad's voice or any other Alpha team member's voice.
- Drafts are grounded in the local Tier A MacKenzie corpus and project calibration files.
- Outputs are framed as drafts for human review, not deceptive or unsupervised impersonation.
- Feedback from MacKenzie/Patch/reviewers is captured as structured training data and treated as higher signal than public corpus examples.
- Hard constraints are enforced before delivery: no em dashes, no generic AI/marketing phrases, canonical Alpha language preserved when known.

## Phases

1. **Load context.** Read `mackenzie-price-style/processed/mackenzie-tier-a-master-corpus-v0.1.manifest.json`, the relevant corpus snippets, `mackenzie-price-style/training/grading-schema.md`, and calibration notes under `mackenzie-price-style/training/feedback/`.
2. **Clarify the artifact.** Identify audience, sender, format, goal, required facts, CTA, length, and any canonical Alpha phrases. Ask only if a missing fact would make the draft materially wrong.
3. **Draft in MacKenzie voice.** Use parent/founder voice: concrete, direct, warm, opinionated, practical. Prefer real parent stakes and kid-centered examples over launch hype or generic brand language.
4. **Run self-critique.** Grade against the schema: sounds_like_mackenzie, clarity, conviction, parent_resonance, alpha_accuracy, not_generic, too_salesy, too_corporate, forbidden_phrases, keeper_phrases.
5. **Revise once before showing.** Remove em dashes, hype, CRM phrases, generic warmth, and non-earned abstractions. Preserve canonical Alpha commitments/language instead of paraphrasing.
6. **Capture feedback.** When Patch, MacKenzie, or another reviewer reacts, append a structured entry to `mackenzie-price-style/training/examples/feedback-ledger.jsonl` and, when useful, save the accepted revision as a Markdown example.
7. **Promote learnings.** If a feedback pattern repeats or MacKenzie explicitly says something is right/wrong, update `mackenzie-price-style/voice-guide/mackenzie-voice-guide-v0.1.md`.

## Output Format

For draft requests, return:

1. The requested artifact(s), ready for review.
2. Optional short notes only if needed, clearly marked `Calibration notes`.

For review/training requests, return:

- `Scores` using the grading schema.
- `Keep` phrases that worked.
- `Change` phrases that missed.
- `Revision` if requested.
- `Training capture` path if feedback was written to disk.

## Voice Rules

- MacKenzie voice is parent/founder, not sales/marketing.
- She is direct, concrete, and willing to say school is broken when that is the point.
- She uses parent empathy from lived experience, especially boredom, wanting kids to love school, and wanting kids to be challenged at the right level.
- She explains with examples, not corporate abstraction.
- She can be warm and excited, but not gushy.
- She is practical about what families should expect.
- Avoid over-mythologizing founding families.
- Avoid phrases that read AI-ish: "that matters," "the energy this moment deserves," "journey," "unlock potential" unless grounded in a concrete example.
- No em dashes. Ever.
- Do not paraphrase the three Alpha commitments if the exact canonical wording is available. Use canonical language or ask for it.

## Anti-Patterns

- Drafting in Rachel Goodlad's voice. Rachel materials are evaluator context only.
- Producing generic Alpha brand copy instead of MacKenzie voice.
- Using unsourced claims, fake anecdotes, or fake personal experiences.
- Treating public/Whisper transcripts as final-locked without caveats.
- Overfitting one reviewer note into a universal rule before MacKenzie confirms it.
- Hiding uncertainty about missing facts, dates, location, links, or canonical language.

## Tools Used

- `read`: load corpus, grading schema, calibration notes, and prior examples.
- `write` / `edit`: save feedback, accepted revisions, voice-guide updates, and review-session artifacts.
- `exec`: run local helper scripts, validation checks, and corpus tooling.
