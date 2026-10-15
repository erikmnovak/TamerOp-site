"""Read the sealed QPA and PHAT measurements for the common report figures.

The displayed aggregates retain each study's declared weights. Absolute times
are medians of case times; they are deliberately separate from paired ratios.
No benchmark is run and no archived result is modified here.
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import median


def _read(root: Path, relative: str):
    return json.loads((root / relative).read_text())


def _ratio(label: str, item: dict, interval_key: str) -> dict:
    low, high = item[interval_key]
    return {"label": label, "value": item["ratio"], "low": low, "high": high}


def build_data(root: Path) -> list[dict]:
    """Return figure inputs, with ``root`` the website repository directory."""
    qpa_base = "docs/benchmarks/qpa_v1"
    qpa_sources = [f"{qpa_base}/{name}" for name in
                   ("results.json", "observations.json", "provenance.json")]
    qpa = _read(root, qpa_sources[0])
    qpa_rows = [r for r in _read(root, qpa_sources[1])
                if r["phase"] == "construction_and_query"]
    qpa_matched = [r for r in qpa_rows if r["mathematically_matched"]]
    if len(qpa_rows) != 220 or len(qpa_matched) != 200:
        raise ValueError("QPA figures require the fixed 220 requests and 200 matched pairs")
    qpa_labels = [
        ("Q1", "Hom basis"), ("Q2", "Ext¹ dimension"),
        ("Q3", "Complete Hom/Ext"), ("Q4", "Kernel, image, cokernel"),
        ("Q5", "Resolutions"), ("Q6", "Pushouts and pullbacks"),
        ("Q7", "Homology and mapping cones"), ("Q8", "Yoneda products"),
        ("Q9", "Induced Ext maps"),
    ]
    qpa_ratio_rows = [_ratio("All completed comparisons",
                             qpa["completed_pair_aggregate"], "interval95")]
    qpa_ratio_rows += [_ratio(label, qpa["by_workflow"][key], "interval95")
                      for key, label in qpa_labels]
    qpa_time_rows = []
    for key, label in qpa_labels:
        if key == "Q3":
            continue
        selected = [r for r in qpa_matched if r["workflow"] == key]
        qpa_time_rows.append({
            "label": label,
            "tamerop_seconds": median(r["TamerOp"]["median_seconds"] for r in selected),
            "comparator_seconds": median(r["QPA"]["median_seconds"] for r in selected),
            "cases": len(selected),
        })
    qpa_data = {
        "id": "qpa", "comparator": "QPA",
        "timing_label": "Native construction and complete query",
        "ratio_rows": qpa_ratio_rows,
        "interval_label": "95% intervals across five paired process passes",
        "time_rows": qpa_time_rows, "sources": qpa_sources,
        "ratio_basis": "Declared area/request/field weights; 200 completed pairs",
        "time_basis": "Median of case times within each request group; each case time is the median of five process medians",
        "time_selection": "Eight request groups; combined Hom/Ext and incomplete tensor comparison remain in the report table",
        "planned_cases": 220, "matched_cases": 200,
        "missing_comparisons": {"Balanced tensor and evaluations": 20},
    }

    phat_base = "docs/benchmarks/phat_v2"
    phat_sources = [f"{phat_base}/{name}" for name in
                    ("results.json", "observations.json", "provenance.json")]
    phat = _read(root, phat_sources[0])
    phat_rows = [r for r in _read(root, phat_sources[1]) if r["phase"] == "combined"]
    if len(phat_rows) != 48:
        raise ValueError("PHAT figures require the fixed 48 complete requests")
    phat_labels = [("graph", "Graphs"), ("simplicial", "Simplicial inputs"),
                   ("cubical", "Cubical grids"), ("algebraic", "Algebraic controls")]
    phat_ratio_rows = [_ratio("All comparisons", phat["coverage"]["aggregate"], "ci95")]
    phat_ratio_rows += [_ratio(label, phat["coverage"]["families"][key]["timing"], "ci95")
                       for key, label in phat_labels]
    phat_time_rows = []
    for key, label in phat_labels:
        selected = [r for r in phat_rows if r["family"] == key]
        if len(selected) != 12:
            raise ValueError(f"PHAT family {key} must retain all twelve inputs")
        phat_time_rows.append({
            "label": label,
            "tamerop_seconds": median(r["tamerop_seconds"] for r in selected),
            "comparator_seconds": median(r["phat_seconds"] for r in selected),
            "cases": len(selected),
        })
    phat_data = {
        "id": "phat", "comparator": "PHAT",
        "timing_label": "Native construction and complete barcode query",
        "ratio_rows": phat_ratio_rows,
        "interval_label": "95% intervals across five paired process passes",
        "time_rows": phat_time_rows, "sources": phat_sources,
        "ratio_basis": "Equal weight for families, variants and sizes",
        "time_basis": "Median of twelve case times per family; each case time is the median of five process medians",
        "time_selection": "All four families, with all twelve inputs in each family",
        "planned_cases": 48, "matched_cases": 48,
    }
    return [qpa_data, phat_data]
