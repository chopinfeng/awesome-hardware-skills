#!/usr/bin/env python3
"""Refresh stars, last-push month, renames and staleness for every GitHub entry in both READMEs.

  refresh_meta.py            report and rewrite README.md and README.zh-CN.md in place
  refresh_meta.py --dry-run  report only

Needs an authenticated `gh` CLI. Queries GitHub GraphQL 50 repositories at a time.
An entry whose repository is gone is reported, never deleted automatically: removal is a maintainer decision.
A repository with no push in the last 12 months gets `stale since YYYY-MM`; one that is pushed again loses it.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / "README.md", ROOT / "README.zh-CN.md"]
ENTRY = re.compile(r"^(- \[)([^\]]+)(\]\()(https://github\.com/([^/)\s]+)/([^/)\s#?]+)[^)\s]*)(\) - )(.+)$")
TAIL = re.compile(r"(\s?)\(([^()]*(?:★|stale since)[^()]*)\)\s*$")


def stars_fmt(n: int) -> str:
    if n < 1000:
        return f"★{n}"
    return "★" + f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"


def query(repos: list[tuple[str, str]]) -> dict:
    parts = []
    for i, (o, r) in enumerate(repos):
        parts.append(f'r{i}: repository(owner: {json.dumps(o)}, name: {json.dumps(r)}) '
                     '{ nameWithOwner stargazerCount pushedAt isArchived isFork }')
    q = "query {" + " ".join(parts) + "}"
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"], capture_output=True, text=True)
    data = json.loads(out.stdout or "{}").get("data") or {}
    return {repos[int(k[1:])]: v for k, v in data.items()}


def main() -> int:
    dry = "--dry-run" in sys.argv
    today = dt.date.today()
    cutoff = today.replace(year=today.year - 1).isoformat()
    keys = []
    for f in FILES:
        for line in f.read_text().split("\n"):
            m = ENTRY.match(line)
            if m:
                keys.append((m.group(5), m.group(6).removesuffix(".git")))
    uniq = sorted(set(keys))
    meta: dict = {}
    for i in range(0, len(uniq), 50):
        meta.update(query(uniq[i:i + 50]))
    gone = [k for k in uniq if not meta.get(k)]

    changes = {"stars/date": 0, "renamed": 0, "now stale": 0, "no longer stale": 0}
    report = []
    for f in FILES:
        out = []
        for n, line in enumerate(f.read_text().split("\n"), 1):
            m = ENTRY.match(line)
            info = meta.get((m.group(5), m.group(6).removesuffix(".git"))) if m else None
            if not m or not info:
                out.append(line)
                continue
            name, url, desc = m.group(2), m.group(4), m.group(8)
            owner_repo = f"{m.group(5)}/{m.group(6)}"
            new_full = info["nameWithOwner"]
            if new_full.lower() != owner_repo.lower():
                url = url.replace(f"github.com/{owner_repo}", f"github.com/{new_full}", 1)
                if name.lower().startswith(owner_repo.lower()):
                    name = new_full + name[len(owner_repo):]
                if f.name == "README.md":
                    changes["renamed"] += 1
                    report.append(f"renamed {owner_repo} -> {new_full}")
            t = TAIL.search(desc)
            if t:
                sep, parts = t.group(1), [p.strip() for p in t.group(2).split("·")]
                pushed = info["pushedAt"][:7]
                was_stale = any(p.startswith("stale since") for p in parts)
                is_stale = info["pushedAt"][:10] < cutoff or info["isArchived"]
                tags = [p for p in parts if not (p.startswith("★") or p.startswith("stale since")
                                                  or re.fullmatch(r"\d{4}-\d{2}", p))]
                new_parts = tags + [stars_fmt(info["stargazerCount"]),
                                    f"stale since {pushed}" if is_stale else pushed]
                new_desc = desc[: t.start()] + f"{sep}({' · '.join(new_parts)})"
                if new_desc != desc and f.name == "README.md":
                    changes["stars/date"] += 1
                    if is_stale and not was_stale:
                        changes["now stale"] += 1
                        report.append(f"now stale: {new_full} (last push {pushed}, archived={info['isArchived']})")
                    if was_stale and not is_stale:
                        changes["no longer stale"] += 1
                desc = new_desc
            out.append(f"{m.group(1)}{name}{m.group(3)}{url}{m.group(7)}{desc}")
        if not dry:
            f.write_text("\n".join(out))
    for k in gone:
        report.append(f"GONE (404, needs a decision): github.com/{k[0]}/{k[1]}")
    print("\n".join(report))
    print(f"{len(uniq)} repositories checked; " + ", ".join(f"{k}: {v}" for k, v in changes.items())
          + f"; gone: {len(gone)}" + (" (dry run)" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
