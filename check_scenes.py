"""Exercise the whole movie with frame rasterization stubbed out.

A 2K60 render of twenty-seven sections takes hours, but the expensive part is
rasterizing frames, not evaluating the scene graph. This harness runs every
scene_N method in order with ``play`` and ``wait`` replaced by recorders, so
wrong argument names, bad mobject attributes and broken layout logic surface in
seconds. Each section still calls ``verify_budget``, so the transcript is checked
against the pauses that were actually emitted.

It is a logic smoke test, not a visual one. ``--frames`` additionally rebuilds
every closing picture and asserts that nothing escapes the safe area, which is
the check that catches text running off the edge of the frame.

    python check_scenes.py                 # all 27 sections
    python check_scenes.py S18 S19         # just those
    python check_scenes.py --frames        # only the layout/continuity audit
"""

from __future__ import annotations

import sys
import traceback

from manim import config

config.disable_caching = True
config.write_to_movie = False
config.save_last_frame = False
config.verbosity = "ERROR"
config.pixel_width = 480
config.pixel_height = 270
config.frame_rate = 15

import scene as production  # noqa: E402


def exercise(name: str) -> tuple[bool, str]:
    scene = production.Gaokao22Scene()
    scene.camera.background_color = production.BG
    played: list[str] = []

    def fake_play(*animations, **kwargs):
        for animation in animations:
            played.append(type(animation).__name__)

    scene.play = fake_play
    scene.wait = lambda seconds: None

    try:
        scene.run_section(name)
    except Exception:
        return False, traceback.format_exc(limit=6)

    held = sum(scene._pause_log[0]) if scene._pause_log else 0.0
    detail = (f"{len(played):>3} animations, "
              f"{len(scene._pause_log[0]):>2} beats, "
              f"{held:6.1f}s narration")
    return True, detail


def exercise_playback(name: str) -> tuple[bool, str]:
    """Run the real animation lifecycle without rasterising a single frame.

    The fast gate above replaces ``play`` outright, which means it never reaches
    ``Animation.clean_up_from_scene``. That is precisely where a Transform
    targeting a container mobject blew up, and it is why the fast gate once
    reported ALL SCENES OK for code that could not render. Here ``play`` stays
    real and only ``skip_rendering`` is forced, so ``begin``/``interpolate``/
    ``finish``/``clean_up_from_scene`` all execute and no pixels are produced.
    """
    scene = production.Gaokao22Scene()
    scene.camera.background_color = production.BG
    cls = type(scene)
    real_play = cls.play

    def fast_play(self, *animations, **kwargs):
        kwargs["skip_rendering"] = True
        return real_play(self, *animations, **kwargs)

    scene.play = fast_play.__get__(scene, cls)
    scene.wait = lambda seconds: None

    try:
        scene.run_section(name)
    except Exception:
        return False, traceback.format_exc(limit=8)

    held = sum(scene._pause_log[0]) if scene._pause_log else 0.0
    return True, f"real playback ok, {len(scene._pause_log[0]):>2} beats, {held:6.1f}s"


def audit_frames() -> tuple[bool, str]:
    lines: list[str] = []
    bad = 0
    for index in range(1, production.SECTION_COUNT + 1):
        name = f"S{index}"
        try:
            picture = production.frame_of(name)
        except Exception:
            bad += 1
            lines.append(f"  {name}: FRAME FAILED\n{traceback.format_exc(limit=4)}")
            continue
        over = []
        if picture.get_left()[0] < -production.SAFE_X - 0.02:
            over.append(f"left {picture.get_left()[0]:.2f}")
        if picture.get_right()[0] > production.SAFE_X + 0.02:
            over.append(f"right {picture.get_right()[0]:.2f}")
        if picture.get_top()[1] > production.SAFE_Y + 0.02:
            over.append(f"top {picture.get_top()[1]:.2f}")
        if picture.get_bottom()[1] < -production.SAFE_Y - 0.02:
            over.append(f"bottom {picture.get_bottom()[1]:.2f}")
        if over:
            bad += 1
            lines.append(f"  {name}: OUT OF BOUNDS ({', '.join(over)})")
    if bad:
        return False, "\n".join(lines)
    return True, (f"all {production.SECTION_COUNT} closing pictures fit inside "
                  f"x=±{production.SAFE_X}, y=±{production.SAFE_Y}")


def main() -> int:
    args = sys.argv[1:]
    playback = "--playback" in args
    failures = 0

    ok, detail = audit_frames()
    print(f"{'PASS' if ok else 'FAIL'}  frames  {detail}")
    failures += 0 if ok else 1
    if args == ["--frames"]:
        print()
        print("ALL FRAMES OK" if not failures else "FRAME AUDIT FAILED")
        return 1 if failures else 0

    runner = exercise_playback if playback else exercise
    mode = "playback" if playback else "fast"
    names = [a for a in args if not a.startswith("-")] or [
        f"S{i}" for i in range(1, production.SECTION_COUNT + 1)
    ]
    for raw in names:
        name = raw if raw.startswith("S") else f"S{raw}"
        passed, detail = runner(name)
        print(f"{'PASS' if passed else 'FAIL'}  {name:<4}  [{mode}]  {detail}")
        if not passed:
            failures += 1
            print(detail)
    print()
    print(f"ALL SCENES OK ({mode})" if not failures else f"{failures} FAILURE(S) ({mode})")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
