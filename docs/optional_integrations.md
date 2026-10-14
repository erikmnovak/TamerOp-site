# Optional integrations

TamerOp can compute a persistence diagram before any plotting package is
loaded. To draw it, import a renderer; to exchange its features with another
package, import the corresponding table or file adapter. Julia's package
extensions connect these capabilities when the required packages are loaded in
the same session, leaving each project free to choose the integrations it
needs.

## Add a renderer

In your activated Julia environment, install CairoMakie once:

```julia
import Pkg
Pkg.add("CairoMakie")
```

Then import it in each session where you want static figures. This small image
has a ring of pixels at value zero and a center pixel at value two. In degree
one its persistence interval is `[0,2)`: the hole appears with the ring and is
filled when the center enters.

```julia
import TamerOp as OP
using CairoMakie

diagram = OP.cubical_persistence([0 0 0; 0 2 0; 0 0 0])
OP.visualize(diagram; kind=:barcode, dim=1)
```

The computation uses the default coefficient field of characteristic two.
`kind=:barcode` requests intervals and `dim=1` selects the holes in degree one.
To save that view, use `OP.save_visual("barcode.svg", diagram; kind=:barcode,
dim=1)`. Computing the diagram, inspecting it and preparing its drawing
specification with `OP.Advanced.visual_spec` do not require a renderer.

WGLMakie supplies interactive rendering and HTML figure export. Install it with
`Pkg.add("WGLMakie")` and load it with `using WGLMakie`. Which controls a
figure provides depends on its object and on whether a Julia session remains
connected; the [visualization guide](visualization.md) explains those
distinctions. A missing renderer or a failed export raises an error, so a saved
summary cannot be mistaken for the requested rendered figure.

## Choose the integrations for your task

| Capability | Install and import |
| --- | --- |
| Static plots and PNG/SVG/PDF export | `CairoMakie` |
| Interactive plots and HTML figure export | `WGLMakie` |
| Reading feature CSV files and extra CSV writer options | `CSV` |
| Table interface | `Tables` |
| Data frame conversion | `DataFrames`, `Tables` |
| Arrow feature storage | `Arrow`, `Tables` |
| Parquet feature storage | `Parquet2`, `Tables` |
| NumPy storage | `NPZ` |
| Nearest neighbor acceleration | `NearestNeighbors` |
| Planar Delaunay acceleration | `DelaunayTriangulation` |
| Distance objects | `Distances` |
| Kernel objects | `KernelFunctions` |
| Batch execution through Folds | `Folds` |
| Progress reporting | `ProgressLogging` |
| Additional certification for rational indecomposable summands | `Hecke` |

For example, loading `DelaunayTriangulation` makes its faster implementation
available to `delaunay_backend=:auto`. Without it, automatic selection uses the
native implementation. An explicit request for `:fast` requires the package to
be loaded. Nearest neighbor selection behaves similarly: `:auto` can fall back
to the deterministic search that compares all candidate points. These
operations use the integrations you have loaded and do not import additional
packages themselves.

Basic feature CSV export and native ingestion of delimited datasets are
available in TamerOp alone. The CSV extension is needed to read saved feature
CSV files or pass writer keywords specific to CSV.jl. Requiring both packages
in a table row, such as `Arrow` and `Tables`, means that both must be loaded to
activate that extension.

`OP.BatchOptions(backend=:folds)` requires `using Folds` when threading is
enabled; `threaded=false` selects serial execution.
`OP.BatchOptions(progress=true)` requires `using ProgressLogging`. The batch
checks these requirements before doing any computation, including for empty
inputs.

Hecke extends the certification available for an indecomposable decomposition
with rational coefficients. After installing and loading it, `backend=:hecke`
can certify additional pieces that the native rational method may leave
unresolved, including ones whose endomorphism division algebra is
noncommutative. Here an *endomorphism* is a map from a module to itself, and a
*division algebra* is an algebra in which every nonzero element has an inverse;
noncommutative means that multiplication can depend on order. The extension
keeps the native splitting search and accepts rational coefficients only.
Finite search limits can still be exhausted, which raises an error rather than
returning a partial decomposition as complete. The [decomposition
reference](src/reference/decomposition.md#general-indecomposable-decompositions)
gives the result's contracts and the distinction from interval decompositions.

## Keep integrations in the project that uses them

Load TamerOp normally with `import TamerOp` or `using TamerOp` so Julia can
activate its extensions. Including `src/TamerOp.jl` directly bypasses that
package workflow. If an import fails, resolve the reported dependency error;
manual inclusion of an extension file does not replace package loading.

Nemo, Polyhedra and CDDLib are required dependencies for exact algebra and
polyhedral geometry. The optional packages above add capabilities around that
core. `Pkg.add` records a chosen integration in the active environment's
`Project.toml` and resolves its `Manifest.toml`. A separate environment is
useful when another project needs a different collection of renderers or
adapters.