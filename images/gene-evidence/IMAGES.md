# gene-evidence: images for the home page

None of these is required. The home's `#gene-evidence` and `#connections` sections are complete
without them: the relationship diagram is inline SVG in `index.html` (`figure.linkmap`), drawn with the
site's own tokens (`--bg-2`, `--sep`, `--ink`, `--dim`, `--green` for built, `--orange` for next), so it
needs no file. The site has one theme (parchment, `color-scheme: light`), so there is no dark variant.

Three optional plates are specified below. Their `<figure>` blocks sit in `index.html`, at the end of
`<section id="gene-evidence">` (after its `.pillars` block), **inside one HTML comment** so that nothing
renders broken before the files exist. To ship one: add the file at the path given, then cut its
`<figure>…</figure>` out of the comment and paste it just above the comment's opening `<!-- Images:`
line (leave the comment in place for the others; delete it once all three have shipped).

The source repository is public: <https://github.com/EvolvingAgentsLabs/gene-evidence>. Every number
in a plate comes from a file committed there under `runs/2026-10-09-rat-dev/`, and the home's copy of
those numbers is checked nightly by `scripts/check-numbers.py`. Do not put a number in a plate that the
check does not cover or that the committed files do not contain.

Directory convention: the home's pictures live in `assets/img/<project>/` (see `assets/img/lora-kernel/`),
so the files go in **`assets/img/gene-evidence/`**. This instructions file is the only thing in `images/gene-evidence/`.

---

## 1. `assets/img/gene-evidence/hero.jpg`

- **Size / aspect:** 1800 × 720 px (5 : 2), the same as `assets/img/lora-kernel/hero.jpg`.
- **Format:** JPEG, quality ~82, sRGB, under ~350 KB (recompress like the lora-kernel plates).
- **What it shows:** the idea of the project in the house style of the lora-kernel plates (ink line
  drawing with muted watercolour wash on parchment): a lab bench; a long horizontal genome track with
  gene boxes; one predicted gene on the track circled in pencil; a printed report on the bench whose
  lines each have a thin thread running to a small index card pinned above (the cards stand for tool
  outputs: a homology hit, a domain, a "pseudogene here" flag). One card, the pseudogene flag, is pinned
  first and slightly larger. No people, no logos, no legible text or gene names.
- **Prompt (ready to paste):**
  > Ink line drawing with a muted watercolour wash on warm parchment paper, the style of a 19th-century
  > scientific plate, wide 5:2 composition. A tidy laboratory bench seen slightly from above. Across the
  > top runs a long horizontal strip like a genome browser track, with small rectangular gene boxes
  > joined by thin lines; one box near the centre is circled in pencil. On the bench lies a printed report;
  > from the end of each of its lines a fine red thread runs up to a small index card pinned on a cork
  > strip above the bench. The cards carry tiny abstract diagrams only (a bar chart, a row of coloured
  > blocks, a crossed-out box), no legible words. The card with the crossed-out box is pinned first and
  > is a little larger. Palette: sepia ink, slate blue, sage green, rust orange, ochre. Calm, precise,
  > generous margins, no text, no logos, no people.
- **Alt text:** "A bench with a genome browser track; one predicted gene is circled, and thin threads
  run from each line of a printed report to small cards of tool output pinned above."
- **Un-comment:** move the `<figure>` whose `src` is `/assets/img/gene-evidence/hero.jpg` out of the
  comment, as described at the top.
- **Caption:** "Every sentence of the report is tied to the tool output it rests on."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#gene-evidence`.

## 2. `assets/img/gene-evidence/locus-context.png`

- **Size / aspect:** 1600 × 700 px (16 : 7). **Format:** PNG (a chart; flat colour, keep it sharp), under ~120 KB.
- **What it shows:** the 947 candidates of the rat development run by locus context, one horizontal bar
  per class, longest first: pseudogene 578, nothing 285, protein-coding gene (other strand or intron) 45,
  non-coding gene 39. Each bar labelled with its count; the pseudogene bar also with "61 %". It is the
  number behind "the evidence against comes first".
- **Source:** `runs/2026-10-09-rat-dev/all_candidates.tsv` in gene-evidence (947 data rows, column
  `locus_context`). Nothing else.
- **Exact steps** (any machine with Python 3 and matplotlib; no model, seconds):
  ```bash
  curl -sLO https://raw.githubusercontent.com/EvolvingAgentsLabs/gene-evidence/main/runs/2026-10-09-rat-dev/all_candidates.tsv
  cut -f4 all_candidates.tsv | tail -n +2 | sort | uniq -c | sort -rn
  # expect: 578 pseudogene · 285 nothing · 45 protein-coding gene · 39 non-coding gene (sum 947)
  ```
  ```python
  import csv, collections, matplotlib
  matplotlib.use("Agg"); import matplotlib.pyplot as plt
  rows = list(csv.DictReader(open("all_candidates.tsv"), delimiter="\t"))
  assert len(rows) == 947
  c = collections.Counter(r["locus_context"] for r in rows)
  order = ["pseudogene", "nothing", "protein-coding gene", "non-coding gene"]
  labels = ["pseudogene", "nothing", "protein-coding gene\n(other strand or intron)", "non-coding gene"]
  vals = [c[k] for k in order]
  fig, ax = plt.subplots(figsize=(16, 7), dpi=100)
  fig.patch.set_facecolor("#F4ECDB"); ax.set_facecolor("#F4ECDB")          # --bg
  bars = ax.barh(labels[::-1], vals[::-1],
                 color=["#5C5344", "#5C5344", "#5C5344", "#B5651D"])        # --dim; --orange = evidence against
  for b, v in zip(bars, vals[::-1]):
      t = f"{v}" + (f"  ({round(100*v/len(rows))} %)" if v == c["pseudogene"] else "")
      ax.text(b.get_width() + 6, b.get_y() + b.get_height()/2, t, va="center", fontsize=20, color="#211C15")
  ax.set_xlim(0, 700); ax.tick_params(labelsize=18, colors="#211C15")
  for s in ("top", "right"): ax.spines[s].set_visible(False)
  for s in ("left", "bottom"): ax.spines[s].set_color("#CDBF9F")             # --sep
  ax.set_title("947 candidates, rat development run: what the reference annotates at the locus",
               fontsize=20, color="#211C15", loc="left", pad=16)
  fig.tight_layout(); fig.savefig("locus-context.png", facecolor=fig.get_facecolor())
  ```
  Then `assets/img/gene-evidence/locus-context.png`. Read the image back before committing: four bars,
  counts 578 / 285 / 45 / 39, nothing else. Colours are the site tokens (`--bg`, `--ink`, `--dim`,
  `--sep`; `--orange` marks the evidence against, as in the site's own diagrams); no green or red, which
  the site spends only on verdicts.
- **Alt text:** "Bar chart of the 947 candidates of the rat development run by what the reference
  annotates at the locus: pseudogene 578, nothing 285, protein-coding gene on the other strand or in an
  intron 45, non-coding gene 39."
- **Caption:** "The rat development run: 578 of the 947 candidates sit on loci the reference already
  calls pseudogenes. That is why locus context is read before homology."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#gene-evidence`.
- **Un-comment:** move the `<figure>` whose `src` is `/assets/img/gene-evidence/locus-context.png` out of
  the comment, as described at the top.

## 3. `assets/img/gene-evidence/report-candidate.png`

- **Size / aspect:** 1600 × 1000 px (8 : 5). **Format:** PNG (text screenshot; keep it sharp).
- **What it shows:** the rank-1 candidate's section of the committed rat development report, rendered as
  Markdown: heading, Evidence FOR, Evidence AGAINST, Context, Suggested validation, each line ending
  in bracketed graph-node citations such as `[sprot:…]` `[rule:tiers]`. (Rank 1 is a retroviral Pol
  polyprotein hit, the multi-copy failure mode the home names; the caption does not hide it.)
- **Exact steps:**
  1. Open <https://github.com/EvolvingAgentsLabs/gene-evidence/blob/main/runs/2026-10-09-rat-dev/run1/report.md>
     and take lines **117–141** (the section `### 1. GCA_036323735.1_gene00003511: tier 1 (FOR-strong)`
     through its two **Suggested validation** bullets; line 142 is blank, 143 starts rank 2). Raw:
     `curl -sL https://raw.githubusercontent.com/EvolvingAgentsLabs/gene-evidence/main/runs/2026-10-09-rat-dev/run1/report.md | sed -n 117,141p > snippet.md`
  2. Render that Markdown on a light background (e.g. GitHub's Markdown preview, or
     `pandoc snippet.md -s -o snippet.html` opened in a browser at 1600 px width, zoom 125 %).
  3. Screenshot the rendered block at 1600 × 1000; if it is taller, keep the heading, both evidence
     blocks and the validation bullets, and cut the Context block's last lines rather than shrinking text.
  4. Before committing: read the image and confirm it contains no local paths and no account names.
- **Alt text:** "One candidate's section of a gene-evidence report: evidence for, evidence against,
  context and a suggested validation experiment, each line ending in bracketed graph-node citations."
- **Caption:** "Rank 1 of the rat development run: every line ends in the graph nodes it cites."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#gene-evidence`.
- **Un-comment:** move the `<figure>` whose `src` is `/assets/img/gene-evidence/report-candidate.png` out
  of the comment, as described at the top.
