#!/usr/bin/env python3
"""Checks an eval package for the defects EVALS.md says L0 does not catch.

  check_package.py <skill-dir>                 static checks
  check_package.py <skill-dir> --run-empty     also run every exit_code cmd and build.cmd in an empty
                                               directory (Phase 0 check 2, host part). This executes the
                                               package's own commands, so only use it on a package you trust.
  check_package.py <skill-dir> --attest        also require what an attestation needs: fixtures filled in
                                               and eval_validated complete

Output lines start with ERROR (the package is wrong), REVIEW (a human must judge) or NOTE.
Exit status is 1 if any ERROR was printed, else 0. REVIEW lines never fail the run: leakage and
prompt wording are judgements, not regexes.

This script does not replace L0; run l0_check.py skill <skill-dir> as well.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

errors = 0
VALIDATED_FIELDS = ["date", "board", "framework_version", "reference_passed", "empty_failed",
                    "broken_caught", "spoof_caught", "exploit_caught", "leakage_reviewed", "evidence"]
# Build-system and include lines every project of a framework shares; not answers.
BOILERPLATE = re.compile(r"^(#include|include\(|idf_component_register|cmake_minimum_required|project\(|CONFIG_|zephyr_|target_sources|find_package)")
FAMILY_WORDS = re.compile(r"^(esp32|esp32-s3|esp32-c3|nrf52|stm32|rp2040|arduino|raspberry ?pi)$", re.I)


def err(msg: str) -> None:
    global errors
    errors += 1
    print(f"ERROR  {msg}")


def review(msg: str) -> None:
    print(f"REVIEW {msg}")


def note(msg: str) -> None:
    print(f"NOTE   {msg}")


def load(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        err(f"{path}: invalid YAML: {e}")
        return {}


def regex_literals(pattern: str) -> list[str]:
    """Literal runs of 3+ characters a regex requires, e.g. '^temp=(\\d+) C$' -> ['temp=']."""
    s = re.sub(r"\\[dDwWsSbB]", " ", pattern)          # classes
    s = re.sub(r"\[[^\]]*\]", " ", s)                   # bracket sets
    s = re.sub(r"\{\d+(,\d*)?\}", " ", s)               # quantifiers
    s = re.sub(r"\(\?[:=!<]*", " ", s)                  # group openers
    s = re.sub(r"\\(.)", r"\1", s)                       # escaped literals
    parts = re.split(r"[\^$()|*+?.]", s)
    out = []
    for part in parts:
        part = part.strip()
        if len(part) >= 3:
            out.append(part)
    return out


def check_prompt_values(tid: str, prompt: str, a: dict) -> None:
    t = a.get("type")
    low = prompt.lower()
    if t == "serial_match":
        pat = str(a.get("pattern", ""))
        lits = regex_literals(pat)
        if not lits:
            review(f"{tid}: serial_match pattern {pat!r} has no literal text; confirm the prompt fixes the output format")
        for lit in lits:
            if lit not in prompt:
                err(f"{tid}: serial_match needs {lit!r} but the prompt never says it (rule 4: the prompt states every matched value)")
        if a.get("max_matches") is not None and a["max_matches"] < a.get("min_matches", 1):
            err(f"{tid}: serial_match max_matches is below min_matches")
        if re.search(r"\b\d+(\.\d+)?\s*hz\b", low) and not re.search(r"every\s+\d+\s*ms|period|each\s+\d+\s*ms", low):
            review(f"{tid}: the prompt gives a rate in Hz; say whether it means toggles or full cycles (e.g. 'toggle every 250 ms')")
        if a.get("baud") and str(a["baud"]) not in prompt:
            err(f"{tid}: serial_match baud {a['baud']} is not in the prompt")
    elif t == "gpio_state":
        pin = a.get("pin")
        if pin is None:
            err(f"{tid}: gpio_state without pin")
        elif not re.search(rf"(gpio|io|pin|p\d\.)\s*0*{pin}\b", low):
            err(f"{tid}: gpio_state pin {pin} is not named in the prompt (write it as GPIO{pin} or pin {pin})")
        for k in ("expect", "min_edges", "within_s"):
            if a.get(k) is None:
                err(f"{tid}: gpio_state missing {k}")
        if a.get("max_edges") is not None and a.get("min_edges") is not None and a["max_edges"] < a["min_edges"]:
            err(f"{tid}: gpio_state max_edges is below min_edges")
    elif t == "bus_capture":
        exp = a.get("expect") or {}
        for k in ("adv_name", "service_uuid", "char_uuid"):
            v = exp.get(k)
            if v and str(v).lower() not in low:
                err(f"{tid}: bus_capture {k} {v!r} is not in the prompt")
        if not a.get("bus"):
            err(f"{tid}: bus_capture without bus")
    elif t == "exit_code":
        if not a.get("cmd"):
            err(f"{tid}: exit_code without cmd")
        review(f"{tid}: exit_code `{a.get('cmd')}` - confirm the prompt states the rule this command enforces")


def run_empty(tid: str, label: str, cmd: str, expect_ok: int) -> None:
    with tempfile.TemporaryDirectory(prefix="hwsc-empty-") as d:
        try:
            r = subprocess.run(cmd, shell=True, cwd=d, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            review(f"{tid}: {label} timed out after 900 s in an empty directory; cannot tell whether it is vacuous")
            return
    if r.returncode in (126, 127):
        err(f"{tid}: {label} `{cmd}` could not run (exit {r.returncode}, command not found or not executable). "
            "Load the toolchain (e.g. check `idf.py --version`) and rerun; a missing tool is not a failing assertion")
        return
    if r.returncode == expect_ok:
        err(f"{tid}: {label} `{cmd}` PASSES in an empty directory (exit {r.returncode}): the assertion is vacuous. "
            "Make absence a failure, e.g. `ls *.ino >/dev/null 2>&1 && ! grep -q X *.ino`")
    else:
        note(f"{tid}: {label} fails in an empty directory as it should (exit {r.returncode})")


def fixture_is_placeholder(d: Path) -> bool:
    files = [f for f in d.rglob("*") if f.is_file()]
    return not files or all(f.name == "PLACEHOLDER.md" for f in files)


def skill_text(root: Path) -> str:
    chunks = []
    for f in [root / "SKILL.md", *sorted((root / "references").rglob("*")), *sorted((root / "scripts").rglob("*"))]:
        if f.is_file() and f.stat().st_size < 2_000_000:
            try:
                chunks.append(f.read_text())
            except UnicodeDecodeError:
                pass
    return "\n".join(chunks)


def check_leakage(root: Path, tid: str, task: dict, fixtures: Path) -> None:
    text = skill_text(root)
    for a in task.get("assertions") or []:
        exp = a.get("expect") if isinstance(a.get("expect"), dict) else {}
        for lit in regex_literals(str(a.get("pattern", ""))) + [str(v) for v in exp.values() if isinstance(v, str)]:
            if len(lit) >= 6 and lit in text:
                review(f"{tid}: the skill contains {lit!r}, which an assertion matches. Knowledge about the part is fine; "
                       "an output string written exactly as the eval checks it is an answer")
    ref = fixtures / tid / "reference"
    if ref.is_dir():
        for f in ref.rglob("*"):
            if not f.is_file() or f.suffix not in {".c", ".h", ".cpp", ".ino", ".py", ".rs", ".txt", ".yaml", ".conf"}:
                continue
            try:
                lines = f.read_text().splitlines()
            except UnicodeDecodeError:
                continue
            for line in lines:
                s = line.strip()
                if BOILERPLATE.match(s):
                    continue
                if len(s) >= 40 and s in text:
                    review(f"{tid}: a line of reference/{f.relative_to(ref)} appears verbatim in the skill: {s[:80]!r}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill")
    ap.add_argument("--run-empty", action="store_true")
    ap.add_argument("--attest", action="store_true")
    args = ap.parse_args()
    root = Path(args.skill)
    evals = root / "evals"
    if not (root / "SKILL.md").is_file() or not (evals / "manifest.yaml").is_file():
        err(f"{root}: needs SKILL.md and evals/manifest.yaml")
        return 1

    for f in [root / "SKILL.md", *evals.rglob("*.yaml"), *(root / "references").rglob("*.md")]:
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if "TODO:" in re.sub(r"`[^`]*`", "", line):  # a TODO: quoted in backticks is prose about markers
                err(f"{f.relative_to(root)}:{n}: unfinished TODO")

    m = load(evals / "manifest.yaml")
    board = str((m.get("target") or {}).get("board", ""))
    if FAMILY_WORDS.match(board.strip()):
        err(f"manifest target.board {board!r} is a family name; use the exact board id")
    if not m.get("boot_banner"):
        err("manifest has no boot_banner; a crash loop can satisfy min_matches on its own")
    if not m.get("reboot_patterns"):
        err("manifest has no reboot_patterns; a panic that does not reboot goes unnoticed")
    else:
        for p in [*m["reboot_patterns"], *([m["boot_banner"]] if m.get("boot_banner") else [])]:
            try:
                re.compile(p)
            except re.error as e:
                err(f"reboot_patterns {p!r} is not a valid regex: {e}")

    tasks = sorted((evals / "tasks").glob("*.yaml"))
    if len(tasks) < 3:
        review(f"{len(tasks)} task(s); EVALS.md recommends three (easy, medium, hard)")
    fixtures = evals / "fixtures"
    for tf in tasks:
        t = load(tf)
        tid = t.get("id", tf.stem)
        if "todo" in tid:
            err(f"{tid}: rename the task (and its fixtures directory)")
        prompt = t.get("prompt") or ""
        if not (t.get("build") or {}).get("cmd"):
            err(f"{tid}: build.cmd missing; the tester cannot rebuild the frozen copy")
        flash_cmd = (t.get("flash") or {}).get("cmd")
        if flash_cmd and "{port}" not in flash_cmd:
            review(f"{tid}: flash.cmd has no {{port}}; a hard-coded port breaks on another bench")
        if re.search(r"chip[ _-]?id|unique id|read[-_ ]mac", prompt, re.I):
            review(f"{tid}: the prompt mentions the chip ID; only the reference prints it, asking the agent changes the task")
        types = [a.get("type") for a in t.get("assertions") or []]
        if all(x in ("compile_only", "exit_code") for x in types):
            review(f"{tid}: no runtime observation; prefer serial, GPIO or bus evidence from the board")
        if t.get("human_action"):
            if not any(a.get("after_human_action") for a in t.get("assertions") or []):
                review(f"{tid}: has human_action but no assertion sets after_human_action: true, so there is no control window")
        for a in t.get("assertions") or []:
            check_prompt_values(tid, prompt, a)
            if args.run_empty and a.get("type") == "exit_code" and a.get("cmd"):
                run_empty(tid, "exit_code", a["cmd"], int(a.get("expect", 0)))
        if args.run_empty and (t.get("build") or {}).get("cmd") and "TODO:" not in t["build"]["cmd"]:
            run_empty(tid, "build.cmd", t["build"]["cmd"], 0)

        for kind in ("reference", "broken", "spoof"):
            d = fixtures / tid / kind
            if not d.is_dir():
                (err if args.attest else review)(f"{tid}: missing fixtures/{tid}/{kind}/ (Phase 0)")
            elif fixture_is_placeholder(d):
                (err if args.attest else note)(f"{tid}: fixtures/{tid}/{kind}/ is still a placeholder")
        check_leakage(root, tid, t, fixtures)

    tq = evals / "trigger_queries.json"
    if not tq.is_file():
        review("no evals/trigger_queries.json; the trigger pre-check (EVALS.md, Pre-checks) is the cheapest check there is")
    else:
        import json
        try:
            queries = json.loads(tq.read_text())
        except json.JSONDecodeError as e:
            queries = None
            err(f"evals/trigger_queries.json is not valid JSON: {e}")
        if queries is not None:
            if not isinstance(queries, list) or not all(isinstance(q, dict) and isinstance(q.get("query"), str)
                                                        and isinstance(q.get("should_trigger"), bool) for q in queries):
                err("evals/trigger_queries.json must be a list of {\"query\": str, \"should_trigger\": bool}")
            else:
                if any("TODO:" in q["query"] for q in queries):
                    err("evals/trigger_queries.json: unfinished TODO")
                pos = sum(q["should_trigger"] for q in queries)
                if pos < 8 or len(queries) - pos < 8:
                    review(f"evals/trigger_queries.json has {pos} should-trigger and {len(queries) - pos} near-miss "
                           "queries; aim for 8-10 of each")

    v = m.get("eval_validated")
    if not v:
        (err if args.attest else note)("eval_validated is empty: Phase 0 has not been recorded, so no attestation is accepted")
    else:
        for k in VALIDATED_FIELDS:
            if v.get(k) in (None, "", False):
                err(f"eval_validated.{k} is missing or false")

    print(f"{'FAILED' if errors else 'OK'}: {errors} error(s) in {root}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
