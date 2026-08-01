# evolvingagentslabs.github.io

Source for **[evolvingagentslabs.github.io](https://evolvingagentslabs.github.io)**.

> ai-os — an agent-based operating system.

The site leads with **[ai-os](https://github.com/EvolvingAgentsLabs/ai-os)**, the
organisation's only active project. Everything else is frozen and lives under
`/archive/`.

## Structure

```
index.html                      ai-os — the home
archive/index.html              the frozen experiments, 2025-2026
experiments/<slug>/index.html   one detail page per frozen experiment
assets/site.css                 all styles, hand-written
tools/{data,build}.py           optional generator (see below)
```

Navigation mirrors [labs.google/code](https://labs.google/code): a visitor reads what
a thing is, and what is actually established about it, before landing in a source
tree. That still holds for `/archive/` — cards link to a detail page and the
repository appears there as a CTA.

**The home is the exception, on purpose.** ai-os has no demo and no results yet; its
design documents *are* the artifact, so the home links straight to `doc/`.

Deployment is GitHub Pages on the default branch — push to `main` and it is live.
There is no build step and nothing is templated; Jekyll passes the HTML through
untouched. Preview locally with:

```bash
python3 -m http.server 8000
```

## Adding or editing an experiment

The HTML is generated but **the output is committed**, so the site stays buildless.
Edit [`tools/data.py`](tools/data.py) and re-render:

```bash
python3 tools/build.py .
```

Each entry needs a slug, name, badge, date, `sort` key (controls index order), the
"what if" question, a one-paragraph blurb, a repo URL, an optional demo URL, and a
list of `(heading, html)` sections.

You can also just hand-edit the HTML — nothing depends on the generator having
produced it. If you do, keep `tools/data.py` in sync or delete it.

## The badges

They describe **evidence**, not roadmap stage. That distinction is the point of the
page, and it is what makes it worth publishing next to everyone else's.

| Badge | Means |
|---|---|
| `Reproducible` | clone it and run it, no API key |
| `Results` | published findings, negative ones included |
| `Prototype` | runs, but needs setup or has no eval yet |

Do not promote a row without the artifact that backs it. Every detail page carries a
**What's proven** section, and each one is expected to say plainly what is *not*
established — the sample sizes, the missing controls, the things that break on a
clean clone. That section is the reason a reader should believe the rest.

---

Apache 2.0 · permanently alpha
