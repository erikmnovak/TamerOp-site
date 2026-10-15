"""Read published cubical and interaction evidence for the shared report figures.

This module performs no timed work and never changes a recorded measurement.
"""
from pathlib import Path
import json
import math
import statistics


def _read(root: Path, relative: str):
    return json.loads((root / relative).read_text())


def _same(actual: float, recorded: float) -> None:
    if not math.isclose(actual, recorded, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError(f"Summary differs from recorded samples: {actual} != {recorded}")


def _cubical(root: Path) -> dict:
    source = "docs/benchmarks/cubicalripser_v1/analysis.json"
    data = _read(root, source)
    records = data["records"]
    if len(records) != data["total"] or not all(r["verified"] for r in records):
        raise ValueError("Cubical report requires the full verified population")
    for record in records:
        for tool in ("tamerop", "cubicalripser"):
            timings = record["tools"][tool]
            for process in timings["passes"]:
                _same(statistics.median(process["samples"]), process["seconds"])
            _same(statistics.median(p["seconds"] for p in timings["passes"]),
                  timings["seconds"])
        by_tool = {
            tool: {p["pass_id"]: p["seconds"] for p in record["tools"][tool]["passes"]}
            for tool in ("tamerop", "cubicalripser")
        }
        if by_tool["tamerop"].keys() != by_tool["cubicalripser"].keys():
            raise ValueError("Unpaired process timings")
        _same(statistics.geometric_mean(
            by_tool["cubicalripser"][p] / by_tool["tamerop"][p]
            for p in by_tool["tamerop"]), record["ratio"])
    _same(statistics.geometric_mean(r["ratio"] for r in records), data["balanced_ratio"])

    ratio_rows = []
    for group in data["groups"]:
        matching = [r for r in records if all(
            r[k] == group[k] for k in ("dimension", "convention", "pattern"))]
        if len(matching) != 4:
            raise ValueError("Expected four requests per cubical family")
        value = statistics.geometric_mean(r["ratio"] for r in matching)
        _same(value, group["ratio"])
        convention = "vertices" if group["convention"] == "V" else "top cells"
        ratio_rows.append({
            "label": f"{group['dimension']}D {convention}, {group['pattern']}",
            "value": value,
            "case_ratios": [r["ratio"] for r in matching],
        })

    selected = ["2d_V_noise_size3", "2d_V_smooth_size3"] + [
        f"3d_{convention}_{pattern}_size3"
        for pattern in ("noise", "binary", "smooth")
        for convention in ("V", "T")
    ]
    by_id = {r["id"]: r for r in records}
    time_rows = []
    for case_id in selected:
        record = by_id[case_id]
        convention = "vertices" if record["convention"] == "V" else "top cells"
        shape = " × ".join(map(str, record["shape"]))
        time_rows.append({
            "label": f"{record['pattern'].capitalize()}, {convention} ({shape})",
            "tamerop_seconds": record["tools"]["tamerop"]["seconds"],
            "comparator_seconds": record["tools"]["cubicalripser"]["seconds"],
            "case_id": case_id,
        })
    return {
        "id": "cubicalripser", "comparator": "CubicalRipser",
        "timing_label": "Loaded array to complete barcode, after compilation",
        "ratio_rows": ratio_rows,
        "interval_label": "Family geometric means; four equally weighted requests each",
        "time_rows": time_rows,
        "aggregate_ratio": data["balanced_ratio"],
        "practical_band": [1 / 1.1, 1.1],
        "sources": [source, "docs/benchmarks/cubicalripser_v1/samples.json",
                    "docs/benchmarks/cubicalripser_v1/formal_manifest.json"],
    }


def _visual(root: Path) -> dict:
    source = "docs/benchmarks/visual_interaction_v1/measurements.json"
    data = _read(root, source)
    labels = {
        "continuous": "Ring, 49 cells",
        "continuous-large": "Image, 2,601 cells",
        "continuous-slices": "Two squares, new line restrictions",
    }
    rows = []
    for sample in data["samples"]:
        values = sample.get("warmMs", sample.get("warmDistinctLinesMs"))
        median = statistics.median(values)
        p95 = sorted(values)[math.ceil(0.95 * len(values)) - 1]
        _same(median, sample["medianMs"])
        _same(p95, sample["p95Ms"])
        rows.append({
            "label": labels[sample["route"]], "median_ms": median,
            "p95_ms": p95, "samples_ms": values,
            "first_ms": sample.get("firstQueryMs", sample.get("firstSliceQueryMs")),
        })
    return {
        "id": "visual_interaction", "type": "latency", "comparator": None,
        "timing_label": "Browser input to committed picture after first use",
        "latency_rows": rows,
        "interval_label": "Observed median and nearest-rank 95th percentile",
        "sources": [source, "docs/benchmarks/visual_interaction_v1/machine.json"],
    }


def build_data(root: Path) -> list[dict]:
    """Return summaries recomputed from the retained process and browser samples."""
    root = Path(root)
    return [_cubical(root), _visual(root)]
