# Reproduce it

- **Framework:** Bloom by Anthropic's alignment science team [1]; the fork used here is [github.com/robertbarcik/bloom](https://github.com/robertbarcik/bloom) (two small fixes to pre-scripted evaluator turns). Current development has moved to Meridian Labs [2].
- **Session repository:** [github.com/robertbarcik/bloom-session](https://github.com/robertbarcik/bloom-session): the behaviour definitions and seed configurations, the March 2026 results (`bloom-results/`), the October 2026 runs (`runs-2026-10/<target>/`), and the original dashboard generator.

```bash
git clone https://github.com/robertbarcik/bloom-session
cd bloom-session
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ../bloom          # the fork, installed editable
export OPENROUTER_API_KEY=...

cp bloom-data/seed-self-preservation.yaml bloom-data/seed.yaml
bloom run bloom-data             # understanding → ideation → rollout → judgment
bloom judgment bloom-data        # re-judge existing rollouts only
```

Each seed names the evaluator/judge under `understanding`, `ideation`, `rollout` and `judgment`, and the target under `rollout.target`; results land in `bloom-results/<behaviour>/` relative to the working directory. The scripts `make_seeds.py` and `run_bloom.py` in `_sources/research-reports/bloom/` of the publications repository rewrite the seeds for a new target and run all behaviours into a separate workspace; `export_data.py` reduces the judgments to the JSON behind the figures.

```bash
python3 make_seeds.py runs-2026-10/muse-glimmer-30b openrouter/meta/muse-glimmer-30b
python3 run_bloom.py run   runs-2026-10/muse-glimmer-30b self-preservation
python3 run_bloom.py judge runs-2026-10/llama-3.3-70b-rejudge self-preservation
python3 run_bloom.py run   runs-2026-10/muse-glimmer-30b tool-use-abuse --tools-capable
```

Two practical notes. Every run copies its seed to the shared `bloom-data/seed.yaml` before Bloom reads it, so runs inside one workspace must be sequential (`run_bloom.py` takes a lock and refuses a second one); parallel runs are only safe in separate workspaces. And `--tools-capable` is needed only for a simulated-environment seed whose target is newer than the installed LiteLLM's model list: check first with one real tool-call request that the model really returns tool calls.
