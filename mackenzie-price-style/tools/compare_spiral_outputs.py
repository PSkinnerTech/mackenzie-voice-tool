#!/usr/bin/env python3
"""Generate local MacKenzie Voice Tool vs. Spiral comparison reports."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT / "mackenzie-price-style" / "training" / "review-sessions" / "spiral-comparisons"
)
GRADING_SCHEMA_PATH = REPO_ROOT / "mackenzie-price-style" / "training" / "grading-schema.md"
DEFAULT_RUNNER = "bunx @every-env/spiral-cli"
FORBIDDEN_PHRASES = [
    "that matters",
    "the energy this moment deserves",
    "journey",
    "unlock potential",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare a saved MacKenzie Voice Tool baseline draft with Spiral CLI output."
    )
    parser.add_argument("--mode", choices=["write", "personalize", "humanize"], required=True)
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("--prompt", help="Original drafting prompt.")
    prompt_group.add_argument("--prompt-file", type=Path, help="File containing the original prompt.")
    parser.add_argument(
        "--baseline-file",
        type=Path,
        help="Saved MacKenzie Voice Tool baseline draft. Required for personalize/humanize.",
    )
    parser.add_argument(
        "--context-pack",
        type=Path,
        help="Optional context file passed to Spiral write with --file.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--runner", default=DEFAULT_RUNNER)
    parser.add_argument("--timeout-seconds", type=int, default=90)
    parser.add_argument("--title", help="Optional human-readable report title.")
    return parser.parse_args()


def read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Could not read {label} at {path}: {exc}") from exc


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return read_text(args.prompt_file, "prompt file").strip()
    return (args.prompt or "").strip()


def require_inputs(args: argparse.Namespace, prompt: str) -> None:
    if args.mode == "write" and not prompt:
        raise SystemExit("--prompt or --prompt-file is required for write mode.")
    if args.mode in {"personalize", "humanize"} and not args.baseline_file:
        raise SystemExit("--baseline-file is required for personalize and humanize modes.")
    if args.context_pack and args.mode != "write":
        raise SystemExit("--context-pack is only supported for write mode in this v1 wrapper.")


def build_spiral_command(args: argparse.Namespace, prompt: str, baseline: str | None) -> list[str]:
    command = shlex.split(args.runner)
    if args.mode == "write":
        command.extend(["write", prompt, "--instant", "--json"])
        if args.context_pack:
            command.extend(["--file", str(args.context_pack)])
        return command

    assert baseline is not None
    command.extend([args.mode, baseline, "--json"])
    return command


def parse_json_output(stdout: str) -> Any | None:
    text = stdout.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def summarize_parsed_output(parsed: Any) -> str | None:
    if parsed is None:
        return None
    if isinstance(parsed, dict):
        for key in ("output", "text", "content", "result", "message"):
            value = parsed.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        error = parsed.get("error")
        if isinstance(error, str) and error.strip():
            return f"Error: {error.strip()}"
        if isinstance(error, dict):
            message = error.get("message") or error.get("error")
            if isinstance(message, str) and message.strip():
                return f"Error: {message.strip()}"
    if isinstance(parsed, str):
        return parsed.strip()
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def hard_constraint_summary(text: str) -> list[str]:
    checks = [
        ("em dash", text.count("\u2014")),
        ("en dash", text.count("\u2013")),
    ]
    lines = [f"- {label}: {count}" for label, count in checks]
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        lines.append(f"- phrase '{phrase}': {lower_text.count(phrase)}")
    return lines


def run_spiral(command: list[str], timeout_seconds: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        elapsed = time.monotonic() - started
        return {
            "timed_out": False,
            "elapsed_seconds": round(elapsed, 3),
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except FileNotFoundError as exc:
        elapsed = time.monotonic() - started
        return {
            "timed_out": False,
            "elapsed_seconds": round(elapsed, 3),
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "timed_out": True,
            "elapsed_seconds": timeout_seconds,
            "exit_code": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or f"Timed out after {timeout_seconds} seconds.",
        }


def fenced(text: str, language: str = "") -> str:
    return f"~~~{language}\n{text.rstrip()}\n~~~"


def write_report(
    args: argparse.Namespace,
    prompt: str,
    baseline: str | None,
    command: list[str],
    result: dict[str, Any],
) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    stem = f"{timestamp}-{args.mode}"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    stdout_path = args.output_dir / f"{stem}-spiral.stdout.txt"
    stderr_path = args.output_dir / f"{stem}-spiral.stderr.txt"
    metadata_path = args.output_dir / f"{stem}-metadata.json"
    report_path = args.output_dir / f"{stem}-comparison.md"

    stdout = result["stdout"]
    stderr = result["stderr"]
    parsed = parse_json_output(stdout)
    spiral_summary = summarize_parsed_output(parsed)

    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")

    metadata = {
        "timestamp": timestamp,
        "mode": args.mode,
        "runner": args.runner,
        "command": command,
        "prompt_file": str(args.prompt_file) if args.prompt_file else None,
        "baseline_file": str(args.baseline_file) if args.baseline_file else None,
        "context_pack": str(args.context_pack) if args.context_pack else None,
        "output_files": {
            "report": str(report_path),
            "stdout": str(stdout_path),
            "stderr": str(stderr_path),
            "metadata": str(metadata_path),
        },
        "result": {
            "timed_out": result["timed_out"],
            "elapsed_seconds": result["elapsed_seconds"],
            "exit_code": result["exit_code"],
            "stdout_json_valid": parsed is not None,
            "hard_constraints": hard_constraint_summary(spiral_summary or stdout),
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    if GRADING_SCHEMA_PATH.exists():
        grading_schema = read_text(GRADING_SCHEMA_PATH, "grading schema").rstrip()
    else:
        grading_schema = "\n".join(
            [
                "- sounds_like_mackenzie",
                "- clarity",
                "- conviction",
                "- parent_resonance",
                "- alpha_accuracy",
                "- not_generic",
                "- too_salesy",
                "- too_corporate",
                "- forbidden_phrases",
                "- keeper_phrases",
            ]
        )

    stderr_summary = stderr.strip() or "(empty)"
    title = args.title or "Spiral CLI Comparison"

    sections = [
        f"# {title}",
        "All content in this report is draft-only and requires human review before use.",
        "## Run Metadata",
        f"- Timestamp: {timestamp}",
        f"- Mode: {args.mode}",
        f"- Runner: {args.runner}",
        f"- Elapsed seconds: {result['elapsed_seconds']}",
        f"- Exit code: {result['exit_code']}",
        f"- Timed out: {result['timed_out']}",
        f"- Raw stdout: {stdout_path.relative_to(REPO_ROOT)}",
        f"- Raw stderr: {stderr_path.relative_to(REPO_ROOT)}",
        f"- Metadata: {metadata_path.relative_to(REPO_ROOT)}",
        "## Spiral Command",
        fenced(shlex.join(command), "bash"),
        "## Prompt",
        fenced(prompt or "(not provided)", "text"),
        "## Baseline MacKenzie Voice Tool Draft",
        fenced(baseline or "(not provided for write mode)", "markdown"),
        "## Spiral Output",
        fenced(spiral_summary or stdout.strip() or "(empty stdout)", "markdown"),
        "## Hard Constraint Check",
        "\n".join(hard_constraint_summary(spiral_summary or stdout)),
        "## Spiral Stderr Summary",
        fenced(stderr_summary, "text"),
        "## Scoring Checklist",
        grading_schema,
        "## Reviewer Notes",
        "- sounds_like_mackenzie:",
        "- clarity:",
        "- conviction:",
        "- parent_resonance:",
        "- alpha_accuracy:",
        "- not_generic:",
        "- too_salesy:",
        "- too_corporate:",
        "- forbidden_phrases:",
        "- keeper_phrases:",
        "- accepted_revision:",
    ]
    report_path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    args = parse_args()
    prompt = load_prompt(args)
    require_inputs(args, prompt)

    baseline = None
    if args.baseline_file:
        baseline = read_text(args.baseline_file, "baseline file").strip()

    command = build_spiral_command(args, prompt, baseline)
    result = run_spiral(command, args.timeout_seconds)
    report_path = write_report(args, prompt, baseline, command, result)

    print(f"Wrote comparison report: {report_path}")
    print(f"Spiral exit code: {result['exit_code']}")
    if result["timed_out"]:
        print(f"Timed out after {args.timeout_seconds} seconds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
