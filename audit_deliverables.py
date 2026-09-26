"""Audit the deliverables before anyone watches a frame.

Everything here is a hard requirement from the brief, checked mechanically:
the two cuts exist, the plan is long enough, the movie is two-dimensional, the
voiceover script sits at the end of the voiceover file, the transcript is
non-trivial, every section has a closing picture, and the maths verifies.

    python audit_deliverables.py
"""

from __future__ import annotations

import ast
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

VO_FILE = ROOT / "scene.py"
NOVO_FILE = ROOT / "scene_no_vo.py"
PLAN = ROOT / "plan.md"
FORBIDDEN_3D = ("ThreeDScene", "ThreeDAxes", "Surface", "ThreeDVMobject")

results: list[tuple[bool, str, str]] = []


def check(ok: bool, label: str, detail: str) -> None:
    results.append((ok, label, detail))


def main() -> int:
    import scene as production

    check(VO_FILE.exists(), "voiceover file exists", VO_FILE.name)
    check(NOVO_FILE.exists(), "no-voiceover file exists", NOVO_FILE.name)

    src = VO_FILE.read_text(encoding="utf-8")
    tree = ast.parse(src)

    offenders = [name for name in FORBIDDEN_3D if name in src]
    check(not offenders, "2D only", f"no 3D constructs found" if not offenders
          else f"found {offenders}")

    methods = sorted(n.name for n in ast.walk(tree)
                     if isinstance(n, ast.FunctionDef) and n.name.startswith("scene_"))
    check(len(methods) == production.SECTION_COUNT,
          "one method per section",
          f"{len(methods)} scene_* methods for {production.SECTION_COUNT} sections")

    check(all(f"S{i}" in production.FRAME_BUILDERS
              for i in range(1, production.SECTION_COUNT + 1)),
          "every section has a closing picture",
          f"{len(production.FRAME_BUILDERS)} frame builders")

    beats = sum(len(v) for v in production.NARRATION.values())
    check(beats >= 100, "transcript is substantial",
          f"{beats} lines, {production.TOTAL_NARRATION:.0f}s of narration")

    total_lines = len(src.splitlines())
    definition_line = next(
        (n for n, line in enumerate(src.splitlines(), 1)
         if line.startswith("VOICEOVER_SCRIPT = build_voiceover_script")),
        0,
    )
    check(definition_line > total_lines * 0.9 and len(production.VOICEOVER_SCRIPT) > 5000,
          "voiceover script is at the end of the file",
          f"defined at line {definition_line}/{total_lines}, "
          f"generates {len(production.VOICEOVER_SCRIPT)} chars")

    plan_lines = len(PLAN.read_text(encoding="utf-8").splitlines()) if PLAN.exists() else 0
    check(plan_lines >= 500, "plan.md is at least 500 lines", f"{plan_lines} lines")

    plan_text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    check("gaokao" in plan_text.lower() or "jiangxi" in plan_text.lower(),
          "plan.md documents this problem",
          "mentions the Jiangxi problem" if plan_text else "plan.md missing")

    check(production.STATS["below"] == 0 and production.STATS["above"] == 0,
          "sampled f never leaves (1, 2)",
          f"{production.STATS['below']} at or below 1, "
          f"{production.STATS['above']} at or above 2")

    width = max(len(label) for _, label, _ in results)
    failed = 0
    for ok, label, detail in results:
        if not ok:
            failed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {label:<{width}}  {detail}")

    print()
    proc = subprocess.run([sys.executable, str(ROOT / "verification" / "verify_math.py")],
                          capture_output=True, text=True, cwd=ROOT)
    tail_line = [ln for ln in proc.stdout.splitlines() if "checks passed" in ln]
    check(proc.returncode == 0, "proof verifies numerically",
          tail_line[-1] if tail_line else proc.stderr.strip()[-120:])
    ok, label, detail = results[-1]
    print(f"[{'PASS' if ok else 'FAIL'}] {label:<{width}}  {detail}")

    total, bad = len(results), sum(1 for ok, _, _ in results if not ok)
    print()
    print(f"{total - bad}/{total} deliverable checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
