# Options must affect the requested computation

Some options change the mathematical problem; others select a way to compute
its answer or decide which data to retain. For example, changing the
coefficient field can change homology, while changing the storage of a finite
poset should leave its order intact. Keeping that distinction in view helps
explain which results ought to agree when an option changes.

Use the options object for the operation you are requesting. These types are
available from `TamerOp.Options` and `TamerOp.Advanced`. The [ingestion
guide](ingestion_options.md) covers filtration construction, grids, fields and
replaying saved inputs; the contracts below concern finite presentations,
derived computations and module queries.

## Finite encoding

An encoding combines a finite poset, a module on it and a map assigning
original parameters to its labels. `EncodingOptions(poset_kind=:dense)` stores
the finite order as a dense relation, whether called through an owner module or
the main workflow. An explicit `poset_kind` keyword overrides the value in the
options object; when that keyword is absent, the object's value is used.

A geometric operation that constructs only a poset has no coefficient field to
change. An operation producing a presentation or module uses `opts.field`. For
a lattice presentation (a Zn flange), omitting an explicit options object
preserves its existing field. Supplying `EncodingOptions()` chooses the
object's default, `QQ`, the rational field. Changing characteristic can change
ranks and homology, and a rational coefficient cannot be converted to a field
in which its denominator is zero.

`strict_eps` concerns feasibility in general piecewise linear geometry: whether
there is a point satisfying a region's strict inequalities. With the default
`nothing`, this question is decided over the rationals, so arbitrarily narrow
nonempty regions can be retained. An explicit positive margin requires at least that much slack between the
two sides of each strict inequality and may omit a narrow region. This margin
depends on how the inequality is scaled; it is not an intrinsic distance from
the boundary. Membership queries still use the original boundaries. The
result records `feasibility=:exact_rational` or `:fixed_margin` in its
provenance.

The lattice and specialized box encoders have no use for that margin and reject
a nondefault `strict_eps`. Derived computations using lattice boxes apply their
encoding field and region budget, and likewise reject controls that do not
belong to the construction. See the [box encoding
account](implementation/box_encoding.md) for the separate treatment of closed
boundaries.

## Derived computations

`DerivedFunctorOptions` chooses how a derived computation is represented. For
Ext, the projective model resolves the first module and the injective model
resolves the second. A call tied to one of these models rejects options
requesting the other. `canon=:auto` chooses coordinates for the model actually
used, while `canon=:none` retains its native coordinates. A unified Ext result
also permits comparison of its projective and injective coordinates. Tor uses
its own `:first` and `:second` resolution choices and rejects canonical
coordinate settings that do not apply.

Pass these controls through the documented `opts` keyword, for example in
`ExtLongExactSequenceFirst(...; opts=DerivedFunctorOptions(...))`. The ellipses
stand for the sequence data and chosen options, as specified in the [derived
reference](src/reference/derived.md). Long exact sequences and derived Kan
computations validate their required model before building or using a cached
result. Requested degrees must be nonnegative.

`ResolutionOptions(check=true)` checks the alignment of resolution terms,
generator data and the fact that consecutive differentials compose to zero.
Cached results undergo the same checks. These identities are necessary for a
resolution, but checking them alone does not prove its exactness. The finite
poset builders construct minimal resolutions; when `minimal=true`, enabled
checking also verifies their minimality. Setting `check=false` skips those
diagnostics. A negative length bound is rejected in either case.

`ExtDoubleComplex(M, N; maxlen=...)` constructs a bounded array of resolution
terms with its two differentials. `ExtSpectralSequence(M, N; maxlen=...)`
requires complete resolutions for its limiting groups to compute Ext. A bound
that constructs a bicomplex therefore need not suffice for the spectral
sequence's asserted limit; the [derived guide](tutorials/derived.ipynb)
explains the role of these degrees.

## Module construction and queries

`ModuleOptions(cache=cover_cache)` supplies the cover relations used in module
construction and map queries. A cover is an ordered pair with no vertex
strictly between its endpoints; composing the stored cover maps recovers maps
between more distant comparable vertices. The cache must belong to the module's
poset, and both incompatible caches and conflicting cache arguments are
rejected even for identity maps or empty batches.

The constructor option `check_sizes=false` lets a caller take responsibility
for the dimensions of supplied matrices. It does not apply to map queries:
those always validate indices and comparability. With default checking,
construction validates reused matrix storage as well. Finite fringe
constructors receive their coefficient, checking and storage arguments
directly, rather than through this module options object.