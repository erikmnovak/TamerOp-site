# Ripser.py: Vietoris–Rips persistence

[Ripser.py](https://ripser.scikit-tda.org/en/latest/) brings Ripser's C++
persistence engine to Python. It accepts dense and sparse distance data,
can select a smaller set of representative points called landmarks, and
returns representative cochains, algebraic descriptions of the detected
classes. These capabilities let us compare choosing points, computing their
barcodes and retaining information about the classes those bars describe.
This report uses Ripser.py 0.6.15 and the measurements of 5 October 2026.

## Results

**TamerOp was 5.05× as fast on the supplied dense distances used during development.**
Across all six development families, the equally weighted geometric mean of
the query ratios was **1.32×**. Euclidean clouds and larger dense inputs favored
TamerOp; sparse inputs and small controls favored Ripser.py in their family
summaries. Landmark performance depended on how many points were selected.

The difference is substantial in elapsed time on the largest dense requests.
The 1,024-point circle took **7.01 s in TamerOp and 30.4 s in Ripser.py**;
the 512-point planar input took **2.15 s and 11.7 s**. These measurements cover
a complete query from each program's prepared input, after compilation, with
fresh mathematical work on every call.

```@raw html
<a href="presentation/ripser_ratios.svg"><picture>
<source media="(max-width: 600px)" srcset="presentation/ripser_ratios_narrow.svg">
<img src="presentation/ripser_ratios.svg" alt="Ratios for the six development families, showing which families favor TamerOp and which favor Ripser.py." loading="lazy" style="width:100%;max-width:780px;height:auto">
</picture></a>
```

Each marker is a geometric mean of Ripser.py time divided by TamerOp time.
A value of 2 means TamerOp took half as long; a value of 0.5 means Ripser.py
took half as long. The lines show the range across four rounds of measurements,
called passes in the data tables.
The 31 development requests were used during optimization; the six reserved
evaluation requests are reported separately below.

| Development family | Requests | Ripser.py / TamerOp time | Range across passes |
| :--- | ---: | ---: | ---: |
| Euclidean clouds | 4 | 3.16× | 2.50–3.80× |
| Supplied dense distances | 7 | 5.05× | 4.23–6.53× |
| Supplied sparse distances | 4 | 0.843× | 0.752–0.984× |
| Weighted vertices | 4 | 0.938× | 0.797–1.20× |
| Landmark selection | 8 | 1.34× | 1.08–1.72× |
| Small controls | 4 | 0.317× | 0.229–0.448× |

Each request has equal weight within its family, and each family has equal
weight in the 1.32× development aggregate. Its range across passes is
1.18–1.49×. The ranges describe the observed repetitions; they are not
confidence intervals.

### Actual runtimes and input sizes

The examples below cover all six development families, including the largest
dense requests, the largest grids, a landmark request favoring Ripser.py and
a small control in degree three. The [complete table](ripser_v1/summary.csv)
contains every request. For each input, we take the middle time from each
round of measurements, then the median of those four times. A degree
label H₂ includes H₀, H₁ and H₂; F₂, F₃ and F₁₀₁ denote arithmetic modulo
2, 3 and 101.

| Input | Points or vertices | Field / through | TamerOp (s) | Ripser.py (s) |
| :--- | ---: | :--- | ---: | ---: |
| Circle distances | 1,024 | F₂ / H₁ | 7.01 | 30.4 |
| Planar distances | 512 | F₁₀₁ / H₂ | 2.15 | 11.7 |
| Sphere point cloud | 128 | F₁₀₁ / H₂ | 0.156 | 0.530 |
| Sparse grid | 4,096 | F₂ / H₁ | 0.00266 | 0.00407 |
| Grid with weighted vertices | 4,096 | F₂ / H₁ | 0.00416 | 0.00415 |
| Landmark selection | 2,048 → 128 | F₂ / H₁ | 0.0139 | 0.00766 |
| 3-sphere control | 8 | F₂ / H₃ | 0.00145 | 0.000188 |

```@raw html
<a href="presentation/ripser_times.svg"><picture>
<source media="(max-width: 600px)" srcset="presentation/ripser_times_narrow.svg">
<img src="presentation/ripser_times.svg" alt="Query times for the same seven requests, with TamerOp and Ripser.py on a common logarithmic scale in seconds." loading="lazy" style="width:100%;max-width:780px;height:auto">
</picture></a>
```

The plot shows the same examples as the table. Keeping actual seconds beside
the ratios distinguishes a saving of several seconds from a difference of a
fraction of a millisecond. Ratios are averaged within paired process passes,
so dividing the displayed median times need not reproduce the reported ratio.

### Reserved evaluation requests

These inputs were reserved before optimization and measured with the same
frozen implementation. They retain the same mixed pattern: TamerOp is faster
on the circle, dense distances and grid, while Ripser.py is faster on the
weighted octahedra and the selected landmark request.

| Input | Points or vertices | Field / through | TamerOp (s) | Ripser.py (s) | Ripser.py / TamerOp |
| :--- | ---: | :--- | ---: | ---: | ---: |
| Jittered circle | 512 | F₂ / H₁ | 0.854 | 3.51 | 4.13× |
| Random planar distances | 128 | F₁₀₁ / H₂ | 0.0254 | 0.127 | 4.83× |
| Random sphere distances, with cocycles | 96 | F₃ / H₂ | 0.0497 | 0.186 | 3.81× |
| Permuted grid | 4,096 | F₂ / H₁ | 0.00419 | 0.00769 | 1.85× |
| Permuted octahedra with weighted vertices, with cocycles | 96 | F₁₀₁ / H₂ | 0.000747 | 0.000621 | 0.832× |
| Landmark selection | 2,048 → 128 | F₂ / H₁ | 0.0157 | 0.00790 | 0.546× |

## What the comparison computes

As a distance threshold increases, a Vietoris–Rips complex adds edges between
nearby points and fills every clique with its simplex. The barcode records
when homology classes appear and disappear. Both programs return every
positive-length interval through the requested degree, including classes
that remain at the end of the filtration and repeated intervals.

Some requests also retain **cocycles**, cochains representing cohomology
classes. Their coefficients can differ between programs while describing
valid classes. A landmark request selects a smaller set of points, computes
persistence on that set, and returns its distance table and coverage
information. Selection is part of the timed query.

The inputs include Euclidean point clouds, supplied dense and sparse distances,
and graphs whose vertices have assigned birth grades. An omitted sparse entry
means an absent edge; an explicitly stored zero remains an edge. The fields
and requested degrees are recorded for each case in the
[manifest](ripser_v1/manifest.json).

TamerOp computes these ordinary barcodes directly. A
[finite encoding](../finite_encodings.md) serves questions that require the
module's vector spaces and maps, particularly with several parameters. The
[original C++ Ripser report](ripser_cpp.md) compares larger barcode requests
through the upstream executable; its different inputs and timing boundary
make it a separate comparison.

## How the measurements were taken

The main timer starts with each program's input objects already built and
ends when the complete answer is ready. Building those objects is measured
separately; the downloads also give the sum of the construction and query
times. Generating and reading input files, checking answers and writing
results to disk happen outside both timers.

We ran four rounds of measurements, reversing the program and input order
between rounds. Each request receives a preliminary run followed by three
timed computations. The code is already compiled, and each computation
builds a new graph and calculates its answer afresh.

Cocycle requests include the time to construct the representatives. TamerOp
retains representatives in H₀ as well as higher degrees; Ripser.py returns
them only in higher degrees. For landmark requests, TamerOp keeps the distance
from every point to its nearest landmark, while Ripser.py returns the largest
of those distances, called the covering radius. We compare that radius after
timing.

### Matching the answers

The complete barcodes agree exactly on supplied distances, including repeated
intervals. For point clouds, each program calculates distances at its own
numerical precision, so the comparison allows for rounding. Very short bars
that disappear under rounding are recorded separately.

Independent checks reconstruct landmark choices and distances, compare small
barcodes with a separate calculation, and check that selected cocycles
represent nonzero classes. The [verification record](ripser_v1/verification.json)
specifies the checked outputs and rounding tolerance.

### Computer and versions

The study ran on [the benchmark computer](../benchmarking.md#the-benchmark-computer)
with one computation thread per program and one program running at a time.
Other work was running on the computer during this study; the plotted ranges
show the variation between rounds.

| Component | Recorded version or setting |
| :--- | :--- |
| TamerOp | Frozen source identified by [source hashes](ripser_v1/candidate_hashes.json) |
| Julia | 1.12.1 |
| Python | 3.12.3 |
| Ripser.py | 0.6.15, built from source with optimization enabled |

The [build record](ripser_v1/build_verified.json) gives the exact compiler
settings and dependencies.

## Reproduce the results

Follow [Reproduce a benchmark report](../benchmark_reproduction.md) to verify
the downloaded records and regenerate the common figures. The central files
for this study are:

| Record | Download |
| :--- | :--- |
| File and field descriptions | [Data dictionary](ripser_data.md) |
| Full summary and paired ratios | [summary.json](ripser_v1/summary.json) · [summary.csv](ripser_v1/summary.csv) |
| Accepted timing samples | [accepted_samples.json](ripser_v1/accepted_samples.json) |
| Mathematical checks | [verification.json](ripser_v1/verification.json) |
| Inputs and reserved evaluation | [manifest.json](ripser_v1/manifest.json) · [heldout_reservation.json](ripser_v1/heldout_reservation.json) |
| Software, harness and computer | [source hashes](ripser_v1/candidate_hashes.json) · [harness hashes](ripser_v1/harness_hashes.json) · [comparator build](ripser_v1/build_verified.json) · [Python dependencies](ripser_v1/python-freeze.txt) · [machine.json](ripser_v1/machine.json) |
| Integrity checks | [SHA256SUMS](ripser_v1/SHA256SUMS) |

The SHA-256 of `summary.json` is:

```text
cbf7b4abf1755eb08e137e8fa7d072c286512c1c1eddafc2f79e4d122cd08f63
```

The [benchmark project](https://github.com/erikmnovak/TamerOp-benchmarks/tree/cc389ab410d3d3e6df163a6af6bef48c9cf7b1f1/studies/ripser-py-v1)
provides the frozen source, measurement workers and deterministic input
generators. Preparation checks every generated input against its original hash;
new timings are saved separately from the published evidence. The reproduction
guide covers checking these records, rebuilding the figures and running the
computations on your own machine.
