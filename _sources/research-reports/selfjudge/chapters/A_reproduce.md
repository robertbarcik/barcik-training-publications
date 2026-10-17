# Reproduce it

The framework and all results are public.

- **Code:** [github.com/robertbarcik/selfjudge](https://github.com/robertbarcik/selfjudge) (Python, Click CLI, async OpenRouter client, Jinja2 report).
- **Data:** [github.com/robertbarcik/selfjudge-results](https://github.com/robertbarcik/selfjudge-results): one folder per model with every intermediate JSON (responses, ground truth, self, anchor and cross judgments, meta-judge reviews, metrics), the shared test cases with the planted anchors, and the archived March 2026 run.

```bash
git clone https://github.com/robertbarcik/selfjudge
cd selfjudge
uv venv --python 3.12 venv && source venv/bin/activate && uv pip install -e .
export OPENROUTER_API_KEY=...

python -m selfjudge evaluate --preset small-all --dry-run        # the July 2026 set
python -m selfjudge evaluate --preset small-ext-2026-10          # the October 2026 extension
python -m selfjudge evaluate --model qwen/qwen3.5-9b             # one model, comparable if shared/test_cases.json exists
python -m selfjudge report-all                                   # one report.html across every run in the results dir
```

Runs resume from the last saved step. The shared test cases are generated once; delete `shared/test_cases.json` to force a fresh set, which breaks comparability with everything before it. A full 14-model run cost under four dollars of API credit in July 2026.

The figures in this report are built from the `metrics.json` files by `_sources/research-reports/selfjudge/figures/build_figures.py` in the publications repository; the page itself by `_sources/research-reports/tools/build_report.py`.
