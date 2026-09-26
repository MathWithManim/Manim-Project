"""Run the whole movie's logic with frame rendering stubbed out.

A full 2K60 render of nine scenes takes hours, but the expensive part is
rasterizing frames, not evaluating the scene graph. This harness executes every
self.play(...) and self.pause(...) call in order, with the renderer disabled, so
wrong argument names, bad mobject attributes, and missing state surface in
seconds. It is a logic smoke test, not a visual one -- for that, render frames.

    python check_scenes.py            # all nine scenes
    python check_scenes.py S8 S9      # just those
"""

from __future__ import annotations

import sys
import traceback

from manim import config

config.disable_caching = True
config.write_to_movie = False
config.save_last_frame = False
config.verbosity = "ERROR"
config.frame_width = 480
config.frame_height = 270
config.frame_rate = 15

import scene as production  # noqa: E402


def exercise(name: str) -> tuple[bool, str]:
    scene = production.HopfFibrationScene()
    scene._pause_log = []
    scene.camera.background_color = "#0B0E14"

    played: list[str] = []

    def fake_play(*animations, **kwargs):
        for animation in animations:
            played.append(type(animation).__name__)

    scene.play = fake_play
    scene.wait = lambda seconds: None
    scene.add_fixed_in_frame_mobjects = lambda *mobs: scene.add(*mobs)

    try:
        scene.run_section(name)
    except Exception:
        return False, traceback.format_exc(limit=6)

    plays = len(played)
    logged = scene._pause_log[0]
    expected_plays, expected_pauses = production.SCENE_BUDGET[name][1], production.SCENE_BUDGET[name][2]
    detail = (
        f"{plays} animations, {len(logged)} pauses, "
        f"timeline {expected_plays + sum(logged):.1f} s"
    )
    return True, detail


def main() -> int:
    names = sys.argv[1:] or [f"S{i}" for i in range(1, 10)]
    failures = 0
    for name in names:
        if not name.startswith("S"):
            name = f"S{name}"
        passed, detail = exercise(name)
        if passed:
            print(f"PASS  {name}  {detail}")
        else:
            failures += 1
            print(f"FAIL  {name}\n{detail}")
    print()
    print("ALL SCENES OK" if not failures else f"{failures} SCENE(S) FAILED")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
