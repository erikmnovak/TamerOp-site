# Reading the QPA benchmark data

The [QPA comparison](qpa.md) measures computations with modules described by
finite diagrams of vector spaces and linear maps. Its data let us follow a
reported result back
to a particular input, see how its time varied between runs, and check which
answers were successfully compared. This page explains how to read those
records for the study completed on 3 October 2026.

## Choose a file

Start with [timings.csv](qpa_v1/timings.csv), a table you can open in a
spreadsheet. Each row describes one request and one timed stage. There are
220 requests, with three stages recorded for each. The JSON files preserve
the more detailed records, including measurements nested under each program's
name.

| File | What you can learn from it |
| :--- | :--- |
| [timings.csv](qpa_v1/timings.csv) | The input, stage, time and speed ratio for each row. |
| [observations.json](qpa_v1/observations.json) | The five run summaries behind each row, together with answer checks and memory counters. |
| [results.json](qpa_v1/results.json) | The combined results by mathematical area, workflow, coefficient field and timed stage. |
| [provenance.json](qpa_v1/provenance.json) | The computer, software versions and source fingerprints that identify the study. |

## Read a row

Find `Q1:hom_basis:cube3_presentation_r1_QQ_s11` with
`phase = construction_and_query`. This request finds a basis for the linear
maps between two modules that respect their structure maps. The basis
describes all such maps by linear combinations. Here the coefficients are
rational numbers. The
[report's workflow table](qpa.md) explains the other requested operations.

| Field | Value and meaning |
| :--- | :--- |
| `poset_vertices` | 8: the finite partially ordered set has eight vertices, where the module's vector spaces are placed. |
| `input_stalk_sum` | 25: Adding the dimensions of the supplied vector spaces gives 25, counting each input module once. A *stalk* here means the vector space at one vertex. |
| `TamerOp_seconds` | 0.000461408: the summary time for TamerOp, about 0.461 milliseconds. |
| `QPA_seconds` | 0.000825484: the summary time for QPA, about 0.825 milliseconds. |
| `ratio` | 1.75901…: the comparison of paired runs gives TamerOp about 1.76 times QPA's speed on this request. |

The ratio always divides QPA time by TamerOp time, so a value above 1 favors
TamerOp. The two displayed times and the ratio summarize the repeated runs
separately; dividing those displayed times need not recover `ratio`.

## Understand the timings

The `phase` field tells us where the timer starts and ends:

| Phase | Work inside the timer |
| :--- | :--- |
| `native_construction` | Turn the prepared input into each program's own mathematical objects. |
| `complete_query` | Starting with those objects, compute the complete requested answer. |
| `construction_and_query` | Construct the objects and compute the answer in one uninterrupted measurement. This is the report's main comparison. |

A *pass* is one round of measurements in separately launched processes. Each
of the five passes summarizes three computations with independently reset
inputs. Its median is the middle of the three times; the displayed tool time
is then the middle of the five pass medians. In `observations.json`, these
values appear under `TamerOp` and `QPA` as `pass_medians_seconds`,
`sample_counts` and `median_seconds`.

For each pass we divide QPA's median by TamerOp's median. The reported ratio
is their geometric mean: multiply the five ratios and take the fifth root.
This averages multiplicative differences while keeping the runs paired.
`pass_ratios` retains all five ratios, and `pass_range` gives their smallest
and largest values.

`interval95`, or `ci_low` and `ci_high` in the CSV, gives an approximate 95%
confidence interval for the ratio, estimated from variation between passes.
It is calculated on logarithms of the five ratios using Student's t
distribution with four degrees of freedom. Unlike `pass_range`, it estimates
uncertainty in the comparison rather than listing the observed extremes.
The [measurement account](../benchmarking.md) explains how these summaries
are used in the reports.

## Identify and combine requests

| Field | Meaning |
| :--- | :--- |
| `case` | The request identifier, shared by its three timed stages. |
| `workflow`, `variant` | The operation, labeled Q1–Q10 in the report, and its particular form. The example above uses `Q1` and `hom_basis` to request a basis of maps. |
| `area` | One of the five mathematical groups used to balance the overall comparison. |
| `field` | `QQ` means rational coefficients; `F2`, `F3` and `F101` mean arithmetic modulo the indicated prime. |
| `split` | Whether the input belonged to development or to the evaluation set reserved until the implementation was fixed. |
| `coefficient_max_bits` | The largest number of binary digits needed for a numerator or denominator in the supplied structure matrices. This describes the input coefficients. |
| `weight` | This request's share of the original suite, written as an exact fraction. |

Choose one phase before combining rows, since the same request's weight
appears three times. For an aggregate, keep requests with completed, matched
answers and rescale their weights to sum to 1. The main comparison uses 200
requests, whose original weights sum to 9/10.

The other 20 requests ask for tensor computations whose QPA query did not
complete. Their missing measurements appear as JSON `null` or empty CSV
fields. A construction time may still be present because the input was built
successfully. Use `mathematically_matched` and each tool's `verified` flag in
`observations.json` to distinguish this partial work from a completed answer.
The reported phase aggregates all use the same 200 matched requests.

`classification` applies the study's practical margin to the ratio: `win`
above 1.10, `loss` below 1/1.10, and `near_tie` between those bounds. These
labels describe the size of the measured difference. Read the interval and
individual passes alongside them to see its uncertainty and variation.

## Read the memory and verification records

The CSV fields `TamerOp_allocated_bytes` and `QPA_allocated_bytes` count
bytes requested during a computation, including
temporary objects that may already have been freed. Julia's counter excludes
allocations inside the FLINT dependency. `median_gc_seconds` records time
spent reclaiming unused objects, called garbage collection.
`exported_answer_json_bytes` is the size of the written answer file.

The summary's `peak_process_rss_mib` describes resident memory: memory held
in physical RAM by the whole running program. Its unit is MiB, or 2²⁰ bytes.
The other size counters use bytes. A process's memory, its accumulated
allocations and the size of its exported answer describe different parts of
the computation.

The [checksum list](qpa_v1/SHA256SUMS) gives SHA-256 fingerprints, which
identify the exact archived files. To verify those files and rerun the study,
follow [Reproduce a benchmark report](../benchmark_reproduction.md) with
the study name `qpa-v1`. The five pass medians in each observation also let
you reconstruct the reported ratios and intervals without collecting new
timings.
