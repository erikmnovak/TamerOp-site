# Reading the C++ Ripser benchmark data

The [C++ Ripser comparison](ripser_cpp.md) follows a request from a distance
file to its complete barcode. Its data contain ten requests, together with
their repeated timings and answer checks. Each row lets us see both how long
the request took and how much that comparison varied between runs.

## Choose a file

Start with [summary.csv](ripser_cpp_v1/summary.csv), a table with one row per
request that you can open in a spreadsheet. The JSON files preserve the
measurements and input definitions behind it.

| File | What you can learn from it |
| :--- | :--- |
| [summary.csv](ripser_cpp_v1/summary.csv) | Each input's size, times, speed ratio and memory measurements. |
| [summary.json](ripser_cpp_v1/summary.json) | The same results with pass times, input filenames and interval counts by degree. |
| [observations.json](ripser_cpp_v1/observations.json) | Individual observations, including warmups and measurements rejected because they included compilation. |
| [manifest.json](ripser_cpp_v1/manifest.json) and [fixtures.json](ripser_cpp_v1/fixtures.json) | The fixed request settings, timing protocol and input constructions. |
| [verification.json](ripser_cpp_v1/verification.json) | The comparison of complete barcodes. |

## Read a row

The row `circle_1280_f2` uses distances between 1,280 points on a circle.
It computes homology through degree 1 with coefficients modulo 2: connected
components in degree 0 and loops in degree 1.

| Field | Value and meaning |
| :--- | :--- |
| `n`, `edges` | 1280, 818560: the number of vertices and supplied edges. |
| `tamerop_seconds` | 15.527778…: TamerOp's summary time for the full request. |
| `cpp_seconds` | 28.592399…: C++ Ripser's summary time for the full request. |
| `ratio` | 1.83084…: the paired runs give TamerOp about 1.83 times C++ Ripser's speed on this request. |
| `ratio_min`, `ratio_max` | 1.72793…, 1.92879…: the smallest and largest paired ratios observed across the three passes. |
| `intervals` | 1281: the barcode contains 1,280 degree 0 intervals and one degree 1 interval. |

Ratios divide C++ Ripser time by TamerOp time. Values above 1 favor TamerOp;
values below 1 favor C++ Ripser. The displayed ratio summarizes the paired
runs, so it need not equal the quotient of the two displayed times.

## Understand the timings

All times are in seconds. The main timer includes reading the distance file,
building the program's own input objects, computing the barcode and emitting
the full answer. C++ Ripser launches a new executable for each call, so its
launch time is included. TamerOp runs in an already loaded Julia process with
compiled methods.

The study uses three *passes*, or rounds of measurements. Each case starts
a fresh Julia process in each pass. A discarded warmup precedes two accepted
samples per tool; their median is the average of the two times. The displayed
tool time is the middle of its three pass medians. The JSON fields
`tamerop_pass_seconds` and `cpp_pass_seconds` retain those medians.

The reported ratio is the geometric mean of the three paired C++/TamerOp
ratios: multiply them and take the cube root. `ratio_min` and `ratio_max`
are the observed extremes, rather than confidence intervals.
`construction_seconds` and `query_seconds` describe parts of TamerOp's main
timer. Their separate summaries need not add to its total, which also includes
file reading and answer output.

## Identify the request and its answer

| Field | Meaning |
| :--- | :--- |
| `id`, `family` | The request identifier and its input family. |
| `n`, `prime`, `degree` | The vertex count, coefficient prime and highest requested homology degree. |
| `format` | In JSON, how distances are stored, such as a lower triangular distance table. |
| `threshold` | In JSON, the distance cutoff; `null` means no finite cutoff was supplied for that request. |
| `input`, `sha256` | In JSON, the input filename and the SHA-256 fingerprint identifying its bytes. |
| `interval_counts` | In JSON, interval counts in degree order, beginning with degree 0. Their sum is `intervals`. |

The barcode checks compare births, deaths and repeated intervals by degree.
[Small control examples](ripser_cpp_v1/control_verification.json) additionally
compare against an independent boundary-matrix calculation.
The [sparse-cutoff record](ripser_cpp_v1/sparse_threshold_limitation.json)
and its [four-vertex input](ripser_cpp_v1/sparse_threshold_control.txt)
describe a separate input on which C++ Ripser's behavior disagreed with the
intended finite-cutoff answer. That control is excluded from the timing table.

## Read the memory and verification records

All memory fields use bytes:

| Field | Meaning |
| :--- | :--- |
| `allocation_bytes` | Memory requested during TamerOp's measured call, including temporary objects. |
| `retained_result_bytes` | The size of TamerOp's returned barcode object. |
| `tamerop_peak_rss_bytes` | The largest recorded resident memory, or physical RAM use, for the case's Julia process. This includes loading, compilation, warmup and repeated samples of that case. |
| `cpp_peak_rss_bytes` | The peak observed by sampling C++ invocations separately. |

These process peaks include more than the returned barcode, and the two
programs' process lifetimes differ. The
[machine and build record](ripser_cpp_v1/machine_and_build.json) supplies the
software and memory settings. The
[configuration record](ripser_cpp_v1/runtime_configuration_revision.json)
explains the changes that preceded the reported runs;
[default-heap observations](ripser_cpp_v1/initial_default_heap_observations.json)
and [shared-session observations](ripser_cpp_v1/shared_heap_hint_observations.json)
retain those excluded attempts. The
[recovery record](ripser_cpp_v1/execution_recovery.json) identifies resumed work.

[Source fingerprints](ripser_cpp_v1/candidate_hashes.json),
[measurement-script fingerprints](ripser_cpp_v1/harness_hashes.json) and the
[checksum list](ripser_cpp_v1/SHA256SUMS) identify the exact code and archived
files. Follow [Reproduce a benchmark report](../benchmark_reproduction.md)
with the study name `ripser-cpp-v1` to check them, regenerate the distance
files and collect new measurements.
