"""Render the cumulative signed weights used in the composition recipe."""
from pathlib import Path
import argparse

OUT = Path(__file__).resolve().parents[1] / "assets/composition/cumulative_weights.svg"
ATOMS = ((0, 0, 1), (2, 0, -1), (0, 2, -1), (2, 2, 1))


def render():
    rows = ['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="790" viewBox="0 0 520 790" role="img" aria-labelledby="title desc">',
            '<title id="title">Recovering the square from signed weights</title>',
            '<desc id="desc">At one comma one the lower positive atom gives one. At two comma one the lower positive and negative atoms cancel. Shaded rectangles select atoms below the query in both coordinates.</desc>',
            '<rect width="520" height="790" fill="white"/>',
            '<g font-family="DejaVu Sans, sans-serif" font-size="22" fill="#19334b">']
    for top, qx, expected in ((0, 1, 1), (390, 2, 0)):
        qy = 1
        total = sum(w for x, y, w in ATOMS if x <= qx and y <= qy)
        assert total == expected
        def x(t): return 115 + 112 * t
        def y(t): return top + 280 - 85 * t
        rows += [f'<text x="260" y="{top+30}" text-anchor="middle">Query ({qx}, 1)</text>',
                 f'<rect x="{x(-.4)}" y="{y(qy)}" width="{x(qx)-x(-.4)}" height="{y(-.4)-y(qy)}" fill="#e5f0f5"/>',
                 f'<path d="M {x(-.4)} {y(qy)} H {x(qx)} V {y(-.4)}" fill="none" stroke="#517b94" stroke-width="2"/>',
                 f'<path d="M {x(-.4)} {y(-.4)} H {x(2.6)} M {x(-.4)} {y(-.4)} V {y(2.6)}" fill="none" stroke="#667782" stroke-width="1.5"/>']
        for t in (0, 1, 2):
            rows += [f'<text x="{x(t)}" y="{y(-.4)+27}" text-anchor="middle">{t}</text>',
                     f'<text x="{x(-.4)-14}" y="{y(t)+7}" text-anchor="end">{t}</text>']
        rows += [f'<text x="{x(2.7)}" y="{y(-.4)+7}">x</text>',
                 f'<text x="{x(-.4)-7}" y="{y(2.7)}">y</text>']
        for ax, ay, weight in ATOMS:
            included = ax <= qx and ay <= qy
            rows += [f'<circle cx="{x(ax)}" cy="{y(ay)}" r="7" fill="{"#156b91" if included else "white"}" stroke="#156b91" stroke-width="2"/>',
                     f'<text x="{x(ax)+13}" y="{y(ay)-11}" font-size="24">{"+1" if weight>0 else "−1"}</text>']
        rows += [f'<path d="M {x(qx)-7} {y(qy)-7} L {x(qx)+7} {y(qy)+7} M {x(qx)-7} {y(qy)+7} L {x(qx)+7} {y(qy)-7}" stroke="#a04c13" stroke-width="3"/>',
                 f'<text x="260" y="{top+375}" text-anchor="middle">Sum: {"+1 = 1" if expected else "+1 − 1 = 0"}</text>']
    rows += ['<text x="260" y="786" text-anchor="middle" font-size="19">Filled dots contribute; the cross marks the query.</text>', '</g></svg>']
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = render()
    if args.check:
        if not OUT.exists() or OUT.read_text() != result:
            raise SystemExit("Composition diagram needs regeneration")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result)
