#!/usr/bin/env python3
"""Render the benchmark reports from their archived measurements, without timing code."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, MaxNLocator, NullFormatter

ROOT = Path(__file__).resolve().parents[2]
MODULES = ("benchmark_report_qpa_phat", "benchmark_report_ripser", "benchmark_report_cubical_visual")
BLUE, ORANGE, GRAY = "#156b91", "#d36935", "#44505b"


def load_reports(root: Path = ROOT) -> list[dict]:
    return [report for name in MODULES for report in importlib.import_module(name).build_data(root)]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_archives() -> None:
    """Check historical files before interpreting or redrawing their results."""
    for name in ("qpa_v1", "phat_v2", "ripser_v1", "ripser_cpp_v1", "cubicalripser_v1", "visual_interaction_v1"):
        archive = ROOT / "docs/benchmarks" / name
        for line in (archive / "SHA256SUMS").read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            expected, relative = line.split(maxsplit=1)
            target = archive / relative.removeprefix("*")
            if digest(target) != expected:
                raise ValueError(f"Archived measurement file changed: {target}")


def check_data(report: dict) -> None:
    for row in report.get("ratio_rows", []):
        assert row["value"] > 0, row
        if "low" in row or "high" in row:
            assert 0 < row["low"] <= row["value"] <= row["high"], row
    for row in report.get("time_rows", []):
        assert row["tamerop_seconds"] > 0 and row["comparator_seconds"] > 0, row
    for row in report.get("latency_rows", []):
        assert 0 < row["median_ms"] <= row["p95_ms"], row


def number(value: float) -> str:
    return f"{value:,.3g}"


def axes(rows: list[dict], narrow: bool):
    count = len(rows)
    fig, ax = plt.subplots(figsize=((3.8 if narrow else 7.8),
                                    1.2 + count * (.73 if narrow else .42)))
    fig.subplots_adjust(left=.065 if narrow else .36, right=.96,
                        top=.96, bottom=min(.26, .83 / fig.get_figheight()))
    ax.set_ylim(count - .3, -.85 if narrow else -.6)
    ax.grid(False, axis="y")
    if narrow:
        ax.set_yticks([])
        for i, row in enumerate(rows):
            label = textwrap.fill(row["label"], width=39)
            ax.text(0, i - .21, label, transform=ax.get_yaxis_transform(),
                    ha="left", va="bottom", fontsize=10.5,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
    else:
        ax.set_yticks(range(count), [textwrap.fill(row["label"], 30) for row in rows])
        ax.tick_params(axis="y", length=0, pad=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    return fig, ax


def log_axis(ax, narrow: bool, *, parity: bool = False):
    ax.set_xscale("log")
    low, high = ax.get_xlim()
    powers = range(math.floor(math.log10(low)), math.ceil(math.log10(high)) + 1)
    ticks = [m * 10.0 ** p for p in powers for m in (1, 2, 5)
             if low <= m * 10.0 ** p <= high]
    if len(ticks) > (5 if narrow else 8):
        ticks = [10.0 ** p for p in powers if low <= 10.0 ** p <= high]
    if len(ticks) < 3:
        ticks = [t for t in MaxNLocator(nbins=4 if narrow else 6).tick_values(low, high)
                 if low <= t <= high and t > 0]
    if parity and low <= 1 <= high:
        ticks = sorted({1.0, *(t for t in ticks if abs(math.log(t)) > .12)})
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:g}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis="x", labelsize=10)


def save(fig, out: Path, stem: str) -> list[Path]:
    # SVG text remains readable/selectable; all variants share the same data.
    result = []
    for suffix in ("svg", "png"):
        path = out / f"{stem}.{suffix}"
        fig.savefig(path, metadata={"Date": None} if suffix == "svg" else None,
                    bbox_inches="tight", pad_inches=.12)
        result.append(path)
    plt.close(fig)
    return result


def render_ratios(report: dict, out: Path, narrow: bool) -> list[Path]:
    rows = report["ratio_rows"]
    fig, ax = axes(rows, narrow)
    ax.axvline(1, color=GRAY, linewidth=1, zorder=1)
    for i, row in enumerate(rows):
        if "low" in row:
            ax.plot([row["low"], row["high"]], [i, i], color=BLUE, linewidth=2)
        ax.plot(row["value"], i, "D", color=BLUE, markersize=5)
    ax.set_xlabel(f"{report['comparator']} time / TamerOp time\nAbove 1: TamerOp takes less time\nLogarithmic scale", fontsize=10.5)
    bounds = [x for r in rows for x in (r.get("low", r["value"]), r.get("high", r["value"]))]
    ax.set_xlim(min(.85, min(bounds) / 1.3), max(1.2, max(bounds) * 1.35))
    log_axis(ax, narrow, parity=True)
    return save(fig, out, report["id"] + "_ratios" + ("_narrow" if narrow else ""))


def render_times(report: dict, out: Path, narrow: bool) -> list[Path]:
    latency = bool(report.get("latency_rows"))
    milliseconds = latency or report["id"] in ("qpa", "phat")
    scale = 1000 if milliseconds else 1
    rows = report["latency_rows"] if latency else report["time_rows"]
    fig, ax = axes(rows, narrow)
    for i, row in enumerate(rows):
        first = row["median_ms"] / 1000 if latency else row["tamerop_seconds"]
        second = row["p95_ms"] / 1000 if latency else row["comparator_seconds"]
        first, second = first * scale, second * scale
        ax.plot([first, second], [i, i], color="#b5bcc2", linewidth=1.2, zorder=1)
        ax.plot(first, i, "o", color=BLUE, markersize=5, zorder=3)
        ax.plot(second, i, "s", color=GRAY if latency else ORANGE, markersize=5, zorder=2)
    # Set logarithmic autoscaling before choosing readable, nonoverlapping ticks.
    ax.set_xscale("log")
    ax.relim()
    ax.autoscale_view()
    log_axis(ax, narrow)
    unit = "ms" if milliseconds else "seconds"
    ax.set_xlabel(f"Time ({unit}; logarithmic scale)", fontsize=10.5)
    labels = ["Median", "95th percentile"] if latency else ["TamerOp", report["comparator"]]
    handles = [Line2D([], [], color=BLUE, marker="o", linestyle="", label=labels[0]),
               Line2D([], [], color=GRAY if latency else ORANGE, marker="s", linestyle="", label=labels[1])]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5, -.25 if len(rows)<5 else -.13),
              ncol=2, frameon=False, fontsize=10)
    return save(fig, out, report["id"] + "_times" + ("_narrow" if narrow else ""))


def render(output: Path, only: str | None = None) -> dict:
    verify_archives()
    output.mkdir(parents=True, exist_ok=True)
    reports = [r for r in load_reports() if only is None or r["id"] == only]
    if not reports:
        raise ValueError(f"Unknown report: {only}")
    files = []
    with plt.style.context(ROOT / "docs/assets/benchmarks/report.mplstyle"), \
            matplotlib.rc_context({"svg.hashsalt": "tamerop-benchmark-reports-v1"}):
        for report in reports:
            check_data(report)
            for narrow in (False, True):
                if report.get("ratio_rows"):
                    files.extend(render_ratios(report, output, narrow))
                if report.get("time_rows") or report.get("latency_rows"):
                    files.extend(render_times(report, output, narrow))
    sources = sorted({s for r in reports for s in r["sources"]})
    rendering_sources = ["docs/build_scripts/render_benchmark_reports.py",
                         "docs/assets/benchmarks/report.mplstyle",
                         *(f"docs/build_scripts/{name}.py" for name in MODULES)]
    record = {"schema_version": 1, "description": "Figures redrawn from archived measurements; no new timings",
              "reports": reports, "inputs": {s: digest(ROOT / s) for s in sources},
              "rendering_sources": {s: digest(ROOT / s) for s in rendering_sources},
              "matplotlib_version": matplotlib.__version__,
              "outputs": {p.name: digest(p) for p in files}}
    (output / "presentation.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    sealed = sorted(files + [output / "presentation.json"])
    (output / "SHA256SUMS").write_text("".join(f"{digest(p)}  {p.name}\n" for p in sealed))
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/benchmarks/presentation")
    parser.add_argument("--report", help="Render one report, e.g. phat; use a separate output directory")
    args = parser.parse_args()
    result = render(args.output, args.report)
    print(f"Rendered {len(result['reports'])} benchmark reports in {args.output}")
