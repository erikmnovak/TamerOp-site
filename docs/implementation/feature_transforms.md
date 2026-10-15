# From sampled landscapes to ambient queries

A sampled landscape records heights at points along selected lines. To draw
those heights over the original parameter domain, we need to recover the
location of each sample and the units in which its height was measured.
The line's basepoint and direction provide both pieces of information. This
account explains that step and the numerical information it preserves. The [features guide](../tutorials/features.ipynb)
works through a finite module supported on a square before using the same display
contract for other scalar fields. Its prepared viewers for landscape layers and coordinate sections
keep the samples fixed while the selected scalar function or drawing plane
changes.

## Preserve the line parameter before placing a height

`MPLandscape` stores an array indexed by direction, offset, landscape layer and
line parameter. At a point on an ordinary barcode, each interval contributes a
tent: its height is the distance to the nearer endpoint while the point lies
inside the interval, and zero outside. Layer $k$ records the $k$th largest
height. Thus the layer index selects a different scalar function on the same
line. The stored slice weights support aggregation and integration over a sampled
family. A pointwise landscape height does not involve those weights.
`mp_landscape` first restricts the encoded module to chosen lines, obtains their
barcodes and evaluates ordinary landscape tents on the common parameter grid.
It retains the normalized directions used by that computation. In particular,
the workflow normalizes supplied directions in the one-norm, the sum of absolute coordinate values: requesting `(1,1)`
stores `(1/2,1/2)`. Treating its parameter as either ambient coordinate would
therefore put both locations and heights on the wrong scale.

The adapter takes the actual basepoint of each stored offset. If a line has
basepoint `b`, positive direction `d`, and stored parameter `t`, its location is

```math
x=b+td.
```

Here $b$ is the line's basepoint, $d$ its direction and $t$ the stored parameter.
The caller supplies `b` explicitly, since a scalar offset or a plotting label
alone need not determine its convention. For each requested grid point,
`ambient_landscape` solves for `t` using the largest direction component and
checks the residual in every coordinate. An absolute tolerance governs this
geometric membership check. Coincident lines and lines whose separation falls
within twice the tolerance are rejected, since a query could then belong to
more than one stored line and have competing answers.

The stored height is measured in units of `t`. Multiplication by
`maximum(d)` converts that height to distance along the line in the ambient
infinity norm, the largest absolute coordinate change. For example,
$d=(1/2,1/2)$ carries a parameter change of four to an ambient
change of $(2,2)$, whose infinity norm is two. A tent of height four in the
stored parameter therefore has height two in those ambient units. For equal
direction components this gives the diagonal landscape
described by Vipond: its restrictions to diagonal lines are ordinary landscapes
with the appropriate parameter. Unequal positive components describe a
directional summary, which the result identifies separately. The adapter
does not average directions or identify this summary with the diagonal invariant.
[Vipond's construction](https://www.jmlr.org/papers/v21/19-054.html) supplies the
mathematical interpretation; the adapter for a finite grid and its masking contract
are library choices.

## Distinguish sampling, interpolation and unavailable queries

Each query must lie within both the range of retained evaluation times and
the declared source window for its line. A query outside that window or a point without a stored line
gets `NaN` and a false coverage flag. Zero is reserved for an available zero
height. The algorithm performs no extrapolation and no interpolation between
different lines. Finite source windows may themselves reflect a restricted or
censored computation; supplying their endpoints does not undo that restriction.

Within a line, a binary search finds neighboring sample times. Both neighbors
must lie inside the declared source window; crossing that window boundary does
not justify borrowing an unavailable sample. Linear
interpolation supplies the height. If their distances from the query are
`a` and `b`, the Lipschitz property of an ordinary landscape gives an
interpolation error at most `2ab/(a+b)`, with zero error at a sample time.
The relevant Lipschitz constant is one: moving by a distance $h$ along the
line changes a tent height, and hence any ordered layer height, by at most
$h$. If $u<t<v$ are neighboring sample times, put $a=t-u$ and $b=v-t$.
The interpolated value is $(b\lambda(u)+a\lambda(v))/(a+b)$, so

$$
\left|\frac{b\lambda(u)+a\lambda(v)}{a+b}-\lambda(t)\right|
\leq \frac{b a+a b}{a+b}.
$$

At the midpoint this bound is half the sample spacing. It can be attained
when the two samples lie at the feet of a tent and its peak lies midway
between them, which explains why exact samples alone do not make arbitrary
interpolation exact. A supplied uniform bound on the sample error is added before
conversion to ambient units. Without that supplied bound, the error against the
intended landscape is recorded as unknown. When the line membership test uses a nonzero
tolerance the bound concerns the projected point on the stored line.

This bound addresses numerical evaluation of the stated line landscape. It
does not establish an error for the original point cloud, a previous grid
approximation, capped essential intervals or statistical inference.
`ambient_coverage` and `ambient_errors` make the distinction inspectable.

For `Q` grid points, `S` stored offsets, `T` parameter samples and `K` layers,
the straightforward query pass costs up to `O(Q(S + log(T) + K))`, with an
additional factor for the ambient dimension in the line membership checks.
It stores `O(QK)` values and `O(Q)` coverage/error entries. A pairwise line
uniqueness check costs `O(S²)` before evaluation. `max_points` limits the
product of grid points and retained layers before allocation. This path
consumes retained features and does not repeat barcode or rank computations.

## Keep the numerical field separate from its rendering

`ScalarField` turns declared coordinate axes and sampled values into a
visualization input. When constructed from an ambient landscape grid, it retains the grid's interpretation and
window metadata, with landscape layers as stable IDs. Other scalar invariants
can use the same adapter after their values have been computed; a plain field
does not claim to be a module or a finite encoding.

The [visual specification account](visual_specs.md#coordinate-sections-and-shared-scales)
explains orientation, masks, shared scales and interpolated contours. Those
contours introduce an explicitly declared display interpolation across neighboring
grid values; the ambient query error bounds do not certify the contour curves. The
[session account](inspection_sessions.md#linked-coordinate-sections) explains
how controls reuse those data. Assembly of a table of features and numerical
integration are separate operations, so changing a view cannot silently change
an experiment's feature vector.

## References

See the [implementation bibliography](references.md), particularly Oliver
Vipond's multiparameter landscapes and Peter Bubenik's ordinary landscapes.
