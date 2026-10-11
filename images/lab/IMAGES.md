# The lab: one plate for the top of the home

Optional. The home's `#projects` section is complete without it, and `#connections` already draws the links
as an inline SVG. What this plate adds is the first picture a newcomer sees: the three active projects as three
benches in one room, and which links between them exist.

Its `<figure>` sits in `index.html` at the end of `<section id="projects">`, **inside an HTML comment marked
`IMAGE PLACEHOLDER`**, so nothing renders broken before the file exists. Once the file is committed, delete the
two comment lines around the figure. That is the only edit.

Directory convention: the home's pictures live in `assets/img/<project>/`; this one belongs to no single project,
so it goes in **`assets/img/lab/`**. This file is the only thing in `images/lab/`.

---

## 1. `assets/img/lab/three-projects.jpg`

- **Size / aspect:** 1800 × 720 px (5 : 2), like `assets/img/lora-kernel/hero.jpg`.
- **Format:** JPEG, quality ~82, sRGB, under ~350 KB.
- **What it shows:** the three benches each repeat the motif of their project's own plate (the library and the
  radar lamp; the machine and its sealed ledger; the report tied by threads to evidence cards), so the plate
  reads as the three heroes in one room. The connections must be exactly as true today: **one solid link**
  between the lora-kernel and agentvcs benches (built: agentvcs's LK0 example imports lora-kernel's
  configuration, imported not live), and **two dashed links** from the gene-evidence bench to each of the other two
  (planned, not built). No people, no legible text, no numbers.
- **Prompt (ready to paste):**

```
A wide 5:2 plate in the style of a 19th-century natural-history and engineering engraving: fine sepia ink
linework with a muted, transparent watercolour wash on warm, slightly textured parchment paper (#F3EBDD), soft
even daylight, generous empty margins.

Scene: one long, calm workshop room seen from the front and slightly above, with three separate wooden
workbenches spaced evenly from left to right, each with its own small world on it. No people.

Left bench (a library): behind it a tall card-catalogue cabinet of small wooden drawers with brass pulls; on the
bench a small brass radar dish on a stand whose pale beam lights exactly three drawers; one thick leather-bound
volume lies beside a few thin ones.

Middle bench (a machine and its ledger): a compact brass machine of gears and levers, one gear freshly replaced in
brighter brass; from the machine a paper ledger unrolls across the bench, each ruled line ending in a small round
wax seal, the seals slate blue (#5B7186) before the swapped gear and rust orange (#B5603A) after it.

Right bench (a naturalist's evidence table): a single printed report lies flat, its lines suggested by fine grey
strokes; from the end of each line a very fine red thread rises to one of five small cream index cards pinned to a
cork strip above the bench, each card carrying only a tiny abstract diagram (a bar chart, coloured blocks, a wavy
line, a grid, a crossed-out box). A brass magnifying glass rests beside the report.

Connections: a single solid cord in sage green (#8A9A6B) runs low along the floor from the left bench to the middle
bench, firmly tied at both ends. From the right bench, two thin dashed lines drawn in ochre chalk (#C9A54A), clearly
dashed and slightly faint, lead one to the left bench and one to the middle bench, as if marked out for later.

Palette limited to sepia ink, slate blue, sage green, rust orange and ochre on parchment. Orderly, precise, quiet.

Strictly no legible text or letters, no numbers, no logos, no people or hands, no robots, no DNA double helix, no
glow, no gradients, no 3D render, no photographic look.
```
