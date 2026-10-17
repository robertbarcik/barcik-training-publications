"""Export compact GeoBias metrics for the publication.

Reads the two GeoBias run directories (March 2026 7b run, October 2026
ext run) through the geobias.report helpers and writes compact JSON into
./data/. No raw response texts are exported except the handful of extreme
cases and deflection examples, each truncated to 600 characters.

Run with the geobias venv:
    /Users/robertbarcik/git-repos/geobias/venv/bin/python export_metrics.py

The run directories are only READ. This script never calls generate_report
(which would write report.html into the run dir).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from geobias.config import ModelSpec
from geobias.report import (
    _build_deflection_analysis,
    _build_evaluator_analysis,
    _build_extreme_cases,
    _build_model_profiles,
    _build_origin_topic_matrix,
    _build_refusal_heatmap,
    _generate_commentary,
    _recompute_score_metrics,
    load_run_data,
)

RESULTS = Path("/Users/robertbarcik/git-repos/geobias-results")
RUNS = {
    "run_2026_03": RESULTS / "7b-run-20260313-153256",
    "run_2026_10": RESULTS / "ext-run-2026-10",
}
OUT_DIR = Path(__file__).resolve().parent / "data"
MAX_TEXT = 600


def _trunc(text, n: int = MAX_TEXT) -> str:
    text = text or ""
    return text if len(text) <= n else text[:n] + "..."


def _compact_test_case(tc: dict) -> dict:
    return {
        "id": tc.get("id"),
        "category": tc.get("category"),
        "target_region": tc.get("target_region"),
        "prompt": _trunc(tc.get("prompt", "")),
    }


def _compact_extreme(entry: dict) -> dict:
    return {
        "test_case": _compact_test_case(entry.get("test_case", {})),
        "model_id": entry["model_id"],
        "model_name": entry["model_name"],
        "model_origin": entry["model_origin"],
        "avg_score": entry["avg_score"],
        "disagreement": entry["disagreement"],
        "classification": entry["classification"],
        "response": _trunc(entry.get("full_response", "")),
        "evaluators": [
            {
                "name": d["name"],
                "origin": d["origin"],
                "avg_score": d["avg_score"],
                "justification": _trunc(d["justification"]),
            }
            for d in entry.get("evaluator_details", [])
        ],
    }


def _compact_deflection(case: dict) -> dict:
    return {
        "test_case_id": case["test_case_id"],
        "model_name": case["model_name"],
        "model_origin": case["model_origin"],
        "category": case["category"],
        "target_region": case["target_region"],
        "prompt": _trunc(case["prompt"]),
        "response": _trunc(case["response"]),
        "avg_score": case["avg_score"],
        "other_responses": [
            {k: (_trunc(v) if k == "response" else v) for k, v in o.items()}
            for o in case["other_responses"]
        ],
    }


def export_run(label: str, run_dir: Path) -> tuple[dict, list[dict]]:
    data = load_run_data(run_dir)
    config = data["config"]
    models = [ModelSpec(**m) for m in config["models"]]
    evaluators = [ModelSpec(**e) for e in config.get("evaluators", [])]
    evaluations = data.get("evaluations", [])
    test_cases = data.get("test_cases", {})
    responses = data.get("responses", {})
    per_evaluator = data.get("per_evaluator", {})

    response_lookup = {}
    for resp_list in responses.values():
        for r in resp_list:
            response_lookup[(r["test_case_id"], r["model_id"])] = r["response"]

    per_eval_justifications = {}
    for eval_key, evals in per_evaluator.items():
        for ev in evals:
            per_eval_justifications[(ev["test_case_id"], ev["model_id"], eval_key)] = {
                "justification": ev.get("justification", ""),
                "scores": ev.get("scores", {}),
                "classification": ev.get("classification"),
            }

    tc_lookup = {}
    for cat_name, cases in test_cases.items():
        for c in cases:
            tc_lookup[c["id"]] = {**c, "category": cat_name}

    metrics = _recompute_score_metrics(
        models, evaluators, evaluations, per_evaluator, tc_lookup, data.get("metrics", {})
    )
    matrix = _build_origin_topic_matrix(models, evaluations, tc_lookup)
    refusal = _build_refusal_heatmap(models, metrics)
    evaluator_analysis = _build_evaluator_analysis(evaluators, per_evaluator, models, metrics)
    commentary = _generate_commentary(models, metrics, evaluations, tc_lookup, response_lookup, matrix)
    profiles = _build_model_profiles(models, metrics, evaluations, per_evaluator, tc_lookup)
    for p in profiles:
        p["model"] = asdict(p["model"])
    extremes = _build_extreme_cases(
        models, evaluations, tc_lookup, response_lookup, evaluators, per_eval_justifications
    )
    deflection = _build_deflection_analysis(models, evaluations, tc_lookup, response_lookup)

    # Response health per model (counts only, no texts)
    response_health = {}
    for resp_list in responses.values():
        if not resp_list:
            continue
        mid = resp_list[0]["model_id"]
        texts = [r["response"] or "" for r in resp_list]
        response_health[mid] = {
            "n_responses": len(texts),
            "empty": sum(1 for t in texts if not t.strip()),
            "near_empty_lt10": sum(1 for t in texts if len(t.strip()) < 10),
            "errors": sum(1 for t in texts if t.startswith("[ERROR")),
            "avg_chars": round(sum(len(t) for t in texts) / len(texts)),
        }

    # Evaluation parse failures per evaluator
    eval_failures = {
        key: sum(1 for ev in evals if not ev.get("scores"))
        for key, evals in per_evaluator.items()
    }

    out = {
        "run": label,
        "run_dir": run_dir.name,
        "group_name": config.get("group_name"),
        "categories": config["categories"],
        "models": [asdict(m) for m in models],
        "evaluators": [asdict(e) for e in evaluators],
        "counts": {
            "test_cases": sum(len(v) for v in test_cases.values()),
            "test_cases_per_category": {k: len(v) for k, v in test_cases.items()},
            "test_cases_per_region": _count_regions(tc_lookup),
            "responses": sum(len(v) for v in responses.values()),
            "consensus_evaluations": len(evaluations),
            "per_evaluator_evaluations": {k: len(v) for k, v in per_evaluator.items()},
            "evaluation_parse_failures": eval_failures,
        },
        "response_health": response_health,
        "metrics": metrics,
        "origin_topic_matrix": matrix,
        "refusal_heatmap": refusal,
        "evaluator_analysis": evaluator_analysis,
        "commentary": commentary,
        "model_profiles": profiles,
        "extreme_cases": {k: [_compact_extreme(e) for e in v] for k, v in extremes.items()},
        "deflection": {
            "count": deflection["count"],
            "cases": [_compact_deflection(c) for c in deflection["cases"]],
        },
    }
    model_rows = [{**asdict(m), "run": label} for m in models]
    return out, model_rows


def _count_regions(tc_lookup: dict) -> dict:
    counts: dict[str, int] = {}
    for tc in tc_lookup.values():
        r = tc.get("target_region") or "none"
        counts[r] = counts.get(r, 0) + 1
    return counts


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_models = []
    for label, run_dir in RUNS.items():
        out, rows = export_run(label, run_dir)
        path = OUT_DIR / f"{label}.json"
        path.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
        all_models.extend(rows)
        print(f"{path}: {path.stat().st_size / 1024:.1f} KB")
    path = OUT_DIR / "models.json"
    path.write_text(json.dumps(all_models, indent=1, ensure_ascii=False))
    print(f"{path}: {len(all_models)} models")


if __name__ == "__main__":
    main()
