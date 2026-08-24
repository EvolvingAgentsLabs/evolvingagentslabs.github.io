#!/usr/bin/env python3
"""Every number this website publishes, against the artifact that produced it.

The front page says the numbers here are tied to the artifacts that produced
them and checked before publication. Until this file existed that was a promise,
which is exactly the distinction `hemo-verified/PROVENANCE.md` makes about
itself: a promise does not make a claim checkable, a check does.

So: fetch the attested reports from the `ai-os` repository, render each declared
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
RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/ai-os/{ref}/{path}"

H0 = "projects/hemo-verified/gates/reports/h0.json"


def fetch(path: str, ref: str) -> dict:
    url = RAW.format(ref=ref, path=path)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"could not read {url}: {e}", file=sys.stderr)
        print("The artifacts live in the ai-os repository. Without them this "
              "script cannot check anything, and reporting success would be "
              "worse than reporting nothing.", file=sys.stderr)
        raise SystemExit(2)


def claims(h0: dict) -> list[tuple[str, str, str]]:
    """(page, rendered value, what it is) — the whole contract, in one place."""
    a = h0
    per = a["auc_per_oracle"]
    hemo = "hemo-verified/index.html"
    home = "index.html"
    out: list[tuple[str, str, str]] = []

    # Both pages carry the headline and the kill line.
    for page in (home, hemo):
        out.append((page, f"{a['auc_composite']:.3f}", "H0 composite AUC"))
        out.append((page, str(a["kill_threshold"]), "the kill threshold"))

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main", help="git ref to read the artifacts from")
    args = ap.parse_args()

    h0 = fetch(H0, args.ref)
    pages: dict[str, str] = {}
    bad = 0
    checked = 0

    for page, value, what in claims(h0):
        if page not in pages:
            f = ROOT / page
            if not f.exists():
                print(f"MISSING PAGE {page}", file=sys.stderr)
                return 1
            pages[page] = f.read_text(encoding="utf-8")
        checked += 1
        if value not in pages[page]:
            print(f"STALE  {page}: {what} should read {value} — "
                  f"the page does not contain it ({H0})", file=sys.stderr)
            bad += 1

    if bad:
        print(f"\n{bad} of {checked} claims no longer match the artifact they name.",
              file=sys.stderr)
        return 1
    print(f"site numbers: {checked} claim(s) resolved to the artifact they name")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
