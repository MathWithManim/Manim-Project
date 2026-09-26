"""Visual-only build of the Hopf fibration movie.

Same geometry, same timing, same nine sections as ``scene.py`` -- but with the
narration pauses removed, so the render is a clean silent cut for people who
want to voice it themselves (or drop their own music under it).

    manim render scene_no_vo.py HopfFibrationVisual

How this works
--------------
``HopfFibrationVisual`` wraps ``HopfFibrationScene`` and intercepts ``pause``.
Every visual beat in the parent class is followed by ``self.pause(X)``; here
``pause`` sleeps for ``X / SPEED`` instead of ``X``. SPEED = 1.0 reproduces the
15-minute cut exactly. SPEED = 1.5 gives a 9:26 cut that is noticeably brisker
and is the default for this file, because silent footage read at 14 minutes
per minute of geometry feels slow when there is no voice carrying it.

Set the speed from the environment so you do not have to edit the file:
    set HOPF_SPEED=1.0 && manim render scene_no_vo.py HopfFibrationVisual
"""

from __future__ import annotations

import os

from scene import HopfFibrationScene

SPEED = float(os.environ.get("HOPF_SPEED", "1.5"))


class HopfFibrationVisual(HopfFibrationScene):
    """The full movie with narration pauses compressed by ``SPEED``."""

    def pause(self, seconds: float) -> None:
        self.wait(seconds / SPEED)
        self._pause_log[-1].append(round(float(seconds), 3))
