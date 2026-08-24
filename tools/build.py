#!/usr/bin/env python3
"""Render the Evolving Agents Labs site. Output is committed; this is not a build step."""
import os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import EXPERIMENTS, ORIGIN, BADGES, THESIS

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"

# The stylesheet is READ, not carried. It used to be a verbatim copy of
# assets/site.css pasted into this file, and the copy had already drifted: the
# shipped sheet grew the pillars, the stripe and the ai-os home while this one
# still described a site with none of them. A second copy of a thing nobody
# diffs is how a number goes stale, and a design system is no different.
CSS = (pathlib.Path(__file__).resolve().parent.parent / "assets" / "site.css").read_text()


FONTS = ("<!-- No webfont link, deliberately. This site publishes numbers it says you\n"
         "     can check with the machine in front of you, and /verify/ already refuses\n"
         "     a stylesheet from fonts.googleapis.com for exactly that reason. The two\n"
         "     stacks in site.css are the demo's, and they are already on the machine. -->")

ICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect x='2' y='2' width='13' height='13' rx='4' fill='%23F2F2F7'/%3E"
    "%3Crect x='17' y='2' width='13' height='13' rx='4' fill='%23F2F2F7'/%3E"
    "%3Crect x='2' y='17' width='13' height='13' rx='4' fill='%23F2F2F7'/%3E"
    "%3Crect x='18' y='18' width='11' height='11' rx='3' fill='none' "
    "stroke='%23F2F2F7' stroke-width='2' opacity='.42'/%3E%3C/svg%3E\">\n"
    '<meta name="theme-color" content="#000000">\n'
    '<meta name="color-scheme" content="dark">'
)

#: The mark, inline, so a page renders it with no request of its own. Four
#: buckets of time: three written into, and one drawn as an outline rather than
#: as a zero. See assets/img/mark.svg.
MARK = (
    '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">'
    '<rect x="2" y="2" width="13" height="13" rx="4" fill="currentColor"/>'
    '<rect x="17" y="2" width="13" height="13" rx="4" fill="currentColor"/>'
    '<rect x="2" y="17" width="13" height="13" rx="4" fill="currentColor"/>'
    '<rect x="18" y="18" width="11" height="11" rx="3" fill="none" '
    'stroke="currentColor" stroke-width="2" opacity=".42"/></svg>'
)

#: The same mark, at hero size. The page used to open on a raster logo made for
#: paper; this one is four rectangles and scales.
MARK_HERO = MARK.replace('class="mark"', 'class="mark" role="img"')

FOOT = """  <footer class="foot">
    <span class="by">Ideas, architecture and implementation by
      <a href="https://github.com/matiasmolinas">Matias Molinas</a> and
      <a href="https://github.com/ismaelfaro">Ismael Faro</a>.
      Every experiment here started as a conversation between the two.</span>
    <span class="meta-foot">Apache 2.0 · permanently alpha ·
      <a href="https://github.com/EvolvingAgentsLabs">github.com/EvolvingAgentsLabs</a></span>
  </footer>"""


def head(title, desc, css_path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{ICON}
{FONTS}
<link rel="stylesheet" href="{css_path}">
</head>
<body>
"""


def masthead(prefix, here=""):
    """The bar, which is the demo's bar. It lives outside .wrap: the chrome spans
    the window even where the prose does not."""
    items = [
        ("/demo/", "Demo"),
        ("/verify/", "Verify"),
        ("/coclea-sr/", "COCLEA-SR"),
        ("/hemo-verified/", "HEMO-VERIFIED"),
        ("/archive/", "Archive"),
        ("https://github.com/EvolvingAgentsLabs/ai-os", "GitHub"),
    ]
    links = "\n".join(
        '      <a href="%s"%s>%s</a>'
        % (href, ' aria-current="page"' if href == here else "", label)
        for href, label in items
    )
    return f"""<header class="masthead">
  <div class="masthead-in">
    <a class="wordmark" href="{prefix}">{MARK}ai-os<span class="org">Evolving Agents Labs</span></a>
    <nav class="navlinks">
{links}
    </nav>
  </div>
</header>
"""


def build_index(exps):
    rows = []
    for e in exps:
        label, _ = BADGES[e["badge"]]
        thumb = (f'<span class="thumb"><img src="/assets/img/{e["image"]}.jpg" '
                 f'alt="" aria-hidden="true" loading="lazy"></span>') if e.get("image") else ""
        rows.append(f"""    <a class="row" href="/experiments/{e['slug']}/">
      {thumb}
      <span class="rowhead">
        <span class="name">{e['name']}</span>
        <span class="badge {e['badge']}">{label}</span>
      </span>
      <span>
        <p class="question">{e['question']}</p>
        <p class="note">{e['blurb']}</p>
      </span>
      <span class="meta">{e['date']} <span class="arrow" aria-hidden="true">→</span></span>
    </a>""")

    legend = "\n".join(
        f'    <div><span class="badge {k}">{v[0]}</span> {v[1]}</div>'
        for k, v in BADGES.items())

    return head(
        "Evolving Agents Labs — Experiments in how agents learn, remember, and prove what they know",
        "Open experiments in agent memory, self-modification, interpretability and constrained execution. Each one labelled by how much evidence stands behind it.",
        "/assets/site.css") + f"""
{masthead("/", "/archive/")}
<div class="wrap">

  <section class="hero">
    {MARK_HERO}
    <h1>Experiments in how agents learn, remember, and <em>prove</em> what they know.</h1>
    <p>Agents that modify themselves are easy to build and hard to trust. Everything here attacks the second half of that sentence — versioning an agent's evolution so a human can review it, reading a model's internal workspace to catch a memory it was tricked into keeping, or constraining a small model at the decoder so invalid output is not discouraged but impossible.</p>
    <p>Each experiment is labelled by how much evidence stands behind it — including the ones where the evidence went against us.</p>
    <p class="who">Everything here comes out of an ongoing conversation between
      <a href="https://github.com/matiasmolinas">Matias Molinas</a> and
      <a href="https://github.com/ismaelfaro">Ismael Faro</a> — the ideas, the
      architecture, and the code. The repositories are where those conversations
      got tested.</p>
  </section>

  <div class="legend" id="method">
{legend}
  </div>

  <main class="listing" id="experiments">

    <p class="sectionlabel">Where all of it started</p>

    <a class="row origin" href="/experiments/{ORIGIN['slug']}/">
      <span class="thumb"><img src="/assets/img/{ORIGIN['image']}.jpg" alt="" aria-hidden="true" loading="lazy"></span>
      <span class="rowhead">
        <span class="name">{ORIGIN['name']}</span>
      </span>
      <span>
        <p class="question">{ORIGIN['question']}</p>
        <p class="note">{ORIGIN['blurb']}</p>
      </span>
      <span class="meta">{ORIGIN['date']} <span class="arrow" aria-hidden="true">→</span></span>
    </a>

    <p class="sectionlabel">What came out of it — 2026</p>

{chr(10).join(rows)}


  </main>

{FOOT}

</div>

</body>
</html>
"""


def build_detail(e, prev_e, next_e):
    label = BADGES[e["badge"]][0] if e.get("badge") else None
    ctas = [f'<a class="cta primary" href="{e["repo"]}">GitHub <span aria-hidden="true">→</span></a>']
    if e.get("demo"):
        ctas.insert(0, f'<a class="cta" href="{e["demo"]}">Demo <span aria-hidden="true">→</span></a>')

    body = "\n".join(
        f"    <h2>{title}</h2>{content.rstrip()}\n" for title, content in e["sections"])

    badge_html = f'<span class="badge {e["badge"]}">{label}</span>\n      ' if label else ""
    figure = ""
    if e.get("image"):
        figure = (f'  <figure class="hero-figure">\n'
                  f'    <img src="/assets/img/{e["image"]}.jpg" alt="{e.get("image_alt","")}" loading="lazy">\n'
                  f'  </figure>')

    nav = []
    if prev_e:
        nav.append(f'<a href="/experiments/{prev_e["slug"]}/">← {prev_e["name"]}</a>')
    if next_e:
        nav.append(f'<a href="/experiments/{next_e["slug"]}/">{next_e["name"]} →</a>')
    navhtml = ""
    if nav:
        navhtml = f'  <div class="nextprev">{" &nbsp;·&nbsp; ".join(nav)}</div>\n'

    return head(f"{e['name']} — Evolving Agents Labs", e["blurb"], "/assets/site.css") + f"""
{masthead("/", "/archive/")}
<div class="wrap narrow">

  <p class="crumb"><a href="/">ai-os</a><span>/</span><a href="/archive/">Archive</a><span>/</span>{e['name']}</p>

  <section class="detail-hero">
    <h1>{e['name']}</h1>
    <p class="question">{e['question']}</p>
    <div class="hero-meta">
      {badge_html}<span class="when">{e['date']}</span>
    </div>
    <div class="ctas">
      {chr(10).join("      " + c for c in ctas).strip()}
    </div>
  </section>

{figure}
  <article class="article">
{body}  </article>

{navhtml}{FOOT}

</div>

</body>
</html>
"""


def build_thesis():
    return head(
        "What we are actually testing — Evolving Agents Labs",
        "Three mechanisms that kept working across eight experiments, the ones that did not, and where they point.",
        "/assets/site.css") + f"""
{masthead("/", "/archive/")}
<div class="wrap narrow">

  <p class="crumb"><a href="/">ai-os</a><span>/</span><a href="/archive/">Archive</a><span>/</span>Thesis</p>

  <section class="detail-hero">
    <h1>What we are actually testing</h1>
    <p class="question">Not whether an agent can do something — how you would know it did.</p>
  </section>

  <article class="article">
{THESIS}  </article>

{FOOT}

</div>

</body>
</html>
"""


def main():
    exps = sorted(EXPERIMENTS, key=lambda x: x["sort"], reverse=True)

    os.makedirs(f"{OUT}/assets", exist_ok=True)
    with open(f"{OUT}/assets/site.css", "w") as f:
        f.write(CSS)

    # The listing goes to /archive/, never to /index.html. It was the home once;
    # the home is ai-os now, hand-written, and pointing this at the site root
    # would silently replace it with a page about twenty-six frozen experiments.
    # A generator that can destroy the thing it is not the source of is not a
    # convenience.
    os.makedirs(f"{OUT}/archive", exist_ok=True)
    with open(f"{OUT}/archive/index.html", "w") as f:
        f.write(build_index(exps))

    os.makedirs(f"{OUT}/thesis", exist_ok=True)
    with open(f"{OUT}/thesis/index.html", "w") as f:
        f.write(build_thesis())

    d = f"{OUT}/experiments/{ORIGIN['slug']}"
    os.makedirs(d, exist_ok=True)
    with open(f"{d}/index.html", "w") as f:
        f.write(build_detail(ORIGIN, None, None))

    for i, e in enumerate(exps):
        d = f"{OUT}/experiments/{e['slug']}"
        os.makedirs(d, exist_ok=True)
        prev_e = exps[i - 1] if i > 0 else None
        next_e = exps[i + 1] if i < len(exps) - 1 else None
        with open(f"{d}/index.html", "w") as f:
            f.write(build_detail(e, prev_e, next_e))

    print(f"wrote archive/ + {len(exps)} detail pages to {OUT}/")


if __name__ == "__main__":
    main()
