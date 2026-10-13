# Compose a scalar background and signed changes

Suppose we have a table of dimensions and want to show which changes recover
its entries by summation. We will use the square $[0,2)^2$: its dimension is
one inside the square and zero elsewhere. The following calls place its
signed changes over a gray background of sampled dimensions.

```julia
import TamerOp as OP
using CairoMakie

xs = [-1, 0, 1, 2, 3]
ys = [-1, 0, 1, 2, 3]
values = [Int(0 <= x < 2 && 0 <= y < 2) for x in xs, y in ys]
atoms = OP.SignedMeasures.point_signed_measure(values, (xs, ys))

context = OP.VisualContext(domain="square parameters",
    units=("x", "y"), provenance="square support formula")
background = OP.visual_panel(permutedims(values); x=xs, y=ys,
    quantity="dimension", context)
changes = OP.visual_panel(atoms; kind=:signed_atoms, context,
    limits=(x=(-1, 3), y=(-1, 3)))
overlay = OP.overlay_visuals((background=background, changes=changes);
    title="A square and its signed changes")
OP.visualize(overlay)
```

An atom is a point with a weight. Here the lower corner $(0,0)$ has weight
$+1$, the corners $(2,0)$ and $(0,2)$ have weight $-1$, and $(2,2)$ has
weight $+1$. To recover the dimension at $(x,y)$, sum the weights at points
whose coordinates are at most $x$ and $y$. At $(1,1)$ only the first atom
contributes, giving one. At $(2,1)$ the negative atom on the right has entered
the sum and cancels it. Beyond both upper boundaries, the last positive atom
corrects for subtracting the first contribution twice.

![Two sums of the square's signed atom weights. At the query one comma one, only the positive atom at zero comma zero is included, giving dimension one. At two comma one, the negative atom at two comma zero also contributes, giving zero. The shaded rectangles identify which atoms are included in each sum.](../assets/composition/cumulative_weights.svg)

*Each shaded rectangle selects atoms below the query in both coordinates.
Its lower and left edges are cuts made by this schematic's viewing window;
the mathematical sum includes all atoms below the query.*

`VisualContext` records the common parameter domain, units and data description
so composition can check that the panels agree. The table's first index is
$x$, while rows of the plotted matrix follow $y$, which explains the
`permutedims` call. The shaded cells in the computed background are centred on
grid samples. Their edges are drawing conventions; the support's precise
included and excluded boundaries come from the supplied square formula.

We can add an explanation at a chosen place in the figure by naming its panel
and giving two endpoints in data coordinates. Here they bound a highlight of
the square:

```julia
note = OP.VisualAnnotation(
    OP.VisualAnchor(:square; point=(0, 0)),
    OP.VisualAnchor(:square; point=(2, 2));
    kind=:highlight, label="The square support")
figure = OP.compose_visuals((square=overlay,); annotations=(note,),
    title="The square support and its dimension samples")
OP.visualize(figure)
```

The dashed highlight records an explanation we supplied. A solid connector
has a more specific meaning when it comes from a checked computation: the
[composition guide](../tutorials/compose_figures.ipynb) connects a retained
source cycle to its actual barcode interval and explains what that check
establishes.

Save the selected figure as SVG for a document, or as HTML to open it in a
browser:

```julia
OP.save_visual("figures", "square", figure; format=:svg)
OP.save_visual("figures", "square", figure; format=:html)
```

The HTML embeds the SVG and descriptions of its annotations. It can reopen
without Julia or network access, with a scrollable figure at the saved size
on narrow screens. It preserves this selected picture. To save several
selections and resume supported queries, continue with the
[saved session guide](../tutorials/live_inspection.ipynb).

For a scalar field with more than two coordinates, first choose which two
coordinates will vary and fix the others. The
[features guide](../tutorials/features.ipynb) uses `ScalarField` and
`field_session` for that construction. The
[composition reference](../src/reference/visualization.md#composing-views-and-annotations)
gives the compatibility conditions for combining the resulting panels.
