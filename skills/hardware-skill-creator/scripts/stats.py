#!/usr/bin/env python3
"""The numbers EVALS.md asks for, computed the way it defines them.

  stats.py wilson K N                        95% Wilson interval for k/n
  stats.py task RESULT [RESULT ...]          two-of-at-most-three verdict; results are pass|fail|invalid in run order
  stats.py delta K_WITH N_WITH K_WITHOUT N_WITHOUT
                                             ΔPass with its 95% Newcombe interval and label
                                             (gain | harm | low-gain | inconclusive)
  stats.py passk C N K                       unbiased pass^k from C passes in N runs, e.g. passk 4 5 2 -> 0.6
  stats.py selftest                          checks the formulas against published reference values

Invalid runs are rerun and never counted; they are skipped by `task` but still belong in the record.
"""
from __future__ import annotations

import sys
from math import sqrt


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def delta_pass(k_with: int, n_with: int, k_without: int, n_without: int):
    p1, p2 = k_with / n_with, k_without / n_without
    l1, u1 = wilson(k_with, n_with)
    l2, u2 = wilson(k_without, n_without)
    d = p1 - p2
    lo = d - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    label = "gain" if lo > 0 else "harm" if hi < 0 else "low-gain" if hi < 0.15 else "inconclusive"
    return d, lo, hi, label


def pass_k(c: int, n: int, k: int) -> float:
    """Unbiased estimate of pass^k (all k independent runs pass) from c passes in n runs: C(c,k)/C(n,k)."""
    from math import comb
    if not 0 <= c <= n or k > n:
        raise SystemExit("need 0 <= c <= n and k <= n")
    return comb(c, k) / comb(n, k)


def task_verdict(results: list[str]) -> str:
    counted = [r for r in results if r in ("pass", "fail")]
    bad = [r for r in results if r not in ("pass", "fail", "invalid")]
    if bad:
        raise SystemExit(f"unknown result(s) {bad}; use pass, fail or invalid")
    k, n = counted.count("pass"), len(counted)
    if k >= 2:
        verdict = "task pass"
    elif n - k >= 2:
        verdict = "task fail"
    elif n < 2:
        return f"{k}/{n} counted - run again"
    else:
        return f"{k}/{n} counted - split, run a third time"
    extra = "" if n <= 3 else "  WARNING: more than three counted runs; the rule stops at the second agreeing run"
    lo, hi = wilson(k, n)
    return f"{verdict} ({k}/{n}), 95% Wilson [{lo:.2f}, {hi:.2f}]{extra}"


def selftest() -> None:
    # Newcombe (1998) method 10, example (56/70 v 48/80): 0.200 [0.0524, 0.3339]
    d, lo, hi, _ = delta_pass(56, 70, 48, 80)
    assert (round(d, 3), round(lo, 3), round(hi, 3)) == (0.2, 0.052, 0.334), (d, lo, hi)
    # Wilson for 0/10: [0, 0.278] (Newcombe 1998, method 3)
    lo, hi = wilson(0, 10)
    assert abs(lo) < 1e-9 and round(hi, 3) == 0.278, (lo, hi)
    assert task_verdict(["pass", "pass"]).startswith("task pass")
    assert task_verdict(["pass", "fail"]).endswith("run a third time")
    assert task_verdict(["pass", "invalid", "fail", "pass"]).startswith("task pass (2/3)")
    assert task_verdict(["fail", "fail"]).startswith("task fail")
    assert delta_pass(0, 15, 10, 15)[3] == "harm"
    assert [round(pass_k(c, 5, 2), 2) for c in (5, 4, 3)] == [1.0, 0.6, 0.3]
    print("selftest ok")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "wilson":
        k, n = map(int, rest)
        lo, hi = wilson(k, n)
        print(f"{k}/{n} = {k / n:.2f}, 95% Wilson [{lo:.2f}, {hi:.2f}]")
    elif cmd == "task":
        print(task_verdict(rest))
    elif cmd == "delta":
        kw, nw, ko, no = map(int, rest)
        d, lo, hi, label = delta_pass(kw, nw, ko, no)
        print(f"ΔPass {d * 100:+.0f} pts [{lo * 100:+.0f}, {hi * 100:+.0f}] ({nw} v {no}), {label}")
        if nw < 100 or no < 100:
            print("note: below ~100 runs per arm, low-gain is out of reach; inconclusive is the honest label")
    elif cmd == "passk":
        c, n, k = map(int, rest)
        print(f"pass^{k} = {pass_k(c, n, k):.2f} ({c}/{n} runs passed)")
    elif cmd == "selftest":
        selftest()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
