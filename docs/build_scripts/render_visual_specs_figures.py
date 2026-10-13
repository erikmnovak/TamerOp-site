#!/usr/bin/env python3
"""Draw the mathematical schematics in the visual specification account.

Run with --check to verify the committed SVGs against these sources.
These figures explain coefficient and coordinate conventions; they are not
captures of package computations or assertions about a particular resolution.
"""

from argparse import ArgumentParser
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "visual_specs"
INK = "#172b42"
BLUE = "#245c99"
ORANGE = "#9a470b"
GRAY = "#475569"


class Drawing:
    def __init__(self, height, title, description):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="{height}" '
            f'viewBox="0 0 520 {height}" role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="description">{escape(description)}</desc>',
            '<!-- Authored schematic; regenerate with docs/build_scripts/render_visual_specs_figures.py. -->',
            f'<rect width="520" height="{height}" fill="white"/>',
            f'<g font-family="DejaVu Sans, sans-serif" fill="{INK}" text-anchor="middle">',
        ]

    def text(self, x, y, value, size=24, color=INK, anchor="middle"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" '
                          f'fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')

    def path(self, points, color=GRAY, width=2, dash=""):
        self.parts.append(f'<path d="{points}" fill="none" stroke="{color}" '
                          f'stroke-width="{width}" stroke-dasharray="{dash}"/>')

    def box(self, x, y, width, height, fill, stroke="none"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                          f'rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def circle(self, x, y):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{BLUE}"/>')

    def finish(self):
        return "\n".join(self.parts + ["</g></svg>", ""])


def principal_coefficients():
    d = Drawing(490, "Two zeros in a principal summand matrix",
                "On the poset 1 less than 2, a map from P_u to P_v can have a "
                "nonzero coefficient only when v is at most u. The example is "
                "the identity matrix on P1 plus P2. Rows are targets and columns "
                "are sources. The upper right zero is allowed; the lower left "
                "zero is forced and is marked with a dagger.")
    d.text(260, 36, "Principal modules on 1 < 2", 25)
    d.text(318, 82, "Source columns", 23)
    d.text(253, 123, "P₁", 26)
    d.text(383, 123, "P₂", 26)
    d.text(81, 188, "Target", 22)
    d.text(81, 216, "rows", 22)
    d.text(165, 185, "P₁", 26)
    d.text(165, 265, "P₂", 26)
    d.box(338, 145, 90, 55, "#eff6ff", BLUE)
    d.box(208, 225, 90, 55, "#fff7ed", ORANGE)
    d.path("M 208 140 H 197 V 287 H 208", INK, 2.5)
    d.path("M 428 140 H 439 V 287 H 428", INK, 2.5)
    d.text(253, 185, "1", 30)
    d.text(383, 185, "0", 30, BLUE)
    d.text(253, 265, "0†", 30, ORANGE)
    d.text(383, 265, "1", 30)
    d.text(260, 340, "P₂ → P₁: 1 ≤ 2, so zero is allowed.", 23, BLUE)
    d.text(260, 386, "P₁ → P₂: 2 ≰ 1, so zero is forced.", 23, ORANGE)
    d.text(260, 448, "† marks the order condition.", 22, GRAY)
    return d.finish()


def anchor_coordinates():
    d = Drawing(705, "One data anchor in two horizontal windows",
                "The same data point (1,1) appears in two axis windows. "
                "Both vertical axes run from zero to two. The first horizontal "
                "axis runs from zero to two, placing the point halfway across; "
                "the second runs from zero to four, placing it one quarter "
                "across. A connector must use the updated pixel position.")
    d.text(260, 36, "The data anchor stays at (1, 1)", 25)
    for top, maximum, title in ((102, 2, "Horizontal window: 0 to 2"),
                                (390, 4, "Horizontal window: 0 to 4")):
        left, right, bottom = 90, 450, top + 150
        width = right - left
        point_x = left + width / maximum
        point_y = top + 75
        d.text(260, top - 20, title, 23)
        d.path(f"M {left} {top} V {bottom} H {right}", INK)
        for y, value in ((top, "2"), (point_y, "1"), (bottom, "0")):
            d.path(f"M {left-5} {y} H {left}")
            d.text(left-17, y+8, value, 22, anchor="end")
        d.text(48, top + 44, "y", 23)
        for value in range(maximum+1):
            x = left + width * value / maximum
            d.path(f"M {x} {bottom} V {bottom+5}")
            d.text(x, bottom+30, str(value), 22)
        d.text(472, bottom+8, "x", 23)
        d.path(f"M {left} {point_y} H {point_x} V {bottom}", BLUE, dash="5 5")
        d.circle(point_x, point_y)
        d.text(point_x+18, point_y-13, "(1, 1)", 24, BLUE, anchor="start")
        fraction = "halfway across" if maximum == 2 else "one quarter across"
        d.text(270, bottom+70, fraction, 22, BLUE)
    d.text(260, 652, "Axis limits change the pixel position.", 22, GRAY)
    d.text(260, 683, "The selected point does not change.", 22, GRAY)
    return d.finish()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drawings = {"principal_coefficients.svg": principal_coefficients(),
                "anchor_coordinates.svg": anchor_coordinates()}
    if not args.check:
        ASSETS.mkdir(parents=True, exist_ok=True)
    for name, svg in drawings.items():
        path = ASSETS / name
        if args.check:
            if not path.exists() or path.read_text() != svg:
                raise SystemExit(f"Regenerate {path}")
        else:
            path.write_text(svg)


if __name__ == "__main__":
    main()
