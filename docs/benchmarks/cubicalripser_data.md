# Reading the CubicalRipser benchmark data

The [CubicalRipser comparison](cubicalripser.md) measures barcodes from images
and volumes. Its data contain all 48 requests, including the smaller sizes
behind the report's scaling plots. Each request fixes an array, a way to turn
its values into a growing cubical complex, and the direction in which those
values are traversed.

## Choose a file

Start with [results.csv](cubicalripser_v1/results.csv), a spreadsheet table
with one row per request. The JSON files preserve nested records, including
the repeated measurements behind each row and the intervals of each barcode.

| File | What you can learn from it |
| :--- | :--- |
| [results.csv](cubicalripser_v1/results.csv) | Array settings, output counts, times and speed ratios for each request. |
| [analysis.json](cubicalripser_v1/analysis.json) | The pass summaries under `records`, with combined results under `groups` and `balanced_ratio`. |
| [samples.json](cubicalripser_v1/samples.json) | Individual accepted measurements, including compilation and input-reset counters. |
| [formal_manifest.json](cubicalripser_v1/formal_manifest.json) | Array shapes, random seeds, construction rules and input fingerprints. |
| [verification.json](cubicalripser_v1/verification.json) and [barcodes.json](cubicalripser_v1/barcodes.json) | The barcode comparisons and the intervals that were compared. |

## Read a row

The row `2d_V_noise_size1` uses a 4096 × 4096 array of noise values. Its `V`
convention places array values at vertices; a square enters when all its
vertices have entered. With `order = sublevel`, increasing the threshold
admits vertices whose values are at most that threshold.

| Field | Value and meaning |
| :--- | :--- |
| `dimension`, `shape` | 2, 4096x4096: A two dimensional square array. |
| `elements` | 16777216: the number of scalar values in the array. |
| `tamerop_seconds` | 3.982081403: TamerOp's summary time, about 3.98 seconds. |
| `cubicalripser_seconds` | 4.906119814…: CubicalRipser's summary time, about 4.91 seconds. |
| `ratio` | 1.25997…: the paired measurements give TamerOp about 1.26 times CubicalRipser's speed on this request. |
| `intervals` | 4437562: the number of barcode intervals, counting repeated intervals separately. |

Ratios divide CubicalRipser time by TamerOp time, so values above 1 favor
TamerOp. The ratio summarizes paired measurements; it need not equal the
quotient of the two displayed summary times.

## Understand the timings

Times are in seconds. The timer starts from the supplied array and includes
building the cubical input, required conversions, negating values for a
superlevel request, and producing the complete result. Loading the input
file, checking its fingerprint and comparing barcodes happen outside the timer.

There are three *passes*, each using a fresh process for each tool and
request. After warmup, each process measures three fresh computations.
The middle of those times is its pass median; the middle of the three pass
medians is the displayed tool time. In `analysis.json`, each request's
`tools.tamerop.passes` and `tools.cubicalripser.passes` retain both the
individual `samples` and their median, `seconds`.

The reported ratio is the geometric mean of the three paired ratios:
multiply them and take the cube root. `ratio_min` and `ratio_max` in the CSV,
or `ratio_range` in the JSON, give the observed extremes across passes.
Each tool's `range_seconds` similarly gives the extremes of its pass medians.
These are observed ranges rather than confidence intervals.

## Identify and combine requests

| Field | Meaning |
| :--- | :--- |
| `case` in CSV, `id` in JSON | The request identifier shared by the measurement and input records. |
| `dimension`, `shape`, `elements` | The number of array axes, their lengths and the total number of scalar entries. |
| `convention` | `V` places values at vertices. `T` places them on the largest cells, such as squares or cubes; their faces enter with the earliest incident cell. |
| `pattern` | The rule producing the values: noise, binary or smooth data. |
| `order` | `sublevel` grows from smaller values upward; `superlevel` grows from larger values downward. |
| `reserved` | Whether the input was held back until the computation and measurement procedure had been fixed. |
| `verified` | Whether its complete barcode agreed between the programs. |
| `classification` in CSV, `similarity` in JSON | The practical comparison label, using a 10% margin around equal speed. |

The manifest supplies the random seed and exact generator for each request.
`analysis.json` groups requests by dimension, convention and pattern. The
overall `balanced_ratio` is the geometric mean of the 48 request ratios.
Each of the twelve groups has four requests, giving the groups equal weight.
The
[report](cubicalripser.md) explains how the two cubical conventions change
the mathematical input.

### Read a barcode

In `barcodes.json`, each interval record has four entries:

```text
[degree, birth, death, multiplicity]
```

The degree identifies the kind of hole: 0 for components, 1 for loops and 2
for enclosed voids. Birth and death are the parameter values where the class
appears and disappears. Multiplicity counts how many times that same interval
occurs, allowing repeated intervals to be stored together.

For example, the illustrative row `[1, 2, 5, 3]` means three degree 1
intervals born at 2 and dying at 5. A `null` death denotes an essential
interval, which continues indefinitely. Superlevel requests store grades for
the negated scalar function, so negate those grades to recover thresholds in
the original values.

## Read the memory and verification records

The per-pass records in `analysis.json` use bytes for sizes and memory:

| Field | Meaning |
| :--- | :--- |
| `allocation_bytes` | Memory requested during the call, including temporary objects; `null` for CubicalRipser, where this counter was not collected. |
| `input_bytes`, `result_bytes` | Storage measured for the input array and returned result. |
| `process_peak_rss_bytes`, `query_peak_rss_bytes` | Peak recorded resident memory, or physical RAM use, over the process and query observation periods respectively. |
| `import_seconds`, `warmup` | Package loading and warmup measurements, kept separate from the accepted query times. |
| `worker_wall_seconds` | Total elapsed time for the worker, including preparation and repeated computations. |

The [machine record](cubicalripser_v1/MACHINE.json) and
[build record](cubicalripser_v1/build.json) identify the computer and software.
[Qualification checks](cubicalripser_v1/qualification.json) describe independent
controls, including failures outside the timed requests;
[calibration.json](cubicalripser_v1/calibration.json) records the size trials
used to select feasible inputs. The
[fixed task specification](cubicalripser_v1/TASK_FREEZE.json),
[public-call inspection](cubicalripser_v1/PUBLIC_CALL_REVIEW.json),
[source fingerprints](cubicalripser_v1/candidate_hashes.json) and
[study binding](cubicalripser_v1/binding.json) connect those definitions to
the measured implementation.

The [checksum list](cubicalripser_v1/SHA256SUMS) identifies the archived files
by SHA-256 fingerprints. Follow
[Reproduce a benchmark report](../benchmark_reproduction.md) with the study
name `cubicalripser-v1` to verify those records, generate the arrays and
collect new measurements.
