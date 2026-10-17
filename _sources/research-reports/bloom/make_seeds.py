#!/usr/bin/env python3
"""Rewrite every seed-*.yaml in a Bloom workspace for a new evaluator/judge and target.

Usage: make_seeds.py <workspace> <target_id> [--evaluator <id>]

Line-based edit: inside the top-level sections understanding / ideation / rollout /
judgment, the indented `model:` value becomes the evaluator id; inside rollout, the
`target:` value becomes the target id. Everything else stays byte-identical.
Fails (no file written) if any seed does not end up with exactly 4 model keys and 1 target.
"""
import re
import sys
from pathlib import Path

DEFAULT_EVALUATOR = "openrouter/qwen/qwen3-235b-a22b-2507"
SECTIONS = {"understanding", "ideation", "rollout", "judgment"}
SECTION_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(#.*)?$")
KEY_RE = re.compile(r'^(\s+)(model|target):(\s*)("[^"]*"|\'[^\']*\'|\S+)(.*)$')


def rewrite(text: str, evaluator: str, target: str) -> tuple[str, int, int]:
    out, section, n_model, n_target = [], None, 0, 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        nl = line[len(body):]
        m = SECTION_RE.match(body)
        if m:
            section = m.group(1)
        elif body and not body[0].isspace() and not body.startswith("#"):
            section = None
        k = KEY_RE.match(body)
        if k and section in SECTIONS:
            indent, key, sp, _old, rest = k.groups()
            if key == "model":
                body = f'{indent}model:{sp}"{evaluator}"{rest}'
                n_model += 1
            elif key == "target" and section == "rollout":
                body = f'{indent}target:{sp}"{target}"{rest}'
                n_target += 1
        out.append(body + nl)
    return "".join(out), n_model, n_target


def main() -> None:
    args = sys.argv[1:]
    evaluator = DEFAULT_EVALUATOR
    if "--evaluator" in args:
        i = args.index("--evaluator")
        evaluator = args[i + 1]
        del args[i : i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    workspace, target = Path(args[0]), args[1]
    seeds = sorted((workspace / "bloom-data").glob("seed-*.yaml"))
    if not seeds:
        sys.exit(f"no seed-*.yaml under {workspace}/bloom-data")
    results = {}
    for p in seeds:
        new, nm, nt = rewrite(p.read_text(encoding="utf-8"), evaluator, target)
        if nm != 4 or nt != 1:
            sys.exit(f"{p.name}: found {nm} model keys and {nt} target keys; nothing written")
        results[p] = new
    for p, new in results.items():
        p.write_text(new, encoding="utf-8")
        print(f"rewrote {p}")


if __name__ == "__main__":
    main()
