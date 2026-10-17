#!/usr/bin/env python3
"""Copy the SelfJudge metrics into this report's data/ folder (compact, no per-case transcripts).

    ~/git-repos/selfjudge/venv/bin/python _sources/research-reports/selfjudge/collect_data.py   (needs 3.10+: config.py syntax)

Reads  ~/git-repos/selfjudge-results/<model>/metrics.json   (skips shared/ and archive/)
       ~/git-repos/selfjudge/src/selfjudge/config.py        (roster: sizes, release months, flags)
Writes data/metrics/<model-dir>.json  and  data/models.json
"""
import glob
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.expanduser("~/git-repos/selfjudge-results")
CONFIG = os.path.expanduser("~/git-repos/selfjudge/src/selfjudge/config.py")

spec = importlib.util.spec_from_file_location("sj_config", CONFIG)
cfg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cfg)

roster = {}
for preset, models in cfg.SMALL_MODEL_PRESETS.items():
    run = "2026-07" if preset == "small-all" else "2026-10"
    for m in models:
        roster[m["id"]] = dict(m, run=run)

os.makedirs(os.path.join(HERE, "data", "metrics"), exist_ok=True)
kept, out_models = 0, []
for path in sorted(glob.glob(os.path.join(RESULTS, "*", "metrics.json"))):
    d = os.path.basename(os.path.dirname(path))
    if d in ("shared", "archive"):
        continue
    with open(path, encoding="utf-8") as fh:
        m = json.load(fh)
    for cat in m.get("categories", {}).values():
        cat.pop("cases", None)
        cat.pop("calibration", None)
    r = roster.get(m["model_id"], {})
    m["release"] = m.get("release") or r.get("release")
    m["closed"] = bool(r.get("closed"))
    m["note"] = r.get("note")
    m["run"] = r.get("run", "unknown")
    with open(os.path.join(HERE, "data", "metrics", d + ".json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1)
    kept += 1
    out_models.append({
        "dir": d, "id": m["model_id"], "display_name": m["display_name"], "params_b": m.get("params_b"),
        "total_params_b": m.get("total_params_b"), "moe": bool(m.get("moe")), "release": m["release"],
        "closed": m["closed"], "note": m["note"], "run": m["run"],
        "anchor_accuracy": m["overall"].get("anchors", {}).get("accuracy"),
        "self_accuracy": m["overall"].get("accuracy"),
        "self_leniency": m["overall"].get("self_leniency"),
        "self_preference": (m.get("cross") or {}).get("self_preference"),
        "peer": (m.get("cross") or {}).get("peer_display_name"),
        "n_own_fail": m["overall"].get("n_gt_fail"),
        "n_own_pass": m["overall"].get("n_gt_pass"),
        "own_failure_miss_rate": m["overall"].get("own_failure_miss_rate"),
        "anchor_failure_miss_rate": m["overall"].get("anchor_failure_miss_rate"),
    })
with open(os.path.join(HERE, "data", "models.json"), "w", encoding="utf-8") as fh:
    json.dump(sorted(out_models, key=lambda x: (x["params_b"] is None, x["params_b"] or 0)), fh, indent=1)
print(f"copied {kept} metrics files; roster entries without results: "
      f"{sorted(set(roster) - {m['id'] for m in out_models})}")
