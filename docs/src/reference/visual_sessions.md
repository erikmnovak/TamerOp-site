# Live and saved inspection sessions

An inspection session keeps a selection together with the answer it produced.
For example, selecting two comparable parameters in an encoded module retains
those parameters, their finite labels and the matrix of the structure map.
Changing the selection asks Julia to prepare another answer. Saving a selection
keeps its values and figure available after that Julia session has ended.

This reference specifies how to create, update, capture and reopen these
sessions. The [live inspection guide](../../tutorials/live_inspection.ipynb)
works through a finite encoding, while the
[reopening recipe](../../recipes/reopen_session.md) saves an ordinary interval
for use in a browser. The [visualization reference](visualization.md) describes
which mathematical objects can be drawn and the choices of view, style and
figure format.

## Choose the execution contract

A *snapshot* is the current `VisualizationSpec`: the data and instructions for
drawing an answer. A captured *state* adds the exact selection and, for
supported inspectors, the request needed to reconstruct it. A saved session
is a named collection of these states. The mathematical source, such as an
encoding or persistence diagram, is retained only when explicitly requested.

| Operation | Result | Execution requirement |
| :--- | :--- | :--- |
| `inspection_session(object; ...)` | A session that can change its selection | Julia and a supported mathematical object |
| `Advanced.inspection_snapshot(session)` | Its prepared static specification | No new selection query |
| `visual_state(session)` | A detached record of the selected view | Julia at capture time; no live callback in the result |
| `save_visual_session("view.json", states; ...)` | A data record with a checked format version | No plotting package needed to retain prepared states |
| `save_visual_session("view.html", states; ...)` | A self-contained collection of prepared SVG views and data | CairoMakie at export; browser only after export |
| `load_visual_session(path)` | A `SavedVisualSession` | Julia, with no plotting backend needed merely to load |
| `visualize(saved; state=...)` | A rendering of one stored answer | A supported rendering backend |
| `inspection_session(saved; state=...)` | A new inspector with the saved selection | Julia, a supported recorded request and its matching source |

The HTML state selector switches among the saved answers without Julia or
network access. To make a new selection, reopen a supported inspector in Julia
with its matching mathematical source. Including that source in HTML makes
it available to Julia later; the browser continues to display the prepared
states only.

Live browser controls use WGLMakie with Julia running. Static notebook figures,
a standalone browser inspector and live controls embedded in a notebook have
separate capabilities; consult the [display support matrix](../../visualization_support.md)
for the intended host. Live controls in IJulia, Pluto and VS Code have not
been qualified by the standalone browser checks.

A [parameter atlas](visualization.md#parameter-atlases) retains answers at a
finite declared set of parameters. Its live session selects source and target
states and retained event witnesses without recomputing homology. Saved atlas
states keep their figures, matrices and witness coefficients, but have no
request for reconstructing a live atlas inspector.

## Create and update a live session

`inspection_session` chooses an inspector from the supplied mathematical
object. The shared operations are available through `TamerOp.Advanced`,
abbreviated below as `A`:

```julia
A = TamerOp.Advanced
A.inspection_selection(session)
A.inspection_snapshot(session)
A.inspection_summary(session)
A.select_inspection!(session; ...)
A.reset_inspection!(session)
A.close_inspection!(session)
```

`inspection_selection` returns the selected parameters or indices, and
`inspection_snapshot` returns their current static `VisualizationSpec`.
`inspection_summary` reports the retained state, available operations and
whether the session is closed, without requesting another mathematical answer.

A direct `select_inspection!` call validates and prepares the new answer before
returning. If the request is invalid, the previous selection and snapshot
remain available. After a successful update, the session notifies the
renderers subscribed to it. An error in one of those notifications is recorded
without undoing the accepted answer; attempting another update from inside a
notification is rejected.

Treat the input object and returned mathematical data as read only. The
session cannot detect arbitrary changes to the underlying maps or encoding,
so construct a new session after making such changes. Query options for each
kind of object are described below and in the [visualization reference](visualization.md).

Reset follows the selected object's contract. For a module inspector it clears
the selected endpoints and basis opt-in while retaining its view, viewport,
supports and slice line. Other families can restore their own initial query.
Closing releases live resources while leaving the last selection and static
snapshot available. Closing it again has no effect; a new query requires a
new session.

### Continuous browser requests

A slider may move again while Julia is answering its previous request. For
retained filtered complexes and slices of encoded modules, all viewers of one
session therefore share one running request and one waiting request. A new
request replaces the waiting one. The running calculation prepares its answer
separately, and the session checks that it is still wanted before accepting it.
The displayed selection continues to describe the old answer until the new
answer is accepted.

The exact entry and Reset controls for filtered complexes, and slice Apply,
use the same queue. Applying exact text preserves its coordinates; a pending
readout distinguishes that request from the answer still on screen. As with a
gesture, a newer request can replace an exact entry that has not started.
The [control reference](visualization.md#continuous-filtration-controls)
specifies slider ranges, pointer approximations and steps between exact events.

A direct `select_inspection!` or reset supersedes pending gestures. Closing a
viewer cancels its requests; closing the session cancels every request. An
algebraic calculation already running may finish before its answer is discarded.
When a viewer is disposed after disconnection, its plot updates stop; other
linked viewers retain the shared mathematical session.

For these two session families, `A.inspection_summary(session).requests` reports
whether a request is `pending` or `running`, together with counts of requests
`submitted`, `committed` and `discarded`. These describe queued browser
requests; direct Julia selections do not increase them. A replaced or obsolete
request counts as discarded. Cancelling a waiting request or encountering a
query error does not add a committed answer, so these counters are not a
partition of all submitted requests. The queue retains no unbounded history
of visited parameters. Capture or save once the desired answer is accepted,
since a pending gesture has not yet changed the snapshot.

### Finite modules and encodings

```julia
inspection_session(object; view=:module, box=nothing,
    matrix_limit=(12, 12), cache_limit=16,
    upset=nothing, downset=nothing,
    slice=nothing, slice_scope=:window, slice_limit=512)
```

`object` is a finite `PModule` or an `EncodingResult`. An encoding can also
show geometry and accept original parameters when it retains a supported
planar classifier, the map assigning each parameter to a finite label.
`box` fixes the viewing window without changing the module.

| View | Coordinates or values shown |
| :--- | :--- |
| `:module` | Spaces and maps in the stored finite module's bases. |
| `:presentation` | Spaces and maps in the image bases of a retained indicator presentation; this requires a fringe witness. |
| `:rank_from` | Ranks of maps with the source endpoint fixed. |
| `:rank_to` | Ranks of maps with the target endpoint fixed. |

The last two views are sections of the ordinary pair rank: both coordinates
of the chosen endpoint remain fixed while the other endpoint varies. See
[spaces and maps](../../spaces_and_maps.md) for the relation between a module
and its presentation coordinates.

Use one selector at a time: `vertex`, `pair`, `point` or `parameter_pair`.
Parameter selections retain their supplied coordinates and finite labels.
Comparability is checked in the original parameter order even when two points
share a label. A classifier result outside the represented labels supplies no
stalk; it must not be interpreted as a represented vector space of dimension
zero.
`input=:pointer` identifies approximate pointer coordinates; supplied values
use `:provided`.

`matrix_limit` restricts displayed entries, not construction of the map.
`cache_limit` bounds each of the caches for selected algebra and slice
results; zero disables them. A slice retains the line and its requested
scope. With `slice_scope=:window`, an interval reaching the window boundary
may be censored: the available restriction does not determine its endpoint
beyond that boundary. A `:global` request needs a classifier representing the
whole line and enough information to certify its outer behavior. Interval
IDs belong to the current line and are cleared when that line or its scope
changes. The [slice guide](../../tutorials/slices_diagrams.ipynb) develops these endpoint
conventions.

### Ordinary intervals

```julia
inspection_session(diagram; dim=0, window=nothing, max_intervals=200)
A.select_inspection!(session; interval=1, member=1, representative=true)
```

`dim` chooses the homological degree. An interval group collects intervals
with the same endpoints and endpoint decorations, which specify whether each
end is included. Grouping also preserves whether endpoints are finite,
certified infinite, or censored by a restriction window. `member` identifies
an original interval within that group.
Representatives are read only when explicitly requested and when the original
computation retained them. The window and display limit affect the drawing
without changing the endpoints, and selecting an interval does not rerun
persistence.

Interval inspectors also accept raw barcodes and supported slice or projection
results, using `index` when a member of a barcode family must be chosen. Those
inputs can supply saved snapshots, but live restoration through
`inspection_session(saved)` is supported here only for an ordinary
`PersistenceDiagram` with a matching saved source.

## Query generalized-rank regions

`generalized_rank_session` retains the rank of the natural map from the limit
to the colimit over a selected region. The [generalized rank account](../../implementation/generalized_rank.md)
constructs this map, explaining how compatible vectors and identifications
along structure maps determine it.

```julia
generalized_rank_session(M; vertices, witnesses=false, boundary=false)
```

This returns an `Advanced.GeneralizedRankInspectionSession`. `M` may be a
finite `PModule` or an `EncodingResult`. `vertices` must contain distinct
labels forming a nonempty connected, order convex subset: any two selected
vertices must be joined by a path of comparable selected vertices, and every
vertex between two selected comparable vertices must also be selected. The
supported fields are $\mathbb Q$ and prime fields. The default retains the
scalar rank; `witnesses=true` additionally retains the limit, quotient and
comparison matrices. `matrix_limit=(8,8)` bounds their displayed entries.

`boundary=true` additionally requires a two dimensional grid encoding with
both axes increasing, the actual product order and labels in Julia's column
major array order. It computes the boundary barcode on grid indices described
below. `occurrence=0` and `bar=0` mean no selection; positive values index the retained path and
barcode entries. Multiplicities are not expanded into indistinguishable rows.

The alternative constructor selects a continuous closed region called a
*worm* on the same supported grid encoding:

```julia
generalized_rank_session(enc; center, width=0, length=1,
    levels=(1,2,3), lengths=(1,2,3), level=1)
```

For length one, a worm is the closed square with the supplied center and
half side length `width`. Greater lengths extend that square continuously
along the direction $(1,-1)$; the [geometric definition](../../implementation/generalized_rank.md#from-a-grid-encoding-to-a-continuous-worm)
give its precise boundaries. The landscape records the supremum of widths
for which the generalized rank is at least a specified level: their least
upper bound, which need not itself be an admissible width. `level` chooses
one of these retained landscape layers.

The center is a planar tuple or vector. Integer, rational and finite floating
coordinates keep their exact represented values, and width must be
nonnegative. The positive integers `level` and `length` must occur in the
declared `levels` and `lengths` families. The grid module takes its lower
left label on each half open cell, is zero below either first axis coordinate,
and stays constant along the upper tails. These boundary conventions are
part of the query. Finite label witnesses and boundary barcodes are unavailable
for this continuous region.

Both constructors accept `budget=Advanced.GeneralizedRankBudget()` and
`max_vertices=120` for the finite drawing. Budget failures raise an error
without accepting a partial answer. The encoding input first goes through
`encoding_module`, which materializes and caches a lazy input's full finite
module before checking query and drawing budgets. Those budgets therefore
do not bound initial materialization.

| Selection through `Advanced.select_inspection!` | Computation |
| :--- | :--- |
| Changed finite `vertices` | New region rank; clears the old occurrence and bar selections. |
| `witnesses`, `boundary` | Additional finite region computations as requested. |
| `occurrence`, `bar` | Retained boundary selection; no rank computation |
| Worm `center` | New landscape for the declared levels and lengths, and a new worm rank. |
| `width`, `length` | New worm rank; reuses the landscape at this center |
| `level` | Displays a retained layer; reuses both landscape and worm rank |

`inspection_selection`, `inspection_summary`, `inspection_snapshot`,
`check_inspection_selection`, `check_inspection_session`, `reset_inspection!`
and `close_inspection!` use the shared Advanced lifecycle. Invalid updates
preserve the old selection, snapshot and counters. Closing releases the input
and listeners but retains the final snapshot. Summary counters distinguish
region/worm queries, landscape calls and boundary calls; they are not a count
of every elimination inside those compound operations.

With Julia running, the WGLMakie viewer offers exact entry from the keyboard,
selection of finite vertices and boundary occurrences or bars, and selection
of a worm center and landscape layer. Pointer coordinates are approximate,
while hover reads retained values without a query.
`visualize(Advanced.inspection_snapshot(session))` and `save_visual` produce
static views; exporting a linked inspector itself is rejected. The
[usage guide](../../tutorials/generalized_rank_queries.ipynb) develops these choices through examples whose ranks can be calculated by hand.

### Boundary barcode data

`Advanced.boundary_zigzag(M, grid; vertices, budget)` accepts a finite module
and a supported grid or its compiled wrapper. It returns a
`BoundaryZigzagResult`. Its path follows the selected region's grid boundary,
and can visit the same finite label more than once. Each visit is a separate
*occurrence*, indexed by its position in the path; barcode endpoints refer to
these positions and include both ends. The input must be a supported finite
region, rather than a continuous worm or an arbitrary supplied path.

- `Advanced.boundary_path(result)` returns copies of `vertices`, `indices`,
  `arrows` and `dimensions`. Indices are lattice positions. Arrow sign `+1`
  means left-to-right; `-1` means right-to-left. Repeated labels are distinct
  positions joined by the indicated maps, including an identity when required.
- `Advanced.boundary_bars(result)` returns `(first, last, multiplicity)` tuples.
  Endpoints are one-based, inclusive path occurrences. Multiplicities are positive.
- `generalized_rank(result)` returns the multiplicity of bars spanning the
  complete path, checked against
  the original region rank. `describe(result)` reports scope and query count.
- `Advanced.check_boundary_zigzag(result; throw=false)` checks retained shapes,
  barcode dimension reconstruction and agreement between full path bars and
  the region rank. It does not rerun
  the original module maps.

This computation obtains the rank on each contiguous part of the path and
recovers interval multiplicities by finite differences. For `t` occurrences
it requests `t*(t+1)/2 + 1` ranks, including the original region check, and
the algebra budgets count repeated stalks. Its result decomposes the boundary
path representation into intervals; it does not decompose the ambient module.

## Summands of a finite module

`summand_session(result_or_collection)` explores a checked direct sum splitting
of a finite module. The snapshot compares the dimensions of the full module,
selected summands and remaining summands at each vertex. A checked splitting
and a supplied drawing of its supports are recorded separately, since a
proposed support drawing can require further verification. Ordering and
filtering the displayed summands, support layouts and optional ordinary Hom
queries are specified in the [decomposition reference](decomposition.md#checked-summand-collections-and-visual-inspection).
The [decomposition guide](../../tutorials/decomposition.ipynb) follows the same
square from multiplicities to supports and actual maps.

The common selection, validation, reset, close and capture operations apply.
A source and target pair selects a structure map inside the focused summand.
A Hom pair instead selects two summands and asks for module morphisms between
them. Saved states preserve their readouts and figures, but there is no source
representation for reopening arbitrary summand queries from that saved file.
The live browser controls require Julia and WGLMakie.

## Author a finite module or presentation

`module_editor` makes an independent draft of a finite module or indicator
presentation. The draft can retain a failed relation so that you can inspect
and repair it before constructing a mathematical object. It has type
`Advanced.ModuleEditorSession`; its main operations are:

```julia
module_editor(M; history_limit=32, max_vertices=32,
    max_dimension=32, max_entries=20000)
module_editor(; order, dimensions, maps, field=CoreModules.QQField(), ...)
module_editor(; order, upsets, downsets, matrix, field=CoreModules.QQField(), ...)
edit_module!(editor; map=((source, target), coefficient_matrix))
editor_object(editor)
editor_code(editor)
```

`M` may be a finite `PModule` or `FringeModule`. With a raw constructor,
a valid module or presentation requires the following data.

| Input | Meaning and required form |
| :--- | :--- |
| `order` | The full relation matrix: `order[i,j]` records $i\leq j$, including the diagonal and all transitive relations. |
| `dimensions`, `maps` | One nonnegative dimension per vertex and exactly one matrix for each cover $i<j$, meaning a comparable pair with no vertex strictly between them. Rows use the target basis and columns the source basis. |
| `upsets`, `downsets`, `matrix` | Lists of vertex IDs for each support in an indicator presentation. Upsets must be closed upward and downsets downward. Matrix rows index downsets and columns index upsets; an entry whose two supports have empty intersection must be zero. |

The supplied order, supports and matrices are validated as entered. In
particular, the editor does not add missing transitive relations or complete
the closure of a support. The [construction guide](../../tutorials/presentations.ipynb)
explains indicator presentations, and the [recipe](../../recipes/build_module.md)
constructs a diamond whose two paths agree. Drawing a finite diagram supplies
no assignment from ambient parameters to its vertices.

### Draft validity and edit history

A draft with inconsistent composites remains visible because those matrices
are the information needed to repair it.
`Advanced.check_module_editor(editor; throw=false)` returns `valid`, `issues`,
`witness`, `field` and `input_kind`. When two paths disagree, the witness
contains both paths and their composite matrices; see
[`module_path_witness`](modules.md#diagnose-a-failed-commuting-relation).
Wrap the report in `Advanced.VisualizationValidationSummary` for a compact
notebook display, or use `throw=true` to raise `ArgumentError` when it is
invalid. The separate `check_inspection_session` operation checks the session's
stored state and cleanup conditions, so it can accept a correctly recorded
editing session whose draft still has mathematical errors.

`edit_module!` replaces supplied `order`, `dimensions`, `maps`, `field`, or
presentation `upsets`, `downsets`, `matrix` in one undoable transaction. The
single-map form `map=(edge, nothing)` removes an entry. Do not supply `map`
and `maps` together. Changing a dimension does not resize its adjacent maps.
Malformed input types, literal syntax and budget violations leave the draft,
selection and history unchanged. Rational and prime fields use exact equality.
Real fields use the numerical tolerance for matrix composition, scaled by the
matrices being multiplied. Editing the field reinterprets the entered numbers
and validates them again; it gives no assertion that the resulting module is
unchanged. For example, `1/3` cannot be entered over $\mathbb F_3$, the field
with three elements, because its denominator is zero there.

| Advanced operation | Meaning |
| :--- | :--- |
| `editor_draft(editor)` | Independent copy of entered data, including invalid data |
| `select_inspection!(editor; vertex, edge)` | Select a stalk or entered cover matrix; no history entry |
| `undo_module_edit!(editor)` / `redo_module_edit!(editor)` | Move one step through retained draft edits |
| `reset_inspection!(editor)` | Restore initial input as an undoable edit |
| `inspection_summary(editor)` | Validity, selection, revision, history lengths, budgets and listener diagnostics |
| `inspection_snapshot(editor)` | Static panels, including failed paths and coefficients when present |
| `close_inspection!(editor)` | Release editable data, history and listeners; retain the final snapshot |

History is bounded by `history_limit`; zero disables undo. A new edit clears
redo. `max_dimension` bounds matrix axes, stalk dimensions and the number of
supports in each family. `max_vertices` bounds order axes and the number of
vertices listed in each support. `max_entries` bounds the total entries in
all cover matrices or in the presentation matrix.
These limits bound the entered draft. The separate matrix display shows at
most 12 rows and 12 columns.

### Export and live controls

`editor_object` constructs a fresh, checked ordinary mathematical object.
`editor_code` generates Julia source from the checked numerical data, with
qualified names for the required operations. Both require a valid open draft.
Code export supports the rational field `QQ`, prime fields and real fields
using Float16, Float32 or Float64. Entered text and loaded data are never
evaluated as Julia code. Save the returned source with
`write(path, editor_code(editor))` and review it before running it.

`visualize(editor; backend=:wglmakie)` provides keyboard-accessible table
controls for order, dimensions, coefficients, fields and indicator supports,
together with undo, redo and downloads. Semicolons separate matrix rows, and
fractions such as `1/3` retain their exact values. Explicit row and column
counts preserve the shape when one axis is empty. The field control accepts
QQ, F followed by a prime, or Real(Float16), Real(Float32) or Real(Float64).
These controls require Julia. For a static figure, render
`inspection_snapshot(editor)` with CairoMakie or WGLMakie instead.

`save_visual_session(path, editor)` retains the draft in the snapshot,
including invalid input and its diagnostics. `module_editor(load_visual_session(path))`
revalidates that draft in Julia and begins a fresh history. Neither callbacks
nor undo history are serialized. Saved HTML shows the retained answer offline;
it cannot edit coefficients. Closing an editor leaves its last snapshot
saveable, while new object/code export requires an open editor.

## Capture a selected view

```julia
frame = visual_state(session)
```

`frame` is an independent copy of the selected view. It keeps the specification,
selection, axes, scales and layout, so later selections in the original session
do not alter it. For an inspector with supported live restoration, it also
records the construction options and selection request as data. These are
instructions understood by the supported loader, with no saved Julia code
or callbacks.

The result type is `Advanced.VisualSessionState`.
`describe(frame)` reports its visual kind, selection, resumable family and
omitted metadata. Style and figure size are supplied separately when saving.
Capture retains the specification's declared windows and axes. It does not
read a renderer's transient camera, pan or zoom state.

For an inspector with live restoration, capture records a *source content
identity*, a SHA-256 digest, or fixed length value, computed from a canonical
representation of the complete source data. This
identifies the retained data and coordinates rather than the isomorphism
class of the module. Computing it can materialize a lazy encoded module and
validate its maps; even a change away from the selected readout changes the
identity. Capture the specification directly when you need a static view
without this source calculation or a request for live restoration:

```julia
static_frame = visual_state(Advanced.inspection_snapshot(session);
    selection=Advanced.inspection_selection(session))
```

For a specification, `selection` defaults to an empty named tuple. Supplying
it as above keeps the selected values alongside the figure; it does not add a
request for reconstructing an inspector.

The saved data support exact scalars, coefficient fields, supported containers
and visual layers. Callbacks, locks, caches, renderer handles and arbitrary
runtime objects are excluded. Metadata with no supported data representation
is reported in `describe(frame).omissions`; a displayed description of an
object cannot serve as its mathematical source.

A closed session can still supply a static capture. Its released mathematical
object and live callbacks are not recovered by capturing that snapshot.

## Save one state or a named collection

```julia
save_visual_session(path, input; object=nothing, object_path=nothing,
    selected=nothing, caption="", title="Saved mathematical views",
    style=VisualStyle(), size=nothing, provenance=(;), max_bytes=268435456)
```

```julia
save_visual_session("view.json", session;
    object=enc, caption="The selected structure map.")

save_visual_session("views.html", (overview=frame1, selected=frame2);
    selected=:selected, caption="Two prepared views of the same result.")
```

Create the containing directory before saving. The principal arguments are:

| Argument | Accepted value and effect |
| :--- | :--- |
| `path` | A `.json` or `.html` path, choosing the saved format. |
| `input` | A session, captured state, supported visual specification, or named tuple containing such values. A single input receives the name `:view`. |
| `selected` | A symbol naming a saved state. The default `nothing` selects the first one. |
| `caption`, `title` | Text accompanying the collection. |
| `provenance` | A named tuple of explanatory data about the figure's origin or construction. It is not a mathematical certificate. |
| `style`, `size` | The shared `VisualStyle` and optional `(width, height)` for the saved figures. Pass a nondefault style explicitly; capture does not read the renderer's palette. |
| `max_bytes` | A positive integer limiting the file size, with a default of 256 MiB. |

Collections contain between 1 and 128 named states, and each name contains
1 to 256 UTF-8 bytes. Saving first prepares a complete temporary file, so an
encoding or rendering failure leaves an existing destination intact.

By default the file retains prepared states and readouts. `object=...` can
include a finite module, supported encoding or ordinary `PersistenceDiagram`
in TamerOp's supported mathematical data format. A state can use that source
to reopen an inspector only if capture recorded a supported construction
request. Attaching a source to a static specification does not create one.
Conversely, saving a persistence diagram by itself retains the result without
the selected member, viewing window or figure choices.

An attached or referenced source must match every resumable frame's captured
identity. Saving also reconstructs the supported requests and compares their
selections and prepared answers with the retained frames. These checks can
repeat mathematical query work. A different source is rejected even when one
selected readout happens to be equal.

An ordinary encoding file reconstructs the module as the image of its
indicator presentation and may therefore use different bases. A source saved
with a visual session retains the original finite module coordinates as well,
so reopening uses the same matrix convention. This representation has a
default limit of 10,000 vertices and validates the module data, including
agreement of composites along different cover paths. The
[serialization account](../../implementation/serialization.md#a-coordinate-matrix-needs-more-than-an-isomorphism-class)
explains why equality of ranks alone would not preserve a selected matrix.

`object_path` refers to a supported source file inside the directory containing
the saved session. The file can hold a visual source record, encoding or
ordinary diagram in TamerOp's formats. The reference records its relative path,
a digest of the file bytes and the source content identity, so preserve the resource and its
relative location when moving the collection. An absolute input path is
accepted only when the resolved resource lies inside that directory; the
stored path is always relative.

Opening a prepared view does not read that resource. Resuming queries does,
and rejects a missing or changed file. When both `object` and `object_path`
are supplied, their source identities must agree, including the module
coordinates. Referencing a plain encoding file is therefore sufficient only
when its reconstructed coordinates agree with those used to capture the view.

### JSON and HTML preserve different presentations of the same record

JSON stores the versioned session data for later inspection or rendering in
Julia. HTML embeds the session data and SVG for every retained state, along
with its own state-selection controls. The browser shows the selected
figure and its mathematical context, and offers downloads of the plotted
values and complete session record.

HTML does not fetch a renderer, mathematical source or script from the
network. The state and download controls require JavaScript; the initial figure
remains visible when those controls cannot run. A fragment such as
`#state=selected` identifies a named prepared view. Complete figures can be
scrolled on a narrow screen without reducing their labels to fit its width.

Connectors in composed figures keep their recorded coordinates and the status
of any previously checked correspondence. An explanatory arrow supplied by the
author remains an authored annotation. Reopening the figure reads that record
without rerunning its checks or relating it to a changed source object.

## Load, inspect and resume

```julia
saved = load_visual_session("views.html")
ids = Advanced.visual_session_states(saved)
selection = Advanced.inspection_selection(saved; state=:selected)
snapshot = Advanced.inspection_snapshot(saved; state=:selected)
visualize(saved; state=:selected)
```

`load_visual_session(path; max_bytes=268435456)` accepts either representation
and returns an `Advanced.SavedVisualSession`. It validates format version 1,
the content digest and the supported data types. For HTML, it reads the
embedded record without executing the page's JavaScript. A plotting package
is needed only when rendering. Omitting `state` selects the file's initial
state; an unknown state name raises an error.

`describe(saved)` and `Advanced.inspection_summary(saved)` report the state
names, initial selection, source location and identity, supported restoration
families and omissions. `Advanced.check_visual_session(saved; throw=false)`
checks the state names, requests, snapshots and source reference structure,
returning a report with `valid` and `issues`. With `throw=true`, an invalid
record raises an error. This check reads no referenced source and performs
no mathematical query; source contents are checked when resuming. The digest
detects altered data but does not authenticate who supplied them.

```julia
resumed = inspection_session(saved; state=:selected, object=nothing)
```

This constructs a new supported live session from the retained request and
source, then restores its selection through the normal validation path.
Caches and callbacks are created afresh. Supplying `object` can replace an
unavailable source file only when it matches the recorded content identity;
it cannot add a source to a session saved without one.

Each case below can restore its recorded static view when the snapshot uses
supported visual layers. Resuming live work has the following conditions:

| Saved material | Live restoration |
| :--- | :--- |
| Prepared specification and selection only | No recorded construction request. Attaching a source alone does not add one. |
| Matching finite module source and supported recorded request | Supported in Julia. |
| Matching encoding source with supported classifier and recorded request | Supported in Julia. |
| Matching ordinary diagram source and recorded interval request | Supported in Julia. |
| Editor snapshot containing its input draft | `module_editor(saved)` revalidates the draft and starts a new history. |
| Other inspector's prepared snapshot | No general route through `inspection_session(saved)`; consult that family's contract. |
| Capture made after closing an ordinary or finite module inspector | No construction request is recovered from its released source. |

A source missing from a saved state is unavailable, not a zero mathematical
answer. Invalid selections, incompatible requests, unsupported format data
and changed source identities raise errors when the corresponding operation
validates them.

## Export a saved figure with its data record

```julia
save_visual("figures", "selected", saved; state=:selected, format=:svg)
save_visual("figures/selected.pdf", saved; state=:selected)
```

These saved-session overloads use the stored style and size unless overridden.
SVG, PNG and PDF exports default to `sidecar=true`: alongside the image at
`path`, they write `path * ".json"`. Thus `selected.svg` has a companion
`selected.svg.json` that can be opened with `load_visual_session`.

This companion file, called a *sidecar*, holds the static snapshot with its
exact available plotted values, selection, caption and provenance. It records
the original source identity together with the image's filename and SHA-256
digest, so the data identify the exported image. Loading the companion recovers
the data without reading that image. It contains neither the full mathematical
source nor a request for live restoration. Use `sidecar=false` when only the
image is needed.

Both files are prepared before either destination is replaced. Each individual
replacement is atomic, meaning that a reader sees the complete old or new
file. The two replacements are separate operations, so an interruption
between them can leave the old companion beside the new image.

`save_visual(...; format=:html)` exports the chosen state as HTML containing
the static answer and the original source identity in its provenance. This
export does not carry the full source, even when the input saved session
includes one. Use `save_visual_session` when keeping a collection or attaching
a supported source for new queries.

## Costs and preservation limits

Capturing and saving copies prepared data. A resumable capture also identifies
its complete source, potentially materializing a lazy module and checking its
maps. Saving with that source repeats supported requests to check the selected
answers. Multiple states retain multiple snapshots, and HTML additionally
retains every rendered SVG. Including a mathematical object increases storage
and may require materializing the data
needed to serialize it. Runtime caches are excluded.

Restoring a recorded snapshot avoids its original mathematical query; rendering
still has a cost. Resuming an inspector can recompute construction and selected
queries. Display budgets do not establish bounds on that mathematical work.
Stored exact values remain separate from the numerical coordinates used for
drawing. A different rendering environment can therefore change the layout
without changing the retained mathematical data.

For the computation behind these choices, see
[linked inspection sessions](../../implementation/inspection_sessions.md) and
[serialization and provenance](../../implementation/serialization.md).
