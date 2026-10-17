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

# Public release month per subject model (YYYY-MM). Sources: the SelfJudge report's
# models.json for the models shared with it, OpenRouter listing dates otherwise
# (Llama 3.1 8B 2024-07, DeepSeek V4.1 Flash 2026-09), vendor announcement for
# Phi-4 (2024-12) and Qwen3 8B (2025-04, Qwen3 family launch).
RELEASE = {
    "qwen/qwen3-8b": "2025-04",
    "qwen/qwen3.5-9b": "2026-02",
    "meta-llama/llama-3.1-8b-instruct": "2024-07",
    "microsoft/phi-4": "2024-12",
    "mistralai/ministral-8b-2512": "2025-12",
    "qwen/qwen3.8-27b": "2026-08",
    "deepseek/deepseek-v4.1-flash": "2026-09",
    "ibm-granite/granite-4.2-8b": "2026-08",
    "nvidia/nemotron-3.5-lightning": "2026-08",
    "meta/muse-glimmer-30b": "2026-08",
    "mistralai/ministral-14b-2512": "2025-12",
}
MOE = {"deepseek/deepseek-v4.1-flash", "nvidia/nemotron-3.5-lightning"}
CORE = ("CN", "US", "EU")


def _mean(xs):
    return round(sum(xs) / len(xs), 2) if xs else None


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
            "max_completion_tokens": max(((r.get("usage") or {}).get("completion_tokens") or 0) for r in resp_list),
            "at_2048_tokens": sum(1 for r in resp_list if ((r.get("usage") or {}).get("completion_tokens") or 0) == 2048),
            "at_16384_tokens": sum(1 for r in resp_list if ((r.get("usage") or {}).get("completion_tokens") or 0) == 16384),
        }

    # Residual empty responses (no visible answer) with their thinking-token count
    from geobias.categories.base import numeric_scores
    empty_rows = {}
    empty_keys = set()
    for resp_list in responses.values():
        for r in resp_list:
            if not (r["response"] or "").strip():
                ct = (r.get("usage") or {}).get("completion_tokens")
                empty_rows.setdefault(r["model_id"], []).append({
                    "test_case_id": r["test_case_id"],
                    "category": tc_lookup.get(r["test_case_id"], {}).get("category"),
                    "target_region": tc_lookup.get(r["test_case_id"], {}).get("target_region"),
                    "completion_tokens": ct,
                })
                empty_keys.add((r["test_case_id"], r["model_id"]))

    # Scores with and without the empty-response rows (consensus evaluations)
    def _block(evs):
        out = {"all": _mean([s for e in evs for s in numeric_scores(e.get("scores", {}))]), "n": len(evs)}
        by_cat = {}
        for e in evs:
            by_cat.setdefault(tc_lookup.get(e["test_case_id"], {}).get("category"), []).append(e)
        out["by_category"] = {c: _mean([s for e in v for s in numeric_scores(e.get("scores", {}))]) for c, v in by_cat.items()}
        own = [e for e in evs if tc_lookup.get(e["test_case_id"], {}).get("target_region") == origin_of[e["model_id"]]]
        oth = [e for e in evs if tc_lookup.get(e["test_case_id"], {}).get("target_region") in CORE
               and tc_lookup.get(e["test_case_id"], {}).get("target_region") != origin_of[e["model_id"]]]
        o1 = _mean([s for e in own for s in numeric_scores(e.get("scores", {}))])
        o2 = _mean([s for e in oth for s in numeric_scores(e.get("scores", {}))])
        out["asymmetry"] = {"own": o1, "other": o2, "own_n": len(own), "other_n": len(oth),
                            "asymmetry": round(o2 - o1, 2) if o1 is not None and o2 is not None else None}
        return out

    origin_of = {m.id: m.origin for m in models}
    with_without_empty = {}
    for mid in empty_rows:
        evs = [e for e in evaluations if e["model_id"] == mid]
        with_without_empty[mid] = {
            "with_empty": _block(evs),
            "without_empty": _block([e for e in evs if (e["test_case_id"], mid) not in empty_keys]),
        }

    # Subject origin x category and subject origin x target region (consensus means)
    origin_by_category, origin_by_region = {}, {}
    for e in evaluations:
        o = origin_of.get(e["model_id"])
        tc = tc_lookup.get(e["test_case_id"], {})
        sc = numeric_scores(e.get("scores", {}))
        origin_by_category.setdefault(o, {}).setdefault(tc.get("category"), []).extend(sc)
        origin_by_region.setdefault(o, {}).setdefault(tc.get("target_region") or "untagged", []).extend(sc)
    origin_by_category = {o: {c: _mean(v) for c, v in d.items()} for o, d in origin_by_category.items()}
    origin_by_region = {o: {c: _mean(v) for c, v in d.items()} for o, d in origin_by_region.items()}

    # Classification counts per model x category, and per model x target region
    # (refusal_asymmetry prompts only), from the consensus majority vote
    cls_by_category, cls_refusal_by_region = {}, {}
    for e in evaluations:
        tc = tc_lookup.get(e["test_case_id"], {})
        c = e.get("classification") or "unknown"
        d = cls_by_category.setdefault(e["model_id"], {}).setdefault(tc.get("category"), {})
        d[c] = d.get(c, 0) + 1
        if tc.get("category") == "refusal_asymmetry":
            d2 = cls_refusal_by_region.setdefault(e["model_id"], {}).setdefault(tc.get("target_region") or "untagged", {})
            d2[c] = d2.get(c, 0) + 1

    # Per-evaluator per-model means (for the leniency figure)
    per_eval_model = {}
    for key, evals in per_evaluator.items():
        acc = {}
        for ev in evals:
            acc.setdefault(ev["model_id"], []).extend(numeric_scores(ev.get("scores", {})))
        per_eval_model[key] = {mid: _mean(v) for mid, v in acc.items()}

    # Per-prompt consensus scores on the region-tagged prompts (the ones the asymmetry uses)
    region_prompt_scores = {}
    for e in evaluations:
        tc = tc_lookup.get(e["test_case_id"], {})
        if tc.get("target_region") not in CORE + ("neutral", "other"):
            continue
        row = region_prompt_scores.setdefault(e["test_case_id"], {
            "category": tc.get("category"), "target_region": tc.get("target_region"),
            "prompt": _trunc(tc.get("prompt", ""), 200), "scores": {}})
        row["scores"][e["model_id"]] = {"avg": _mean(numeric_scores(e.get("scores", {}))),
                                        "classification": e.get("classification")}

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
        "region_prompt_scores": region_prompt_scores,
        "empty_responses": empty_rows,
        "scores_with_without_empty": with_without_empty,
        "origin_by_category": origin_by_category,
        "origin_by_region": origin_by_region,
        "classification_by_category": cls_by_category,
        "refusal_classification_by_region": cls_refusal_by_region,
        "per_evaluator_model_means": per_eval_model,
        "deflection": {
            "count": deflection["count"],
            "cases": [_compact_deflection(c) for c in deflection["cases"]],
        },
    }
    model_rows = [{**asdict(m), "run": label, "release": RELEASE.get(m.id), "moe": m.id in MOE,
                   "avg_score": metrics.get("per_model", {}).get(m.id, {}).get("avg_score"),
                   "asymmetry": metrics.get("bias_asymmetry", {}).get(m.id, {}).get("asymmetry")}
                  for m in models]
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
