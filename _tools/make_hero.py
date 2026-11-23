#!/usr/bin/env python3
"""Write _hero.qmd: the home-page illustration.

A top-down sketch of two rooms mapped with Gaussian splats, with a figure-eight
camera path and pose frames along it that look toward the middle of each room (x red, y green, z out of the page).
Colours come from CSS variables in theme/base.scss, so the same SVG works in
light and dark mode. The output is deterministic; edit and rerun:

    python3 _tools/make_hero.py
"""

import math
import random
from pathlib import Path

W, H = 1000, 360
VB = "64 36 872 288"  # cropped to the walls so the left wall lines up with the text column
SEED = 7
OUT = Path(__file__).resolve().parent.parent / "_hero.qmd"

rng = random.Random(SEED)

# ---------------------------------------------------------------- camera path
CX, CY, A, SY = 560.0, 202.0, 300.0, 0.86  # figure-eight centred in the doorway


def lemniscate(t):
    d = 1.0 + math.sin(t) ** 2
    return CX + A * math.cos(t) / d, CY + SY * A * math.sin(t) * math.cos(t) / d


path = [lemniscate(2 * math.pi * k / 360) for k in range(361)]
seg = [math.dist(path[k], path[k + 1]) for k in range(360)]
length = sum(seg)
cum = [0.0]
for s in seg:
    cum.append(cum[-1] + s)


def dist_to_path(x, y):
    return min(math.dist((x, y), p) for p in path[::3])


# ------------------------------------------------------------------- splats
splats = []  # (cx, cy, rx, ry, angle, gradient, opacity)


def add(cx, cy, rx, ry, ang, grad, op):
    splats.append((cx, cy, rx, ry, ang, grad, op))


# Outer walls: a rounded rectangle, with a door gap in the bottom wall.
X0, Y0, X1, Y1, R = 70.0, 44.0, 930.0, 316.0, 34.0
L_h, L_v, L_a = X1 - X0 - 2 * R, Y1 - Y0 - 2 * R, math.pi * R / 2
TOTAL = 2 * L_h + 2 * L_v + 4 * L_a


def wall_point(s):
    """Point and tangent angle (degrees) at arc length s along the outer wall."""
    pieces = [
        ("line", (X0 + R, Y0), 0.0, L_h),
        ("arc", (X1 - R, Y0 + R), -90.0, L_a),
        ("line", (X1, Y0 + R), 90.0, L_v),
        ("arc", (X1 - R, Y1 - R), 0.0, L_a),
        ("line", (X1 - R, Y1), 180.0, L_h),
        ("arc", (X0 + R, Y1 - R), 90.0, L_a),
        ("line", (X0, Y1 - R), 270.0, L_v),
        ("arc", (X0 + R, Y0 + R), 180.0, L_a),
    ]
    for kind, p, ang, ln in pieces:
        if s <= ln:
            if kind == "line":
                a = math.radians(ang)
                return p[0] + s * math.cos(a), p[1] + s * math.sin(a), ang
            phi = ang + math.degrees(s / R)
            a = math.radians(phi)
            return p[0] + R * math.cos(a), p[1] + R * math.sin(a), phi + 90.0
        s -= ln
    return X0 + R, Y0, 0.0


def wall_splat(x, y, tangent, scale=1.0):
    n = math.radians(tangent + 90.0)
    off = rng.gauss(0, 1.0)
    add(x + off * math.cos(n), y + off * math.sin(n),
        rng.uniform(10, 16) * scale, rng.uniform(2.0, 3.3) * scale,
        tangent + rng.gauss(0, 3), "wall", rng.uniform(0.5, 0.82))


for k in range(240):
    s = (k + rng.uniform(-0.35, 0.35)) / 240 * TOTAL
    x, y, tan = wall_point(s % TOTAL)
    if abs(y - Y1) < 1 and 395 < x < 455:  # front door
        continue
    wall_splat(x, y, tan)

# Partition between the rooms, with a doorway the path passes through.
for y in [rng.uniform(Y0 + 4, 158) for _ in range(26)] + [rng.uniform(248, Y1 - 4) for _ in range(15)]:
    wall_splat(560 + rng.gauss(0, 1.2), y, 90.0)


def cluster(cx, cy, w, h, n, grad, rx=(5, 12), ry=(3.5, 8), ang=None, op=(0.22, 0.45)):
    placed, tries = 0, 0
    while placed < n and tries < 50 * n:
        tries += 1
        x, y = cx + rng.uniform(-w / 2, w / 2), cy + rng.uniform(-h / 2, h / 2)
        if dist_to_path(x, y) < 16:
            continue
        a = rng.uniform(0, 180) if ang is None else ang + rng.gauss(0, 6)
        add(x, y, rng.uniform(*rx), rng.uniform(*ry), a, grad, rng.uniform(*op))
        placed += 1


# Left room: shelf of books, table with chairs, armchair.
cluster(205, 66, 190, 9, 22, "wall", rx=(4, 9), ry=(2, 3.5), ang=0, op=(0.3, 0.55))
cluster(392, 204, 86, 40, 22, "z", rx=(7, 14), ry=(5, 9))
for dx, dy in [(-56, -12), (-56, 14), (56, -12), (56, 14)]:
    cluster(392 + dx, 204 + dy, 14, 12, 4, "x", rx=(4, 7), ry=(3, 5), op=(0.25, 0.45))
cluster(128, 272, 46, 40, 12, "x", rx=(6, 13), ry=(5, 9))
cluster(392, 204, 170, 96, 8, "z", rx=(26, 44), ry=(16, 26), op=(0.05, 0.09))  # rug under the table
cluster(92, 168, 12, 92, 12, "wall", rx=(6, 12), ry=(2.5, 4), ang=90, op=(0.3, 0.55))  # cabinet

# Right room: desk, plant, sofa, coffee table.
cluster(720, 66, 150, 10, 16, "wall", rx=(6, 14), ry=(2.5, 4), ang=0, op=(0.3, 0.55))
cluster(884, 86, 44, 44, 16, "y", rx=(5, 11), ry=(4, 8), op=(0.25, 0.5))
cluster(902, 206, 20, 112, 14, "x", rx=(7, 14), ry=(4, 7), ang=90)
cluster(728, 204, 50, 30, 10, "y", rx=(6, 11), ry=(4, 7), op=(0.2, 0.38))
cluster(728, 204, 150, 84, 7, "y", rx=(24, 40), ry=(14, 24), op=(0.05, 0.08))  # rug
cluster(640, 292, 70, 14, 10, "z", rx=(6, 12), ry=(3, 5), ang=0, op=(0.25, 0.45))  # low cabinet

# ------------------------------------------------------------- pose frames
frames = []
n_frames = 12
for k in range(n_frames):
    target = (k + 0.5) / n_frames * length
    i = next(j for j in range(360) if cum[j + 1] >= target)
    (x0, y0), (x1, y1) = path[i], path[i + 1]
    if math.dist((x0, y0), (CX, CY)) < 40:  # keep the crossing clear
        continue
    lx = CX - 0.62 * A if x0 < CX else CX + 0.62 * A  # centre of this loop
    th = math.atan2(CY - y0, lx - x0)
    frames.append((x0, y0, th, cum[i] / length))

# ------------------------------------------------------------------ output
GRADS = {"wall": "--splat-wall", "x": "--axis-x", "y": "--axis-y", "z": "--axis-z"}


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


lines = [
    "```{=html}",
    f'<svg viewBox="{VB}" role="img" aria-labelledby="hero-title" xmlns="http://www.w3.org/2000/svg">',
    '<title id="hero-title">Top-down sketch of two rooms mapped with Gaussian splats, '
    "with a figure-eight camera path and pose frames along it.</title>",
    "<defs>",
]
for name, var in GRADS.items():
    lines.append(
        f'<radialGradient id="g-{name}">'
        f'<stop offset="0" style="stop-color:var({var});stop-opacity:1"/>'
        f'<stop offset="0.45" style="stop-color:var({var});stop-opacity:0.62"/>'
        f'<stop offset="0.75" style="stop-color:var({var});stop-opacity:0.2"/>'
        f'<stop offset="1" style="stop-color:var({var});stop-opacity:0"/>'
        "</radialGradient>"
    )
lines.append("</defs>")
lines.append('<g class="splats">')
for i, (cx, cy, rx, ry, ang, grad, op) in enumerate(splats):
    lines.append(
        f'<ellipse class="s" cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" '
        f'transform="rotate({f(ang)} {f(cx)} {f(cy)})" fill="url(#g-{grad})" '
        f'fill-opacity="{op:.2f}" style="--i:{i}"/>'
    )
lines.append("</g>")
d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in path)
lines.append(f'<path class="hero-path" d="{d}" style="--len:{length:.0f}"/>')
lines.append('<g class="tfs">')
L = 15.0
for x, y, th, t in frames:
    xe = (x + L * math.cos(th), y + L * math.sin(th))
    ye = (x + L * math.sin(th), y - L * math.cos(th))
    lines.append(
        f'<g class="tf" style="--t:{t:.3f}">'
        f'<line class="tf-x" x1="{f(x)}" y1="{f(y)}" x2="{f(xe[0])}" y2="{f(xe[1])}"/>'
        f'<line class="tf-y" x1="{f(x)}" y1="{f(y)}" x2="{f(ye[0])}" y2="{f(ye[1])}"/>'
        f'<circle class="tf-z" cx="{f(x)}" cy="{f(y)}" r="3.2"/>'
        f'<circle class="tf-z-dot" cx="{f(x)}" cy="{f(y)}" r="1.1"/>'
        "</g>"
    )
lines.append("</g>")
lines.append("</svg>")
lines.append("```")
OUT.write_text("\n".join(lines) + "\n")
print(f"wrote {OUT.name}: {len(splats)} splats, {len(frames)} pose frames, path {length:.0f} px")
