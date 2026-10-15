# Geometric inputs and filtrations

Geometric input carries choices before any persistence calculation begins:
which distances matter, how cells enter, which coordinates are parameters and
what happens at a boundary. [Ingestion options and their mathematical
effects](../../../../ingestion_options.md) helps you identify the choices that change
the represented module. It is useful whenever two constructions from the same
data seem to give different answers.

[Exploring radius, depth and the finite model](../../../../tutorials/multicover.ipynb) develops
these questions through coverage. Radius determines the size of the
neighborhoods, while depth records how many must cover a point. Varying the two
coordinates gives a geometric way to understand why incomparable parameters
arise and how the construction reaches a finite module. Start here for the
worked picture behind the more specialized grade and window choices.

Near a geometric event, rounding can make distinct parameter values look
identical. [Exact rhomboid grades](../../../../exact_grades.md) follows the filtration
coordinates through queries, figures and saving. It separates the arithmetic
used to decide whether a cell has entered from the coordinates used to draw
it, so the meaning of an exact answer remains clear even when the display
cannot show two nearby events separately.

You may only need a range of coverage depths. [Exact coverage-depth
windows](../../../../rhomboid_depth.md) explains how to restrict that calculation while
preserving the intended module on the requested window. Read it when the
window is part of your mathematical question or you want to avoid constructing
irrelevant depths. The resulting guarantee is about that specified range,
which makes the boundary conventions worth checking alongside the query.
