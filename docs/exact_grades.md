# Exact rhomboid grades

Two nearby radii can mark different topological events even when a plot places
them at the same position. A *grade* is the parameter value at which a cell
appears. If we round two distinct grades to one value, a cell and a boundary
that entered at different times may appear together, changing the persistence
module. Keeping the grades distinct lets the finite encoding retain the spaces
and maps of the supplied rhomboid filtration.

`RhomboidFiltration()` stores physical radii as `AlgebraicReal` values: real
roots of polynomials with rational coefficients, represented exactly. The
construction first computes rational squared radii, then takes exact square
roots. Sorting, membership, cell attachments and grid indices all use these
values. A conversion to `Float64` supplies an approximation for display without
replacing the stored grade.

```julia
import TamerOp as OP

r = sqrt(OP.AlgebraicReal(2))
r^2 == 2                       # true exactly
Float64(r)                     # an approximation for display

points = OP.PointCloud(reshape(OP.QQ[0, 2, 4 + OP.QQ(1, big(2)^70)], :, 1))
enc = OP.encode(points, OP.RhomboidFiltration(); degree=0)
OP.encoding_axes(enc)           # distinct exact critical values
OP.provenance(enc).approximation.grade_arithmetic  # :exact_real_algebraic
```

The gap between the second and third points is slightly larger than the gap
between the first two. Writing that difference as a rational number preserves
it before construction begins. Exactness always refers to the coordinates
supplied: if a coordinate arrives as a floating number, its represented binary
value is the input, even if a different decimal value was intended.

At depth one, the two gaps close at radii $\rho_1=1$ and
$\rho_2=1+2^{-71}$. Degree zero homology counts connected components, so a
radius between these events gives two components. Explore the exact queries
below. At and between the two events, a floating display of 1 conceals
different answers. The
spacing in the illustration is enlarged so that the two events can be seen.

```@raw html
<link rel="stylesheet" href="../assets/arithmetic/choices.css">
<figure class="arithmetic-example" id="grades-explorer" data-arithmetic-example="grades">
<div class="choice-control"><label for="grades-choice">Exact radius r</label>
<select id="grades-choice" aria-describedby="grades-explanation" disabled>
<option value="before">r = 1/2</option>
<option value="first">r = 1</option>
<option value="between" selected>r = 1 + 2⁻⁷²</option>
<option value="second">r = 1 + 2⁻⁷¹</option>
</select></div>
<div class="choice-drawing"><svg viewBox="0 0 250 230" role="img" aria-label="r = 1 + 2⁻⁷²: between the mergers. The first two points remain in one component, and the third has not joined them. This exact radius lies strictly between the two events, although all three radii have Float64 display 1."><line x1="36" y1="63" x2="119" y2="63" class="retained"></line><line x1="131" y1="63" x2="214" y2="63" class="omitted"></line><circle cx="30" cy="63" r="5" class="retained"></circle><text x="30" y="45" text-anchor="start" class="">0</text><circle cx="125" cy="63" r="5" class="retained"></circle><text x="125" y="45" text-anchor="middle" class="">2</text><circle cx="220" cy="63" r="5" class="retained"></circle><text x="220" y="45" text-anchor="end" class="">4 + δ</text><text x="125" y="96" text-anchor="middle" class="small">Joined points lie in one component.</text><line x1="25" y1="160" x2="225" y2="160" class="axis"></line><line x1="85" y1="150" x2="85" y2="167" class="axis"></line><text x="85" y="189" text-anchor="middle" class="">ρ₁</text><line x1="165" y1="150" x2="165" y2="167" class="axis"></line><text x="165" y="189" text-anchor="middle" class="">ρ₂</text><circle cx="125" cy="142" r="6" class="query"></circle><line x1="125" y1="149" x2="125" y2="160" class="cutoff"></line><text x="135" y="139" text-anchor="start" class="">r</text><text x="125" y="219" text-anchor="middle" class="small">The gap between the radii is enlarged.</text></svg></div>
<dl class="choice-values">
<dt>First critical radius ρ₁</dt><dd>1</dd>
<dt>Second critical radius ρ₂</dt><dd>1 + 2⁻⁷¹</dd>
<dt>Float64 display of the selected radius</dt><dd data-value="floating">1</dd>
<dt>Connected components</dt><dd data-value="components">2</dd>
</dl>
<p class="choice-convention">This is a schematic of connectivity at depth 1, with δ = 2⁻⁷⁰. Solid edges join points in one component; dashed gaps separate components. The exact query coordinates are not replaced by their floating displays.</p>
<figcaption id="grades-explanation" data-choice-explanation aria-live="polite">The first two points remain in one component, and the third has not joined them. This exact radius lies strictly between the two events, although all three radii have Float64 display 1.</figcaption>
<noscript><p>The displayed case remains available; enable JavaScript to change the selection.</p></noscript>
</figure>
<script src="../assets/arithmetic/choices.js"></script>
```

An exact cutoff such as
`OP.RhomboidFiltration(radius=sqrt(OP.AlgebraicReal(2)))` includes cells born
at that radius. Finite grades smaller or larger than the `Float64` range remain
valid. Arithmetic and comparisons between `AlgebraicReal` values are exact;
converting an irrational value to `QQ` or `Int` raises `InexactError`, because
that target cannot represent the value.

## Coordinates and queries

The physical parameters are radius $r$ and depth $k$. Increasing radius or
*decreasing* depth adds cells, so the stored axes are $(r,-k)$, with both
coordinates increasing along the order. The encoding map, which assigns each
physical parameter its finite label, handles this reversal when queried by
`locate`.

| Operation | Coordinates it receives or returns |
| --- | --- |
| `locate` on the rhomboid encoding map | Physical radius and depth, $(r,k)$ |
| Stored encoding axes | Increasing coordinates $(r,-k)$ |
| Grid signed measures and Euler tables | The stored oriented coordinates $(r,-k)$ |

This distinction matters when you supply your own axes. The default critical
grid retains every birth. A coarser grid, or a quantization that replaces
grades by chosen levels, changes where births occur;
`OP.provenance(enc).discretization` records that choice. The [finite encoding
introduction](finite_encodings.md) explains how the axes and encoding map
relate the original parameters to the finite model.

Radius is also different from squared radius. Replacing $r$ by $r^2$ preserves
the order of births for $r\geq0$, but bends straight slices and changes metric
values. Slicing and matching therefore retain the radius coordinate. The exact
2D matching optimizer requires a finite window and an encoding map whose two
coordinates increase with the order. The default rhomboid map has orientation
`(1,-1)` and is rejected by that optimizer. A comparison in $(r,-k)$
coordinates uses a map with orientation `(1,1)` on the same stored axes and
finite poset, with the matching window expressed in those coordinates. The
optimizer's geometry is exact; its final scalar output is `Float64`.

## Which later computations remain exact?

An exact 2D slice query retains algebraic interval endpoints. A sampled query
instead classifies the supplied sample points exactly and describes those
samples; it cannot discover a short interval between them. For a grid you
construct yourself, use `OP.AlgebraicReal.(axis)` on each axis to select the
same exact arithmetic for locating slice crossings. Other families of encoding
maps have their own arithmetic contracts.

Feature specifications retain exact directions, offsets, slice bounds
`tmin`/`tmax`, clipping `window` bounds and supplied axes for invariant
queries. Saving their metadata preserves these coordinates. Barcode summaries
and the features formed from the longest intervals compare exact endpoints and
subtract them before converting interval lengths to numerical outputs.
Persistence images, silhouettes and entropy likewise form exact endpoint
differences before evaluating powers, exponentials or logarithms numerically.
Euler tables retain exact axis labels, including through Tables.jl.

The grids on which a feature is *evaluated*, such as landscape `tgrid` and
image `xgrid`/`ygrid`, are numerical, as are weights, kernel parameters and
final feature vectors. A narrow feature can fall between those samples even
though its exact underlying grades remain distinct. The two choices answer
different questions: exact grades preserve when an event occurred, while the
evaluation grid determines where we look at the resulting feature.

Projection invariants retain algebraic levels when constructing their finite
target chains and pushforward maps. Their barcodes have exact endpoints, and
distance evaluation subtracts those endpoints before rounding. A pushforward
along a projection and a restriction to a line are different constructions, so
their invariants need not agree. Numerical integration and final feature
outputs still use their declared floating precision.

## Reusing exact requests

Compiled sampled slice plans retain their parameter values and can be reused
across modules. A cache reuses a computation only when the relevant requests
agree exactly, including their filtration parameters, bounds, directions,
offsets and sample values. Ingestion keys include the final encoding axes, so
changing the grid cannot retrieve a module computed on the old one.

Request arrays are copied into immutable keys when stored. Later edits to an
array therefore leave the existing entry intact. A hash helps find possible
matches, but equality of the exact values decides whether the entry can be
reused. Composite feature groups follow the same rule when sharing work.

## Saving and inspecting

TamerOp's dataset and encoding JSON formats store rational coordinates as
canonical rational strings. A real algebraic coordinate is stored by its
primitive integer minimal polynomial and the index specifying which real root
it represents. Loading checks these records and preserves exact values,
orientations and maps; ordinary floating arrays keep their numeric storage.

After loading an ingestion encoding, `OP.provenance(enc).coordinate_semantics`
reports its recorded grade scale, orientation and arithmetic. A raw graded
complex has generic coordinates, so save its filtration specification as well
when the geometric meaning is needed. An artifact can recover only the
construction information that was recorded.

Exact algebraic arithmetic costs more than floating arithmetic. It is useful
here because separating births matters to the represented module. The
[multicover guide](tutorials/multicover.ipynb) develops the construction,
including bounds on depth and the exact backend for degenerate inputs.