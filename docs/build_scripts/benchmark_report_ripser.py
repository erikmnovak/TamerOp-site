"""Read the archived Rips comparisons for the shared benchmark figures."""

import json
from pathlib import Path


def build_data(root: Path) -> list[dict]:
    """Return report figures without changing the archived measurements."""
    py_source = "docs/benchmarks/ripser_v1/summary.json"
    cpp_source = "docs/benchmarks/ripser_cpp_v1/summary.json"
    py = json.loads((root / py_source).read_text())
    cpp = json.loads((root / cpp_source).read_text())
    families = {
        "cloud": "Euclidean clouds",
        "dense": "Supplied dense distances",
        "sparse": "Supplied sparse distances",
        "weighted": "Weighted vertices",
        "landmark": "Landmark selection",
        "control": "Small controls",
    }
    py_examples = [
        ("dense_circle1024_f2", "Circle distances: 1,024 points"),
        ("dense_planar512_f101", "Planar distances: 512 points"),
        ("cloud_sphere128_f101", "Sphere cloud: 128 points"),
        ("sparse_grid64_f2", "Sparse grid: 4,096 vertices"),
        ("weighted_grid64_f2", "Weighted grid: 4,096 vertices"),
        ("landmark_2048_128_f2", "Landmarks: 128 of 2,048 points"),
        ("control_sphere3_f2", "3-sphere control: 8 vertices"),
    ]
    py_cases = {row["id"]: row for row in py["cases"]}
    cpp_examples = [
        ("circle_1408_f2", "Circle: 1,408 vertices, F₂"),
        ("planar_1152_f2", "Planar: 1,152 vertices, F₂"),
        ("planar_1152_f101", "Planar: 1,152 vertices, F₁₀₁"),
        ("sphere_512_f3", "Sphere: 512 vertices, F₃"),
        ("sparse_sphere_704_f2", "Sparse sphere: 704 vertices, F₂"),
    ]
    cpp_cases = {row["id"]: row for row in cpp}
    cpp_families = {
        "circle": "Circle",
        "planar": "Planar",
        "sphere": "Sphere",
        "sparse_sphere": "Sparse sphere",
    }
    return [
        {
            "id": "ripser",
            "comparator": "Ripser.py",
            "timing_label": "Complete query from native inputs",
            "ratio_rows": [
                {
                    "label": families[row["family"]],
                    "value": row["ratio_seconds"],
                    "low": row["ratio_seconds_pass_range"][0],
                    "high": row["ratio_seconds_pass_range"][1],
                }
                for row in py["development_families"]
            ],
            "interval_label": "Range across four paired process passes",
            "time_rows": [
                {
                    "label": label,
                    "tamerop_seconds": py_cases[case_id]["tamerop_seconds"],
                    "comparator_seconds": py_cases[case_id]["ripser_seconds"],
                }
                for case_id, label in py_examples
            ],
            "sources": [py_source],
        },
        {
            "id": "ripser_cpp",
            "comparator": "C++ Ripser",
            "timing_label": "Distance file to complete barcode output",
            "ratio_rows": [
                {
                    "label": f"{cpp_families[row['family']]}: {row['n']:,}, F{row['prime']}",
                    "value": row["ratio"],
                    "low": row["ratio_min"],
                    "high": row["ratio_max"],
                }
                for row in cpp
            ],
            "interval_label": "Range across three paired process passes",
            "time_rows": [
                {
                    "label": label,
                    "tamerop_seconds": cpp_cases[case_id]["tamerop_seconds"],
                    "comparator_seconds": cpp_cases[case_id]["cpp_seconds"],
                }
                for case_id, label in cpp_examples
            ],
            "sources": [cpp_source],
        },
    ]
