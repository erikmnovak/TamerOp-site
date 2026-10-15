# Writing a benchmark report

Use the [PHAT report](benchmarks/phat.md) as the structural model: a clear
performance result, variation across meaningful families, and actual waiting
times before the measurement details. The QPA figures established the shared
blue and orange palette, white backgrounds and light grids. The
[Matplotlib preset](assets/benchmarks/report.mplstyle) and
[common figure generator](build_scripts/render_benchmark_reports.py) carry
that visual identity across the reports.

The reports deliberately share an order and vocabulary. Readers should find
the answer, understand its size, and then examine how it was measured without
learning a different report format for every comparator. The
[measurement account](benchmarking.md) explains the common interpretation;
the [execution protocol](https://github.com/erikmnovak/TamerOp-benchmarks/blob/main/PROTOCOL.md)
governs the studies themselves. Formatting never changes the population,
weights, timing boundary or meaning of a measurement.

## Page rhythm and tables

Use a descriptive title such as “Finite module algebra: TamerOp and QPA”.
Open with one short paragraph introducing the comparator, the problem it is
known for solving, and why that makes it relevant here. Cite its own project
or authors. Avoid unsupported claims about popularity or superiority.

Follow the template below. Put the numerical finding at the start of Results,
then the common ratio plot and actual runtimes. A weighted aggregate can be a
headline when the study declares one. Otherwise use a concrete family or
example, preserving substantial results in the other direction nearby.
Say “2.18× as fast” or “about 54% less time”, with the scope that makes the
number meaningful. Do not write “2.18× times faster”, treat a mean ratio as
a universal factor, or invent an aggregate to fill a template slot.

Keep methods, software and reproduction after the main results. Give the
reader enough immediate context to understand the comparison, then develop
the detailed conditions in their own sections. Remove authoring status,
future-page promises and generic defensive disclaimers. A substantive timing
boundary or missing comparison still belongs wherever it changes the claim.

Keep the native documentation typography and ordinary Markdown tables. Use
short connected paragraphs, descriptive headings, and bold only for the few
numbers or qualifications that carry the conclusion. Avoid decorative cards,
badges, colored winner tables and repeated headline numbers. The
[presentation guidance](benchmarking.md#practical-significance-and-presentation)
governs the wording of gains, similar performance and material losses.

Put the request or family first in tables, then input sizes and measurements.
Keep TamerOp before the comparator in time columns and legends. Left-align
labels and prose, right-align numeric columns, put units in headers, and use
consistent rounding within a column. Display roughly three significant figures
for comparisons; fixed
decimal places are useful for a runtime table when they retain meaningful
small values. Give full precision in downloads. Define medians, ranges and
intervals before the table. A range across different inputs must look and read
differently from a confidence interval. Use explicit missing-result text such
as “No verified completion”, never a zero or an unexplained blank.

## Shared figure settings

These settings reproduce QPA's visual character. Sizes are starting points
at export size; check legibility at the width used on the page.

| Element | Default |
| :--- | :--- |
| TamerOp | Blue `#156b91`, always the first tool in the key |
| Comparator | Orange `#d36935`, labeled with the actual software name |
| Background and text | Opaque white figure and axes; black text |
| Typography | DejaVu Sans or a comparable plain sans serif; normal weight |
| Text sizes | 10 pt ticks, axis labels and legend; 12 pt panel titles; 11 pt shared heading/key |
| Axes | Thin black lines, 0.8 pt; outward ticks. Common horizontal comparison plots use the bottom frame; scaling panels may retain the full frame. |
| Grid | Major ticks only, gray `#b0b0b0`, opacity 0.20, width 0.8 pt; behind the data |
| Lines and points | 2 pt comparison lines; about 5 pt line markers; scatter area 22 pt² and opacity 0.65 when overlap matters |
| Supporting marks | Gray `#788590` for individual ratio observations; `#44505b` for parity/reference lines; pale gray `#eeeeee` for a declared practical band |
| Export | SVG with an opaque white canvas; PNG when a raster copy is useful |

Supporting grays extend the QPA pair to other chart types; they do not create
a second competitor palette. Keep tool identity independent of performance:
the blue series is still TamerOp on a slower case. Additional tools need an
explicit, consistent key rather than cycling the two colors and making them
ambiguous. Color can be supplemented with solid/dashed lines, distinct markers
or direct labels. Do not rely on color alone to identify a series.

For coefficient fields, retain QPA's circle/square/triangle/diamond convention
for QQ/F₂/F₃/F₁₀₁ when those fields occur together. When shape already denotes
field, use line style, direct labels or separate clearly titled tool panels
for redundant tool identification; do not make shape mean two things in one
figure. Keep semantic mappings stable across the report.

Prefer one shared key for a panel group, positioned outside the data, rather
than repeating the same legend in every panel. A single plot can use a small
legend in unused space. Titles identify the request or structural variant;
the caption explains the conclusion. Use whitespace and alignment to separate
panels. A 7 × 4 inch single plot matches QPA's profile; panel groups can use
two or three columns when readable. Split a large sheet before shrinking
labels to fit the page. QPA's full thirteen-panel sheet is not a required layout.

## Match the plot to the evidence

| Reader's question | Preferred treatment |
| :--- | :--- |
| How much of the suite completes within a given relative time? | A performance profile with the shared tool colors, a labeled factor axis and a fraction axis from zero to one. State the full denominator and any weighting. |
| How does runtime vary across heterogeneous inputs? | QPA-style scatter panels, grouped by meaningful request; show actual sizes and times without joining unrelated cases. |
| How does one structural variant scale across measured sizes? | Connected points for that variant's ordered size ladder, with the same tool colors and a shared key. State that connecting lines guide the eye. |
| Which families favor either tool, and by how much? | A horizontal ratio plot: subdued individual points, blue aggregate markers with labeled uncertainty, a gray parity line, and an optional neutral practical band. |
| Where does the memory go? | A separate labeled memory figure or table. Distinguish process RSS, allocation traffic and retained objects; use the tool colors only for genuinely comparable measurements. |

PHAT's scaling and interval plots answer questions that QPA's scatter and
profile do not. Keep those forms available within the shared style. For a
ratio plot, label the direction explicitly as `competitor time / TamerOp time`;
values above one favor TamerOp. Its aggregate marker represents a ratio,
not a standalone TamerOp runtime. Explain this in the key. The practical band
must be the one declared by the study, not a new threshold chosen for the plot.

Use logarithmic axes for multiplicative ratios or sizes/times spanning orders
of magnitude when that helps interpretation. State the scale and units.
Keep units consistent between companion plots and tables where practical;
if one uses seconds and the other milliseconds, say so explicitly. Share
axis limits between directly comparable panels when useful; visibly label
different scales. Choose limits to show all relevant data and uncertainty.
Do not copy QPA's numerical ranges or its 220-request denominator.

An empirical performance profile is a step function; render its actual jumps
rather than smoothing them. Incomplete results remain incomplete coverage,
not zero or infinite measured runtimes. Do not connect missing observations
as though they were measured. A caption should identify the population,
timing boundary, encodings and one fact to notice, with important limitations
beside the figure. Supply useful alternative text and link the underlying data.

## Reuse and review

Use [report.mplstyle](assets/benchmarks/report.mplstyle) inside a Matplotlib
style context so unrelated plots are unaffected. Resolve the path from the
report generator's repository root. The preset supplies appearance; explicitly
map tool names to colors and define scientific axes, markers and aggregation
in the generator. Other plotting libraries should reproduce the same visual
choices rather than being required to use Matplotlib.

Keep SVG labels as text when possible. This improves selection and inspection
over QPA's original outlined lettering; check mathematical glyphs in the
export. Preserve a white canvas in dark-mode pages so figure colors and text
remain readable. Figure sizing, accessible series distinctions, explicit unit
conversions and step profiles are refinements of the reference, not claims
that every original QPA figure already follows them.

Before publishing, inspect the report at ordinary page width and on a narrow
screen, including light and dark themes. Check label size, clipping, legend
placement, alternative text, numeric table alignment and access to full-size
figures. Compare each chart's values, bounds, missing cases and captions with
the data. Keep tables or downloads available where a dense figure requires
zooming. The opening should follow the same structure as PHAT and use the shared
figure language without requiring readers to learn its subject beforehand.

An aesthetic revision re-renders existing measurements; it does not require
new timing runs. Keep sealed measurement evidence intact. Publish revised
figures with appropriate presentation provenance/checksums rather than silently
overwriting an archived result set. A report may claim to use this style only
after its actual exported figures have been reviewed.

## Report template

Use these section names and this sequence for new reports. An interaction or
single-tool study keeps the sequence while naming its actual measurement; it
does not need an artificial competitor or ratio.

```markdown
# Subject: TamerOp and Comparator

Introduce the comparator, its distinctive purpose and why we compare it here.

## Results

State the principal supported performance finding, its workload and boundary.
Show the standard ratio figure with a short explanatory caption.
Include meaningful family differences and incomplete comparisons.

### Actual runtimes and input sizes

Give an understandable time example and a compact table or time plot.
Identify the cases or groups shown and how those times were summarized.

## What the comparison computes

Explain the inputs, requested mathematical answer and relevant conventions.
Define necessary terminology and why the outputs are comparable.

## How the measurements were taken

State the timer boundary, preparation/reset, repetitions and aggregation.
Explain how the answers were checked. Link the common computer specification.
Give a consistent software/resource table and the meaningful memory results.

## Reproduce the results

Link the common reproduction recipe and the versioned benchmark study.
Provide the principal result JSON and its literal SHA-256 fingerprint.
List the supporting observations, input/source records and checksum manifest.
```

### One hardware reference, specific study records

The [benchmark computer](benchmarking.md#the-benchmark-computer) is the
canonical human-readable hardware description. The overview gives a brief
processor/memory summary and links there. Individual reports link there too,
then use a two-column Component / Recorded version or setting table for their
software versions, source identity, thread or affinity choices, memory and
time limits, and relevant environmental differences. Keep the original
machine JSON with each study; a common computer does not imply unchanged
software or background activity.

### Common figures and exact evidence

Generate the leading ratio and time figures with
`docs/build_scripts/render_benchmark_reports.py`. Its study adapters read the
archived JSON directly. Each figure has an ordinary and a narrow layout,
selected through a native HTML picture element; labels remain readable on
a phone without shrinking a wide multipanel sheet. Match the prose and table
units to the actual axis. Use a logarithmic scale for multiplicative ratios,
and identify that scale in the caption. State whether marks show confidence
intervals, pass ranges, or no uncertainty estimate.

Choose additional scaling plots when they explain a result. The shared
appearance does not require the same statistical graphic for incompatible
measurements. Supply explanatory captions and alternative text, with tables
or linked JSON retaining exact values. Image links can open the SVG without
an extra instruction or download button.

Keep the evidence owned by TamerOp-benchmarks and the website's copies
identical. The report records a benchmark commit or release, never just a
moving branch for its reproducibility claim. Later data receive a new study
version. When an archived README belongs to a checksum manifest, keep its
historical bytes as a download and maintain the website's data dictionary in
a separate authored source. Route that source to the existing dictionary
address and link it from the report. This preserves the evidence while allowing
the reader's explanation to improve. Presentation outputs have their own
checksum manifest.

## Data dictionary template

A data dictionary teaches someone how to read the measurements. Use
[Reading the PHAT benchmark data](benchmarks/phat_data.md) as the example.
The reader should be able to open a file, interpret a row and understand how
it contributes to the report. A list of filenames and technical abbreviations
alone does not accomplish that.

Use the following order for each dictionary. Keep exact field names in code
format, with their meaning in ordinary prose. Explain a technical term where
it first becomes useful: a pass is a round of measurements, a median selects
the middle value, and resident memory is physical RAM held by a process.
Adapt these descriptions to the actual study rather than copying assumptions
from another comparison.

```text
# Reading the [comparator] benchmark data

Introduce the computation and what the records let the reader understand.
Link to the report. Identify the study version or date where needed.

## Choose a file
Recommend a starting table and explain what one row represents.
Give a short File / What you can learn from it table with working links.

## Read a row
Choose one real, understandable request from the data.
Use Field / Value and meaning columns for a small worked example.
Interpret its time, ratio and output in words, with explicit units.

## Understand the timings
Explain the timer's beginning and end before introducing statistical fields.
Describe samples, passes, medians and pairing in the order they are computed.
State the ratio direction and explain geometric averaging if used.
Distinguish observed ranges from confidence intervals.

## Identify and combine requests
Define input settings, output counts, grouping fields and missing values.
Explain weights, separate evaluation sets and incomplete comparisons.
Include a small output example if its stored form needs interpretation.

## Read the memory and verification records
Explain units and distinguish allocations, retained objects and process memory.
Place detailed machine, source, verification and excluded-run records here.
Link the checksum manifest and common reproduction recipe, with the study name.
```

Keep the main file table short enough to help someone choose. Introduce
specialist records later, alongside the question they answer. Define each
field through the quantity it measures, rather than expanding an abbreviation
into another unexplained phrase. For nested JSON, show the path to the value.
Explain the meaning of `null`, an empty field or a verification flag where it
affects interpretation; a missing measurement and an unrequested output may
use the same marker for different reasons.

Check example values against the released data. Preserve exact column names,
timing boundaries, weights and statistical procedures. The shared outline
helps readers find explanations; it does not make different studies use the
same experiment. Numerical detail belongs where it lets the reader interpret
or reconstruct a result, with the full measurement files available for further
inspection.

Review the dictionary alongside its report. Changes to field meanings,
download locations or study versions require checking both pages. An archived
file's checksum does not exempt its public explanation from editorial review.
