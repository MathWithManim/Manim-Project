"""Audit the five production deliverables against the original spec.

Each check re-derives its answer from the file on disk rather than trusting the
build log, so a stale todo cannot be marked done on the strength of an old
claim. Exits non-zero if any check fails.
"""

from __future__ import annotations

import ast
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        FAILURES.append(label)


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------- deliverable 1
print("1. plan.md — Stage 1 draft + Stage 2 audit + final revised plan")
plan = read("plan.md")
for stage in ("# STAGE 1", "# STAGE 2", "# STAGE 3"):
    check(f"contains {stage}", stage in plan)
check("has VO transcript section", "VOICEOVER TRANSCRIPT" in plan)
check("has budget verification table", "Budget verification" in plan)
check("documents HUD architecture", "add_fixed_in_frame_mobjects" in plan)
check("states the 15:00 cap", "15:00" in plan)


def to_seconds(stamp: str) -> int:
    minutes, _, seconds = stamp.partition(":")
    return int(minutes) * 60 + int(seconds)


# Every "## Sn ... H:MM-H:MM" header, in file order: Stage 3 block then transcript.
headers = re.findall(r"^## (S\d)\b.*?(\d{1,2}:\d{2})\D(\d{1,2}:\d{2})", plan, re.M)
check("18 timestamped headers (9 in Stage 3 + 9 in transcript)", len(headers) == 18,
      f"{len(headers)} found")

if len(headers) == 18:
    stage3, transcript = headers[:9], headers[9:]
    check("Stage 3 and transcript agree on every window",
          [(s, a, b) for s, a, b in stage3] == [(s, a, b) for s, a, b in transcript])
    check("scene order is S1..S9", [s for s, _, _ in stage3] == [f"S{i}" for i in range(1, 10)])
    contiguous = all(stage3[i][2] == stage3[i + 1][1] for i in range(8))
    check("timeline is contiguous (no gaps or overlaps)", contiguous,
          " -> ".join(f"{a}-{b}" for _, a, b in stage3))
    check("timeline ends at 14:09 (849 s)", to_seconds(stage3[-1][2]) == 849,
          stage3[-1][2])
    check("timeline starts at 0:00", to_seconds(stage3[0][1]) == 0, stage3[0][1])

# ---------------------------------------------------------------- deliverable 2
print("\n2. manim.cfg — 2K60 CLI config")
cfg = read("manim.cfg")
for key, want in (
    ("pixel_width", "2560"),
    ("pixel_height", "1440"),
    ("frame_rate", "60"),
):
    m = re.search(rf"^{key}\s*=\s*(\S+)", cfg, re.M)
    check(f"{key} = {want}", bool(m) and m.group(1) == want, m.group(1) if m else "missing")
bg = re.search(r"^background_color\s*=\s*(\S+)", cfg, re.M)
check("dark background", bool(bg) and bg.group(1).upper() == "#0B0E14",
      bg.group(1) if bg else "missing")
check("[CLI] section present", "[CLI]" in cfg)

# ---------------------------------------------------------------- deliverable 3
print("\n3. scene.py — modular ThreeDScene, 9 scenes, waits match pauses, VO at bottom")
src = read("scene.py")
tree = ast.parse(src)
classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
check("class HopfFibrationScene exists", "HopfFibrationScene" in classes)
check("inherits ThreeDScene",
      bool(classes.get("HopfFibrationScene")
           and any(isinstance(b, ast.Name) and b.id == "ThreeDScene"
                   for b in classes["HopfFibrationScene"].bases)))
cls = classes.get("HopfFibrationScene")
methods = [f.name for f in cls.body if isinstance(f, ast.FunctionDef)] if cls else []
scene_methods = sorted(m for m in methods if re.fullmatch(r"scene_[1-9]", m))
check("9 modular scene methods", len(scene_methods) == 9, ", ".join(scene_methods))

budget_node = next((n for n in tree.body
                    if isinstance(n, ast.AnnAssign) and getattr(n.target, "id", "") == "SCENE_BUDGET"), None)
ns: dict = {}
exec(compile(ast.Module(body=[budget_node], type_ignores=[]), "<b>", "exec"), ns)
budget = ns["SCENE_BUDGET"]
check("SCENE_BUDGET has 9 entries", len(budget) == 9)
total = sum(d for d, _, _ in budget.values())
check("total runtime is 849 s", abs(total - 849.0) < 1e-6, f"{total} s")

# every self.pause(X) in each scene must equal that scene's scripted waits
for fn in cls.body:
    if not (isinstance(fn, ast.FunctionDef) and re.fullmatch(r"scene_[1-9]", fn.name)):
        continue
    name = "S" + fn.name.split("_")[1]
    logged = [round(float(ast.literal_eval(n.args[0])), 3)
              for n in ast.walk(fn)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr == "pause" and n.args]
    check(f"{name} pauses match script", logged == budget[name][2],
          f"{len(logged)} pauses")

check("VOICEOVER_SCRIPT present", "VOICEOVER_SCRIPT" in src)
last = tree.body[-1]
check("VO script is the final top-level statement",
      isinstance(last, ast.Assign) and getattr(last.targets[0], "id", "") == "VOICEOVER_SCRIPT",
      type(last).__name__)

# no unused imports (what a type checker would flag)
imported: dict[str, int] = {}
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom):
        for a in node.names:
            imported[a.asname or a.name] = imported.get(a.asname or a.name, 0)
    elif isinstance(node, ast.Import):
        for a in node.names:
            imported[(a.asname or a.name).split(".")[0]] = imported.get((a.asname or a.name).split(".")[0], 0)
used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
used |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
for node in ast.walk(tree):
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        used.add(node.value.id)
unused = sorted(k for k in imported if k not in used and k != "annotations")
check("no unused imports", not unused, ", ".join(unused) if unused else "clean")

# ---------------------------------------------------------------- deliverable 4
print("\n4. render.yml — matrix section render + ffmpeg concat")
try:
    import yaml
    wf = yaml.safe_load(read(".github/workflows/render.yml"))
except ImportError:
    wf = None
    check("pyyaml available for workflow check", False, "pip install pyyaml")
if wf:
    jobs = wf["jobs"]
    check("has a render matrix job", "render" in jobs
          and jobs["render"]["strategy"]["matrix"]["i"] == [1, 2, 3, 4, 5, 6, 7, 8, 9])
    check("assemble job needs render", jobs["assemble"]["needs"] == "render")
    blob = json.dumps(wf) if (json := __import__("json")) else ""
    check("uses ffmpeg concat", "concat" in blob and "-c copy" in blob)
    check("assembles in numeric scene order", "seq 1 9" in blob)
    check("trigger covers master", "master" in (wf.get(True) or wf.get("on"))["push"]["branches"])

# ---------------------------------------------------------------- deliverable 5
print("\n5. Verify — compile + runtime validation of all nine scenes")
py = ["scene.py", "scene_no_vo.py", "build_narration.py", "check_scenes.py"]
r = subprocess.run([sys.executable, "-m", "py_compile", *py], capture_output=True, text=True)
check("py_compile exit 0", r.returncode == 0, r.stderr.strip()[:200])

r = subprocess.run([sys.executable, "check_scenes.py"], capture_output=True, text=True, cwd=ROOT)
check("all 9 scenes pass runtime check", r.returncode == 0 and "ALL SCENES OK" in r.stdout,
      r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:200])

r = subprocess.run([sys.executable, "build_narration.py"], capture_output=True, text=True, cwd=ROOT)
check("narration regenerates from code", r.returncode == 0, r.stderr.strip()[:200])

r = subprocess.run(["git", "diff", "--exit-code", "--", "narration.txt"],
                   capture_output=True, text=True, cwd=ROOT)
check("narration.txt in sync with code (what CI gates on)", r.returncode == 0)

print("\n" + "=" * 62)
if FAILURES:
    print(f"{len(FAILURES)} CHECK(S) FAILED:")
    for f in FAILURES:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASS — every deliverable verified from disk")
