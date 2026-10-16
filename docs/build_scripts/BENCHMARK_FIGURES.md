# Rendering benchmark figures

The benchmark reports use archived measurements and a common plotting preset.
This guide describes how to regenerate their figures and retain the evidence
behind them. For a new study or a run on another machine, use the
[TamerOp-benchmarks contribution guide](https://github.com/erikmnovak/TamerOp-benchmarks/blob/main/CONTRIBUTING.md)
and its [measurement protocol](https://github.com/erikmnovak/TamerOp-benchmarks/blob/main/PROTOCOL.md).

## Regenerate the report figures

Install Matplotlib 3.9.3 in the website's Python environment. From the repository
root:

```sh
docs/.venv/bin/python -m pip install matplotlib==3.9.3
MPLCONFIGDIR=/tmp/tamerop-matplotlib docs/.venv/bin/python docs/build_scripts/render_benchmark_reports.py
```

On Windows, use `docs\.venv\Scripts\python.exe` and a writable
`MPLCONFIGDIR` set through your shell. Matplotlib is needed for rendering;
ordinary website builds use the tracked figures.

[render_benchmark_reports.py](render_benchmark_reports.py) verifies the archived
files against their `SHA256SUMS`, reads them through the study adapters and
writes SVG/PNG figures to `docs/benchmarks/presentation/`. It produces ordinary
and narrow layouts from the same values. `presentation.json` records those
values, the input hashes, plotting source hashes and Matplotlib version;
`SHA256SUMS` covers the presentation outputs.

To inspect one report, choose a separate output directory:

```sh
docs/.venv/bin/python docs/build_scripts/render_benchmark_reports.py --report phat --output docs/.build/phat-figures
```

The current adapters are
[benchmark_report_qpa_phat.py](benchmark_report_qpa_phat.py),
[benchmark_report_ripser.py](benchmark_report_ripser.py) and
[benchmark_report_cubical_visual.py](benchmark_report_cubical_visual.py).
They prepare the values plotted by the shared renderer. Check an adapter's
population, timing boundary, unit conversions and summary calculation against
the study when adding or changing a figure.

## Use the plotting preset

[report.mplstyle](../assets/benchmarks/report.mplstyle) supplies the common
appearance. Apply it inside a Matplotlib style context so its settings stay
local to these plots:

```python
from pathlib import Path
import matplotlib.pyplot as plt

# For a script in docs/build_scripts/.
root = Path(__file__).resolve().parents[2]
with plt.style.context(root / "docs/assets/benchmarks/report.mplstyle"):
    fig, ax = plt.subplots()
    # Draw the measured values and label the axes here.
```

Map tools to colors explicitly. A missing series must not shift the remaining
tool to a different color.

| Element | Convention |
| --- | --- |
| TamerOp | Blue `#156b91`, first in the legend. |
| Comparator | Orange `#d36935`, labeled with its software name. |
| Other marks | Gray `#788590` for individual ratios, `#44505b` for reference lines, `#eeeeee` for a declared practical band. |
| Canvas and text | Opaque white background, black text, DejaVu Sans. |
| Type and strokes | The preset uses 10 pt labels and ticks, 12 pt panel titles, 2 pt lines and 5 pt markers. Adjust layout so these remain readable at page width. |
| Export | SVG with labels retained as text and a white canvas; PNG companions when useful. |

For scatter plots with overlapping points, an area of 22 pt² and opacity 0.65
are useful starting values. A shared heading or legend for several panels can
use 11 pt text. Set these choices in the renderer when the layout calls for
them, and check readability at the displayed page width; ordinary legends keep
the preset's size.

Use labels, line styles or markers as well as color to distinguish series.
When coefficient fields share a figure, the existing convention is circle,
square, triangle and diamond for QQ, F₂, F₃ and F₁₀₁. Keep each visual encoding's
meaning consistent: if shape denotes field, use labels or line style to
distinguish tools. Put a shared legend outside the data when a group of panels
uses the same key.

## Preserve the meaning of the measurements

Axes need quantities and units. Ratio plots use **comparator time / TamerOp
time**, so values above one favor TamerOp; draw and label equality at one.
State when a logarithmic scale is used. Identify interval marks as confidence
intervals, observed ranges or another quantity actually supplied by the study.

Use the same units in companion tables and figures where practical, and
label conversions explicitly. Comparable panels should use consistent limits
or visibly identify their different scales. Limits must retain the relevant
observations and uncertainty.

A performance profile is a step function: show its measured jumps and state
the population and weighting. Connect points along an ordered size sequence
only when they describe the same structural variant; leave unrelated inputs
as separate points. Missing or incomplete results remain visibly missing.
Use the study's declared practical band rather than choosing a new threshold
while plotting.

The report's native `picture` element selects the narrow layout on small
screens. For example, from a report under `docs/benchmarks/`:

```html
<a href="presentation/phat_ratios.svg"><picture>
<source media="(max-width: 600px)" srcset="presentation/phat_ratios_narrow.svg">
<img src="presentation/phat_ratios.svg"
     alt="PHAT time divided by TamerOp time for the measured input families."
     loading="lazy" style="width:100%;max-width:780px;height:auto">
</picture></a>
```

Write alternative text and a caption that explain the actual comparison.
Check readable labels, mathematical glyphs, legends and clipping at ordinary
and narrow page widths in both themes. Compare plotted values, missing cases,
uncertainty and captions with the underlying data; use the report's tables
and linked JSON for exact values.

## Keep measurements and presentation separate

Regenerating a figure redraws the recorded measurements. Keep the study's
archived inputs, measurements and checksum-covered README unchanged. New
measurements receive a new study version. The website's evidence copies must
match the versioned files in TamerOp-benchmarks, and the report must identify
the benchmark commit or release.

Presentation files have their own checksums, so a revised layout can be
recorded without rewriting the measurement archive. A maintained data
dictionary is a separate authored page; the archived README remains an exact
download. After changing figures, rebuild the site using the
[build guide](../README.md#build-and-preview), run the site checks and review
the rendered report and dictionary.
