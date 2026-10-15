# Reproduce a benchmark report

We will reproduce the steps behind a report: check its recorded files, prepare
the same mathematical inputs and software, compute a small verified example,
and then collect new measurements. The same commands select each comparison,
so changing from PHAT to a Rips or finite module study does not require
learning another procedure.

The original result files stay separate from your run. Their checksums
identify the measurements behind the report; your new observations describe
the same computation on your computer.

## Get the study

Install Python 3.12, Julia 1.12.1 and the compiler or browser tools listed
in the chosen study's README. The timing drivers target Linux, where they can
record the process and resource information used by these studies.

Clone the benchmark repository and select the revision used by these reports:

```sh
git clone https://github.com/erikmnovak/TamerOp-benchmarks.git
cd TamerOp-benchmarks
git checkout cc389ab410d3d3e6df163a6af6bef48c9cf7b1f1
python run.py list
```

The study names correspond to the reports:

| Name to pass to the command | Computation |
| :--- | :--- |
| qpa-v1 | Finite module algebra with GAP/QPA |
| phat-v2 | Barcodes from filtered boundary matrices with PHAT |
| ripser-py-v1 | Rips persistence, cocycles and landmarks with Ripser.py |
| ripser-cpp-v1 | Distance files to barcodes with the original C++ Ripser |
| cubicalripser-v1 | Image and volume barcodes with CubicalRipser |
| visual-interaction-v1 | Browser input through a live Julia result |

We will use PHAT for the commands below. Replace `phat-v2` with another
study name to follow its preparation and measurement procedure.

## Check the files

```sh
python run.py verify phat-v2
```

This verifies the published evidence, selected source files and study harness.
A mismatch names the affected file before you spend time preparing a run.

The report also gives the SHA-256 fingerprint of its principal JSON result.
To check that download directly, run:

```sh
sha256sum studies/phat-v2/evidence/results.json
```

Compare the printed hexadecimal value with the one under Reproduce the results
in the [PHAT report](benchmarks/phat.md). The study's SHA256SUMS file applies
the same check to its supporting records. These fingerprints identify the
files; the mathematical validation in the next steps checks their computations.

## Prepare the software and inputs

```sh
python run.py prepare phat-v2
```

Preparation creates a study directory under `_work/`, builds the pinned
comparator through its upstream source recipe, prepares the recorded Julia
environment and generates the inputs. Downloaded tools and generated matrices
stay in this work directory. Input hashes are checked against the archived
definitions where the study records exact bytes.

Each study README lists its additional tools, expected storage and relevant
options; `python run.py prepare phat-v2 --help` lists the options at the terminal.
For example, the Rips studies generate their larger distance matrices
locally instead of putting hundreds of megabytes of generated input into the
repository. QPA prepares GAP and its packages; the browser study prepares the
specified browser environment.

If Julia is installed under a versioned path, supply it explicitly:

```sh
python run.py prepare phat-v2 --julia /path/to/julia
```

The runner checks the requested version rather than silently choosing another
implementation. Source snapshots identify the historical TamerOp computation,
including changes that were not yet part of its recorded base commit.

## Compute a small checked example

```sh
python run.py smoke phat-v2
```

This command runs a small complete request and checks its mathematical answer.
For PHAT, the check compares full barcodes; other studies use the verification
appropriate to their output, such as cocycle equations or maps between
modules. The command succeeds only after its computation and checks finish.

Run this step before the full study. It verifies that the prepared tools can
execute the intended task on your machine and that their output is readable
by the comparison harness.

## Collect new measurements

```sh
python run.py measure phat-v2
```

The full command uses the study's fixed input suite, warmup, sample counts and
process passes. Leave the machine otherwise idle and run one study at a time.
The shared runner prevents simultaneous measurement jobs from this repository.

Fresh observations and verification records are written under
`_work/phat-v2/`. The study README identifies the final result files and
its resume behavior. Keep the warmups, failed attempts and process records
with the accepted timings, since they explain which measurements entered the
summary.

To keep an additional run in its own directory, use the same path for every
stage:

```sh
python run.py prepare phat-v2 --work /path/to/another-run
python run.py smoke phat-v2 --work /path/to/another-run
python run.py measure phat-v2 --work /path/to/another-run
```

Compare matched requests and timing phases. A newly launched Julia session,
a compiled fresh query and an interaction with a retained object measure
different things. The [measurement account](benchmarking.md) explains those
boundaries and the statistics used by the reports.

## Redraw the published figures

To inspect the reported results without collecting new timings, use the
website's presentation scripts. They read the archived JSON and retain the
original weights, populations and missing results.

```sh
git clone https://github.com/erikmnovak/TamerOp-site.git
cd TamerOp-site
python -m venv .venv
.venv/bin/python -m pip install matplotlib==3.9.3
.venv/bin/python docs/build_scripts/render_benchmark_reports.py --output /tmp/tamerop-report-figures
```

The output contains the SVG and PNG figures, narrow versions for phones,
the values drawn in each plot and a separate SHA256SUMS file. Rendering these
figures does not run Julia or change the original evidence. The
[report template](benchmark_style.md#report-template) explains how to use
the same presentation for another study.
