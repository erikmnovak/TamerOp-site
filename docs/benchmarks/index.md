# Benchmark results

These comparisons measure the computations behind TamerOp's algebra,
barcodes and interactive views. Each report follows the same path: the main
result, a graph showing where it holds, actual runtimes, and then the
mathematical and experimental details. The comparison programs specialize in
different parts of this work, so the reports are organized by the question
being answered.

## Results at a glance

| Comparison | Main result |
| :--- | :--- |
| [QPA: finite module algebra](qpa.md) | **TamerOp was 135.7× as fast** in the weighted aggregate of 200 completed comparisons, including construction and the complete query. The remaining 20 tensor requests did not complete in QPA and have no speed ratio. |
| [PHAT: ordinary persistence](phat.md) | **TamerOp took about 25% less time**, a 1.33× ratio across four equally weighted input families. Graphs showed a 2.03× advantage; the algebraic controls had similar aggregate performance. |
| [Ripser.py: Vietoris–Rips persistence](ripser.md) | **TamerOp was 1.32× as fast** across the six equally weighted development families. Supplied dense distances showed a 5.05× advantage; sparse distances and small controls favored Ripser.py. |
| [C++ Ripser: ordinary Rips barcodes](ripser_cpp.md) | **TamerOp was about 1.8× as fast on the circle inputs.** C++ Ripser was 1.61–1.77× as fast on the sparse spheres; most planar results were closer. |
| [CubicalRipser: cubical barcodes](cubicalripser.md) | **TamerOp was 2.18× as fast** in the balanced aggregate. The largest noisy 3D vertex volume took 4.57 seconds versus 15.7 seconds. Binary vertex volumes favored CubicalRipser. |
| [Browser interaction with a Julia viewer](visual_interaction.md) | **Median response was 274 ms for the small ring**, 4.97 seconds for the larger image and 582 ms for the two-square slice query. The report separates typical response from longer delays. |

A ratio of 2 means TamerOp took half as long. Ratios summarize the specified
inputs and timing boundary; the report graphs show how the result varies
across tasks. Absolute times then give that difference a practical scale.
The browser study measures response time within TamerOp rather than a
comparison with another library.

## Choose the computation

[QPA](qpa.md) concerns the algebra of finite modules: maps, kernels,
resolutions and derived operations. It begins after the finite category and
scalar inputs are prepared, measuring native construction and the complete
requested algebraic answer.

[PHAT](phat.md) takes supplied filtered boundary matrices, while
[Ripser.py](ripser.md) and [C++ Ripser](ripser_cpp.md) compute persistence from
points or distances. [CubicalRipser](cubicalripser.md) works directly with
image and volume arrays. These starting objects explain why the barcode
comparisons have separate reports, even when their final answers are all
collections of intervals.

The [interaction report](visual_interaction.md) follows a different part of
the workflow: a reader changes a browser control, Julia computes the
corresponding answer, and the figure updates. Its measurements include the
time needed to deliver and display that result.

## Computer and reproducibility

The studies use the same Intel Core i7-1365U workstation with 32 GB of
installed memory. The [measurement account](../benchmarking.md) gives the
shared specifications, explains the ratios and timing boundaries, and links
the exact machine records. Each report records its own software versions
and resource settings.

Follow [Reproduce a benchmark report](../benchmark_reproduction.md) to check
the downloaded JSON against its SHA-256 fingerprint, redraw the figures or
run the computation yourself.
