# MacKenzie Voice Tool

Source-backed MacKenzie Price voice drafting and review-loop tooling for Alpha School communications.

Status: **v0.2, expanded usable draft but not locked**.

Current training base: **~234 total minutes of video/audio transcript material** across 9 source-backed examples, with the corpus designed to be updated regularly as new MacKenzie-approved material and feedback becomes available.

This repository contains:

- a MacKenzie-only voice corpus
- a first-pass MacKenzie voice guide
- an installable AI skill
- review-session materials for calibrating with MacKenzie
- scripts for capturing feedback and turning it into training data

The goal is not to impersonate MacKenzie or send unsupervised messages. The goal is to generate high-quality drafts for human review, then improve the drafting system from MacKenzie’s actual edits.

## Quick setup for Claude

Clone the repo:

```bash
git clone git@github.com:PSkinnerTech/mackenzie-voice-tool.git
cd mackenzie-voice-tool
```

Then open Claude Code from the repo root and ask Claude to install it:

```text
Install this repository as a Claude skill. Set up the mackenzie-voice skill so I can invoke it later with "use the mackenzie-voice skill." Keep the supporting mackenzie-price-style corpus files available to the skill, and do not copy only SKILL.md if that would break the relative paths.
```

If Claude asks what install method to use, say:

```text
Prefer a symlink from this repo's skills/mackenzie-voice folder into ~/.claude/skills/mackenzie-voice. If symlinks are not supported in this environment, copy the skill folder and document that I still need to run Claude from the repo root for corpus access.
```

Test the install:

```text
Use the mackenzie-voice skill. Confirm you can see the voice guide, grading schema, and corpus manifest. Do not draft anything yet.
```

## Quick setup for Perplexity

Perplexity does not currently use Claude-style `SKILL.md` installs. The closest equivalent is a **Perplexity Space** with custom instructions plus uploaded project files. Perplexity Spaces are project hubs that can use Space-level instructions and uploaded files as sources.

Create a compact upload file first:

```bash
python3 mackenzie-price-style/tools/mackenzie_voice_context.py > mackenzie-voice-context-pack.md
```

Then create a new Perplexity Space:

1. Open Perplexity.
2. Go to **Spaces**.
3. Click **Create a Space**.
4. Name it `MacKenzie Voice Tool`.
5. Add the custom instructions below.
6. Upload `mackenzie-voice-context-pack.md`.
7. Also upload these files if your plan/file limits allow it:
   - `skills/mackenzie-voice/SKILL.md`
   - `mackenzie-price-style/voice-guide/mackenzie-voice-guide-v0.1.md`
   - `mackenzie-price-style/processed/mackenzie-tier-a-master-corpus-v0.2.md`
   - `mackenzie-price-style/training/grading-schema.md`
   - `mackenzie-price-style/training/feedback/2026-05-13-sales-director-feedback.md`
   - `mackenzie-price-style/training/examples/miami-founding-family/review-scorecard.md`

Paste this into the Space custom instructions:

```text
You are the MacKenzie Voice Tool. Your target voice is MacKenzie Price only. Never draft in Rachel Goodlad's voice or any other Alpha team member's voice. Rachel-related materials, if present, are evaluator context only.

Use the uploaded MacKenzie corpus, voice guide, grading schema, and feedback notes as your source context. Treat outputs as drafts for human review, not final sends.

Hard rules:
- No em dashes.
- No generic marketing or CRM language.
- Do not invent personal anecdotes.
- Do not paraphrase canonical Alpha commitments if exact wording is available. Use canonical language or ask for it.
- Prefer concrete parent and kid details over abstract launch language.
- MacKenzie's direct edits outrank all prior guidance.

When drafting, first identify the artifact type, audience, goal, required facts, CTA, and missing details. If required event facts are missing, use bracketed placeholders rather than inventing. Before returning, revise once against the voice guide and grading schema.

For review requests, score the draft on sounds_like_mackenzie, clarity, conviction, parent_resonance, alpha_accuracy, not_generic, too_salesy, and too_corporate. List forbidden phrases, keeper phrases, and a revised draft if useful.
```

Use this first Perplexity prompt to test the Space:

```text
Confirm you are using the MacKenzie Voice Tool instructions and uploaded files. Tell me which corpus, voice guide, and grading schema files you can see. Do not draft anything yet.
```

Then use this drafting prompt:

```text
Draft in MacKenzie Price's voice only. Artifact: [email / short blog / social / other]. Audience: [audience]. Goal: [goal]. Required facts: [facts]. CTA: [CTA]. Length: [length]. Use the MacKenzie Voice Tool files in this Space. Return the draft and a short self-check.
```

Research notes: Perplexity Spaces are the right target because they support project-specific custom instructions, uploaded files, and shared/collaborative threads. Third-party guides also note that Spaces are commonly used as Perplexity's closest equivalent to custom GPTs. See Perplexity Spaces references: <https://www.testingdocs.com/perplexity-templates-and-spaces/>, <https://airespo.com/resources/perplexity-spaces-explained-in-depth/>, and <https://mguhlin.org/2025/03/04/creating-custom-gpts-in-perplexity/>.


## Current corpus version

Status: **v0.2, expanded usable draft but not locked**.

The v0.2 Tier A corpus contains **41,395 words** from **9 sources**, representing approximately **234 total minutes** of video/audio transcript material:

- Modern Wisdom #981 video/podcast: 71 minutes
- Future of Education podcast selected episodes: 163 minutes

## Is this a “true skill”?

Yes, with one important distinction:

- For **OpenClaw / GBrain-style agents**, `skills/mackenzie-voice/SKILL.md` is already a proper skill file.
- For **Claude or other AI tools**, it can be installed as a skill/context pack, but the tool also needs access to the supporting corpus under `mackenzie-price-style/`.

Do **not** copy only `SKILL.md` and expect full performance. The skill instructions reference local project files for the corpus, voice guide, grading schema, examples, and feedback ledger.

## Key artifacts

- `skills/mackenzie-voice/SKILL.md`  
  The skill definition and workflow.

- `mackenzie-price-style/processed/mackenzie-tier-a-master-corpus-v0.2.md`  
  The v0.2 Tier A MacKenzie corpus.

- `mackenzie-price-style/voice-guide/mackenzie-voice-guide-v0.1.md`  
  The current voice guide.

- `mackenzie-price-style/training/grading-schema.md`  
  Review rubric for MacKenzie/user feedback.

- `mackenzie-price-style/training/review-sessions/2026-05-14-mackenzie-review-plan.md`  
  Tomorrow’s calibration plan.

- `mackenzie-price-style/training/examples/miami-founding-family/`  
  Seed drafts and scorecard for the first review.

- `mackenzie-price-style/tools/mackenzie_voice_context.py`  
  Prints a compact context pack for use in Claude, ChatGPT, or other tools.

- `mackenzie-price-style/tools/capture_mackenzie_feedback.py`  
  Appends structured review feedback to the feedback ledger.

## Safety / voice boundary

Target voice is **MacKenzie Price only**.

Rachel Goodlad materials are evaluator context only. They must never be used as the target voice.

Outputs are drafts for human review, not unsupervised or deceptive impersonation.

Hard constraints:

- No em dashes.
- Do not draft in Rachel’s voice.
- Do not invent personal anecdotes.
- Do not paraphrase canonical Alpha commitments if exact wording is available. Use canonical language or ask for it.
- Avoid generic AI/marketing phrases.
- Treat MacKenzie’s edits as higher-signal than the public corpus.

## Quick start

Clone the repo:

```bash
git clone git@github.com:PSkinnerTech/mackenzie-voice-tool.git
cd mackenzie-voice-tool
```

Print the context pack:

```bash
python3 mackenzie-price-style/tools/mackenzie_voice_context.py
```

Use that output as the setup/context for Claude, ChatGPT, or another AI tool if native skill loading is not available.

## Installing as a Claude skill

Claude skill support varies by Claude product and environment. The reliable pattern is:

1. Keep this repository cloned locally.
2. Install or link the skill folder into Claude’s skill directory.
3. Ensure Claude can read the repository files, especially `mackenzie-price-style/`.
4. Start drafting from the repository root so relative paths in the skill resolve correctly.

### Option A: Symlink the skill into Claude Code

From the repo root:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/mackenzie-voice" ~/.claude/skills/mackenzie-voice
```

Then open Claude Code from the repo root:

```bash
cd /path/to/mackenzie-voice-tool
claude
```

Prompt Claude with something like:

```text
Use the mackenzie-voice skill. Draft an email from MacKenzie Price to founding families at Alpha Miami announcing a first-day meetup. Use the local corpus and voice guide. Return the draft and a brief self-check.
```

### Option B: Copy the skill folder

If symlinks are not preferred:

```bash
mkdir -p ~/.claude/skills/mackenzie-voice
cp -R skills/mackenzie-voice/* ~/.claude/skills/mackenzie-voice/
```

Still keep this repo available and work from the repo root, because the skill expects the support files in `mackenzie-price-style/`.

### Option C: Claude Project instructions

If your Claude environment does not support skills, create a Claude Project and add this to the project instructions:

```text
You are using the MacKenzie Voice Tool. Target voice is MacKenzie Price only. Never draft in Rachel Goodlad's voice. Use the repository files as source context, especially:

- skills/mackenzie-voice/SKILL.md
- mackenzie-price-style/voice-guide/mackenzie-voice-guide-v0.1.md
- mackenzie-price-style/processed/mackenzie-tier-a-master-corpus-v0.2.md
- mackenzie-price-style/training/grading-schema.md
- mackenzie-price-style/training/feedback/

All outputs are drafts for human review. No em dashes. Avoid generic marketing/AI phrases. Do not invent anecdotes. MacKenzie's edits outrank all prior guidance.
```

Then upload or attach the context pack generated by:

```bash
python3 mackenzie-price-style/tools/mackenzie_voice_context.py > mackenzie-voice-context-pack.md
```

## Using with other AI tools

For ChatGPT, Gemini, Cursor, or any tool without native skill loading:

1. Generate the context pack:

   ```bash
   python3 mackenzie-price-style/tools/mackenzie_voice_context.py > mackenzie-voice-context-pack.md
   ```

2. Attach or paste:

   - `mackenzie-voice-context-pack.md`
   - the specific draft request
   - any required facts, date, time, location, CTA, and canonical Alpha language

3. Use this prompt:

   ```text
   Use the attached MacKenzie Voice Context Pack. Draft in MacKenzie Price's voice only. Do not draft in Rachel Goodlad's voice. This is a draft for human review. Before returning, revise once for: no em dashes, no generic marketing language, no invented anecdotes, concrete parent/kid details, and MacKenzie-specific parent/founder voice.
   ```

## Recommended workflow for tomorrow’s MacKenzie review

Use the review plan:

```bash
cat mackenzie-price-style/training/review-sessions/2026-05-14-mackenzie-review-plan.md
```

Review the seed drafts:

```bash
cat mackenzie-price-style/training/examples/miami-founding-family/v0.1-email.md
cat mackenzie-price-style/training/examples/miami-founding-family/v0.1-short-blog.md
cat mackenzie-price-style/training/examples/miami-founding-family/review-scorecard.md
```

Ask MacKenzie:

1. What sounds like me?
2. What does not sound like me?
3. What would you say instead?
4. Which phrases should we never use again?
5. Which phrases should we reuse?
6. Is anything factually wrong or off-brand for Alpha?
7. Score 1-5 for: sounds like me, clarity, parent resonance, not generic.

## Capturing MacKenzie feedback

Create a notes file and optional accepted revision file:

```bash
mkdir -p /tmp/mackenzie-review
nano /tmp/mackenzie-review/notes.txt
nano /tmp/mackenzie-review/accepted.md
```

Append structured feedback:

```bash
python3 mackenzie-price-style/tools/capture_mackenzie_feedback.py \
  --artifact-id miami-founding-family-email-v0.1 \
  --reviewer MacKenzie \
  --draft-path mackenzie-price-style/training/examples/miami-founding-family/v0.1-email.md \
  --notes-file /tmp/mackenzie-review/notes.txt \
  --accepted-revision-file /tmp/mackenzie-review/accepted.md \
  --sounds-like 4 \
  --clarity 5 \
  --conviction 4 \
  --parent-resonance 4 \
  --alpha-accuracy 5 \
  --not-generic 4 \
  --forbidden-phrase "example phrase to ban" \
  --keeper-phrase "example phrase to keep"
```

Feedback is written to:

```text
mackenzie-price-style/training/examples/feedback-ledger.jsonl
```

## Promoting feedback into the voice guide

Update the voice guide only when:

- MacKenzie explicitly confirms a rule, phrase, or rewrite, or
- the same pattern appears in at least two review examples.

Primary guide:

```text
mackenzie-price-style/voice-guide/mackenzie-voice-guide-v0.1.md
```

Promotion examples:

- Add forbidden phrases MacKenzie rejects.
- Add keeper phrases she says sound right.
- Add structure notes, such as preferred openings, closings, or parent-story moves.
- Add canonical Alpha language once verified.

## Drafting prompt template

Use:

```text
mackenzie-price-style/training/mackenzie-drafting-prompt-template.md
```

Minimum required facts for a good draft:

- audience
- sender, usually MacKenzie Price
- artifact type, email/blog/etc.
- goal
- date/time/location if event-related
- CTA or next step
- canonical Alpha language, if relevant
- length
- anything to avoid

## Validation checklist before showing MacKenzie

- [ ] Target voice is MacKenzie only.
- [ ] No em dashes.
- [ ] No Rachel voice.
- [ ] No invented personal anecdotes.
- [ ] No generic launch hype.
- [ ] No sales/CRM phrasing.
- [ ] Concrete parent/kid details are present.
- [ ] Canonical Alpha commitments are not paraphrased.
- [ ] Draft feels useful even if the family does not take the next step.
- [ ] Self-score is at least 4/5 on sounds_like_mackenzie, parent_resonance, and not_generic.

## Current limitations

- The v0.2 corpus is expanded and usable but not locked.
- Modern Wisdom should be verified against original audio/video.
- Future of Education transcripts are Whisper-based and need spot checks.
- The voice guide needs MacKenzie’s direct calibration before broader team rollout.

## Repository hygiene

Large MP3 source audio files are intentionally excluded from git. The repo stores transcripts, processed corpus, source metadata, and tooling.

If you regenerate audio locally, keep it under:

```text
mackenzie-price-style/raw/future-of-education-podcast/audio/
```

That path is ignored by `.gitignore`.
