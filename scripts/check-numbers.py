#!/usr/bin/env python3
"""Every number this website publishes, against the artifact that produced it.

The front page says the numbers here are tied to the artifacts that produced
them and checked before publication. Until this file existed that was a promise,
which is exactly the distinction `hemo-verified/PROVENANCE.md` makes about
itself: a promise does not make a claim checkable, a check does.

So: fetch the attested reports from the repository that holds `ai-os`, render each declared
number the way the page renders it, and fail if the page does not contain it.
Declared explicitly rather than scraped, because the failure worth catching is a
page that quietly stops carrying a number, and a scraper cannot see an absence
it was never told to expect.

    python3 scripts/check-numbers.py            # against the working tree
    python3 scripts/check-numbers.py --ref main # pin the artifacts to a ref

Exit 0 if every declared claim resolves, 1 otherwise.

What it catches, and what it does not. It catches the failure this project has
actually had: an artifact moves and the pages do not — the gate count went from
26/125 to 28/135 and thirteen places kept saying the old one for six days. It
does **not** catch one mistyped occurrence among several, because the test is
whether the page contains the value anywhere, and `0.906` appearing correctly in
one sentence satisfies it while a second sentence says `0.912`. Saying so here
rather than letting the script look stronger than it is.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
# ai-os moved into `evolving-agents` as a subtree on 2026-09-06 and the old
# repository was archived. Archived repositories still serve raw content, which
# is the dangerous part: this script would have kept resolving every claim
# against a tree that can no longer change, and reported success while the page
# drifted from the artifacts that now produce it. That is the exact failure it
# was written to catch, running backwards.
RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/evolving-agents/{ref}/ai-os/{path}"

H0 = "projects/hemo-verified/gates/reports/h0.json"

# The front page is lora-kernel, and since 2026-09-19 it publishes numbers of its
# own. They live in another repository, in the results files the runs wrote.
LK_RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/lora-kernel/{ref}/{path}"
LK_CORPUS_MODE = "results/M7-arm0b-corpus-mode-20260919/corpus_mode.json"
LK_POOL = "results/M1-pool-qwen35-20260919/pool_base.json"


def fetch(path: str, ref: str, raw: str = RAW) -> dict:
    url = raw.format(ref=ref, path=path)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"could not read {url}: {e}", file=sys.stderr)
        print("The artifacts live under ai-os/ in the evolving-agents repository. Without them this "
              "script cannot check anything, and reporting success would be "
              "worse than reporting nothing.", file=sys.stderr)
        raise SystemExit(2)


def claims(h0: dict) -> list[tuple[str, str, str]]:
    """(page, rendered value, what it is) — the whole contract, in one place."""
    a = h0
    per = a["auc_per_oracle"]
    hemo = "hemo-verified/index.html"
    # Until 2026-09-06 the headline and the kill line appeared twice: on the
    # front page and on the detail page. The front page became lora-kernel and
    # the ai-os page was deleted, so hemo-verified is now the only page that
    # states them. One page stating a number once is still a checked claim; two
    # entries pointed at a page that does not exist would report MISSING, which
    # reads as a regression in the artifact rather than in the site.
    out: list[tuple[str, str, str]] = []

    out.append((hemo, f"{a['auc_composite']:.3f}", "H0 composite AUC"))
    out.append((hemo, str(a["kill_threshold"]), "the kill threshold"))

    # The detail page carries the panel, cell by cell. These are the numbers
    # that were wrong once — A5 and A6 transposed, A4 reading 0.706 — which is
    # why every one of them is named here rather than sampled.
    for oracle in ("A1", "A2", "A3", "A4", "A5", "A6", "A10"):
        out.append((hemo, f"{per[oracle]:.3f}", f"{oracle} alone"))

    out += [
        (hemo, str(a["n"]), "how many predictions"),
        (hemo, f"{a['bad_fraction'] * 100:.1f}%", "the bad fraction"),
        (hemo, f"{a['spearman_composite']:.3f}", "Spearman rho"),
        (hemo, f"{a['false_accept_rate'] * 100:.1f}%", "the false-accept rate"),
        (hemo, str(a["accepted"]), "ACCEPT count"),
        (hemo, str(a["escalated"]), "ESCALATE count"),
        (hemo, str(a["rejected"]), "REJECT count"),
        (hemo, a["environment"]["python"], "the python it ran on"),
        (hemo, a["environment"]["numpy"], "the numpy it ran on"),
        (hemo, a["environment"]["scipy"], "the scipy it ran on"),
    ]
    return out


def lora_kernel_claims(mode: dict, pool: dict) -> list[tuple[str, str, str]]:
    """The front page's numbers, each rendered the way the page renders it."""
    home = "index.html"
    pr = mode["pairs"][0]
    arms = pool["arms"]
    email, desk, base = arms["email-full"], arms["desk-commitment"], arms["base:email"]
    return [
        (home, f"{pr['a_total']}/{pr['n_paired']}", "the fluids expert in corpus mode"),
        (home, f"{pr['b_total']}/{pr['n_paired']}", "the same expert through tool_calls"),
        (home, f"{pr['only_a']}&nbsp;:&nbsp;{pr['only_b']}", "the discordant pairs"),
        (home, f"{email['correct']}/{email['n']}", "email-full on Qwen3.5-4B"),
        (home, f"{base['correct']}/{base['n']}", "the bare 4B on the same cases"),
        (home, f"{desk['correct']}/{desk['n']}", "desk-commitment on Qwen3.5-4B"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main", help="git ref to read the artifacts from")
    args = ap.parse_args()

    h0 = fetch(H0, args.ref)
    pages: dict[str, str] = {}
    bad = 0
    checked = 0

    # lora-kernel's own default branch is `main`; --ref pins evolving-agents only.
    lk = lora_kernel_claims(fetch(LK_CORPUS_MODE, "main", LK_RAW), fetch(LK_POOL, "main", LK_RAW))
    for page, value, what in claims(h0) + lk:
        if page not in pages:
            f = ROOT / page
            if not f.exists():
                print(f"MISSING PAGE {page}", file=sys.stderr)
                return 1
            pages[page] = f.read_text(encoding="utf-8")
        checked += 1
        if value not in pages[page]:
            print(f"STALE  {page}: {what} should read {value} — "
                  f"the page does not contain it", file=sys.stderr)
            bad += 1

    if bad:
        print(f"\n{bad} of {checked} claims no longer match the artifact they name.",
              file=sys.stderr)
        return 1
    print(f"site numbers: {checked} claim(s) resolved to the artifact they name")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
