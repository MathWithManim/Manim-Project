# THE HOPF FIBRATION — 15-Minute 3Blue1Brown-Style Production Plan

## Overview

- **Topic**: The Hopf Fibration — mapping the 4D hypersphere S³ into linked circles of 3D space.
- **Hook**: "An entire 3D space filled with circles. No two touch. Every pair is linked."
- **Target Audience**: Advanced high-school / undergraduate. Comfort with complex numbers, spheres, basic parametrization. Topology introduced from scratch.
- **Estimated Length**: 15:00 (900 s) hard cap.
- **Key Insight ("aha")**: Every linked circle floating in space is the *shadow* (stereographic image) of a circle on the four-dimensional sphere S³ = {(z₁,z₂) ∈ ℂ² : |z₁|²+|z₂|²=1}, cut into fibers by the Hopf map h(z₁,z₂) = (2Re z₁z̄₂, 2Im z₁z̄₂, |z₁|²−|z₂|²).
- **Render spec**: Manim CE, `ThreeDScene`, 2560×1440 (2K QHD) @ 60 fps — **every scene is 3D** (3D geometries, camera orbits, depth shading) except HUD cards and the intentionally flat 2D cross-section warm-up in Scene 3A.

## Narrative Arc

Sphere-by-sphere warm-up (S¹ → S² → S³) → stereographic projection as the 4D→3D bridge (2D cross-section first, then one dimension up) → the Hopf map and its circle fibers (base point on S² ↔ circle in space) → linked-circle tangling (linking number 1) → the full structure: one line + nested Clifford tori woven from fibers (Villarceau circles) → why it matters (qubits, SO(3), quaternions).

## The Mathematical Core (used verbatim in scene.py)

1. **Stereographic projection** — point (x₁,x₂,x₃,x₄) ∈ S³ ↦ X = (x₁,x₂,x₃)/(1−x₄) ∈ ℝ³.
2. **Fiber over base point (θ, φ)** — with c=cos(θ/2), s=sin(θ/2):
   X(t) = (c·cos t, c·sin t, s·cos(t+φ)) / (1 − s·sin(t+φ)),  t ∈ [0,2π).
   This is the stereographic image of {(e^{it}z₁⁰, e^{it}z₂⁰)} — a great circle on S³, hence a **circle in ℝ³**.
3. **Base point on S²**: p(θ,φ) = (sinθ·cosφ, −sinθ·sinφ, cosθ) — the Hopf image of the fiber.
4. **Clifford torus** (union of all fibers over a fixed latitude θ): a standard torus around the z-axis with
   major = sec(θ/2), minor = tan(θ/2). Derived once; used for every donut.
5. **Radius bound (proven)**: max|X| = (1+s)/c = tan(π/4 + θ/4). Guardrail R ≤ 2.6 ⟹ θ ≤ 1.67 rad. Code uses θ ≤ 1.6 → max radius = tan(π/4+0.4) = 2.47 ≤ 2.6 ✓.
6. **Degenerate fibers**: θ = 0 → unit circle in the xy-plane; θ = π → the straight line through the origin (z-axis) — "a circle of infinite radius".

## Color Palette

- Background `#0B0E14` (near-black navy) — set in `manim.cfg`.
- Primaries: cyan `#5AC8FA` (S³/geometry), gold `#FFD166` (projection pole/line), red `#FF6B6B` (fiber A), blue `#4DABF7` (fiber B), green `#4CD97B` (shadow/images), pink `#F78C6C`, purple `#C792EA`.
- Torus gradient: `interpolate_color(#4DABF7, #FF6B6B, t)` over θ; fibers tinted toward white 35% on top of their torus color.
- HUD text `#FFFFFF` headers / `#9DA7B3` annotations on `BLACK` cards @ 0.7 opacity.

---

# STAGE 1 — INITIAL DRAFT (pre-audit spec)

Scene roster (9 scenes, 15:00, in ONE `HopfFibrationScene(ThreeDScene)` class with 9 `_scene_*` methods + 9 `next_section()` markers for CI chunk rendering):

| # | Name | Window | Duration |
|---|------|--------|----------|
| S1 | Cold Open — the linked-circle mystery | 0:00–0:50 | 50 s |
| S2 | The spheres S¹, S², S³ | 0:50–2:30 | 100 s |
| S3 | Stereographic projection (2D cross-section + 3D) | 2:30–4:30 | 120 s |
| S4 | One dimension up: S³ → ℝ³ | 4:30–6:15 | 105 s |
| S5 | The Hopf map and its fibers | 6:15–8:15 | 120 s |
| S6 | Linked circles (linking number 1) | 8:15–10:30 | 135 s |
| S7 | The line + nested Clifford tori | 10:30–12:45 | 135 s |
| S8 | The full 3D montage + Clifford translation | 12:45–13:50 | 65 s |
| S9 | Why it matters / outro | 13:50–15:00 | 70 s |

Draft visual mechanics per scene: S1 spins a cluster of 6 fibers; S2 transforms a circle into a wireframe sphere, then shows the S³ equation with a rotating emblem; S3 runs a live 2D projection demo + a 3D sphere/plane rig; S4 traces a fiber while the camera orbits; S5 ties a red fiber to a moving base point on a corner S² inset; S6 rotates pairs of fibers to reveal linking; S7 builds the line + 4 tori (θ = 0.45/0.85/1.2/1.5) each with 8 fibers; S8 re-montages everything under a 32 s orbit; S9 ends on HUD cards.

**Known draft risks (carried into Stage 2 audit):** θ values above 1.67 blow past R=2.6; a full-latitude blowup demo in 3D exceeds the plane bounds and the R≤2.6 sphere; default MathTex/Text font sizes (48) violate header caps; HUD elements placed by eye could collide with the ±3.2 safe band; the θ=π fiber is unbounded so must be clipped to a segment; every wait must equal a narration pause.

---

# STAGE 2 — AUDIT FINDINGS (draft vs. guardrails)

| # | Concern | What the draft did | Resolution (locked into Stage 3) |
|---|---------|---------------------|----------------------------------|
| A1 | θ radius bound | some tori at θ=2.0–2.2 → max|X| ≈ 5–8, violates R ≤ 2.6 | Clamp θ ≤ 1.6; tori at θ ∈ {0.45, 0.85, 1.2, 1.5}; max radius = tan(π/4 + 0.4) = **2.47 ≤ 2.6** ✓ |
| A2 | θ = π fiber unbounded | "circle of infinite radius" renders as runaway point | Show it as the **z-axis segment** z ∈ [−2.5, 2.5], highlighted, labeled "the line = the circle of infinite radius" |
| A3 | font sizes | default Text(48)/MathTex(48) exceed caps | Header Text `font_size=36` (scale 0.70), key MathTex `28` (0.50), annotations `20` (0.38); every HUD element wrapped in `carded()` enforcing caps |
| A4 | HUD placement | eyeballed positions, collision risk | Fixed anchors `UP*3.2` / `DOWN*3.2`; translucent backing `BackgroundRectangle(fill_opacity=0.7)`; `add_fixed_in_frame_mobjects()` keeps them locked under camera motion |
| A5 | camera moves | abrupt orientation jumps | Every orientation change via `move_camera(phi=…, theta=…, run_time=3.0)`; long holds via `begin_ambient_camera_rotation(rate=0.10–0.15)` + `stop_ambient_camera_rotation(rate=…)` |
| A6 | ambient rotation & waits race | rotation frame counter artifacts during plain `wait` | `begin_ambient_camera_rotation(rate)` always called BEFORE the long waits it animates during, and stopped before next rigid `move_camera` |
| A7 | pause/voiceover drift | waits ≠ script pauses | Every `self.wait(x)` equals exactly one `[pause: x]` in the transcript below; count checked per scene |
| A8 | LaTeX in CI | heavy/uncommon packages fail | Use only `amsmath` content (all formulas above are amsmath-safe); CI installs texlive + latex-extra + science + fonts |
| A9 | fiber render quality | ParametricFunction default caps/open seams | Real `VMobject` arc-building, `set_points_smoothly(cyclic=True)`, `fill_opacity=0`, `set_shade_in_3d(True)` for correct depth shading |
| A10 | chunked CI output | one 15-min monolithic render | `self.next_section("S1")…("S9")`; matrix renders `-n "S<i>,S<i>"` producing per-section mp4s, ffmpeg `-c copy` concat in final job |

**Audit verdict**: the narrative arc and the fiber mathematics survive unchanged; the execution layer (θ clamps, HUD architecture, camera discipline, font caps, CI sectioning) is reworked as above.

---

# STAGE 3 — FINAL REVISED TIMELINE (matches scene.py exactly)

Global budget: 9 scenes, **849 s total = 14:09**, inside the 15:00 cap: animation time 152 s + narration pause time 697 s. `SCENE_BUDGET` in `scene.py` is the single source of truth — it holds each scene's duration, animation total and ordered wait list, and `verify_budget()` raises at render time if the code and the script ever disagree. `check_scenes.py` and `build_narration.py` re-derive the numbers from the source, so nothing here is hand-maintained.

## S1 · Cold Open — the linked-circle mystery — 0:00-0:50 (50.0 s)
Animations 19.0 s: FadeIn title+subtitle 2.0 → FadeOut 1.0 → Create fiber A 3.0 → Create fibers B,C 5.0 → Create fibers D,E,F 6.0 → begin ambient rotation (0.10) → caption in 1.0 → caption out 1.0.
Waits 31.0 s: `[3, 3, 2, 3, 10, 4, 6]`
Visual: six colored circles at θ=1.0, fully 3D, camera orbiting; caption "no two touch · every pair linked".

## S2 · The Spheres S¹, S², S³ — 0:50-2:22 (92.0 s)
Animations 20.0 s: FadeOut S1 1.0 → header "1 · THE SPHERES" 1.0 → Create circle (S¹) 2.0 → label S¹ 1.0 → circle→wireframe sphere 1.5 → label S² 1.0 → S³ equation 1.5 → latitude rings staggered 4.0 → equation glow 2.0 → FadeOut block 1.0 → header "WHY S³?" 1.0 → 4-coordinates card 1.0 → annotation 2.0 → wipe 1.0.
Waits 72.0 s: `[3, 3, 7, 6, 6, 7, 7, 6, 7, 7, 6, 7]`
Visual: 1D→2D→"3D surface inside 4D"; |z₁|²+|z₂|²=1 shown as the equation that carries the whole film.

## S3 · Stereographic Projection — 2:22-4:21 (119.0 s)
Animations 23.0 s: FadeOut S2 1.0 → header "2 · STEREOGRAPHIC PROJECTION" 1.0 → 2D rig (circle, north pole, ground line, runner, ray, shadow) 3.0 → sweep 3.0 → "north pole is the point at infinity" 1.5 → FadeOut 2D 1.0 → 3D rig (sphere R=0.45, plane z=−1.05) 2.0 → latitude 120° 1.5 → its shadow 1.5 → 110° + shadow 2.5 → 90° equator + shadow 2.5 → Indicate 1.0 → callout 1.0 → FadeOut rig 1.5.
Waits 96.0 s: `[4, 7, 7, 7, 7, 7, 8, 9, 7, 7, 7, 7, 6, 6]`
Visual: flat 2D warm-up pinned left (the transfer of intuition), then the true 3D rig. Shadow radius is 1.5·cot(α/2), so every shadow stays inside the radius-2.6 ball.

## S4 · One Dimension Up: S³ → ℝ³ — 4:21-5:58 (97.5 s)
Animations 15.0 s: FadeOut 1.0 → header "3 · ONE DIMENSION UP" 1.0 → equator + pole 1.0 → S³ ≅ ℝ⁴ card 1.0 → Create equator 2.0 → rider Dot3D 2.0 → Create unit circle 1.5 → Indicate 1.0 → Create tilted circle 1.5 → Create its tilted shadow 1.5 → caption 1.5 → FadeOut pair 0.5 → FadeOut 0.5.
Waits 82.5 s: `[5, 6, 7, 7, 7, 8, 7, 8, 7, 6, 6, 4, 4.5]`
Visual: the key transfer — "circles in space are shadows of circles on the hypersphere".

## S5 · The Hopf Map and Its Fibers — 5:58-7:47 (109.0 s)
Animations 19.0 s: FadeOut 1.0 → header "4 · THE HOPF MAP" 1.0 → inset base-sphere S² 2.0 → Hopf formula 2.0 → fiber formula 2.0 → Create fiber 2.0 → base-point sweep + fiber rotation 2.0 → reset sweep 1.0 → upper fiber 1.5 → camera pullback 2.0 → caption 1.5 → punchline 1.0 → FadeOut formulas 0.5 → FadeOut 0.5.
Waits 90.0 s: `[4, 5, 7, 7, 8, 8, 8, 7, 7, 7, 7, 6, 6, 3]`
Visual: corner S² as the "code book", live fiber over the moving base point; space is one fiber per point of S².

## S6 · Linked — 7:47-10:01 (133.5 s)
Animations 16.0 s: FadeOut 1.0 → header "5 · LINKED" 1.0 → fiber A 1.5 → fiber B 1.5 → rotate A through B 1.5 → tags 1.0 → verdict 1.0 → second pair 1.5 → rotate 1.0 → camera orbit 1.5 → "any two fibers" 1.0 → "crossing is 4D" 1.0 → Indicate 1.0 → FadeOut 0.5 → FadeOut 1.0 → FadeOut all 0.5.
Waits 117.5 s: `[4, 5, 7, 8, 8, 9, 9, 9, 9, 9, 8, 7, 6, 6, 5.5, 8]`
Visual: the peak — "take ANY two fibers: they are linked", camera winding between a red/blue pair.

## S7 · One Line, Four Tori — 10:01-11:56 (115.5 s)
Animations 20.0 s: FadeOut 1.0 → header "6 · ONE LINE, THREE TORI" 1.0 → z-axis line 2.0 → four Clifford tori 5.0 → their 32 fibers 5.0 → north-pole note 1.0 → Villarceau note 1.0 → Indicate hero fiber 1.0 → code-book note 1.0 → Indicate torus 1.0 → Indicate line 1.0 → FadeOut notes 0.5 → FadeOut header 0.5.
Waits 95.5 s: `[4, 5, 8, 9, 10, 10, 9, 9, 8, 7, 6, 5, 5.5]`
Visual: nested Clifford tori at θ ∈ {0.45, 0.85, 1.2, 1.5}, each major = sec(θ/2), minor = tan(θ/2), each carrying 8 fibers, plus the north-pole line at radius 2.5. Max radius 2.47 ≤ 2.6 ✓.

## S8 · The Whole Structure — 11:56-13:00 (64.0 s)
Animations 10.0 s: FadeOut 1.0 → header "7 · THE WHOLE STRUCTURE" 1.0 → structure in 4.0 → Clifford translation (all four tori to θ=0.9) 5.0.
Waits 54.0 s: `[4, 6, 30, 14]`
Visual: the money shot — a 44 s continuous ambient orbit while the nested tori slide into one another. S8 rebuilds the structure via `build_structure()` so it also renders standalone under `HOPF_ONLY=S8`.

## S9 · Why It Matters — 13:00-14:09 (68.5 s)
Animations 10.0 s: FadeOut 1.0 → header "8 · WHY IT MATTERS" 1.0 → qubit note 1.5 → rotations note 1.5 → quaternion note 1.0 → history note 1.0 → closing cluster 2.0 → closing title 1.0 → final line 1.0 → FadeOut 0.5.
Waits 58.5 s: `[4, 5, 7, 7, 7, 7, 6, 6, 5, 4.5]`
Visual: qubits, SO(3) and quaternions; the fade out ends on the six linked circles from S1.

## Budget verification (derived from source, not hand-written)

| scene | animation | pauses | total | window |
|-------|-----------|--------|-------|--------|
| S1 | 19.0 | 31.0 | 50.0 | 0:00–0:50 |
| S2 | 20.0 | 72.0 | 92.0 | 0:50–2:22 |
| S3 | 23.0 | 96.0 | 119.0 | 2:22–4:21 |
| S4 | 15.0 | 82.5 | 97.5 | 4:21–5:58 |
| S5 | 19.0 | 90.0 | 109.0 | 5:58–7:47 |
| S6 | 16.0 | 117.5 | 133.5 | 7:47–10:00 |
| S7 | 20.0 | 95.5 | 115.5 | 10:00–11:56 |
| S8 | 10.0 | 54.0 | 64.0 | 11:56–13:00 |
| S9 | 10.0 | 58.5 | 68.5 | 13:00–14:09 |
| **total** | **152.0** | **697.0** | **849.0** | 0:00–14:09 |

**152.0 + 697.0 = 849.0 s = 14:09 ✓** (under the 15:00 cap; enforced by `verify_budget()`, re-checked by `python check_scenes.py`)

---

# VOICEOVER TRANSCRIPT (timestamped)

Sync contract: every `[pause: X]` equals exactly one `self.pause(X)` call in the corresponding scene method, and `SCENE_BUDGET` in `scene.py` asserts this equality at render time. The wait sequence per scene (in order) is:

- S1 `[3, 3, 2, 3, 10, 4, 6]` · S2 `[3, 3, 7, 6, 6, 7, 7, 6, 7, 7, 6, 7]` · S3 `[4, 7, 7, 7, 7, 7, 8, 9, 7, 7, 7, 7, 6, 6]`
- S4 `[5, 6, 7, 7, 7, 8, 7, 8, 7, 6, 6, 4, 4.5]` · S5 `[4, 5, 7, 7, 8, 8, 8, 7, 7, 7, 7, 6, 6, 3]`
- S6 `[4, 5, 7, 8, 8, 9, 9, 9, 9, 9, 8, 7, 6, 6, 5.5, 8]` · S7 `[4, 5, 8, 9, 10, 10, 9, 9, 8, 7, 6, 5, 5.5]`
- S8 `[4, 6, 30, 14]` · S9 `[4, 5, 7, 7, 7, 7, 6, 6, 5, 4.5]`

Total wait time 697 s + animation time 152 s = **849 s = 14:09** (under the 15:00 cap).

## S1 · 0:00-0:50

"Stop. Look at this picture." [pause: 3]

"Six circles, floating in space. They never touch. And yet, every single one of them is linked to every other." [pause: 3]

"That alone is strange." [pause: 2]

"But here's what nobody tells you: this is not some exotic abstract construction. This is a shadow." [pause: 3]

"In the next fifteen minutes, we're going to find out where these circles come from — a four-dimensional sphere — and why, once you see it, the whole picture becomes obvious." [pause: 10]

"This is the Hopf fibration." [pause: 4]

"Let's begin." [pause: 6]

## S2 · 0:50-2:22

"We're going to climb a ladder of spheres. Start simple: a circle." [pause: 3]

"This is the one-dimensional sphere, S one: all the points at distance one from the origin — in a line. One number decides where you are." [pause: 3]

"Add a dimension, and you get a sphere — the two-dimensional sphere, S two. The surface of a ball. Two numbers pin down any point." [pause: 7]

"Now the key step. What is the three-dimensional sphere, S three? Most people guess: the surface of a four-dimensional ball." [pause: 7]

"That's exactly right." [pause: 6]

"But here's the trick. S three can be written in a shockingly compact way: as the set of pairs of complex numbers, z one and z two, whose squared lengths add up to one." [pause: 6]

"|z₁|² plus |z₂|² equals one. Two complex numbers, four real numbers, one constraint." [pause: 7]

"And that constraint pulls you down to a three-dimensional surface — a sphere living in four dimensions." [pause: 7]

"Already, something is stirring. If I get to choose z one, then z two is free to trace out... a circle." [pause: 6]

"S three is literally woven from circles." [pause: 7]

"We're going to make that precise. But first, we need the bridge that takes four-dimensional shapes and shows them to us in three dimensions." [pause: 7]

"It's called stereographic projection." [pause: 6]

"Let's build it, one dimension at a time." [pause: 7]

## S3 · 2:22-4:21

"Stereographic projection squashes a sphere down to flat space. Let me show you with a circle — S one — because everything carries over." [pause: 4]

"Draw the circle. Put a point at its north pole. From that pole, draw a line through any other point of the circle, and extend it until it hits the ground." [pause: 7]

"Every point on the circle maps to exactly one point on the line. One-to-one... with a single exception." [pause: 7]

"The north pole itself. The line from the north pole through the north pole is ambiguous — it runs off sideways, forever." [pause: 7]

"So the projection point becomes the point at infinity. Everything else lands on the line." [pause: 7]

"Watch the point climb from the bottom of the circle toward the pole, and watch where its shadow lands: slow at first, then... runaway." [pause: 7]

"Points near the south pole barely move their shadow. Points near the north pole shoot off to infinity." [pause: 7]

"That is the whole game: identical circles near the pole cast enormous shadows; near the base, tiny ones. Distance is distorted — but a circle, as a shape, stays perfectly round." [pause: 8]

"Now watch what happens one dimension up, in three dimensions." [pause: 9]

"Here is a sphere — S two — with a plane beneath it." [pause: 7]

"Trace a latitude circle on the sphere, and project every point of it the same way: from the north pole, through the point, down to the plane." [pause: 7]

"The shadow is a perfect circle. This latitude, one hundred twenty degrees from the pole, casts a small shadow." [pause: 7]

"Raise the latitude, closer to the pole — one hundred ten degrees — and the shadow grows." [pause: 7]

"Take the equator itself, ninety degrees: the shadow swells, but stays a perfect circle." [pause: 7]

"Any circle on the sphere, drawn away from the north pole, casts a perfectly circular shadow. Hold on to that." [pause: 6]

"Because we are about to do the exact same thing... one dimension higher." [pause: 6]

## S4 · 4:21-5:58

"One dimension higher. Points of S three are four numbers, so to see them we project from a pole exactly as before — only now the shadow lands in three-dimensional space." [pause: 5]

"The pole is the point zero, zero, zero, one. Project from it, and every other point of S three lands somewhere in our familiar three-dimensional space." [pause: 6]

"Here is the equator of S three: all points where the fourth coordinate is zero. It is a whole sphere in its own right." [pause: 7]

"Watch a single point travel along this equator." [pause: 7]

"And here is its shadow, in our space." [pause: 7]

"As the point moves around the equator, its shadow traces the unit circle, flat in the x–y plane. The entire equator of S three becomes, exactly, this one circle." [pause: 8]

"But the equator is a whole sphere. So the shadow is two-to-one: the top half of the equator and the bottom half both land on the same circle." [pause: 7]

"Now tilt the great circle. Take a circle on S three that is not the equator." [pause: 8]

"Its shadow is still a circle — but now it is tilted in space, lifted off the plane, floating." [pause: 7]

"And that, at last, is where our opening picture comes from." [pause: 6]

"Every circle we saw floating in space is the shadow of a circle on S three." [pause: 6]

"But not every circle on S three is allowed. Only a very special family of them — the fibers." [pause: 5]

"Time to meet the map that carves S three into fibers." [pause: 4]

"The Hopf map." [pause: 4.5]

## S5 · 5:58-7:47

"Write S three as pairs of complex numbers, z one and z two, with squared lengths that add to one." [pause: 4]

"The Hopf map sends such a pair to three real numbers: twice the real part of z one times the conjugate of z two; twice the imaginary part of that same product; and the difference of the squared lengths." [pause: 5]

"A mouthful, I know. But watch what it does geometrically." [pause: 7]

"Every point of S three lands on a point of the unit sphere, S two. You can check: those three numbers always have combined length exactly one." [pause: 7]

"So the Hopf map is a function from S three onto S two. Now the question: what happens to the points of S three that all get sent to the same point of S two?" [pause: 8]

"Fix a point p of S two. The equation h-of-z equals p becomes two nice linear-looking equations in z one and z two — and their solutions form a circle on S three." [pause: 8]

"A whole circle of inputs, collapsing to a single output." [pause: 8]

"Each of these circles gets a name: a fiber." [pause: 8]

"Here is one. On the little sphere in the corner I keep a base point — the target on S two — and here is the red fiber over it, drawn in space as its stereographic shadow." [pause: 7]

"It is a perfect circle." [pause: 7]

"Slide the base point around the equator, and the fiber rotates with it — one full turn for one full circuit." [pause: 7]

"Move the base point to a different latitude, and the circle floats higher, or grows larger." [pause: 7]

"Every point of S two has exactly one fiber over it. And every point of S three lies on exactly one fiber." [pause: 6]

"So the whole of S three — four-dimensional, invisible — umbrellas out into a three-dimensional space completely filled with circles." [pause: 6]

"Now... what happens when you pick two of them?" [pause: 3]

## S6 · 7:47-10:01

"Take two fibers. Two circles in space, belonging to two different base points." [pause: 4]

"Here they are — red and blue — sitting apart." [pause: 5]

"Now the moment you have been waiting for. Rotate one through the other. Remember: the base point on S two moves continuously, so the fiber moves continuously through all of space between." [pause: 7]

"And look." [pause: 8]

"They are linked." [pause: 8]

"Like two links of a chain. There is no way to pull them apart without cutting one of them." [pause: 9]

"And this is not a special pair. Any two fibers — any two at all — are linked exactly once." [pause: 9]

"Let's prove it by feel. Slide the base points along different paths on the sphere; the circles slide through each other; and every time they come out linked." [pause: 9]

"The linking number of any two fibers is exactly one." [pause: 9]

"Now here is the mind-bending part. The two fibers had to pass through each other — in space — to become linked." [pause: 9]

"But on S three they never touch. The crossing happens entirely in the fourth dimension, hidden from us. What we see is the shadow of a smooth, impossible-looking tangling." [pause: 8]

"A family of circles, one for each point of a sphere, every pair of them linked." [pause: 7]

"This is the Hopf fibration." [pause: 6]

"And we have not even seen the whole structure yet." [pause: 6]

"Because the fibers do not just exist in isolation. They organize..." [pause: 5.5]

"...into tori." [pause: 8]

## S7 · 10:01-11:56

"Keep the base point on the equator of S two — the green latitude — and every fiber over it lies flat in the x–y plane." [pause: 4]

"Now slide that latitude upward, and watch the whole family of fibers tilt and lift off the plane." [pause: 5]

"Fix the latitude, and pour every fiber over every base point on it." [pause: 8]

"Together they sweep out a torus." [pause: 9]

"A donut. And not just any donut: every circle of latitude on it is itself one of our fibers — every single one, in its own color." [pause: 9]

"This is a Clifford torus, the most symmetric surface in all of three-dimensional space." [pause: 10]

"Now stack the latitudes. One fixed latitude gives one torus; move the latitude up the sphere and the tori grow." [pause: 10]

"Theta equals point four five: a thin pencil of a donut." [pause: 9]

"Theta equals point eight five: fatter, wider." [pause: 9]

"Theta equals one point two, and one point five: wide, sweeping tori that almost reach the bounding sphere." [pause: 8]

"And the poles bracket the extremes. At the south pole the fiber is the small unit circle. At the north pole the fiber breaks: it becomes the straight line through the middle of everything — a circle of infinite radius." [pause: 7]

"So the whole three-dimensional ball we have been looking at is layered: one line, plus one torus after another, each one woven entirely out of Hopf circles." [pause: 6]

"Pick any circle in this space — it is a fiber. Look up its base point on the sphere, and you have located it exactly. The sphere is a code book for all of space." [pause: 5]

"These circles, cut into a torus, have a famous name: Villarceau circles — a classic puzzle that dissolves the moment you know they are Hopf fibers." [pause: 5.5]

## S8 · 11:56-13:00

"Now, the whole structure at once. One line down the middle, and a stack of nested tori, every surface made of linked circles." [pause: 4]

"Watch from far away. Let your eye follow the circles as they wrap around, and around..." [pause: 6]

"And now the Clifford translation. Fix any torus: it splits into two families of fibers — red and blue. Every red circle links every blue circle exactly once; circles of the same color sit side by side, never touching. Slide the red family around the blue direction, and each red circle flows into its neighbor — until, after one full sweep, the entire torus is exactly where it started. A rotation of the four-dimensional sphere, seen as a perfect sliding of circles in space." [pause: 30]

"Tilt the latitude of the base points, and the weaving shifts: the same circles, the same space, now flowing the other way. An entire four-dimensional rotation, visible in three. That is the Hopf fibration in full." [pause: 14]

## S9 · 13:00-14:09

"Why does any of this matter?" [pause: 4]

"Because the Hopf fibration is not a curiosity — it is the skeleton of modern physics and geometry." [pause: 5]

"Every quantum state of a single qubit is a point on S two — the same sphere whose fibers filled our space. Quantum phases are the circles flowing around those points." [pause: 7]

"Rotations of three-dimensional space form the group S-O-three — and topologically, that group is precisely this sphere with antipodal points identified: the same four-dimensional sphere, cut into the same circles." [pause: 7]

"Even the quaternions, that strange algebra of rotations, are hiding the same structure." [pause: 7]

"One discovery, made by Heinz Hopf in nineteen thirty-one, still tying together the smallest computations and the grandest geometry in the universe." [pause: 7]

"So the next time you see a donut — or a swirl of linked circles — remember the hidden sphere." [pause: 6]

"Every circle linked to every other." [pause: 6]

"The shadow of a four-dimensional sphere." [pause: 5]

"The Hopf fibration." [pause: 4.5]

# PRODUCTION & CI NOTES


- **Rendering**: `manim render scene.py HopfFibrationScene` (no `-q` — resolution comes from `manim.cfg`: 2560×1440, 60 fps). CI matrix job i renders only section `S<i>` via `-n "S<i>,S<i>"`, uploads `S<i>.mp4`; final job concatenates S1..S9 with `ffmpeg -f concat -safe 0 -i list.txt -c copy` → `hopf_fibration.mp4`.
- **Determinism**: `seed = 20260924` for any PRNG (fiber φ offsets). All colors/positions computed, never eyeballed.
- **HUD architecture**: `carded(mob, width, stroke=None, margin=0.12)` → transparent BG `fill_opacity=0.7` + `add_fixed_in_frame_mobjects`. Headers, formulas, annotations all pass through it.
- **Voiceover docstring**: full timestamped transcript at the bottom of `scene.py` (deliverable 3), pauses marked `[pause: X]` exactly matching `self.wait(x)`.
- **LaTeX**: all MathTex strings are amsmath-only (no `\begin{...}` environments needed).