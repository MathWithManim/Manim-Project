# Production Plan — 2008 Jiangxi Gaokao Q22

## `1 < f(x,a) < 2` for all `x, a > 0`

A 17-minute, 2D-only, fully connected Manim Community Edition lecture.
Every proof step is its own scene. The first frame of every scene is the last
frame of the previous scene, built by a shared frame constructor so the handoff
is pixel-identical and every scene is still renderable standalone.

---

## 1. Overview

| Field | Value |
|---|---|
| Topic | Proving a two-variable inequality from the 2008 Jiangxi Gaokao |
| Engine | Manim Community Edition, 2D only (`Scene`, never `ThreeDScene`) |
| Audience | Graduating high-school students who know calculus |
| Voice | College professor: rigorous, warm, unhurried, never talks down |
| Target length | 17 minutes 30 seconds (tolerance 17:00 – 17:45) |
| Scene count | 27 scenes |
| Deliverable A | `scene.py` — one `Gaokao22Scene` class, 27 `next_section` markers, `VOICEOVER_SCRIPT` generated at the end of the file |
| Deliverable B | `scene_no_vo.py` — subclasses the same scene with `GAOKAO_CAPTIONS=1`, narration burned onto the screen |
| Deliverable C | `plan.md` — this document |
| Deliverable D | `verification/verify_math.py` — machine check of all 24 proof steps |
| Deliverable E | `verification/numerical_report.txt` — the 10,000-sample statistics table |

### The hook

The claim looks harmless: a sum of two shrinking square-root terms and one
growing square-root term, sandwiched between 1 and 2. The trap is that the
obvious attack dies immediately. Two variables, no constraint linking them, and
the three terms pull in *opposite* directions — as `x` grows the first term
falls while the third rises. There is no single monotonicity to exploit. The
problem is only solvable after a substitution that makes the three terms
*look* identical, and only if you then exploit the fact that their product is
pinned at exactly `8`.

### The aha moment

The third term `sqrt(ax/(ax+8))` looks like a different animal from
`1/sqrt(1+x)`. It is not. Divide top and bottom by `ax` and it *is*
`1/sqrt(1 + 8/(ax))` — the same function, evaluated at a third number. Now the
whole expression is one function applied to three numbers whose product is
pinned at `8`, and the entire problem inherits the symmetry it was hiding.

### The honesty beat

The constants are sharp. `f` approaches `1` as `x, a → +infinity` and approaches
`2` as `x, a → 0+`, and attains neither. We prove a strict inequality and then
prove we could not have written `1.0001` or `1.9999` instead. The lower-bound
proof is deliberately *not* sharp — it lands at `1` by a route with slack to
spare — and the video says so out loud rather than pretending otherwise.

---

## 2. The mathematics dossier

This is the content the animation must transmit exactly. Every line here has
been checked numerically by `verification/verify_math.py`.

### 2.1 The substitution

Set

```
A = x,    B = a,    C = 8 / (A*B)
```

Then `A*B*C = 8` and, because

```
1/sqrt(1 + 8/(AB))  =  sqrt(AB/(AB + 8))  =  sqrt(AB/(AB + ABC))
                    =  sqrt(1/(1 + C))    =  1/sqrt(1 + C),
```

the original expression becomes

```
f = 1/sqrt(1+A) + 1/sqrt(1+B) + 1/sqrt(1+C),      A, B, C > 0,  ABC = 8.
```

Write `phi(t) = 1/sqrt(1+t)`. The entire problem is now:

> For `A, B, C > 0` with `ABC = 8`, prove `1 < phi(A)+phi(B)+phi(C) < 2`.

This form is symmetric in `A`, `B`, `C`, which licenses the ordering
`A ≤ B ≤ C` without loss of generality. From `ABC = 8` and `A ≤ B ≤ C` we get
`A ≤ 2 ≤ C` and, more importantly, `A ≤ 2`.

### 2.2 Lower bound

**Step L1.** For every `t > 0`, `phi(t) > 1/(1+t)`.
Because `1+t > 1` we have `1+t > sqrt(1+t)`, so `1/(1+t) > 1/sqrt(1+t)`… with
the inequality read the other way: `sqrt(1+t) < 1+t` hence
`1/sqrt(1+t) > 1/(1+t)`. Strict, because `t > 0`.

**Step L2.** With `ABC = 8`,

```
1/(1+A) + 1/(1+B) + 1/(1+C) >= 1    <==>    A+B+C >= 6.
```

Proof: clear the positive denominator `(1+A)(1+B)(1+C)`. Let `S = A+B+C` and
`Q = AB+BC+CA`. The left side becomes

```
(1+B)(1+C) + (1+A)(1+C) + (1+A)(1+B)  =  3 + 2S + Q
```

and the right side becomes

```
(1+A)(1+B)(1+C)  =  1 + S + Q + ABC  =  9 + S + Q
```

using `ABC = 8`. The inequality `3 + 2S + Q >= 9 + S + Q` is exactly `S >= 6`.
Every other term cancels — this is the whole reason the number `8` was chosen
by the exam setters.

**Step L3.** AM–GM: `S = A+B+C >= 3*(ABC)^(1/3) = 3*2 = 6`, with equality only
at `A = B = C = 2`.

**Conclusion.** `f > 1/(1+A)+1/(1+B)+1/(1+C) >= 1`, so `f > 1`. The first
inequality is strict, so the chain is strict regardless of whether L3 is tight.

### 2.3 Upper bound

Order the variables `A ≤ B ≤ C`. The dangerous configuration is `A, B → 0` with
`C → +infinity`, where the first two terms tend to `1` each and the third tends
to `0`, so `f → 2`. The supremum lives exactly on that corner, which means the
proof must be *sharp* near it — no crude bound will do.

Set `s = A+B` and `p = AB`, so `C = 8/p` and `phi(C) = sqrt(p/(p+8))` exactly.

**Step U0 (Cauchy–Schwarz).**

```
phi(A) + phi(B)  <=  sqrt( 2 * (1/(1+A) + 1/(1+B))  )  =  sqrt( 2(2+s)/(1+s+p) )
```

because `(1+A)(1+B) = 1+s+p`.

**Monotonicity fact.** The derivative of `(2+s)/(1+s+p)` with respect to `s` is
`(p-1)/(1+s+p)^2`, so the bound in U0 *decreases* in `s` when `p < 1` and
*increases* in `s` when `p > 1`. Also `s >= 2*sqrt(p)` by AM–GM, with equality at
`A = B`.

**Lemma L3 (one variable, sharp).** For every `q > 0`,

```
2/sqrt(1+q) + q/sqrt(q^2+8)  <  2.
```

*Proof.* Rearrange to

```
q/sqrt(q^2+8)  <  2 - 2/sqrt(1+q)  =  2q / (1 + q + sqrt(1+q))
```

(using `sqrt(1+q) - 1 = q/(sqrt(1+q)+1)`). Since `q > 0`, divide by `q` and it
suffices to show

```
1 + q + sqrt(1+q)  <  2 sqrt(q^2 + 8).
```

Now `sqrt(1+q) <= 1 + q/2` (square both sides: `1+q+q^2/4 >= 1+q`), so the left
side is at most `2 + 3q/2`. And

```
4(q^2+8) - (2 + 3q/2)^2  =  4q^2 + 32 - 4 - 6q - (9/4)q^2  =  (7/4)q^2 - 6q + 28.
```

The discriminant of `(7/4)q^2 - 6q + 28` is `36 - 196 = -160 < 0` with positive
leading coefficient, so it is positive for all real `q`. Hence
`2 + 3q/2 < 2 sqrt(q^2+8)`, and the lemma follows. ∎

**Case 1: `A + B >= 6`.** Since `A ≤ 2`, we get `B >= 6 - A >= 4`, and since
`C >= B`, also `C >= 4`. Therefore

```
f = phi(A) + phi(B) + phi(C)  <  1 + 1/sqrt(5) + 1/sqrt(5)  =  1 + 2/sqrt(5)  <  2
```

because `2/sqrt(5) < 1` is just `4 < 5`. Note `phi(A) < 1` strictly since `A > 0`.

**Case 2: `A + B < 6`.** First, `p = AB < A(6-A)`, and because `0 < A <= 2` the
map `A -> A(6-A)` is increasing on `(0,2]` with value `8` at `A=2`. Hence
`p < 8`. Now three sub-ranges, all bounded above by `2`:

*Sub-range (i), `p <= 1`.* U0's bound decreases in `s`, so it is largest at the
minimal feasible `s = 2 sqrt(p)`:

```
phi(A)+phi(B)  <=  sqrt( 2(2+2sqrt(p)) / (1+2sqrt(p)+p) )  =  2/sqrt(1+sqrt(p)).
```

Adding the third term and putting `q = sqrt(p) > 0` gives
`f <= 2/sqrt(1+q) + q/sqrt(q^2+8) < 2` by Lemma L3.

*Sub-range (ii), `1 < p <= 3`.* U0's bound increases in `s`, and `s < 6`, so

```
f  <  sqrt( 2*8/(7+p) ) + sqrt(p/(p+8))  <=  sqrt(2) + sqrt(3/11)  <  2.
```

The last step is exact: `2 - sqrt(2) > sqrt(3/11)` because
`(2-sqrt2)^2 = 6-4sqrt2 > 3/11`, i.e. `63 > 44 sqrt(2)`, i.e. `3969 > 3872`.

*Sub-range (iii), `3 < p < 8`.* Same bound, with `sqrt(16/10) = 4/sqrt(10)` and
`sqrt(8/16) = 1/sqrt(2)`:

```
f  <  4/sqrt(10) + 1/sqrt(2)  <  2.
```

Exact: `2 - 1/sqrt(2) > 4/sqrt(10)` because `(2 - 1/sqrt2)^2 = 9/2 - 2 sqrt 2`
and `16/10 < 9/2 - 2 sqrt 2` reduces to `2.9 > 2 sqrt 2`, i.e. `8.41 > 8`.

**Conclusion.** Every case gives `f < 2`, so `1 < f < 2` for all `x, a > 0`. ∎

### 2.4 Why the bounds are optimal

* `x, a → +infinity`: `f → 0 + 0 + 1 = 1` from above. So the infimum is `1`.
* `x, a → 0+`: `f → 1 + 1 + 0 = 2` from below. So the supremum is `2`.

Neither is attained for positive `x, a`, which is exactly why the statement uses
strict inequalities. This is a fact about the *problem*, not about our proof,
and the video separates the two clearly.

### 2.5 Verification ledger

`verification/verify_math.py` checks all of the above on dense grids: the
substitution identity, the strictness of L1, the equivalence in L2 including
the cleared-denominator identity, AM–GM, the Cauchy bound U0 on every feasible
`(s, p)`, the derivative sign used for the monotonicity, all three lines of the
Lemma L3 proof, the Case 1 region, the Case 2 region including all three
sub-ranges, and the 10,000-sample table. All 24 checks pass.

One earlier draft of this plan used a different, prettier lemma — that
`sup{phi(A)+phi(B) : AB=p}` equals `max(1, 2/sqrt(1+sqrt p))`. Numerical
testing killed it: at `p = 9` the true supremum is `1.0607`, not the claimed
`1.0000`. The bound is wrong, and the Cauchy route above replaced it. The video
does not teach the false version.

---

## 3. Design system

### 3.1 Palette

| Token | Hex | Role |
|---|---|---|
| `BG` | `#0B0E14` | Background, near-black blue |
| `INK` | `#F2F4F8` | Primary text and formulas |
| `MUTED` | `#8B95A5` | Secondary text, axis labels, scaffolding |
| `GRID` | `#2A3140` | Grid lines, frame furniture |
| `BLUE` | `#4C8DFF` | The function `phi`, the first two terms |
| `TEAL` | `#2DD4A7` | Lower-bound `1`, safe region, "yes" |
| `AMBER` | `#FFC24B` | AM–GM, the key inequality being proved |
| `CORAL` | `#FF6B6B` | Upper-bound `2`, danger region, "no" |
| `VIOLET` | `#A78BFA` | The third term, the substitution |

Rule: a colour always means the same thing. Teal is always "the lower bound or
the good side". Coral is always "the upper bound or the danger". Amber is
always "the tool I am using right now". This is the single most important
decision for making 17 minutes feel like one lecture.

### 3.2 Layout grid

The Manim frame is 14.222 by 8.0 units. Three fixed horizontal zones:

| Zone | Vertical extent | Contents |
|---|---|---|
| Header | `y` from `2.95` to `3.75` | Scene number, scene title, part label |
| Stage | `y` from `-2.45` to `2.85` | Everything mathematical |
| Caption | `y` from `-3.70` to `-2.65` | Narration, or the key-idea callout |

Nothing is ever placed outside `|x| <= 6.95`, `|y| <= 3.75`. All positioning
goes through helpers, never raw `.shift()` calls with hand-tuned numbers, so
the "not out of bounds" requirement is enforced structurally rather than by
eyeballing.

### 3.3 Type scale

| Role | Size | Weight |
|---|---|---|
| Scene title | 34 | semibold |
| Hero formula | 50 | regular |
| Working formula | 40 | regular |
| Label, axis text | 24 | regular |
| Caption text | 27 | regular |
| Micro-annotation | 21 | regular |

### 3.4 Motion language

* Formulas are *written*, never typed letter by letter. `Write` on a `MathTex`
  is the default reveal.
* A formula that is being proved arrives in amber and settles to ink.
* Inequalities that are strict get a `≠`-style highlight: the strict sign is
  drawn in teal, the loose sign in muted grey, so the audience can see at a
  glance which step carries the strictness.
* Nothing enters from off-screen. Every mobject fades or writes *in place*.
* Scene-to-scene, the outgoing frame is never wiped. It is transformed.

---

## 4. Scene-by-scene specification

Timing totals 1050 seconds. Every scene opens by adding the previous scene's
frame via `frame_k()` and closes by settling into `frame_k()`.

---

### Scene 01 — Title

**Duration** 40 s · **Part** Hook · **Frame in** none · **Frame out** `frame_01()`

*Purpose.* Establish subject, level, and promise.

*Visuals.* Faint contour-map texture of `f` across the whole background at low
opacity, so the video opens on the actual object of study. Centre: the
statement `1 < f(x,a) < 2` at hero size in ink, with `x, a > 0` beneath in
muted. Above it a single line: `2008 Jiangxi Gaokao · Q22`. Below: the full
three-term expression at working size. Bottom-left: `17-minute proof, every
step on screen`.

*Narration.* Open on the problem as a *promise*, not a task: this is a hard
problem, and we are going to take it apart completely.

*Technical.* Background contour map is a `set_color_by_gradient` on a
`VMobject` grid drawn once and cached; it must cost under 0.4 s to build or it
eats the scene.

---

### Scene 02 — Why this is hard

**Duration** 30 s · **Part** Hook · **Frame in** `frame_01()` · **Frame out** `frame_02()`

*Purpose.* Kill the naive approach before the audience tries it, and reveal the
opposing-directions trap.

*Visuals.* Two small `Axes` side by side. Left: `phi(x) = 1/sqrt(1+x)` falling
from 1 to 0, in blue. Right: `sqrt(ax/(ax+8))` rising from 0 to 1, in violet,
with `a` fixed. Between them a coral double-headed arrow labelled
`they fight each other`. Underneath, in muted: `x ↑ ⇒ first term ↓, third term ↑`.

*Narration.* Explain the mechanical obstruction: the two depend on `x` in
opposite directions, so there is no single monotonicity to lean on. This is why
students hand this problem in blank.

*Technical.* Both curves are `Axes.plot` with `x_range` chosen so the shapes are
legible at the small size; use `x_range=[0, 40, 40]` for the falling curve so
its tail is visible rather than infinitely flat.

---

### Scene 03 — The shape of `phi`

**Duration** 40 s · **Part** Toolkit · **Frame in** `frame_02()` · **Frame out** `frame_03()`

*Purpose.* Meet the single function the whole video is about.

*Visuals.* One large `Axes` filling the stage. `phi(t)` in blue, `t` from 0 to
12. The value `phi(0) = 1` marked with a teal dot and a dashed guide to the
axis. The tail behaviour annotated: `phi(t) ~ 1/sqrt(t)` in muted, with the
words `dies slowly`. A soft vertical band shading `0 < t < 1` in blue at low
opacity.

*Narration.* Define `phi`. Stress the two facts we will actually use: it is
*bounded above by 1*, and it *decreases*, but it decreases like `1/sqrt(t)`,
which is slow enough to be dangerous.

*Technical.* Use `Axes(x_range=[0,12,6], y_range=[0,1.05,0.25])`; set
`x_length=7.4, y_length=4.6` so it fits the stage with axis labels inside the
safe area.

---

### Scene 04 — What an integral is, and why we care

**Duration** 50 s · **Part** Toolkit · **Frame in** `frame_03()` · **Frame out** `frame_04()`

*Purpose.* Build the area intuition that makes the later comparisons obvious.
The user asked for this explicitly.

*Visuals.* Same axes. Under the curve, a Riemann sum animating in: `n` thin
vertical bars in blue at low opacity, `n` doubling `2 → 4 → 8 → 16 → ∞` as the
bars become the filled region. The region fill is teal at low opacity. The
integral sign and value fade in above: `∫₀¹ dt/sqrt(1+t) = 2(sqrt 2 − 1)`. Then
a coral dashed line at height 1 spanning the interval, with the caption
`the curve hides under the line y = 1`.

*Narration.* Define an integral as accumulated area under a curve, built from
rectangles. Then make the point that matters: the area under `phi` on `[0,1]` is
`2(sqrt2 − 1) ≈ 0.83`, strictly less than the area of the unit rectangle. This
is the first hint that `phi` lives *below* `1`, and that a comparison of areas
can prove inequalities without any calculus at all.

*Technical.* Animate the Riemann sum with `LaggedStart(*[Create(b) for b in
bars], lag_ratio=0.08)`. Swap bars for the filled region with
`Transform(bars, region)`. Do not use `FadeTransform` on hundreds of thin
mobjects; keep `n <= 32`.

---

### Scene 05 — AM–GM for two numbers, from zero

**Duration** 50 s · **Part** Toolkit · **Frame in** `frame_04()` · **Frame out** `frame_05()`

*Purpose.* Do not assume AM–GM. Prove it, twice, and mean it.

*Visuals.* Split stage. **Left, geometric:** a circle of radius `a+b` with a
horizontal chord at height `sqrt(ab)`; a right triangle with hypotenuse `a+b`
and altitude `sqrt(ab)` inscribed, its two base segments labelled `a` and `b`.
The altitude is at most half the hypotenuse, drawn as a teal dashed line, with
the label `sqrt(ab) <= (a+b)/2`. **Right, analytic:** the function
`g(t) = t + 1/t` plotted for `t` from 0.2 to 5, with its minimum at `t=1` marked
`g(1) = 2`, and the rearrangement `a + b >= 2 sqrt(ab)` written beneath.

*Narration.* State the inequality, prove it as a geometric fact about altitudes
in a semicircle, then prove it again as a calculus fact about a minimum. Tell
the audience explicitly: this is the tool that will produce the number `6`, so
it is worth being pedantic about it.

*Technical.* The semicircle construction is `Circle` plus two `Line`s plus two
`RightAngle` markers. Put the whole construction in a `VGroup` and scale it to
`height=3.4` so it never crosses the caption zone.

---

### Scene 06 — AM–GM for three numbers

**Duration** 35 s · **Part** Toolkit · **Frame in** `frame_05()` · **Frame out** `frame_06()`

*Purpose.* Generalise to the form actually used.

*Visuals.* The geometric half fades back. Centre stage:
`A + B + C >= 3 (ABC)^(1/3)`, hero size, with the equality condition
`iff A = B = C` in teal underneath. Then the substitution of the constraint:
`(ABC)^(1/3) = 8^(1/3) = 2`, so `A+B+C >= 6`, in amber, arriving as a
`Transform` so the viewer *sees* the `6` fall out of the `8`.

*Narration.* Three-variable AM–GM. Then plant the payoff early: the moment the
product is pinned at `8`, the cube root is `2`, and three times `2` is `6`.
That `6` is going to show up twice — once for the lower bound, once as the
case split for the upper bound.

*Technical.* Use `TransformMatchingTex` from the general form to the specialised
form so the `3(ABC)^(1/3)` morphs into `3·2 = 6` rather than cutting.

---

### Scene 07 — Convexity: the bending-up idea

**Duration** 40 s · **Part** Toolkit · **Frame in** `frame_06()` · **Frame out** `frame_07()`

*Purpose.* Give the vocabulary for why `phi` behaves, and one usable fact.

*Visuals.* A single `Axes` showing three curves bending upward in blue, plus
`phi` overlaid in amber. On the left half, a tangent line to `phi` drawn in
coral at `t = 3`, with the curve visibly *above* it everywhere. Annotation in
teal: `convex ⇒ every tangent line is a global lower bound`. On the right
half, the two-limit demonstration: as `t → 0`, `phi(t) → 1`, drawn as a
sequence of dots marching toward the dashed line `y=1` that `phi` never touches.

*Narration.* Define convexity as "bends upward". Give the one consequence we
will use: a convex function lies above all of its tangent lines. Note that the
limit `phi → 1` from below is *not* attained, which is the seed of the
sharpness discussion in the final act.

*Technical.* `phi` second derivative is `(3/4)(1+t)^{-5/2} > 0`; show that
computation briefly in muted beside the plot, because a professor would.

---

### Scene 08 — Cauchy–Schwarz, from zero

**Duration** 45 s · **Part** Toolkit · **Frame in** `frame_07()` · **Frame out** `frame_08()`

*Purpose.* Prove the exact form used in the upper bound.

*Visuals.* Left: a vector picture. Two arrows from the origin, `u` in blue and
`v` in violet, with the parallelogram shaded. The projection of `u` onto `v`
drawn dashed in teal, and the leftover component drawn in coral. Label:
`|u|² = (projection)² + (leftover)² ≥ (projection)²`.
Right: the algebraic form arriving as a `Write`:

```
(phi(A) + phi(B))^2  <=  2 ( 1/(1+A) + 1/(1+B) )
```

and immediately the simplification that the whole upper bound will run on:

```
(1+A)(1+B) = 1 + s + p        with   s = A+B,  p = AB
```

*Narration.* Derive it as "the projection can never be longer than the vector".
Then state the promise: in the hard part of the proof we will bound two of the
three terms with this and handle the third exactly, so we will need to know
exactly how much this costs.

*Technical.* Keep the vector diagram to `scale_factor` such that its bounding
box is at most 4.2 units wide, leaving room for the formulas on the right.

---

### Scene 09 — The third term is not a third term

**Duration** 45 s · **Part** Substitution · **Frame in** `frame_08()` · **Frame out** `frame_09()`

*Purpose.* The pivot of the entire lecture.

*Visuals.* Centre stage, the third term alone, huge, in violet:

```
sqrt( ax / (ax + 8) )
```

Then an animated division of numerator and denominator by `ax`, written as a
`Transform` so the `ax` visibly cancels:

```
=  sqrt( 1 / (1 + 8/(ax)) )  =  1 / sqrt(1 + C),      C := 8/(ax)
```

The letter `C` arrives in amber. Below, in ink at working size, the whole
expression reassembles in a single line, all three terms now the same colour:

```
f = phi(A) + phi(B) + phi(C),        A = x,  B = a,  C = 8/(AB)
```

*Narration.* Slow down here. This is the aha moment. For nineteen minutes the
audience has been looking at two square roots and a ratio; now they see three
copies of the same function. The asymmetry that made the problem look hostile
was an illusion of notation.

*Technical.* The cancelling division is best done with two `MathTex` objects and
`TransformMatchingTex` on the `ax` tokens, with `key_matching=False` guard
against colour mismatches.

---

### Scene 10 — The real problem: three numbers, product eight

**Duration** 40 s · **Part** Substitution · **Frame in** `frame_09()` · **Frame out** `frame_10()`

*Purpose.* State the reduced problem cleanly and reveal why 8 is the magic
number.

*Visuals.* The `A + B + C` line from Scene 06 reappears and morphs into
`A · B · C = 8` — the *sum* bound of 6 replaced by the *product* constraint.
Alongside, the reduced problem in a bordered card, centred:

```
A, B, C > 0,   ABC = 8
        prove   1  <  phi(A) + phi(B) + phi(C)  <  2
```

A small annotation in amber: `8 = 2³ — three terms, each centred at 2`.

*Narration.* Point out that `8` is not arbitrary: it is `2³`, so the geometric
mean of the three variables can be `2`, and the natural centre of the problem
is "all three equal to 2". Then note that the problem just became symmetric,
which is a structural gift we are about to spend.

*Technical.* Card is a `RoundedRectangle` with `corner_radius=0.18`, fill
`#121722`, stroke `GRID` at 1.5. Keep its width at most 11.5 units.

---

### Scene 11 — Symmetry buys an ordering

**Duration** 30 s · **Part** Substitution · **Frame in** `frame_10()` · **Frame out** `frame_11()`

*Purpose.* Legitimise `A ≤ B ≤ C`, which the whole upper bound depends on.

*Visuals.* Three identical chips labelled `A`, `B`, `C` in a row, each
carrying `phi(·)`. Animate them swapping places twice to make the symmetry
obvious, then settle into ascending order with a `WLOG A <= B <= C` label in
teal. Under it, the two consequences, arriving one at a time:
`A <= 2` and `2 <= C`, each with a one-line justification in muted
(`A³ <= ABC = 8`).

*Narration.* Because the expression no longer knows the difference between the
three letters, we are allowed to sort them. Flag `A <= 2` explicitly: that
single fact is what makes the upper bound's case split work.

*Technical.* The chip swap uses `AnimationGroup` of `Transform`s with
`path_arc` so the motion reads as a permutation, not a dissolve.

---

### Scene 12 — `phi(t) > 1/(1+t)`

**Duration** 35 s · **Part** Lower bound · **Frame in** `frame_11()` · **Frame out** `frame_12()`

*Purpose.* The engine of the lower bound: replace a square root by a rational
function that we can sum exactly.

*Visuals.* The stage axes return. `phi(t)` in blue and `1/(1+t)` in amber
plotted together. The two curves are visibly ordered, with the gap shaded
between them in teal at low opacity. The reason, written beside: for `t > 0`,
`1+t > 1` so `1+t > sqrt(1+t)`, therefore `1/sqrt(1+t) > 1/(1+t)`. A teal
`>` sign emphasised with a small circle.

*Narration.* The move is to trade an awkward square root for a rational
function. The trade is strictly one-sided, in our favour, and the rational
version of the same sum turns out to collapse to a single linear condition.

*Technical.* Both plots share one `Axes` so the vertical comparison is honest.
Shade the gap with a `Polygon` built from the two sampled polylines, not from a
thousands of thin bars.

---

### Scene 13 — Summing the rational version

**Duration** 45 s · **Part** Lower bound · **Frame in** `frame_12()` · **Frame out** `frame_13()`

*Purpose.* The algebraic heart: clear denominators and watch everything cancel.

*Visuals.* A three-line derivation, each line arriving with `Write` and the
cancelled terms visibly struck through in muted as the next line appears.

```
1/(1+A) + 1/(1+B) + 1/(1+C)  >=  1
(1+B)(1+C) + (1+A)(1+C) + (1+A)(1+B)  >=  (1+A)(1+B)(1+C)
                3 + 2S + Q   >=   1 + S + Q + ABC
                3 + 2S + Q   >=   1 + S + Q + 8
                3 + 2S + Q   >=   9 + S + Q
                              A + B + C  >=  6
```

with `S = A+B+C`, `Q = AB+BC+CA` defined in muted at the side. The final line
lands in amber at hero size. Immediately after, `A+B+C >= 3(ABC)^(1/3) = 6` from
Scene 06 flies in underneath as a `TransformFrom`, closing the argument.

*Narration.* Walk the cancellation slowly; this is the moment the exam-setters'
choice of `8` pays off, because every symmetric term drops out and only a
single linear inequality survives. Then invoke AM–GM.

*Technical.* Strike-throughs via `Line` mobjects with `stroke_width=2` in
`GRID`, animated with `Create`. Lay the three derivation lines with
`arrange(DOWN, buff=0.42)` starting from `STAGE_TOP` so the block never grows
downward into the caption zone.

---

### Scene 14 — Lower bound closed

**Duration** 20 s · **Part** Lower bound · **Frame in** `frame_13()` · **Frame out** `frame_14()`

*Purpose.* Lock in `f > 1` and be honest that the proof has slack.

*Visuals.* The full chain assembled as one horizontal strip in the stage, each
link in its established colour:

```
f  >  1/(1+A)+1/(1+B)+1/(1+C)  >=  1
```

The first `>` in teal and circled, the second `>=` in amber, then a large
`f > 1` in teal fading in above. Beneath, in muted: `equality in AM–GM would
need A=B=C=2, but the first step is strict, so f > 1 regardless`.

*Narration.* State the conclusion. Then immediately volunteer the weakness:
at `A=B=C=2` we have `f = sqrt 3 ≈ 1.73`, not `1`, so this route has real slack.
We will not need it to be sharp, but the audience should know.

*Technical.* The circled strict sign is a `Circle` of radius 0.17 with
`stroke_width=2.5` in teal, added after the chain settles.

---

### Scene 15 — Why 2 is the enemy

**Duration** 35 s · **Part** Upper bound · **Frame in** `frame_14()` · **Frame out** `frame_15()`

*Purpose.* Show the audience the danger corner *before* the proof, so the case
split feels motivated rather than arbitrary.

*Visuals.* The `(x, a)` stage axes from Scene 02, now with a coral path drawn
in the corner `x, a → 0+`, and a value tracker pushing a marker along it. The
running value of `f` displayed large, climbing `1.0 → 1.4 → 1.7 → 1.88 → 1.97 →
1.999…`, never reaching `2`. A coral dashed line at `f = 2` sits just above,
untouched. Annotation: `sup f = 2, never attained`.

*Narration.* Walk the corner. The sum approaches 2 from below and would cross it
if we were careless. Therefore the proof must be sharp exactly here, and that
rules out any bound that is comfortable in the middle of the domain and loose
at the edges.

*Technical.* Drive with a `ValueTracker` on `t` from 1 down to 0.02 and a
`always_redraw` display group, so the running value is genuinely computed
rather than keyframed.

---

### Scene 16 — Case 1: `A + B >= 6`

**Duration** 35 s · **Part** Upper bound · **Frame in** `frame_15()` · **Frame out** `frame_16()`

*Purpose.* Dispatch the easy case with total confidence.

*Visuals.* Three number-line style bars for `A`, `B`, `C` stacked vertically in
the stage. Fill in blue up to the current value, amber past it. The reasoning
arrives as a chain, each step on its own line with the *previous* step's
conclusion highlighted:

```
A <= 2            (from Scene 11)
B >= 6 - A >= 4   (case hypothesis)
C >= B >= 4       (ordering)
f < 1 + 1/sqrt5 + 1/sqrt5 = 1 + 2/sqrt5 = 1.894... < 2
```

The final number `1.894` in teal, with `2/sqrt5 < 1` justified beneath as
`4 < 5`.

*Narration.* Note the shape of the argument: the case hypothesis is strong, so
two of the three variables are forced to be at least 4, which caps two of the
three terms at `1/sqrt5` and leaves the third term strictly below 1. Done.

*Technical.* Bars are `Rectangle`s on a shared baseline `Line`, heights scaled
so a value of 6 occupies 2.6 units.

---

### Scene 17 — Case 2: set-up

**Duration** 45 s · **Part** Upper bound · **Frame in** `frame_16()` · **Frame out** `frame_17()`

*Purpose.* Derive the single master bound for the hard case and the key
restriction `p < 8`.

*Visuals.* Centre stage, `s = A+B` and `p = AB` introduced as two labelled
dials. Then the two facts, each with its derivation:

```
phi(C) = sqrt( p / (p+8) )                     exactly
phi(A)+phi(B) <= sqrt( 2(2+s)/(1+s+p) )        by Cauchy
```

Then `p < 8` with its proof: `p = AB < A(6-A)`, and the parabola `A(6-A)`
plotted for `A` in `(0,2]` peaking at `8` exactly at `A = 2` — a small parabola
in amber with its right endpoint marked. Then the master bound in a card:

```
f  <  sqrt( 2(2+s)/(1+s+p) )  +  sqrt( p/(p+8) ),        0 < p < 8
```

*Narration.* The third term is now exact — we know it to the digit. Only the
first two are approximated, and only by Cauchy. Then the restriction that makes
the estimate finite: because the case hypothesis caps the sum and `A <= 2`
caps the smaller variable, the product is bounded, and `8` is the sharp cap.

*Technical.* The small parabola is `Axes.plot(lambda t: t*(6-t), x_range=[0,2.2])`
with `x_length` and `y_length` around 2.6, placed to the right of the card, not
overlapping it.

---

### Scene 18 — The sharp sub-case and the lemma

**Duration** 55 s · **Part** Upper bound · **Frame in** `frame_17()` · **Frame out** `frame_18()`

*Purpose.* Handle `p <= 1`, where any crude bound fails, by proving a sharp
one-variable lemma. The intellectual centre of the upper bound.

*Visuals.* The sub-range `0 < p <= 1` highlighted on the `p` dial. Then the
monotonicity fact, with the derivative computed and its sign read off:

```
d/ds [ (2+s)/(1+s+p) ]  =  (p-1)/(1+s+p)^2   <=  0   for p <= 1
```

so the Cauchy bound is *largest* at the smallest feasible `s = 2 sqrt(p)` (from
AM–GM), which evaluates to the clean form `2/sqrt(1+sqrt p)`. Then the reduced
statement, `q := sqrt p`:

```
2/sqrt(1+q)  +  q/sqrt(q^2+8)  <  2          for every q > 0
```

declared as **Lemma** in a bordered card. Then its three-line proof, animated
one line at a time with each rearrangement justified:

```
2 - 2/sqrt(1+q)  =  2q / (1 + q + sqrt(1+q))        [rationalise]
1 + q + sqrt(1+q)  <=  2 + 3q/2                      [sqrt(1+q) <= 1+q/2]
(7/4)q^2 - 6q + 28  >  0    because  discriminant = -160 < 0
=>  2 + 3q/2  <  2 sqrt(q^2+8)   =>   lemma
```

*Narration.* Take your time. Explain *why* this sub-case needs a sharp tool: as
`p → 0` the crude bound tends to `2` from the wrong side, so no amount of
slack in a rougher inequality will do. Then note the lemma is proved for all
`q > 0`, which is more than we need — a small generosity worth remarking on.

*Technical.* Lemma card uses a violet stroke, width at most 11.0, centred at
`y = 0.1`. The discriminant line gets a small inline `Circle` around `-160`.

---

### Scene 19 — The remaining sub-ranges

**Duration** 40 s · **Part** Upper bound · **Frame in** `frame_18()` · **Frame out** `frame_19()`

*Purpose.* Finish Case 2 with two sub-ranges where slack is available.

*Visuals.* A compact three-row table builds in the stage, one row per
sub-range, each row filling in as it is discussed:

| sub-range | bound on the first two terms | bound on the third | total |
|---|---|---|---|
| `p <= 1` | `2/sqrt(1+sqrt p)` | `sqrt(p/(p+8))` | `< 2` (Lemma) |
| `1 < p <= 3` | `sqrt 2` | `sqrt(3/11)` | `1.9364 < 2` |
| `3 < p < 8` | `4/sqrt 10` | `1/sqrt 2` | `1.9720 < 2` |

The `p` dial behind the table fills with a teal-to-amber gradient across the
three ranges so the audience sees the partition. The exactness of the last two
rows appears on demand beneath: `63 > 44 sqrt 2` and `2.9 > 2 sqrt 2`.

*Narration.* Here slack is available, so the arithmetic is quick. Emphasise that
the sub-ranges are chosen only so that a *single* worst-case number works per
row; nothing deep is happening in this scene. The deep part was the lemma.

*Technical.* The table is a `Table` mobject with `cell_height` tuned so total
height stays under 3.2 units, or build it manually from `Text` and `MathTex` in
a `VGroup` arranged with `arrange(DOWN, aligned_edge=LEFT)`, which gives
predictable width control.

---

### Scene 20 — Upper bound closed

**Duration** 20 s · **Part** Upper bound · **Frame in** `frame_19()` · **Frame out** `frame_20()`

*Purpose.* Close the argument and present the theorem.

*Visuals.* The table collapses into a single verdict card. `1 < f < 2` at hero
size in ink, with the `1` in teal and the `2` in coral. Under it, the
substitution line, small and muted, so the viewer can read the whole proof as
one chain: `A=x, B=a, C=8/(AB), ABC=8`.

*Narration.* Both bounds closed. Read the theorem. Then a beat of silence
before the pictures — the rest of the video is about *seeing* it.

*Technical.* Card fades in over the table with `FadeTransform`, keeping the
table's mobjects underneath at reduced opacity for one beat, then clearing.

---

### Scene 21 — Panel 1: the contour map, and the forbidden levels

**Duration** 50 s · **Part** Pictures · **Frame in** `frame_20()` · **Frame out** `frame_21()`

*Purpose.* Panel 1 of the requested figure set, in 2D. Instead of a 3D surface
we draw its shadow: a filled contour map of `f` over `x, a` with the level
curves `f = 1` and `f = 2` drawn as heavy isolines. The point lands visually —
the whole square is coloured, and *neither* heavy line is ever crossed by the
field, because the field never reaches those values.

*Visuals.* `x, a` on log-scaled axes from `1e-3` to `1e3`, so the interesting
structure is not crushed into a corner. Filled contours of `f` in a
teal-to-amber ramp, about fourteen bands. The `f = 1` isoline in heavy teal and
the `f = 2` isoline in heavy coral, both drawn as `Create` on sampled
`ParametricFunction`s solved by bisection along each row. A marker walks the
diagonal and the running value is displayed. Axis labels `x` and `a`.

*Narration.* Explain the honest substitution we made: a 3D surface would hide
the very thing we care about, which is that the surface never touches the planes
`z=1` and `z=2`. Drawn as contours, the claim becomes a picture you can check
with your eyes: the colour field lives strictly between two isolines that it
never reaches.

*Technical.* Build the field on a 260-by-260 log-spaced grid; store as a numpy
array and emit one `Polygon` per band via marching along rows. Keep the
polygon count near fourteen by choosing band edges as quantiles of the sampled
values, not as a linear ramp — a linear ramp produces almost no visible
structure because `f` clusters near 1.6.

---

### Scene 22 — Panel 2: the slice viewer

**Duration** 45 s · **Part** Pictures · **Frame in** `frame_21()` · **Frame out** `frame_22()`

*Purpose.* Panel 2: fix `a`, sweep `x`, and watch the three terms add up.

*Visuals.* Large `Axes` for `x` from 0 to 30, vertical range 0 to 2. Four
curves: `phi(x)` in blue, `phi(a_fixed)` as a horizontal dashed line in blue,
`sqrt(ax/(ax+8))` in violet, and their sum in ink at higher stroke width. A
horizontal band between `f=1` and `f=2` shaded teal at very low opacity. A
`ValueTracker` sweeps `x`; at each position three short vertical segments stack
to show the running addition, and a large readout shows the total, which visibly
stays inside the band. The fixed value `a = 2` is labelled and can be changed
by the viewer later in the file.

*Narration.* Slow the sweep. Point out the counter-motion: as `x` grows the blue
curve collapses and the violet curve rises to meet it, and the total never
leaves the band. This is the two-terms-fighting picture from Scene 02, now with
the arithmetic attached.

*Technical.* The stacked segments are an `always_redraw` `VGroup` reading the
tracker, so they are exact. Keep the readout at `y = 2.35`, inside the stage.

---

### Scene 23 — Panel 3: the `abc = 8` landscape

**Duration** 40 s · **Part** Pictures · **Frame in** `frame_22()` · **Frame out** `frame_23()`

*Purpose.* Panel 3: the symmetric transformation, shown in the coordinates
where it is actually simple.

*Visuals.* Two panels. **Left:** `ln A` against `ln B` on a square grid, with
the constraint surface `ln A + ln B + ln C = ln 8` appearing as the family of
lines `ln A + ln B = const`, each labelled by the resulting `C`. The line
`ln A + ln B = ln 8` (i.e. `C = 1`) drawn heavy, with the point `A = B = 2`
marked as the centre. **Right:** the same information as a colour map of `f`
restricted to that surface, using the same teal-to-amber ramp as Panel 1, so
the two panels are visibly the same object in two coordinates.

*Narration.* Explain the substitution's real content: taking logarithms turns
the multiplicative constraint into a plane, so "product 8" is really "a plane
in log-space", and the symmetric point `A=B=C=2` is the origin of that plane.
The surface has no boundary, but `f` still has a supremum, attained as the
audience sees, out at the corners.

*Technical.* Log axes: use ordinary `Axes` but set tick labels via
`DecimalTracker` to powers of ten, or simply label with explicit `Text` marks
at `-3, 0, 3` to keep it clean and 2D.

---

### Scene 24 — Panel 4: the case inspector

**Duration** 40 s · **Part** Pictures · **Frame in** `frame_23()` · **Frame out** `frame_24()`

*Purpose.* Panel 4: show which case each point of the domain falls into, so the
case split is visible as a *partition* rather than an abstract dichotomy.

*Visuals.* The `(A, B)` plane with `A, B` in `(0, 6]`, `A <= B` half shown.
The region `A + B >= 6` filled teal at low opacity and labelled **Case 1**. The
complement filled amber at low opacity and labelled **Case 2**. Within Case 2,
the three sub-ranges of `p = AB` separated by hyperbolas `p = 1` and `p = 3`,
each labelled with its bound. A marker walks a path that crosses the boundary
line, and the active case label flashes as it crosses.

*Narration.* Tie the abstraction back to geometry. The proof's two cases are
literally two regions of the domain, separated by a straight line, and the
sub-ranges are separated by two hyperbolas. Nothing mysterious is happening;
the case split is just bookkeeping for where our estimates are sharp.

*Technical.* Region fills via `Polygon` from explicit vertex lists, clipped
numerically to the `A <= B` half. Hyperbolas are `ParametricFunction`s of
`p` over the clipped range.

---

### Scene 25 — The numerical verification table

**Duration** 40 s · **Part** Pictures · **Frame in** `frame_24()` · **Frame out** `frame_25()`

*Purpose.* Panel 5, the requested statistics, presented as evidence and as a
caution about what sampling can and cannot prove.

*Visuals.* A clean table built row by row on screen, values arriving in
monospace-aligned teal: sample size 10,000; minimum 1.0057185834; maximum
1.9999952380; mean 1.5829599535; variance 0.1160372704. Below it, two
histogram bars: a `BarChart` of the distribution of `f` across the samples, in
teal, with a coral dashed marker at 1 and at 2 showing the sample range occupies
only a sliver of the allowed interval, and a caption `0 samples at or below 1,
0 samples at or above 2`.

*Narration.* Read the table. Then the honest caveat, said plainly: ten
thousand samples is evidence, not proof — the closest approach to 2 was within
five-millionths, which shows how tight the bound is, but no amount of sampling
proves a strict inequality. That is what the proof is for.

*Technical.* Precompute all statistics with numpy inside the scene module at
import time so the scene itself only animates. Use `seed=20080` so the numbers
on screen are exactly the numbers in `verification/numerical_report.txt`.

---

### Scene 26 — Sharpness: 1 and 2 cannot be improved

**Duration** 35 s · **Part** Pictures · **Frame in** `frame_25()` · **Frame out** `frame_26()`

*Purpose.* The payoff: both constants are optimal, and the strictness is
forced.

*Visuals.* Two halves. **Left:** as `x, a → +infinity`, three small readouts —
`phi(x) → 0`, `phi(a) → 0`, third term `→ 1` — and the total `→ 1` from above,
in teal. **Right:** as `x, a → 0+`, readouts `→ 1`, `→ 1`, `→ 0`, total `→ 2`
from below, in coral. Between them, a single line: `inf f = 1, sup f = 2,
neither attained`. Then the two-limit animation: two markers running off
towards `0` and towards `infinity` along the diagonal, with the total
asymptote labels following.

*Narration.* Because the infimum is 1, writing `1.0001` would be false.
Because the supremum is 2, writing `1.9999` would be false. And because
neither limit is attained, the problem *must* be stated with strict
inequalities. The exam-setters chose 1 and 2 for a reason.

*Technical.* The two running totals are `always_redraw` from a `ValueTracker`
on a parameter `t` with `x = a = 10^t`, `t` sweeping `-3` to `3`, so both
halves are driven by one honest computation.

---

### Scene 27 — Closing

**Duration** 25 s · **Part** Pictures · **Frame in** `frame_26()` · **Frame out** `frame_27()`

*Purpose.* Leave the complete proof on screen and end cleanly.

*Visuals.* Everything condenses into one column: the substitution, the lower
bound chain, the upper bound's two-case structure in miniature, and the
verdict. A final line in muted: `verification/verify_math.py — 24/24 checks
pass`. The header title returns to `1 < f(x,a) < 2`.

*Narration.* Read the whole proof once, start to finish, in about fifteen
seconds. Invite the audience to run the verification script themselves.

*Technical.* Final frame must be visually calm: no more than nine distinct
elements, generous spacing, and a long final `wait` so the video does not cut
abruptly.

---

## 5. Continuity contract

* `frame_of(name)` is a pure function returning a `VGroup` that reconstructs the
  closing picture of any section from scratch, via the `FRAME_BUILDERS` registry.
* Section `k` opens by adding `frame_{k-1}()` and closes by transforming its
  working mobjects into `frame_k()` via `finish()`.
* Because both the outgoing and incoming frames come from the same builder, the
  last frame of section `k` and the first frame of section `k+1` are identical by
  construction, not by hand-matching.
* Every scene is therefore renderable in isolation: rendering scene 14 alone
  still produces the correct opening picture.
* No scene is allowed to `self.clear()` its inherited frame. Transitions are
  `Transform`, `FadeTransform`, `ReplacementTransform`, or `Write` on top.

## 6. Caption and voiceover system

One shared beat table, `BEATS`, maps a key like `"s13.b2"` to a
`(text, duration)` pair. Scenes call `self.say("s13.b2")`.

* In `scene.py` the global `CAPTIONS` is `False`, so `say` simply holds for the
  beat's duration, through `pause()`, which also records the timeline. The narration text lives in the beat table
  only, and the full voiceover script is written out at the **end of the file**
  as `VOICEOVER_SCRIPT`, grouped by scene, ready to be recorded against.
* In `scene_no_vo.py` the global `CAPTIONS` is `True`, so `say`
  renders the beat's text into the caption zone at the bottom of the frame,
  wrapped to 13.0 units, and holds for the same duration.

Because both files read the same table and the same durations, the captioned
version is frame-for-frame synchronised with the voiceover version. There is no
second copy of the text to drift out of sync.

Caption rendering rules: 27-point, `INK` at 92 percent opacity, on a
`#121722` rounded bar with 78 percent opacity, `word_wrap=True`,
`width=13.0`, vertically centred at `y = -3.15`, and never allowed to exceed
two lines — beats are written to fit.

## 7. Implementation order

1. Core: palette constants, layout constants, `BEATS`, `say`, caption bar,
   title bar, `frame_k` stubs, `TIMINGS` ledger.
2. Toolkit scenes 03 to 08, since they define the visual vocabulary.
3. Hook sections 1 and 2, written after the vocabulary exists.
4. Substitution sections 9 to 11.
5. Lower bound sections 12 to 14.
6. Upper bound sections 15 to 20, the most algebraically dense block.
7. Picture panels 21 to 24.
8. Numerics and sharpness 25 and 26.
9. Close 27.
10. `VOICEOVER_SCRIPT` generated from the transcript at the end of `scene.py`.
11. `scene_no_vo.py` as a thin driver that flips the caption flag.

## 8. Quality gates

| Gate | Criterion |
|---|---|
| Import | `python -m py_compile scene.py scene_no_vo.py` exits 0 |
| Construct | `python check_scenes.py` runs all 27 sections plus the layout audit, exit 0 |
| Duration | The `assemble` job reports the joined duration; the narration floor is 15:30 |
| Bounds | `check_scenes.py --frames` proves every closing picture fits `x = ±6.95`, `y = ±3.75` |
| Legibility | Smallest text on screen is 21-point equivalent, and no formula is scaled below 0.62 of hero size |
| Continuity | `frame_of()` rebuilds each closing picture, so handoffs match by construction and CI can render any section alone |
| Math | `python verification/verify_math.py` prints `ALL PROOF STEPS VERIFIED`, exit 0, 24/24 |
| No 3D | `audit_deliverables.py` greps both files for `ThreeDScene`, `ThreeDAxes`, `Surface` |

## 9. Risks and mitigations

* **LaTeX availability.** `MathTex` needs a TeX install. If it is missing on the
  render machine, every scene fails at once. Mitigation: confirm TeX before the
  first real render, and keep a `Tex`-free fallback only for the two table
  scenes, where plain `Text` is used anyway.
* **Contour polygons are heavy.** Panel 1 can generate thousands of vertices.
  Mitigation: cap the grid at 260 by 260 and use quantile band edges, and build
  the field once at module import, cached in a module-level global.
* **Beat drift.** If a scene's animations grow longer than planned, the
  narration desynchronises. Mitigation: `say` takes its duration from the table
  and the `TIMINGS` ledger prints the real per-scene totals, so drift is
  measured rather than guessed.
* **Over-stuffing.** 17 minutes across 27 scenes averages 39 seconds each; the
  temptation to cram is real. Mitigation: the stage is capped at roughly nine
  simultaneous elements, and every scene in this plan has been specified with an
  explicit element budget.
* **Teaching a false lemma.** The first draft of the upper bound used a wrong
  pairwise supremum, caught only by numerical testing. Mitigation: no inequality
  reaches a scene until `verify_math.py` has checked it on a dense grid.


---

## 10. Build and verification commands

```bash
python verification/verify_math.py   # 24 proof-step checks + the 10,000-sample table
python check_scenes.py                # 27-section logic smoke test + layout audit
python check_scenes.py --frames       # layout and continuity audit only
python build_narration.py             # regenerate narration.txt from the transcript
python audit_deliverables.py          # every hard requirement from the brief
python scene.py                       # print the full timecoded voiceover script
```

Rendering never happens locally. `.github/workflows/render.yml` runs a `verify`
job first, which byte-compiles every module, runs the smoke test with
rasterization stubbed out, regenerates `narration.txt` and fails if the
committed copy is stale, runs the numerical proof check, and runs the
deliverable audit. Only then does the matrix fan out, one job per section per
variant, and a final `assemble` job joins each variant and reports its duration.

## 11. What the smoke test caught

The layout and logic harness earned its keep before a single frame was
rendered, and every one of these would have failed a CI render:

* `weight="bold"` is not a valid Manim weight. Pango wants the `BOLD` constant,
  so all nineteen bold titles raised before the first frame.
* `MathTex` emits one submobject per LaTeX *argument*. A single-string formula
  has exactly one submobject, so every attempt to colour the `1` and the `2` by
  index raised `IndexError`. The bounds now come from a `verdict_tex` helper
  that passes the bounds as separate arguments.

  The glyph-map route was tried and is not available in 0.21. Measured on this
  build: `tex_to_color_map=` is accepted and inert, `substrings_to_isolate=` is
  accepted and leaves the formula as one submobject, `get_parts_by_tex()` raises
  `TypeError: getter() takes 1 positional argument but 2 were given`, and
  `set_color_by_tex()` silently does nothing because it calls the broken one.
  Each submobject's `tex_string` is populated correctly, so the map data is
  there and only the accessors are broken. Direct index assignment
  (`verdict[0].set_color(...)`) is therefore the only working mechanism, which
  is what `verdict_tex` does.
* `Text` lost its `word_wrap` and `width` kwargs, so the caption bar wraps its
  own lines and then clamps them with `fit_width` as a backstop.
* `get_riemann_rectangles` forwards keyword arguments to `Rectangle`, so the
  integrality argument is `fill_opacity`, not `opacity`.
* `run_section` assumed `construct` had already run, which defeated its whole
  purpose as a standalone entry point for the CI matrix.
* `stage_fit` only constrained width, so a tall stack of formulas escaped
  through the top of the frame. It now shrinks to fit both dimensions and clamps
  both axes, and the audit checks all 27 closing pictures.
* A diagonal plotted against an axis whose y-range stopped at 2.1 ran off to
  y = 19. Plotted curves are not clipped by Manim.

The first draft of the upper bound used a pairwise supremum lemma that is simply
false. It was killed by dense numerical testing at p = 9 and replaced by the
Cauchy argument that is actually proved on screen. Nothing reaches a scene
before `verify_math.py` has checked it on a grid.
