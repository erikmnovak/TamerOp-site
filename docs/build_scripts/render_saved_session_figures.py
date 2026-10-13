"""Draw the exact selections in the saved square-module example."""
from pathlib import Path
import argparse

OUT = Path(__file__).resolve().parents[1] / "assets/saved_sessions/square_selections.svg"


def render():
    # Independent support formula for the labelled stalks in the schematic.
    dimension = lambda p: int(all(0 <= t <= 2 for t in p))
    x, y, b, z = (.5, .5), (1.5, 1.5), (2, 1), (2.5, 1)
    assert [dimension(p) for p in (x, y, b, z)] == [1, 1, 1, 0]
    assert all(a <= b for a, b in zip(x, y))
    X = lambda t: 120 + 104 * t
    Y = lambda t: 390 - 104 * t
    rows = ['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="690" viewBox="0 0 520 690" role="img" aria-labelledby="title desc">',
            '<title id="title">Three saved selections in a closed square module</title>',
            '<desc id="desc">The interior points x and y have rational vector spaces and their map is the identity. The boundary point b has the same rational space. The point z beyond the square has zero space. All four parameters belong to the encoding domain.</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#156b91"/></marker></defs>',
            '<rect width="520" height="690" fill="white"/>',
            '<g font-family="DejaVu Sans,sans-serif" font-size="24" fill="#19334b">',
            '<text x="260" y="35" text-anchor="middle">The selections we keep</text>',
            '<text x="260" y="75" text-anchor="middle">ℚ on the closed square; 0 outside</text>',
            f'<rect x="{X(0)}" y="{Y(2)}" width="208" height="208" fill="#dcebf3" stroke="#156b91" stroke-width="3"/>',
            f'<path d="M {X(-.5)} {Y(2.65)} V {Y(-.5)} H {X(3.15)}" fill="none" stroke="#667782" stroke-width="1.5"/>']
    for tick in (0, 1, 2):
        rows += [f'<text x="{X(tick)}" y="475" text-anchor="middle">{tick}</text>',
                 f'<text x="55" y="{Y(tick)+8}" text-anchor="end">{tick}</text>']
    rows += ['<text x="458" y="450">x₁</text>', '<text x="61" y="106">x₂</text>',
             f'<path d="M {X(.5)} {Y(.5)} L {X(1.43)} {Y(1.43)}" stroke="#156b91" stroke-width="2.5" marker-end="url(#arrow)"/>',
             '<text x="192" y="272">[1]</text>']
    for label, point, dx, dy, color in [('x', x, -25, -10, '#156b91'), ('y', y, 13, -12, '#156b91'), ('b', b, -25, -13, '#a04c13'), ('z', z, 14, 8, '#a04c13')]:
        rows += [f'<circle cx="{X(point[0])}" cy="{Y(point[1])}" r="6" fill="{color}"/>',
                 f'<text x="{X(point[0])+dx}" y="{Y(point[1])+dy}">{label}</text>']
    rows += ['<text x="260" y="520" text-anchor="middle" font-size="22">x = (1/2, 1/2), y = (3/2, 3/2)</text>',
             '<text x="260" y="558" text-anchor="middle">M(x ≤ y) = [1]</text>',
             '<text x="260" y="597" text-anchor="middle">M(b) = ℚ,  b = (2, 1)</text>',
             '<text x="260" y="636" text-anchor="middle">M(z) = 0,  z = (5/2, 1)</text>',
             '<text x="260" y="678" text-anchor="middle" font-size="21">All four parameters are represented.</text>', '</g></svg>']
    return '\n'.join(rows) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render()
    if args.check:
        if not OUT.exists() or OUT.read_text() != result:
            raise SystemExit('Saved-session schematic needs regeneration')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result)
