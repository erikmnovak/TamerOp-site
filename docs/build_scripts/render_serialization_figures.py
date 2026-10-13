#!/usr/bin/env python3
"""Draw the coordinate example in the serialization implementation account.

This is an authored schematic. Run with --check to compare the SVG with
its source and verify the displayed basis change using exact integer data.
"""

from argparse import ArgumentParser
from pathlib import Path
from xml.sax.saxutils import escape

DESTINATION = Path(__file__).resolve().parents[1] / "assets" / "serialization"


def basis_coordinates():
    # Columns of S are the F basis vectors expressed in basis E.
    A = (1, 2)
    S = ((1, 1), (0, 1))
    x_f = (0, 1)
    x_e = tuple(sum(row[j] * x_f[j] for j in range(2)) for row in S)
    a_f = tuple(sum(A[i] * S[i][j] for i in range(2)) for j in range(2))
    assert x_e == (1, 1) and a_f == (1, 3)
    assert sum(a * x for a, x in zip(A, x_e)) == 3
    assert sum(a * x for a, x in zip(a_f, x_f)) == 3
    assert S[0][0] * S[1][1] - S[0][1] * S[1][0] == 1

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="690" '
             'viewBox="0 0 520 690" role="img" aria-labelledby="title desc">',
             '<title id="title">One vector in two coordinate bases</title>',
             '<desc id="desc">The old basis is E equals e1, e2. The new basis '
             'is F equals e1, e1 plus e2. The vector e1 plus e2 has E '
             'coordinates one, one and F coordinates zero, one. Applying S '
             'changes the F coordinates to E coordinates. Applying A in the '
             'old basis or AS in the new basis gives the same answer, three.</desc>',
             '<!-- Authored schematic; regenerate with render_serialization_figures.py. -->',
             '<rect width="520" height="690" fill="white"/>',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
             'refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 Z" '
             'fill="#526576"/></marker></defs>',
             '<g font-family="DejaVu Sans, sans-serif" fill="#172b42" text-anchor="middle">']

    def text(x, y, value, size=25, fill="#172b42"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">{escape(value)}</text>')

    def arrow(path):
        parts.append(f'<path d="{path}" fill="none" stroke="#526576" '
                     'stroke-width="2.5" marker-end="url(#arrow)"/>')

    def vector(x, y, a, b, color):
        parts.append(f'<path d="M {x-18} {y-13} H {x-26} V {y+57} H {x-18} '
                     f'M {x+18} {y-13} H {x+26} V {y+57} H {x+18}" '
                     f'fill="none" stroke="{color}" stroke-width="2"/>')
        text(x, y+12, str(a), 29, color)
        text(x, y+47, str(b), 29, color)

    text(260, 36, "One vector: x = e₁ + e₂", 27)
    text(260, 81, "Old basis E = (e₁, e₂)", 24, "#245c99")
    text(260, 117, "New basis F = (e₁, e₁ + e₂)", 24, "#9a470b")
    text(97, 180, "[x]F", 25, "#9a470b")
    vector(97, 214, 0, 1, "#9a470b")
    text(413, 249, "3", 34)
    arrow("M 152 239 H 364")
    text(261, 213, "AS = [1  3]", 24, "#9a470b")
    arrow("M 97 299 V 451")
    text(225, 360, "S converts F", 24)
    text(225, 393, "coordinates to E", 24)
    text(413, 388, "=", 32)
    text(97, 478, "[x]E", 25, "#245c99")
    vector(97, 510, 1, 1, "#245c99")
    text(413, 545, "3", 34)
    arrow("M 152 535 H 364")
    text(261, 508, "A = [1  2]", 24, "#245c99")
    text(260, 616, "Same vector and same image.", 25)
    text(260, 655, "The matrix depends on the basis.", 24)
    return "\n".join(parts + ["</g></svg>", ""])


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {"basis_coordinates.svg": basis_coordinates()}
    for name, contents in outputs.items():
        path = DESTINATION / name
        if args.check:
            if not path.exists() or path.read_text() != contents:
                raise SystemExit(f"Regenerate {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents)


if __name__ == "__main__":
    main()
