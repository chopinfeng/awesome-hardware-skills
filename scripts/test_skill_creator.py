#!/usr/bin/env python3
"""Regression tests for skills/hardware-skill-creator/scripts. Run: python scripts/test_skill_creator.py"""
from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / "skills" / "hardware-skill-creator"
S = SK / "scripts"
failures = 0


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd)


def check(name: str, cond: bool, detail: str = "") -> None:
    global failures
    if cond:
        print(f"ok   {name}")
    else:
        failures += 1
        print(f"FAIL {name}\n{textwrap.indent(detail, '     ')}")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text))


def main() -> int:
    check("l0_check.py copy is identical to scripts/l0_check.py",
          filecmp.cmp(ROOT / "scripts" / "l0_check.py", S / "l0_check.py", shallow=False))

    r = run(str(S / "stats.py"), "selftest")
    check("stats selftest (Newcombe and Wilson reference values)", r.returncode == 0, r.stdout + r.stderr)

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)

        r = run(str(S / "init_skill.py"), "named", "--board", "b", "--framework", "f", "--framework-version", "1",
                "--family", "esp32", "--task-ids", "toggle,boot-button,isr-count", "--out", str(t))
        check("scaffold with --task-ids names tasks and fixtures",
              (t / "named/evals/tasks/02-boot-button.yaml").exists()
              and (t / "named/evals/fixtures/03-isr-count/spoof/PLACEHOLDER.md").exists(), r.stdout + r.stderr)

        for fam in ("esp32", "nrf52", "stm32", "rp2040", "other"):
            r = run(str(S / "init_skill.py"), f"demo-{fam}", "--board", "b", "--framework", "f",
                    "--framework-version", "1", "--family", fam, "--out", str(t))
            check(f"scaffold {fam}", r.returncode == 0, r.stderr)
            r = run(str(ROOT / "scripts" / "l0_check.py"), "skill", str(t / f"demo-{fam}"))
            check(f"scaffold {fam} passes L0", r.returncode == 0, r.stdout)
            r = run(str(S / "check_package.py"), str(t / f"demo-{fam}"))
            check(f"scaffold {fam} fails check_package until TODOs are filled",
                  r.returncode == 1 and "unfinished TODO" in r.stdout, r.stdout)

        pkg = t / "vacuous"
        write(pkg / "SKILL.md", """\
            ---
            name: vacuous
            description: A test skill whose eval contains the vacuous grep assertion documented in EVALS.md Phase 0.
            ---
            body
            """)
        write(pkg / "evals" / "manifest.yaml", """\
            skill: vacuous
            target: {board: esp32-c3-devkitm-1, framework: arduino, framework_version: "3.0"}
            simulator: none
            assertions_supported: [compile_only, serial_match, exit_code]
            boot_banner: '^rst:0x'
            reboot_patterns: ['Guru Meditation']
            """)
        write(pkg / "evals" / "tasks" / "01-scan.yaml", """\
            id: 01-scan
            level: medium
            timeout_s: 600
            prompt: |
              Scan I2C and print "found 0x.." for each address. Do not call Wire.begin().
            build: {cmd: "exit 1"}
            assertions:
              - type: serial_match
                baud: 115200
                pattern: 'found 0x34'
                min_matches: 1
                within_s: 5
              - type: exit_code
                cmd: '! grep -q "Wire.begin(" *.ino'
                expect: 0
            """)
        r = run(str(S / "check_package.py"), str(pkg), "--run-empty")
        check("check_package flags the vacuous grep", "is vacuous" in r.stdout, r.stdout)
        check("check_package flags a baud missing from the prompt", "baud 115200 is not in the prompt" in r.stdout, r.stdout)

        missing = t / "missing-tool"
        missing.mkdir()
        for sub in ("SKILL.md", "evals"):
            src = pkg / sub
            (missing / sub).parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copytree(pkg, missing, dirs_exist_ok=True)
        tf = missing / "evals" / "tasks" / "01-scan.yaml"
        tf.write_text(tf.read_text().replace('build: {cmd: "exit 1"}', 'build: {cmd: "no-such-build-tool-hwsc build"}'))
        r = run(str(S / "check_package.py"), str(missing), "--run-empty")
        check("check_package treats a missing build tool as an error, not a failing assertion",
              "could not run (exit 127" in r.stdout, r.stdout)

        (pkg / "evals" / "trigger_queries.json").write_text('[{"query": "x"}]')
        r = run(str(S / "check_package.py"), str(pkg))
        check("check_package rejects a malformed trigger_queries.json", "must be a list of" in r.stdout, r.stdout)
        (pkg / "evals" / "trigger_queries.json").unlink()

        r = run(str(S / "stats.py"), "delta", "0", "15", "10", "15")
        check("stats labels a significant negative ΔPass as harm", r.stdout.strip().split("\n")[0].endswith("harm"), r.stdout)

        r = run(str(S / "check_package.py"), str(SK))
        check("hardware-skill-creator's own eval package has no errors", r.returncode == 0, r.stdout)
        r = run(str(S / "check_package.py"), str(ROOT / "template"))
        check("template eval package has no errors", r.returncode == 0, r.stdout)

        write(t / "m.yaml", """\
            boot_banner: '^rst:0x'
            reboot_patterns: ['Guru Meditation|abort\\(\\) was called|assert failed:|Backtrace:', 'Brownout detector']
            """)
        write(t / "task.yaml", """\
            id: x
            assertions:
              - {type: serial_match, pattern: '^tick$', min_matches: 4, max_matches: 8, within_s: 3}
              - {type: serial_match, pattern: '^button down$', min_matches: 1, within_s: 10, after_human_action: true}
            """)
        logs = {
            "clean": ["100.06\trst:0x1 (POWERON)", *[f"{100.5 + i * 0.5}\ttick" for i in range(4)], "106.0\tbutton down"],
            "panic": ["100.06\trst:0x1 (POWERON)", *[f"{100.5 + i * 0.5}\ttick" for i in range(4)],
                      "102.6\tGuru Meditation Error: Core  0 panic'ed", "106.0\tbutton down"],
            "second-banner": ["100.06\trst:0x1 (POWERON)", "100.5\ttick", "101.0\trst:0xc (SW_CPU_RESET)",
                              *[f"{101.2 + i * 0.3}\ttick" for i in range(4)], "106.0\tbutton down"],
            "too-fast": ["100.06\trst:0x1 (POWERON)", *[f"{100.1 + i * 0.1}\ttick" for i in range(20)], "106.0\tbutton down"],
            "early-output": ["100.06\trst:0x1 (POWERON)", *[f"{100.5 + i * 0.5}\ttick" for i in range(4)],
                             "103.0\tbutton down"],
        }
        expected = {"clean": 0, "panic": 1, "second-banner": 1, "too-fast": 1, "early-output": 1}
        for name, lines in logs.items():
            (t / f"{name}.log").write_text("# time_zero 100.0\n" + "\n".join(lines) + "\n")
            r = run(str(S / "bench.py"), "serial", str(t / f"{name}.log"), str(t / "task.yaml"),
                    "--manifest", str(t / "m.yaml"), "--action-at", "5,8")
            check(f"bench serial: {name} log -> exit {expected[name]}", r.returncode == expected[name], r.stdout + r.stderr)

        (t / "inst").mkdir()
        r = run(str(S / "bench.py"), "install", str(SK), str(t / "inst"))
        inst = t / "inst" / SK.name
        check("bench install strips evals/", r.returncode == 0 and (inst / "SKILL.md").exists()
              and not (inst / "evals").exists(), r.stdout + r.stderr)
        before = r.stdout.split("skill_dir_sha256.before: ")[1].split()[0] if r.returncode == 0 else ""
        (inst / "SKILL.md").write_text((inst / "SKILL.md").read_text() + "\ntampered\n")
        r = run(str(S / "bench.py"), "hash", str(inst))
        check("bench hash changes when the installed skill is edited", r.stdout.strip() != before, r.stdout)

    print(f"{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
