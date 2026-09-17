#!/usr/bin/env python3
"""Bench helpers for Phase 1-3 runs in EVALS.md.

  bench.py install <skill-dir> <dest-parent>   copy the skill WITHOUT evals/ and .git, print its tree hash
  bench.py hash <dir>                          SHA-256 of a directory tree (paths + contents, sorted)
  bench.py freeze <workdir> <out.tar.gz>       archive the agent's working directory, print both hashes
  bench.py capture --port P --baud B --seconds S --out LOG [--reset rts]
                                               log serial lines with host timestamps; time zero is written
                                               first. --reset rts pulses RTS the way esptool's hard reset
                                               does (EN low on ESP32 dev boards with the auto-reset circuit).
                                               Without it, press Enter and then reset the board by hand;
                                               time zero is the Enter, so windows err on the strict side. Needs pyserial.
  bench.py serial <LOG> <task.yaml> [--manifest manifest.yaml] [--action-at S[,S...]]
                                               evaluate the task's serial_match assertions and the reboot
                                               guard against a captured log

Log format: a first line '# time_zero <unix seconds>', then '<unix seconds>\\t<line>' per line.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tarfile
import time
from pathlib import Path

import yaml

EXCLUDE = {"evals", ".git"}


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            h.update(f"L {rel} {os.readlink(p)}\n".encode())
        elif p.is_file():
            h.update(f"F {rel} {hashlib.sha256(p.read_bytes()).hexdigest()}\n".encode())
        elif p.is_dir():
            h.update(f"D {rel}\n".encode())
    return h.hexdigest()


def cmd_install(a) -> int:
    src = Path(a.skill).resolve()
    dest = Path(a.dest) / src.name
    if dest.exists():
        print(f"{dest} exists; restore the host baseline instead of installing over an old copy", file=sys.stderr)
        return 2
    shutil.copytree(src, dest, ignore=lambda d, names: [n for n in names if Path(d) == src and n in EXCLUDE or n == ".git"])
    leftovers = [p for p in [dest / "evals", *dest.rglob(".git")] if p.exists()]
    if leftovers:
        print(f"refusing: {leftovers[0]} still present in the installed copy", file=sys.stderr)
        return 1
    print(f"installed {dest}")
    print(f"skill_dir_sha256.before: {tree_hash(dest)}")
    print("Keep the eval package outside every path the agent's harness can read.")
    return 0


def cmd_hash(a) -> int:
    print(tree_hash(Path(a.dir)))
    return 0


def cmd_freeze(a) -> int:
    wd = Path(a.workdir)
    digest = tree_hash(wd)
    with tarfile.open(a.out, "w:gz") as tar:
        tar.add(wd, arcname=wd.name)
    print(f"workdir_sha256: {digest}")
    print(f"archive_sha256: {hashlib.sha256(Path(a.out).read_bytes()).hexdigest()}")
    print("Build, flash and observe from this archive, not from the live directory.")
    return 0


def cmd_capture(a) -> int:
    try:
        import serial  # type: ignore
    except ImportError:
        print("pyserial is required: pip install pyserial", file=sys.stderr)
        return 2
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = a.port, a.baud, 0.1
    s.dtr = False  # opening the port must not reset the board or hold it in the bootloader
    s.rts = False
    s.open()
    out = open(a.out, "w")
    if a.reset == "rts":
        s.rts = True
        time.sleep(0.1)
        s.rts = False
        t0 = time.time()
    else:
        # Time zero is taken before the tester's reset, so windows can only get shorter, never longer.
        input("Press Enter, then immediately press and release the board's reset button... ")
        t0 = time.time()
    out.write(f"# time_zero {t0:.3f}\n")
    buf = b""
    try:
        while time.time() - t0 < a.seconds:
            chunk = s.read(4096)
            if not chunk:
                continue
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                out.write(f"{time.time():.3f}\t{line.decode('utf-8', 'replace').rstrip(chr(13))}\n")
                out.flush()
    except serial.SerialException as e:
        out.write(f"# port error at +{time.time() - t0:.3f}s: {e}\n")
        print(f"port lost ({e}); on native USB this is a re-enumeration and counts as a reboot", file=sys.stderr)
    finally:
        if buf:
            out.write(f"{time.time():.3f}\t{buf.decode('utf-8', 'replace')}\n")
        out.close()
        s.close()
    print(f"wrote {a.out}; now read the chip ID on the same port within 10 s, without unplugging")
    return 0


def read_log(path: Path) -> tuple[float, list[tuple[float, str]], list[str]]:
    t0, lines, notes = None, [], []
    for raw in path.read_text().splitlines():
        if raw.startswith("# time_zero "):
            t0 = float(raw.split()[2])
        elif raw.startswith("#"):
            notes.append(raw)
        elif "\t" in raw:
            ts, text = raw.split("\t", 1)
            lines.append((float(ts), text))
    if t0 is None:
        raise SystemExit(f"{path}: no '# time_zero' line")
    return t0, lines, notes


def cmd_serial(a) -> int:
    t0, lines, notes = read_log(Path(a.log))
    task = yaml.safe_load(Path(a.task).read_text()) or {}
    manifest = yaml.safe_load(Path(a.manifest).read_text()) if a.manifest else {}
    patterns = (manifest or {}).get("reboot_patterns") or []
    banner = (manifest or {}).get("boot_banner")
    ok = True

    if task.get("expect_reset"):
        print("reboot_guard: skipped (expect_reset: true)")
    else:
        after = [(ts - t0, text) for ts, text in lines if ts >= t0]
        fatal = [(r, text) for r, text in after if any(re.search(p, text) for p in patterns)]
        boots = [(r, text) for r, text in after if banner and re.search(banner, text)]
        lost = [n for n in notes if "port error" in n]
        # The boot that time zero starts prints the banner once; a second banner is a reboot.
        if fatal or len(boots) > 1 or lost:
            ok = False
            if fatal:
                why = f"+{fatal[0][0]:.2f}s {fatal[0][1]!r}"
            elif len(boots) > 1:
                why = f"second boot banner at +{boots[1][0]:.2f}s {boots[1][1]!r}"
            else:
                why = lost[0]
            print(f"reboot_guard: FAIL ({why})")
        elif not patterns and not banner:
            print("reboot_guard: NOT CHECKED - manifest has no boot_banner or reboot_patterns")
        else:
            print(f"reboot_guard: pass ({len(boots)} boot banner(s), no fatal pattern)")

    for i, asrt in enumerate(task.get("assertions") or []):
        if asrt.get("type") != "serial_match":
            continue
        pat = re.compile(asrt["pattern"])
        window = float(asrt.get("within_s", 1e9))
        rel = [(ts - t0, text) for ts, text in lines]
        matched = [r for r, text in rel if 0 <= r <= window and pat.search(text)]
        need = int(asrt.get("min_matches", 1))
        cap = asrt.get("max_matches")
        result = len(matched) >= need and (cap is None or len(matched) <= int(cap))
        detail = f"{len(matched)} match(es) in [0, {window:g}] s, need {need}" + ("" if cap is None else f" to {cap}")
        if asrt.get("after_human_action"):
            if a.action_at is None:
                result, detail = False, detail + "; after_human_action set but no --action-at given"
            else:
                first_action = min(a.action_at)
                early = [r for r in matched if r < first_action]
                if early:
                    result = False
                    detail += f"; {len(early)} before the first human action at +{first_action:g}s (control window)"
                else:
                    detail += f"; none before the first human action at +{first_action:g}s"
        ok &= result
        print(f"assertion[{i}] serial_match {asrt['pattern']!r}: {'pass' if result else 'FAIL'} ({detail})")

    print("serial result:", "pass" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("install"); p.add_argument("skill"); p.add_argument("dest"); p.set_defaults(f=cmd_install)
    p = sub.add_parser("hash"); p.add_argument("dir"); p.set_defaults(f=cmd_hash)
    p = sub.add_parser("freeze"); p.add_argument("workdir"); p.add_argument("out"); p.set_defaults(f=cmd_freeze)
    p = sub.add_parser("capture")
    p.add_argument("--port", required=True); p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--seconds", type=float, required=True); p.add_argument("--out", required=True)
    p.add_argument("--reset", choices=["rts", "manual"], default="manual"); p.set_defaults(f=cmd_capture)
    p = sub.add_parser("serial")
    p.add_argument("log"); p.add_argument("task"); p.add_argument("--manifest")
    p.add_argument("--action-at", type=lambda v: [float(x) for x in v.split(",")],
                   help="seconds after time zero of each human action, comma-separated, e.g. 5,8,11")
    p.set_defaults(f=cmd_serial)
    a = ap.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
