# Change of posets and encoding comparisons

An order map $\pi:Q\to P$ lets us read a module on $P$ as a module on $Q$ by
restriction. Left and right Kan extensions provide two ways to send a module
in the other direction, using colimits or limits of its spaces. This reference
specifies those operations, the common bases used to compare encodings, and
the data their viewers inspect.

The [comparison notebook](../../tutorials/compare_encodings.ipynb) works through
two descriptions of a square and a Kan comparison. The
[prepared squares](../../tutorials/compare_encodings.ipynb#compare-the-three-pairs)
let us compare the two naturality composites for an interior pair, a zero
target and a pair with no forward map. The
[implementation account](../../implementation/change_of_posets.md) develops the
limit and colimit constructions and explains how the comparison equations
are checked. Code names below assume `import TamerOp as OP`; `Advanced` names
are available through `OP.Advanced`.

## Computation and retained results

An `Advanced.EncodingMap` retains its source `Q`, target `P` and the target
label of each source vertex. `Advanced.check_monotone_map(pi)` checks that
these labels respect the two orders. A match in vertex counts does not supply
an order map or identify the posets.

For $M$ on $P$, restriction assigns $M(\pi(q))$ to $q$ and uses the original
maps between projected labels. For $N$ on $Q$, its left Kan extension at $p$
identifies vectors with their images over the diagram $\pi(q)\leq p$, forming
a colimit. Its right Kan extension takes compatible families over
$p\leq\pi(q)$, forming a limit. All three operations retain the specified
coefficient field.

| Operation | Input and output contract |
| :--- | :--- |
| `restriction(pi, enc)` | `enc` is on `P`. Returns a `ModuleTranslationResult` on `Q`, retaining `enc` and `pi`. No ambient classifier into `Q` is inferred. |
| `pushforward_left(pi, enc)` | `enc` is on `Q`. Returns its left Kan extension on `P` in a `ModuleTranslationResult`, retaining the original result and the postcomposed classifier when available. |
| `pushforward_right(pi, enc)` | Returns the right Kan extension of an encoding on `Q`, with the same wrapper and classifier convention. |
| `Advanced.joint_encoding(left, right)` | The two monotone classifiers must have the same labelled finite source. Returns the occurring label pairs with the induced product order, without constructing the full product. |
| `common_refinement(A, B)` | Restricts both modules to a common finite base. When their bases differ, this is the abstract product; no intersections of continuous fibers are computed. |
| `common_refinement(A, B, joint)` | Uses the supplied finite joint image. Its projection targets must be the original module bases. |

The workflow calls on encodings accept `cache=:auto`, or `cache=sc` for a
`SessionCache` that retains reusable preparation. Restriction and Kan operations
also accept `PModule` and `PMorphism` inputs, returning modules and morphisms
rather than workflow result wrappers. These methods preserve the owning
module's options; see their method docstrings for `check`, threading and
`session_cache` details.

A *unit* or *counit* is a canonical comparison between a module and an object
obtained by restriction and Kan extension. With $\pi^*$ denoting restriction,
$\operatorname{Lan}_\pi$ left Kan extension and $\operatorname{Ran}_\pi$ right
Kan extension, the four comparisons are:

| Call | Module's base | Returned morphism |
| :--- | :--- | :--- |
| `Advanced.kan_unit(pi, M; side=:left)` | `Q` | $M\to\pi^*\operatorname{Lan}_\pi M$ |
| `Advanced.kan_counit(pi, M; side=:left)` | `P` | $\operatorname{Lan}_\pi\pi^*M\to M$ |
| `Advanced.kan_unit(pi, M; side=:right)` | `P` | $M\to\operatorname{Ran}_\pi\pi^*M$ |
| `Advanced.kan_counit(pi, M; side=:right)` | `Q` | $\pi^*\operatorname{Ran}_\pi M\to M$ |

These calls return `PMorphism` components in the computed coordinates. The
default `check=true` validates the order map; the module must live on the
required labelled base and must already satisfy its module relations. A unit
or counit need not be invertible.

For a common refinement, `Advanced.common_poset`, `Advanced.projection_maps`
and `Advanced.translated_modules` recover the base, its two projections and
the restricted modules. A joint result supports `encoding_map` and
`Advanced.check_joint_encoding`. On a translation result,
`Advanced.translation_map`, `Advanced.translation_kind`,
`Advanced.translated_module` and `Advanced.source_result` recover the map,
operation, new module and original result. `describe` and `provenance` expose
construction and category information without requiring direct field access.

## Static comparison views

`visualize`, `Advanced.visual_spec` and `save_visual` accept the following
objects. The common base is the poset on which both displayed modules are
restricted for comparison.

| Object | Default view | Left, right and common base |
| :--- | :--- | :--- |
| `EncodingMap` | `:order_map` | Source `Q`, target `P`, common base `Q`. |
| `JointEncodingResult` | `:joint_encoding` | Two classifier targets and their realized joint base. |
| `CommonRefinementTranslationResult` | `:common_refinement` | The projection targets and the retained common base. |
| `ModuleTranslationResult` with a finite map | `:change_of_poset` | Modules on `Q` and `P`. Restriction creates the left module; either Kan extension creates the right module. |

The Hasse views draw the order of arbitrary finite posets. Coordinate views
`:regions`, `:region_labels` and `:pushforward_overlay` are available when the
finite map has the required coordinate layout. Their coordinates show vertex
occupancy; they do not describe continuous parameter fibers.

### Supply modules, a realization witness or a comparison

`sources=(left,right)` supplies the original `PModule` or `EncodingResult`
objects for an order map or refinement view. A refinement result retains its
restrictions, so these originals must be supplied separately when needed.
A translation result already retains its source and rejects `sources`.
Compatibility checks compare fields, labelled posets and actual maps;
incompatible inputs raise `ArgumentError`.

`joint=witness` supplies evidence of which pairs occur on a declared finite
source. A `JointEncodingResult` already serves as its own witness. The witness
targets must be the displayed posets, and a realized common base must have
exactly the witness's projected pairs. Without a witness, metadata reports how
the base was constructed but does not declare absent Cartesian pairs unrealized.
No finite witness by itself proves completeness over an unenumerated ambient
parameter space.

`comparison=f` supplies a `PMorphism` between the two modules restricted to
the common base. Its direction defaults to `:left_to_right`;
`:right_to_left` accommodates a right Kan counit, for example. Endpoints must
match the actual modules and their cover maps, beyond agreement of dimensions.
Incompatible endpoints or component shapes raise. A comparison of the right
shape whose naturality equations fail remains inspectable, with those failures
reported. The natural isomorphism readout uses every cover square and the rank
of every component.

### Select a space or map

Use one selection form per request:

| Selection | Meaning |
| :--- | :--- |
| `vertex=q` | One vertex of the common base. |
| `pair=(p,q)` | A directed pair in the common base. |
| `point=(x,y)` | An exact parameter query through two retained supported planar classifiers. |
| `side=:left/:right/:base, label=q` | A label on that side and all its preimages in the common base. |

A parameter query reports missing or multiple common labels without choosing
an arbitrary candidate. Classifier label `0` means unrepresented, rather than
a represented stalk of dimension zero.

`view=:overview` links the three finite posets, their label pairs and any
available parameter geometry. `view=:square` displays the four arrows of a
selected comparison square and the two composites. Without a supplied morphism,
it shows the available maps of the two restrictions. Reversed or incomparable
pairs have no forward square.

| Display option | Contract |
| :--- | :--- |
| `box=((xmin,ymin),(xmax,ymax))` | A finite window for actual parameter geometry. |
| `max_vertices=200` | Refuses a larger displayed poset. Above 20 vertices, Hasse text labels are limited to the selection; every vertex and ID remains in metadata and live hover. |
| `max_pairs=2500` | Bounds the optional Cartesian background. Pairs belonging to the common base remain drawn. |
| `matrix_limit=(12,12)` | Crops displayed entries while retaining the full matrices. |

Matrices have source columns and target rows in the stored module coordinates.
Comparisons over rational and prime fields are exact. With `RealField`, equations
use `atol + rtol * max(maxabs(left), maxabs(right))`, and ranks use the field's
numerical rank policy. Agreement within tolerance is a numerical statement.

Preparation validates supplied modules and cover maps, materializing lazy
encodings when necessary. Session navigation reuses that preparation, although
a selected pair may still require composing transitive maps. A viewer does not
compute a missing Kan extension, unit, counit, table of all pair ranks or
derived functor. `check_visual_request` checks the recipe and selection syntax;
the full source and comparison checks occur when building the specification
or session.

## Live inspection and scope

`inspection_session(result; kwargs...)` creates an
`Advanced.TransportInspectionSession` with the same options. In `Advanced`,
`select_inspection!` changes its selection or view; `inspection_selection`,
`inspection_summary` and `inspection_snapshot` read the retained state.
`check_inspection_selection` and `check_inspection_session` validate requests
or the session. `reset_inspection!` resets selection, and `close_inspection!`
releases it. A failed update preserves the previous snapshot and revision.
Changing only the view preserves the selection; a new selector replaces it.
Keep the inputs unchanged while a session exists.

Rendering a live session requires an explicit WGLMakie import and a running
Julia process. Hasse clicks select side labels, while hover reads retained
labels without performing algebra. Controls accept exact rational parameter
coordinates and directed pairs on the common base. Multiple viewers can share
a session; disconnecting one releases its callbacks without closing the others.
Closing the session releases its source objects, prepared data and listeners,
while preserving the final static snapshot for export. The exported snapshot
has no live controls.

A commuting square and invertible components identify the two restrictions
in their displayed finite representation category. Even an invertible Kan
unit on one module does not establish an equivalence between two different
finite derived categories. Comparisons of ambient modules and derived
invariants require their own hypotheses and maps, as developed in the
[category lesson](../../math_categories.md).
