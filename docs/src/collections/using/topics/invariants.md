# Invariants, slices and distances

A finite encoding keeps spaces and maps available while we ask simpler
questions of them. An invariant is unchanged when the module is replaced by
an isomorphic one, but an invariant need not determine the module. [Exploring
slices, intervals and signed contributions](../../../../tutorials/slices_diagrams.ipynb)
is a useful first investigation: restrict to an increasing line to obtain a
slice barcode, then compare that answer with ranks of maps and signed sums
of rectangle contributions.

Once slices are familiar, [exact matching distance in a finite
window](../../../../exact_matching.md) compares two modules along a family of lines.
For each line, a bottleneck matching minimizes the largest cost of matching
intervals; matching distance takes the supremum of the appropriately weighted
comparisons. The guide follows a line and assignment attaining the answer.
Choose it when you need to understand both a distance and the comparison
responsible for it, keeping the finite window part of the question.

A branching region asks for agreement along several routes through the
module. [Querying regions and building GRIL features](../../../../tutorials/generalized_rank_queries.ipynb)
introduces generalized rank through compatible vectors and their common
images. Two maps can have the same individual ranks while their image lines
intersect differently, so the question about a whole region can distinguish them.
Expanding a chosen region and recording the widths at which a rank persists
leads to the generalized rank invariant landscape, or GRIL.

Signed summaries give another way to compare or turn results into numerical
features. Their negative coefficients correct overlap rather than represent
negative dimensions. Comparing or smoothing these signed measures requires
choices about mass, cancellation, the distance between locations and boundary
behavior. When the signed atoms are the objects we want to compare, those
choices define a different question from matching ordinary barcode intervals.

When the original calculation is too large, an approximation needs a statement
of what it preserves or how its error is controlled. A useful way to study
an approximation is to begin with a small exact answer, then vary the budget
or error parameter and compare the resulting objects. Choosing the invariant
first helps us decide which differences matter: an approximation serves our
question through the information and guarantees it retains.
