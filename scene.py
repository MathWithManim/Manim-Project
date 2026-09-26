"""THE HOPF FIBRATION -- 15-minute Manim CE production scene.

Deliverable 3 of 4. Render with:
    manim render scene.py HopfFibrationScene

Conventions enforced by this module
-----------------------------------
* one class, nine ``next_section`` markers -> CI renders S1..S9 independently
* every ``self.pause(x)`` is exactly one narration pause; ``SCENE_BUDGET`` locks
  the per-scene animation total and the ordered wait list, and ``construct``
  asserts both, so the plan and the movie cannot drift apart
* total runtime is asserted to 900 s (15:00)
* fonts are capped by the header / formula / note helpers (36 / 28 / 20)
* HUD elements go through ``carded`` -> translucent card, fixed in frame
* 3D geometry stays inside the radius-2.6 ball; see ``SAFE_THETA_MAX``
"""

from __future__ import annotations

import os

import numpy as np
from manim import (
    DEGREES,
    PI,
    TAU,
    WHITE,
    BackgroundRectangle,
    Circle,
    Create,
    Dot,
    Dot3D,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Line3D,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Sphere,
    Text,
    ThreeDScene,
    Torus,
    Transform,
    VGroup,
    ValueTracker,
    VMobject,
    always_redraw,
)

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
CYAN = "#5AC8FA"
GOLD = "#FFD166"
CORAL = "#FF6B6B"
SKY = "#4DABF7"
MINT = "#4CD97B"
LILAC = "#C792EA"
ROSE = "#F78C6C"
DIM = "#9DA7B3"

# Pinned so local renders and CI renders match. CI installs fonts-dejavu-core.
# Windows usually lacks it, so override per machine instead of editing code:
#   set HOPF_FONT=Arial
# Pango falls back rather than failing if the font is missing, but the warning
# it prints ("expect ugly") means the local preview no longer matches CI.
FONT = os.environ.get("HOPF_FONT", "DejaVu Sans")

# --------------------------------------------------------------------------
# mathematics
# --------------------------------------------------------------------------
# stereographic image (1 - x4)^-1 * (x1, x2, x3) of the Hopf fiber over
# (theta, phi) in S^2;  t parameterises the fiber, 0 <= t < TAU.
#
# radius bound: max |X| = (1 + sin(theta/2)) / cos(theta/2)
#                         = tan(pi/4 + theta/4) <= 2.6
#                         <=> theta <= 1.669 rad
SAFE_THETA_MAX = 1.6

GROUND_Y = -1.9
SPHERE_R = 0.45
PLANE_Z = -1.05
POLE_TO_PLANE = SPHERE_R - PLANE_Z  # 1.5

# Tessellation. Cairo shades per face, so low resolution reads as visible
# triangles on curved surfaces; Manim's own default is 32, which is not enough
# for shapes this large on screen. (u, v) = steps around the ring, then around
# the tube. Raise these for still smoother surfaces, at a linear render cost.
TORUS_RESOLUTION = (120, 60)
SPHERE_RESOLUTION = (56, 36)
SPHERE_RESOLUTION_SMALL = (36, 24)

# scene name -> (duration, animation total, ordered narration waits)
SCENE_BUDGET: dict[str, tuple[float, float, list[float]]] = {
    "S1": (50.0, 19.0, [3.0, 3.0, 2.0, 3.0, 10.0, 4.0, 6.0]),
    "S2": (92.0, 20.0, [3.0, 3.0, 7.0, 6.0, 6.0, 7.0, 7.0, 6.0, 7.0, 7.0, 6.0, 7.0]),
    "S3": (119.0, 23.0, [4.0, 7.0, 7.0, 7.0, 7.0, 7.0, 8.0, 9.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0]),
    "S4": (97.5, 15.0, [5.0, 6.0, 7.0, 7.0, 7.0, 8.0, 7.0, 8.0, 7.0, 6.0, 6.0, 4.0, 4.5]),
    "S5": (109.0, 19.0, [4.0, 5.0, 7.0, 7.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 3.0]),
    "S6": (133.5, 16.0, [4.0, 5.0, 7.0, 8.0, 8.0, 9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 7.0, 6.0, 6.0, 5.5, 8.0]),
    "S7": (115.5, 20.0, [4.0, 5.0, 8.0, 9.0, 10.0, 10.0, 9.0, 9.0, 8.0, 7.0, 6.0, 5.0, 5.5]),
    "S8": (64.0, 10.0, [4.0, 6.0, 30.0, 14.0]),
    "S9": (68.5, 10.0, [4.0, 5.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 5.0, 4.5]),
}
TOTAL_RUNTIME = sum(duration for duration, _, _ in SCENE_BUDGET.values())


def hopf_point(t: float, theta: float, phi: float) -> np.ndarray:
    """Point of the stereographic shadow of the Hopf fiber over (theta, phi)."""
    half = theta / 2.0
    cos_half = np.cos(half)
    sin_half = np.sin(half)
    denominator = 1.0 - sin_half * np.sin(t + phi)
    return np.array(
        [
            cos_half * np.cos(t) / denominator,
            cos_half * np.sin(t) / denominator,
            sin_half * np.cos(t + phi) / denominator,
        ]
    )


def make_fiber(theta: float, phi: float, color: str, samples: int = 180) -> VMobject:
    """Closed 3D circle: the stereographic image of one Hopf fiber."""
    points = [hopf_point(TAU * i / samples, theta, phi) for i in range(samples + 1)]
    fiber = VMobject()
    fiber.set_points_smoothly(points)
    fiber.set_stroke(color, width=3.0)
    fiber.set_fill(opacity=0.0)
    fiber.set_shade_in_3d(True)
    return fiber


def torus_pair(theta: float) -> tuple[float, float]:
    """(major, minor) radii of the Clifford torus that carries latitude theta."""
    half = theta / 2.0
    return float(1.0 / np.cos(half)), float(np.tan(half))


def torus_bundle(theta: float, color: str) -> tuple[Torus, VGroup]:
    """Clifford torus at latitude theta plus eight fibers woven over it."""
    major, minor = torus_pair(theta)
    shell = Torus(
        major_radius=major, minor_radius=minor, resolution=TORUS_RESOLUTION
    )
    shell.set_fill(color, opacity=0.12)
    shell.set_stroke(color, 2.4)
    shell.set_shade_in_3d(True)
    fibers = VGroup(
        *[make_fiber(theta, TAU * k / 8 + 0.2, color, samples=120) for k in range(8)]
    )
    return shell, fibers


def shadow_radius(alpha_deg: float) -> float:
    """Radius of the stereographic shadow of latitude alpha (degrees)."""
    alpha = np.deg2rad(alpha_deg)
    return POLE_TO_PLANE * float(np.cos(alpha / 2) / np.sin(alpha / 2))


class HopfFibrationScene(ThreeDScene):
    """S^3 -> S^2 as linked circles, in nine sections."""

    # ------------------------------------------------------------------
    # plumbing
    # ------------------------------------------------------------------
    def pause(self, seconds: float) -> None:
        """A narration pause; recorded so the budget assertion can check it."""
        self.wait(seconds)
        self._pause_log[-1].append(round(float(seconds), 3))

    def fade_all(self, run_time: float) -> None:
        """Clear the stage between sections."""
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=run_time)

    def carded(self, mob, at):
        """Wrap mob in a translucent HUD card pinned to the frame."""
        mob.move_to(at)
        card = BackgroundRectangle(mob, fill_opacity=0.7, buff=0.14)
        group = VGroup(card, mob)
        self.add_fixed_in_frame_mobjects(group)
        return group

    def header(self, text: str) -> Text:
        return Text(text, font_size=36, color=WHITE, font=FONT).scale(0.70)

    def formula(self, tex: str) -> MathTex:
        return MathTex(tex, font_size=28, color=WHITE).scale(0.50)

    def note(self, text: str) -> Text:
        return Text(text, font_size=20, color=DIM, font=FONT).scale(0.38)

    def construct(self) -> None:
        self._pause_log: list[list[float]] = []
        self.camera.background_color = "#0B0E14"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-52 * DEGREES, zoom=1.6)

        only = os.environ.get("HOPF_ONLY")
        if only:
            self.run_section(only.strip().upper())
            return

        for index in range(1, len(SCENE_BUDGET) + 1):
            self.next_section(f"S{index}")
            getattr(self, f"scene_{index}")()

        self.verify_budget()

    def run_section(self, name: str) -> None:
        """Render one scene in isolation. Used by CI and by HOPF_ONLY=... .

        Manim's ``-n`` flag takes animation indices, not section names, so
        chunked rendering goes through this instead. Every scene is written to
        stand on its own, so S8 rebuilds the structure rather than inheriting
        it from S7.
        """
        if not name.startswith("S"):
            name = f"S{name}"
        if name not in SCENE_BUDGET:
            raise SystemExit(f"unknown scene {name!r}; expected S1..S9")
        self.next_section(name)
        getattr(self, f"scene_{name[1:]}")()
        self.verify_budget(names=[name])

    def verify_budget(self, names: list[str] | None = None) -> None:
        """Fail loudly if the movie no longer matches the narration script."""
        selected = list(SCENE_BUDGET) if names is None else names
        if len(self._pause_log) != len(selected):
            raise AssertionError(
                f"ran {len(self._pause_log)} scenes, expected {len(selected)}"
            )
        for name, logged in zip(selected, self._pause_log):
            duration, animation, waits = SCENE_BUDGET[name]
            if logged != waits:
                raise AssertionError(f"{name}: pauses {logged} != script {waits}")
            if abs(animation + sum(waits) - duration) > 1e-6:
                raise AssertionError(f"{name}: duration drift")

    # ------------------------------------------------------------------
    # S1 -- cold open
    # ------------------------------------------------------------------
    def scene_1(self) -> None:
        self._pause_log.append([])

        title = Text(
            "THE HOPF FIBRATION", font_size=36, color=WHITE, font=FONT
        ).to_edge(__import__("manim").UP, buff=2.0)
        subtitle = Text(
            "every circle linked to every other",
            font_size=28,
            color=DIM,
            font=FONT,
        ).next_to(title, __import__("manim").DOWN, buff=0.5)
        opener = VGroup(title, subtitle)
        self.play(FadeIn(opener), run_time=2.0)
        self.pause(3.0)
        self.play(FadeOut(opener), run_time=1.0)
        self.pause(3.0)

        palette = [CYAN, CORAL, SKY, MINT, GOLD, LILAC]
        cluster = [make_fiber(1.0, TAU * k / 6 + 0.35, color) for k, color in enumerate(palette)]
        self.play(Create(cluster[0]), run_time=3.0)
        self.pause(2.0)
        self.play(Create(VGroup(cluster[1], cluster[2])), run_time=5.0)
        self.pause(3.0)
        self.play(Create(VGroup(cluster[3], cluster[4], cluster[5])), run_time=6.0)

        self.begin_ambient_camera_rotation(rate=0.10, about="phi")
        self.pause(10.0)

        caption = self.carded(
            self.note("no two touch  ·  every pair linked"),
            __import__("manim").DOWN * 3.0,
        )
        self.play(FadeIn(caption), run_time=1.0)
        self.pause(4.0)
        self.play(FadeOut(caption), run_time=1.0)
        self.pause(6.0)
        self.stop_ambient_camera_rotation()

    # ------------------------------------------------------------------
    # S2 -- the spheres
    # ------------------------------------------------------------------
    def scene_2(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN

        self.fade_all(1.0)
        self.pause(3.0)

        header = self.carded(self.header("1 · THE SPHERES"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(3.0)

        ring = Circle(radius=1.5, color=CYAN, stroke_width=4)
        self.play(Create(ring), run_time=2.0)
        label_one = self.carded(self.formula("S^{1}"), down * 3.0)
        self.play(FadeIn(label_one), run_time=1.0)
        self.pause(7.0)

        shell = Sphere(radius=1.5, resolution=SPHERE_RESOLUTION)
        shell.set_fill(CYAN, opacity=0.08)
        shell.set_stroke(CYAN, 1.6)
        shell.set_shade_in_3d(True)
        self.play(ReplacementTransform(ring, shell), run_time=1.5)
        self.pause(6.0)

        label_two = self.carded(self.formula("S^{2}"), down * 3.0)
        self.play(FadeIn(label_two), run_time=1.0)

        equation = self.carded(
            self.formula(r"|z_1|^2 + |z_2|^2 = 1"), up * 2.3
        )
        self.play(FadeIn(equation), run_time=1.5)
        self.pause(6.0)

        rings = VGroup(
            *[
                Circle(radius=0.9 + 0.25 * k, color=SKY, stroke_width=1.2)
                for k in range(4)
            ]
        )
        self.play(
            LaggedStart(*[Create(ring) for ring in rings], lag_ratio=0.15),
            run_time=4.0,
        )
        self.pause(7.0)

        self.play(Indicate(equation, color=GOLD), run_time=2.0)
        self.pause(7.0)

        self.play(FadeOut(VGroup(shell, rings)), run_time=1.0)
        self.pause(6.0)

        header_two = self.carded(self.header("WHY S^3?"), up * 3.1)
        self.play(FadeIn(header_two), run_time=1.0)
        self.pause(7.0)

        coordinates = self.carded(
            self.formula(r"(x_1,\,x_2,\,x_3,\,x_4)\in\mathbb{R}^4"), up * 2.3
        )
        self.play(FadeIn(coordinates), run_time=1.0)
        self.pause(7.0)

        annotation = self.carded(
            self.note("four numbers, one constraint"), down * 3.0
        )
        self.play(FadeIn(annotation), run_time=2.0)
        self.pause(6.0)

        self.play(FadeOut(VGroup(header_two, coordinates, annotation)), run_time=1.0)
        self.pause(7.0)

    # ------------------------------------------------------------------
    # S3 -- stereographic projection
    # ------------------------------------------------------------------
    def scene_3(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN
        left = __import__("manim").LEFT

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("2 · STEREOGRAPHIC PROJECTION"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(7.0)

        # -- 2D warm-up, pinned left, flat by design -------------------
        center = left * 4.2 + up * 0.2
        circle_2d = Circle(radius=1.6, color=CYAN, stroke_width=3).move_to(center)
        pole = Dot(circle_2d.get_top(), radius=0.09, color=GOLD)
        ground = Line(
            left * 7.0 + down * 1.9, left * 1.4 + down * 1.9, color=DIM
        )
        sweep = ValueTracker(0.0)

        def target() -> np.ndarray:
            return circle_2d.point_at_angle(-PI / 2 + sweep.get_value() * PI * 0.999)

        def projected() -> np.ndarray:
            aim = target()
            origin = pole.get_center()
            vertical = aim[1] - origin[1]
            if abs(vertical) < 1e-6:
                return np.array([origin[0], GROUND_Y, 0.0])
            factor = (GROUND_Y - origin[1]) / vertical
            landing = origin + factor * (aim - origin)
            return np.array(
                [float(np.clip(landing[0], -6.9, -1.2)), GROUND_Y, 0.0]
            )

        runner = always_redraw(lambda: Dot(target(), radius=0.07, color=SKY))
        ray = always_redraw(
            lambda: Line(pole.get_center(), projected(), color=GOLD, stroke_width=2)
        )
        shadow = always_redraw(lambda: Dot(projected(), radius=0.09, color=MINT))

        self.play(
            FadeIn(circle_2d),
            FadeIn(pole),
            Create(ground),
            FadeIn(runner),
            FadeIn(ray),
            FadeIn(shadow),
            run_time=3.0,
        )
        self.pause(7.0)

        self.play(sweep.animate.set_value(1.0), run_time=3.0)
        self.pause(7.0)

        pole_note = self.carded(
            self.note("the north pole is the point at infinity"), down * 3.0
        )
        self.play(FadeIn(pole_note), run_time=1.5)
        self.pause(7.0)

        self.play(
            FadeOut(VGroup(circle_2d, pole, ground, runner, ray, shadow)),
            run_time=1.0,
        )
        self.pause(7.0)

        # -- the real thing, in 3D ------------------------------------
        globe = Sphere(radius=SPHERE_R, resolution=SPHERE_RESOLUTION)
        globe.set_fill(CYAN, opacity=0.10)
        globe.set_stroke(CYAN, 1.4)
        globe.set_shade_in_3d(True)
        north = Dot3D(point=np.array([0.0, 0.0, SPHERE_R]), color=GOLD, radius=0.05)
        table = Rectangle(width=4.0, height=4.0, stroke_width=1.2)
        table.set_fill(DIM, opacity=0.04)
        table.set_stroke(DIM, 1.2)
        table.move_to(np.array([0.0, 0.0, PLANE_Z]))
        table.set_shade_in_3d(True)

        def latitude(alpha_deg: float, color: str) -> Circle:
            alpha = np.deg2rad(alpha_deg)
            ring = Circle(
                radius=SPHERE_R * float(np.sin(alpha)), color=color, stroke_width=2.0
            )
            ring.move_to(np.array([0.0, 0.0, SPHERE_R * float(np.cos(alpha))]))
            ring.set_shade_in_3d(True)
            return ring

        def shadow_circle(alpha_deg: float, color: str) -> Circle:
            disc = Circle(radius=shadow_radius(alpha_deg), color=color, stroke_width=2.0)
            disc.move_to(np.array([0.0, 0.0, PLANE_Z]))
            disc.set_shade_in_3d(True)
            return disc

        self.play(Create(globe), FadeIn(north), Create(table), run_time=2.0)
        self.pause(8.0)

        lat_a = latitude(120, SKY)
        self.play(Create(lat_a), run_time=1.5)
        self.pause(9.0)

        shadow_a = shadow_circle(120, MINT)
        self.play(Create(shadow_a), run_time=1.5)
        self.pause(7.0)

        lat_b = latitude(110, SKY)
        shadow_b = shadow_circle(110, MINT)
        self.play(Create(lat_b), Create(shadow_b), run_time=2.5)
        self.pause(7.0)

        lat_c = latitude(90, GOLD)
        shadow_c = shadow_circle(90, MINT)
        self.play(Create(lat_c), Create(shadow_c), run_time=2.5)
        self.pause(7.0)

        self.play(
            Indicate(shadow_c, color=MINT),
            FadeIn(self.carded(self.note("a circle stays a circle"), down * 3.0)),
            run_time=1.0,
        )
        self.pause(7.0)

        self.play(
            FadeIn(
                self.carded(
                    self.note("closer to the pole, bigger shadow"), down * 2.4
                )
            ),
            run_time=1.0,
        )
        self.pause(6.0)

        self.play(
            FadeOut(
                VGroup(
                    globe,
                    north,
                    table,
                    lat_a,
                    shadow_a,
                    lat_b,
                    shadow_b,
                    lat_c,
                    shadow_c,
                    header,
                )
            ),
            run_time=1.5,
        )
        self.pause(6.0)

    # ------------------------------------------------------------------
    # S4 -- one dimension up
    # ------------------------------------------------------------------
    def scene_4(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN
        right = __import__("manim").RIGHT

        self.fade_all(1.0)
        self.pause(5.0)

        header = self.carded(self.header("3 · ONE DIMENSION UP"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(6.0)

        ambient = Circle(radius=1.6, color=SKY, stroke_width=2.5)
        ambient.set_shade_in_3d(True)
        pole = Dot3D(point=ambient.get_top(), color=GOLD, radius=0.05)
        self.play(Create(ambient), FadeIn(pole), run_time=1.0)
        self.pause(7.0)

        label = self.carded(self.formula(r"S^3 \simeq \mathbb{R}^4"), up * 2.3)
        self.play(FadeIn(label), run_time=1.0)
        self.pause(7.0)

        equator = Circle(radius=1.4, color=SKY, stroke_width=2.5)
        equator.set_shade_in_3d(True)
        self.play(Create(equator), run_time=2.0)
        self.pause(7.0)

        rider = Dot3D(point=equator.point_at_angle(0), color=GOLD, radius=0.06)
        self.play(FadeIn(rider), run_time=2.0)
        self.pause(8.0)

        shadow = Circle(radius=1.0, color=MINT, stroke_width=2.5)
        shadow.set_shade_in_3d(True)
        self.play(Create(shadow), run_time=1.5)
        self.pause(7.0)

        self.play(Indicate(VGroup(equator, shadow), color=WHITE), run_time=1.0)
        self.pause(8.0)

        tilted = Circle(radius=1.2, color=CORAL, stroke_width=2.5)
        tilted.rotate(PI / 4, axis=right)
        tilted.set_shade_in_3d(True)
        self.play(Create(tilted), run_time=1.5)
        self.pause(7.0)

        tilted_shadow = Circle(radius=0.9, color=ROSE, stroke_width=2.5)
        tilted_shadow.rotate(PI / 4, axis=right)
        tilted_shadow.set_shade_in_3d(True)
        self.play(Create(tilted_shadow), run_time=1.5)
        self.pause(6.0)

        caption = self.carded(
            self.note("the equator of S^3 is this circle in space"), down * 3.0
        )
        self.play(FadeIn(caption), run_time=1.5)
        self.pause(6.0)

        self.play(FadeOut(VGroup(tilted, tilted_shadow)), run_time=0.5)
        self.pause(4.0)

        self.play(
            FadeOut(VGroup(ambient, pole, equator, rider, shadow)), run_time=0.5
        )
        self.pause(4.5)

    # ------------------------------------------------------------------
    # S5 -- the Hopf map and its fibers
    # ------------------------------------------------------------------
    def scene_5(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("4 · THE HOPF MAP"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(5.0)

        base_center = np.array([-3.4, 1.1, 0.0])
        base_sphere = Sphere(radius=0.6, resolution=SPHERE_RESOLUTION_SMALL)
        base_sphere.move_to(base_center)
        base_sphere.set_fill(MINT, opacity=0.12)
        base_sphere.set_stroke(MINT, 1.2)
        base_sphere.set_shade_in_3d(True)
        self.play(Create(base_sphere), run_time=2.0)
        self.pause(7.0)

        hopf = self.carded(
            self.formula(
                r"h(z_1,z_2)=\bigl(2\operatorname{Re}z_1\bar{z}_2,\;"
                r"2\operatorname{Im}z_1\bar{z}_2,\;|z_1|^2-|z_2|^2\bigr)"
            ),
            down * 2.6,
        )
        self.play(FadeIn(hopf), run_time=2.0)
        self.pause(7.0)

        fiber_formula = self.carded(
            self.formula(
                r"\mathrm{fiber}(p)=\{(e^{it}z_1,e^{it}z_2):t\in[0,2\pi)\}"
            ),
            down * 1.7,
        )
        self.play(FadeIn(fiber_formula), run_time=2.0)
        self.pause(8.0)

        fiber = make_fiber(0.9, 0.0, CORAL)
        base_dot = Dot3D(point=base_center, color=GOLD, radius=0.06)
        self.play(Create(fiber), FadeIn(base_dot), run_time=2.0)
        self.pause(8.0)

        sweep = ValueTracker(0.0)

        def moving_base() -> np.ndarray:
            angle = TAU * sweep.get_value()
            return base_center + 0.6 * np.array([np.cos(angle), 0.0, np.sin(angle)])

        base_follower = always_redraw(
            lambda: Dot3D(moving_base(), color=GOLD, radius=0.06)
        )
        self.play(
            FadeOut(base_dot),
            FadeIn(base_follower),
            sweep.animate.set_value(1.0),
            fiber.animate.rotate(TAU, axis=up),
            run_time=2.0,
        )
        self.pause(8.0)

        self.play(
            sweep.animate.set_value(0.0),
            fiber.animate.rotate(TAU, axis=up),
            run_time=1.0,
        )
        self.pause(7.0)

        upper_fiber = make_fiber(1.3, 0.0, ROSE)
        self.play(FadeOut(fiber), Create(upper_fiber), run_time=1.5)
        self.pause(7.0)

        self.move_camera(
            phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.9, run_time=2.0
        )
        self.pause(7.0)

        caption = self.carded(self.note("one base point, one circle"), down * 3.0)
        self.play(FadeIn(caption), run_time=1.5)
        self.pause(7.0)

        punchline = self.carded(
            self.note("the fiber is the shadow of a great circle on S^3"),
            down * 2.3,
        )
        self.play(FadeIn(punchline), run_time=1.0)
        self.pause(6.0)

        self.play(FadeOut(VGroup(hopf, fiber_formula)), run_time=0.5)
        self.pause(6.0)

        self.play(
            FadeOut(VGroup(base_sphere, base_follower, upper_fiber)), run_time=0.5
        )
        self.pause(3.0)

    # ------------------------------------------------------------------
    # S6 -- linked
    # ------------------------------------------------------------------
    def scene_6(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN
        left = __import__("manim").LEFT

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("5 · LINKED"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(5.0)

        fiber_a = make_fiber(0.9, 0.0, CORAL)
        fiber_b = make_fiber(0.9, 2.1, SKY)
        self.play(Create(fiber_a), run_time=1.5)
        self.pause(7.0)

        self.play(Create(fiber_b), run_time=1.5)
        self.pause(8.0)

        self.play(fiber_a.animate.rotate(PI * 0.9, axis=up), run_time=1.5)
        self.pause(8.0)

        tag_a = self.carded(self.note("fiber A"), up * 2.2 + left * 3.0)
        tag_b = self.carded(self.note("fiber B"), up * 1.6 + left * 3.0)
        tag_a[1].set_color(CORAL)
        tag_b[1].set_color(SKY)
        self.play(FadeIn(tag_a), FadeIn(tag_b), run_time=1.0)
        self.pause(9.0)

        verdict = self.carded(
            self.note("linked: they cannot be pulled apart"), down * 3.0
        )
        self.play(FadeIn(verdict), run_time=1.0)
        self.pause(9.0)

        fiber_c = make_fiber(0.6, 0.8, MINT)
        fiber_d = make_fiber(0.6, 3.9, GOLD)
        self.play(Create(fiber_c), Create(fiber_d), run_time=1.5)
        self.pause(9.0)

        self.play(fiber_c.animate.rotate(PI * 0.8, axis=up), run_time=1.0)
        self.pause(9.0)

        self.move_camera(phi=40 * DEGREES, theta=-80 * DEGREES, run_time=1.5)
        self.pause(9.0)

        universal = self.carded(
            self.note("any two fibers: linking number one"), down * 3.0
        )
        self.play(FadeIn(universal), run_time=1.0)
        self.pause(8.0)

        in_four_d = self.carded(
            self.note("the crossing only exists in four dimensions"), down * 2.3
        )
        self.play(FadeIn(in_four_d), run_time=1.0)
        self.pause(7.0)

        self.play(Indicate(VGroup(fiber_a, fiber_b), color=WHITE), run_time=1.0)
        self.pause(6.0)

        self.play(
            FadeOut(VGroup(tag_a, tag_b, verdict, fiber_c, fiber_d)), run_time=0.5
        )
        self.pause(6.0)

        self.play(
            FadeOut(VGroup(fiber_a, fiber_b, universal, in_four_d)), run_time=1.0
        )
        self.pause(5.5)

        self.fade_all(0.5)
        self.pause(8.0)

    def build_structure(self) -> VGroup:
        """The line plus four nested Clifford tori, each woven with fibers."""
        z_line = Line3D(
            np.array([0.0, 0.0, -2.5]),
            np.array([0.0, 0.0, 2.5]),
            color=GOLD,
            thickness=0.02,
        )
        latitudes = [0.45, 0.85, 1.2, 1.5]
        colors = [SKY, MINT, CORAL, LILAC]
        bundles = [
            torus_bundle(theta, color) for theta, color in zip(latitudes, colors)
        ]
        shells = VGroup(*[shell for shell, _ in bundles])
        fibers = VGroup(*[group for _, group in bundles])
        return VGroup(z_line, shells, fibers)

    # ------------------------------------------------------------------
    # S7 -- the line and the Clifford tori
    # ------------------------------------------------------------------
    def scene_7(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("6 · ONE LINE, THREE TORI"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(5.0)

        z_line = Line3D(
            np.array([0.0, 0.0, -2.5]),
            np.array([0.0, 0.0, 2.5]),
            color=GOLD,
            thickness=0.02,
        )
        self.set_camera_orientation(
            phi=65 * DEGREES, theta=-52 * DEGREES, zoom=1.15
        )
        self.play(Create(z_line), run_time=2.0)
        self.pause(8.0)

        latitudes = [0.45, 0.85, 1.2, 1.5]
        colors = [SKY, MINT, CORAL, LILAC]
        bundles = [
            torus_bundle(theta, color) for theta, color in zip(latitudes, colors)
        ]
        shells = VGroup(*[shell for shell, _ in bundles])
        self.play(*[Create(shell) for shell in shells], run_time=5.0)
        self.pause(9.0)

        all_fibers = VGroup(*[fibers for _, fibers in bundles])
        self.play(*[Create(fibers) for fibers in all_fibers], run_time=5.0)
        self.pause(10.0)

        line_note = self.carded(
            self.note("the north-pole fiber: a circle of infinite radius"),
            down * 3.0,
        )
        self.play(FadeIn(line_note), run_time=1.0)
        self.pause(10.0)

        villarceau = self.carded(
            self.note("Villarceau circles: each torus is woven from fibers"),
            down * 2.3,
        )
        self.play(FadeIn(villarceau), run_time=1.0)
        self.pause(9.0)

        hero = bundles[-1][1][0]
        self.play(Indicate(hero, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.pause(9.0)

        codebook = self.carded(
            self.note("every circle here belongs to a base point"), down * 3.0
        )
        self.play(FadeIn(codebook), run_time=1.0)
        self.pause(8.0)

        self.play(Indicate(shells[0], color=SKY), run_time=1.0)
        self.pause(7.0)

        self.play(Indicate(VGroup(z_line), color=GOLD, scale_factor=1.05), run_time=1.0)
        self.pause(6.0)

        self.play(FadeOut(VGroup(line_note, villarceau, codebook)), run_time=0.5)
        self.pause(5.0)

        self.play(FadeOut(header), run_time=0.5)
        self.pause(5.5)

        self._carried = VGroup(z_line, shells, all_fibers)

    # ------------------------------------------------------------------
    # S8 -- the whole structure, Clifford translation
    # ------------------------------------------------------------------
    def scene_8(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("7 · THE WHOLE STRUCTURE"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(6.0)

        self.set_camera_orientation(
            phi=65 * DEGREES, theta=-52 * DEGREES, zoom=1.15
        )
        self.begin_ambient_camera_rotation(rate=0.15, about="phi")
        structure = self.build_structure()
        self.play(FadeIn(structure), run_time=4.0)
        self.pause(30.0)
        self.stop_ambient_camera_rotation()

        target_major, target_minor = torus_pair(0.9)
        shells = VGroup(
            *[
                Torus(
                    major_radius=target_major,
                    minor_radius=target_minor,
                    resolution=TORUS_RESOLUTION,
                )
                for _ in range(4)
            ]
        )
        for index in range(len(shells)):
            shells[index].set_fill(GOLD, opacity=0.18)
            shells[index].set_stroke(GOLD, 2.0)
            shells[index].set_shade_in_3d(True)

        self.play(Transform(structure[1], shells), run_time=5.0)
        self.pause(14.0)

    # ------------------------------------------------------------------
    # S9 -- why it matters
    # ------------------------------------------------------------------
    def scene_9(self) -> None:
        self._pause_log.append([])
        up = __import__("manim").UP
        down = __import__("manim").DOWN
        origin = __import__("manim").ORIGIN

        self.fade_all(1.0)
        self.pause(4.0)

        header = self.carded(self.header("8 · WHY IT MATTERS"), up * 3.1)
        self.play(FadeIn(header), run_time=1.0)
        self.pause(5.0)

        qubits = self.carded(
            self.note("a qubit state is a point on S two -- its phase is a fiber"),
            up * 2.2,
        )
        self.play(FadeIn(qubits), run_time=1.5)
        self.pause(7.0)

        rotations = self.carded(
            self.note("rotations of space: S three with antipodes glued"),
            down * 3.0,
        )
        self.play(FadeIn(rotations), run_time=1.5)
        self.pause(7.0)

        quaternions = self.carded(
            self.note("and the quaternions hide the same four-sphere"),
            down * 2.3,
        )
        self.play(FadeIn(quaternions), run_time=1.0)
        self.pause(7.0)

        history = self.carded(self.note("Heinz Hopf, 1931"), up * 3.1)
        self.play(FadeIn(history), run_time=1.0)
        self.pause(7.0)

        closing_cluster = VGroup(
            *[
                make_fiber(0.35 + 0.25 * k, TAU * k / 6, color, samples=90)
                for k, color in enumerate([CYAN, CORAL, SKY, MINT, GOLD, LILAC])
            ]
        )
        self.play(FadeIn(closing_cluster), run_time=2.0)
        self.pause(6.0)

        closing_title = Text(
            "THE HOPF FIBRATION", font_size=36, color=WHITE, font=FONT
        )
        self.play(FadeIn(closing_title.move_to(origin)), run_time=1.0)
        self.pause(6.0)

        final = self.carded(
            self.note("every circle linked to every other"), down * 3.0
        )
        self.play(FadeIn(final), run_time=1.0)
        self.pause(5.0)

        self.fade_all(0.5)
        self.pause(4.5)


VOICEOVER_SCRIPT = """
THE HOPF FIBRATION -- VOICEOVER SCRIPT
=====================================
Runtime 14:09. Total narration pause time 697 s.
Every [pause: X] below is exactly one self.pause(X) call in the matching
scene method, in the same order. SCENE_BUDGET asserts that equality, so this
transcript cannot drift out of sync with the render.
The audio track itself lives in narration.txt; nothing here is burned into
the picture as subtitles.

-- S1  0:00-0:50 --
"Stop. Look at this picture." [pause: 3]
"Six circles, floating in space. They never touch. And yet, every single one of them is linked to every other." [pause: 3]
"That alone is strange." [pause: 2]
"But here's what nobody tells you. This is not some exotic abstract construction. This is a shadow." [pause: 3]
"In the next fifteen minutes, we're going to find out where these circles come from. A four-dimensional sphere. And why, once you see it, the whole picture becomes obvious." [pause: 10]
"This is the Hopf fibration." [pause: 4]
"Let's begin." [pause: 6]

-- S2  0:50-2:22 --
"We're going to climb a ladder of spheres. Start simple. A circle." [pause: 3]
"This is the one-dimensional sphere, S one. All the points at distance one from the origin. One number decides where you are." [pause: 3]
"Add a dimension, and you get a sphere. The two-dimensional sphere, S two. The surface of a ball. Two numbers pin down any point." [pause: 7]
"Now the key step. What is the three-dimensional sphere, S three? Most people guess. The surface of a four-dimensional ball." [pause: 6]
"That's exactly right." [pause: 6]
"But here's the trick. S three can be written in a shockingly compact way. As the set of pairs of complex numbers, z one and z two, whose squared lengths add up to one." [pause: 7]
"And that single constraint pulls you down to a three-dimensional surface. A sphere, living in four dimensions." [pause: 7]
"Already, something is stirring. If I get to choose z one, then z two is free to trace out a circle." [pause: 6]
"S three is literally woven from circles." [pause: 7]
"We're going to make that precise. But first, we need the bridge that takes four-dimensional shapes and shows them to us in three dimensions." [pause: 7]
"It's called stereographic projection." [pause: 6]
"Let's build it, one dimension at a time." [pause: 7]
-- S3  2:22-4:21 --
"Stereographic projection squashes a sphere down to flat space. Let me show you with a circle. S one. Because everything carries over." [pause: 4]
"Draw the circle. Put a point at its north pole. From that pole, draw a line through any other point of the circle, and extend it until it hits the ground. Every point on the circle maps to exactly one point on the line." [pause: 7]
"One to one. With a single exception. The north pole itself. The line from the north pole through the north pole is ambiguous. It runs off sideways, forever." [pause: 7]
"So the projection point becomes the point at infinity. Everything else lands on the line." [pause: 7]
"Watch the point climb from the bottom of the circle toward the pole, and watch where its shadow lands. Slow at first, then runaway." [pause: 7]
"Points near the south pole barely move their shadow. Points near the north pole shoot off to infinity. That is the whole game." [pause: 7]
"Identical circles near the pole cast enormous shadows. Near the base, tiny ones. Distance is distorted. But a circle, as a shape, stays perfectly round." [pause: 8]
"Now watch what happens one dimension up, in three dimensions." [pause: 9]
"Here is a sphere. S two. With a plane beneath it." [pause: 7]
"Trace a latitude circle on the sphere, and project every point of it the same way. From the north pole, through the point, down to the plane. The shadow is a perfect circle." [pause: 7]
"This latitude, one hundred twenty degrees from the pole, casts a small shadow. Raise the latitude, closer to the pole. One hundred ten degrees. And the shadow grows." [pause: 7]
"Take the equator itself, ninety degrees. The shadow swells, but stays a perfect circle." [pause: 7]
"Any circle on the sphere, drawn away from the north pole, casts a perfectly circular shadow. Hold on to that." [pause: 6]
"Because we are about to do the exact same thing. One dimension higher." [pause: 6]
-- S4  4:21-5:58 --
"One dimension higher. Points of S three are four numbers, so to see them we project from a pole exactly as before. Only now the shadow lands in three-dimensional space." [pause: 5]
"The pole is the point zero, zero, zero, one. Project from it, and every other point of S three lands somewhere in our familiar three-dimensional space." [pause: 6]
"Here is the equator of S three. All points where the fourth coordinate is zero. It is a whole sphere in its own right." [pause: 7]
"Watch a single point travel along this equator." [pause: 7]
"And here is its shadow, in our space." [pause: 7]
"As the point moves around the equator, its shadow traces the unit circle, flat in the x y plane. The entire equator of S three becomes, exactly, this one circle." [pause: 8]
"Now tilt the great circle. Take a circle on S three that is not the equator." [pause: 7]
"Its shadow is still a circle. But now it is tilted in space, lifted off the plane, floating." [pause: 8]
"And that, at last, is where our opening picture comes from." [pause: 7]
"Every circle we saw floating in space is the shadow of a circle on S three." [pause: 6]
"But not every circle on S three is allowed. Only a very special family of them. The fibers." [pause: 6]
"Time to meet the map that carves S three into fibers." [pause: 4]
"The Hopf map." [pause: 4.5]
-- S5  5:58-7:47 --
"Write S three as pairs of complex numbers, z one and z two, with squared lengths that add to one." [pause: 4]
"The Hopf map sends such a pair to three real numbers. Twice the real part of z one times the conjugate of z two. Twice the imaginary part of that same product. And the difference of the squared lengths." [pause: 5]
"A mouthful, I know. But watch what it does geometrically." [pause: 7]
"Every point of S three lands on a point of the unit sphere, S two. You can check. Those three numbers always have combined length exactly one." [pause: 7]
"So the Hopf map is a function from S three onto S two. Now the question. What happens to the points of S three that all get sent to the same point of S two?" [pause: 8]
"Fix a point P of S two. The equation, h of z equals P, becomes two nice linear-looking equations in z one and z two. And their solutions form a circle on S three." [pause: 8]
"A whole circle of inputs, collapsing to a single output. Each of these circles gets a name. A fiber." [pause: 8]
"Here is one. On the little sphere in the corner I keep a base point. The target on S two. And here is the red fiber over it, drawn in space as its stereographic shadow." [pause: 7]
"It is a perfect circle." [pause: 7]
"Slide the base point around the equator, and the fiber rotates with it. One full turn for one full circuit." [pause: 7]
"Move the base point to a different latitude, and the circle floats higher, or grows larger." [pause: 7]
"Every point of S two has exactly one fiber over it. And every point of S three lies on exactly one fiber." [pause: 7]
"So the whole of S three, four-dimensional and invisible, umbrellas out into a three-dimensional space completely filled with circles." [pause: 6]
"Now, what happens when you pick two of them?" [pause: 6]
-- S6  7:47-10:01 --
"Take two fibers. Two circles in space, belonging to two different base points." [pause: 4]
"Here they are. Red and blue. Sitting apart." [pause: 5]
"Now the moment you have been waiting for. Rotate one through the other. Remember. The base point on S two moves continuously, so the fiber moves continuously through all of space between." [pause: 7]
"And look." [pause: 8]
"They are linked." [pause: 8]
"Like two links of a chain. There is no way to pull them apart without cutting one of them." [pause: 9]
"And this is not a special pair. Any two fibers. Any two at all. Are linked exactly once." [pause: 9]
"Let's prove it by feel. Slide the base points along different paths on the sphere. The circles slide through each other. And every time, they come out linked." [pause: 9]
"The linking number of any two fibers is exactly one." [pause: 9]
"Now here is the mind-bending part. The two fibers had to pass through each other, in space, to become linked." [pause: 9]
"But on S three they never touch. The crossing happens entirely in the fourth dimension, hidden from us. What we see is the shadow of a smooth, impossible-looking tangling." [pause: 9]
"A family of circles, one for each point of a sphere, every pair of them linked." [pause: 8]
"This is the Hopf fibration." [pause: 7]
"And we have not even seen the whole structure yet." [pause: 6]
"Because the fibers do not just exist in isolation. They organize into tori." [pause: 6]
"And one more beautiful fact. Fix any torus. It splits into two families of fibers. Red and blue. Every red circle links every blue circle exactly once. Circles of the same color sit side by side, never touching. Slide the red family around the blue direction, and each red circle flows into its neighbor. Until, after one full sweep, the entire torus is exactly where it started. That is the Clifford translation. A rotation of the four-dimensional sphere, seen as a perfect sliding of circles in space." [pause: 5.5]
-- S7  10:01-11:56 --
"Now the whole structure at once. One line down the middle, and a stack of nested tori, every surface made of linked circles." [pause: 4]
"Watch from far away. Let your eye follow the circles as they wrap around, and around." [pause: 5]
"And now let them slide. The red family flows one way, the blue family flows the other. No circle ever crosses another circle of its own color. The torus is not spinning. It is being woven." [pause: 8]
"Tilt the latitude of the base points, and the whole weaving shifts. The same circles. The same space. Now flowing the other way. An entire four-dimensional rotation, visible in three. That is the Hopf fibration in full." [pause: 9]
"Now look closer. The line down the middle is not a special case. It is the fiber over the north pole. A circle of infinite radius." [pause: 10]
"Everything else is a stack of Clifford tori. Theta equals point four five. A thin pencil of a donut. Theta equals point eight five, fatter and wider. Theta equals one point two, and one point five, wide sweeping tori that almost reach the bounding sphere." [pause: 10]
"Every one of those surfaces is woven from eight fibers, and those circles have a name. Villarceau circles." [pause: 9]
"A classic puzzle that dissolves the moment you know they are Hopf fibers." [pause: 9]
"Pick any circle in this space. It is a fiber. Look up its base point on the sphere, and you have located it exactly. The sphere is a code book for all of space." [pause: 8]
"And a line is just a circle of infinite radius." [pause: 7]
"Hopf found all of this in nineteen thirty-one." [pause: 6]
"And it never stopped mattering." [pause: 5]
"This is the structure. This is the whole map, drawn in space." [pause: 5.5]
-- S8  11:56-13:00 --
"Why does any of this matter?" [pause: 4]
"Because the Hopf fibration is not a curiosity. It is the skeleton of modern physics and geometry." [pause: 6]
"Every quantum state of a single qubit is a point on S two. The same sphere whose fibers filled our space. Quantum phases are the circles flowing around those points. The state of a two-qubit system is four complex numbers, and its phases are two linked circles. Entanglement is not a mystery. It is literally this picture. And rotations of three-dimensional space form the group S O three. Topologically, that group is precisely this sphere with antipodal points identified. The same four-dimensional sphere, cut into the same circles. Even the quaternions, that strange algebra of rotations, are hiding the same structure. One discovery, made by Heinz Hopf in nineteen thirty-one, still tying together the smallest computations and the grandest geometry in the universe." [pause: 30]
"So the next time you see a donut, or a swirl of linked circles, remember the hidden sphere. Four dimensions, folded down into three. Every circle linked to every other. The shadow of a four-dimensional sphere. This is the Hopf fibration." [pause: 14]
-- S9  13:00-14:09 --
"Six circles, to begin with. One for each of six directions on a sphere." [pause: 4]
"We began with a circle, and climbed to a sphere, and then to a sphere of spheres." [pause: 5]
"We learned to see four dimensions in three, by cutting out one point and letting it go to infinity." [pause: 7]
"We found a map from the four-sphere onto the two-sphere, and saw that every point of the two-sphere owns exactly one circle." [pause: 7]
"We proved that any two of those circles are linked. Once. No exceptions." [pause: 7]
"We stacked the latitudes into Clifford tori, and watched the whole thing weave itself without ever crossing." [pause: 7]
"And we found the same object hiding in qubits, in rotations, in quaternions." [pause: 6]
"Four numbers. One constraint. A whole universe of circles." [pause: 6]
"The Hopf fibration. Every circle linked to every other." [pause: 5]
"Thank you for watching." [pause: 4.5]
"""
