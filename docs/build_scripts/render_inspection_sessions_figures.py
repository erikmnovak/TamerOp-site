#!/usr/bin/env python3
"""Generate the two explanatory schematics used by the inspection account.

These are authored mathematical examples, not screenshots of a live viewer.
Only the Python standard library is needed. Use --check to verify the assets.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "inspection_sessions"
BLUE = "#156b91"
ORANGE = "#b45323"
INK = "#25333b"


def text(x, y, value, *, size=23, anchor="start", color=INK, weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{color}" font-weight="{weight}">{escape(value)}</text>')


def svg(title, description, height, elements):
    return '\n'.join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="520" '
        f'height="{height}" viewBox="0 0 520 {height}" role="img" '
        'aria-labelledby="title description">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="description">{escape(description)}</desc>',
        '<defs>',
        f'<marker id="blue-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="{BLUE}"/></marker>',
        f'<marker id="orange-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="{ORANGE}"/></marker>',
        '</defs>',
        f'<rect width="520" height="{height}" fill="white"/>',
        '<g font-family="DejaVu Sans, sans-serif">',
        *elements, '</g>', '</svg>', '',
    ])


def parameter_order():
    # The product order requires both coordinates to increase. A constant
    # encoding label on the square cannot add a comparison in the plane.
    x = (Fraction(1, 2), Fraction(3, 2))
    y = (Fraction(3, 2), Fraction(1, 2))
    assert all(0 < z < 2 for p in (x, y) for z in p)
    assert not all(a <= b for a, b in zip(x, y))
    assert not all(b <= a for a, b in zip(x, y))
    e = [
        text(260, 37, 'Same label, different parameters', anchor='middle', size=25),
        text(260, 75, 'Closed support [0, 2] × [0, 2]', anchor='middle'),
        '<rect x="120" y="120" width="280" height="280" fill="#e7f2f7" stroke="#156b91" stroke-width="3"/>',
        '<path d="M 120 102 V 422 M 100 400 H 449" fill="none" stroke="#46545e" stroke-width="2"/>',
        text(461, 408, 'p₁'), text(107, 103, 'p₂', anchor='end'),
        text(107, 429, '0', anchor='end'), text(400, 429, '2', anchor='middle'),
        text(105, 129, '2', anchor='end'),
        '<path d="M 120 190 H 190 V 400 M 120 330 H 330 V 400" fill="none" stroke="#7e9baa" stroke-width="1.5" stroke-dasharray="5 5"/>',
        f'<circle cx="190" cy="190" r="8" fill="{BLUE}"/>',
        f'<rect x="322" y="322" width="16" height="16" fill="{ORANGE}"/>',
        text(153, 163, 'x = (½, 3/2)', color=BLUE),
        text(254, 305, 'y = (3/2, ½)', color=ORANGE),
        text(260, 482, 'qₓ = qᵧ = q,   N(q) = ℚ', anchor='middle', size=25),
        '<path d="M 35 509 H 485" stroke="#d4dce0" stroke-width="1.5"/>',
        text(260, 552, 'x₁ < y₁   and   x₂ > y₂', anchor='middle', size=25),
        text(260, 595, 'Neither x ≤ y nor y ≤ x.', anchor='middle'),
        text(260, 637, 'No structure map in either direction.', anchor='middle', size=22),
    ]
    return svg('Parameter order survives finite encoding',
               'The rational square module has the same finite label q at x=(1/2,3/2) and y=(3/2,1/2). '
               'The first coordinate increases from x to y while the second decreases. '
               'Neither pair is comparable in product order, so the original module prescribes no map between them.', 664, e)


def draft_diamond():
    # Each entered coefficient acts on Q. Their two path products disagree.
    maps = {(1, 2): Fraction(1), (2, 4): Fraction(1),
            (1, 3): Fraction(1), (3, 4): Fraction(2)}
    first = maps[2, 4] * maps[1, 2]
    second = maps[3, 4] * maps[1, 3]
    assert first == 1 and second == 2 and first != second
    e = [
        text(260, 36, 'A draft with two different composites', anchor='middle', size=23),
        text(260, 73, 'Every stalk is ℚ; arrows act by scalars.', anchor='middle', size=22),
        f'<path d="M 241 398 L 108 287" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#blue-arrow)"/>',
        f'<path d="M 107 239 L 238 134" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#blue-arrow)"/>',
        f'<path d="M 279 398 L 412 287" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#orange-arrow)"/>',
        f'<path d="M 413 239 L 282 134" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#orange-arrow)"/>',
    ]
    for label, cx, cy in [(1, 260, 416), (2, 84, 263), (3, 436, 263), (4, 260, 116)]:
        e.append(f'<circle cx="{cx}" cy="{cy}" r="27" fill="white" stroke="#46545e" stroke-width="2"/>')
        e.append(text(cx, cy + 8, str(label), anchor='middle', size=25))
    e += [
        text(146, 351, '1', color=BLUE, size=26), text(153, 180, '1', color=BLUE, size=26),
        text(361, 351, '1', color=ORANGE, size=26), text(358, 180, '2', color=ORANGE, size=26),
        f'<path d="M 35 491 H 95" fill="none" stroke="{BLUE}" stroke-width="3"/>',
        text(112, 499, '1 → 2 → 4:   1 × 1 = 1', color=BLUE),
        f'<path d="M 35 539 H 95" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="8 5"/>',
        text(112, 547, '1 → 3 → 4:   2 × 1 = 2', color=ORANGE),
        text(260, 596, 'A module requires these maps to agree.', anchor='middle', size=22),
    ]
    return svg('The diamond draft fails path independence',
               'All four stalks are rational one dimensional spaces. Solid arrows 1 to 2 and 2 to 4 have coefficient one. '
               'Dashed arrows 1 to 3 and 3 to 4 have coefficients one and two. '
               'The resulting maps from 1 to 4 differ, so this is an invalid draft, not a module.', 625, e)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = {'parameter_order.svg': parameter_order(), 'draft_diamond.svg': draft_diamond()}
    for name, content in outputs.items():
        path = ASSETS / name
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                raise SystemExit(f'Figure differs from generated source: {path}')
        else:
            ASSETS.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    print('Inspection schematics match their source.' if args.check else 'Wrote inspection schematics.')


if __name__ == '__main__':
    main()
