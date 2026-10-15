# Reading the PHAT benchmark data

The [PHAT comparison](phat.md) starts with a filtered boundary matrix, which
records the cells of a growing complex and their boundaries, and computes its
barcode. The data cover 48 inputs in four families: graphs, simplicial
complexes, cubical complexes and algebraically constructed chain complexes.
Each input has separate measurements for construction, the barcode query and
the complete computation.

## Choose a file

Start with [timings.csv](phat_v2/timings.csv), which opens as a spreadsheet
table. Its 144 rows are the 48 inputs measured in three stages. The JSON
records keep the individual run summaries and experimental details behind
that table.

| File | What you can learn from it |
| :--- | :--- |
| [timings.csv](phat_v2/timings.csv) | Input sizes, times and speed ratios for each input and stage. |
| [observations.json](phat_v2/observations.json) | The five run summaries behind each row, including memory counters and mathematical checks. |
| [results.json](phat_v2/results.json) | Results combined by family and stage, together with the timing protocol and resource observations. |
| [provenance.json](phat_v2/provenance.json) | The computer, software versions and fingerprints of the source and input files. |

## Read a row

Find `case = graph_s1_v1` and `phase = combined`. This is the first size of
the first graph variant. Its input has 8,191 cells, and its barcode contains
2,817 intervals. The row describes these quantities as follows:

| Field | Value and meaning |
| :--- | :--- |
| `cells` | 8191: the number of input cells, including both vertices and edges. |
| `nonzeros` | 8190: the number of nonzero entries in the boundary matrix. |
| `bars` | 2817: the number of intervals in the resulting barcode. |
| `tamerop_seconds` | 0.000455998: TamerOp's summary time, about 0.456 milliseconds. |
| `phat_seconds` | 0.000672263: PHAT's summary time, about 0.672 milliseconds. |
| `phat_over_tamerop` | 1.34877…: the paired measurements give TamerOp about 1.35 times PHAT's speed on this request. |

The ratio divides PHAT time by TamerOp time. A ratio above 1 favors TamerOp;
a ratio below 1 favors PHAT. It summarizes the paired runs, so it need not
equal the quotient of the two displayed summary times.

## Understand the timings

| `phase` | Work inside the timer |
| :--- | :--- |
| `construction` | Convert decoded boundary data into each program's own input objects. |
| `query` | Compute the complete barcode from those objects and materialize its sorted intervals. |
| `combined` | Construct the input and compute the answer in one uninterrupted measurement. This is the report's main comparison. |

All times are in seconds. Input generation, parsing, package loading,
compilation and answer verification happen outside these timers.

A *pass* is one round of measurements in separately launched processes.
Each of the five passes begins with two warmups and then measures three fresh
computations. The middle of those three times is the pass median; the middle
of the five pass medians is the displayed tool time. In `observations.json`,
`tools.tamerop` and `tools.phat` retain the summaries for each pass, with
`pass_id`, `seconds` and `sample_count` identifying the round, its median
time and its number of accepted measurements.

The ratio is the geometric mean of the five paired PHAT/TamerOp ratios:
multiply them and take the fifth root. `pass_ratios` preserves those five
values. The CSV's `pass_min` and `pass_max` give their observed extremes;
the same pair appears as `uncertainty.pass_range` in the JSON.

`ci_low` and `ci_high`, or `uncertainty.ci95`, give an approximate 95%
confidence interval estimated from variation between passes. The calculation
uses logarithms of the paired ratios and Student's t distribution with four
degrees of freedom. Family and overall intervals first combine measurements
within each pass, preserving the pairing. The
[measurement account](../benchmarking.md) explains the statistical procedure.

## Identify and combine requests

| Field | Meaning |
| :--- | :--- |
| `case`, `family` | The individual input and its mathematical family. |
| `field` | `F2` means arithmetic modulo 2, the coefficient field used throughout this comparison. |
| `variant` | Which of the four constructions within a family produced the input. |
| `size_level` | Its position among that variant's three sizes. |
| `parameter` | The generator setting used to create that size. Its meaning depends on the variant. |
| `fixture_sha256` | A fingerprint identifying the exact input file. |
| `mathematical_check` | The independent calculation used to check the answer, such as graph component and cycle counts. |

For example, `size_level = 1` means the smallest tested size of that variant;
it does not mean a one dimensional complex. The report describes the
constructions so that the generator parameter can be read in context.

The overall comparison gives equal weight to each family, each variant within
a family and each size within a variant. Choose one phase when combining rows
so each request enters once. The `classification` field uses `win` above
1.10, `loss` below 1/1.10, and `near_tie` between them. These labels apply to
the estimated ratio; the interval and individual passes show how much that
estimate varies.

## Read the memory and verification records

Memory and allocation quantities use bytes. They answer different questions:

| Field or record | Meaning |
| :--- | :--- |
| `tamerop_allocation_bytes`, per-pass `allocation_bytes` | Memory requested during the timed call, including temporary objects. |
| `retained_input_bytes`, `retained_answer_bytes` | Sizes measured from the input and answer objects separately after construction. |
| `gc_seconds` | Time spent reclaiming unused objects through garbage collection. |
| Worker `sampled_peak_worker_rss_bytes` in `results.json` | The largest observed amount of physical RAM held by a running process, including runtime and untimed work. Sampling can miss a brief peak. |

PHAT's allocation and retained-object counters are `null` because those
quantities were not measured. They do not represent zero memory use.
The mathematical checks and completed-answer records describe the output
separately from these resource measurements.

The [checksum list](phat_v2/SHA256SUMS) gives SHA-256 fingerprints identifying
the archived files. Follow
[Reproduce a benchmark report](../benchmark_reproduction.md) with the study
name `phat-v2` to verify the files, prepare the same inputs and collect new
measurements. The retained pass summaries are sufficient to reconstruct the
published ratios and figures.
