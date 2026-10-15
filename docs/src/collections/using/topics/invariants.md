# Invariants, slices and distances

A finite encoding gives us vector spaces and the maps between them. We can
keep this object and ask several different questions of it: what persists
along a line, what survives across a branching region, or how two modules
compare. An *invariant* is a quantity or construction that is unchanged when
we replace a module by an isomorphic one. Such a summary can be easier to
inspect than all the spaces and maps, although it need not determine the
module from which it came.

The guides in this group begin with an encoding or a finite module already in
hand. If you are still getting acquainted with that object, first
[explore its spaces and maps](../../../../spaces_and_maps.md). From there,
your next step depends on the question you want to follow.

## Start with a line when you want to read a barcode

Along an increasing line through the parameter plane, the parameters are
totally ordered. Restricting the module to that line gives a *slice*, whose
barcode records the intervals over which classes persist. This is a useful
way to begin reading a multiparameter example because we can follow one
direction at a time.

[Exploring slices, intervals and signed contributions](../../../../tutorials/slices_diagrams.ipynb)
starts with two overlapping strips. Following a diagonal produces one
interval; querying maps between parameters leads to a different summary,
written as a sum of rectangle contributions. The overlap explains why one
coefficient must be negative. That coefficient corrects the sum, and does
not describe a vector space of negative dimension.

Choose this guide if you want to connect a picture in the parameter plane to
its barcode or understand what the terms of a signed summary are counting.
A selected slice answers a question along that line; it leaves the other
directions available for further investigation.

## Compare two modules by varying the line

Once slice barcodes are familiar, we can compare two modules along a common
line. The *bottleneck distance* matches their intervals while minimizing the
largest matching cost. Moving the line changes the barcodes and can change
which assignment gives that minimum.

[Exact matching distance in a finite window](../../../../exact_matching.md)
asks for the supremum of these comparisons over positive-slope lines, with
a direction-dependent weight and both barcodes clipped to the same finite
rectangle. It explains the assumptions on the two encodings and follows a
witness: a line and interval assignment that realize the reported optimum.

Choose this guide when your question concerns a pair of modules and you need
to understand both the distance and the comparison responsible for it. The
chosen rectangle is part of the question. Computing its answer exactly does
not turn it into a distance over an unrestricted parameter domain.

## Query a region when several branches must agree

A line visits parameters in sequence. A region can contain incomparable
parameters whose images meet later, so we can ask whether vectors carried
along different branches agree. *Generalized rank* measures the dimension
of the image of compatible vector choices after identifying vectors related
by the module's maps.

[Querying regions and building GRIL features](../../../../tutorials/generalized_rank_queries.ipynb)
begins with two lines mapping into a plane. The individual maps have the
same ranks in two examples, yet the ranks on the whole branching region
differ. The guide then connects finite region queries to boundary barcodes
and to expanding regions in the parameter plane. The widths up to which a
chosen rank survives form a *generalized rank invariant landscape*, or GRIL.

Choose this guide when a single line leaves out the compatibility you want
to examine, or when you want numerical features built from those region
queries. You can begin with its small diagram without first computing a
matching distance. Its finite label queries and geometric regions have
different assumptions, which the examples explain where they are used.

These are complementary ways to investigate a retained module. Slices make
one ordered restriction readable; matching distance compares two modules
through a family of such restrictions; region queries follow compatibility
across several directions. You can move between the guides as the question
changes, while keeping the original spaces and maps available.
