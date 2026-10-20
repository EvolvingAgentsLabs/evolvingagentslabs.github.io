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
# Added 2026-10-11, when lora-kernel's measured detail moved from the home to its own page
# (lora-kernel/index.html): the three rows of that table that had no check yet (P41, P62, P61),
# and the τ² headroom line (T1, T1b), read from T1b's verdict, which recomputes T1's arms.
LK_P41 = "results/P41-routing-20260915/routing.json"
LK_P62 = "results/P62-route-per-request-20260918/replay.json"
LK_P61 = "results/P61-knowledge-vs-weights-20260918/session.json"
LK_TAU2 = "results/TAU2-T1b-12b-base-20261006/verdict.json"

# Where each project's numbers are published. The home keeps a short list per project; the
# detail page carries every measured row. A number on both pages is checked on both.
HOME = "index.html"
LK_PAGE = "lora-kernel/index.html"
# The lora-kernel claims the home repeats in its short section, by their `what`.
LK_ON_HOME = {
    "the fluids expert in corpus mode", "the same expert through tool_calls", "the discordant pairs",
    "email-full on Qwen3.5-4B",
    "REAL3: the real-document member on an unseen family", "REAL3: the untrained base on the same rows",
    "EDIT0: rows answering the edited value", "EDIT0: stale answers",
    "ROUTE0: foreign text served locally, factored router", "ROUTE0: the same, keyword dictionary",
}

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

# agentvcs, since 2026-10-11: the home quotes its Gate F2 rerun on a real model
# (Qwen2.5-1.5B on llama.cpp), read from the result file that run committed.
AV_RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/agentvcs/{ref}/{path}"
AV_F2 = "examples/toy_pipeline/runs/f2-rerun-2026-10-06/result.json"
# Added 2026-10-14 with the director (evolving-agents/packages/director): its scores are stated in its briefs,
# each in a table or a sentence written from the run; the check reads them there.
EA_RAW = "https://raw.githubusercontent.com/EvolvingAgentsLabs/evolving-agents/{ref}/{path}"
DIR_D0, DIR_D2, DIR_D3 = (f"packages/director/docs/BRIEF-{d}.md" for d in ("D0", "D2", "D3"))
# Added 2026-10-20: the plugin (P0), local planning by recipes (D15) and the directory of lanes (D16, flat).
DIR_P0, DIR_D15, DIR_D16 = (f"packages/director/docs/BRIEF-{d}.md" for d in ("P0", "D15", "D16"))


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
    """lora-kernel's first numbers, each rendered the way the detail page renders it."""
    home = LK_PAGE
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
    """The real-document, edit and router numbers, rendered the way the detail page renders them."""
    home = LK_PAGE
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


def lora_kernel_more_claims(p41: dict, p62: dict, p61: dict, tau2: dict) -> list[tuple[str, str, str]]:
    """The routing replay, the pasted-procedure arm and the τ² headroom line, on the detail page."""
    page = LK_PAGE
    never = "(the artifact no longer supports this claim)"
    local = p41["policies"]["everything local"]["accuracy"]
    req = p62["by_request"]
    v = p61["verdict"]
    ev = v["expert_vs_kb"]
    t, g, h = tau2["pass1"], tau2["12B_vs_E4B"], tau2["31B_vs_12B"]
    w = g["wins"].replace(":", "&nbsp;:&nbsp;")
    return [
        (page, f"{local:.3f} &rarr; {req['accuracy']:.3f}", "P41/P62: everything local against routed, 240-case replay"),
        (page, f"{req['misrouted']} misrouted", "P62: requests handed to the wrong member"),
        (page, f"{ev['only_a']}&nbsp;:&nbsp;{ev['only_b']}" if v["kb_calls"] == 0 else never,
         "P61: the expert against the pasted procedure, which made no tool calls"),
        (page, f"pass^1 <b>{t['12B']}</b>", "τ² T1b: the 12B base on airline test"),
        (page, f"the E4B&rsquo;s {t['E4B']}", "τ² T1: the E4B base"),
        (page, f"+{g['delta_pp']}&nbsp;pp, {w} tasks" if tau2["decision"] == "12B IS THE STUDENT" else never,
         "τ² T1b: the 12B over the E4B, paired"),
        (page, f"the 31B&rsquo;s {t['31B']} is +{h['delta_pp']}&nbsp;pp over the 12B, inside the noise"
         if h["ci_pp"][0] <= 0 <= h["ci_pp"][1] else never, "τ² T1b: the 31B over the 12B, CI crossing 0"),
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


def agentvcs_claims(f2: dict) -> list[tuple[str, str, str]]:
    """agentvcs's Gate F2 rerun, rendered the way the home renders it."""
    home = "index.html"
    never = "(the artifact no longer supports this claim)"
    attr = f2["blame"]["extract.recall"]["attributions"]
    applied = [r["patch_id"] for r in f2["harness"]["reloads"]]
    one = len(attr) == 1 and attr[0]["patches"] == applied == [f2["patch_id"]]
    return [
        (home, f"+{f2['gate']['extract.recall.gain']:.3f}" if f2["ok"] else never,
         "agentvcs F2: paired gate gain on the real model"),
        (home, f"+{attr[0]['delta']:.3f}" if one else never, "agentvcs F2: blame delta"),
        (home, "exactly one patch" if one and f2["verify"] else never,
         "agentvcs F2: one attribution, to the patch that was applied, ledger verified"),
    ]


def director_claims(d0: str, d2: str, d3: str) -> list[tuple[str, str, str]]:
    """The director's D0, D2 and D3, rendered the way the home renders them."""
    home = "index.html"
    never = "(the artifact no longer supports this claim)"
    m0 = re.search(r"\| mean \| (0\.\d+) \| (0\.\d+) \| \*\*(0\.\d+)\*\* \|", d0)
    m2 = re.search(r"T1b − T0c = \*\*\+(0\.\d+)\*\*", d2)
    g2 = re.search(r"guard (0\.\d+) ≥ 0\.86 → \*\*LEARNS\*\*", d2)
    m3 = re.search(r"\| public-facing tasks planned on the frontier \| \*\*0\.0\*\* \(0 / 6\) \| \*\*1\.0\*\* \(6 / 6\) \|", d3)
    return [
        (home, f"<b>{m0.group(1)}</b>" if m0 else never, "director D0: today's session"),
        (home, f"<b>{m0.group(2)}</b>" if m0 else never, "director D0: told to walk its files (A+)"),
        (home, f"<b>{m0.group(3)}</b>" if m0 else never, "director D0: the director"),
        (home, f"<b>{m2.group(1)}</b>" if m2 else never, "director D2: probes after learning"),
        (home, f"<b>{g2.group(1)}</b>" if g2 else never, "director D2: guard on D0"),
        (home, "<b>0 / 6 &rarr; 6 / 6</b>" if m3 else never, "director D3: public-facing drafts to the frontier"),
    ]


def director_more_claims(p0: str, d15: str, d16: str) -> list[tuple[str, str, str]]:
    """P0 (the plugin), D15 (recipes on a local 12B) and D16 (the directory, published flat), as the home renders them."""
    home = "index.html"
    never = "(the artifact no longer supports this claim)"
    mp = re.search(r"\| mean, 14 cases × k = 2 \| \*\*(0\.\d+)\*\* \| \*\*(0\.\d+)\*\* \|", p0)
    g12 = re.search(r"\| \*\*G12\*\* `gemma4:12b-mlx` \| \*\*(0\.\d+)\*\* \|", d15)
    t15 = re.search(r"\| T \(Sonnet walking with tools\) \| (0\.\d+) \|", d15)
    m16 = re.search(r"\| 1 · lane accuracy, 15 cases × k = 2 \| (0\.\d+) \| \*\*(0\.\d+)\*\* \|", d16)
    return [
        (home, f"<b>{mp.group(2)}</b>" if mp else never, "director P0: the walk through the plugin"),
        (home, f"<b>{g12.group(1)}</b>" if g12 else never, "director D15: gemma4:12b following recipes"),
        (home, f"<b>{t15.group(1)}</b>" if t15 else never, "director D15: Sonnet walking with tools"),
        (home, f"<b>{m16.group(2)}</b>" if m16 else never, "director D16: the directory's lane accuracy"),
        (home, f"<b>{m16.group(1)}</b>" if m16 else never, "director D16: prose's lane accuracy"),
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
    lk += [(HOME, value, what + " (home)") for _, value, what in lk if what in LK_ON_HOME]
    if len({w for _, _, w in lk if w in LK_ON_HOME}) != len(LK_ON_HOME):
        print("LK_ON_HOME names a claim that no longer exists", file=sys.stderr)
        return 1
    lk += lora_kernel_more_claims(fetch(LK_P41, "main", LK_RAW), fetch(LK_P62, "main", LK_RAW),
                                  fetch(LK_P61, "main", LK_RAW), fetch(LK_TAU2, "main", LK_RAW))
    # gene-evidence's default branch is `main`, like lora-kernel's.
    ge = gene_evidence_claims(fetch_text(GE_TSV, "main", GE_RAW), fetch_text(GE_DETERMINISM, "main", GE_RAW),
                              fetch_text(GE_CHECK, "main", GE_RAW), fetch_text(GE_BRIEF, "main", GE_RAW))
    # agentvcs's default branch is `main` too.
    av = agentvcs_claims(fetch(AV_F2, "main", AV_RAW))
    di = director_claims(fetch_text(DIR_D0, "main", EA_RAW), fetch_text(DIR_D2, "main", EA_RAW),
                         fetch_text(DIR_D3, "main", EA_RAW))
    di += director_more_claims(fetch_text(DIR_P0, "main", EA_RAW), fetch_text(DIR_D15, "main", EA_RAW),
                               fetch_text(DIR_D16, "main", EA_RAW))
    for page, value, what in claims(h0) + lk + ge + av + di:
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
