# Numerical derived algebra

The algebra of a finite module depends on which vectors are independent, which
are sent to zero, and which represent the same class after taking a quotient.
With floating coefficients, these questions require a numerical rank decision.
This guide explains how tolerances affect derived computations on the retained
finite module and how to assess their results. The [category
guide](math_categories.md) specifies what its Hom, Ext, and Tor calculations
mean; the numerical choices here do not change that category.

A kernel consists of the vectors sent to zero; an image consists of the vectors
reached by a map. `RealField` computes numerical versions of these spaces, and
of coordinates in their quotients, using tolerances stored in the field. A
sufficiently small error in a matrix equation is treated as zero. Consequently
these computations depend on the scale of the entries and the chosen
tolerances; `QQField` and prime fields make the corresponding decisions
exactly.

For example, a diagonal matrix with entries $1$ and $10^{-14}$ is invertible
over the reals, but a computation that discards directions below $10^{-12}$
will retain only the first coordinate. Its numerical image then has dimension
one. This is a choice about the precision at which we distinguish directions,
and it propagates into any kernel or quotient built from that matrix.

```julia
import TamerOp as OP

field = OP.CoreModules.RealField(Float64; atol=1e-12, rtol=1e-10)
```

Use the same field, including its tolerances, throughout a derived computation.
Changing tolerances can change a numerical quotient and its coordinates.
Complexes, homology/cohomology data, and spectral subquotients retain this
field through construction, lazy representatives, shifts, cones, and induced
maps. Raw matrix constructors accept `field=...`; omitting it infers the
default field from the coefficient type. Summaries and provenance expose the
stored field so a custom tolerance remains inspectable.

For numerical cancellation, choose a positive absolute tolerance appropriate to
the units of the data. The default `RealField` has `atol=0`: a mathematically
zero product represented by tiny rounding residuals can then fail a purely
relative consistency check. Retaining a positive tolerance chosen by the caller
is essential; it does not justify silently loosening that tolerance.

Independent computations can choose different bases even when they represent
the same homology group. Compare them using a coordinate transport or a
mathematical quantity independent of the basis, rather than assuming their
matrices must be entrywise equal.

## Rank and solve decisions

The numerical rank cutoff for a coefficient matrix `A` is

```text
tau(A) = atol + rtol * opnorm(A, 1).
```

Here `opnorm(A, 1)` is the largest absolute column sum. The absolute tolerance
`atol` gives a fixed floor, while the relative tolerance `rtol` multiplies this
matrix scale. If the entries of `A` are all multiplied by a large constant, the
relative part of the cutoff grows with them. The fixed part matters when the
matrix itself is small. Entries and tolerances must be finite, and both
tolerances must be nonnegative; rescale the data if forming the cutoff or
factorizing the matrix would overflow.

For the diagonal matrix $A=\operatorname{diag}(1,10^{-14})$, the singular
values measure how much its two coordinate directions are stretched: they are
$1$ and $10^{-14}$. Compare three cutoffs while keeping the matrix fixed. This
example uses the singular value decomposition (SVD) rule, which retains singular values strictly greater than
$\tau$; the exact matrix remains invertible throughout.

```@raw html
<link rel="stylesheet" href="../assets/arithmetic/choices.css">
<figure class="arithmetic-example" id="cutoff-explorer" data-arithmetic-example="cutoff">
<div class="choice-control"><label for="cutoff-choice">Absolute cutoff τ</label>
<select id="cutoff-choice" aria-describedby="cutoff-explanation" disabled>
<option value="fine">τ = 10⁻¹⁶</option>
<option value="equal">τ = 10⁻¹⁴</option>
<option value="coarse" selected>τ = 10⁻¹²</option>
</select></div>
<div class="choice-drawing"><svg viewBox="0 0 250 230" role="img" aria-label="τ = 10⁻¹². The second direction lies below the cutoff. The numerical image keeps the first coordinate, while the second coordinate enters the numerical kernel. The underlying matrix is still invertible."><line x1="22" y1="167" x2="228" y2="167" class="axis"></line><line x1="22" y1="164" x2="22" y2="171" class="axis"></line><text x="22" y="191" text-anchor="middle" class="small">10⁻¹⁶</text><line x1="73.5" y1="164" x2="73.5" y2="171" class="axis"></line><text x="73.5" y="191" text-anchor="middle" class="small">10⁻¹²</text><line x1="125" y1="164" x2="125" y2="171" class="axis"></line><text x="125" y="191" text-anchor="middle" class="small">10⁻⁸</text><line x1="176.5" y1="164" x2="176.5" y2="171" class="axis"></line><text x="176.5" y="191" text-anchor="middle" class="small">10⁻⁴</text><line x1="228" y1="164" x2="228" y2="171" class="axis"></line><text x="228" y="191" text-anchor="middle" class="small">1</text><text x="125" y="218" text-anchor="middle" class="small">Singular value (logarithmic scale)</text><line x1="73.5" y1="40" x2="73.5" y2="163" class="cutoff"></line><text x="73.5" y="25" text-anchor="middle" class="">τ</text><circle cx="228" cy="65" r="5" class="retained"></circle><text x="216" y="70" text-anchor="end" class="">σ₁ = 1</text><circle cx="47.75" cy="118" r="5" class="omitted"></circle><text x="137.5" y="123" text-anchor="start" class="">σ₂ = 10⁻¹⁴</text></svg></div>
<dl class="choice-values">
<dt>Exact rank</dt><dd>2</dd>
<dt>Numerical image dimension</dt><dd data-value="rank">1</dd>
<dt>Numerical kernel dimension</dt><dd data-value="nullity">1</dd>
</dl>
<p class="choice-convention">Filled dots are retained; hollow dots are discarded. The dashed line marks τ. Here rtol = 0, so τ = atol.</p>
<figcaption id="cutoff-explanation" data-choice-explanation aria-live="polite">The second direction lies below the cutoff. The numerical image keeps the first coordinate, while the second coordinate enters the numerical kernel. The underlying matrix is still invertible.</figcaption>
<noscript><p>The displayed case remains available; enable JavaScript to change the selection.</p></noscript>
</figure>
<script src="../assets/arithmetic/choices.js"></script>
```

The linear algebra owner, `OP.FieldLinAlg`, offers several implementations
through the `backend` keyword:

| Operation | Explicit real backends |
| --- | --- |
| Rank and nullspace | `:float_dense_qr`, `:float_sparse_qr`, `:float_dense_svd` |
| Column space and solve with independent columns | `:float_dense_qr`, `:float_sparse_qr` |
| Reduced row echelon form | `:float_dense_rref`, `:float_sparse_rref` |

`backend=:auto` selects the implementation for the operation and matrix
storage. The table uses three standard abbreviations. Reduced row echelon form
(RREF) uses elimination, visiting columns from left to right and choosing row
pivots. QR factorization writes a matrix as an orthogonal factor times a
triangular factor and uses pivoting to select independent columns. Singular
value decomposition (SVD) measures the independent directions by nonnegative
singular values and compares them with the cutoff. A direction near that cutoff
can be accepted by one method and discarded by another, so comparing explicit
backends is useful when the rank decision appears sensitive.

Sparse QR receives the field cutoff during factorization. Its reported rank and
column permutation are used together when constructing the image and kernel.
Factoring with a different cutoff and then merely counting accepted diagonal
entries is invalid: the accepted columns need not form the prefix assumed by
the subsequent triangular solve.

Once a matrix `B` has been accepted as having independent columns, a solve asks
whether a supplied vector lies in its numerical image. For each supplied column
`y_j` and computed coordinate vector `x_j`, the solver checks

```text
norm(B*x_j - y_j) <= atol + rtol * (norm(B)*norm(x_j) + norm(y_j)).
```

The vector norms are Euclidean and the matrix norm is Frobenius. The left side
is the *residual*, the difference between the requested vector and the one
reconstructed from its coordinates. The right side scales that difference by
the sizes of the input and computed solution. This is a backward error check:
it measures how closely the computed coordinates satisfy the supplied equation,
without promising equally accurate coordinates when the matrix is nearly
singular. Each column must pass, so a large, accurately reconstructed column
cannot hide an incompatible smaller one. Scaling a compatible supplied vector
should not cause rejection merely because the coefficient matrix stayed small.
This residual criterion checks compatibility with the selected numerical image;
it does not restore a direction discarded by the rank decision. The explicit
`check_rhs=false` option bypasses this consistency check.

## Checking numerical results

Dimensions alone do not establish that a numerical derived computation has
preserved the expected maps. Check the relevant matrix identities too: for
example, two successive differentials should compose to zero, and a proposed
module morphism should commute with the structure maps. For an identity `X=Y`,
a comparison using tolerances can use

```text
norm(X-Y) <= atol + rtol * max(norm(X), norm(Y)).
```

Here `atol` and `rtol` are the tolerances chosen for the comparison. Inspect
the residual relative to `max(1, norm(X), norm(Y))` together with the condition
numbers of any changes of basis. The condition number compares largest and
smallest singular values and indicates how sensitive coordinates can be to
input perturbations. A zero singular value makes that ratio infinite; for a
differential with such values, inspect the remaining singular values and their
separation from the rank cutoff instead. A small residual describes that
computation, not numerical stability for arbitrary input scales.

Numerical `Hom` forms the equations requiring a proposed morphism to commute
with every structure map. These are its *naturality constraints*. Their
numerical nullspace describes the accepted solutions. The tolerance prevents
rounding residuals in dependent equations from being treated automatically as
new independent constraints. Tor multiplication requires explicit compatible
product data; numerical tolerance does not create a canonical product on
arbitrary additive Tor groups.

Cached solves require an unchanged coefficient matrix.
For cached sparse QR, a change to the field's effective rank cutoff triggers
refactorization. Use `cache=false` throughout workflows that reuse a matrix
object while changing its entries.

## Near-singular inputs

A singular value or elimination pivot close to `tau(A)` makes numerical rank
sensitive to perturbations, scaling and backend choice. Different operations
can then select different ranks, so the library cannot promise one coherent
numerical quotient across an entire derived computation. A downstream solve,
check of a chain map or quotient construction may reject incompatible numerical
decisions. An ambiguous rank is not mathematically exact, and computation does
not silently switch to rational algebra. When that distinction matters, inspect
the gap between singular values, compare backends or tolerances, and retain the
original rational input for an exact computation.

An approximate kernel vector must still satisfy its residual contract, and an
image basis must span the selected numerical image. Likewise, a solve checks
the supplied vectors, and a product on a quotient must be independent of the
chosen representatives. Inspect these properties alongside the numerical rank;
a dimension alone does not determine the resulting algebra.