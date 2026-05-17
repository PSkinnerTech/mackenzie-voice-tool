# Spiral CLI Comparison Review - 2026-05-16

## Bottom Line

The side-by-side comparison idea is sound, but it is still a plan, not a working tool. The correct v1 is a local CLI report generator that compares a known MacKenzie Voice Tool baseline draft against one Spiral output, saves raw command output, and leaves scoring to the human reviewer.

Do not start with a UI and do not try to automate the baseline drafting lane yet. The baseline lane depends on the MacKenzie Voice Tool skill/context workflow, not a deterministic local generation command.

## What Was Verified

- `bunx --bun @every-env/spiral-cli --help` works.
- Plain `bunx @every-env/spiral-cli --version` works and reports `1.5.0`.
- Plain `bunx @every-env/spiral-cli auth status` works and reports `Not authenticated`.
- `bunx --bun @every-env/spiral-cli auth status` failed locally before auth status, in a transitive dependency path.
- `humanize`, `personalize`, and `write --instant` are reachable with `--json`, but currently return JSON `AuthenticationError` until Spiral auth is configured.

## Design Review

### Keep

- Spiral should be a comparison lane, not a replacement for the MacKenzie Voice Tool.
- Output should be saved as local review artifacts only.
- Reports should align to the existing grading schema.
- Raw Spiral stdout/stderr should be preserved for debugging and later parser changes.
- Auth must remain local user setup. No token files in the repo.

### Change

- Replace the hard-coded `bunx --bun` runner with a configurable runner that defaults to plain `bunx @every-env/spiral-cli`.
- Treat auth failures and command failures as reportable outcomes, not script crashes.
- Make `--baseline-file` required for `personalize` and `humanize`.
- For `write`, require `--prompt` and optionally allow `--context-pack` via Spiral's `--file` flag.
- Generate a timestamped report plus a raw JSON/stdout file pair per Spiral run.

### Avoid

- Do not shell out from a browser UI.
- Do not send Spiral the entire corpus by default.
- Do not store or ask for API tokens in prompts, markdown, browser state, or committed config.
- Do not automatically promote Spiral-improved drafts into the voice guide.
- Do not treat Spiral output as MacKenzie-approved. It is only another draft candidate.

## Recommended V1 Contract

Script path:

```text
mackenzie-price-style/tools/compare_spiral_outputs.py
```

Minimum command:

```bash
python3 mackenzie-price-style/tools/compare_spiral_outputs.py \
  --mode humanize \
  --prompt-file prompts/founding-family-email.md \
  --baseline-file mackenzie-price-style/training/examples/miami-founding-family/v0.1-email.md
```

Useful flags:

- `--mode write|personalize|humanize`
- `--prompt` or `--prompt-file`
- `--baseline-file`
- `--context-pack`
- `--output-dir`
- `--runner`
- `--timeout-seconds`

Default output directory:

```text
mackenzie-price-style/training/review-sessions/spiral-comparisons/
```

Each run should produce:

- `YYYY-MM-DD-HHMMSS-<mode>-comparison.md`
- `YYYY-MM-DD-HHMMSS-<mode>-spiral.stdout.txt`
- `YYYY-MM-DD-HHMMSS-<mode>-spiral.stderr.txt`
- `YYYY-MM-DD-HHMMSS-<mode>-metadata.json`

## Report Template

The markdown report should include:

- timestamp
- runner and exact Spiral command
- mode
- elapsed time
- exit code
- prompt
- baseline draft
- Spiral output, parsed when JSON is valid
- stderr summary
- raw output paths
- scoring checklist from `training/grading-schema.md`
- explicit note that all content is draft-only and requires human review

## Open Product Questions

1. Which mode actually improves the MacKenzie workflow: `write`, `personalize`, or `humanize`?
2. Should Spiral get the compact context pack for `write`, or only the prompt?
3. Are comparison reports training artifacts worth committing, or temporary review artifacts?
4. When a Spiral draft wins, should the final human-approved version be captured in `feedback-ledger.jsonl` as a new accepted revision?

## Recommendation

Implement the CLI wrapper next. Start with `humanize` and `personalize` against an existing baseline draft, because those compare Spiral's editing value without confounding the test with a different first-draft generator.
