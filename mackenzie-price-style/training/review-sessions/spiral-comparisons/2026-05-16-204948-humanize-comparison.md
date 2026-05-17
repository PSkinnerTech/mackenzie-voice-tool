# Spiral CLI Comparison

All content in this report is draft-only and requires human review before use.

## Run Metadata

- Timestamp: 2026-05-16-204948

- Mode: humanize

- Runner: bunx @every-env/spiral-cli

- Elapsed seconds: 2.556

- Exit code: 0

- Timed out: False

- Raw stdout: mackenzie-price-style/training/review-sessions/spiral-comparisons/2026-05-16-204948-humanize-spiral.stdout.txt

- Raw stderr: mackenzie-price-style/training/review-sessions/spiral-comparisons/2026-05-16-204948-humanize-spiral.stderr.txt

- Metadata: mackenzie-price-style/training/review-sessions/spiral-comparisons/2026-05-16-204948-humanize-metadata.json

## Spiral Command

~~~bash
bunx @every-env/spiral-cli humanize '# Draft v0.1: Alpha Miami founding family first-day meetup email

**Subject:** Alpha Miami founding families, first day meetup details

Hi Alpha Miami Founding Families,

We are almost there.

I remember the feeling of sending my own kids into a new school year. There is excitement, of course, but there are also all the parent questions running in the background. Will they make friends? Will they feel known? Will they be challenged in the right way? Will they come home happy?

That is why I’m especially excited to bring our founding Alpha Miami families together before the first day of school.

**Founding Family First Day Meetup**
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION]

This will be a chance for your kids to meet each other, for families to connect, and for you to spend time with the Alpha Miami team before the school year begins.

Being a founding family is special. You are helping create the culture of this campus from the very beginning. The friendships, the standards, the joy, the courage to do school differently, all of that starts with this first group of families.

I’m so grateful you’re part of it, and I can’t wait for your kids to experience what school can feel like when they are known, challenged, and excited to walk through the doors.

See you soon,

MacKenzie' --json
~~~

## Prompt

~~~text
Draft an email from MacKenzie Price to founding families at Alpha Miami announcing a first-day meetup.
~~~

## Baseline MacKenzie Voice Tool Draft

~~~markdown
# Draft v0.1: Alpha Miami founding family first-day meetup email

**Subject:** Alpha Miami founding families, first day meetup details

Hi Alpha Miami Founding Families,

We are almost there.

I remember the feeling of sending my own kids into a new school year. There is excitement, of course, but there are also all the parent questions running in the background. Will they make friends? Will they feel known? Will they be challenged in the right way? Will they come home happy?

That is why I’m especially excited to bring our founding Alpha Miami families together before the first day of school.

**Founding Family First Day Meetup**
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION]

This will be a chance for your kids to meet each other, for families to connect, and for you to spend time with the Alpha Miami team before the school year begins.

Being a founding family is special. You are helping create the culture of this campus from the very beginning. The friendships, the standards, the joy, the courage to do school differently, all of that starts with this first group of families.

I’m so grateful you’re part of it, and I can’t wait for your kids to experience what school can feel like when they are known, challenged, and excited to walk through the doors.

See you soon,

MacKenzie
~~~

## Spiral Output

~~~markdown
# Draft v0.1: Alpha Miami founding family first-day meetup email

**Subject:** Alpha Miami founding families, first day meetup details

Hi Alpha Miami Founding Families,

We are almost there.

I remember the feeling of sending my own kids into a new school year. There is excitement, of course, but there are also all the parent questions running in the background. Will they make friends? Will they feel known? Will they be challenged in the right way? Will they come home happy?

I’m especially excited to bring our founding Alpha Miami families together before the first day of school.

**Founding Family First Day Meetup**
**Date:** [DATE]
**Time:** [TIME]
**Location:** [LOCATION]

This will be a chance for your kids to meet each other, for families to connect, and for you to spend time with the Alpha Miami team before the school year begins.

Being a founding family is special. You are helping create the culture of this campus from the very beginning. The friendships, the standards, the joy, the courage to do school differently – all of that starts with this first group of families.

I’m so grateful you’re part of it, and I can’t wait for your kids to experience what school can feel like when they are known, challenged, and excited to walk through the doors.

See you soon,

MacKenzie
~~~

## Hard Constraint Check

- em dash: 0
- en dash: 1
- phrase 'that matters': 0
- phrase 'the energy this moment deserves': 0
- phrase 'journey': 0
- phrase 'unlock potential': 0

## Spiral Stderr Summary

~~~text
Resolving dependencies
Resolved, downloaded and extracted [2]
Saved lockfile
~~~

## Scoring Checklist

# Grading Schema

Each generated draft should be reviewed with:

- `sounds_like_mackenzie` (1-5)
- `clarity` (1-5)
- `conviction` (1-5)
- `parent_resonance` (1-5)
- `alpha_accuracy` (1-5)
- `not_generic` (1-5)
- `too_salesy` (boolean)
- `too_corporate` (boolean)
- `forbidden_phrases` (list)
- `keeper_phrases` (list)
- `reviewer_notes` (verbatim)
- `accepted_revision` (final human-edited version)

MacKenzie's edits and rejects are higher-signal than public sources.

## Reviewer Notes

- sounds_like_mackenzie:

- clarity:

- conviction:

- parent_resonance:

- alpha_accuracy:

- not_generic:

- too_salesy:

- too_corporate:

- forbidden_phrases:

- keeper_phrases:

- accepted_revision:
