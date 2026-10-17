# Reproduce it

The framework, the prompts and every response and judgment are public.

- **Code:** [github.com/robertbarcik/geobias](https://github.com/robertbarcik/geobias) (Python, Click CLI, async OpenRouter client, Jinja2 dashboard).
- **Data:** [github.com/robertbarcik/geobias-results](https://github.com/robertbarcik/geobias-results): one folder per run with `config.json`, the frozen `test_cases.json`, every model's responses, the consensus and per-evaluator judgments, the metrics, and the generated interactive dashboard (`geobias-report.html`).

```bash
git clone https://github.com/robertbarcik/geobias
cd geobias
python3 -m venv venv && source venv/bin/activate && pip install -e .
export OPENROUTER_API_KEY=...

python -m geobias models                                        # model groups and the evaluator panel
python -m geobias evaluate --group ext-2026-10 --dry-run        # call counts, no spend
python -m geobias evaluate --group ext-2026-10 --resume ./my-run   # reuse test_cases.json copied into ./my-run
python -m geobias report --input ./my-run                       # regenerate the dashboard
```

To compare with these results, copy `test_cases.json` from one of the published run folders into your run directory before starting, and keep the default evaluator panel. Responses are cached per model, so an interrupted run resumes; evaluations are re-requested on every run.

The figures in this report are built from the run folders by `_sources/research-reports/geobias/export_metrics.py` and `figures/build_figures.py` in the publications repository; the page by `_sources/research-reports/tools/build_report.py`. The archived March 2026 dashboard remains at [/reports/geobias-7b/](/reports/geobias-7b/).
