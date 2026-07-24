# evolvingagentslabs.github.io

Source for **[evolvingagentslabs.github.io](https://evolvingagentslabs.github.io)** — the Evolving Agents Labs site.

> Experiments in how agents learn, remember, and prove what they know.

## How it works

`index.html` is hand-written static HTML with inline CSS. There is no build step, no framework, and nothing is templated — Jekyll passes the file through untouched. Deployment is GitHub Pages on the default branch: push to `main` and it is live.

To preview locally:

```bash
python3 -m http.server 8000
```

## Editing the experiment list

Each experiment is one `<a class="row">` block in `index.html`, ordered newest first. A row carries the repo name, an evidence badge, a "what if" question, a short note, and a date.

The three badges describe **evidence**, not roadmap stage — that distinction is the point of the page:

| Badge | Means |
|---|---|
| `Reproducible` | clone it and run it, no API key |
| `Results` | published findings, negative ones included |
| `Prototype` | runs, but needs setup or has no eval yet |

Do not promote a row to `Reproducible` or `Results` without the artifact that backs it.

---

Apache 2.0 · permanently alpha
