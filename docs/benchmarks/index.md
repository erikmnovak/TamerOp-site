# Benchmark results

These studies compare TamerOp's algebra and barcode computations with
specialized libraries, and measure how long its live viewers take to update.

## Results at a glance

| Comparison | Main result | What it computes |
| :--- | :--- | :--- |
| [QPA: finite module algebra](qpa.md) | **TamerOp was 135.7× as fast** across 200 completed comparisons. QPA failed on 20 tensor requests. | Maps, kernels, resolutions and related algebraic operations on finite modules. |
| [PHAT: ordinary persistence](phat.md) | **TamerOp took about 25% less time overall**, with similar times on the algebraic controls. | Barcodes from supplied boundary matrices, which describe the cells and how their boundaries fit together. |
| [Ripser.py: Vietoris–Rips persistence](ripser.md) | **TamerOp was 1.32× as fast overall** on the development inputs. Sparse inputs and small controls favored Ripser.py. | Barcodes from points or distances, with requests that also select representative points or describe the detected classes. |
| [C++ Ripser: ordinary Rips barcodes](ripser_cpp.md) | **TamerOp was about 1.8× as fast on circles.** C++ Ripser was faster on sparse spheres. | Barcodes from supplied distance files, using larger point sets. |
| [CubicalRipser: cubical barcodes](cubicalripser.md) | **TamerOp was 2.18× as fast overall.** Binary volumes with values assigned to vertices favored CubicalRipser. | Barcodes from images and volumes, with values assigned to vertices or to pixels and voxels. |
| [Continuous inspection: time from input to picture](visual_interaction.md) | **Median updates took 0.274 s** for the ring, **4.97 s** for the image and **0.582 s** for a line restriction. | The wait from changing a browser control to seeing the figure update after Julia's computation. |

Here, 2× as fast means TamerOp took half as long. Each report shows the
variation across inputs and the actual waiting times.

## Computer and reproducibility

The studies use the same Intel Core i7-1365U workstation with 32 GB of
installed memory. [How the benchmarks were measured](../benchmarking.md)
explains what was timed and how the comparisons were made, with the full
computer specifications in one place.

Follow [Reproduce a benchmark report](../benchmark_reproduction.md) to check
the downloaded JSON against its SHA-256 fingerprint, redraw the figures or
run the computation yourself.
