"""The no-voiceover cut: identical visuals, narration burned onto the screen.

    manim render scene_no_vo.py Gaokao22Scene
    GAOKAO_ONLY=S18 manim render scene_no_vo.py Gaokao22Scene

Setting GAOKAO_CAPTIONS=1 makes Gaokao22Scene.say paint each transcript line into
the caption zone for exactly as long as the voiceover version holds on it, so the
two renders are frame-for-frame synchronised from one source of truth.
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
os.environ["GAOKAO_CAPTIONS"] = "1"

import scene as production  # noqa: E402

assert production.CAPTIONS, "caption mode failed to engage"


class Gaokao22Scene(production.Gaokao22Scene):
    """The captioned cut. Same class, captions instead of a voice track."""
