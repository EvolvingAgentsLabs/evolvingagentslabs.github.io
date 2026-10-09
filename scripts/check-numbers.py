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
import re
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
# Added 2026-10-08, when the home stopped saying "no real data yet": the runs on
# real documents, the edit-after-training test and the router that replaced the
# keyword dictionary as the proxy's default.
LK_REAL3 = "results/REAL3-real-corpus-20260930/real3_fresh.json"
LK_EDIT0 = "results/EDIT0-edit-without-retraining-20261004/verdict.json"
LK_ROUTE0 = "results/ROUTE0-factored-router-20261002/verdict.json"

# gene-evidence opened on 2026-10-09. Its numbers on the home come from the rat
# development run committed in that repository. Counts are recomputed from the
# per-candidate table rather than copied from prose, so a re-run that moves them
# fails here. Two are read from the run record's own [ran] sentences instead:
# the unit-test count and the T-cell receptor / immunoglobulin count, which the
# record states as a reading of the top 100 by name and no column encodes.
GE_RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/gene-evidence/{ref}/{path}"
GE_RUN = "runs/2026-10-09-rat-dev"
GE_TSV = f"{GE_RUN}/all_candidates.tsv"
GE_DETERMINISM = f"{GE_RUN}/determinism.txt"
GE_CHECK = f"{GE_RUN}/check.txt"
GE_BRIEF = "BRIEF.md"


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


def fetch_text(path: str, ref: str, raw: str) -> str:
    url = raw.format(ref=ref, path=path)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode()
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"could not read {url}: {e}", file=sys.stderr)
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


def lora_kernel_real_claims(real3: dict, edit0: dict, route0: dict) -> list[tuple[str, str, str]]:
    """The real-document, edit and router numbers, rendered the way the page renders them."""
    home = "index.html"
    pr = real3["analysis"]["pairs"]["headline"][0]
    f3 = route0["per_set"]["factored"]["F3"]
    return [
        (home, f"{pr['a_total']}/{pr['n_paired']}", "REAL3: the real-document member on an unseen family"),
        (home, f"{pr['b_total']}/{pr['n_paired']}", "REAL3: the untrained base on the same rows"),
        (home, f"{pr['only_a']}&nbsp;:&nbsp;{pr['only_b']}", "REAL3: the discordant pairs"),
        (home, edit0["right_new_value"], "EDIT0: rows answering the edited value"),
        (home, f"{len(edit0['stale'])} stale", "EDIT0: stale answers"),
        (home, route0["foreign_misrouted"], "ROUTE0: foreign text served locally, factored router"),
        (home, route0["dictionary_foreign_misrouted"], "ROUTE0: the same, keyword dictionary"),
        (home, f"{f3['lost_local']} of {f3['n']} lost", "ROUTE0: unseen senders lost"),
        (home, route0["B3_recovered"], "ROUTE0: paraphrases kept local"),
    ]


def gene_evidence_claims(tsv: str, determinism: str, check: str, brief: str) -> list[tuple[str, str, str]]:
    """gene-evidence's rat development run, rendered the way the home renders it."""
    home = "index.html"
    lines = [l for l in tsv.splitlines() if l.strip()]
    head = lines[0].split("\t")
    rows = [dict(zip(head, l.split("\t"))) for l in lines[1:]]
    n = len(rows)
    pseudo = sum(r["locus_context"] == "pseudogene" for r in rows)
    top = [r for r in rows if int(r["rank"]) <= 100]
    smok = sum("SMKY_" in r["swissprot_best"] for r in top)
    pol = sum("|POL_" in r["swissprot_best"] for r in top)
    rank1_pol = any(r["rank"] == "1" and "|POL_" in r["swissprot_best"] for r in rows)
    all_tier1 = len(top) == 100 and all(r["tier"] == "1" for r in top)

    # determinism.txt: two sha256 pairs and a verdict. Recheck the pairs, do not
    # trust the verdict line alone.
    hashes: dict[str, set[str]] = {}
    for l in determinism.splitlines():
        parts = l.split()
        if len(parts) == 2 and "/" in parts[1]:
            hashes.setdefault(parts[1].split("/", 1)[1], set()).add(parts[0])
    identical = (determinism.strip().splitlines()[-1].strip() == "IDENTICAL"
                 and set(hashes) == {"graph.json", "report.md"}
                 and all(len(v) == 1 for v in hashes.values()))
    passed = check.strip() == "PASS"

    m_tests = re.search(r"\*\*PASS\*\*\. (\d+) tests", brief)
    m_tcr = re.search(r"(\d+) hit T-cell receptor or immunoglobulin variable segments", brief)
    never = "(the artifact no longer supports this claim)"
    return [
        (home, f"{n} candidates", "gene-evidence: candidates analysed"),
        (home, f"{pseudo} of {n}", "gene-evidence: candidates on reference pseudogene loci"),
        (home, f"{round(100 * pseudo / n)}&nbsp;%", "gene-evidence: pseudogene share"),
        (home, f"{smok} hit the Smok", "gene-evidence: Smok kinase hits in the top 100"),
        (home, f"{pol} retroviral Pol" if rank1_pol else never, "gene-evidence: Pol polyproteins, rank 1 among them"),
        (home, "all tier 1" if all_tier1 else never, "gene-evidence: the top 100 are all tier 1"),
        (home, (m_tcr.group(1) if m_tcr else never) + " T-cell receptor or immunoglobulin",
         "gene-evidence: TCR / Ig variable hits in the top 100 (run record)"),
        (home, (m_tests.group(1) if m_tests else never) + " unit tests", "gene-evidence: unit tests (run record)"),
        (home, "byte-identical" if identical else never, "gene-evidence: two runs, identical graph and report"),
        (home, "every sentence passed the citation check" if passed else never,
         "gene-evidence: check-report on the committed report"),
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
    lk += lora_kernel_real_claims(fetch(LK_REAL3, "main", LK_RAW), fetch(LK_EDIT0, "main", LK_RAW),
                                  fetch(LK_ROUTE0, "main", LK_RAW))
    # gene-evidence's default branch is `main`, like lora-kernel's.
    ge = gene_evidence_claims(fetch_text(GE_TSV, "main", GE_RAW), fetch_text(GE_DETERMINISM, "main", GE_RAW),
                              fetch_text(GE_CHECK, "main", GE_RAW), fetch_text(GE_BRIEF, "main", GE_RAW))
    for page, value, what in claims(h0) + lk + ge:
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
