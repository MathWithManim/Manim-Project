"""2008 Jiangxi Gaokao Q22 - a 17-minute connected 2D proof of  1 < f < 2.

    f(x,a) = 1/sqrt(1+x) + 1/sqrt(1+a) + sqrt(ax/(ax+8)),    x, a > 0

One Scene class, twenty-seven ``next_section`` markers, so CI renders each
section independently via ``GAOKAO_ONLY=...``.  ``pause`` is the narration clock:
its sequence is recorded, asserted against NARRATION at the end of the render,
and mined by build_narration.py to emit narration.txt, so the transcript cannot
drift away from the movie.

Continuity: the first frame of every section is the last frame of the one before
it.  ``frame_of`` rebuilds that closing picture from scratch, which keeps each
handoff pixel-identical and every section independently renderable.

Set ``GAOKAO_CAPTIONS=1`` (see scene_no_vo.py) to burn the same transcript onto
the screen as a caption bar instead of leaving it to narration.

Every inequality shown here is machine-checked by verification/verify_math.py.
"""

from __future__ import annotations

import os

import numpy as np
from manim import *


BG = "#0B0E14"
CARD = "#121722"
INK = "#F2F4F8"
MUTED = "#8B95A5"
GRID = "#2A3140"
BLUE = "#4C8DFF"
TEAL = "#2DD4A7"
AMBER = "#FFC24B"
CORAL = "#FF6B6B"
VIOLET = "#A78BFA"

# ---------------------------------------------------------------------------
# layout grid - nothing is ever placed outside these bounds
# ---------------------------------------------------------------------------
FRAME_W = 14.222
FRAME_H = 8.0
SAFE_X = 6.95
SAFE_Y = 3.75
HEADER_Y = 3.20
STAGE_TOP = 2.80
STAGE_BOT = -2.45
STAGE_CY = (STAGE_TOP + STAGE_BOT) / 2.0
CAPTION_Y = -3.12
CAPTION_W = 13.0

FS_TITLE = 34
FS_HERO = 50
FS_WORK = 40
FS_LABEL = 24
FS_CAPTION = 27
FS_MICRO = 21

CAPTIONS = bool(int(os.environ.get("GAOKAO_CAPTIONS", "0")))
ONLY = os.environ.get("GAOKAO_ONLY")
SECTION_COUNT = 27

PHI = lambda t: 1.0 / np.sqrt(1.0 + t)
F2 = lambda x, a: PHI(x) + PHI(a) + np.sqrt(a * x / (a * x + 8.0))

# ---------------------------------------------------------------------------
# transcript - single source of truth for wording and timing
# ---------------------------------------------------------------------------
BEATS: dict[str, tuple[str, float]] = {
    's01.b1': ('Here is a problem twenty thousandth of a million Chinese students met in 2008. Most handed in a blank page.', 7.0),
    's01.b2': ('Prove that for every x and a greater than zero, this expression is trapped between one and two.', 6.3),
    's01.b3': ('I will take it apart completely. Nothing skipped, nothing assumed.', 3.5),
    's01.b4': ('Seventeen minutes. Twenty seven scenes. Every step on screen.', 3.2),
    's01.b5': ('First we build the toolkit, because the proof leans on four ideas.', 4.2),
    's01.b6': ('The function, the integral, the arithmetic geometric mean, and Cauchy Schwarz. Here we go.', 4.9),
    's02.b1': ('Before attacking it, let me show you why the obvious attack does not work.', 4.9),
    's02.b2': ('Push x right. The blue term collapses. The purple term climbs to meet it.', 4.9),
    's02.b3': ('Two terms, one variable, opposite directions. No single monotonicity to exploit.', 3.9),
    's02.b4': ('That is the whole difficulty. It is not that the algebra is ugly. It is that the terms are fighting each other.', 7.7),
    's02.b5': ('So we need a substitution that makes them stop fighting.', 3.5),
    's03.b1': ('Our whole problem lives inside one function. Let us meet it.', 3.9),
    's03.b2': ('Phi of t equals one over square root of one plus t, for t positive.', 5.3),
    's03.b3': ('Two facts matter. It never exceeds one, because the square root of one plus t is at least one.', 6.7),
    's03.b4': ('And it decreases, but slowly. It dies like one over the square root of t, and slow decay is what makes this dangerous.', 8.1),
    's03.b5': ('Keep that picture. A function that starts at one and dies slowly is hard to sum.', 5.6),
    's04.b1': ('Why care about area? Because comparisons of area prove inequalities with no algebra.', 4.6),
    's04.b2': ('An integral is accumulated area, built from rectangles. Twice as many, four, eight, sixteen.', 4.9),
    's04.b3': ('In the limit the rectangles become the region, and the region becomes a number: the integral.', 5.6),
    's04.b2b': ('The integral of one over square root of one plus t, from zero to one, is two root two minus one.', 7.4),
    's04.b4': ('That is zero point eight two eight. The whole region fits strictly under the line y equals one.', 6.3),
    's04.b5': ('Phi never reaches its own starting height. Hold that thought. We are about to trade the square root away, and this picture tells us which way.', 9.0),
    's05.b1': ('Tool number one. I am not going to assume it. Let us prove it.', 4.9),
    's05.b2': ('Geometrically: in a right triangle, the altitude to the hypotenuse is at most half of it.', 5.6),
    's05.b3': ('Drop the altitude. It splits the hypotenuse into a and b, and its square is a times b.', 6.3),
    's05.b4': ('So root a b is at most a plus b over two. There is the arithmetic geometric mean, by geometry.', 7.0),
    's05.b5': ('Now prove it with calculus, because I want to be pedantic. Consider t plus one over t.', 6.0),
    's05.b6': ('Its minimum is at t equals one, and that minimum is two. Rearranged, a plus b is at least two root a b.', 8.1),
    's05.b7': ('Same inequality, two proofs. We need the three variable version.', 3.5),
    's06.b1': ('The three variable form: A plus B plus C is at least three times the cube root of A B C.', 7.4),
    's06.b2': ('Equality exactly when A equals B equals C.', 2.8),
    's06.b3': ('Now plug in the constraint. The cube root of eight is two.', 4.2),
    's06.b4': ('Three times two is six. Remember the six. It appears twice in this proof, and both times it does real work.', 7.4),
    's07.b1': ('Tool number two. Convexity.', 2.2),
    's07.b2': ('A function is convex when its graph bends upward. The second derivative is positive, and ours always is.', 6.3),
    's07.b3': ('The consequence I want: a convex function lies above every one of its tangent lines. Draw any tangent, and the curve is above it everywhere.', 8.8),
    's07.b4': ('And as t goes to zero, Phi goes to one. From below. It never touches it.', 5.6),
    's07.b5': ('That limit is not attained. Remember it, because at the end I will show you the same thing happens to the whole sum.', 8.1),
    's08.b1': ('Tool number three. Cauchy Schwarz.', 2.2),
    's08.b2': ('Project u onto v. The projection can never be longer than the vector itself, so the leftover squared is non negative.', 7.4),
    's08.b3': ('Written down: the sum of two Phis, squared, is at most two times their sum of squares.', 6.0),
    's08.b4': ('For the form I need: two Phis, squared, is at most two times their sum of squares. And that sum simplifies: one plus A times one plus B is one plus s plus p.', 9.0),
    's08.b5': ('Hold on to that. In the hard part I will bound two of the three terms with exactly this, and I will need to know what it costs.', 9.0),
    's09.b1': ('Now the turn. That third term looks like a different animal from the other two.', 5.3),
    's09.b2': ('It is not. Divide the numerator and the denominator by a x.', 4.2),
    's09.b3': ('The a x cancels, and you get one over the square root of one plus eight over a x.', 6.7),
    's09.b4': ('Now define C as eight over a x. The third term is one over the square root of one plus C. The same function.', 8.4),
    's09.b5': ('So the whole expression is Phi of A, plus Phi of B, plus Phi of C. One function, three times.', 7.0),
    's09.b6': ('The asymmetry that made this look hostile was an illusion of notation.', 4.2),
    's10.b1': ('And the constraint transforms with it. A times B times C is exactly eight.', 4.9),
    's10.b2': ('So: three positive numbers, product eight, prove their Phi sum is between one and two.', 5.3),
    's10.b3': ('Notice the eight is not arbitrary. It is two cubed, so the geometric mean of the three numbers is two, and the natural centre is all three equal to two.', 9.0),
    's10.b4': ('And the second gift: the expression is now completely symmetric.', 3.5),
    's11.b1': ('Because it is symmetric, I am allowed to sort the three letters.', 4.2),
    's11.b2': ('Without loss of generality, A at most B at most C. Nothing is lost.', 4.9),
    's11.b3': ('Two consequences. A is at most two and C is at least two, because A cubed is at most A B C, which is eight.', 8.8),
    's11.b4': ('Flag that A is at most two. The entire upper bound hangs on it.', 4.9),
    's12.b1': ('Lower bound. Here is the trade I promised.', 2.8),
    's12.b2': ('For t positive, one plus t beats the square root of one plus t, so its reciprocal is smaller.', 6.7),
    's12.b3': ('So Phi of t is strictly bigger than one over one plus t. The blue curve is above the amber one.', 7.4),
    's12.b4': ('So we may push f down to a sum of rational functions. The trade is one sided, and it is in our favour.', 8.1),
    's13.b1': ('Now sum those, and ask when their sum is at least one.', 4.2),
    's13.b2': ('Clear the denominators. They are positive, so the inequality survives.', 3.5),
    's13.b3': ('Write S for A plus B plus C and Q for A B plus B C plus C A. The left side is three plus two S plus Q.', 9.0),
    's13.b4': ('The right side is one plus S plus Q plus A B C, and A B C is eight, so nine plus S plus Q.', 8.8),
    's13.b5': ('Three plus two S plus Q at least nine plus S plus Q. Every Q cancels.', 5.6),
    's13.b6': ('All that survives is S at least six. That is the whole content of the step.', 5.6),
    's13.b7': ('And six is exactly what AM-GM hands us, because the cube root of eight is two.', 5.6),
    's14.b1': ('So f is strictly greater than the rational sum, which is at least one. The lower bound is closed.', 6.7),
    's14.b2': ('Honest note: this proof has slack. At the symmetric point f is root three, about one point seven three, not one.', 7.4),
    's14.b3': ('We will not need it sharp. But you should know it is not.', 4.6),
    's15.b1': ('Lower bound done. Now the hard half: the upper bound.', 3.5),
    's15.b2': ('Before proving it, let me show you exactly where the danger lives.', 4.2),
    's15.b3': ('Send x and a towards zero, along the diagonal.', 3.2),
    's15.b4': ('The first two terms climb towards one each. The third term falls to zero. Watch the total.', 6.0),
    's15.b5': ('It approaches two from below, and it would cross two if we were careless.', 4.9),
    's15.b6': ('So the proof has to be sharp exactly here, in this corner. That rules out every comfortable estimate.', 6.3),
    's16.b1': ('Case one. Suppose A plus B is at least six.', 3.5),
    's16.b2': ('A is at most two, so B is at least six minus A, which is at least four.', 6.3),
    's16.b3': ('And since C is at least B, C is at least four too.', 4.6),
    's16.b4': ('Two terms are capped at one over root five, and the third is strictly below one.', 5.6),
    's16.b5': ('One plus two over root five is one point eight nine four, less than two, because two over root five is less than one. That is just four less than five.', 9.0),
    's17.b1': ('Case two. A plus B is less than six. This is the hard half.', 4.9),
    's17.b2': ('Set s to A plus B, and p to A B. Then C is eight over p, and the third term is exactly root p over p plus eight. No approximation at all.', 9.0),
    's17.b3': ('For the first two terms, all I have is Cauchy Schwarz.', 3.9),
    's17.b4': ('The case hypothesis caps the product: B is less than six minus A.', 4.6),
    's17.b5': ('On zero to two that parabola is increasing, and at A equals two it is exactly eight. So p is less than eight.', 8.1),
    's17.b6': ('Everything now hangs on one number, p, in the open interval zero to eight.', 4.9),
    's18.b1': ('Split on p, starting with p at most one. This is the delicate range.', 4.9),
    's18.b2': ('Here the Cauchy bound decreases as s grows, because the derivative has the sign of p minus one.', 6.3),
    's18.b3': ('So the bound is largest at the smallest s allowed, which is two root p. That evaluates to two over root one plus root p.', 8.8),
    's18.b4': ('Add the third term, put q equal to root p, and we need this. One line, for every q greater than zero.', 7.7),
    's18.b5': ('Three lines: rationalise, bound the root, and the remaining quadratic has negative discriminant.', 4.6),
    's18.b6': ('Notice how sharp that had to be. As p goes to zero the crude bound tends to two from the wrong side, so no rougher inequality would have worked.', 9.0),
    's19.b1': ('The other two sub-ranges are easy, because slack is available.', 3.5),
    's19.b2': ('Now the bound increases with s, and s is less than six, so plug six in.', 5.6),
    's19.b3': ('For one to three, that gives root two plus root three over eleven, which is one point nine three six.', 7.0),
    's19.b4': ('For three to eight, four over root ten plus one over root two, which is one point nine seven two.', 7.0),
    's19.b5': ('Both exact, not numerical. Sixty three beats forty four root two, and two point nine beats two root two.', 6.7),
    's19.b6': ('Nothing deep is happening here. The deep part was the lemma.', 3.9),
    's20.b1': ('Every case gives f less than two. Read the theorem.', 3.5),
    's20.b2': ('One less than f, less than two, for every positive x and a.', 4.6),
    's20.b3': ('Now let us look at it.', 2.2),
    's21.b1': ('Panel one. Instead of a surface in three dimensions, I want to show you its shadow, because the shadow tells the truth better.', 8.1),
    's21.b2': ('Here is the field. Both axes are logarithmic, because that is where the structure lives.', 5.3),
    's21.b3': ('Colour is the value of f. Teal near one, amber middle, coral near two.', 4.9),
    's21.b4': ('The thin curves are level sets. Read where the colour sits.', 3.9),
    's21.b5': ('Now the point of the whole picture. The scale bar runs from one to two.', 5.3),
    's21.b6': ('Not one pixel of this field is ever one, and not one pixel is ever two. The colour lives strictly between the two ends of the bar.', 9.0),
    's21.b7': ('A surface in three dimensions would have hidden this. As contours, you can check it yourself.', 5.6),
    's22.b1': ('Panel two. Fix a, and sweep x. Here a is two.', 3.9),
    's22.b2': ('The blue term collapses. The flat blue line is Phi of a, which does not move.', 5.6),
    's22.b3': ('The violet term rises to meet it. That is the opening fight, now with arithmetic attached.', 5.6),
    's22.b4': ('And the black total never leaves the shaded band between one and two.', 4.6),
    's22.b5': ('The dashed lines are the bounds. The curve gets close to the coral one when x is small, which is the corner we had to be careful about.', 9.0),
    's22.b6': ('Change a in the code and the picture changes, but the total stays inside. It has to.', 6.0),
    's23.b1': ('Panel three. The symmetric transformation, in coordinates where it is actually simple.', 4.2),
    's23.b2': ('On the left, take logarithms. The product constraint A B C equals eight becomes the plane ln A plus ln B plus ln C equals ln eight.', 9.0),
    's23.b3': ('A product constraint is a plane. That is the whole content of the substitution.', 4.9),
    's23.b4': ('The symmetric point A equals B equals C equals two is the origin of that plane.', 5.6),
    's23.b5': ('The heavy line is where C equals one.', 2.8),
    's23.b6': ('On the right, the same function on that surface. Same colours as panel one. It has no boundary, yet f still has a supremum, out at the corners.', 9.0),
    's24.b1': ('Panel four. Where do the two cases actually live?', 3.2),
    's24.b2': ('Here is the A B plane, with the ordering A at most B that we are allowed to assume.', 6.7),
    's24.b3': ('The line A plus B equals six splits it. Above and left, case one.', 4.9),
    's24.b4': ('The two hyperbolas split case two into the three sub-ranges, by the product p.', 4.9),
    's24.b5': ('And the region where p exceeds eight is empty inside case two, which is why we never had to consider it.', 7.4),
    's24.b6': ('So the case split was never mysterious. It is bookkeeping for where our estimates are sharp.', 5.6),
    's25.b1': ('Panel five. Ten thousand random positive pairs, sampled logarithmically.', 3.2),
    's25.b2': ('Minimum one point zero zero five seven. Maximum one point nine nine nine nine nine five.', 5.6),
    's25.b3': ('Mean one point five eight three. Variance zero point one one six.', 4.2),
    's25.b4': ('Not one sample at or below one. Not one sample at or above two.', 4.9),
    's25.b5': ('Look at the histogram. The samples crowd away from both ends.', 3.9),
    's25.b6': ('The closest approach to two was within five millionths. That is how tight it is.', 5.3),
    's25.b7': ('But let me be honest. Ten thousand samples is evidence, not proof. No amount of sampling proves a strict inequality. That is what the proof was for.', 9.0),
    's26.b1': ('One last picture, and it is the payoff.', 2.8),
    's26.b2': ('Send x and a to infinity. Two terms die, the third goes to one. So f approaches one.', 6.3),
    's26.b3': ('Send them to zero. Two terms go to one, the third dies. So f approaches two.', 5.6),
    's26.b4': ('The infimum is one and the supremum is two, and neither is ever attained.', 4.9),
    's26.b5': ('So writing one point zero zero zero one would be false. Writing one point nine nine nine nine would be false.', 7.4),
    's26.b6': ('Because neither limit is reached, the statement must use strict inequalities.', 3.9),
    's27.b1': ('That is the proof. Let us read it once, start to finish.', 4.2),
    's27.b2': ('Substitute, and the product constraint appears for free.', 2.8),
    's27.b3': ('The lower bound is the rational trade plus AM-GM.', 3.2),
    's27.b4': ('The upper bound splits on A plus B, then on the product. One lemma does the real work.', 6.3),
    's27.b5': ('The script for this video, and the checker that verifies every inequality in it, are both in the repository. Run them yourself.', 7.7),
}

NARRATION: dict[str, list[tuple[str, str, float]]] = {}
for _beat, (_line, _hold) in BEATS.items():
    NARRATION.setdefault(f"S{int(_beat[1:3])}", []).append((_beat, _line, _hold))
NARRATION = {k: NARRATION[k] for k in sorted(NARRATION, key=lambda s: int(s[1:]))}

SCENE_BUDGET: dict[str, list[float]] = {
    name: [dur for _, _, dur in lines] for name, lines in NARRATION.items()
}
TOTAL_NARRATION = round(sum(sum(v) for v in SCENE_BUDGET.values()), 3)


# ---------------------------------------------------------------------------
# precomputed evidence for the closing panels (seed 20080, matches
# verification/numerical_report.txt line for line)
# ---------------------------------------------------------------------------
_RNG = np.random.default_rng(20080)
SAMPLE_X = np.exp(_RNG.uniform(-12, 12, 10_000))
SAMPLE_A = np.exp(_RNG.uniform(-12, 12, 10_000))
SAMPLE_F = F2(SAMPLE_X, SAMPLE_A)
STATS = {
    "n": int(SAMPLE_F.size),
    "min": float(SAMPLE_F.min()),
    "max": float(SAMPLE_F.max()),
    "mean": float(SAMPLE_F.mean()),
    "var": float(SAMPLE_F.var()),
    "std": float(SAMPLE_F.std()),
    "median": float(np.median(SAMPLE_F)),
    "p1": float(np.percentile(SAMPLE_F, 1)),
    "p99": float(np.percentile(SAMPLE_F, 99)),
    "below": int((SAMPLE_F <= 1.0).sum()),
    "above": int((SAMPLE_F >= 2.0).sum()),
}
HIST, HIST_EDGES = np.histogram(SAMPLE_F, bins=26, range=(1.0, 2.0))


def fit_width(group: Mobject, limit: float = SAFE_X * 2) -> Mobject:
    if group.width > limit:
        group.scale_to_fit_width(limit)
    return group


def clamp_y(group: Mobject, top: float = STAGE_TOP, bot: float = STAGE_BOT) -> Mobject:
    if group.get_top()[1] > top:
        group.shift(DOWN * (group.get_top()[1] - top))
    if group.get_bottom()[1] < bot:
        group.shift(UP * (bot - group.get_bottom()[1]))
    return group


def clamp_x(group: Mobject, limit: float = SAFE_X) -> Mobject:
    if group.get_left()[0] < -limit:
        group.shift(RIGHT * (-limit - group.get_left()[0]))
    if group.get_right()[0] > limit:
        group.shift(LEFT * (group.get_right()[0] - limit))
    return group


def stage_fit(group: Mobject, limit_w: float = 12.6,
              limit_h: float = STAGE_TOP - STAGE_BOT) -> Mobject:
    """Shrink to fit the stage box, then clamp both axes.

    Both dimensions matter: constraining width alone lets a tall stack of
    formulas escape through the top of the frame, which is exactly the failure
    the layout audit exists to catch.
    """
    k = min(limit_w / max(group.width, 1e-6),
            limit_h / max(group.height, 1e-6),
            1.0)
    if k < 1.0:
        group.scale(k)
    clamp_y(group)
    clamp_x(group)
    return group


def title_bar(label: str, title: str) -> VGroup:
    tag = Text(label, font_size=FS_LABEL, color=MUTED, weight=BOLD)
    name = Text(title, font_size=FS_TITLE, color=INK, weight=BOLD)
    tag.next_to(name, LEFT, buff=0.34).align_to(name, UP)
    bar = VGroup(tag, name).arrange(RIGHT, buff=0.34)
    bar.to_edge(UP, buff=0.30)
    if bar.get_right()[0] > SAFE_X:
        bar.shift(LEFT * (bar.get_right()[0] - SAFE_X))
    return bar


def _wrap_caption(text: str, width: float, font_size: int) -> list[str]:
    """Greedy word wrap.

    ManimCE 0.21 dropped Text's ``word_wrap``/``width`` kwargs, so the line
    breaks are computed here from an average glyph width and then clamped by
    fit_width as a backstop.
    """
    per_line = max(12, int(width / (0.0092 * font_size)))
    lines: list[str] = []
    current = ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > per_line:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).strip()
    if current:
        lines.append(current)
    return lines


def caption_bar(text: str) -> VGroup:
    body = VGroup(*[
        Text(line, font_size=FS_CAPTION, color=INK) for line in
        _wrap_caption(text, CAPTION_W, FS_CAPTION)
    ]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fit_width(body, CAPTION_W)
    body.set_opacity(0.94)
    plate = RoundedRectangle(
        corner_radius=0.16,
        width=body.width + 0.72,
        height=body.height + 0.52,
        stroke_color=GRID,
        stroke_width=1.2,
        fill_color=CARD,
        fill_opacity=0.82,
    )
    plate.move_to(body.get_center())
    return VGroup(plate, body).move_to([0.0, CAPTION_Y, 0.0])


def card(contents: Mobject, width: float = 11.4, color: str = GRID) -> VGroup:
    plate = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=contents.height + 0.86,
        stroke_color=color,
        stroke_width=1.6,
        fill_color=CARD,
        fill_opacity=0.92,
    )
    plate.move_to(contents.get_center())
    return VGroup(plate, contents)


def key_idea(tex: str, color: str = AMBER, size: int = FS_WORK) -> VGroup:
    label = Text("KEY IDEA", font_size=FS_MICRO, color=color, weight=BOLD)
    body = MathTex(tex, font_size=size, color=INK)
    inner = VGroup(label, body).arrange(DOWN, buff=0.16)
    plate = RoundedRectangle(
        corner_radius=0.16,
        width=inner.width + 0.9,
        height=inner.height + 0.62,
        stroke_color=color,
        stroke_width=1.6,
        fill_color=color,
        fill_opacity=0.10,
    )
    plate.move_to(inner.get_center())
    return VGroup(plate, inner)


def note(text: str, size: int = FS_MICRO, color: str = MUTED) -> VGroup:
    body = VGroup(*[
        Text(line, font_size=size, color=color)
        for line in _wrap_caption(text, 12.2, size)
    ]).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
    return fit_width(body, 12.2)


def vchain(parts: list, buff: float = 0.34) -> VGroup:
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def vstack(parts: list, buff: float = 0.30, aligned: str = "LEFT") -> VGroup:
    return VGroup(*parts).arrange(DOWN, buff=buff, aligned_edge=aligned)


def strike(target: Mobject, color: str = MUTED) -> Line:
    line = Line(
        target.get_corner(UL),
        target.get_corner(DR),
        stroke_width=2.0,
        color=color,
    )
    return line


def frame_00() -> VGroup:
    return VGroup()


def frame_01() -> VGroup:
    head = Text("2008 Jiangxi Gaokao  ·  Q22", font_size=FS_LABEL,
                color=MUTED, weight=BOLD)
    verdict = verdict_tex(r"f(x,a)", 76)
    domain = MathTex(r"x,\,a\;>\;0", font_size=FS_WORK, color=MUTED)
    expr = MathTex(
        r"f(x,a)=\frac{1}{\sqrt{1+x}}+\frac{1}{\sqrt{1+a}}"
        r"+\sqrt{\frac{ax}{ax+8}}",
        font_size=40,
        color=INK,
    )
    foot = Text("a 17-minute proof  ·  every step on screen",
                font_size=FS_LABEL, color=MUTED)
    stack = VGroup(head, verdict, domain, expr, foot).arrange(DOWN, buff=0.30)
    stage_fit(stack, 12.0)
    stack.move_to([0.0, 0.15, 0.0])
    return stack


def frame_02() -> VGroup:
    head = title_bar("01  HOOK", "Why the obvious attack fails")
    left = Axes(
        x_range=[0, 40, 10], y_range=[0, 1.1, 0.5],
        x_length=3.5, y_length=2.5,
        axis_config={"include_ticks": False, "stroke_color": GRID, "stroke_width": 2},
        tips=False,
    )
    right = left.copy()
    left.move_to([-4.3, -0.15, 0.0])
    right.move_to([2.1, -0.15, 0.0])
    c1 = left.plot(lambda t: PHI(min(t, 1e9)), x_range=[0, 40], color=BLUE, stroke_width=4)
    c2 = right.plot(lambda t: np.sqrt(2 * min(t, 1e9) / (2 * min(t, 1e9) + 8)),
                    x_range=[0, 40], color=VIOLET, stroke_width=4)
    l1 = Text("first term", font_size=FS_MICRO, color=BLUE).next_to(c1, UP, buff=0.14)
    l2 = Text("third term", font_size=FS_MICRO, color=VIOLET).next_to(c2, DOWN, buff=0.14)
    clash = MathTex(r"\longleftarrow\ \text{fight}\ \longrightarrow", font_size=FS_LABEL,
                    color=CORAL)
    clash.move_to([-1.1, 1.35, 0.0])
    tail = MathTex(r"x\uparrow\ \Rightarrow\ \phi(x)\downarrow,\quad"
                   r"\sqrt{\tfrac{ax}{ax+8}}\uparrow", font_size=FS_WORK, color=MUTED)
    tail.move_to([0.0, -1.95, 0.0])
    stage_fit(VGroup(head, left, right, c1, c2, l1, l2, clash, tail), 13.4)
    return VGroup(head, left, right, c1, c2, l1, l2, clash, tail)


def frame_03() -> VGroup:
    head = title_bar("02  TOOLKIT", "The one function we live inside")
    ax = Axes(
        x_range=[0, 12, 3], y_range=[0, 1.1, 0.25],
        x_length=8.2, y_length=4.3,
        axis_config={"stroke_color": GRID, "stroke_width": 2.4,
                     "include_tip": False},
    )
    ax.move_to([-1.2, 0.05, 0.0])
    curve = ax.plot(lambda t: PHI(t), x_range=[0, 12], color=BLUE, stroke_width=5)
    band = ax.plot(lambda t: PHI(t), x_range=[0, 1], color=BLUE, stroke_width=16)
    band.set_opacity(0.18)
    dot = Dot(ax.c2p(0, 1.0), color=TEAL, radius=0.07)
    guide = DashedLine(ax.c2p(0, 1.0), ax.c2p(4.6, 1.0), color=TEAL,
                       stroke_width=2, dash_length=0.12)
    lbl = Text("phi(0) = 1", font_size=FS_LABEL, color=TEAL)
    lbl.next_to(dot, RIGHT, buff=0.16)
    asym = MathTex(r"\phi(t)\sim t^{-1/2}", font_size=FS_WORK, color=AMBER)
    asym.move_to([4.35, 1.75, 0.0])
    slow = Text("dies slowly", font_size=FS_MICRO, color=MUTED)
    slow.next_to(asym, DOWN, buff=0.12)
    xlab = Text("t", font_size=FS_LABEL, color=MUTED).next_to(ax, DOWN, buff=0.14)
    return stage_fit(VGroup(head, ax, curve, band, dot, guide, lbl, asym, slow, xlab))


def frame_04() -> VGroup:
    head = title_bar("02  TOOLKIT", "An integral is accumulated area")
    ax = Axes(
        x_range=[0, 1, 0.25], y_range=[0, 1.15, 0.25],
        x_length=5.0, y_length=4.3,
        axis_config={"stroke_color": GRID, "stroke_width": 2.4, "include_tip": False},
    )
    ax.move_to([-3.4, 0.0, 0.0])
    curve = ax.plot(lambda t: PHI(t), x_range=[0, 1], color=BLUE, stroke_width=5)
    region = ax.get_area(curve, x_range=(0, 1), color=TEAL, opacity=0.22)
    ceil = DashedLine(ax.c2p(0, 1.0), ax.c2p(1, 1.0), color=CORAL,
                      stroke_width=2.6, dash_length=0.12)
    clbl = Text("y = 1", font_size=FS_MICRO, color=CORAL).next_to(ceil, UP, buff=0.10)
    bars = VGroup(*[
        ax.get_riemann_rectangles(curve, x_range=(0, 1), dx=1.0 / 16, color=BLUE,
                                  fill_opacity=0.30, stroke_width=0)
        for _ in range(1)
    ])
    val = MathTex(r"\int_0^1\frac{dt}{\sqrt{1+t}}=2(\sqrt2-1)\approx0.828",
                  font_size=FS_WORK, color=INK)
    val.move_to([3.1, 1.55, 0.0])
    side = VGroup(
        Text("the whole region fits", font_size=FS_LABEL, color=INK),
        Text("strictly under y = 1", font_size=FS_LABEL, color=CORAL),
        Text("so phi never reaches 1", font_size=FS_LABEL, color=TEAL),
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    side.move_to([3.1, -0.35, 0.0])
    return stage_fit(VGroup(head, ax, curve, region, bars, ceil, clbl, val, side))


def frame_05() -> VGroup:
    head = title_bar("02  TOOLKIT", "AM-GM, proved twice")
    left = VGroup()
    circ = Circle(radius=1.45, color=GRID, stroke_width=2.4).move_to([-4.1, 0.5, 0])
    left.add(circ)
    left.add(Line([-5.55, 0.5, 0], [-2.65, 0.5, 0], color=MUTED, stroke_width=2))
    left.add(Line([-4.1, 0.5, 0], [-5.15, -0.75, 0], color=BLUE, stroke_width=3.4))
    left.add(Line([-4.1, 0.5, 0], [-3.05, -0.75, 0], color=VIOLET, stroke_width=3.4))
    alt = DashedLine([-5.15, -0.75, 0], [-3.05, -0.75, 0], color=TEAL, stroke_width=2.4)
    left.add(alt)
    left.add(Text("a", font_size=FS_MICRO, color=BLUE).move_to([-4.7, -0.55, 0]))
    left.add(Text("b", font_size=FS_MICRO, color=VIOLET).move_to([-3.5, -0.55, 0]))
    left.add(Text("altitude = sqrt(ab)", font_size=FS_MICRO, color=TEAL)
             .next_to(alt, DOWN, buff=0.16))
    geo = MathTex(r"\sqrt{ab}\le\frac{a+b}{2}", font_size=FS_WORK, color=INK)
    geo.move_to([-4.1, -1.62, 0.0])
    left.add(geo)
    gtag = Text("GEOMETRIC", font_size=FS_MICRO, color=MUTED, weight=BOLD)
    gtag.next_to(geo, UP, buff=0.22)
    left.add(gtag)

    ax = Axes(
        x_range=[0.2, 5, 1], y_range=[0, 6, 2],
        x_length=4.6, y_length=3.3,
        axis_config={"stroke_color": GRID, "stroke_width": 2, "include_tip": False},
    )
    ax.move_to([3.5, 0.55, 0])
    g = ax.plot(lambda t: t + 1.0 / t, x_range=[0.2, 5], color=AMBER, stroke_width=4.4)
    mn = Dot(ax.c2p(1, 2), color=TEAL, radius=0.07)
    mg = DashedLine(ax.c2p(0.2, 2), ax.c2p(1, 2), color=TEAL, stroke_width=1.6)
    ml = Text("min = 2 at t = 1", font_size=FS_MICRO, color=TEAL)
    ml.next_to(mn, RIGHT, buff=0.14)
    ana = MathTex(r"t+\tfrac1t\ge2\ \Longrightarrow\ a+b\ge2\sqrt{ab}",
                  font_size=32, color=INK)
    ana.move_to([3.5, -1.62, 0.0])
    atag = Text("ANALYTIC", font_size=FS_MICRO, color=MUTED, weight=BOLD)
    atag.next_to(ana, UP, buff=0.22)
    right = VGroup(ax, g, mn, mg, ml, ana, atag)
    grp = VGroup(left, right)
    return stage_fit(VGroup(head, grp))


def frame_06() -> VGroup:
    head = title_bar("02  TOOLKIT", "Three numbers: the form we will use")
    main = MathTex(r"A+B+C\ \ge\ 3\sqrt[3]{ABC}", font_size=60, color=INK)
    eq = Text("equality exactly when A = B = C", font_size=FS_LABEL, color=TEAL)
    eq.next_to(main, DOWN, buff=0.26)
    sub = MathTex(r"\sqrt[3]{8}=2\qquad\Longrightarrow\qquad A+B+C\ \ge\ 3\cdot2=6",
                  font_size=44, color=AMBER)
    note6 = Text("remember the 6 — it appears twice, and it earns its keep twice",
                 font_size=FS_LABEL, color=MUTED)
    grp = VGroup(main, eq, sub, note6).arrange(DOWN, buff=0.34)
    grp.move_to([0.0, 0.15, 0.0])
    return stage_fit(VGroup(head, grp))


def frame_07() -> VGroup:
    head = title_bar("02  TOOLKIT", "Convexity: bending upward")
    ax = Axes(
        x_range=[0, 10, 2], y_range=[0, 1.15, 0.25],
        x_length=5.4, y_length=3.7,
        axis_config={"stroke_color": GRID, "stroke_width": 2.2, "include_tip": False},
    )
    ax.move_to([-3.7, 0.15, 0])
    curve = ax.plot(lambda t: PHI(t), x_range=[0, 10], color=AMBER, stroke_width=5)
    t0 = 3.0
    slope = -0.5 * (1 + t0) ** -1.5
    tang = ax.plot(lambda t: PHI(t0) + slope * (t - t0), x_range=[0, 10],
                   color=CORAL, stroke_width=2.6)
    th = ax.plot(lambda t: PHI(t0) + slope * (t - t0), x_range=[0, 3.0],
                 color=CORAL, stroke_width=6)
    th.set_opacity(0.5)
    l1 = Text("curve above every tangent", font_size=FS_MICRO, color=TEAL)
    l1.next_to(tang, UP, buff=0.16).shift(LEFT * 0.4)
    l2 = Text("tangent line", font_size=FS_MICRO, color=CORAL)
    l2.next_to(ax.c2p(8, PHI(8) + slope * 5), RIGHT, buff=0.10)
    dd = MathTex(r"\phi''(t)=\tfrac34(1+t)^{-5/2}>0", font_size=32, color=MUTED)
    dd.move_to([3.5, 1.35, 0.0])
    side = VGroup(
        Text("as t → 0", font_size=FS_LABEL, color=MUTED),
        MathTex(r"\phi(t)\to1", font_size=44, color=TEAL),
        Text("from below, never touching", font_size=FS_MICRO, color=MUTED),
    ).arrange(DOWN, buff=0.16)
    side.move_to([3.5, -0.75, 0.0])
    return stage_fit(VGroup(head, ax, curve, tang, th, l1, l2, dd, side))


def frame_08() -> VGroup:
    head = title_bar("02  TOOLKIT", "Cauchy-Schwarz: the projection bound")
    o = np.array([0.0, 0.0, 0.0])
    u = np.array([1.55, 1.15, 0.0])
    v = np.array([2.25, -0.35, 0.0])
    ua, va = Arrow(o, u, buff=0, color=BLUE, stroke_width=5,
                   max_tip_length_to_length_ratio=0.09)
    vv = Arrow(o, v, buff=0, color=VIOLET, stroke_width=5,
               max_tip_length_to_length_ratio=0.09)
    proj_len = float(np.dot(u, v) / np.linalg.norm(v))
    ph = v / np.linalg.norm(v) * proj_len
    perp = u - ph
    dashed = DashedLine(o, ph, color=TEAL, stroke_width=3, dash_length=0.1)
    left = VGroup(ua, vv, dashed, Line(ph, u, color=CORAL, stroke_width=4))
    lu = Text("u", font_size=FS_LABEL, color=BLUE).next_to(ua.get_end(), RIGHT, buff=0.08)
    lv = Text("v", font_size=FS_LABEL, color=VIOLET).next_to(vv.get_end(), RIGHT, buff=0.08)
    lproj = Text("projection", font_size=FS_MICRO, color=TEAL)
    lproj.next_to(dashed, DOWN, buff=0.16)
    lperp = Text("leftover ≥ 0", font_size=FS_MICRO, color=CORAL)
    lperp.next_to(Line(ph, u), UP, buff=0.14)
    leftgrp = VGroup(left, lu, lv, lproj, lperp)
    leftgrp.move_to([-3.9, 0.15, 0.0])
    lines = VGroup(
        MathTex(r"\bigl(\phi(A)+\phi(B)\bigr)^2\le 2\left(\tfrac1{1+A}+\tfrac1{1+B}\right)",
                font_size=36, color=INK),
        MathTex(r"(1+A)(1+B)=1+s+p,\qquad s=A+B,\ p=AB", font_size=36, color=AMBER),
        MathTex(r"\phi(A)+\phi(B)\ \le\ \sqrt{\frac{2(2+s)}{1+s+p}}", font_size=40,
                color=TEAL),
    ).arrange(DOWN, buff=0.42)
    lines.move_to([2.9, 0.15, 0.0])
    return stage_fit(VGroup(head, leftgrp, lines))


def frame_09() -> VGroup:
    head = title_bar("03  SUBSTITUTION", "The third term was never a third term")
    top = MathTex(r"\sqrt{\frac{ax}{ax+8}}", font_size=64, color=VIOLET)
    mid = MathTex(r"=\ \sqrt{\frac{1}{1+\frac{8}{ax}}}\ =\ \frac{1}{\sqrt{1+C}}",
                  font_size=44, color=INK)
    defn = MathTex(r"C:=\frac{8}{ax}", font_size=36, color=AMBER)
    whole = MathTex(
        r"f=\phi(A)+\phi(B)+\phi(C),\qquad A=x,\ B=a,\ C=\frac{8}{AB}",
        font_size=40, color=INK,
    )
    grp = VGroup(top, mid, defn, whole).arrange(DOWN, buff=0.36)
    grp.move_to([0.0, 0.15, 0.0])
    return stage_fit(VGroup(head, grp))


def frame_10() -> VGroup:
    head = title_bar("03  SUBSTITUTION", "The real problem: three numbers, product eight")
    inner = VGroup(
        MathTex(r"A,B,C>0,\qquad ABC=8", font_size=44, color=AMBER),
        verdict_tex(r"\phi(A)+\phi(B)+\phi(C)", 48),
    ).arrange(DOWN, buff=0.34)
    box = card(inner, 11.6)
    why = Text("8 = 2³ — three terms, each naturally centred at 2",
               font_size=FS_LABEL, color=MUTED)
    why.next_to(box, DOWN, buff=0.32)
    gift = Text("and the problem just became symmetric — a gift we are about to spend",
                font_size=FS_LABEL, color=VIOLET)
    gift.next_to(why, DOWN, buff=0.16)
    grp = VGroup(box, why, gift)
    grp.move_to([0.0, 0.2, 0.0])
    return stage_fit(VGroup(head, grp))


def frame_11() -> VGroup:
    head = title_bar("03  SUBSTITUTION", "Symmetry buys an ordering")
    chips = VGroup()
    for i, (nm, col) in enumerate([("A", BLUE), ("B", BLUE), ("C", BLUE)]):
        c = VGroup(
            RoundedRectangle(corner_radius=0.14, width=1.5, height=1.5,
                             stroke_color=col, stroke_width=2.4,
                             fill_color=col, fill_opacity=0.12),
            MathTex(nm, font_size=44, color=col),
        )
        c.move_to([-3.1 + 3.1 * i, 1.55, 0.0])
        chips.add(c)
    swapnote = Text("the expression cannot tell them apart", font_size=FS_MICRO,
                    color=MUTED)
    swapnote.next_to(chips, DOWN, buff=0.24)
    wlog = MathTex(r"\mathrm{WLOG}\quad A\le B\le C", font_size=44, color=TEAL)
    wlog.move_to([0.0, -0.55, 0.0])
    cons = VGroup(
        MathTex(r"A\le2", font_size=40, color=AMBER),
        MathTex(r"2\le C", font_size=40, color=AMBER),
    ).arrange(RIGHT, buff=1.5)
    cons.move_to([0.0, -1.85, 0.0])
    why = Text("from A³ ≤ ABC = 8", font_size=FS_MICRO, color=MUTED)
    why.next_to(cons, DOWN, buff=0.16)
    grp = VGroup(chips, swapnote, wlog, cons, why)
    return stage_fit(VGroup(head, grp))


def frame_12() -> VGroup:
    head = title_bar("04  LOWER BOUND", "Trade the square root for a rational function")
    ax = Axes(
        x_range=[0, 9, 3], y_range=[0, 1.15, 0.25],
        x_length=6.2, y_length=4.0,
        axis_config={"stroke_color": GRID, "stroke_width": 2.2, "include_tip": False},
    )
    ax.move_to([-3.1, 0.1, 0])
    c1 = ax.plot(lambda t: PHI(t), x_range=[0, 9], color=BLUE, stroke_width=5)
    c2 = ax.plot(lambda t: 1.0 / (1.0 + t), x_range=[0, 9], color=AMBER, stroke_width=4)
    l1 = Text("phi(t)", font_size=FS_LABEL, color=BLUE).next_to(c1, UP, buff=0.14)
    l2 = Text("1/(1+t)", font_size=FS_LABEL, color=AMBER).next_to(c2, DOWN, buff=0.16)
    reason = VGroup(
        Text("for t > 0 :", font_size=FS_LABEL, color=MUTED),
        MathTex(r"1+t>\sqrt{1+t}", font_size=36, color=INK),
        MathTex(r"\Longrightarrow\ \frac{1}{\sqrt{1+t}}>\frac{1}{1+t}",
                font_size=40, color=TEAL),
    ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    reason.move_to([3.4, 0.15, 0.0])
    gain = Text("and this trade is strictly in our favour", font_size=FS_MICRO,
                color=VIOLET)
    gain.next_to(reason, DOWN, buff=0.26)
    return stage_fit(VGroup(head, ax, c1, c2, l1, l2, reason, gain))


def frame_13() -> VGroup:
    head = title_bar("04  LOWER BOUND", "Clear denominators — watch it collapse")
    l1 = MathTex(r"\frac1{1+A}+\frac1{1+B}+\frac1{1+C}\ \ge\ 1", font_size=44, color=INK)
    l2 = MathTex(r"(1+B)(1+C)+(1+A)(1+C)+(1+A)(1+B)\ \ge\ (1+A)(1+B)(1+C)",
                 font_size=32, color=MUTED)
    l3 = MathTex(r"3+2S+Q\ \ge\ 1+S+Q+ABC", font_size=40, color=INK)
    l4 = MathTex(r"3+2S+Q\ \ge\ 1+S+Q+8", font_size=40, color=AMBER)
    l5 = MathTex(r"A+B+C\ \ge\ 6", font_size=54, color=AMBER)
    defs = Text("S = A+B+C ,  Q = AB+BC+CA", font_size=FS_MICRO, color=MUTED)
    body = VGroup(l1, l2, l3, l4, l5).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    defs.next_to(body, DOWN, buff=0.18).align_to(body, RIGHT)
    amg = MathTex(r"A+B+C\ \ge\ 3\sqrt[3]{ABC}=3\cdot2=6", font_size=38, color=TEAL)
    amg.next_to(body, DOWN, buff=0.30)
    grp = VGroup(head, body, defs, amg)
    stage_fit(grp)
    grp.move_to([0.0, 0.15, 0.0])
    return grp


def frame_14() -> VGroup:
    head = title_bar("04  LOWER BOUND", "Lower bound closed")
    chain = vchain([
        MathTex(r"f", font_size=52, color=INK),
        MathTex(r">", font_size=52, color=TEAL),
        MathTex(r"\tfrac1{1+A}+\tfrac1{1+B}+\tfrac1{1+C}", font_size=44, color=INK),
        MathTex(r"\ge\ 1", font_size=52, color=AMBER),
    ])
    ring = Circle(radius=0.24, color=TEAL, stroke_width=3).move_to(chain[1].get_center())
    verdict = MathTex(r"f\;>\;1", font_size=64, color=TEAL)
    verdict.next_to(chain, DOWN, buff=0.55)
    honesty = Text("slack to spare: at A=B=C=2 we get f = sqrt 3 ≈ 1.73, not 1",
                   font_size=FS_LABEL, color=MUTED)
    honesty.next_to(verdict, DOWN, buff=0.24)
    grp = VGroup(head, chain, ring, verdict, honesty)
    grp.move_to([0.0, 0.2, 0.0])
    return stage_fit(grp)



FRAME_BUILDERS = {
    "S0": frame_00,
    "S1": frame_01,
    "S2": frame_02,
    "S3": frame_03,
    "S4": frame_04,
    "S5": frame_05,
    "S6": frame_06,
    "S7": frame_07,
    "S8": frame_08,
    "S9": frame_09,
    "S10": frame_10,
    "S11": frame_11,
    "S12": frame_12,
    "S13": frame_13,
    "S14": frame_14,
}


def verdict_tex(body: str, size: int) -> MathTex:
    """1 < body < 2, with the two bounds already coloured.

    MathTex emits one submobject per LaTeX *argument*, so the bounds must be
    passed as separate arguments to be addressable at all.
    """
    out = MathTex("1", r"\,<\,", body, r"\,<\,", "2", font_size=size, color=INK)
    out[0].set_color(TEAL)
    out[4].set_color(CORAL)
    return out


def frame_of(name: str) -> VGroup:
    """Rebuild the closing picture of ``name`` from scratch."""
    builder = FRAME_BUILDERS.get(name)
    return builder() if builder else VGroup()


def previous_section(name: str) -> str | None:
    index = int(name[1:])
    return f"S{index - 1}" if index > 1 else None


# ---------------------------------------------------------------------------
# colour ramps and scalar fields for the picture panels
# ---------------------------------------------------------------------------
def _rgb(value: str) -> np.ndarray:
    return np.array([int(value[i:i + 2], 16) / 255.0 for i in (1, 3, 5)])


_RAMP = (_rgb(TEAL), _rgb(AMBER), _rgb(CORAL))


def _ramp(t: np.ndarray) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    out = np.empty(t.shape + (3,), dtype=float)
    low = t < 0.5
    out[low] = _RAMP[0] + (_RAMP[1] - _RAMP[0]) * (t[low] / 0.5)[..., None]
    out[~low] = _RAMP[1] + (_RAMP[2] - _RAMP[1]) * ((t[~low] - 0.5) / 0.5)[..., None]
    return out


def _rgba(rgb: np.ndarray) -> np.ndarray:
    alpha = np.full(rgb.shape[:2] + (1,), 255, dtype=np.uint8)
    return np.dstack([(np.clip(rgb, 0.0, 1.0) * 255).astype(np.uint8), alpha])


def _domain_image(n: int = 260, lo: float = -3.2, hi: float = 3.2) -> np.ndarray:
    grid = np.exp(np.linspace(lo, hi, n))
    X, Y = np.meshgrid(grid, grid)
    return _rgba(_ramp(F2(X, Y) - 1.0))[::-1]


def _logplane_image(n: int = 240) -> np.ndarray:
    la = np.linspace(-4.2, 4.2, n)
    lb = np.linspace(-4.2, 4.2, n)
    LA, LB = np.meshgrid(la, lb)
    LC = np.log(8.0) - LA - LB
    A, B, C = np.exp(LA), np.exp(LB), np.exp(LC)
    return _rgba(_ramp(F2(A, B) - 1.0))[::-1]


def _ramp_strip(height: int = 96) -> np.ndarray:
    t = np.linspace(0.0, 1.0, 256)
    row = _ramp(t)
    return _rgba(np.repeat(row[None, :, :], height, axis=0))


def _iso_segments(level: float, rows: int = 54,
                  lo: float = -3.2, hi: float = 3.4) -> list[tuple]:
    """Short segments along the level set ``f = level``, one row at a time."""
    out: list[tuple] = []
    probe = np.exp(np.linspace(lo, hi, 160))
    for xv in np.exp(np.linspace(lo, hi, rows)):
        v = F2(xv, probe) - level
        hits = np.where(np.sign(v[:-1]) * np.sign(v[1:]) < 0)[0]
        roots = []
        for i in hits:
            a0, a1, f0 = probe[i], probe[i + 1], v[i]
            for _ in range(34):
                mid = np.sqrt(a0 * a1)
                if (F2(xv, mid) - level) * f0 <= 0:
                    a1 = mid
                else:
                    a0 = mid
            roots.append((xv, float(np.sqrt(a0 * a1))))
        for j in range(0, len(roots) - 1, 2):
            out.append((roots[j], roots[j + 1]))
    return out


def _iso_group(level: float, color: str, width: float, opacity: float) -> VGroup:
    segs = _iso_segments(level)
    return VGroup(*[
        Line(np.array([p[0], p[1], 0.0]), np.array([q[0], q[1], 0.0]),
             color=color, stroke_width=width)
        for p, q in segs
    ]).set_opacity(opacity)


def _pow(k: int) -> MathTex:
    return MathTex(rf"10^{{{k}}}", font_size=FS_MICRO, color=MUTED)


# ---------------------------------------------------------------------------
# panel 1 - the scalar field over (x, a)
# ---------------------------------------------------------------------------
def panel_contour() -> VGroup:
    head = title_bar("05  PICTURES", "Panel 1 · the field, and the levels it never reaches")
    img = ImageMobject(_domain_image()).scale_to_fit_height(4.35)
    box = Rectangle(width=img.width + 0.12, height=img.height + 0.12,
                    stroke_color=GRID, stroke_width=2).move_to(img.get_center())
    field = Group(img, box).move_to([-1.85, 0.15, 0.0])
    contours = VGroup(*[
        _iso_group(level, INK, 1.3, 0.30) for level in
        (1.15, 1.3, 1.45, 1.6, 1.7, 1.8, 1.9)
    ]).move_to(field.get_center())
    contours.scale_to_fit_width(field.width).scale_to_fit_height(field.height)

    ticks = VGroup()
    for k in (-3, -2, -1, 0, 1, 2, 3):
        frac = (k + 3.2) / 6.4
        pos = field.get_left()[0] + frac * field.width
        ticks.add(Line([pos, field.get_bottom()[1], 0],
                       [pos, field.get_bottom()[1] - 0.11, 0],
                       color=GRID, stroke_width=1.5))
        lab = _pow(k)
        lab.move_to([pos, field.get_bottom()[1] - 0.33, 0])
        ticks.add(lab)
    xlab = MathTex(r"x", font_size=FS_LABEL, color=MUTED)
    xlab.next_to(ticks, DOWN, buff=0.16).align_to(field, RIGHT)
    ylab = MathTex(r"a", font_size=FS_LABEL, color=MUTED)
    ylab.next_to(field, LEFT, buff=0.20).align_to(field, UP)

    bar = ImageMobject(_ramp_strip()).scale_to_fit_height(4.35)
    bar.scale_to_fit_width(0.30).next_to(field, RIGHT, buff=0.95)
    barlab = VGroup()
    for value, col in ((1.0, TEAL), (1.5, AMBER), (2.0, CORAL)):
        m = MathTex(rf"{value:.1f}", font_size=FS_MICRO, color=col)
        m.move_to([bar.get_right()[0] + 0.42,
                   bar.get_center()[1] + (value - 1.5) * bar.height, 0.0])
        barlab.add(m)
    btitle = Text("value of f", font_size=FS_MICRO, color=MUTED)
    btitle.next_to(bar, UP, buff=0.14)
    never = VGroup(
        Text("no pixel of this field", font_size=FS_MICRO, color=INK),
        Text("is ever 1 or 2", font_size=FS_LABEL, color=TEAL),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    never.next_to(bar, DOWN, buff=0.34).align_to(bar, LEFT)
    return stage_fit(Group(head, field, contours, ticks, xlab, ylab,
                          bar, barlab, btitle, never))


# ---------------------------------------------------------------------------
# panel 2 - one slice, a fixed a, swept in x
# ---------------------------------------------------------------------------
def panel_slice(a_fixed: float = 2.0, xmax: float = 30.0) -> VGroup:
    head = title_bar("05  PICTURES", "Panel 2 · fix a, sweep x, watch the three terms add up")
    ax = Axes(x_range=[0, xmax, 5], y_range=[0, 2.05, 0.5], x_length=8.6, y_length=4.4,
              axis_config={"stroke_color": GRID, "stroke_width": 2.2,
                           "include_tip": False})
    ax.move_to([-1.5, 0.05, 0.0])
    band = Polygon(ax.c2p(0, 1), ax.c2p(xmax, 1), ax.c2p(xmax, 2), ax.c2p(0, 2),
                   stroke_width=0, fill_color=TEAL, fill_opacity=0.10).set_z_index(-1)
    lo = DashedLine(ax.c2p(0, 1), ax.c2p(xmax, 1), color=TEAL, stroke_width=2,
                    dash_length=0.14)
    hi = DashedLine(ax.c2p(0, 2), ax.c2p(xmax, 2), color=CORAL, stroke_width=2,
                    dash_length=0.14)
    t1 = ax.plot(lambda t: PHI(t), x_range=[0, xmax], color=BLUE, stroke_width=4.4)
    t3 = ax.plot(lambda t: np.sqrt(a_fixed * t / (a_fixed * t + 8.0)), x_range=[0, xmax],
                 color=VIOLET, stroke_width=4.4)
    t2 = DashedLine(ax.c2p(0, PHI(a_fixed)), ax.c2p(xmax, PHI(a_fixed)),
                    color=BLUE, stroke_width=2, dash_length=0.12)
    total = ax.plot(lambda t: F2(t, a_fixed), x_range=[0, xmax], color=INK, stroke_width=5)
    legend = VGroup(
        MathTex(r"\phi(x)", font_size=FS_MICRO, color=BLUE),
        MathTex(rf"\phi({a_fixed:g})", font_size=FS_MICRO, color=BLUE),
        MathTex(r"\sqrt{\tfrac{ax}{ax+8}}", font_size=FS_MICRO, color=VIOLET),
        MathTex(r"f", font_size=FS_MICRO, color=INK),
    ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    legend.next_to(ax, RIGHT, buff=0.30).align_to(ax, UP)
    side = VGroup(
        Text("the blue term collapses,", font_size=FS_MICRO, color=MUTED),
        Text("the violet term rises to meet it,", font_size=FS_MICRO, color=MUTED),
        Text("and the total never leaves the band", font_size=FS_LABEL, color=TEAL),
    ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    side.next_to(ax, DOWN, buff=0.30).align_to(ax, LEFT)
    return stage_fit(VGroup(head, ax, band, lo, hi, t1, t2, t3, total, legend, side))


# ---------------------------------------------------------------------------
# panel 3 - the constraint surface, straightened out by logarithms
# ---------------------------------------------------------------------------
def panel_logspace() -> VGroup:
    head = title_bar("05  PICTURES", "Panel 3 · the constraint ABC = 8, straightened")
    img = ImageMobject(_logplane_image()).scale_to_fit_height(4.2)
    box = Rectangle(width=img.width + 0.12, height=img.height + 0.12,
                    stroke_color=GRID, stroke_width=2).move_to(img.get_center())
    right = Group(img, box).move_to([2.6, 0.2, 0.0])
    rlab = VGroup(
        MathTex(r"\ln A", font_size=FS_MICRO, color=MUTED),
        MathTex(r"\ln B", font_size=FS_MICRO, color=MUTED),
    )
    rlab[0].next_to(right, UP, buff=0.14)
    rlab[1].next_to(right, LEFT, buff=0.20).align_to(right, DOWN)
    rtitle = Text("f on the surface", font_size=FS_MICRO, color=INK)
    rtitle.next_to(right, DOWN, buff=0.34)

    ax = Axes(x_range=[-4.2, 4.2, 2], y_range=[-4.2, 4.2, 2], x_length=5.2,
              y_length=4.2, axis_config={"stroke_color": GRID, "stroke_width": 2,
                                         "include_tip": False})
    ax.move_to([-3.4, 0.2, 0.0])
    centre = Dot(ax.c2p(0, 0), color=TEAL, radius=0.07)
    family = VGroup(*[
        ax.plot(lambda t, c=c: c - t, x_range=[-4.2, 4.2], color=GRID, stroke_width=1.4)
        for c in (-2.0, 0.0, 2.0)
    ])
    heavy = ax.plot(lambda t: np.log(8.0) - t, x_range=[-4.2, 4.2], color=AMBER,
                    stroke_width=3.4)
    hlab = MathTex(r"\ln A+\ln B=\ln 8\ \ (C=1)", font_size=FS_MICRO, color=AMBER)
    hlab.next_to(ax.c2p(1.6, np.log(8.0) - 1.6), UP, buff=0.14)
    clab = Text("A = B = C = 2", font_size=FS_MICRO, color=TEAL)
    clab.next_to(centre, DOWN, buff=0.20)
    ltitle = MathTex(r"\ln A+\ln B+\ln C=\ln 8", font_size=FS_LABEL, color=INK)
    ltitle.next_to(ax, UP, buff=0.22)
    lnote = Text("a product constraint is a plane in log-space",
                 font_size=FS_MICRO, color=MUTED)
    lnote.next_to(ax, DOWN, buff=0.34)
    return stage_fit(Group(head, ax, family, heavy, centre, clab, hlab, ltitle, lnote,
                          right, rlab, rtitle))


# ---------------------------------------------------------------------------
# panel 4 - the case split as a partition of the domain
# ---------------------------------------------------------------------------
def panel_cases() -> VGroup:
    head = title_bar("05  PICTURES", "Panel 4 · the case split is just a partition")
    ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=5.6, y_length=5.0,
              axis_config={"stroke_color": GRID, "stroke_width": 2.2,
                           "include_tip": False})
    ax.move_to([-3.1, 0.15, 0.0])
    case1 = Polygon(ax.c2p(0, 6), ax.c2p(3, 3), ax.c2p(6, 6),
                    stroke_width=2, stroke_color=TEAL, fill_color=TEAL,
                    fill_opacity=0.22)
    case2 = Polygon(ax.c2p(0, 0), ax.c2p(3, 3), ax.c2p(0, 6),
                    stroke_width=2, stroke_color=AMBER, fill_color=AMBER,
                    fill_opacity=0.20)
    split = DashedLine(ax.c2p(0, 6), ax.c2p(3, 3), color=INK, stroke_width=2.6,
                       dash_length=0.14)
    hyper = VGroup()
    for p, col in ((1.0, VIOLET), (3.0, VIOLET)):
        aa = np.linspace(0.02, min(3.0, p), 220)
        ok = aa + p / aa < 6.0
        aa = aa[ok]
        hyper.add(ax.plot(lambda t, p=p: p / t, x_range=[aa.min(), aa.max()],
                          color=col, stroke_width=2.4))
    c1 = Text("CASE 1", font_size=FS_LABEL, color=TEAL, weight=BOLD)
    c1.move_to(ax.c2p(4.6, 5.0))
    c1b = MathTex(r"A+B\ge6", font_size=FS_MICRO, color=TEAL)
    c1b.next_to(c1, DOWN, buff=0.12)
    c2 = Text("CASE 2", font_size=FS_LABEL, color=AMBER, weight=BOLD)
    c2.move_to(ax.c2p(0.95, 2.3))
    c2b = MathTex(r"A+B<6", font_size=FS_MICRO, color=AMBER)
    c2b.next_to(c2, DOWN, buff=0.12)
    plab = MathTex(r"AB=1", font_size=FS_MICRO, color=VIOLET)
    plab.next_to(ax.c2p(0.55, 1 / 0.55), RIGHT, buff=0.10)
    plab2 = MathTex(r"AB=3", font_size=FS_MICRO, color=VIOLET)
    plab2.next_to(ax.c2p(1.3, 3 / 1.3), RIGHT, buff=0.10)
    wlog = Text("shown for A ≤ B, the ordering we may assume", font_size=FS_MICRO,
                color=MUTED)
    wlog.next_to(ax, DOWN, buff=0.26)

    rows = VGroup(
        Text("p = AB ≤ 1        sharp lemma", font_size=FS_MICRO, color=AMBER),
        Text("1 < p ≤ 3        slack available", font_size=FS_MICRO, color=AMBER),
        Text("3 < p < 8        slack available", font_size=FS_MICRO, color=AMBER),
        Text("p = AB > 8       impossible when A + B < 6", font_size=FS_MICRO,
             color=MUTED),
    ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    rows.move_to([3.3, 0.35, 0.0])
    rtitle = Text("how Case 2 is split", font_size=FS_LABEL, color=INK)
    rtitle.next_to(rows, UP, buff=0.26).align_to(rows, LEFT)
    return stage_fit(VGroup(head, ax, case2, case1, split, hyper, c1, c1b, c2, c2b,
                            plab, plab2, wlog, rtitle, rows))


# ---------------------------------------------------------------------------
# panel 5 - the sampling evidence
# ---------------------------------------------------------------------------
def panel_stats() -> VGroup:
    head = title_bar("05  PICTURES", "Panel 5 · ten thousand samples, and what they cannot prove")
    rows = VGroup()
    for label, value, col in (
        ("samples", f"{STATS['n']:,}", INK),
        ("minimum f", f"{STATS['min']:.10f}", TEAL),
        ("maximum f", f"{STATS['max']:.10f}", CORAL),
        ("mean f", f"{STATS['mean']:.10f}", INK),
        ("variance", f"{STATS['var']:.10f}", INK),
    ):
        rows.add(VGroup(
            Text(label, font_size=FS_LABEL, color=MUTED),
            Text(value, font_size=FS_LABEL, color=col, weight=BOLD),
        ).arrange(RIGHT, buff=0.9, aligned_edge=LEFT))
    rows.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
    tbl = card(rows, 6.6)
    tbl.move_to([-4.0, 0.9, 0.0])

    counts = VGroup(*[
        Rectangle(width=0.155, height=float(c) / HIST.max() * 2.5,
                  stroke_width=0, fill_color=TEAL, fill_opacity=0.85)
        for c in HIST
    ])
    for i, bar in enumerate(counts):
        bar.move_to([-1.15 + 0.175 * i, -1.35 + bar.height / 2, 0.0])
    base = Line([-1.35, -1.35, 0], [3.45, -1.35, 0], color=GRID, stroke_width=2)
    span = HIST_EDGES[-1] - HIST_EDGES[0]
    left_edge = counts[0].get_left()[0]
    right_edge = counts[-1].get_right()[0]
    for value, col in ((1.0, TEAL), (2.0, CORAL)):
        pos = left_edge + (value - 1.0) / span * (right_edge - left_edge)
        marker = DashedLine([pos, -1.35, 0], [pos, 1.35, 0], color=col, stroke_width=2.2,
                            dash_length=0.12)
        lab = MathTex(rf"{value:.0f}", font_size=FS_MICRO, color=col)
        lab.move_to([pos, 1.55, 0.0])
        counts.add(marker, lab)
    htitle = Text("distribution of f over the samples", font_size=FS_LABEL, color=INK)
    htitle.move_to([1.0, 1.95, 0.0])
    hnote = Text(f"{STATS['below']} samples at or below 1     "
                 f"{STATS['above']} samples at or above 2",
                 font_size=FS_MICRO, color=MUTED)
    hnote.move_to([1.0, -1.95, 0.0])

    caveat = Text("evidence, not proof: the closest approach to 2 was within 5e-6",
                  font_size=FS_MICRO, color=VIOLET)
    caveat.next_to(tbl, DOWN, buff=0.34)
    return stage_fit(VGroup(head, tbl, caveat, htitle, base, counts, hnote))


# ---------------------------------------------------------------------------
# panel 6 - sharpness
# ---------------------------------------------------------------------------
def panel_sharp() -> VGroup:
    head = title_bar("05  PICTURES", "Panel 6 · both constants are optimal")
    left = VGroup(
        Text("x, a → +∞", font_size=FS_LABEL, color=MUTED),
        MathTex(r"\phi(x)\to0,\quad \phi(a)\to0,\quad"
                r"\sqrt{\tfrac{ax}{ax+8}}\to1", font_size=30, color=INK),
        MathTex(r"f\to1\ \text{from above}", font_size=40, color=TEAL),
    ).arrange(DOWN, buff=0.26)
    right = VGroup(
        Text("x, a → 0⁺", font_size=FS_LABEL, color=MUTED),
        MathTex(r"\phi(x)\to1,\quad \phi(a)\to1,\quad"
                r"\sqrt{\tfrac{ax}{ax+8}}\to0", font_size=30, color=INK),
        MathTex(r"f\to2\ \text{from below}", font_size=40, color=CORAL),
    ).arrange(DOWN, buff=0.26)
    pair = VGroup(left, right).arrange(RIGHT, buff=1.1)
    pair.move_to([0.0, 0.55, 0.0])
    verdict = MathTex(r"\inf f=1\qquad\sup f=2\qquad\text{neither attained}",
                      font_size=44, color=INK)
    verdict.next_to(pair, DOWN, buff=0.55)
    forced = VGroup(
        Text("so 1.0001 would be false, 1.9999 would be false,", font_size=FS_LABEL,
             color=MUTED),
        Text("and the statement must use strict inequalities", font_size=FS_LABEL,
             color=AMBER),
    ).arrange(DOWN, buff=0.16)
    forced.next_to(verdict, DOWN, buff=0.34)
    return stage_fit(VGroup(head, pair, verdict, forced))


# ---------------------------------------------------------------------------
# closing pictures for sections 15-27
# ---------------------------------------------------------------------------
def frame_15() -> VGroup:
    head = title_bar("05  UPPER BOUND", "First, where the danger lives")
    ax = Axes(x_range=[0, 12, 3], y_range=[0, 2.1, 0.5], x_length=6.4, y_length=4.3,
              axis_config={"stroke_color": GRID, "stroke_width": 2.2,
                           "include_tip": False})
    ax.move_to([-2.9, 0.1, 0.0])
    path = ax.plot(lambda t: t, x_range=[0.35, 2.02], color=VIOLET, stroke_width=4)
    mark = Dot(ax.c2p(1.1, 1.1), color=VIOLET, radius=0.09)
    top = DashedLine(ax.c2p(0, 2), ax.c2p(12, 2), color=CORAL, stroke_width=2.6,
                     dash_length=0.14)
    toplab = MathTex(r"f=2", font_size=FS_LABEL, color=CORAL)
    toplab.next_to(top, UP, buff=0.10)
    read = Text("f = 1.99...", font_size=FS_WORK, color=CORAL)
    read.move_to([2.6, 1.05, 0.0])
    warn = VGroup(
        Text("x, a → 0⁺", font_size=FS_LABEL, color=VIOLET),
        Text("the sum approaches 2 from below", font_size=FS_MICRO, color=MUTED),
        Text("and would cross it if we were careless", font_size=FS_MICRO, color=CORAL),
        Text("⇒ the proof must be sharp exactly here", font_size=FS_LABEL, color=AMBER),
    ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
    warn.move_to([2.6, -0.75, 0.0])
    return stage_fit(VGroup(head, ax, path, mark, top, toplab, read, warn))


def frame_16() -> VGroup:
    head = title_bar("05  UPPER BOUND", "Case 1 · A + B ≥ 6")
    bars = VGroup()
    for i, (nm, val, txt, col) in enumerate((
        ("A", 2.0, r"A\le2", TEAL),
        ("B", 4.0, r"B\ge6-A\ge4", BLUE),
        ("C", 4.0, r"C\ge B\ge4", BLUE),
    )):
        y = 1.85 - 1.15 * i
        base = Line([-6.3, y, 0], [-1.1, y, 0], color=GRID, stroke_width=2)
        full = Rectangle(width=5.2, height=0.30, stroke_width=0, fill_color=GRID,
                         fill_opacity=0.35).move_to([-3.7, y, 0])
        bar = Rectangle(width=5.2 * val / 6.0, height=0.30, stroke_width=0,
                        fill_color=col, fill_opacity=0.9).move_to(
            [-6.3 + 5.2 * val / 12.0, y, 0])
        lab = MathTex(nm, font_size=FS_LABEL, color=MUTED).move_to([-6.75, y, 0])
        val_ = MathTex(txt, font_size=FS_LABEL, color=col).move_to([-1.1 + 0.55, y, 0])
        bars.add(VGroup(base, full, bar, lab, val_))
    chain = VGroup(
        MathTex(r"f=\phi(A)+\phi(B)+\phi(C)", font_size=36, color=INK),
        MathTex(r"<\ 1+\tfrac{1}{\sqrt5}+\tfrac{1}{\sqrt5}", font_size=36, color=AMBER),
        MathTex(r"=1+\tfrac{2}{\sqrt5}=1.8944\ldots<2", font_size=36, color=TEAL),
    ).arrange(DOWN, buff=0.24)
    chain.move_to([3.6, 0.55, 0.0])
    why = Text("2/√5 < 1 because 4 < 5", font_size=FS_MICRO, color=MUTED)
    why.next_to(chain, DOWN, buff=0.26)
    return stage_fit(VGroup(head, bars, chain, why))


def frame_17() -> VGroup:
    head = title_bar("05  UPPER BOUND", "Case 2 · A + B < 6")
    known = VGroup(
        MathTex(r"\phi(C)=\sqrt{\tfrac{p}{p+8}}\ \ \text{exactly}", font_size=34,
                color=TEAL),
        MathTex(r"\phi(A)+\phi(B)\le\sqrt{\tfrac{2(2+s)}{1+s+p}}"
                r"\ \ \text{(Cauchy)}", font_size=34, color=BLUE),
        MathTex(r"p=AB<A(6-A)\le8\ \Rightarrow\ 0<p<8", font_size=34, color=AMBER),
    ).arrange(DOWN, buff=0.30)
    known.move_to([-3.3, 0.55, 0.0])
    master = card(MathTex(
        r"f<\sqrt{\tfrac{2(2+s)}{1+s+p}}+\sqrt{\tfrac{p}{p+8}}",
        font_size=40, color=INK), 7.0, AMBER)
    master.move_to([3.5, 1.35, 0.0])
    ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, 9, 2], x_length=3.4, y_length=2.6,
              axis_config={"stroke_color": GRID, "stroke_width": 1.8,
                           "include_tip": False})
    ax.move_to([3.4, -1.35, 0.0])
    par = ax.plot(lambda t: t * (6 - t), x_range=[0, 2], color=AMBER, stroke_width=4)
    pardot = Dot(ax.c2p(2, 8), color=CORAL, radius=0.08)
    parl = Text("peak 8 at A = 2", font_size=FS_MICRO, color=CORAL)
    parl.next_to(pardot, RIGHT, buff=0.10)
    return stage_fit(VGroup(head, known, master, ax, par, pardot, parl))


def frame_18() -> VGroup:
    head = title_bar("05  UPPER BOUND", "The sharp sub-case, and one lemma")
    mono = MathTex(r"\tfrac{d}{ds}\!\left[\tfrac{2+s}{1+s+p}\right]"
                   r"=\tfrac{p-1}{(1+s+p)^2}\le0\quad(p\le1)",
                   font_size=34, color=BLUE)
    atmin = MathTex(r"\Rightarrow\ \phi(A)+\phi(B)\le"
                    r"\sqrt{\tfrac{2(2+2\sqrt p)}{(1+\sqrt p)^2}}"
                    r"=\tfrac{2}{\sqrt{1+\sqrt p}}", font_size=34, color=INK)
    atmin.next_to(mono, DOWN, buff=0.26)
    lemma = card(VGroup(
        MathTex(r"\textbf{LEMMA}\quad"
                r"\frac{2}{\sqrt{1+q}}+\frac{q}{\sqrt{q^2+8}}<2"
                r"\quad\text{for every }q>0", font_size=40, color=INK)), 12.2, VIOLET)
    lemma.next_to(atmin, DOWN, buff=0.34)
    proof = VGroup(
        MathTex(r"2-\tfrac{2}{\sqrt{1+q}}=\tfrac{2q}{1+q+\sqrt{1+q}}"
                r"\quad\text{(rationalise)}", font_size=30, color=INK),
        MathTex(r"1+q+\sqrt{1+q}\le2+\tfrac32q"
                r"\quad\text{since }\sqrt{1+q}\le1+\tfrac q2", font_size=30, color=INK),
        MathTex(r"4(q^2+8)-(2+\tfrac32q)^2=\tfrac74q^2-6q+28>0"
                r"\quad(\Delta=-160<0)", font_size=30, color=TEAL),
    ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
    proof.next_to(lemma, DOWN, buff=0.30)
    return stage_fit(VGroup(head, mono, atmin, lemma, proof))


def frame_19() -> VGroup:
    head = title_bar("05  UPPER BOUND", "The rest of Case 2, where slack is available")
    header = VGroup(*[
        Text(t, font_size=FS_MICRO, color=MUTED, weight=BOLD)
        for t in ("sub-range", "first two terms", "third term", "total")
    ])
    header.arrange(RIGHT, buff=0.55, aligned_edge=UP)
    body = VGroup()
    specs = (
        (r"p\le1", r"\tfrac{2}{\sqrt{1+\sqrt p}}", r"\sqrt{\tfrac{p}{p+8}}",
         r"<2\ \text{(Lemma)}", TEAL),
        (r"1<p\le3", r"\sqrt2", r"\sqrt{\tfrac3{11}}", r"1.9364<2", AMBER),
        (r"3<p<8", r"\tfrac4{\sqrt{10}}", r"\tfrac1{\sqrt2}", r"1.9720<2", AMBER),
    )
    for a, b, c, d, col in specs:
        body.add(VGroup(
            MathTex(a, font_size=FS_MICRO, color=INK),
            MathTex(b, font_size=FS_MICRO, color=BLUE),
            MathTex(c, font_size=FS_MICRO, color=VIOLET),
            MathTex(d, font_size=FS_MICRO, color=col),
        ).arrange(RIGHT, buff=0.55, aligned_edge=UP))
    body.arrange(DOWN, buff=0.34, aligned_edge=UP)
    table = VGroup(header, body).arrange(DOWN, buff=0.30, aligned_edge=UP)
    exact = VGroup(
        Text("the last two rows are exact, not numerical:", font_size=FS_MICRO,
             color=MUTED),
        MathTex(r"63>44\sqrt2\ (3969>3872)", font_size=FS_MICRO, color=AMBER),
        MathTex(r"2.9>2\sqrt2\ (8.41>8)", font_size=FS_MICRO, color=AMBER),
    ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    exact.next_to(table, DOWN, buff=0.34).align_to(table, LEFT)
    whole = VGroup(table, exact)
    whole.move_to([0.0, 0.4, 0.0])
    return stage_fit(VGroup(head, whole))


def frame_20() -> VGroup:
    head = title_bar("05  UPPER BOUND", "Upper bound closed")
    verdict = verdict_tex(r"f(x,a)", 88)
    verdict.move_to([0.0, 0.75, 0.0])
    sub = MathTex(r"A=x,\quad B=a,\quad C=\tfrac{8}{AB},\quad ABC=8",
                  font_size=34, color=MUTED)
    sub.next_to(verdict, DOWN, buff=0.50)
    beat = Text("both bounds closed. now let us look at it.", font_size=FS_LABEL,
                color=VIOLET)
    beat.next_to(sub, DOWN, buff=0.28)
    return stage_fit(VGroup(head, verdict, sub, beat))


FRAME_BUILDERS.update({
    "S15": frame_15, "S16": frame_16, "S17": frame_17, "S18": frame_18,
    "S19": frame_19, "S20": frame_20, "S21": panel_contour, "S22": panel_slice,
    "S23": panel_logspace, "S24": panel_cases, "S25": panel_stats,
    "S26": panel_sharp,
})


def frame_27() -> VGroup:
    head = title_bar("05  CLOSE", "The whole proof on one screen")
    col = VGroup(
        MathTex(r"A=x,\ B=a,\ C=\tfrac{8}{AB}\ \Rightarrow\ ABC=8", font_size=32,
                color=AMBER),
        MathTex(r"f=\phi(A)+\phi(B)+\phi(C)", font_size=32, color=INK),
        MathTex(r"f>\tfrac1{1+A}+\tfrac1{1+B}+\tfrac1{1+C}\ge1\quad(A+B+C\ge6)",
                font_size=30, color=TEAL),
        MathTex(r"A+B\ge6:\ f<1+\tfrac2{\sqrt5}<2", font_size=30, color=BLUE),
        MathTex(r"A+B<6:\ p<8,\ \text{then }p\le1,\,1<p\le3,\,3<p<8",
                font_size=30, color=BLUE),
    ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    col.move_to([-0.4, 0.55, 0.0])
    verdict = verdict_tex("f", 64)
    verdict.next_to(col, DOWN, buff=0.40).align_to(col, RIGHT)
    foot = Text("verification/verify_math.py — 24/24 checks pass", font_size=FS_MICRO,
                color=MUTED)
    foot.next_to(col, DOWN, buff=0.70).align_to(col, LEFT)
    return stage_fit(VGroup(head, col, verdict, foot))


FRAME_BUILDERS["S27"] = frame_27


class Gaokao22Scene(Scene):
    """The whole movie, in twenty-seven chained sections."""

    def pause(self, seconds: float) -> None:
        """A narration beat; recorded so the budget assertion can check it."""
        self.wait(seconds)
        self._pause_log[-1].append(round(float(seconds), 3))

    def say(self, key: str) -> None:
        """Deliver one transcript line, as narration or as an on-screen caption."""
        text, dur = BEATS[key]
        if CAPTIONS:
            bar = caption_bar(text)
            self.add(bar)
            self.pause(dur)
            self.remove(bar)
        else:
            self.pause(dur)

    def finish(self, target: Mobject, *extras: Mobject) -> None:
        """Retire the working mobjects and leave exactly ``target`` on screen.

        Deliberately avoids the Transform family. Transform.clean_up_from_scene
        calls ``self.mobject[0].restore()``, and Mobject.become() then invokes
        interpolate_color on every family member. That method is abstract on
        Mobject and only implemented for VMobject, ImageMobject and
        PointCloudMobject, so transforming a container mobject raises
        "Please override in a child class" at cleanup time. Fading out and
        adding is visually equivalent here and cannot hit that path.
        """
        drops = [FadeOut(m) for m in extras if m in self.mobjects]
        body = [FadeOut(m) for m in self.mobjects if m not in extras]
        if drops or body:
            self.play(*drops, *body, run_time=0.8)
        self.add(target)
        self.wait(0.6)

    def construct(self) -> None:
        self._pause_log = []
        self.camera.background_color = BG
        if ONLY:
            self.run_section(ONLY.strip().upper())
            return
        for index in range(1, SECTION_COUNT + 1):
            self.next_section(f"S{index}")
            self._pause_log.append([])
            getattr(self, f"scene_{index}")()
        self.verify_budget()

    def run_section(self, name: str) -> None:
        """Render one section in isolation. Used by CI and by GAOKAO_ONLY=... ."""
        if not name.startswith("S"):
            name = f"S{name}"
        if not 1 <= int(name[1:]) <= SECTION_COUNT:
            raise SystemExit(f"unknown section {name!r}; expected S1..S{SECTION_COUNT}")
        self.next_section(name)
        self._pause_log = [[]]
        getattr(self, f"scene_{name[1:]}")()
        self.verify_budget(names=[name])

    def verify_budget(self, names: list[str] | None = None) -> None:
        """Fail loudly if the movie no longer matches the transcript."""
        selected = list(SCENE_BUDGET) if names is None else names
        if len(self._pause_log) != len(selected):
            raise AssertionError(
                f"ran {len(self._pause_log)} sections, expected {len(selected)}"
            )
        for name, logged in zip(selected, self._pause_log):
            if logged != SCENE_BUDGET[name]:
                raise AssertionError(
                    f"{name}: pauses {logged} != transcript {SCENE_BUDGET[name]}"
                )

    def scene_1(self) -> None:
        dots = VGroup(*[
            Dot(np.array([x, y, 0.0]), radius=0.011, color=GRID)
            for x in np.arange(-6.6, 6.7, 0.55)
            for y in np.arange(-2.2, 2.3, 0.55)
        ])
        self.add(dots)
        self.say("s01.b1")
        self.say("s01.b2")
        head = Text("2008 Jiangxi Gaokao  ·  Q22", font_size=FS_LABEL,
                    color=MUTED, weight=BOLD)
        verdict = verdict_tex(r"f(x,a)", 76)
        domain = MathTex(r"x,\,a\;>\;0", font_size=FS_WORK, color=MUTED)
        stack = VGroup(head, verdict, domain).arrange(DOWN, buff=0.28)
        stack.move_to([0.0, 0.55, 0.0])
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.7)
        self.play(Write(verdict), run_time=1.6)
        self.play(FadeIn(domain), run_time=0.5)
        self.say("s01.b3")
        self.play(Indicate(verdict, color=TEAL, scale_factor=1.03), run_time=1.0)
        self.say("s01.b4")
        expr = MathTex(
            r"f(x,a)=\frac{1}{\sqrt{1+x}}+\frac{1}{\sqrt{1+a}}"
            r"+\sqrt{\frac{ax}{ax+8}}",
            font_size=40, color=INK,
        )
        self.play(Write(expr), run_time=2.0)
        expr.next_to(stack, DOWN, buff=0.55)
        self.say("s01.b5")
        self.say("s01.b6")
        self.finish(frame_01(), dots)

    def scene_2(self) -> None:
        prev = frame_01()
        self.add(prev)
        self.say("s02.b1")
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        left = Axes(x_range=[0, 40, 10], y_range=[0, 1.1, 0.5], x_length=3.5,
                    y_length=2.5, axis_config={"include_ticks": False,
                                               "stroke_color": GRID,
                                               "stroke_width": 2}, tips=False)
        right = left.copy()
        left.move_to([-4.3, -0.15, 0.0])
        right.move_to([2.1, -0.15, 0.0])
        c1 = left.plot(lambda t: PHI(min(t, 1e9)), x_range=[0, 40], color=BLUE,
                       stroke_width=4)
        c2 = right.plot(lambda t: np.sqrt(2 * min(t, 1e9) / (2 * min(t, 1e9) + 8)),
                        x_range=[0, 40], color=VIOLET, stroke_width=4)
        l1 = Text("first term", font_size=FS_MICRO, color=BLUE).next_to(c1, UP, buff=0.12)
        l2 = Text("third term", font_size=FS_MICRO, color=VIOLET).next_to(c2, DOWN, buff=0.12)
        self.play(FadeOut(working), run_time=0.6)
        self.play(FadeIn(left), FadeIn(right), run_time=0.5)
        self.play(Create(c1), run_time=1.3)
        self.say("s02.b2")
        self.play(Create(c2), run_time=1.3)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        clash = MathTex(r"\longleftarrow\ \textbf{fight}\ \longrightarrow",
                        font_size=FS_LABEL, color=CORAL)
        clash.move_to([-1.1, 1.35, 0.0])
        self.play(FadeIn(clash), run_time=0.5)
        self.say("s02.b3")
        tail = MathTex(r"x\uparrow\ \Rightarrow\ \phi(x)\downarrow,\quad"
                       r"\sqrt{\tfrac{ax}{ax+8}}\uparrow", font_size=FS_WORK, color=MUTED)
        tail.move_to([0.0, -1.95, 0.0])
        self.play(Write(tail), run_time=0.9)
        self.say("s02.b4")
        self.say("s02.b5")
        self.finish(frame_02(), left, right, c1, c2, l1, l2, clash, tail)

    def scene_3(self) -> None:
        prev = frame_02()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s03.b1")
        ax = Axes(x_range=[0, 12, 3], y_range=[0, 1.1, 0.25], x_length=8.2,
                  y_length=4.3, axis_config={"stroke_color": GRID,
                                             "stroke_width": 2.4,
                                             "include_tip": False})
        ax.move_to([-1.2, 0.05, 0.0])
        self.play(FadeOut(working), FadeIn(ax), run_time=0.8)
        curve = ax.plot(lambda t: PHI(t), x_range=[0, 12], color=BLUE, stroke_width=5)
        self.play(Create(curve), run_time=1.6)
        self.say("s03.b2")
        dot = Dot(ax.c2p(0, 1.0), color=TEAL, radius=0.07)
        guide = DashedLine(ax.c2p(0, 1.0), ax.c2p(4.6, 1.0), color=TEAL,
                           stroke_width=2, dash_length=0.12)
        lbl = Text("phi(0) = 1", font_size=FS_LABEL, color=TEAL)
        lbl.next_to(dot, RIGHT, buff=0.16)
        self.play(FadeIn(dot), Create(guide), FadeIn(lbl), run_time=0.7)
        self.say("s03.b3")
        band = ax.plot(lambda t: PHI(t), x_range=[0, 1], color=BLUE, stroke_width=18)
        band.set_opacity(0.18)
        self.play(FadeIn(band), run_time=0.5)
        self.say("s03.b4")
        asym = MathTex(r"\phi(t)\sim t^{-1/2}", font_size=FS_WORK, color=AMBER)
        asym.move_to([4.35, 1.75, 0.0])
        slow = Text("dies slowly", font_size=FS_MICRO, color=MUTED)
        slow.next_to(asym, DOWN, buff=0.12)
        self.play(Write(asym), FadeIn(slow), run_time=0.9)
        self.say("s03.b5")
        self.finish(frame_03(), ax, curve, band, dot, guide, lbl, asym, slow)

    def scene_4(self) -> None:
        prev = frame_03()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s04.b1")
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.15, 0.25], x_length=5.0,
                  y_length=4.3, axis_config={"stroke_color": GRID,
                                             "stroke_width": 2.4,
                                             "include_tip": False})
        ax.move_to([-3.4, 0.0, 0.0])
        self.play(FadeOut(working), FadeIn(ax), run_time=0.8)
        curve = ax.plot(lambda t: PHI(t), x_range=[0, 1], color=BLUE, stroke_width=5)
        self.play(Create(curve), run_time=1.2)
        self.say("s04.b2")
        prev_bars = VGroup()
        for n in (2, 4, 8, 16):
            bars = VGroup(*ax.get_riemann_rectangles(
                curve, x_range=(0, 1), dx=1.0 / n, color=BLUE,
                fill_opacity=0.34, stroke_width=0))
            if prev_bars.submobjects:
                self.play(FadeTransform(prev_bars, bars), run_time=0.55)
            else:
                self.play(FadeIn(bars), run_time=0.55)
            prev_bars = bars
        self.say("s04.b3")
        region = ax.get_area(curve, x_range=(0, 1), color=TEAL, opacity=0.24)
        self.play(FadeTransform(prev_bars, region), run_time=0.8)
        self.say("s04.b2b")
        val = MathTex(r"\int_0^1\frac{dt}{\sqrt{1+t}}=2(\sqrt2-1)\approx0.828",
                      font_size=FS_WORK, color=INK)
        val.move_to([3.1, 1.55, 0.0])
        self.play(Write(val), run_time=1.1)
        self.say("s04.b4")
        ceil = DashedLine(ax.c2p(0, 1.0), ax.c2p(1, 1.0), color=CORAL,
                          stroke_width=2.6, dash_length=0.12)
        clbl = Text("y = 1", font_size=FS_MICRO, color=CORAL).next_to(ceil, UP, buff=0.10)
        self.play(Create(ceil), FadeIn(clbl), run_time=0.8)
        self.say("s04.b5")
        side = VGroup(
            Text("the whole region fits", font_size=FS_LABEL, color=INK),
            Text("strictly under y = 1", font_size=FS_LABEL, color=CORAL),
            Text("so phi never reaches 1", font_size=FS_LABEL, color=TEAL),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        side.move_to([3.1, -0.45, 0.0])
        self.play(FadeIn(side), run_time=0.6)
        self.finish(frame_04(), ax, curve, region, ceil, clbl, val, side)

    def scene_5(self) -> None:
        prev = frame_04()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s05.b1")
        left = VGroup()
        circ = Circle(radius=1.45, color=GRID, stroke_width=2.4).move_to([-4.1, 0.55, 0])
        hyp = Line([-5.55, 0.55, 0], [-2.65, 0.55, 0], color=MUTED, stroke_width=2)
        l1 = Line([-4.1, 0.55, 0], [-5.15, -0.70, 0], color=BLUE, stroke_width=3.4)
        l2 = Line([-4.1, 0.55, 0], [-3.05, -0.70, 0], color=VIOLET, stroke_width=3.4)
        alt = DashedLine([-5.15, -0.70, 0], [-3.05, -0.70, 0], color=TEAL, stroke_width=2.4)
        self.play(FadeOut(working), FadeIn(circ), FadeIn(hyp), run_time=0.7)
        self.say("s05.b2")
        self.play(Create(l1), Create(l2), run_time=0.9)
        self.say("s05.b3")
        la = Text("a", font_size=FS_MICRO, color=BLUE).move_to([-4.72, -0.5, 0])
        lb = Text("b", font_size=FS_MICRO, color=VIOLET).move_to([-3.48, -0.5, 0])
        lalt = Text("altitude = sqrt(ab)", font_size=FS_MICRO, color=TEAL)
        lalt.next_to(alt, DOWN, buff=0.16)
        self.play(Create(alt), FadeIn(la), FadeIn(lb), FadeIn(lalt), run_time=0.8)
        self.say("s05.b4")
        geo = MathTex(r"\sqrt{ab}\le\frac{a+b}{2}", font_size=FS_WORK, color=INK)
        geo.move_to([-4.1, -1.72, 0.0])
        gtag = Text("GEOMETRIC", font_size=FS_MICRO, color=MUTED, weight=BOLD)
        gtag.next_to(geo, UP, buff=0.2)
        self.play(Write(geo), FadeIn(gtag), run_time=0.8)
        self.say("s05.b5")
        ax = Axes(x_range=[0.2, 5, 1], y_range=[0, 6, 2], x_length=4.6, y_length=3.3,
                  axis_config={"stroke_color": GRID, "stroke_width": 2,
                               "include_tip": False})
        ax.move_to([3.5, 0.6, 0])
        g = ax.plot(lambda t: t + 1.0 / t, x_range=[0.2, 5], color=AMBER, stroke_width=4.4)
        self.play(FadeIn(ax), Create(g), run_time=1.4)
        self.say("s05.b6")
        mn = Dot(ax.c2p(1, 2), color=TEAL, radius=0.07)
        mg = DashedLine(ax.c2p(0.2, 2), ax.c2p(1, 2), color=TEAL, stroke_width=1.6)
        ml = Text("min = 2 at t = 1", font_size=FS_MICRO, color=TEAL)
        ml.next_to(mn, RIGHT, buff=0.14)
        ana = MathTex(r"t+\tfrac1t\ge2\ \Longrightarrow\ a+b\ge2\sqrt{ab}",
                      font_size=32, color=INK)
        ana.move_to([3.5, -1.72, 0.0])
        atag = Text("ANALYTIC", font_size=FS_MICRO, color=MUTED, weight=BOLD)
        atag.next_to(ana, UP, buff=0.2)
        self.play(FadeIn(mn), Create(mg), FadeIn(ml), run_time=0.7)
        self.play(Write(ana), FadeIn(atag), run_time=0.9)
        self.say("s05.b7")
        self.finish(frame_05(), circ, hyp, l1, l2, alt, la, lb, lalt, geo, gtag,
                    ax, g, mn, mg, ml, ana, atag)

    def scene_6(self) -> None:
        prev = frame_05()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.play(FadeOut(working), run_time=0.7)
        self.say("s06.b1")
        main = MathTex(r"A+B+C\ \ge\ 3\sqrt[3]{ABC}", font_size=60, color=INK)
        main.move_to([0.0, 1.05, 0.0])
        self.play(Write(main), run_time=1.4)
        self.say("s06.b2")
        eq = Text("equality exactly when A = B = C", font_size=FS_LABEL, color=TEAL)
        eq.next_to(main, DOWN, buff=0.26)
        self.play(FadeIn(eq), run_time=0.5)
        self.say("s06.b3")
        sub = MathTex(r"\sqrt[3]{8}=2\qquad\Longrightarrow\qquad A+B+C\ \ge\ 3\cdot2=6",
                      font_size=44, color=AMBER)
        sub.move_to([0.0, -0.95, 0.0])
        self.play(FadeOut(main, shift=UP * 0.18), FadeIn(sub), run_time=1.1)
        self.say("s06.b4")
        note6 = Text("remember the 6 — it appears twice, and it earns its keep twice",
                     font_size=FS_LABEL, color=MUTED)
        note6.next_to(sub, DOWN, buff=0.34)
        self.play(FadeIn(note6), run_time=0.6)
        self.finish(frame_06(), main, eq, sub, note6)

    def scene_7(self) -> None:
        prev = frame_06()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s07.b1")
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1.15, 0.25], x_length=5.4,
                  y_length=3.7, axis_config={"stroke_color": GRID,
                                             "stroke_width": 2.2,
                                             "include_tip": False})
        ax.move_to([-3.7, 0.15, 0])
        self.play(FadeOut(working), FadeIn(ax), run_time=0.7)
        self.say("s07.b2")
        curve = ax.plot(lambda t: PHI(t), x_range=[0, 10], color=AMBER, stroke_width=5)
        self.play(Create(curve), run_time=1.3)
        dd = MathTex(r"\phi''(t)=\tfrac34(1+t)^{-5/2}>0", font_size=32, color=MUTED)
        dd.move_to([3.5, 1.45, 0.0])
        self.play(Write(dd), run_time=0.9)
        self.say("s07.b3")
        t0 = 3.0
        slope = -0.5 * (1 + t0) ** -1.5
        tang = ax.plot(lambda t: PHI(t0) + slope * (t - t0), x_range=[0, 10],
                       color=CORAL, stroke_width=2.6)
        th = ax.plot(lambda t: PHI(t0) + slope * (t - t0), x_range=[0, 3.0],
                     color=CORAL, stroke_width=7)
        th.set_opacity(0.5)
        l1 = Text("curve above every tangent", font_size=FS_MICRO, color=TEAL)
        l1.next_to(tang, UP, buff=0.16).shift(LEFT * 0.35)
        l2 = Text("tangent line", font_size=FS_MICRO, color=CORAL)
        l2.next_to(ax.c2p(8, PHI(8) + slope * 5), RIGHT, buff=0.10)
        self.play(Create(th), Create(tang), run_time=1.1)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.say("s07.b4")
        side = VGroup(
            Text("as t → 0", font_size=FS_LABEL, color=MUTED),
            MathTex(r"\phi(t)\to1", font_size=44, color=TEAL),
            Text("from below, never touching", font_size=FS_MICRO, color=MUTED),
        ).arrange(DOWN, buff=0.16)
        side.move_to([3.5, -0.75, 0.0])
        self.play(FadeIn(side), run_time=0.7)
        self.say("s07.b5")
        self.finish(frame_07(), ax, curve, tang, th, l1, l2, dd, side)

    def scene_8(self) -> None:
        prev = frame_07()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s08.b1")
        o = np.array([0.0, 0.0, 0.0])
        u = np.array([1.55, 1.15, 0.0])
        v = np.array([2.25, -0.35, 0.0])
        ua = Arrow(o, u, buff=0, color=BLUE, stroke_width=5,
                   max_tip_length_to_length_ratio=0.09)
        vv = Arrow(o, v, buff=0, color=VIOLET, stroke_width=5,
                   max_tip_length_to_length_ratio=0.09)
        self.play(FadeOut(working), FadeIn(ua), FadeIn(vv), run_time=0.9)
        self.say("s08.b2")
        proj_len = float(np.dot(u, v) / np.linalg.norm(v))
        ph = v / np.linalg.norm(v) * proj_len
        dashed = DashedLine(o, ph, color=TEAL, stroke_width=3, dash_length=0.1)
        left = VGroup(ua, vv, dashed, Line(ph, u, color=CORAL, stroke_width=4))
        left.move_to([-3.9, 0.15, 0.0])
        lu = Text("u", font_size=FS_LABEL, color=BLUE).next_to(ua.get_end(), RIGHT, buff=0.08)
        lv = Text("v", font_size=FS_LABEL, color=VIOLET).next_to(vv.get_end(), RIGHT, buff=0.08)
        lproj = Text("projection", font_size=FS_MICRO, color=TEAL)
        lperp = Text("leftover ≥ 0", font_size=FS_MICRO, color=CORAL)
        self.play(Create(dashed), FadeIn(lproj), run_time=0.8)
        self.play(FadeIn(lperp), FadeIn(lu), FadeIn(lv), run_time=0.5)
        self.say("s08.b3")
        l3 = MathTex(r"\bigl(\phi(A)+\phi(B)\bigr)^2\le 2\left(\tfrac1{1+A}+\tfrac1{1+B}\right)",
                     font_size=36, color=INK)
        l3.move_to([2.9, 1.55, 0.0])
        self.play(Write(l3), run_time=1.3)
        self.say("s08.b4")
        l4 = MathTex(r"(1+A)(1+B)=1+s+p,\qquad s=A+B,\ p=AB", font_size=36, color=AMBER)
        l4.move_to([2.9, 0.15, 0.0])
        self.play(Write(l4), run_time=1.1)
        self.say("s08.b5")
        l5 = MathTex(r"\phi(A)+\phi(B)\ \le\ \sqrt{\frac{2(2+s)}{1+s+p}}",
                     font_size=40, color=TEAL)
        l5.move_to([2.9, -1.15, 0.0])
        self.play(Write(l5), run_time=1.1)
        self.finish(frame_08(), left, lu, lv, lproj, lperp, l3, l4, l5)

    def scene_9(self) -> None:
        prev = frame_08()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        head = title_bar("03  SUBSTITUTION", "The third term was never a third term")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s09.b1")
        top = MathTex(r"\sqrt{\frac{ax}{ax+8}}", font_size=64, color=VIOLET)
        top.move_to([0.0, 1.5, 0.0])
        self.play(Write(top), run_time=1.4)
        self.say("s09.b2")
        mid = MathTex(r"=\ \sqrt{\frac{1}{1+\frac{8}{ax}}}", font_size=48, color=INK)
        mid.next_to(top, DOWN, buff=0.38)
        self.play(Write(mid), run_time=1.4)
        self.say("s09.b3")
        defn = MathTex(r"=\ \frac{1}{\sqrt{1+C}}", font_size=48, color=INK)
        defn.next_to(mid, DOWN, buff=0.30)
        defn_tag = MathTex(r"C:=\frac{8}{ax}", font_size=48, color=AMBER)
        defn_tag.next_to(defn, RIGHT, buff=0.45)
        defn.next_to(mid, DOWN, buff=0.30)
        self.play(Write(defn), run_time=1.4)
        self.say("s09.b4")
        whole = MathTex(
            r"f=\phi(A)+\phi(B)+\phi(C),\qquad A=x,\ B=a,\ C=\frac{8}{AB}",
            font_size=40, color=INK,
        )
        whole.next_to(defn, DOWN, buff=0.48)
        self.play(Write(whole), run_time=1.5)
        self.say("s09.b5")
        self.say("s09.b6")
        self.finish(frame_09(), head, top, mid, defn, defn_tag, whole)

    def scene_10(self) -> None:
        prev = frame_09()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s10.b1")
        prod = MathTex(r"A\cdot B\cdot C=8", font_size=52, color=AMBER)
        prod.move_to([0.0, 0.75, 0.0])
        self.play(FadeOut(working), Write(prod), run_time=1.2)
        self.say("s10.b2")
        inner = VGroup(
            MathTex(r"A,B,C>0,\qquad ABC=8", font_size=44, color=AMBER),
            verdict_tex(r"\phi(A)+\phi(B)+\phi(C)", 48),
        ).arrange(DOWN, buff=0.34)
        box = card(inner, 11.6)
        box.move_to([0.0, -0.55, 0.0])
        self.play(FadeIn(box), run_time=0.8)
        self.say("s10.b3")
        why = Text("8 = 2³ — three terms, each naturally centred at 2",
                   font_size=FS_LABEL, color=MUTED)
        why.next_to(box, DOWN, buff=0.30)
        self.play(FadeIn(why), run_time=0.6)
        self.say("s10.b4")
        gift = Text("and the problem just became symmetric — a gift we are about to spend",
                    font_size=FS_LABEL, color=VIOLET)
        gift.next_to(why, DOWN, buff=0.16)
        self.play(FadeIn(gift), run_time=0.5)
        self.finish(frame_10(), prod, box, why, gift)

    def scene_11(self) -> None:
        prev = frame_10()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s11.b1")
        chips = VGroup()
        for i, nm in enumerate(["A", "B", "C"]):
            c = VGroup(
                RoundedRectangle(corner_radius=0.14, width=1.5, height=1.5,
                                 stroke_color=BLUE, stroke_width=2.4,
                                 fill_color=BLUE, fill_opacity=0.12),
                MathTex(nm, font_size=44, color=BLUE),
            )
            c.move_to([-3.1 + 3.1 * i, 1.55, 0.0])
            chips.add(c)
        self.play(FadeOut(working), LaggedStart(*[FadeIn(c) for c in chips],
                                               lag_ratio=0.18), run_time=1.1)
        self.say("s11.b2")
        sorted_chips = VGroup(*[
            VGroup(
                RoundedRectangle(corner_radius=0.14, width=1.5, height=1.5,
                                 stroke_color=BLUE, stroke_width=2.4,
                                 fill_color=BLUE, fill_opacity=0.12),
                MathTex(nm, font_size=44, color=BLUE),
            )
            for nm in ("A", "B", "C")
        ])
        for i, chip in enumerate(sorted_chips):
            chip.move_to([-3.1 + 3.1 * i, 1.55, 0.0])
        self.play(*[FadeOut(c) for c in chips], FadeIn(sorted_chips), run_time=0.9)
        chips.become(sorted_chips)
        swapnote = Text("the expression cannot tell them apart", font_size=FS_MICRO,
                        color=MUTED)
        swapnote.next_to(chips, DOWN, buff=0.24)
        self.play(FadeIn(swapnote), run_time=0.5)
        self.say("s11.b3")
        wlog = MathTex(r"\mathrm{WLOG}\quad A\le B\le C", font_size=44, color=TEAL)
        wlog.move_to([0.0, -0.55, 0.0])
        self.play(Write(wlog), run_time=0.9)
        cons = VGroup(
            MathTex(r"A\le2", font_size=40, color=AMBER),
            MathTex(r"2\le C", font_size=40, color=AMBER),
        ).arrange(RIGHT, buff=1.5)
        cons.move_to([0.0, -1.85, 0.0])
        why = Text("from A³ ≤ ABC = 8", font_size=FS_MICRO, color=MUTED)
        why.next_to(cons, DOWN, buff=0.16)
        self.play(FadeIn(cons), FadeIn(why), run_time=0.7)
        self.say("s11.b4")
        self.finish(frame_11(), chips, swapnote, wlog, cons, why)

    def scene_12(self) -> None:
        prev = frame_11()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        head = title_bar("04  LOWER BOUND", "Trade the square root for a rational function")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s12.b1")
        ax = Axes(x_range=[0, 9, 3], y_range=[0, 1.15, 0.25], x_length=6.2,
                  y_length=4.0, axis_config={"stroke_color": GRID,
                                             "stroke_width": 2.2,
                                             "include_tip": False})
        ax.move_to([-3.1, 0.1, 0])
        self.play(FadeIn(ax), run_time=0.6)
        self.say("s12.b2")
        c1 = ax.plot(lambda t: PHI(t), x_range=[0, 9], color=BLUE, stroke_width=5)
        c2 = ax.plot(lambda t: 1.0 / (1.0 + t), x_range=[0, 9], color=AMBER, stroke_width=4)
        self.play(Create(c1), run_time=1.2)
        reason = VGroup(
            Text("for t > 0 :", font_size=FS_LABEL, color=MUTED),
            MathTex(r"1+t>\sqrt{1+t}", font_size=36, color=INK),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        reason.move_to([3.5, 1.35, 0.0])
        self.play(Write(reason), run_time=1.0)
        self.say("s12.b3")
        l1 = Text("phi(t)", font_size=FS_LABEL, color=BLUE).next_to(c1, UP, buff=0.14)
        l2 = Text("1/(1+t)", font_size=FS_LABEL, color=AMBER).next_to(c2, DOWN, buff=0.16)
        self.play(Create(c2), FadeIn(l1), FadeIn(l2), run_time=1.1)
        self.say("s12.b4")
        gain = VGroup(
            MathTex(r"\Longrightarrow\ \frac{1}{\sqrt{1+t}}>\frac{1}{1+t}",
                    font_size=40, color=TEAL),
            Text("one-sided, and in our favour", font_size=FS_MICRO, color=VIOLET),
        ).arrange(DOWN, buff=0.24)
        gain.move_to([3.5, -0.85, 0.0])
        self.play(Write(gain), run_time=1.1)
        self.finish(frame_12(), head, ax, c1, c2, l1, l2, reason, gain)

    def scene_13(self) -> None:
        prev = frame_12()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        head = title_bar("04  LOWER BOUND", "Clear denominators — watch it collapse")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s13.b1")
        l1 = MathTex(r"\frac1{1+A}+\frac1{1+B}+\frac1{1+C}\ \ge\ 1", font_size=44, color=INK)
        l1.move_to([0.0, 1.95, 0.0])
        self.play(Write(l1), run_time=1.2)
        self.say("s13.b2")
        l2 = MathTex(r"(1+B)(1+C)+(1+A)(1+C)+(1+A)(1+B)\ \ge\ (1+A)(1+B)(1+C)",
                     font_size=30, color=MUTED)
        l2.next_to(l1, DOWN, buff=0.34)
        self.play(Write(l2), run_time=1.5)
        self.say("s13.b3")
        defs = Text("S = A+B+C ,  Q = AB+BC+CA", font_size=FS_MICRO, color=MUTED)
        defs.next_to(l2, DOWN, buff=0.18).align_to(l2, RIGHT)
        l3 = MathTex(r"3+2S+Q\ \ge\ 1+S+Q+ABC", font_size=40, color=INK)
        l3.next_to(l2, DOWN, buff=0.46)
        self.play(Write(l3), run_time=1.2)
        self.say("s13.b4")
        l4 = MathTex(r"3+2S+Q\ \ge\ 1+S+Q+8", font_size=40, color=AMBER)
        l4.next_to(l3, DOWN, buff=0.24)
        self.play(Write(l4), run_time=1.0)
        self.say("s13.b5")
        self.say("s13.b6")
        l5 = MathTex(r"A+B+C\ \ge\ 6", font_size=54, color=AMBER)
        l5.next_to(l4, DOWN, buff=0.30)
        self.play(Write(l5), run_time=1.1)
        self.say("s13.b7")
        amg = MathTex(r"A+B+C\ \ge\ 3\sqrt[3]{ABC}=3\cdot2=6", font_size=38, color=TEAL)
        amg.next_to(l5, DOWN, buff=0.34)
        self.play(Write(amg), run_time=1.2)
        self.finish(frame_13(), head, l1, l2, defs, l3, l4, l5, amg)

    def scene_14(self) -> None:
        prev = frame_13()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s14.b1")
        chain = vchain([
            MathTex(r"f", font_size=52, color=INK),
            MathTex(r">", font_size=52, color=TEAL),
            MathTex(r"\tfrac1{1+A}+\tfrac1{1+B}+\tfrac1{1+C}", font_size=44, color=INK),
            MathTex(r"\ge\ 1", font_size=52, color=AMBER),
        ])
        chain.move_to([0.0, 0.85, 0.0])
        self.play(FadeOut(working), LaggedStart(*[Write(c) for c in chain],
                                               lag_ratio=0.22), run_time=2.0)
        ring = Circle(radius=0.24, color=TEAL, stroke_width=3).move_to(chain[1].get_center())
        self.play(Create(ring), run_time=0.6)
        self.say("s14.b2")
        verdict = MathTex(r"f\;>\;1", font_size=64, color=TEAL)
        verdict.next_to(chain, DOWN, buff=0.60)
        self.play(Write(verdict), run_time=1.0)
        honesty = Text("slack to spare: at A=B=C=2 we get f = sqrt 3 ≈ 1.73, not 1",
                       font_size=FS_LABEL, color=MUTED)
        honesty.next_to(verdict, DOWN, buff=0.24)
        self.play(FadeIn(honesty), run_time=0.6)
        self.say("s14.b3")
    def scene_15(self) -> None:
        prev = frame_14()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s15.b1")
        head = title_bar("05  UPPER BOUND", "First, where the danger lives")
        ax = Axes(x_range=[0, 12, 3], y_range=[0, 2.1, 0.5], x_length=6.4, y_length=4.3,
                  axis_config={"stroke_color": GRID, "stroke_width": 2.2,
                               "include_tip": False})
        ax.move_to([-2.9, 0.1, 0.0])
        self.play(FadeOut(working), FadeIn(head), FadeIn(ax), run_time=0.7)
        self.say("s15.b2")
        path = ax.plot(lambda t: t, x_range=[0.35, 2.02], color=VIOLET, stroke_width=4)
        self.play(Create(path), run_time=0.9)
        self.say("s15.b3")
        top = DashedLine(ax.c2p(0, 2), ax.c2p(12, 2), color=CORAL, stroke_width=2.6,
                         dash_length=0.14)
        toplab = MathTex(r"f=2", font_size=FS_LABEL, color=CORAL)
        toplab.next_to(top, UP, buff=0.10)
        self.play(Create(top), FadeIn(toplab), run_time=0.7)
        self.say("s15.b4")
        sweep = ValueTracker(10.2)
        mark = always_redraw(lambda: Dot(ax.c2p(sweep.get_value(),
                                                 sweep.get_value()),
                                         color=VIOLET, radius=0.09))
        read = always_redraw(
            lambda: DecimalNumber(F2(sweep.get_value(), sweep.get_value()),
                                  num_decimal_places=4, color=INK, font_size=44))
        read.next_to(ax, RIGHT, buff=0.35).align_to(ax, UP)
        self.add(mark, read)
        self.play(sweep.animate.set_value(0.55), run_time=5.0, rate_func=rate_functions.ease_in_out_sine)
        self.say("s15.b5")
        self.remove(mark, read)
        warn = VGroup(
            Text("x, a → 0⁺", font_size=FS_LABEL, color=VIOLET),
            Text("the sum approaches 2 from below", font_size=FS_MICRO, color=MUTED),
            Text("and would cross it if we were careless", font_size=FS_MICRO, color=CORAL),
            Text("⇒ the proof must be sharp exactly here", font_size=FS_LABEL, color=AMBER),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        warn.move_to([2.6, -0.85, 0.0])
        self.play(FadeIn(warn), run_time=0.7)
        self.say("s15.b6")
        self.finish(frame_15(), head, ax, path, top, toplab, warn)

    def scene_16(self) -> None:
        prev = frame_15()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s16.b1")
        head = title_bar("05  UPPER BOUND", "Case 1 · A + B ≥ 6")
        bars = VGroup()
        parts = []
        for i, (nm, val, txt, col) in enumerate((
            ("A", 2.0, r"A\le2", TEAL),
            ("B", 4.0, r"B\ge6-A\ge4", BLUE),
            ("C", 4.0, r"C\ge B\ge4", BLUE),
        )):
            y = 1.85 - 1.15 * i
            base = Line([-6.3, y, 0], [-1.1, y, 0], color=GRID, stroke_width=2)
            full = Rectangle(width=5.2, height=0.30, stroke_width=0, fill_color=GRID,
                             fill_opacity=0.35).move_to([-3.7, y, 0])
            bar = Rectangle(width=5.2 * val / 6.0, height=0.30, stroke_width=0,
                            fill_color=col, fill_opacity=0.9).move_to(
                [-6.3 + 5.2 * val / 12.0, y, 0])
            lab = MathTex(nm, font_size=FS_LABEL, color=MUTED).move_to([-6.75, y, 0])
            val_ = MathTex(txt, font_size=FS_LABEL, color=col).move_to([-0.55, y, 0])
            row = VGroup(base, full, bar, lab, val_)
            bars.add(row)
            parts.append(row)
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s16.b2")
        self.play(FadeIn(parts[0]), run_time=0.6)
        self.say("s16.b3")
        self.play(FadeIn(parts[1]), FadeIn(parts[2]), run_time=0.6)
        self.say("s16.b4")
        chain = VGroup(
            MathTex(r"f=\phi(A)+\phi(B)+\phi(C)", font_size=36, color=INK),
            MathTex(r"<\ 1+\tfrac{1}{\sqrt5}+\tfrac{1}{\sqrt5}", font_size=36, color=AMBER),
            MathTex(r"=1+\tfrac{2}{\sqrt5}=1.8944\ldots<2", font_size=36, color=TEAL),
        ).arrange(DOWN, buff=0.24)
        chain.move_to([3.6, 0.55, 0.0])
        self.play(Write(chain), run_time=1.6)
        self.say("s16.b5")
        why = Text("2/√5 < 1 because 4 < 5", font_size=FS_MICRO, color=MUTED)
        why.next_to(chain, DOWN, buff=0.26)
        self.play(FadeIn(why), run_time=0.5)
        self.finish(frame_16(), head, bars, chain, why)

    def scene_17(self) -> None:
        prev = frame_16()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s17.b1")
        head = title_bar("05  UPPER BOUND", "Case 2 · A + B < 6")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s17.b2")
        known = VGroup(
            MathTex(r"\phi(C)=\sqrt{\tfrac{p}{p+8}}\ \ \text{exactly}", font_size=34,
                    color=TEAL),
            MathTex(r"\phi(A)+\phi(B)\le\sqrt{\tfrac{2(2+s)}{1+s+p}}"
                    r"\ \ \text{(Cauchy)}", font_size=34, color=BLUE),
        ).arrange(DOWN, buff=0.30)
        known.move_to([-3.3, 0.85, 0.0])
        self.play(Write(known), run_time=1.8)
        self.say("s17.b3")
        self.say("s17.b4")
        cap = MathTex(r"p=AB<A(6-A)", font_size=34, color=AMBER)
        cap.next_to(known, DOWN, buff=0.34)
        self.play(Write(cap), run_time=1.0)
        self.say("s17.b5")
        ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, 9, 2], x_length=3.4, y_length=2.6,
                  axis_config={"stroke_color": GRID, "stroke_width": 1.8,
                               "include_tip": False})
        ax.move_to([3.4, -1.35, 0.0])
        par = ax.plot(lambda t: t * (6 - t), x_range=[0, 2], color=AMBER, stroke_width=4)
        pardot = Dot(ax.c2p(2, 8), color=CORAL, radius=0.08)
        parl = Text("peak 8 at A = 2", font_size=FS_MICRO, color=CORAL)
        parl.next_to(pardot, RIGHT, buff=0.10)
        self.play(FadeIn(ax), Create(par), run_time=1.3)
        self.play(FadeIn(pardot), FadeIn(parl), run_time=0.5)
        self.say("s17.b6")
        master = card(MathTex(
            r"f<\sqrt{\tfrac{2(2+s)}{1+s+p}}+\sqrt{\tfrac{p}{p+8}}",
            font_size=40, color=INK), 7.0, AMBER)
        master.move_to([3.5, 1.35, 0.0])
        self.play(FadeIn(master), run_time=0.8)
        self.finish(frame_17(), head, known, cap, master, ax, par, pardot, parl)

    def scene_18(self) -> None:
        prev = frame_17()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s18.b1")
        head = title_bar("05  UPPER BOUND", "The sharp sub-case, and one lemma")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s18.b2")
        mono = MathTex(r"\tfrac{d}{ds}\!\left[\tfrac{2+s}{1+s+p}\right]"
                       r"=\tfrac{p-1}{(1+s+p)^2}\le0\quad(p\le1)",
                       font_size=34, color=BLUE)
        mono.move_to([0.0, 1.65, 0.0])
        self.play(Write(mono), run_time=1.6)
        self.say("s18.b3")
        atmin = MathTex(r"\Rightarrow\ \phi(A)+\phi(B)\le"
                        r"\sqrt{\tfrac{2(2+2\sqrt p)}{(1+\sqrt p)^2}}"
                        r"=\tfrac{2}{\sqrt{1+\sqrt p}}", font_size=34, color=INK)
        atmin.next_to(mono, DOWN, buff=0.26)
        self.play(Write(atmin), run_time=1.8)
        self.say("s18.b4")
        lemma = card(VGroup(
            MathTex(r"\textbf{LEMMA}\quad"
                    r"\frac{2}{\sqrt{1+q}}+\frac{q}{\sqrt{q^2+8}}<2"
                    r"\quad\text{for every }q>0", font_size=40, color=INK)), 12.2, VIOLET)
        lemma.next_to(atmin, DOWN, buff=0.30)
        self.play(FadeIn(lemma), run_time=0.9)
        self.say("s18.b5")
        proof = VGroup(
            MathTex(r"2-\tfrac{2}{\sqrt{1+q}}=\tfrac{2q}{1+q+\sqrt{1+q}}"
                    r"\quad\text{(rationalise)}", font_size=30, color=INK),
            MathTex(r"1+q+\sqrt{1+q}\le2+\tfrac32q"
                    r"\quad\text{since }\sqrt{1+q}\le1+\tfrac q2", font_size=30, color=INK),
            MathTex(r"4(q^2+8)-(2+\tfrac32q)^2=\tfrac74q^2-6q+28>0"
                    r"\quad(\Delta=-160<0)", font_size=30, color=TEAL),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        proof.next_to(lemma, DOWN, buff=0.26)
        self.play(LaggedStart(*[Write(p) for p in proof], lag_ratio=0.4), run_time=2.4)
        self.say("s18.b6")
        self.finish(frame_18(), head, mono, atmin, lemma, proof)

    def scene_19(self) -> None:
        prev = frame_18()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s19.b1")
        head = title_bar("05  UPPER BOUND", "The rest of Case 2, where slack is available")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s19.b2")
        plug = MathTex(r"s<6\ \Rightarrow\ "
                       r"\sqrt{\tfrac{2(2+s)}{1+s+p}}<\sqrt{\tfrac{16}{7+p}}",
                       font_size=36, color=BLUE)
        plug.move_to([0.0, 1.65, 0.0])
        self.play(Write(plug), run_time=1.4)
        self.say("s19.b3")
        self.say("s19.b4")
        header = VGroup(*[
            Text(t, font_size=FS_MICRO, color=MUTED, weight=BOLD)
            for t in ("sub-range", "first two terms", "third term", "total")
        ]).arrange(RIGHT, buff=0.55, aligned_edge=UP)
        specs = (
            (r"p\le1", r"\tfrac{2}{\sqrt{1+\sqrt p}}", r"\sqrt{\tfrac{p}{p+8}}",
             r"<2\ \text{(Lemma)}", TEAL),
            (r"1<p\le3", r"\sqrt2", r"\sqrt{\tfrac3{11}}", r"1.9364<2", AMBER),
            (r"3<p<8", r"\tfrac4{\sqrt{10}}", r"\tfrac1{\sqrt2}", r"1.9720<2", AMBER),
        )
        body = VGroup()
        for a, b, c, d, col in specs:
            body.add(VGroup(
                MathTex(a, font_size=FS_MICRO, color=INK),
                MathTex(b, font_size=FS_MICRO, color=BLUE),
                MathTex(c, font_size=FS_MICRO, color=VIOLET),
                MathTex(d, font_size=FS_MICRO, color=col),
            ).arrange(RIGHT, buff=0.55, aligned_edge=UP))
        body.arrange(DOWN, buff=0.30, aligned_edge=UP)
        table = VGroup(header, body).arrange(DOWN, buff=0.28, aligned_edge=UP)
        table.next_to(plug, DOWN, buff=0.34)
        self.play(FadeIn(table), run_time=1.0)
        self.say("s19.b5")
        exact = VGroup(
            Text("the last two rows are exact, not numerical:", font_size=FS_MICRO,
                 color=MUTED),
            MathTex(r"63>44\sqrt2\ (3969>3872)", font_size=FS_MICRO, color=AMBER),
            MathTex(r"2.9>2\sqrt2\ (8.41>8)", font_size=FS_MICRO, color=AMBER),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        exact.next_to(table, DOWN, buff=0.30).align_to(table, LEFT)
        self.play(FadeIn(exact), run_time=0.7)
        self.say("s19.b6")
        whole = VGroup(plug, table, exact).move_to([0.0, 0.35, 0.0])
        self.finish(frame_19(), head, whole)

    def scene_20(self) -> None:
        prev = frame_19()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s20.b1")
        head = title_bar("05  UPPER BOUND", "Upper bound closed")
        verdict = verdict_tex(r"f(x,a)", 88)
        verdict.move_to([0.0, 0.75, 0.0])
        self.play(FadeOut(working), FadeIn(head), Write(verdict), run_time=1.4)
        self.say("s20.b2")
        sub = MathTex(r"A=x,\quad B=a,\quad C=\tfrac{8}{AB},\quad ABC=8",
                      font_size=34, color=MUTED)
        sub.next_to(verdict, DOWN, buff=0.50)
        self.play(FadeIn(sub), run_time=0.7)
        self.say("s20.b3")
        beat = Text("both bounds closed. now let us look at it.", font_size=FS_LABEL,
                    color=VIOLET)
        beat.next_to(sub, DOWN, buff=0.28)
        self.play(FadeIn(beat), run_time=0.6)
        self.finish(frame_20(), head, verdict, sub, beat)

    def _panel(self, builder, *beats: str) -> None:
        panel = builder()
        self.play(FadeIn(panel), run_time=0.9)
        for key in beats:
            self.say(key)

    def scene_21(self) -> None:
        prev = frame_20()
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s21.b1")
        panel = panel_contour()
        self.play(FadeOut(working), FadeIn(panel), run_time=1.0)
        self.say("s21.b2")
        self.say("s21.b3")
        self.say("s21.b4")
        bar = [m for m in panel if isinstance(m, ImageMobject)][-1]
        self.say("s21.b5")
        self.play(Circumscribe(bar, color=AMBER, run_time=1.0), run_time=1.0)
        self.say("s21.b6")
        self.play(Indicate(bar, color=CORAL, scale_factor=1.10), run_time=1.2)
        self.say("s21.b7")
        self.finish(frame_of("S21"), panel)

    def scene_22(self) -> None:
        prev = frame_of("S21")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s22.b1")
        panel = panel_slice()
        self.play(FadeOut(working), FadeIn(panel), run_time=1.0)
        self.say("s22.b2")
        sweep = ValueTracker(0.4)
        target = [m for m in panel if isinstance(m, Axes)][0]
        mark = always_redraw(
            lambda: Dot(target.c2p(sweep.get_value(), 0), color=AMBER, radius=0.08))
        read = always_redraw(
            lambda: DecimalNumber(F2(sweep.get_value(), 2.0), num_decimal_places=4,
                                  color=AMBER, font_size=36))
        read.move_to([5.35, 1.9, 0.0])
        self.add(mark, read)
        self.say("s22.b3")
        self.play(sweep.animate.set_value(28.0), run_time=5.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.remove(mark, read)
        self.say("s22.b4")
        self.say("s22.b5")
        self.say("s22.b6")
        self.finish(frame_of("S22"), panel)

    def scene_23(self) -> None:
        prev = frame_of("S22")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s23.b1")
        panel = panel_logspace()
        self.play(FadeOut(working), FadeIn(panel), run_time=1.0)
        self.say("s23.b2")
        self.say("s23.b3")
        self.say("s23.b4")
        self.say("s23.b5")
        self.say("s23.b6")
        self.finish(frame_of("S23"), panel)

    def scene_24(self) -> None:
        prev = frame_of("S23")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s24.b1")
        panel = panel_cases()
        self.play(FadeOut(working), FadeIn(panel), run_time=1.0)
        self.say("s24.b2")
        self.say("s24.b3")
        dashed = [m for m in panel if isinstance(m, DashedLine)]
        if dashed:
            self.play(Circumscribe(dashed[0], color=INK, run_time=1.0), run_time=1.0)
        self.say("s24.b4")
        self.say("s24.b5")
        self.say("s24.b6")
        self.finish(frame_of("S24"), panel)

    def scene_25(self) -> None:
        prev = frame_of("S24")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s25.b1")
        panel = panel_stats()
        self.play(FadeOut(working), FadeIn(panel), run_time=1.0)
        self.say("s25.b2")
        self.say("s25.b3")
        self.say("s25.b4")
        self.say("s25.b5")
        rects = [m for m in panel if isinstance(m, Rectangle) and m.height > 0.3]
        if rects:
            self.play(LaggedStart(*[Indicate(r, color=TEAL, scale_factor=1.06)
                                   for r in rects[:8]], lag_ratio=0.08), run_time=1.4)
        self.say("s25.b6")
        self.say("s25.b7")
        self.finish(frame_of("S25"), panel)

    def scene_26(self) -> None:
        prev = frame_of("S25")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s26.b1")
        head = title_bar("05  PICTURES", "Panel 6 · both constants are optimal")
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        left = VGroup(
            Text("x, a → +∞", font_size=FS_LABEL, color=MUTED),
            MathTex(r"\phi(x)\to0,\quad \phi(a)\to0,\quad"
                    r"\sqrt{\tfrac{ax}{ax+8}}\to1", font_size=30, color=INK),
            MathTex(r"f\to1\ \text{from above}", font_size=40, color=TEAL),
        ).arrange(DOWN, buff=0.26)
        right = VGroup(
            Text("x, a → 0⁺", font_size=FS_LABEL, color=MUTED),
            MathTex(r"\phi(x)\to1,\quad \phi(a)\to1,\quad"
                    r"\sqrt{\tfrac{ax}{ax+8}}\to0", font_size=30, color=INK),
            MathTex(r"f\to2\ \text{from below}", font_size=40, color=CORAL),
        ).arrange(DOWN, buff=0.26)
        pair = VGroup(left, right).arrange(RIGHT, buff=1.1)
        pair.move_to([0.0, 0.55, 0.0])
        self.play(FadeIn(left), run_time=0.9)
        self.say("s26.b2")
        self.say("s26.b3")
        self.play(FadeIn(right), run_time=0.9)
        self.say("s26.b4")
        verdict = MathTex(r"\inf f=1\qquad\sup f=2\qquad\text{neither attained}",
                          font_size=44, color=INK)
        verdict.next_to(pair, DOWN, buff=0.50)
        self.play(Write(verdict), run_time=1.3)
        self.say("s26.b5")
        forced = VGroup(
            Text("so 1.0001 would be false, 1.9999 would be false,", font_size=FS_LABEL,
                 color=MUTED),
            Text("and the statement must use strict inequalities", font_size=FS_LABEL,
                 color=AMBER),
        ).arrange(DOWN, buff=0.16)
        forced.next_to(verdict, DOWN, buff=0.30)
        self.play(FadeIn(forced), run_time=0.7)
        self.say("s26.b6")
        self.finish(frame_of("S26"), head, pair, verdict, forced)

    def scene_27(self) -> None:
        prev = frame_of("S26")
        self.add(prev)
        working = prev.copy()
        self.remove(prev)
        self.add(working)
        self.say("s27.b1")
        head = title_bar("05  CLOSE", "The whole proof on one screen")
        col = VGroup(
            MathTex(r"A=x,\ B=a,\ C=\tfrac{8}{AB}\ \Rightarrow\ ABC=8", font_size=32,
                    color=AMBER),
            MathTex(r"f=\phi(A)+\phi(B)+\phi(C)", font_size=32, color=INK),
            MathTex(r"f>\tfrac1{1+A}+\tfrac1{1+B}+\tfrac1{1+C}\ge1\quad(A+B+C\ge6)",
                    font_size=30, color=TEAL),
            MathTex(r"A+B\ge6:\ f<1+\tfrac2{\sqrt5}<2", font_size=30, color=BLUE),
            MathTex(r"A+B<6:\ p<8,\ \text{then }p\le1,\,1<p\le3,\,3<p<8",
                    font_size=30, color=BLUE),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        col.move_to([-0.4, 0.75, 0.0])
        self.play(FadeOut(working), FadeIn(head), run_time=0.7)
        self.say("s27.b2")
        self.play(FadeIn(col[0]), FadeIn(col[1]), run_time=0.8)
        self.say("s27.b3")
        self.play(FadeIn(col[2]), run_time=0.7)
        self.say("s27.b4")
        self.play(FadeIn(col[3]), FadeIn(col[4]), run_time=0.8)
        verdict = verdict_tex("f", 64)
        verdict.next_to(col, DOWN, buff=0.34).align_to(col, RIGHT)
        self.play(Write(verdict), run_time=1.0)
        self.say("s27.b5")
        foot = Text("verification/verify_math.py — 24/24 checks pass", font_size=FS_MICRO,
                    color=MUTED)
        foot.next_to(col, DOWN, buff=0.60).align_to(col, LEFT)
        self.play(FadeIn(foot), run_time=0.6)
        self.finish(frame_27(), head, col, verdict, foot)


# ---------------------------------------------------------------------------
# voiceover script - generated from the transcript so it cannot go stale
# ---------------------------------------------------------------------------
def _clock(seconds: float) -> str:
    whole = int(round(seconds))
    return f"{whole // 60:d}:{whole % 60:02d}"


def build_voiceover_script() -> str:
    lines = [
        "THE 2008 JIANGXI GAOKAO PROBLEM -- VOICEOVER SCRIPT",
        "=" * 78,
        "",
        "Generated from the BEATS table in scene.py, which is the same table the",
        "renderer holds on to and that verify_budget asserts against. Do not",
        "hand-edit: change the transcript in scene.py and re-run this.",
        "",
        f"Sections          : {SECTION_COUNT}",
        f"Total narration   : {_clock(TOTAL_NARRATION)} ({TOTAL_NARRATION:.1f}s)",
        f"Caption companion : scene_no_vo.py (GAOKAO_CAPTIONS=1)",
        "",
    ]
    at = 0.0
    for name in sorted(NARRATION, key=lambda s: int(s[1:])):
        beats = NARRATION[name]
        held = sum(d for _, _, d in beats)
        lines.append("-- " + name + " " + "-" * max(0, 68 - len(name)))
        for _, text, dur in beats:
            lines.append(f"  [{_clock(at)} -> {_clock(at + dur)}]  {text}")
            at += dur
        lines.append(f"  (section narration {_clock(held)}, running total {_clock(at)})")
        lines.append("")
    lines.append("=" * 78)
    lines.append(f"END - {_clock(at)} of narration across {SECTION_COUNT} sections")
    return "\n".join(lines)


VOICEOVER_SCRIPT = build_voiceover_script()


if __name__ == "__main__":
    print(VOICEOVER_SCRIPT)


