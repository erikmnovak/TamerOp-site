# Derived spaces, representatives and products

Ext describes module maps and their higher extension classes; Tor is obtained
by tensoring a resolution and taking homology. The calls below compute these
spaces in the representation category of a recorded finite poset. Their
representatives, coordinates and products refer to that category and to the
chosen resolution models. An encoding's recovery map does not establish an
identification with an ambient derived functor. The
[category discussion](../../math_categories.md) explains the comparison, and
the [worked guide](../../tutorials/derived.ipynb) follows the classes and
products on a diamond.

## Compute and inspect a graded space

With `import TamerOp as OP`, the following calls request degrees 0 through 2
for compatible input modules:

```julia
E = OP.ext(M, N; maxdeg=2)
T = OP.tor(Rop, L; maxdeg=2)
OP.Advanced.ext_summary(E)
OP.Advanced.tor_summary(T)
OP.Advanced.dim(E, 2)
OP.visualize(E)
```

`M` and `N` must be `PModule`s on the same finite poset object, or
`EncodingResult`s whose finite modules share that object. Their coefficient
fields must agree. Ext is contravariant in `M` and covariant in `N`: a map
`M′ → M` induces `Extᵗ(M,N) → Extᵗ(M′,N)`, while `N → N′` induces
`Extᵗ(M,N) → Extᵗ(M,N′)`. If the inputs use different encoding posets,
construct a common encoding before making the call.

For Tor, `Rop` is a right module represented on the opposite of the finite
poset supporting the left module `L`. The fields must agree and the indexed
orders must be opposite. Tor is covariant in each module argument. This
pairing uses the incidence algebra of the finite poset, whose basis
represents comparable pairs and whose multiplication composes them. It is
different from the pointwise tensor product of two forward modules.

Both calls default to `maxdeg=3`. This is the highest computed degree, so
the stored range is `0:maxdeg`; the construction retains the next differential
needed to compute the last quotient correctly. Querying a dimension above
that range raises `ArgumentError`, even if the highest computed group is zero.

| Choice | Accepted values and effect |
| :--- | :--- |
| Ext `model` | `:projective`, `:injective`, or `:unified`; the default `:auto` selects projective. |
| Unified Ext `canon` | Chooses the projective or injective model used for canonical coordinates. Bases in another model are related by a comparison map. |
| Tor `model` | `:first` resolves the right argument and `:second` resolves the left; the default `:auto` selects `:first`. |
| `cache` | The default is `:auto`. Supply `sc::OP.SessionCache` to reuse compatible resolution work across calls. |

The models compute the same functor on the fixed finite category, but their
representative vectors and bases can differ. `degree_range`,
`degree_dimensions`, `source_module`, `target_module` and `provenance` on
`OP.Advanced` expose the stored range, groups and inputs without asking a
reader to interpret internal fields.

To obtain an actual class representative, use `basis`, `representative` or
`coordinates` explicitly. If `c` has `dim(E,t)` entries in the quotient
basis, `representative(E,t,c)` returns a cocycle representing that class.
For a cycle `z`, `coordinates(E,t,z)` returns its quotient coordinates.
A noncycle is rejected, including when the quotient has dimension zero.
Tor has the same coordinate operations with cycles in homological degree.

For a result whose degree 2 group is one-dimensional, for example:

```julia
C = OP.Advanced.representative_complex(E)
z = OP.Advanced.representative(E, 2, OP.QQ[1])
```

`representative_complex` returns the retained Hom cochain complex of a native
Ext model, or the canonical model of unified Ext. For Tor, it copies the
boundary matrices into cochain indexing `C^(-s)=C_s`, retaining the additional
incoming term. It does not compute quotient bases. Treat derived models and
retained complexes as read-only; in particular, Ext returns its stored complex.

## Resolutions, module complexes and computed degree ranges

`projective_resolution`, `injective_resolution` and `resolve` use principal
upsets or downsets as their projective or injective terms. Their Betti or Bass
counts are multiplicities on this finite base. A stored prefix may end with
a nonzero kernel or cokernel, so its length alone does not certify completion.
The [resolution guide](../../tutorials/resolutions.ipynb) shows how to inspect
this distinction. `IndicatorResolutions.upset_resolution(M)` and
`downset_resolution(M)` for a finite `PModule` construct these principal
resolutions using projective covers or injective hulls. An arbitrary indicator
presentation supplied separately need not have the same properties.

A `ModuleCochainComplex` has differentials raising degree. Its maps,
homotopies, mapping cones and distinguished triangles belong to the same
finite module category. Cohomology is therefore a module on that base;
a *quasi-isomorphism* means a map inducing an isomorphism on every cohomology
module. The shift convention is `C[k]^t = C^(t+k)`. The
[complex guide](../../tutorials/complexes.ipynb) explains the corresponding
matrix convention and cone differential.

`RHomComplex` and `DerivedTensorComplex` retain total complexes formed from
stored resolution prefixes. Their end degrees can contain cohomology caused
by the cutoff rather than by the intended derived functor. These containers
retain their finite base, whereas extracting a raw scalar complex loses that
module information.

Use `hyperExt(C,N)` or `hyperTor(Rop,C)` for the derived groups justified by
the stored resolutions, where `C` is a module cochain complex. Both expose
that justified range through `degree_range`. If the resolution with budget
`maxlen` is unfinished, only degrees
`-C.tmax:maxlen-C.tmax-1` are certified; higher queries raise `ArgumentError`.
When the resolution terminates, the whole total complex is certified.
Hyper-Tor requires the entire source complex. Its degree `n` corresponds to
total cochain degree `-n`, so a module placed in cochain degree `p`
contributes ordinary `Tor_s` in degree `n=s-p`. Negative hyper-Tor degrees
can consequently occur.

The named `ExtSpectralSequence` and `TorSpectralSequence` constructors require
completed resolutions and reject explicit budgets that stop too early.
Ext uses cohomological indexing; the Tor wrapper reverses both bidegrees.
By contrast, `ExtDoubleComplex`, `TorDoubleComplex` and raw `spectral_sequence`
work with the actual supplied bicomplex, possibly truncated. Its spectral
sequence approaches the total cohomology of that supplied object. Interpreting
this as Ext or Tor needs the appropriate resolution and acyclicity hypotheses.
Here acyclicity means that the resolution terms have no higher derived
contribution to the operation being computed.

For `ExtDoubleComplex(F,dF,E,dE)` with user-supplied indicator terms, complete
projective first terms and injective second terms suffice. Completeness of
arbitrary upset and downset resolutions alone does not. The constructor
starting from a finite module builds the principal indicator resolutions
required for its Ext interpretation.

`ExtZn`, `ExtRn` and the geometric resolution and spectral wrappers likewise
compute on their selected finite encoding or finite box. Retain the classifier
and any chosen window when interpreting the result geometrically. A geometric
input type by itself gives no ambient Ext or Tor identification.

## Read the mathematical provenance

`OP.provenance(E)` records the mathematical input and conventions used for an
Ext result: `category`, the actual `base_poset`, `field`, `degree`,
`degree_convention` and `model`, along with orientation and argument variance.
`ambient_identification=:not_asserted` records that no identification with an
ambient derived functor has been established. Unified Ext also records its
`canonical_model`. The result summaries expose the same record as
`.provenance` without constructing comparison maps or quotient bases.

Tor records `orientation=(right=:opposite,left=:forward)` and
`argument_variance=(:covariant,:covariant)`. Its degree convention is
homological. Ext and Tor functorial maps, long exact sequences, Yoneda
products and the Ext action on Tor use these fixed finite categories and
compatible resolution coordinates. Passing to another encoding category
requires its own functor and comparison hypotheses.

Raw `CochainComplex`, `DoubleComplex` and `SpectralSequence` objects retain
their field, including custom `RealField` tolerances. Constructors from matrices
accept `field=...` and infer a default only when none is supplied. Their
provenance reports `field_source=:stored_field` and `base_poset=nothing`,
because matrices alone do not retain a module's finite base. An explicitly
reindexed Tor spectral sequence cannot recover discarded base information.
Keep the module or derived container when that context will be needed later.
The [numerical algebra guide](../../numerical_algebra.md) explains how the
field's tolerances enter coordinate and equation checks.

## Compose Ext classes

For compatible projective Ext models and quotient coordinate vectors:

```julia
target, c, z = OP.Advanced.yoneda_product(E_MN, p, beta, E_LM, q, alpha;
    ELN=E_LN, return_cocycle=true)
```

This computes the left factor after the right factor,

$$\operatorname{Ext}^p(M,N)\times\operatorname{Ext}^q(L,M)
\longrightarrow\operatorname{Ext}^{p+q}(L,N).$$

All supplied models are `ExtSpaceProjective`s. The vectors `beta` and `alpha`
have lengths `dim(E_MN,p)` and `dim(E_LM,q)` in their models' quotient bases.
Degrees must be nonnegative, the left model must include degree `p`, and the
right resolution must extend through `p+q`. The two descriptions of the middle
module must agree in field, indexed finite order, stalk coordinates and
structure maps. Equal dimension vectors alone cannot identify these modules.
A supplied `ELN` must represent the same `L` and `N` through the output degree;
it fixes the target coordinate system.

The ordinary return is `(target, coordinates)`. With `return_cocycle=true`,
the third value is the actual composite cocycle in the returned target model.
When a supplied target uses a different resolution, a comparison lift transfers
the cocycle into it before coordinates are taken. No extra Koszul sign is
inserted in this composition convention. The call returns a class and,
optionally, a cocycle; it does not construct a sequence of extension modules.

To compose collections of classes, put left coordinates in columns of `B`
and right coordinates in columns of `A`, then use the matrix overload:

```julia
target, products = OP.Advanced.yoneda_product(E_MN, p, B, E_LM, q, A; ELN=E_LN)
```

The shape is `(dim(target,p+q), size(B,2), size(A,2))`.
`products[:,j,i]` is left column `j` composed with right column `i`.
Identity matrices select all basis classes; arbitrary columns select their
specified combinations. Empty column collections are allowed, with the same
degree, model and row-count checks. `return_cocycle=true` adds a third array
with the same last two indices and cochain coordinates in its first index.
Each right class is lifted once per call and used with all left classes.
The [worked matrix example](../../tutorials/derived.ipynb#asking-for-several-extension-products-together)
shows the index order and compares the answer with bilinearity.

## Multiplication tables and Tor structures

```julia
A = OP.ext_algebra(enc; maxdeg=2)
mu = OP.Advanced.multiplication_matrix(A, 1, 1)
```

`ExtAlgebra` retains one projective self-Ext model. Its multiplication table
has shape `dim(A,p+q) × (dim(A,p)*dim(A,q))`, with column
`(i-1)*dim(A,q)+j` equal to the product of left basis vector `i` and right
basis vector `j`. Thus the matrix acts on `kron(left,right)`. Degree pairs
must be nonnegative with their sum in the computed range. Tables are computed
on request and retained by degree pair; `cached_product_degrees` reads the
already stored keys. Returned cached matrices are read-only, so copy a matrix
before editing it.

`OP.Advanced.TorAlgebra(T; mu_chain, mu_chain_gen, unit_coords)` adds supplied
chain multiplication to an existing Tor space. For `(p,q)`, supply a matrix
`C_p ⊗ C_q → C_(p+q)` with the same ordering of tensor coordinates. Missing
products with nonzero source and target are errors; a generator may supply
sparse matrices when requested. To replace multiplication data, use
`OP.DerivedFunctors.set_chain_product!` or `set_chain_product_generator!`,
which invalidate the affected stored results. Mutating a stored array or the
state captured by a generator bypasses that replacement mechanism.

Every new Tor multiplication table checks that products of cycles remain
cycles and that products involving boundaries have zero homology coordinates.
These conditions make the answer independent of the chosen representatives.
`check_tor_algebra(A; algebraic=true)` additionally checks the Leibniz identity,
associativity on homology, and both unit identities when `unit_coords` is
supplied. Its report states the verified degree range. Leibniz checks include
the extra incoming boundary degree needed for that range. These checks do not
assert strict associativity on chains or a unit that was never supplied.
Exact fields use exact equations; `RealField` uses its declared tolerances
and rejects nonfinite data.

## Visualization requests

| Input and kind | Selection and interpretation |
| :--- | :--- |
| Hom, Ext, Tor or algebra: `:graded_dimensions` | Read computed dimensions without requesting products or quotient bases. This is the Ext, Tor and algebra default; Hom defaults to `:hom_basis`. |
| Ext, Tor or algebra: `:derived_class` | `degree=0`, `vector=nothing`. Coordinates select a quotient class. Omitting the vector selects its first basis vector, or zero when the group is zero. The representative and adjacent differential equations are computed and checked. |
| `ExtElement` or `TorElement` | Use the retained algebra, degree and coordinates; degree and vector overrides are unavailable. |
| Algebra: `:product_table` | `p=0`, `q=0` select one complete degree pair. Optional `left` and `right` quotient vectors must be supplied together. |
| Projective Ext: `:yoneda_product` | Supply `right`, `p`, `q`, `left_vector`, `right_vector` and optionally `target`. This computes the selected composition and its cocycle; the right resolution reaches `p+q`. |

`matrix_limit=(rows,columns)` uses positive integers, with default `(12,12)`.
It crops the drawing while retaining full matrices and mathematical selections
in metadata. Exact coefficient strings preserve rational or modular values;
empty groups and matrices retain their actual shapes.

For a product table, `max_products=4096` bounds input basis pairs and
`max_entries=1_000_000` bounds output structure constants before multiplication
is requested. Neither bound limits all intermediate resolution or lift storage.
`validate_algebra=false` is the default. On a Tor algebra, setting it to `true`
requests the broader algebraic checks and can generate degree pairs beyond
the selected table's budget. This option is rejected for Ext algebras.

`OP.Advanced.check_visual_request` checks request shapes, degrees and budgets
without computing products. Specification construction checks model
compatibility and the algebraic equations. Invalid visual requests raise
`ArgumentError`; the mathematical operations reject incompatible models or
invalid chain products. Finite field coordinates accept exact integers and
rationals, rather than silently converting decimal inputs.

`OP.Advanced.visual_spec` returns a `VisualizationSpec` retaining provenance.
Class views add `selection`, table views add `matrix` and `basis_pairs`, and
Yoneda views add `target_space` together with the boundary adjustment from the
computed cocycle to the chosen representative. Numerical equation and zero
class checks use the field tolerances. CairoMakie and WGLMakie render these
static specifications where installed; these requests do not create linked
algebra sessions.

A product drawn as a map in an actual supplied exact sequence uses the
[exact sequence view](visualization.md). The
[implementation account](../../implementation/yoneda_products.md) explains
the representative and product checks, while the
[complex guide](../../tutorials/complexes.ipynb) follows maps and spectral pages.
