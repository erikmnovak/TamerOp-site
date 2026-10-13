#!/usr/bin/env python3
"""Render authored coordinate schematics for generated submodules.

The assertions check the small rational example independently of package code.
Use --check to verify that the committed SVGs match this generator.
"""
from argparse import ArgumentParser
from pathlib import Path
from xml.sax.saxutils import escape

DESTINATION = Path(__file__).resolve().parents[1] / 'assets' / 'generated_submodules'
INK = '#172b42'
BLUE = '#245c99'
ORANGE = '#9a470b'


def opening(title, desc, height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="{height}" viewBox="0 0 560 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<!-- Authored mathematical schematic; see render_generated_submodule_figures.py. -->',
            f'<rect width="560" height="{height}" fill="white"/>',
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 Z" fill="#526576"/></marker></defs>',
            '<g font-family="DejaVu Sans, sans-serif" text-anchor="middle" fill="#172b42">']


def text(parts, x, y, value, size=24, color=INK):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>')


def arrow(parts, path, color='#526576', dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.4"{dash} marker-end="url(#arrow)"/>')


def image_coordinates():
    # For the diagonal line, I_v N_uv = M_uv I_u = [1].
    inclusion_u = (1, 1)
    ambient_map = (0, 1)
    projection_u = (-1, 1)
    assert sum(a*b for a,b in zip(ambient_map, inclusion_u)) == 1
    assert sum(a*b for a,b in zip(projection_u, inclusion_u)) == 0
    p = opening('Maps induced on a generated line',
        'A commuting square: N(u) and N(v) are Q, with identity map across the top. '
        'M(u) is Q squared and M(v) is Q, with row matrix zero, one across the bottom. '
        'Inclusions are the column one, one on the left and scalar one on the right.', 570)
    text(p, 280, 38, 'Follow the generated coordinate a', 26)
    text(p, 105, 115, 'N(u) = Q', 27, BLUE)
    text(p, 455, 115, 'N(v) = Q', 27, BLUE)
    arrow(p, 'M 178 105 H 375')
    text(p, 280, 81, 'Nᵤᵥ = [1]', 24, BLUE)
    text(p, 105, 165, 'a', 25, BLUE)
    text(p, 455, 165, 'a', 25, BLUE)
    arrow(p, 'M 105 187 V 334')
    arrow(p, 'M 455 187 V 334')
    text(p, 193, 245, 'Iᵤ = [1; 1]', 23)
    text(p, 365, 245, 'Iᵥ = [1]', 23)
    text(p, 105, 380, 'M(u) = Q²', 27, ORANGE)
    text(p, 455, 380, 'M(v) = Q', 27, ORANGE)
    arrow(p, 'M 184 370 H 371')
    text(p, 280, 346, 'Mᵤᵥ = [0  1]', 23, ORANGE)
    text(p, 105, 430, '(a, a)', 25, ORANGE)
    text(p, 455, 430, 'a', 25, ORANGE)
    text(p, 280, 492, 'Iᵥ Nᵤᵥ = Mᵤᵥ Iᵤ = [1]', 26)
    text(p, 280, 537, 'Q denotes the rational coefficient field.', 22)
    return '\n'.join(p+['</g></svg>', ''])


def nonsplit():
    # On a two-vertex chain, identity(1) = 1 cannot lie in the proposed zero target.
    assert 1 * 1 != 0
    p = opening('A quotient need not be a complementary submodule',
        'Three diagrams on the chain u less than v. Ambient module: Q maps by identity to Q. '
        'Tail submodule: zero maps to Q. Proposed complement: Q maps to zero, '
        'but the ambient identity sends its scalar one to one outside that zero space.', 665)
    text(p, 280, 37, 'One ambient identity, two proposed parts', 25)
    text(p, 96, 88, 'vertex u', 23)
    text(p, 459, 88, 'vertex v', 23)
    text(p, 280, 132, 'Ambient module M', 24)
    text(p, 96, 181, 'Q', 31)
    text(p, 459, 181, 'Q', 31)
    arrow(p, 'M 136 171 H 418')
    text(p, 280, 160, 'identity', 22)
    text(p, 280, 258, 'Submodule N: closed under the map', 24, BLUE)
    text(p, 96, 311, '0', 31, BLUE)
    text(p, 459, 311, 'Q', 31, BLUE)
    arrow(p, 'M 136 301 H 418')
    text(p, 280, 287, 'zero map', 22)
    text(p, 280, 374, 'Proposed complement L', 24, ORANGE)
    text(p, 96, 427, 'Q', 31, ORANGE)
    text(p, 459, 427, '0', 31, ORANGE)
    arrow(p, 'M 136 417 H 418', dashed=True)
    text(p, 280, 405, 'would have to be zero', 22)
    text(p, 280, 486, 'But the ambient map sends 1 to 1.', 24)
    text(p, 280, 526, 'Its image leaves the proposed space L(v).', 23)
    text(p, 280, 585, 'The quotient M/N has dimensions (1, 0).', 23)
    text(p, 280, 627, 'It does not supply an included complement.', 23)
    return '\n'.join(p+['</g></svg>', ''])


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, contents in {'image_coordinates.svg': image_coordinates(), 'nonsplit.svg': nonsplit()}.items():
        path = DESTINATION/name
        if args.check:
            if not path.exists() or path.read_text() != contents:
                raise SystemExit(f'Regenerate {path}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents)


if __name__ == '__main__':
    main()
