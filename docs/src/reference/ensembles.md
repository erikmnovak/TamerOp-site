# Ensembles of persistence results

An ensemble collects repeated measurements of the same scalar quantity at the
same queries. Each repeat is a *replicate*, and each query location is a *probe*.
`persistence_ensemble` stores this aligned table and its context;
`summarize_ensemble` computes descriptive summaries or bands for a population
mean under a declared sampling model. The [guide](../../tutorials/uncertainty.ipynb)
works through small examples, while the
[implementation account](../../implementation/ensembles.md) explains the
reductions and statistical assumptions.

## Inputs and alignment

```julia
import TamerOp as OP

e = OP.persistence_ensemble([0. 2.; 2. 4.]; axes=([0.,3.],),
    sample_ids=["a","b"], statistic="Dimension at a fixed parameter",
    protocol="Two supplied computations", population="These examples")
s = OP.summarize_ensemble(e)
OP.ensemble_values(s)
```

In this example the rows are `(0,2)` and `(2,4)`, evaluated at parameters 0
and 3. The mean is therefore `(1,3)`, with two observations at each probe.

Supplied array dimensions are `(replicates, length.(axes)...)`: the first
dimension indexes observations and the others index query coordinates. Axes must be
finite and strictly increasing, including after conversion for drawing.
IDs are distinct strings. Values may be finite real numbers or `missing`;
`NaN`, infinity and Boolean values are rejected. The caller must align the observations before construction. The constructor
does not interpolate, normalize or fill missing values. Original values are
retained; statistical outputs are `Float64`.

The overload for ordinary diagrams requires `grid`, `sample_ids`, `protocol` and
`population`. Choose `statistic=:landscape` (default, positive integer `layer`) or
`:betti`, with `dim=0` by default. Sublevel counts use `[birth,death)`;
superlevel counts use `(death,birth]` at original coordinates. Diagrams must
share a coefficient field and filtration order. `essential=:error` rejects essential intervals;
`:drop` explicitly omits them; `:include` is available for Betti counts only.

A vector of compatible `ScalarField` objects may instead provide a common
Cartesian domain. Select `layer` by identity or index. Axis coordinates, labels,
units and ordered layer identities must agree; the coefficient field, degree and normalization remain
caller declarations. A `NaN` used to mask a scalar field becomes a `missing` ensemble entry.
Treating a sampled field as a table does not establish that it is a
multiparameter landscape or that a theorem about such landscapes applies.

## Summaries and statistical meaning

| Option/result | Meaning |
| --- | --- |
| `band=:quantile`, `quantiles=(0.1,0.9)` | Linear empirical quantiles of available replicates; descriptive. |
| `band=:range` | Observed extrema; descriptive. |
| `threshold=0` | `frequency` counts values strictly greater than the threshold. |
| `mean`, `median`, `std`, `counts` | Mean, median, sample standard deviation and number of available observations at each probe. |
| `band=:hoeffding`, `bounds=(lo,hi)` | Population mean intervals under independent, identically distributed (IID) rows and known bounds that hold with probability one. Bounds may be scalars or arrays with the probe grid shape. |
| `band=:bootstrap` | Approximate mean bands from resampling entire rows, without dividing by an estimated standard error. There is no finite sample coverage guarantee. |
| `scope=:simultaneous` | The requested coverage concerns all supplied probe means together; default for inference. |
| `scope=:pointwise` | The requested mean coverage applies separately at each probe. |
| `level=0.95` | Requested inference level; unrelated to empirical quantile spread. |
| `bootstrap_samples=1000`, `seed=0` | Row resampling with a private pseudorandom generator and recorded seed; at least 100 resamples. |

For either inference mode, set `sampling=:iid`, provide at least two complete
rows, and use probes fixed independently of the observations. Independence
concerns the rows; values at different probes within a row may depend on one
another. The declaration records the sampling assumption, which the numerical
table alone cannot establish. The Hoeffding mode checks the observed values
against `bounds`, but those bounds must also be justified for unseen values.
Both inference modes concern only the supplied probes.

Descriptive summaries permit missing entries and retain a separate observation
count at each probe. A probe with no observations has `NaN` summaries; sample
standard deviation requires at least two. Omitting missing values is a
description of available observations and need not give an unbiased estimate
of a population quantity.

`ensemble_values(s)` returns copied arrays with the probe grid shape.
`ensemble_summary(e)`/`ensemble_summary(s)` and `describe` give the retained
context and statistical assumptions and the domain of the coverage statement. `Featurizers.sample_ids(e)` and
`Featurizers.feature_values(e)` return copies; `feature_axes(e)` returns the
original coordinate vectors. Treat object storage as read-only.
`check_ensemble(x; throw=false)` validates retained shape and value requirements and
returns `Advanced.EnsembleValidationSummary`, with `valid` and `issues` fields.
Use `throw=true` to raise on malformed storage. Validation cannot establish
sampling independence or the provenance of supplied observations.

Budgets reject without truncation: `max_cells=1_000_000` at construction,
`max_work=10_000_000` for diagram interval/probe evaluation, and
`max_work=50_000_000` for summary/bootstrap arithmetic.

## Figures and linked selection

`visualize(s)` uses prepared values; it never resamples. Figures support one or
two coordinate axes. For higher-dimensional input, supply an explicitly selected
section before visualization. `sample` accepts an ID or an index starting at 1;
`probe` is a Cartesian linear index starting at 1, with the first coordinate
changing fastest. On a grid of two x coordinates and three y coordinates,
probe 2 is the second x coordinate at the first y coordinate.
`view` is one of `:mean`, `:lower`, `:upper`, `:std`, `:frequency`, `:counts`.
The default mean curve includes its band. `diagram_samples=(1,2)` requests up
to twelve panels showing retained ordinary diagrams. `max_cells=100_000` bounds the
supplied observation table used by a figure.

`samples` optionally contains one named tuple per replicate, with prepared static
`source` and/or `invariant` specifications and optional `metadata`. The selected
replicate displays those panels. The caller supplies their association with the observations. Moving the
pointer over a figure reads prepared data; it does not compute distances or
invoke a user callback.

```julia
session = OP.inspection_session(s)
OP.Advanced.select_inspection!(session; sample="b", probe=2)
snapshot = OP.Advanced.inspection_snapshot(session)
OP.Advanced.close_inspection!(session)
```

Live WGLMakie controls require Julia and permit replicate, probe and view changes.
Invalid selections preserve the previous state. Each linked viewer
releases its own listeners when it closes; closing the session releases its inputs and leaves
a static snapshot. Static CairoMakie exports and WGLMakie HTML scenes do not provide live
statistical recomputation. See the [display choices](../../visualization.md#choose-a-display)
for choosing between figures, prepared selections and live controls.

For a finite set of choices, `save_visual_session` can store named snapshots
whose figures remain selectable in a browser after Julia closes. The
[guide](../../tutorials/uncertainty.ipynb) uses this to compare prepared
replicate and threshold views. Such selection reads saved answers; a new
threshold, probe or sampling calculation must first be prepared in Julia.

Statistical arithmetic is numerical. Known bounds are converted outward to
Float64, with their original declarations retained; an outward endpoint adjustment
prevents a positive interval from disappearing through display rounding.
The statistical reductions themselves still use floating point arithmetic.
