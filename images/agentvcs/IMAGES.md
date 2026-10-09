# agentvcs: images for the home page

None of these is required. The home's `#agentvcs` section is complete without it, and the detail page
`/experiments/agentvcs/` already has its own picture (`assets/img/agentvcs.jpg`, from the 2026 Python
version). The site has one theme (parchment, `color-scheme: light`), so there is no dark variant.

One optional plate is specified below. Its `<figure>` block sits in `index.html`, at the end of
`<section id="agentvcs">` (after its `.pillars` block), **inside an HTML comment** so that nothing renders
broken before the file exists.

Directory convention: the home's pictures live in `assets/img/<project>/` (see `assets/img/lora-kernel/`),
so the file goes in **`assets/img/agentvcs/`**. This instructions file is the only thing in `images/agentvcs/`.

---

## 1. `assets/img/agentvcs/hero.jpg`

- **Size / aspect:** 1800 × 720 px (5 : 2), the same as `assets/img/lora-kernel/hero.jpg`.
- **Format:** JPEG, quality ~82, sRGB, under ~350 KB (recompress like the lora-kernel plates).
- **What it shows:** the idea of the project, not a result (agentvcs publishes no numbers on the home
  until its validation is done): a machine that keeps running while it is changed, and a ledger that
  stamps each of its steps with the version that produced it. In the house style of the lora-kernel
  plates (ink line drawing with muted watercolour wash on parchment). No people, no logos, no legible
  text, no numbers that could be read as measurements.
- **Prompt (ready to paste):**
  > Ink line drawing with a muted watercolour wash on warm parchment paper, the style of a 19th-century
  > engineering plate, wide 5:2 composition. On the left, a small brass machine of gears and levers keeps
  > running; one gear has just been swapped and is drawn in a fresher, brighter brass, a spare old gear
  > resting beside it on the bench. From the machine a long paper ledger unrolls to the right across the
  > bench; each line of the ledger carries a small round wax stamp, the stamps before the swap in one
  > colour and the stamps after it in another. A thin red ribbon runs from the new gear to the first
  > stamped line after the swap. Above the bench, a row of labelled-looking drawer fronts with only
  > abstract marks, no legible words. Palette: sepia ink, slate blue, sage green, rust orange, ochre.
  > Calm, precise, generous margins, no text, no logos, no people.
- **Alt text:** "A long workshop ledger running across a bench; each line of a running machine's log
  carries a small numbered stamp, and a ribbon ties one changed gear in the machine to the stamped lines
  that came after it."
- **Caption:** "Every step stamped with the harness version that produced it, so a change made while the
  system runs can be traced to what it changed."
- **Referenced in:** `index.html`, commented `<figure class="plate">` at the end of `#agentvcs`.
- **Un-comment:** add the file, then delete the two comment lines around the `<figure>`: the line
  starting `<!-- Image: optional, specified in images/agentvcs/IMAGES.md` and the line `-->` after
  `</figure>`.
