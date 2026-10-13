#!/usr/bin/env python3
"""Draw the finite V-diagram and its induced colimit map (an authored schematic)."""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path

DEST = Path(__file__).resolve().parents[1] / 'assets' / 'transport' / 'colimit_addition.svg'
INK = '#25333b'
BLUE = '#156b91'
ORANGE = '#b45323'


def text(x, y, s, size=22, anchor='middle', color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(s)}</text>'


def arrow(x1, y1, x2, y2, color='blue'):
    shade = BLUE if color == 'blue' else ORANGE
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{shade}" stroke-width="2.6" fill="none" marker-end="url(#{color})"/>'


def render():
    # N has relation columns e1-e2 and e1-e3 in its direct sum k^3.
    # Its quotient Q_N=(1,1,1) kills both, and W_N=e3 is a section.
    rel = ((1, 1), (-1, 0), (0, -1))
    q = (1, 1, 1)
    assert [sum(q[i] * rel[i][j] for i in range(3)) for j in range(2)] == [0, 0]
    w = (0, 0, 1)
    assert sum(a*b for a,b in zip(q,w)) == 1
    # The component map from M=(0,k,k) includes its last two summands.
    f = ((0, 0), (1, 0), (0, 1))
    assert tuple(sum(q[i]*f[i][j] for i in range(3)) for j in range(2)) == (1, 1)
    e = [text(260, 35, 'An induced map between colimits', 25),
         text(130, 85, 'M = (0, k, k)'), text(390, 85, 'N = (k, k, k)')]
    for cx, source, labels in [(130, '1: 0', ('0', '0')), (390, '1: k', ('1', '1'))]:
        e += [text(cx-65, 143, '2: k'), text(cx+65, 143, '3: k'),
              text(cx, 262, source), arrow(cx-10, 230, cx-56, 161),
              arrow(cx+10, 230, cx+56, 161),
              text(cx-51, 210, labels[0], 20), text(cx+51, 210, labels[1], 20)]
    e += [text(260, 305, 'The map M → N is identity at 2 and 3.', 21),
          text(260, 337, 'At 1 it is the unique map 0 → k.', 21),
          '<path d="M30 360 H490" stroke="#c8d5dc"/>',
          text(130, 402, 'colim M = k²', 24), text(390, 402, 'colim N = k', 24),
          text(130, 441, '(x, y)', 23), arrow(208, 434, 308, 434, 'orange'),
          text(390, 441, 'x + y', 23),
          text(260, 486, 'In N, the relations identify e₁ = e₂ = e₃.', 21),
          text(260, 519, 'Thus x e₂ + y e₃ becomes (x + y) e₃.', 21)]
    return '\n'.join(['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="548" viewBox="0 0 520 548" role="img" aria-labelledby="title desc">',
        '<title id="title">The addition map induced on two colimits</title>',
        '<desc id="desc">Two modules on 1 below 2 and 3. M has spaces zero, k, k and zero arrows; N has k at every vertex and identity arrows. The natural map is identity at 2 and 3. After collapsing the poset to one point, the colimits are k squared and k, and the induced map sends x,y to x+y.</desc>',
        '<defs>',*[f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>' for name,color in [('blue',BLUE),('orange',ORANGE)]],'</defs>',
        '<rect width="520" height="548" fill="white"/>','<g font-family="DejaVu Sans,sans-serif">',*e,'</g></svg>',''])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    source=render()
    if args.check:
        if not DEST.exists() or DEST.read_text()!=source: raise SystemExit(f'Stale figure: {DEST}')
    else:
        DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(source)
    print('Colimit addition relations and figure verified.')

if __name__=='__main__': main()
