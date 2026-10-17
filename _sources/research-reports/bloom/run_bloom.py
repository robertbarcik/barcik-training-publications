#!/usr/bin/env python3
"""Run Bloom for one behaviour inside a workspace without changing the caller's cwd.

Usage:
  run_bloom.py run   <workspace> <behaviour>   # full pipeline (bloom run bloom-data)
  run_bloom.py judge <workspace> <behaviour>   # judgment only (bloom judgment bloom-data)
  add --tools-capable to register the seed's target as function-calling capable with litellm
  (needed for simenv seeds whose target is newer than the installed litellm registry)

Copies bloom-data/seed-<file>.yaml to bloom-data/seed.yaml, then runs Bloom with
cwd=<workspace>, logging to <workspace>/logs/<behaviour>[.judge].log.
Runs in the SAME workspace must be sequential (enforced by a lock file); parallelism is
only safe across different workspaces.
OPENROUTER_API_KEY is read from selfjudge/.env (the verified key) and passed only via
the child environment.
"""
import fcntl
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

BLOOM = "/Users/robertbarcik/git-repos/bloom-session/.venv/bin/bloom"
KEY_ENV = Path("/Users/robertbarcik/git-repos/selfjudge/.env")

SEEDS = {  # behaviour name -> seed file (table in bloom-session/CLAUDE.md)
    "emotional-bond": "seed-emotional-bond.yaml",
    "social-engineering-assistance": "seed-social-engineering.yaml",
    "self-preservation": "seed-self-preservation.yaml",
    "corrigibility-resistance": "seed-corrigibility.yaml",
    "covert-goal-pursuit": "seed-covert-goals.yaml",
    "authority-compliance": "seed-authority.yaml",
    "dangerous-confirmation-bias": "seed-confirmation.yaml",
    "delusion-sycophancy": "seed-delusion-sycophancy.yaml",
    "information-leakage-under-pressure": "seed-info-leak.yaml",
    "tool-use-abuse": "seed-tool-abuse.yaml",
    "human-life-deprioritization": "seed-human-life.yaml",
}


def read_key() -> str:
    for line in KEY_ENV.read_text().splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:]
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("'\"")
    sys.exit("OPENROUTER_API_KEY not found")


def main() -> None:
    argv = sys.argv[1:]
    tools_capable = "--tools-capable" in argv
    argv = [a for a in argv if a != "--tools-capable"]
    if len(argv) != 3 or argv[0] not in ("run", "judge"):
        sys.exit(__doc__)
    mode, workspace, behaviour = argv[0], Path(argv[1]).resolve(), argv[2]
    if behaviour not in SEEDS:
        sys.exit(f"unknown behaviour {behaviour}; known: {', '.join(SEEDS)}")
    if "bloom-session/bloom-results" in str(workspace) or workspace == Path("/Users/robertbarcik/git-repos/bloom-session"):
        sys.exit("refusing to run in the read-only original workspace")
    data = workspace / "bloom-data"
    # One run per workspace at a time: every run rewrites the shared bloom-data/seed.yaml,
    # so two parallel runs in one workspace would race and run the wrong behaviour.
    lock_fh = open(workspace / ".run_bloom.lock", "w")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another run_bloom.py is active in {workspace}; run sequentially")
    shutil.copyfile(data / SEEDS[behaviour], data / "seed.yaml")
    logs = workspace / "logs"
    logs.mkdir(exist_ok=True)
    log = logs / f"{behaviour}{'.judge' if mode == 'judge' else ''}.log"
    cmd = [BLOOM, "run" if mode == "run" else "judgment", "bloom-data"]
    if tools_capable:
        # Bloom's simenv pre-check asks litellm's model registry (plus a name whitelist in the
        # fork) whether the target supports function calling. Models newer than the installed
        # litellm are unknown there. Register the target as tool-capable in the child process
        # only (verify first with a real tool-call request), then start Bloom's own CLI.
        target = next(
            (ln.split(":", 1)[1].strip().strip("'\"") for ln in (data / "seed.yaml").read_text().splitlines()
             if ln.strip().startswith("target:")), None)
        boot = (
            "import sys, litellm\n"
            f"litellm.register_model({{{target!r}: {{'litellm_provider': 'openrouter', 'mode': 'chat', "
            "'supports_function_calling': True}})\n"
            "from bloom.cli import main\n"
            f"sys.argv = ['bloom'] + {cmd[1:]!r}\n"
            "sys.exit(main())\n"
        )
        cmd = [str(Path(BLOOM).parent / "python3.12"), "-c", boot]
    env = dict(os.environ, OPENROUTER_API_KEY=read_key())
    t0 = time.time()
    with open(log, "a") as fh:
        fh.write(f"\n===== {time.strftime('%Y-%m-%d %H:%M:%S')} {' '.join(cmd)} (cwd={workspace})\n")
        fh.flush()
        rc = subprocess.run(cmd, cwd=workspace, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
        fh.write(f"===== exit {rc} after {time.time() - t0:.0f}s\n")
    print(f"{mode} {behaviour}: exit {rc} in {time.time() - t0:.0f}s, log {log}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
