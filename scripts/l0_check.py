#!/usr/bin/env python3
"""L0 static checks.

  l0_check.py readme README.md          lint list entries + verify links resolve
  l0_check.py skill path/to/skill       lint a skill's SKILL.md frontmatter + evals/ package
"""
from __future__ import annotations

import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\((https?://[^)\s]+)\) - (.+)$")
ASSERTION_TYPES = {
    "compile_only", "serial_match", "gpio_state", "bus_capture",
    "network_probe", "ros_topic", "file_exists", "exit_code",
}
SIMULATORS = {
    "wokwi", "renode", "qemu", "native_sim", "gazebo", "isaac",
    "mujoco", "webots", "ha-demo", "modbus-sim", "opcua-sim", "none",
}
LEVELS = {"easy", "medium", "hard"}
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36})")


def fail(msg: str) -> None:
    print(f"::error::{msg}")
    fail.count += 1


fail.count = 0


def head(url: str) -> tuple[str, int | str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "awesome-hardware-skills-l0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429):
            return url, e.code  # GitHub and friends often reject HEAD; treated as ok below
        return url, e.code
    except Exception:  # noqa: BLE001
        # some hosts reject HEAD at the TLS/HTTP2 layer; confirm with GET before failing
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=req.headers), timeout=15) as r:
                return url, r.status
        except Exception as e:  # noqa: BLE001
            return url, type(e).__name__


def check_readme(path: Path) -> None:
    urls: dict[str, int] = {}
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.startswith("- [") or "](#" in line:
            continue
        m = ENTRY_RE.match(line)
        if not m:
            fail(f"{path}:{n}: entry must be `- [Name](url) - Description`")
            continue
        _, url, desc = m.groups()
        if url in urls:
            fail(f"{path}:{n}: duplicate url {url} (first at line {urls[url]})")
        urls[url] = n
        if not (desc[0].isupper() or desc[0].isdigit() or desc[0] == "`") or not desc.rstrip().endswith((".", ")", "`")):
            fail(f"{path}:{n}: description should start with a capital, digit or code span and end with a period")
    with ThreadPoolExecutor(16) as ex:
        for url, status in ex.map(head, urls):
            if not (isinstance(status, int) and status < 400 or status in (403, 405, 429)):
                fail(f"{path}:{urls[url]}: {url} -> {status}")
    print(f"checked {len(urls)} links")


def check_skill(root: Path) -> None:
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        fail(f"{root}: missing SKILL.md")
        return
    text = skill_md.read_text()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        fail(f"{skill_md}: missing YAML frontmatter")
        return
    meta = yaml.safe_load(fm.group(1)) or {}
    for k in ("name", "description"):
        if not meta.get(k):
            fail(f"{skill_md}: frontmatter missing `{k}`")
    if len(meta.get("description") or "") < 80:
        fail(f"{skill_md}: description under 80 chars — too short to trigger reliably")
    if SECRET_RE.search(text):
        fail(f"{skill_md}: looks like it contains a credential")

    evals = root / "evals"
    manifest_path = evals / "manifest.yaml"
    if not manifest_path.exists():
        fail(f"{root}: missing evals/manifest.yaml")
        return
    manifest = yaml.safe_load(manifest_path.read_text()) or {}
    if manifest.get("skill") != meta.get("name"):
        fail(f"{manifest_path}: `skill` must equal SKILL.md `name`")
    if manifest.get("simulator") not in SIMULATORS:
        fail(f"{manifest_path}: simulator must be one of {sorted(SIMULATORS)}")
    supported = set(manifest.get("assertions_supported") or [])
    if not supported <= ASSERTION_TYPES:
        fail(f"{manifest_path}: unknown assertion types {supported - ASSERTION_TYPES}")
    tgt = manifest.get("target") or {}
    for k in ("board", "framework", "framework_version"):
        if not tgt.get(k):
            fail(f"{manifest_path}: target.{k} required")

    tasks = sorted((evals / "tasks").glob("*.yaml"))
    if not tasks:
        fail(f"{evals}: no tasks/*.yaml")
    has_real_assertion = False
    for t in tasks:
        task = yaml.safe_load(t.read_text()) or {}
        if task.get("id") != t.stem:
            fail(f"{t}: id must equal filename stem")
        if task.get("level") not in LEVELS:
            fail(f"{t}: level must be one of {sorted(LEVELS)}")
        if not (task.get("prompt") or "").strip():
            fail(f"{t}: prompt is empty")
        for a in task.get("assertions") or []:
            if a.get("type") not in ASSERTION_TYPES:
                fail(f"{t}: unknown assertion type {a.get('type')}")
            elif a["type"] not in supported:
                fail(f"{t}: uses `{a['type']}` not declared in manifest.assertions_supported")
            if a.get("type") != "compile_only":
                has_real_assertion = True
    if not has_real_assertion:
        fail(f"{evals}: at least one task needs an assertion stronger than compile_only")
    print(f"checked {root}: {len(tasks)} tasks")


if __name__ == "__main__":
    mode, target = sys.argv[1], Path(sys.argv[2])
    {"readme": check_readme, "skill": check_skill}[mode](target)
    sys.exit(1 if fail.count else 0)
