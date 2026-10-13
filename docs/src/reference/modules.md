# Finite modules, selected vectors and submodules

A finite module assigns a vector space to each vertex of a finite poset and a
linear map to each ordered pair, with identity and composition laws. TamerOp
stores these spaces in chosen bases, so a selected vector is given by its
coordinates in the corresponding stalk. An encoding additionally retains the
classifier that assigns original parameters to finite vertices.

This reference describes how to follow selected vectors, construct the
submodule they generate and inspect the result. For a worked calculation on
two overlapping squares, use the [generated submodule guide](../../tutorials/generated_submodules.ipynb).
The [implementation account](../../implementation/submodules_and_quotients.md)
explains how the image spaces acquire their own bases and structure maps.
To enter or repair a small diagram, see the [construction guide](../../tutorials/presentations.ipynb)
and [editor contract](visual_sessions.md#author-a-finite-module-or-presentation).
The snippets below use `import TamerOp as OP` and an existing module `M` or
encoding `enc`.

## Maps between two finite modules

For modules $M,N$ on the same finite poset, a morphism is a family of linear
maps $f_p:M(p)\to N(p)$ satisfying

$$N(p\leq q)f_p=f_qM(p\leq q).$$

These equations say that applying the component before or after a structure
map gives the same result. Their solutions form the vector space
$\operatorname{Hom}(M,N)$ of natural transformations. This returned Hom is a
single vector space; an *internal Hom*, which would itself be a persistence
module, is a different construction.

`OP.hom(M,N)` computes a `HomSpace` for two `PModule` inputs on the identical
finite base with matching coefficient fields. `OP.Advanced.Hom(M,N)` is the
owning algebra operation. Inspect `OP.Advanced.hom_summary(H)` or
`OP.Advanced.dim(H)` before requesting `OP.Advanced.basis(H)`, which
materializes the individual basis morphisms.

For encodings `A,B`, prefer `OP.hom_dimension(A,B)` when only the dimension is
needed. `OP.hom(A,B)` supplies the Hom object. Both default to
`transport=:shared`, requiring the identical finite poset object, and accept
`cache=:auto` or a `SessionCache` through `cache=sc`. Explicitly requesting
`transport=:common_refinement` allows different bases and computes Hom after
restriction to their common base; the full Hom result may be lazy. The
[transport reference](change_of_posets.md) explains the abstract product used
when no realized joint image is supplied. This operation does not by itself
identify the answer with Hom in an ambient parameter category.

## Select and propagate

Choose a finite vertex `p` and a matrix `B` whose columns are coordinates in
`M(p)`. The propagation result retains these columns and their images wherever
there is a forward map from `p`:

```julia
r = OP.propagate(M; source=p, vectors=B)
summary = OP.propagation_summary(r)
A = OP.Advanced.propagation_image(r; target=q)
```

`OP.propagate(enc; source=p, vectors=B)` performs the same computation after
materializing the encoded module, and retains the encoding as context. A
`PModule` input supplies no classifier. In both forms, `p` and `q` are finite
vertex IDs in `1:nvertices(P)`, excluding booleans; they are not parameter
coordinates.

| Input | Accepted values and meaning |
| :--- | :--- |
| `vectors=v` | A vector of length `dim_at(M,p)`, treated as one selected column. |
| `vectors=B` | A matrix with `dim_at(M,p)` rows. Each column is followed separately. Dependent columns, zero columns and a matrix with no columns are accepted. |
| Coefficients | Converted to the module's field. Incompatible elements, inexact conversions and nonfinite numerical entries fail. |
| Coordinate shape | A wrong number of rows raises `DimensionMismatch`; an invalid vertex ID raises `ArgumentError`. |

The return type is `VectorPropagation`. At a vertex $q\geq p$, its matrix is
$M(p\leq q)B$, with the original column count preserved. Its reported dimension
is the rank of this matrix, hence the dimension of the span of the propagated
vectors. For example, a source selection `[1 2 0]` in a one dimensional stalk
has three columns but spans one dimension. An identity map preserves all three
columns and that rank.

The *upper ideal* of `p` is the set of vertices `q` with `p ≤ q`. Outside it,
`propagation_image` and the image dimension are `nothing`, because there is no
forward map. At a zero target inside it, the image is a matrix with zero rows
and the supplied number of columns. It is a defined zero image.

The input must be a valid module. `propagate` checks storage and compares every
applicable cover route on the selected columns. These comparisons establish
agreement on those vectors; a discrepancy on other vectors could remain
undetected. For a complete check of a hand supplied module, use:

| Check | What it verifies |
| :--- | :--- |
| `Advanced.check_module(M)` | Stored dimensions and shapes of the cover maps. |
| `Advanced.check_module_functoriality(M)` | Agreement of all cover path composites, using exact equality or the declared `RealField` tolerances. |

Both accept `throw=true`. The second uses fresh composition caches, so old cached
maps cannot conceal changed input. It can require substantial work on a large
poset and is used when saving a complete visual source.

### Read and validate a propagation result

`propagation_summary(r)` and `describe(r)` report the source, field, coordinate
convention, column count, image dimensions, applicable vertices, nonzero support
and retained encoding. Here *nonzero support* means the vertices where the
selected image has positive rank. `provenance(r)` additionally records the
finite base and a copy of the source coordinates, together with the encoding's
provenance when present. `dimensions(r)` copies the image dimension vector;
`propagation_image(r; target=q)` returns a copy of the selected matrix without
further algebra.

Exact fields give exact images and ranks. `RealField` uses its numerical rank
tolerances, which can affect dimensions and the reported support. Treat the
retained module, encoding and result arrays as read only while using the
result. A new selection starts a new computation; there is no implicit cache
of results across calls.

`Advanced.check_propagation(r; throw=false)` verifies shapes, applicability,
ranks, source columns and relevant cover equations against the retained module.
It returns a `ValidationSummary` whose `.report.valid` and `.report.issues`
describe the outcome; `throw=true` raises on failure. This check concerns the
selected images, without asserting that they form a complementary summand of
the ambient module.

## Construct the subobject and quotient

Taking the span of the propagated columns at each vertex gives the smallest
submodule containing the original selection. Its inclusion records how those
spans sit inside the ambient spaces:

```julia
S = OP.generated_submodule(r)
N = OP.Advanced.submodule_object(S)
i = OP.Advanced.inclusion_map(S)
Q, projection = OP.Advanced.quotient_with_projection(S)
```

`generated_submodule(r; cache=:auto)` returns a `Submodule` wrapper. Its module
`N` is zero outside the source's upper ideal. The inclusion `i` is a `PMorphism`
with injective components that commute with cover maps; the local bases of
`N` may differ from the original spanning columns.

`ambient_module(S)` retrieves the ambient module, and
`check_submodule(S; throw=false)` validates the constructed module and inclusion.
For advanced reuse, `cache=CoverCache` accepts a categorical cover cache on the
identical base. `quotient(S)` returns the quotient alone;
`quotient_with_projection(S)` returns it with its natural projection from the
ambient module. The projection kills each included vector, so at every vertex
its component composed with the inclusion component is zero. Both morphisms
respect the structure maps. Numerical fields use their coordinate and rank
contracts for these computations.

These are subobjects and quotients in the specified finite representation
category. A quotient does not supply a complementary submodule: such a
complement would require a compatible splitting at every vertex. These calls do not compute an
decomposition into summands or establish independence of derived invariants
from the encoding.

## Inspect the result

```julia
OP.visualize(r)
OP.visualize(r; target=q)
OP.Advanced.visual_spec(r; target=q, matrix_limit=(12,12), max_vertices=200)
```

The result has one view, `:vector_persistence`. Its finite order panel shows the
selected image dimensions, with distinct readouts for zero and absence of a
forward map. A retained supported planar classifier adds a panel of its fibers,
the parameter regions assigned to its finite labels. An optional `box` gives
a finite viewing window in the classifier's usual format; unrepresented
regions remain unknown.

The displayed support is the pullback of the finite submodule just described.
Selecting a finite vertex does not select one original parameter in its
fiber, so this support need not be the upper cone of a chosen parameter point.

| Option | Contract |
| :--- | :--- |
| `target=q` | Requests the full structure map and propagated columns in stored coordinates. An inapplicable target receives a readout stating that no map is defined. |
| `matrix_limit=(12,12)` | Two positive integers limiting the displayed rows and columns. Metadata retains complete matrices. |
| `max_vertices=200` | A positive bound on the finite graph size. Exceeding it raises rather than omitting vertices. |

Building a view validates the retained propagation and may construct planar
geometry. It computes the selected full map only when a target is requested;
it does not construct a generated module or quotient. Morphism views can
inspect a separately computed inclusion or projection and its naturality
squares.

## Link to retained source cycles

A vector in a finite stalk can be drawn on an original complex only when we
know which homology class each coordinate represents. Supply that information
as an ordered homology basis at the target:

```julia
z = OP.Advanced.propagation_source_chain(r; target=q, basis=cycles, column=1)
OP.visualize(z)
```

This operation accepts rational or prime field coefficients. `cycles` must be
a nonempty vector of `SourceChain` cycles, one per target stalk coordinate,
in that coordinate order. All cycles must use the identical source complex,
field, degree and parameter. The routine checks that their cells are active,
that their boundaries vanish and that their classes form a complete independent
homology basis. It then forms their linear combination using the propagated
column selected by `column`.

The association between these homology classes and the module's coordinates
is supplied by the caller and recorded as
`basis_identification=:supplied_by_caller`. The basis checks cannot infer this
association from equality of dimensions, or certify the homological origin
of every module map. The operation uses retained cycles; it cannot recover
discarded representatives or transport cocycles covariantly. A missing forward
map, empty basis, invalid column or incompatible cycle data raises an error.
The returned `SourceChain` retains original cell identities and geometry for
the source cell viewers. See [source representative contracts](source_representatives.md).

## Diagnose a failed commuting relation

`Advanced.module_path_witness(M::PModule)` looks for two cover paths with the
same endpoints and different composite matrices. It returns `nothing` if
all paths agree. Otherwise its record contains `source`, `target`, `first_path`,
`second_path`, `first_composite`, `second_composite` and `field`, with matrices
in the original stalk bases. Structural errors raise `ArgumentError` before
multiplication. Exact fields compare exactly; `RealField` uses the
tolerance scaled for matrix multiplication of `check_module_functoriality`.

The traversal follows cover paths without reading or changing the module's
cached composites. For each source it retains one prefix reaching each vertex
and checks alternative extensions against it. This covers merges of paths
of different lengths as well as four vertex diamonds, without enumerating
every path. The number of visited extensions is polynomial in the poset size,
although matrix multiplication can still be substantial. The diagnostic is
intended for small authored diagrams. A returned failure shows where the
supplied maps violate composition in the stated field or tolerance contract.

The [construction guide](../../tutorials/presentations.ipynb) reads such a witness
through the editor's validation report. The [inspection implementation account](../../implementation/inspection_sessions.md#keep-a-draft-distinct-from-a-mathematical-object)
explains how this traversal keeps an invalid draft separate from a committed
mathematical object.
