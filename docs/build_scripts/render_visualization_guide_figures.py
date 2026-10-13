#!/usr/bin/env python3
"""Draw the exact examples used to interpret views in the visualization guide.

These are mathematical schematics, not screenshots of a package renderer.
They show the F2 ring interval, ranks from (1,1) in the rational square module,
and restrictions of two closed square summands to a diagonal window.
"""
from argparse import ArgumentParser
from pathlib import Path
from render_relative_figures import Drawing, BLUE, TEAL, ORANGE, MUTED

TARGET = Path(__file__).resolve().parents[1] / "assets" / "visualization_guide"


def rectangle(d, x, y, width, height, fill, stroke="none", linewidth=1):
    d.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="{linewidth}"/>')


def finish(d):
    return d.finish().replace("render_relative_figures.py", "render_visualization_guide_figures.py")


def ring_barcode():
    d = Drawing(570, "A ring and its interval in first homology",
                "Over F2, the eight outer maximal cells of a three by three cubical image enter at zero. "
                "The central cell enters at five. Their faces enter with them. First homology is "
                "one dimensional from zero included to five excluded. This schematic identifies "
                "the interval without choosing a cycle from the reduction.")
    d.text(260, 38, "The cell that fills the hole", 26)
    for center, filled, title in ((137, False, "0 ≤ t < 5"), (387, True, "t ≥ 5")):
        d.text(center, 91, title, 25)
        for row in range(3):
            for col in range(3):
                middle = row == 1 and col == 1
                if middle and not filled:
                    continue
                color = "#fbd5b6" if middle else "#d5e6f4"
                rectangle(d, center - 72 + 48 * col, 127 + 48 * row, 48, 48, color, BLUE)
        d.text(center, 317, "H₁ = F₂" if not filled else "H₁ = 0", 26)
    d.line(228, 198, 290, 198, arrow=True)
    d.text(260, 368, "One interval in first homology", 24)
    d.line(104, 421, 410, 421, BLUE, 6)
    d.circle(104, 421, BLUE)
    d.circle(410, 421, "white")
    d.text(104, 464, "0", 25)
    d.text(410, 464, "5", 25)
    d.text(458, 429, "t", 25)
    d.text(260, 510, "Filled end included; open end excluded.", 22)
    d.text(260, 546, "t is the entry threshold of the cells.", 22, MUTED)
    return finish(d)


def rank_section():
    d = Drawing(752, "Ranks from a fixed source in the square module",
                "The module is rational one dimensional on the closed square from zero to two in both "
                "coordinates and zero elsewhere. With source p=(1,1), targets q in the closed square "
                "from one to two have rank one. Comparable targets outside the support have rank zero. "
                "If either target coordinate is less than one, there is no forward structure map from p. "
                "All parameters in this example are represented. The finite viewing box is zero to three.")
    d.text(260, 38, "Keep p = (1, 1) fixed", 26)
    d.text(260, 77, "Vary the target q = (x, y)", 23)
    x0, y0, scale = 102, 418, 106
    px = lambda t: x0 + scale * t
    py = lambda t: y0 - scale * t
    rectangle(d, px(0), py(3), 3*scale, 3*scale, "white", "#a0acb8")
    rectangle(d, px(0), py(3), scale, 3*scale, "#e2e8f0")
    rectangle(d, px(1), py(1), 2*scale, scale, "#e2e8f0")
    rectangle(d, px(1), py(2), scale, scale, "#aacfe5", BLUE, 3)
    # The left and bottom edges belong to the comparable region.
    d.line(px(1), py(1), px(1), py(3), BLUE, 2)
    d.line(px(1), py(1), px(3), py(1), BLUE, 2)
    d.line(px(0), py(0), px(3)+20, py(0), MUTED, 2, arrow=True)
    d.line(px(0), py(0), px(0), py(3)-20, MUTED, 2, arrow=True)
    for t in range(4):
        d.text(px(t), py(0)+33, str(t), 22)
        d.text(px(0)-27, py(t)+8, str(t), 22)
    d.text(px(3)+35, py(0)+8, "x", 24)
    d.text(px(0)-2, py(3)-38, "y", 24)
    d.text(px(1.5), py(1.5)+9, "rank 1", 23)
    d.text(px(2.05), py(2.60)+8, "rank 0", 23)
    d.text(px(1.68), py(0.42)+8, "no forward map", 22, MUTED)
    d.circle(px(1), py(1), ORANGE, ORANGE, radius=7)
    d.text(px(1)+16, py(1)+32, "p", 24, ORANGE, "start")
    d.text(260, 499, "Blue: p ≤ q inside the support", 23)
    d.text(260, 534, "M(p ≤ q) = [1]", 25, BLUE)
    d.text(260, 581, "White: p ≤ q outside the support", 23)
    d.text(260, 616, "M(p ≤ q): ℚ → 0", 25)
    d.text(260, 663, "Gray: x < 1 or y < 1", 23)
    d.text(260, 698, "The order supplies no map from p.", 22, MUTED)
    d.text(260, 737, "The top and right frame only crop the view.", 21, MUTED)
    return finish(d)


def slice_window():
    d = Drawing(713, "Full diagonal intervals and a smaller window",
                "The direct sum of the closed square modules [0,2]^2 and [1,3]^2 restricts to "
                "closed intervals [0,2] and [1,3] on q(t)=(t,t). The window from t=3/2 to t=7/4 "
                "meets both intervals. Restricting the computation to that window returns two "
                "copies of the closed interval [3/2,7/4] with both ends censored. The restricted "
                "answer establishes multiplicity two in the window but does not determine the "
                "ambient endpoints. The lower panel magnifies the window and has a different scale.")
    d.text(260, 38, "Following q(t) = (t, t)", 26)
    d.text(260, 86, "Whole line: two closed intervals", 24)
    x = lambda t: 72 + 124*t
    rectangle(d, x(1.5), 110, x(1.75)-x(1.5), 162, "#fef0d6")
    for t in range(4):
        d.line(x(t), 113, x(t), 256, "#dbe2e8", 1, dash="3 4")
        d.text(x(t), 298, str(t), 23)
    for low, high, y, color in ((0, 2, 155, BLUE), (1, 3, 224, TEAL)):
        d.line(x(low), y, x(high), y, color, 6)
        d.circle(x(low), y, color, color)
        d.circle(x(high), y, color, color)
    d.text(483, 298, "t", 24)
    d.line(x(1.5), 313, x(1.75), 313, ORANGE, 4)
    d.text(260, 353, "Window: 3/2 ≤ t ≤ 7/4", 24, ORANGE)
    d.line(34, 379, 486, 379, "#cbd5e1", 1)
    d.text(260, 421, "Window restriction, magnified", 24)
    rectangle(d, 135, 441, 250, 151, "#fef0d6")
    d.line(135, 496, 385, 496, BLUE, 6)
    for xx in (135, 385):
        d.text(xx, 482, "?", 27, ORANGE)
    d.text(260, 542, "multiplicity 2", 24)
    d.text(135, 581, "3/2", 24)
    d.text(385, 581, "7/4", 24)
    d.text(445, 581, "t", 24)
    d.text(260, 637, "Both classes exist throughout this window.", 22)
    d.text(260, 677, "? leaves their ambient endpoints unknown.", 22, MUTED)
    return finish(d)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drawings = {"ring_barcode.svg": ring_barcode(), "rank_section.svg": rank_section(),
                "slice_window.svg": slice_window()}
    if not args.check:
        TARGET.mkdir(parents=True, exist_ok=True)
    for name, content in drawings.items():
        path = TARGET / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"Figure differs from its source: {path}")
        else:
            path.write_text(content)
    print("Visualization schematics match their source." if args.check else "Rendered visualization schematics.")


if __name__ == "__main__":
    main()
