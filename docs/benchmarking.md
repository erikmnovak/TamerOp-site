# How the benchmarks were measured

The [benchmark reports](benchmarks/index.md) compare the time needed to answer
a specified mathematical question. That question determines where the timer
starts and stops: constructing a barcode is a different task from constructing
a barcode together with representatives of its classes. We arrange for both
programs to receive the same mathematical information and check that their
answers satisfy the same request.

This page explains the measurements and the choices that affect their
interpretation. To run a study yourself, follow
[Reproduce a benchmark report](benchmark_reproduction.md).

## The benchmark computer

The reports use the same workstation. Each study's records identify its
software versions and operating conditions.

| Component | Configuration |
| :--- | :--- |
| Processor | Intel Core i7-1365U, 10 physical cores and 12 logical CPUs |
| Installed memory | 32 GB; approximately 31 GiB visible to Linux |
| Operating system | 64-bit Linux, kernel 6.8 |
| Julia | 1.12.1 |
| Comparative computation | One numerical thread per tool; workers run serially |

The original machine records are available for
[QPA](benchmarks/qpa_v1/provenance.json),
[PHAT](benchmarks/phat_v2/provenance.json),
[Ripser.py](benchmarks/ripser_v1/machine.json),
[C++ Ripser](benchmarks/ripser_cpp_v1/machine_and_build.json),
[CubicalRipser](benchmarks/cubicalripser_v1/MACHINE.json), and
[browser interaction](benchmarks/visual_interaction_v1/machine.json).
They retain the exact kernel, thread settings and other recorded conditions.
The browser study additionally records the browser and rendering software.

Some studies ran while the workstation was doing other work. Their reports
identify this beside the sampling details and show the observed variation.
Using the same hardware makes the environment easier to recognize; the
comparison itself still pairs measurements from the same study.

## Practical significance and presentation

The speed ratio is the comparator's time divided by TamerOp's time for the
same request. A ratio of 2 means TamerOp took half as long; a ratio of 0.5 means
the comparator took half as long. All ratio plots use this direction, with
a line at 1 for equal time. TamerOp is blue and the comparator orange in plots
of elapsed time. A blue ratio marker represents the comparison itself.

For a ratio $r$, TamerOp's reduction in time relative to the comparator is
$100(1-1/r)$ percent. Thus 1.33× as fast corresponds to about 25% less time.
The reports pair these relative differences with actual times: saving half
a millisecond and saving several seconds have different consequences for
someone deciding what to compute.

Each aggregate has a stated population and weighting. PHAT's four input
families have equal weight, so adding more graph examples would not by itself
make graphs more influential in that summary. We use geometric means for
multiplicative ratios: average their logarithms with the declared weights,
then exponentiate. This treats a factor of 2 and its reciprocal symmetrically.

The displayed runtime for a case is usually a median across independent
process passes. The ratio is computed from paired observations before those
display medians are taken. Dividing two rounded table entries therefore need
not recover the reported ratio.

Intervals carry their actual meaning. QPA and PHAT report approximate 95%
intervals; the Rips reports show ranges across process passes. A range across
different inputs describes a third kind of variation. Captions identify which
one is drawn. We do not assign every study the same error bars merely to make
the figures look alike.

The comparison studies use a declared practical band from 1/1.10 to 1.10
where applicable. Point estimates in that band are described as similar
performance, with the measured edge stated. The band is a convention for the
size of a difference, not a statistical equivalence test. Material slowdowns,
incomplete computations and memory costs remain part of the account.

## What each timer includes

A complete request has a starting object and a recognizable answer. These
boundaries distinguish the reports:

| Study | Starting information | Requested answer and primary timer |
| :--- | :--- | :--- |
| QPA | Decoded finite module data in a prepared category | Native construction and the complete algebraic query |
| PHAT | Decoded filtered boundary data | Native construction and the complete barcode |
| Ripser.py | Prepared native cloud, distance or graph input | Complete query, including the representatives or landmarks requested by that case |
| C++ Ripser | Supplied distance file | File reading, barcode computation and interval output |
| CubicalRipser | Decoded image or volume array | Construction and the complete cubical barcode through the public call |
| Browser interaction | An active viewer with its declared retained objects | Browser input through receipt and display of the committed result |

In finite module algebra, a basis of Hom means actual compatible maps, rather
than only the dimension of their space. In a barcode comparison, the degree
range, endpoint conventions and surviving classes determine which intervals
belong to the answer. The report develops these distinctions for its own task.

If programs do equivalent preparation in different stages, a combined timer
can capture construction and the query together. QPA and PHAT use an
uninterrupted timer for this total. Ripser.py's supporting construction-plus-query
statistic instead adds the two separately timed stages within each sample;
its primary result measures the query. Neither procedure adds separately
aggregated medians. Component timings help explain where the difference arises.

### Keep competitor implementations unchanged

Comparators use their recorded upstream implementations through supported
interfaces. The harness converts inputs, calls the tool, measures the declared
work and checks the output. It does not replace the comparator's algorithms.
Build options and selected reduction methods appear in each report.

The tools may represent the same problem differently. QPA uses a quiver and
relations for the finite module problems; persistence packages may reduce
different matrices or work with cohomology. We align the mathematical request
and verify the answer rather than require the same internal steps. A measured
difference does not by itself identify its algorithmic cause.

## Compilation and fresh computation

Most comparative results measure compiled code doing a fresh computation.
Loading and compilation have already happened, but a previous answer has not
been retained. The browser study measures another situation: an active session
whose retained object supports a new interaction.

Each worker first exercises the relevant methods and measurement wrappers.
Before an accepted sample, it discards earlier outputs and resets the
mathematical state that could save query work. That state can include
reductions, resolutions, matrix factors and cached coordinates. The harness
checks the reset, measures one complete request, checks the result outside
the timer, and resets again before another sample.

Constructing a new wrapper around an old object would not establish this
reset. The study records identify which objects and caches were examined
and which input preparation was retained. Work shared *within* the current
request remains available to both programs: discarding a useful resolution
halfway through a calculation would change the algorithm being measured.

Normal public input validation and garbage collection during the request
remain inside the measured operation. Julia's timing record also includes
compilation and recompilation counters. Accepted primary samples record
zero for both. A sample containing compilation stays in the record separately;
after the missing warmup, the computation is reset and measured again.
Compilation time is never subtracted to manufacture an accepted runtime.

First use is measured separately. Loading a package, preparing an input,
compiling a new method and answering a query are distinct costs. A complete
first-answer measurement follows one uninterrupted process from launch to
answer. Isolated stage medians do not add up to that observation.

## Inputs, repetitions and aggregation

The input suite is fixed before the final measurement passes. It includes
several mathematical structures, a bounded range of sizes and small cases
whose answers can be checked independently. Fields, seeds, dimensions and
resource limits are recorded with the inputs.

Different sizes of one family share a construction rule. Different families
can have very different complexity at the same nominal size: an algebraic
boundary matrix with few cells can be much denser than a large graph. The
reports therefore give dimensions, nonzero counts or output sizes alongside
simple point and cell counts.

The studies repeat their measurements in independent process passes, with
several reset samples in each pass. A process pass starts the runtime again;
many function calls in one process do not provide the same independent
replication. Tool or case order is reversed or alternated as specified in
the study. Ratios pair the same case, phase and process pass before any
aggregation across cases.

Development inputs and separate evaluation inputs retain their identities.
Ripser.py's headline uses its development families; CubicalRipser's declared
aggregate includes 36 regular arrays and 12 reserved arrays. Calibration
observations used to determine feasible sizes remain distinguishable from the
final measurements. Each summary follows its study's declared population and
weights.

Raw records retain sample times, warmups, counters, verification outcomes,
process identities and failures. Repetition describes the observed variation;
it cannot remove systematic interference from other work on the computer.
The [study-design guide](benchmark_suites.md) explains how scope, weighting
and sampling are chosen before confirmation.

## Checking the mathematical answers

For barcodes, the checks compare complete interval collections in each
requested degree, including multiplicities and classes that survive to the
end. Supplied exact grades permit exact comparisons. Native floating-point
distance calculations use the explicitly stated tolerance. Representative
cocycles receive their own checks when requested.

For finite module algebra, equal dimensions alone do not verify returned
maps. The checks examine the defining equations, independence, completeness
and the structural maps required by the operation. Resolutions, products and
induced maps are checked in the category and field specified by the request.
Small independent computations provide another route to known answers.

A failure, timeout or unsupported request has no paired speed ratio. It stays
visible in the coverage record with its outcome. QPA's incomplete tensor
evaluations, for example, remain separate from the matched algebraic
comparisons. A timeout records the applied limit rather than an infinite
measured runtime.

## Memory and resource limits

A process can complete a request quickly while requiring more memory, so
the reports retain memory measurements beside their software and resource
settings.

| Quantity | What it measures |
| :--- | :--- |
| Allocated bytes | Memory requested during the operation, including temporary objects |
| Retained result size | Storage still reachable from the specified returned objects |
| Resident set size, or RSS | Memory held in RAM by the process, including the runtime and native libraries |
| Peak RSS | The largest recorded resident footprint over the stated process lifetime |

A small returned barcode can coexist with a large process peak. The memory
tables identify the process lifetime: one C++ invocation and a Julia worker
that loaded, compiled and repeated several requests need not cover the same
stages. Resource limits are recorded separately from observed memory use.

## Files, checksums and reproduction

[TamerOp-benchmarks](https://github.com/erikmnovak/TamerOp-benchmarks) holds the
executable studies, input generators, pinned environments, source snapshots
and versioned measurements. Each website report provides its principal JSON
result, SHA-256 checksum and supporting records. The website's copies retain
the original bytes so the report and evidence can be inspected together.

A SHA-256 checksum is a fingerprint of a file's bytes. Matching it confirms
that a download is the file identified by the report. Mathematical checks
serve a different purpose: they establish what the computation returned.
New timing runs write new records, reflecting the machine on which they ran.

Follow [Reproduce a benchmark report](benchmark_reproduction.md) to verify the
files, regenerate figures or run a comparison. Authors preparing another
study can use the [study charter](benchmark_suites.md#reusable-suite-charter),
[execution protocol](https://github.com/erikmnovak/TamerOp-benchmarks/blob/main/PROTOCOL.md)
and [report template](benchmark_style.md#report-template).
