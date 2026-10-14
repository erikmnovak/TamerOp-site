# Interval multiplicities and certified decomposition

A finite encoding retains enough algebra to ask whether a particular interval
occurs as a direct summand. Restricting to that interval loses boundary maps,
so its generalized rank cannot answer this question. We instead compute maps
both into and out of the interval module on the whole finite base.
Their compositions detect the part that admits a retraction.

The [mathematical lesson](../decomposition.md) explains the distinction;
the [usage guide](../tutorials/decomposition.ipynb) constructs a splitting.
This account follows a single multiplicity calculation into a search for all
interval summands, then explains how to recover compatible inclusions and
projections. The separate
[`indecomposable_decomposition` operation](../src/reference/decomposition.md#general-indecomposable-decompositions)
also seeks pieces that are not intervals; the interval algorithm here answers the narrower
question by exploiting the form of an interval module.

## A small pairing measures the multiplicity

Fix a nonempty connected, order-convex interval $I$, and let $L=k_I$ be its
interval module. Thus $L$ has a copy of $k$ on $I$, identity maps within $I$,
and zero spaces elsewhere. Every endomorphism of $L$ is multiplication by
one scalar: the identity maps force the scalars at comparable vertices to
agree, and connectedness carries that equality across $I$. Composition
therefore gives a bilinear pairing

$$
\operatorname{Hom}(M,L)\times\operatorname{Hom}(L,M)\longrightarrow k,
\qquad (g,f)\longmapsto gf.
$$

Choose bases $f_1,\ldots,f_a$ and $g_1,\ldots,g_b$. The matrix $C$ is defined
by $g_jf_i=C_{ji}1_L$. At any one vertex $q\in I$ this is just the product
of a row and a column. The resulting scalar is the same throughout $I$, so
we can compute it at one vertex even when the interval branches.

The rank of $C$ equals the multiplicity. A nonzero pairing yields maps
$f:L\to M$ and $g:M\to L$ whose composite can be rescaled to $1_L$,
splitting off one copy. Relative to this splitting, the matrix has a
nonzero scalar block for that copy, together with the pairing of the complement.
Induction gives exactly $\operatorname{rank}C$ copies. If the residual pairing
is zero, another split copy would provide a nonzero composite, a contradiction.
This argument works over the supported exact rational and prime fields; it
requires no algebraic closure.

TamerOp obtains the two Hom bases from its existing naturality solver. The
unknowns are the component entries on $I$, and equations use every ambient
cover touching those entries. Here a cover $u\lessdot v$ is an ordered pair
with no vertex strictly between them. For $M=(k\xrightarrow{1}k)$ and $I=\{2\}$,
the incoming edge forces every map $M\to k_I$ to be zero. Omitting this edge
would incorrectly report a copy. The exact solver processes the naturality
equations incrementally, constructs the two bases for their composition, and
discards them after returning a scalar multiplicity.

For the square in the [guide](../tutorials/decomposition.ipynb), the calculation
at $I=\{4\}$ is particularly visible. The two arrows into vertex 4 together
span the first two coordinates of $k^4$. A map $M\to k_I$ must annihilate those
coordinates, while a map $k_I\to M$ can choose any vector at vertex 4. Using
the four coordinate columns for the latter maps and the last two coordinate
rows for the former gives

$$
C=\begin{pmatrix}0&0&1&0\\0&0&0&1\end{pmatrix}.
$$

Its rank is two. The last two coordinates admit projections back to the
interval, which explains why the multiplicity is two although the stalk at
vertex 4 has dimension four.

[Asashiba and Liu](https://arxiv.org/abs/2411.11594) study this multiplicity
problem through formulas involving structure maps and presentations. TamerOp
uses the composition pairing above for the multiplicity itself and their
criterion involving the top and socle to narrow the possible endpoints, as
described next. These calculations use the package's exact linear algebra
without an external decomposition solver.

## Use endpoints to eliminate impossible summands

At vertex $v$, the **top** is the quotient of $M_v$ by the sum of incoming
images, and the **socle** is the intersection of outgoing kernels. They
describe, respectively, directions not supplied from below and directions
that disappear under every outgoing map. It is enough to use covers:
longer incoming images and outgoing conditions factor through them. Their
dimensions are therefore

$$
t_v=\dim M_v-\operatorname{rank}[M_{u,v}]_{u\lessdot v},\qquad
s_v=\dim M_v-\operatorname{rank}\begin{bmatrix}M_{v,w}\end{bmatrix}_{v\lessdot w}.
$$

A copy of $k_I$ contributes one top dimension at each minimum of $I$ and one
socle dimension at each maximum. Thus the multiplicity is bounded by the
smallest corresponding $t_v$, $s_v$, and stalk dimension on $I$.
A zero bound bypasses both Hom computations. The endpoint restriction is the
degree zero criterion of
[Asashiba and Liu, Lemma 3.39](https://arxiv.org/pdf/2411.11594v6#page=37).
Their paper develops further criteria using resolutions; this search uses
the top and socle of the module itself.

For a complete search, enumerate nonempty **antichains**, sets of pairwise
incomparable vertices. Choose $A$ where the top is nonzero and $B$ where the
socle is nonzero. Every candidate interval has the form

$$
I=\uparrow A\cap\downarrow B.
$$

Here $\uparrow A$ consists of vertices above at least one member of $A$, and
$\downarrow B$ consists of vertices below at least one member of $B$. For an
interval, its minima and maxima recover exactly this intersection: convexity
fills every point between them.

Keep only connected sets with actual minima $A$, maxima $B$, and nonzero
stalks throughout. Such intersections are convex. The endpoint sets determine
the interval uniquely, and every interval summand passes these tests. This
proves completeness without enumerating every subset of the ambient base.
A constant module on a chain with 80 vertices has one endpoint pair. A broad
antichain can still have exponentially many endpoint subsets; explicit
antichain and endpoint pair budgets bound that work.

## Recover simultaneous maps only when requested

Select independent columns $J$ of $C$, then independent rows $K$ of $C[:,J]$.
The square minor $D=C[K,J]$ is invertible. The selected incoming maps form
$i:L^{\oplus r}\to M$; multiplying the selected outgoing maps by $D^{-1}$
gives $p:M\to L^{\oplus r}$ with $pi=1$.

Let $j:R\to M$ be the kernel inclusion of $p$. The complement projection is
the unique solution of

$$
jq=1-ip.
$$

The exact solver for a matrix with independent columns checks this equation
in the original coordinates; see [exact rational coordinates](qq_coordinates.md) for its rational route.
It gives $qj=1$, $pj=0$, $qi=0$, and $ip+jq=1$. These equations certify a
module splitting: $ip$ and $jq$ recover the two components of each vector, and
their sum returns that vector.

Different interval supports can have nonzero Hom spaces between them.
Computing separate inclusions into the original module and concatenating
them would not ensure that projection onto one piece annihilates the others.
To retain this compatibility, the witness route extracts
each interval from the current complement and composes its maps through all
previous complement maps. The final summand uses support order, with one block
per positive multiplicity. Its complement may still split into modules that
are not intervals.

When maps are not requested, the algorithm evaluates every candidate against
the original module and subtracts its dimension contribution. Krull–Schmidt uniqueness ensures
that the reported interval copies coexist as a direct summand. It avoids all
kernel modules and retained splitting maps. Both routes report identical
multiplicities and residual dimensions.

## Scope, validation and cost

Inputs are checked for path independence on their complete finite base.
A chosen family certifies multiplicities only for those intervals. A zero
residual already proves that the module is a sum of intervals; a nonzero residual proves
its failure only after the complete pruned search. Budget exhaustion raises
an error without returning a partial negative answer.

With $d=\sum_{v\in I}\dim M_v$, each Hom basis and the composition matrix has
at most $d^2$ logical entries. The bound includes potentially dense output
from sparse elimination. Path validation is bounded by the largest squared
stalk dimension. Matrices for the top and socle and the finite order table
have separate checks against the same entry limit before allocation. Witnesses also
check the sum of squared stalk dimensions before retaining simultaneous maps.
Each limit bounds entries in one workspace. Converting these bounds into a
peak memory estimate would also require accounting for simultaneous allocations
and coefficient sizes; growth of exact rational coefficients can dominate both
storage and arithmetic cost.

For an encoded input, the workflow uses the encoding session cache when
constructing the finite module. The top and socle dimensions are shared within
one decomposition call.
There is no persistent cache of multiplicities or mutable Hom results.
Treat source modules and retained maps as read-only during computation;
validation recomputes the multiplicities and checks all retained naturality,
splitting and reconstruction equations against the current source.

The owner is `IntervalDecompositions`, with task forwarding in `Workflow`.
The result's provenance identifies the finite category and exact coefficient
field. Pullback carries a supplied splitting along a classifier; completeness
in an ambient category is a separate mathematical question.


## Reading a split through its retained maps

A gallery starts from the same inclusion and projection used by the algebra.
For an interval result, the coordinates of the extracted part concatenate
interval blocks at each vertex. Selecting a block therefore selects columns
of its inclusion and the corresponding rows of its projection. The support
list determines where that block is present, while its multiplicity determines
how many coordinates it contributes there. No second decomposition is needed.

The `SummandCollection` adapter checks these maps before preparing a view. It
also accepts supplied general modules, including pieces with thicker stalks,
but requires the maps to commute with every cover, retract onto their pieces,
annihilate the other pieces, and reconstruct the identity. A selected set of blocks has a complement formed from the
omitted blocks and the original residual. Adding their stalk dimensions gives
the dimensions of the full module; the original map equations justify the
direct sum decomposition behind that equality. A supplied piece receives
no automatic indecomposability label.

The geometry uses a separate source of information. A classifier on the same
finite base assigns parameter regions to labels. The renderer pulls the
selected dimensions back along this assignment and merges adjacent pieces
with the same displayed value, preserving included and excluded faces and the
viewing window. Exact coordinates remain available even if distinct points
coincide in the floating drawing. Without a classifier the positions describe
the finite order. Supplied box unions have their own provenance and remain
geometrically unverified; a checked projection cannot certify those boxes.

Preparation retains the splitting, geometry and block statistics. Sorting and
filtering change the displayed IDs and dimension sums, and matrix inspection
selects components in the stored bases. Optional ordinary Hom tables reuse the
existing Hom solver, with a bound on the square of the number of unknowns
before each solve. The cache
is bounded by the last requested table and is pruned when a new table is
requested. Each selected basis element is a module morphism whose component
can be inspected at a finite label. The table records spaces of morphisms
between whole summands, so its rows and columns name summands rather than
vertices of the finite poset.

For $s$ displayed blocks and $n$ finite labels, forming selected dimensions
takes $O(sn)$ additions. Support layers are rebuilt from the retained cells
for the aggregate panels and displayed pieces; their cost also depends on
the geometric subdivision. The live renderer currently replaces the figure
after a committed selection. It reuses the mathematical preparation while
still incurring the cost of drawing the new figure. The drawing and Hom
budgets bound these two kinds of work separately.

A session builds a candidate snapshot before replacing its selected state,
so a failed request leaves the previous figure usable. Hover uses stored
readouts. Closing releases the algebra and geometric preparation, while a
frozen snapshot retains the selected matrices, boundaries and interpretation
for static export. The renderer uses the supplied algebraic result. Choosing
a decomposition algorithm or computing an approximation to a support happens
before that result reaches the renderer.

[Bibliography](references.md)
