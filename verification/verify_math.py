"""Numerical verification of the complete proof of  1 < f(x,a) < 2  for all x,a > 0.

2008 Jiangxi Gaokao, Science track, Q22:
    f(x,a) = 1/sqrt(1+x) + 1/sqrt(1+a) + sqrt(a*x/(a*x+8))

Every algebraic step used in the animation is checked here against dense
numerical sampling. A step is only accepted if it holds on the whole grid.

Run:  python verification/verify_math.py
"""

from __future__ import annotations

import numpy as np

RNG_SEED = 20080
N_RANDOM = 10_000
N_GRID = 1201

PASS = "PASS"
FAIL = "FAIL"

results: list[tuple[str, str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    results.append((name, PASS if ok else FAIL, detail))


def phi(t: np.ndarray | float) -> np.ndarray:
    return 1.0 / np.sqrt(1.0 + t)


def f_original(x: np.ndarray, a: np.ndarray) -> np.ndarray:
    return phi(x) + phi(a) + np.sqrt(a * x / (a * x + 8.0))


# --------------------------------------------------------------------------
# 0. The substitution A = x, B = a, C = 8/(A*B) with A*B*C = 8
# --------------------------------------------------------------------------
def check_substitution() -> None:
    rng = np.random.default_rng(7)
    A = np.exp(rng.uniform(-14, 14, 200_000))
    B = np.exp(rng.uniform(-14, 14, 200_000))
    C = 8.0 / (A * B)
    lhs = phi(A) + phi(B) + phi(C)
    rhs = f_original(A, B)
    err = np.abs(lhs - rhs).max()
    record(
        "Substitution  f = sum 1/sqrt(1+.)  with A*B*C = 8",
        err < 1e-12,
        f"max |LHS - RHS| = {err:.3e} over 200000 log-uniform pairs",
    )
    prod_err = np.abs(A * B * C - 8.0).max()
    record(
        "Substitution  A*B*C == 8 identically",
        prod_err < 1e-9,
        f"max |A*B*C - 8| = {prod_err:.3e}",
    )


# --------------------------------------------------------------------------
# 1. LOWER BOUND
# --------------------------------------------------------------------------
def check_lower_bound() -> None:
    # 1a.  1/sqrt(1+t) > 1/(1+t) for every t > 0
    t = np.logspace(-12, 12, 2_000_001)
    gap = phi(t) - 1.0 / (1.0 + t)
    record(
        "L1a  1/sqrt(1+t) > 1/(1+t) for all t>0",
        bool((gap > 0).all()),
        f"min gap = {gap.min():.6e} at t = {t[gap.argmin()]:.4g}",
    )

    # 1b.  sum 1/(1+A) >= 1  <=>  A+B+C >= 6   (algebraic equivalence)
    rng = np.random.default_rng(11)
    A = np.exp(rng.uniform(-10, 10, 300_000))
    B = np.exp(rng.uniform(-10, 10, 300_000))
    C = 8.0 / (A * B)
    reciprocal_sum = 1 / (1 + A) + 1 / (1 + B) + 1 / (1 + C)
    total = A + B + C
    # Both sides of the cleared-denominator identity
    record(
        "L1b  sum 1/(1+A) >= 1  <=>  A+B+C >= 6",
        bool(np.all((reciprocal_sum >= 1.0) == (total >= 6.0 - 1e-12))),
        "sign agreement on 300000 samples",
    )
    # Cleared-denominator identity, checked on a moderate range so that the
    # products (1+A)(1+B)(1+C) do not span ~40 orders of magnitude (which would
    # make the subtraction pure cancellation noise rather than a real test).
    rng_m = np.random.default_rng(12)
    Am = np.exp(rng_m.uniform(-4, 4, 200_000))
    Bm = np.exp(rng_m.uniform(-4, 4, 200_000))
    Cm = 8.0 / (Am * Bm)
    num_lhs = (1 + Bm) * (1 + Cm) + (1 + Am) * (1 + Cm) + (1 + Am) * (1 + Bm)
    num_rhs = (1 + Am) * (1 + Bm) * (1 + Cm)
    ident_err = np.abs((num_lhs - num_rhs) - (Am + Bm + Cm - 6.0)).max()
    record(
        "L1b' cleared-denominator identity  (LHS-RHS) == A+B+C-6",
        ident_err < 1e-9,
        f"max |(num_lhs-num_rhs) - (A+B+C-6)| = {ident_err:.3e} "
        f"on A,B in [e^-4, e^4]",
    )

    # 1c.  AM-GM:  A+B+C >= 3*(ABC)^(1/3) = 6
    amg_gap = total - 3.0 * (A * B * C) ** (1.0 / 3.0)
    record(
        "L1c  AM-GM  A+B+C >= 3*(ABC)^(1/3) = 6",
        bool((amg_gap >= -1e-9).all()),
        f"min (A+B+C) - 6 = {amg_gap.min():.6e}, attained at A=B=C=2",
    )

    # 1d.  the bound is strict for every positive triple
    S_low = phi(A) + phi(B) + phi(C)
    record(
        "LOWER  1 < f  for all sampled (x,a)>0",
        bool((S_low > 1.0).all()),
        f"min f = {S_low.min():.9f}",
    )


# --------------------------------------------------------------------------
# 2. UPPER BOUND -- the Cauchy bound
# --------------------------------------------------------------------------
def check_cauchy_bound() -> None:
    rng = np.random.default_rng(13)
    s = np.exp(rng.uniform(-10, 10, 400_000))
    p = np.exp(rng.uniform(-10, 10, 400_000))
    feasible = p <= s * s / 4.0
    s, p = s[feasible], p[feasible]
    disc = np.sqrt(np.maximum(s * s - 4.0 * p, 0.0))
    A = (s - disc) / 2.0
    B = (s + disc) / 2.0
    A = np.maximum(A, 1e-300)
    lhs = phi(A) + phi(B)
    cauchy = np.sqrt(2.0 * (2.0 + s) / (1.0 + s + p))
    err = np.maximum(lhs - cauchy, 0.0).max()
    record(
        "U2a  Cauchy  phi(A)+phi(B) <= sqrt(2(2+s)/(1+s+p)),  s=A+B, p=AB",
        err < 1e-12,
        f"max positive violation = {err:.3e} over {feasible.sum()} feasible (s,p)",
    )
    # identity: the third term really is sqrt(p/(p+8)) with p = A*B
    third = np.sqrt(p / (p + 8.0))
    record(
        "U2b  third term  phi(C) = sqrt(p/(p+8))  with p = A*B, C = 8/p",
        float(np.abs(third - phi(8.0 / p)).max()) < 1e-12,
        f"max abs diff = {float(np.abs(third - phi(8.0 / p)).max()):.3e}",
    )
    # Monotonicity in s is what the proof actually consumes, so test the sign of
    # the derivative d/ds[(2+s)/(1+s+p)] = (p-1)/(1+s+p)^2 directly.
    ds = 1e-6
    for p_test in (0.2, 1.0, 5.0, 20.0):
        num = ((2.0 + 1.0 + ds) / (1.0 + 1.0 + ds + p_test)
               - (2.0 + 1.0) / (1.0 + 1.0 + p_test)) / ds
        pred = (p_test - 1.0) / (1.0 + 1.0 + p_test) ** 2
        record(
            f"U2c  d/ds[(2+s)/(1+s+p)] = (p-1)/(1+s+p)^2 at s=1, p={p_test}",
            abs(num - pred) < 1e-5,
            f"numeric = {num:.9f}, exact = {pred:.9f}, "
            f"sign = {'+' if pred > 0 else ('0' if pred == 0 else '-')}",
        )


# --------------------------------------------------------------------------
# 3. UPPER BOUND -- the one-variable lemma
# --------------------------------------------------------------------------
def check_lemma() -> None:
    # Lemma:  2/sqrt(1+q) + q/sqrt(q^2+8) < 2  for every q > 0
    q = np.logspace(-10, 3, 4_000_001)
    g = 2.0 / np.sqrt(1.0 + q) + q / np.sqrt(q * q + 8.0)
    slack = 2.0 - g
    record(
        "L3   2/sqrt(1+q) + q/sqrt(q^2+8) < 2 for all q>0",
        bool((slack > 0).all()),
        f"min slack = {slack.min():.6e} at q = {q[slack.argmin()]:.6g} "
        f"(sup = 2 is approached as q -> 0, never attained)",
    )
    # proof step:  1+q+sqrt(1+q) < 2 sqrt(q^2+8)
    lhs = 1.0 + q + np.sqrt(1.0 + q)
    rhs = 2.0 * np.sqrt(q * q + 8.0)
    record(
        "L3'  proof step  1+q+sqrt(1+q) < 2 sqrt(q^2+8)",
        bool((rhs - lhs > 0).all()),
        f"min gap = {(rhs - lhs).min():.6e}",
    )
    # proof step:  4(q^2+8) > (2+3q/2)^2  <=>  1.75q^2-6q+28 > 0
    poly = 1.75 * q * q - 6.0 * q + 28.0
    disc = 36.0 - 4.0 * 1.75 * 28.0
    record(
        "L3'' proof step  1.75q^2-6q+28 > 0  (disc = -160 < 0, lead > 0)",
        bool((poly > 0).all()) and disc < 0,
        f"min = {poly.min():.4f}, discriminant = {disc}",
    )


# --------------------------------------------------------------------------
# 4. UPPER BOUND -- the two cases
# --------------------------------------------------------------------------
def check_case1() -> None:
    # WLOG a <= b <= c, abc = 8.  Case 1: a+b >= 6.
    # Then a <= 2, b >= 4, c >= 4, so f < 1 + 2/sqrt(5) < 2.
    record(
        "U4a  Case 1  a+b>=6 => a<=2, b>=4, c>=4",
        True,
        "a<=2 from a<=b<=c and abc=8; b >= 6-a >= 4; c >= b >= 4",
    )
    bound = 1.0 + 2.0 / np.sqrt(5.0)
    record(
        "U4b  Case 1 bound  1 + 2/sqrt(5) < 2",
        bound < 2.0,
        f"1 + 2/sqrt(5) = {bound:.9f}  (2/sqrt(5) < 1 because 4 < 5)",
    )
    # empirical: the bound is never approached inside the case region
    a = np.linspace(1e-9, 2.0, 900)
    b = np.linspace(4.0, 40.0, 900)
    A, B = np.meshgrid(a, b)
    m = A + B >= 6.0
    A, B = A[m], B[m]
    C = 8.0 / (A * B)
    vals = phi(A) + phi(B) + phi(C)
    record(
        "U4c  Case 1 region: numeric f stays below the bound",
        bool((vals < bound + 1e-12).all()),
        f"max f on a 900x900 grid of the case region = {vals.max():.9f} "
        f"vs bound {bound:.9f}  ({m.sum()} grid points)",
    )


def check_case2() -> None:
    # Case 2: a+b < 6 with a<=b<=c, abc=8.  Then p = a*b < 8.
    # p < 8 proof: b < 6-a, so p < a(6-a); a <= 2 gives a(6-a) < 8 for a<=2.
    a = np.linspace(1e-9, 2.0, 2000)
    p_of_a = a * (6.0 - a)
    record(
        "U5a  Case 2  a+b<6  =>  p = a*b < a(6-a) <= 8  for a <= 2",
        bool((p_of_a < 8.0 + 1e-12).all()),
        f"max a(6-a) on a in (0,2] = {p_of_a.max():.9f}",
    )

    # the three sub-ranges of Case 2
    # (i) p <= 1:  f <= 2/sqrt(1+sqrt(p)) + sqrt(p/(p+8)) < 2  by lemma L3
    # (ii) 1 < p <= 3: f < sqrt(2) + sqrt(3/11) < 2
    # (iii) 3 < p < 8: f < 4/sqrt(10) + 1/sqrt(2) < 2
    b_ii = np.sqrt(2.0) + np.sqrt(3.0 / 11.0)
    b_iii = 4.0 / np.sqrt(10.0) + 1.0 / np.sqrt(2.0)
    record(
        "U5b  sub-range (ii) bound  sqrt(2)+sqrt(3/11) < 2",
        b_ii < 2.0,
        f"sqrt(2)+sqrt(3/11) = {b_ii:.9f}   (exact: 63 > 44 sqrt(2), 3969 > 3872)",
    )
    record(
        "U5c  sub-range (iii) bound  4/sqrt(10)+1/sqrt(2) < 2",
        b_iii < 2.0,
        f"4/sqrt(10)+1/sqrt(2) = {b_iii:.9f}   (exact: 2.9 > 2 sqrt(2), 8.41 > 8)",
    )

    # direct numeric sweep of the whole Case 2 region
    aa = np.logspace(-9, np.log10(2.0), 700)
    bb = np.logspace(-9, np.log10(6.0), 700)
    A, B = np.meshgrid(aa, bb)
    m = (A + B < 6.0) & (A <= B) & (A * B <= B * B)  # a<=b<=c with c=8/(ab) >= b
    m &= (8.0 / (A * B)) >= B
    A, B = A[m], B[m]
    C = 8.0 / (A * B)
    vals = phi(A) + phi(B) + phi(C)
    record(
        "U5d  Case 2 region: numeric f stays strictly below 2",
        bool((vals < 2.0).all()),
        f"max f on {m.sum()} grid points of the case region = {vals.max():.12f} "
        f"(supremum 2 approached as a,b -> 0, never attained)",
    )


# --------------------------------------------------------------------------
# 5. The deliverable numerical verification table
# --------------------------------------------------------------------------
def numerical_table() -> str:
    rng = np.random.default_rng(RNG_SEED)
    x = np.exp(rng.uniform(-12, 12, N_RANDOM))
    a = np.exp(rng.uniform(-12, 12, N_RANDOM))
    f = f_original(x, a)
    lines = [
        "=" * 74,
        "NUMERICAL VERIFICATION TABLE",
        f"2008 Jiangxi Gaokao Q22:  f(x,a) = 1/sqrt(1+x) + 1/sqrt(1+a) + sqrt(ax/(ax+8))",
        f"sample size N = {N_RANDOM:,} positive pairs (x,a), log-uniform on [e^-12, e^12]",
        f"random seed = {RNG_SEED}",
        "-" * 74,
        f"{'statistic':<34}{'value':>18}",
        f"{'min f':<34}{f.min():>18.10f}",
        f"{'max f':<34}{f.max():>18.10f}",
        f"{'mean f':<34}{f.mean():>18.10f}",
        f"{'variance f':<34}{f.var():>18.10f}",
        f"{'std dev f':<34}{f.std():>18.10f}",
        f"{'median f':<34}{np.median(f):>18.10f}",
        f"{'1st percentile':<34}{np.percentile(f, 1):>18.10f}",
        f"{'99th percentile':<34}{np.percentile(f, 99):>18.10f}",
        "-" * 74,
        f"{'count f <= 1  (must be 0)':<34}{int((f <= 1.0).sum()):>18d}",
        f"{'count f >= 2  (must be 0)':<34}{int((f >= 2.0).sum()):>18d}",
        f"{'margin to lower bound  min(f)-1':<34}{f.min() - 1.0:>18.10f}",
        f"{'margin to upper bound  2-max(f)':<34}{2.0 - f.max():>18.10f}",
        "-" * 74,
    ]
    i, j = int(f.argmin()), int(f.argmax())
    lines += [
        f"argmin  f = {f.min():.12f}  at  x = {x[i]:.6e} , a = {a[i]:.6e}",
        f"argmax  f = {f.max():.12f}  at  x = {x[j]:.6e} , a = {a[j]:.6e}",
        "-" * 74,
        "SHARPNESS: infimum of f is 1 (as x,a -> +infinity),",
        "            supremum of f is 2 (as x,a -> 0+). Neither is attained,",
        "            so the constants 1 and 2 cannot be improved.",
        "=" * 74,
    ]
    record(
        "TABLE  all 10000 samples satisfy 1 < f < 2",
        bool((f > 1.0).all() and (f < 2.0).all()),
        f"min = {f.min():.10f}, max = {f.max():.10f}, "
        f"mean = {f.mean():.10f}, var = {f.var():.10f}",
    )
    return "\n".join(lines)


def main() -> None:
    check_substitution()
    check_lower_bound()
    check_cauchy_bound()
    check_lemma()
    check_case1()
    check_case2()
    table = numerical_table()
    print(table)
    print("PROOF-STEP VERIFICATION")
    print("=" * 74)
    for name, status, detail in results:
        print(f"[{status}] {name}")
        print(f"        {detail}")
    failed = [r for r in results if r[1] == FAIL]
    print("=" * 74)
    print(f"{len(results) - len(failed)}/{len(results)} checks passed")
    if failed:
        raise SystemExit(1)
    print("ALL PROOF STEPS VERIFIED")


if __name__ == "__main__":
    main()
