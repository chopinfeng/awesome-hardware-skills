#!/usr/bin/env python3
"""L0 static checks.

  l0_check.py readme README.md          lint list entries + verify links resolve
  l0_check.py links GAPS.md             verify every link in a markdown file resolves
  l0_check.py sync README.md README.zh-CN.md   translations list the same entries in the same order
  l0_check.py skill path/to/skill       lint a skill's SKILL.md frontmatter + evals/ package
  l0_check.py forms .github/ISSUE_TEMPLATE   issue forms parse and have the fields GitHub requires
"""
from __future__ import annotations

import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\((https?://[^)\s]+)\) - (.+)$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
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
        # some CDNs answer HEAD with 404 for a resource GET serves fine; confirm before failing
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=req.headers), timeout=20) as r:
                return url, r.status
        except Exception:  # noqa: BLE001
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
        if not (desc[0].isupper() or desc[0].isdigit() or desc[0] in "`\"") or not desc.rstrip().endswith((".", ")", "`")):
            fail(f"{path}:{n}: description should start with a capital, digit or code span and end with a period")
    with ThreadPoolExecutor(16) as ex:
        for url, status in ex.map(head, urls):
            if not (isinstance(status, int) and status < 400 or status in (403, 405, 429)):
                fail(f"{path}:{urls[url]}: {url} -> {status}")
    print(f"checked {len(urls)} links")


def check_links(path: Path) -> None:
    """Every link in a markdown file: http(s) must resolve, relative must exist on disk."""
    remote: dict[str, int] = {}
    in_fence = False
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for target in LINK_RE.findall(line):
            if target.startswith("#"):
                continue
            if target.startswith(("http://", "https://")):
                remote.setdefault(target, n)
            else:
                local = (path.parent / target.split("#", 1)[0]).resolve()
                if not local.exists():
                    fail(f"{path}:{n}: {target} does not exist")
    with ThreadPoolExecutor(16) as ex:
        for url, status in ex.map(head, remote):
            if not (isinstance(status, int) and status < 400 or status in (403, 405, 429)):
                fail(f"{path}:{remote[url]}: {url} -> {status}")
    print(f"checked {len(remote)} links in {path}")


def entry_urls(path: Path) -> list[str]:
    return [m.group(2) for ln in path.read_text().splitlines() if (m := ENTRY_RE.match(ln))]


def check_sync(source: Path, translation: Path) -> None:
    """A translation must carry exactly the source's entries, in the same order."""
    src, dst = entry_urls(source), entry_urls(translation)
    missing = [u for u in src if u not in set(dst)]
    extra = [u for u in dst if u not in set(src)]
    for u in missing:
        fail(f"{translation}: missing entry present in {source}: {u}")
    for u in extra:
        fail(f"{translation}: entry not present in {source}: {u}")
    if not missing and not extra and src != dst:
        i = next(i for i, (a, b) in enumerate(zip(src, dst)) if a != b)
        fail(f"{translation}: entry order diverges from {source} at position {i + 1}: {dst[i]} (expected {src[i]})")
    heading = re.compile(r"^(#{2,3}) ", re.M)
    src_h = [h for h in heading.findall(source.read_text())]
    dst_h = [h for h in heading.findall(translation.read_text())]
    if src_h != dst_h:
        fail(f"{translation}: section structure differs from {source} "
             f"({len(src_h)} vs {len(dst_h)} level-2/3 headings) — a section was added or removed on one side only")
    print(f"checked {len(src)} entries and {len(src_h)} sections in {source} against {translation}")


def check_forms(directory: Path) -> None:
    """GitHub silently drops an issue form it cannot parse, so a broken one looks fine until someone needs it."""
    forms = sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml"))
    for f in forms:
        if f.name == "config.yml":
            continue
        try:
            form = yaml.safe_load(f.read_text()) or {}
        except yaml.YAMLError as e:
            fail(f"{f}: not valid YAML — GitHub will not show this form: {str(e).splitlines()[0]}")
            continue
        for k in ("name", "description", "body"):
            if not form.get(k):
                fail(f"{f}: issue form missing `{k}`")
        ids = [el.get("id") for el in form.get("body") or [] if isinstance(el, dict) and el.get("id")]
        if len(ids) != len(set(ids)):
            fail(f"{f}: duplicate element ids")
    print(f"checked {len(forms)} issue forms in {directory}")


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
        if not isinstance(task.get("timeout_s"), (int, float)) or task["timeout_s"] <= 0:
            fail(f"{t}: timeout_s must be a positive number of seconds")
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
    mode, targets = sys.argv[1], [Path(a) for a in sys.argv[2:]]
    {"readme": check_readme, "links": check_links, "sync": check_sync, "forms": check_forms, "skill": check_skill}[mode](*targets)
    sys.exit(1 if fail.count else 0)
