# Implementation reference

The same mathematical answer can be computed in several ways, with different
intermediate data, costs and opportunities for reuse. These accounts follow
TamerOp's choices from the operation being requested to the objects retained
and the checks that justify its result. Each develops the notation it needs and
links the mathematical or usage context at the point where it is useful. You
can begin with the computation you want to understand; there is no prescribed
reading order.

<!-- COLLECTION: implementation -->

[Exact rational coordinates](qq_coordinates.md) follows a vector into a chosen
basis. An invertible set of rows gives candidate coordinates; checking the
remaining rows decides whether those coordinates describe the supplied vector.
The same idea specializes to repeated homology queries.

[Axis-aligned box encoding](box_encoding.md) explains how the grid retains
closed points, faces and corners, carries their maps, and certifies exact
representatives without invoking general polyhedral feasibility.

[Linked inspection sessions](inspection_sessions.md) explains how related views
change together after a selection, which computations can be reused and the
difference between live Julia queries and captured browser states.
[Serialization and mathematical provenance](serialization.md) follows those
states into portable files while keeping the mathematical source, its
coordinate bases and the selected drawing separate.

[Computing generalized rank and GRIL](generalized_rank.md) follows compatible
sections through a common quotient, then explains reconstruction on a chosen
finite family, barcodes of paths along interval boundaries and exact widths for
the regions used in GRIL.

[Exact rhomboid multicover construction](rhomboid_construction.md) follows site
labels through constrained radii and signed boundaries into finite encodings.
It explains lifted cell geometry, closed depth caps and the separation between
source sampling and exact selected-parameter algebra.

[Retaining representatives and tracing them to source
cells](source_representatives.md) explains filtered chain maps, contractions
between cells of equal grade, the reversal of direction when lifting cocycles,
and a search for representatives using fewer source cells. Read it when a
source overlay needs a mathematical correspondence between computed and
original cell bases.

[Change of poset, refinement and Kan extensions](change_of_posets.md) explains
how order maps, actual linear maps and certificates relating finite source data
to the transported result are retained when the parameter poset changes.

[From selected images to submodules and quotients](submodules_and_quotients.md)
follows selected coordinates through the image engine and induced maps, then
through the quotient projection. It explains why a generated submodule need not
be a direct summand.

[Yoneda products and validated Tor algebra](yoneda_products.md) follows
comparison lifts and quotient coordinates, then explains what supplied chain
products must satisfy before they define multiplication on Tor homology.

The [landscape sampling account](feature_transforms.md) explains stored line
parameters, ambient grid queries, missing samples and conditional interpolation
bounds.

[Aligned ensembles and uncertainty computations](ensembles.md) follows repeated
observables through probe alignment, empirical reductions, confidence bands for
bounded means and resampling of whole observations, then explains how visual
selections use the prepared results.

[Relative persistence of filtered pairs](relative_persistence.md) explains when
one quotient complex suffices, when delayed subcomplex entry needs a filtered
cone, and how the actual quotient bases and connecting maps are recovered.

[Interval multiplicities and certified
decomposition](interval_decomposition.md) follows ambient Hom maps into a
scalar pairing, then endpoint pruning and simultaneous splitting maps. It
explains when a residual certifies that a module cannot be decomposed into
intervals and when a selected family leaves that question open.