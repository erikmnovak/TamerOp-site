"""Draw the exact two-assignment calculation in docs/exact_matching.md.

The dashed affine costs and their solid minimum are analytic values, not
samples from the optimizer. Run --check to verify the tracked SVG.
"""
from pathlib import Path
from fractions import Fraction
import argparse
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--check',action='store_true')
a=p.parse_args()
# The two available assignments delete opposite M intervals.
f=lambda h:1+h/2
g=lambda h:Fraction(3,2)-h/2
assert min(f(Fraction(0)),g(Fraction(0)))==1
assert f(Fraction(1,2))==g(Fraction(1,2))==Fraction(5,4)
assert min(f(Fraction(1)),g(Fraction(1)))==1
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="385" viewBox="0 0 560 385" role="img" aria-labelledby="title desc">
<title id="title">An optimal assignment changes at offset one half</title>
<desc id="desc">The two dashed costs are 1 plus h over 2 and 3 over 2 minus h over 2. Their solid minimum is 1 at either endpoint and peaks at 5 over 4 when h is one half. Horizontal coordinate is the offset h in y equals x plus h; vertical coordinate is weighted bottleneck cost.</desc>
<rect x="1" y="1" width="558" height="383" rx="10" fill="white" stroke="#cbd5df"/>
<g font-family="DejaVu Sans, sans-serif" fill="#183549">
<text x="280" y="31" text-anchor="middle" font-size="19">The less costly assignment changes at h = 1/2</text>
<text x="75" y="64" font-size="16">Weighted cost</text>
<path d="M75 290H497 M75 290V76" fill="none" stroke="#465f72" stroke-width="2"/>
<g fill="none" stroke="#d4dce2"><path d="M75 268H495 M75 178H495 M75 88H495"/></g>
<g font-size="16" text-anchor="end"><text x="62" y="274">1</text><text x="62" y="184">5/4</text><text x="62" y="94">3/2</text></g>
<path d="M75 268L495 88" fill="none" stroke="#3876a2" stroke-width="2.5" stroke-dasharray="7 5"/>
<path d="M75 88L495 268" fill="none" stroke="#b06629" stroke-width="2.5" stroke-dasharray="3 5"/>
<path d="M75 268L285 178L495 268" fill="none" stroke="#183549" stroke-width="4"/>
<path d="M285 178V290" fill="none" stroke="#748897" stroke-dasharray="3 5"/>
<g fill="#183549"><circle cx="75" cy="268" r="4"/><circle cx="285" cy="178" r="5"/><circle cx="495" cy="268" r="4"/></g>
<g font-size="16" text-anchor="middle"><text x="75" y="312">0</text><text x="285" y="312">1/2</text><text x="495" y="312">1</text><text x="285" y="337">Offset h in the line y = x + h</text></g>
<text x="111" y="108" font-size="16" fill="#965322">3/2 − h/2</text>
<text x="387" y="108" font-size="16" fill="#28658f">1 + h/2</text>
<text x="285" y="244" text-anchor="middle" font-size="16">Solid: minimum of the two costs</text>
<text x="285" y="366" text-anchor="middle" font-size="15">Each dashed line represents a different deleted interval.</text>
</g></svg>
'''
path=Path(__file__).with_name('cost_switch.svg')
if a.check:
 assert path.read_text()==svg, 'Regenerate cost_switch.svg'
 print('Exact cost-switch graph agrees with its generator.')
else:path.write_text(svg)
