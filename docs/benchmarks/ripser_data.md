# Reading the Ripser.py benchmark data

The [Ripser.py comparison](ripser.md) measures persistence computations from
point clouds and supplied distances. Some requests ask for a barcode alone;
others retain algebraic representatives of the detected classes, called
cocycles, or select landmark points to represent a larger dataset. The data
identify these different
requests so that we can interpret a timing together with the answer it produces.

## Choose a file

Start with [summary.csv](ripser_v1/summary.csv), a spreadsheet table with one
row per request. It contains 31 development requests and six reserved
evaluation requests. [summary.json](ripser_v1/summary.json) adds the run
summaries behind each row and the combined results.

| File | What you can learn from it |
| :--- | :--- |
| [summary.csv](ripser_v1/summary.csv) | Each request's input settings, times, ratios and output sizes. |
| [summary.json](ripser_v1/summary.json) | Per-pass times and ratios under `cases`, followed by summaries for the development families. |
| [accepted_samples.json](ripser_v1/accepted_samples.json) | Individual measurements used in the summaries, with compilation and input-reset records. |
| [manifest.json](ripser_v1/manifest.json) | Input definitions, file fingerprints and the measurement protocol. |
| [verification.json](ripser_v1/verification.json) | The checks on barcodes, cocycles and landmark results. |

## Read a row

The row `cloud_circle96_f2` describes 96 points on a circle, with arithmetic
modulo 2 and homology computed through degree 1. Degree 0 tracks connected
components; degree 1 tracks loops. This request asks for barcodes without
retaining cocycles or selecting landmarks.

| Field | Value and meaning |
| :--- | :--- |
| `n` | 96: the number of input points. |
| `prime`, `degree` | 2, 1: the coefficient prime and highest requested homology degree. |
| `tamerop_seconds` | 0.005805637: TamerOp's summary query time, about 5.81 milliseconds. |
| `ripser_seconds` | 0.0199566745…: Ripser.py's summary query time, about 20.0 milliseconds. |
| `ratio_seconds` | 2.92896…: the paired query measurements give TamerOp about 2.93 times Ripser.py's speed on this request. |
| `interval_count` | 97: the returned barcode has 96 degree 0 intervals and one degree 1 interval. |

Ratios always divide Ripser.py time by TamerOp time, so values above 1 favor
TamerOp. Each ratio summarizes paired runs; dividing the separately
summarized tool times need not give the same number.

## Understand the timings

Each tool has three time fields, all in seconds. The `tamerop_` and `ripser_`
prefixes identify the program:

| Field ending | Work measured |
| :--- | :--- |
| `seconds` | Compute the complete result from the program's own input container. This query time is the main comparison. |
| `construction_seconds` | Build that container from decoded input values. |
| `construction_plus_query_seconds` | Add construction and query times for each sample, then summarize those sums. |

Parsing, generating inputs, exporting answers and checking results happen
outside the timers. `ratio_seconds`, `ratio_construction_seconds` and
`ratio_construction_plus_query_seconds` compare the corresponding stages.

There are four *passes*, each a round of measurements in separately launched
processes. A discarded warmup precedes three fresh computations per request
and tool. The middle of those three times is the pass median. The displayed
time is the median of the four pass medians, meaning the average of the two
middle values when ordered. JSON fields `tamerop_pass_medians` and
`ripser_pass_medians` retain those stage times.

For each stage, the reported ratio is the geometric mean of four paired
ratios: multiply them and take the fourth root. The corresponding `_passes`
field retains those ratios, and `_pass_range` gives their minimum and maximum.
These ranges describe observed variation across runs; they are not confidence
intervals estimating uncertainty in a population mean.

## Identify and combine requests

| Field | Meaning |
| :--- | :--- |
| `id`, `family`, `shape` | The request identifier, its comparison group and its input construction. |
| `cohort` | Whether the request belongs to development or to the separately reported reserved evaluation set. |
| `prime` | The prime used for arithmetic on coefficients. |
| `degree` | The highest homology degree requested, including lower degrees. |
| `cocycles` | Whether the result retains algebraic representatives of the detected classes as well as intervals. |
| `landmarks` | The requested number of selected landmark points. `null` or an empty CSV field means no landmark selection was requested. |
| `status` | Whether the request completed with its answer verified. |
| `intervals_by_degree` | In JSON, the interval counts in degree order, starting with degree 0. Their sum is `interval_count`. |
| `exported_witnesses` | How many cocycle representatives were exported for separate verification. This count describes the checking step. |

All requested representatives are retained inside the timer, even
when only a selection is exported for further checking. The
[report](ripser.md) describes the checks and the two programs' output conventions.

The development summaries give equal weight to requests within each family,
then equal weight to the six families. The six reserved evaluation requests
are reported separately. Keep `cohort` when calculating new summaries so that
those populations remain distinct. `practical_category` describes a query
ratio beyond the study's 10% margin as favoring one tool; values from 1/1.10
through 1.10 are treated as similar performance.

## Read the memory and verification records

Size and memory fields use bytes. `tamerop_allocation_bytes` counts memory
requested during the call, including temporary objects. The two tools'
`retained_output_bytes_estimate` fields estimate storage for the returned
objects using their respective runtime measurements. Their `_rss_bytes`
fields describe resident memory, the physical RAM held by the whole process,
including runtime and temporary working storage. These quantities let us
distinguish the size of an answer from the resources needed to compute it.

[machine.json](ripser_v1/machine.json) records the computer;
[build_verified.json](ripser_v1/build_verified.json) records the comparator
build. [Source fingerprints](ripser_v1/candidate_hashes.json) and
[measurement-script fingerprints](ripser_v1/harness_hashes.json) identify the
code used. [first_use.json](ripser_v1/first_use.json) records startup work,
while [rejected_samples.json](ripser_v1/rejected_samples.json) preserves
observations excluded from the summaries.

The [checksum list](ripser_v1/SHA256SUMS) gives SHA-256 fingerprints for the
archived files. Follow
[Reproduce a benchmark report](../benchmark_reproduction.md) with the study
name `ripser-py-v1` to verify the records, regenerate the inputs and collect
new measurements.
