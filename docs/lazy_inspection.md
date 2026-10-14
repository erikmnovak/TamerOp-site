# Inspection and explicit computation

After constructing an encoding, first ask what is already known and which
calculation your next question requires. Its finite poset and parameter map may
be available before all vector spaces and structure maps have been computed.
Such a result is *lazy*: it keeps enough data to carry out the deferred work
when requested. This guide follows that distinction across encodings, algebra
and geometry, including what repeated queries reuse. For a concrete workflow
from parameters to spaces, matrices and figures, use [Exploring spaces and
maps](spaces_and_maps.md); the [finite encoding
introduction](finite_encodings.md) explains the underlying object.

`show`, `describe`, and the summary functions belonging to each subsystem
inspect stored data. Displaying an encoding therefore leaves any missing
module, ranks or geometric data uncomputed. A summary can still take time: for
example, counting nonzero entries in an existing dimension vector requires
visiting that vector. What distinguishes inspection is that it describes the
retained result without carrying out its deferred mathematical constructions.

For a lazy ingestion encoding `enc`, observe how an explicit query changes what
the result retains:

```julia
describe(enc)              # stored metadata, provenance, materialized status
dimensions(enc)            # dimension vector only; cached for subsequent calls
pmodule(enc)               # full module, including structure maps; cached
```

Before a dimension query, `describe(enc).module_dims` is `nothing` and the text
display says `not computed`. Afterward, the summary reports the cached vector
without constructing the full module. `materialized` distinguishes these
states: having all dimensions does not mean that structure maps exist. A full
module request also makes its dimensions available without repeating the
dimension computation.

`encoding_poset`, `encoding_map`, `encoding_axes`, and provenance accessors do
not materialize the module. An encoded complex's `encoding_complex` accessor
returns its stored complex, which can itself be lazy. Its summary reports the
number of stored terms and differentials; printing it does not fill them.
`encoding_module` has the same explicit behavior of requesting the full module
as `pmodule`.

Repeated ingestion calls with `cache=SessionCache()` identify a computed module
by its actual constructed cells, grades, boundaries, coefficient field and
encoding request. Changing an input boundary or birth must not reuse the old
module even when the input object, grid and dimension vector are unchanged. The
cache snapshots sparse boundary storage without densifying it. This costs a
scan of the constructed chain data on cached calls; `cache=nothing` avoids that
scan. Lazy ingestion results also own snapshots of their sparse boundaries and
classifier axes, so later source edits cannot change a pending computation.
Treat returned modules and lazy results as mathematical values: after editing
source data, call `encode` again rather than mutating an already computed
result or expecting it to update itself.

Geometry caches for point clouds also distinguish coordinate contents: moving a
site invalidates the old Delaunay geometry or landmark radius graph. Landmark
graph keys inspect the selected landmarks; unchanged unselected sites do not
force a new graph. Equality checks retain coordinates, rather than relying on
their hashes alone. Input mutation is supported between calls, not during a
running computation. Use `PointCloud(coords; copy=true)` when the dataset
should own coordinates independently of the supplied matrix.

## Repeated queries and batches

A cache is retained work that a later request may reuse. `SessionCache` makes
that lifetime explicit across calls; the result object itself may also retain
answers, as the dimension example above does. Neither kind of reuse is the same
as Julia compiling a function on its first invocation. A first call can pay for
both compilation and mathematics, so timing a repeated call alone does not
measure the cost of constructing the result from new data.

Here is a small batch whose answer we can predict. We use two presentations
with the same closed interval $[0,2]$. The first has coefficient matrix $[1]$,
so its fiber is $\mathbb Q$ inside the interval. The second has matrix $[0]$,
so every fiber is zero. Both encodings use the same ordered region labels:
before the interval, on it and after it.

```julia
import TamerOp as OP
import TamerOp.Advanced as A

session = OP.SessionCache()
ups = [A.BoxUpset([0.0])]
downs = [A.BoxDownset([2.0])]
options = A.EncodingOptions(field=OP.CoreModules.QQField())

interval = OP.encode(ups, downs, fill(OP.QQ(1), 1, 1), options; cache=session)
zero_module = OP.encode(ups, downs, fill(OP.QQ(0), 1, 1), options; cache=session)
samples = [interval, zero_module]
spec = OP.BarcodeSummarySpec(
    directions=[[1.0]], offsets=[[0.0]], fields=(:count,),
    tmin=-1.0, tmax=3.0, nsteps=9, window=(-1.0, 3.0), threads=false,
)
batch = OP.BatchOptions(threaded=false)

features = OP.featurize(samples, spec; cache=session, batch)
X = A.feature_matrix(features)
@assert X == reshape([1.0, 0.0], 2, 1)
```

`BarcodeSummarySpec` asks for a barcode along the line with direction `[1.0]`
and offset `[0.0]`, so its line parameter is the original coordinate $x$.
The nine samples from $-1$ to $3$ include points before, on and after the
interval. Its restriction to that sampled chain has one interval; the zero
module has none. `fields=(:count,)` therefore gives one feature column with
values $1$ and $0$ for the two rows. The finite window specifies how to clip
any intervals meeting its ends, and `threads=false` keeps each sample's query
serial.

This is a sampled barcode request. A gap between consecutive samples could
hide an event in another input, so the same bounds and samples must be retained
when interpreting repeated answers. Here the interval's endpoints are known
from its presentation and are included among the samples. A compiled plan assigns those sample parameters to finite labels. Each
encoding retains its own map between calls, so repeating the request can reuse
its plan. The module's actual structure maps still determine its barcode.

Repeating the same request with the same session allows the compatible
preparation to be reused:

```julia
repeated = OP.featurize(samples, spec; cache=session, batch)
@assert A.feature_matrix(repeated) == X
```

The retained plan can be reused, while each batch still assembles its output
matrix. A session does not promise that every completed feature vector is
retained, or that a related but different question has already been answered. A new session begins a separate collection
of reusable work; `cache=nothing` opts out of that session reuse. Retain the
inputs and result objects unchanged while using their cached computations, and
release the session and results when they are no longer needed. This also
releases their ownership of retained data, subject to any other live
references.

The example fixes the field, presentation, feature specification and execution
options so that the repeated answer has a precise meaning. For larger batches,
`BatchOptions(threaded=true)` permits parallel execution, while the
specification here keeps each barcode calculation serial with `threads=false`. The
[optional integrations guide](optional_integrations.md) explains the Folds
integration and options for progress reporting. The [features
guide](tutorials/features.ipynb) develops feature choices and comparisons
beyond this small reuse example.

## Selected ranks and the complete invariant

If the question concerns one structure map, use `rank_map(M, a, b)` on a finite
module. The vertices must be comparable in its poset. This avoids requesting
ranks for every other pair; an anchored rank view similarly fixes one end of
the map.

`rank_invariant(M)` explicitly requests the complete invariant. It visits
comparable pairs and stores positive ranks; `store_zeros=true` also retains
zero ranks on comparable pairs. The traversal shares composition work for maps
with the same source and reuses that workspace for the next source. It has no
unconditional square buffer for every possible pair. The returned dictionary
can still be quadratic on a chain, because the requested answer has that many
pairs. Parallel tasks have their own temporary storage and combine their
entries after computation. Category caches and the input module have their own
costs.

## Encoding metadata

`compile_encoding(P, pi)` attaches a classifier to its poset. It does not
generate axes or representative points. The summary's `has_axes` and
`has_representatives` flags report accessor capabilities or supplied metadata,
not whether generated arrays have been cached.

Request `encoding_axes` or `encoding_representatives` when those data are
needed. Grid representatives enumerate the Cartesian product of the axes, so
their number grows as the product of the axis lengths. Generated metadata is
returned on demand, not implicitly memoized; callers who want retained metadata
can supply `axes=...` and `reps=...` when compiling. Adding a workflow session
cache preserves supplied metadata and leaves absent metadata lazy.

## Algebra, geometry, and features

The same distinction applies after encoding: a summary describes what is
stored, while a mathematical query may construct a new answer. Choose the query
from the information you need, such as a dimension, a representative vector, or
a geometric measurement.

- A fringe display reports existing fiber dimensions. Use `fiber_dimension`
  or `dimensions` explicitly to compute ranks.
- A spectral summary reports `convergence_page=nothing` when stored dimension
  tables do not yet certify the first stable page. `convergence_bound` is the
  bound supplied by the finite filtration width. Request `convergence_page(ss)` explicitly to
  compute missing pages. An isolated cached later page does not certify the
  earliest stable page if earlier pages remain unknown.
- Ext comparison maps, homology representatives, algebra products, and
  bases for a common refinement remain lazy under inspection. Their explicit
  mathematical accessors may compute and cache them.
- Geometry summaries leave exact region geometry and cached order relations untouched. Area, membership, and other geometry queries retain their
  own computation contracts.
- `nfeatures(spec)` counts the output slots without constructing feature names.
  `feature_names(spec)` deliberately constructs those labels. A rank feature vector
  always has `nvertices^2` slots, even when its intermediate rank table omits
  zero entries.

For example, after constructing a finite encoded module, you may first want
only the dimensions of its Ext spaces. Over an exact field, that query retains
the cycles and boundaries but leaves the choice of quotient representatives and
their coordinates until you request them. You can still ask the same result for
representatives, coordinates, induced maps, and products. The first such
request does the additional work; later requests reuse the stored data. These
computations remain in the category of modules over a finite poset described in [Mathematical
categories](math_categories.md).

Deferring coordinates does not defer checking that boundaries are cycles.
Cohomology results from exact complexes check that condition when built.
Numerical fields keep their checked boundary solve at construction, with the
supplied tolerances. Cached basis matrices are shared data and should be
treated as read only.

For an Ext result with both projective and injective descriptions, `basis(E,
t)` returns copies of its chosen representatives. Repeating that call reuses
the stored basis. If you request the other resolution model with
`model=:projective` or `model=:injective`, the comparison map carries those
same classes into that model; the order still agrees with the result's
canonical coordinates. Thus changing models does not change which Ext class a
coordinate vector describes. Comparisons check inverse identities exactly over
exact fields and with the supplied field tolerances for numerical coefficients.
Public coordinate queries continue to check that the supplied vectors are
cycles, even after a coordinate calculation has been cached. Over rational
coefficients, the retained calculation uses a set of independent ambient
coordinates to recover the class and checks that every remaining coordinate
agrees with a cycle. This avoids solving for all boundary coordinates on each
query while keeping the check exact. Requesting these coordinates does not
construct the representative matrices: those remain deferred until a basis or
representative is requested. A factorization already needed to check boundaries
is reused by the same result. A vector outside the cycle space is rejected even
when the quotient has dimension zero; numerical coefficients retain their
supplied tolerance rules.

Over a prime field with characteristic greater than three, native coordinate
solves retain their factors on the homology, cohomology or subquotient result.
A factor records work needed to solve the same coefficient matrix again. Later
vectors are still checked against the full represented subspace. A new result
does its own preparation, and discarding the result releases its local factors.
Characteristic two and three use their specialized implementations; selecting
Nemo uses its own arithmetic route.

Validators and explicit mathematical queries are separate from passive
inspection: they can perform the work required by their documented contracts.

## Asking for several extension products together

A table of Yoneda products can share the preparation needed to lift each
extension class through its resolution. The [derived
guide](tutorials/derived.ipynb#asking-for-several-extension-products-together)
develops this calculation with explicit columns, a predicted answer from
bilinearity, and the returned target coordinates. It explains which resolution
degrees are needed, how a different target model is handled, and when to
request the composite cocycles. Its following algebra example shows how
repeated products reuse a completed table for a fixed pair of degrees.

The [implementation account](implementation/yoneda_products.md) follows the
lift and quotient calculation. These products take place in the representation
category of the supplied finite poset, as explained in the [category
lesson](math_categories.md).