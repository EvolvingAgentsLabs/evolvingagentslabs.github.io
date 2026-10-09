# gene-evidence: images for the home page

None of these is required. The home's `#gene-evidence` and `#connections` sections are complete
without them: the relationship diagram is inline SVG in `index.html` (`figure.linkmap`), drawn with the
site's own tokens (`--bg-2`, `--sep`, `--ink`, `--dim`, `--green` for built, `--orange` for next), so it
needs no file. The site has one theme (parchment, `color-scheme: light`), so there is no dark variant.

Two optional raster plates are specified below. Their `<figure>` blocks already sit in `index.html`, at
the end of `<section id="connections">`, **inside an HTML comment** so that nothing renders broken
before the files exist. To ship one: add the file at the path given, then move its `<figure>` out of the
comment (and into `<section id="gene-evidence">` if preferred, after the `.pillars` block).

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
- **Caption:** "Every sentence of the report is tied to the tool output it rests on."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#connections`.

## 2. `assets/img/gene-evidence/report-candidate.png`

- **Size / aspect:** 1600 × 1000 px (8 : 5). **Format:** PNG (text screenshot; keep it sharp).
- **What it shows:** one candidate's section of the committed rat development report, rendered as
  Markdown: heading, Evidence FOR, Evidence AGAINST, Context, Suggested validation, each line ending
  in bracketed graph-node citations such as `[sprot:…]` `[rule:tiers]`.
- **Exact steps:**
  1. In the gene-evidence repository, take lines **117–141** of
     `runs/2026-10-09-rat-dev/run1/report.md` (the section `### 1. GCA_036323735.1_gene00003511: tier 1
     (FOR-strong)` through its **Suggested validation** bullets), copied into a scratch `.md` file.
  2. Render that Markdown on a light background (e.g. GitHub's Markdown preview, or
     `pandoc snippet.md -s -o snippet.html` opened in a browser at 1600 px width, zoom 125 %).
  3. Screenshot the rendered block at 1600 × 1000; if it is taller, keep the heading, both evidence
     blocks and the validation bullets, and cut the Context block's last lines rather than shrinking text.
  4. Before committing: read the image and confirm it contains no local paths and no account names.
- **Alt text:** "One candidate's section of a gene-evidence report: evidence for, evidence against,
  context and a suggested validation experiment, each line ending in bracketed graph-node citations."
- **Caption:** "One candidate from the rat development run: every line ends in the graph nodes it cites."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#connections`.
