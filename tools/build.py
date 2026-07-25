#!/usr/bin/env python3
"""Render the Evolving Agents Labs site. Output is committed; this is not a build step."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import EXPERIMENTS, BADGES

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"

CSS = """/* Evolving Agents Labs — shared styles. Hand-written; no preprocessor. */
:root{
  --paper:#F5F5F2; --ground:#FFFFFF;
  --ink:#15171B; --ink-2:#4A4F58; --ink-3:#767C86;
  --rule:#DEDEDA; --rule-strong:#C4C4BF;
  --accent:#3E52A3; --signal:#8A5C10;
  --serif:"Newsreader",Georgia,"Times New Roman",serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --pad:clamp(1.25rem,5vw,3rem);
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#0F1114; --ground:#15181C;
    --ink:#E8E8E4; --ink-2:#A8ADB6; --ink-3:#767C86;
    --rule:#262A30; --rule-strong:#363B43;
    --accent:#8B9BE0; --signal:#D9A441;
  }
}
:root[data-theme="dark"]{
  --paper:#0F1114; --ground:#15181C;
  --ink:#E8E8E4; --ink-2:#A8ADB6; --ink-3:#767C86;
  --rule:#262A30; --rule-strong:#363B43;
  --accent:#8B9BE0; --signal:#D9A441;
}
:root[data-theme="light"]{
  --paper:#F5F5F2; --ground:#FFFFFF;
  --ink:#15171B; --ink-2:#4A4F58; --ink-3:#767C86;
  --rule:#DEDEDA; --rule-strong:#C4C4BF;
  --accent:#3E52A3; --signal:#8A5C10;
}
*{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:16px;line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px;}
.wrap{max-width:min(64rem,100%);margin:0 auto;padding-inline:var(--pad);}
.wrap.narrow{max-width:min(46rem,100%);}

/* masthead */
.masthead{
  display:flex;align-items:baseline;justify-content:space-between;
  gap:1.5rem;flex-wrap:wrap;padding-block:1.75rem 1.5rem;
  border-bottom:1px solid var(--rule);
}
.wordmark{
  font-family:var(--mono);font-size:.8125rem;font-weight:500;
  letter-spacing:.08em;text-transform:uppercase;text-decoration:none;color:inherit;
}
.wordmark .mark{color:var(--accent);margin-right:.45em;}
.navlinks{display:flex;gap:1.5rem;font-family:var(--mono);font-size:.75rem;letter-spacing:.04em;}
.navlinks a{color:var(--ink-2);text-decoration:none;transition:color .15s;}
.navlinks a:hover{color:var(--accent);}

/* index hero */
.hero{padding-block:clamp(3rem,9vw,5.5rem) clamp(2.5rem,6vw,4rem);}
.hero h1{
  font-family:var(--serif);font-weight:300;
  font-size:clamp(2rem,5.4vw,3.5rem);line-height:1.12;
  letter-spacing:-.018em;margin:0 0 1.5rem;max-width:22ch;text-wrap:balance;
}
.hero h1 em{font-style:italic;color:var(--accent);}
.hero p{margin:0;max-width:66ch;color:var(--ink-2);font-size:1.0625rem;line-height:1.65;}
.hero p + p{margin-top:1rem;}
.hero .who{
  margin-top:1.75rem;padding-top:1.25rem;
  border-top:1px solid var(--rule);
  font-size:.9375rem;color:var(--ink-3);
}
.hero .who a{color:var(--ink-2);text-decoration-thickness:1px;text-underline-offset:2px;}
.hero .who a:hover{color:var(--accent);}

/* legend */
.legend{
  display:flex;flex-wrap:wrap;gap:.6rem 1.75rem;
  padding-block:1.25rem;border-block:1px solid var(--rule);
  font-family:var(--mono);font-size:.75rem;color:var(--ink-3);
}
.legend div{display:flex;align-items:center;gap:.5rem;}

.badge{
  font-family:var(--mono);font-size:.6875rem;font-weight:500;
  letter-spacing:.06em;text-transform:uppercase;
  padding:.2em .55em;border:1px solid currentColor;border-radius:2px;
  white-space:nowrap;line-height:1.3;
}
.badge.reproducible{color:var(--accent);}
.badge.results{color:var(--signal);}
.badge.prototype{color:var(--ink-3);}

/* index listing */
.listing{padding-block:1rem 4rem;}
.sectionlabel{
  font-family:var(--mono);font-size:.6875rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3);margin:0;padding-block:2.25rem 1rem;
}
.row{
  display:grid;grid-template-columns:minmax(11rem,14rem) 1fr auto;
  gap:.5rem 2rem;align-items:start;
  padding:1.5rem .875rem;margin-inline:-.875rem;
  border-bottom:1px solid var(--rule);
  text-decoration:none;color:inherit;border-radius:3px;
  transition:background-color .18s ease;
}
.row:first-of-type{border-top:1px solid var(--rule-strong);}
.row:hover{background:var(--ground);}
.row:hover .name{color:var(--accent);}
.row:hover .arrow{transform:translateX(3px);opacity:1;}
.rowhead{display:flex;flex-direction:column;gap:.55rem;align-items:flex-start;}
.name{font-family:var(--mono);font-size:.9375rem;font-weight:500;letter-spacing:-.01em;transition:color .18s;}
.question{
  font-family:var(--serif);font-weight:300;
  font-size:clamp(1.125rem,2.1vw,1.4375rem);
  line-height:1.34;letter-spacing:-.012em;margin:0;max-width:44ch;text-wrap:balance;
}
.note{margin:.6rem 0 0;font-size:.875rem;line-height:1.55;color:var(--ink-2);max-width:52ch;}
.meta{
  display:flex;align-items:center;gap:.85rem;
  font-family:var(--mono);font-size:.75rem;color:var(--ink-3);
  font-variant-numeric:tabular-nums;white-space:nowrap;
}
.arrow{opacity:.45;transition:transform .18s ease,opacity .18s ease;}
@media (max-width:44rem){
  .row{grid-template-columns:1fr;gap:.85rem;padding-block:1.375rem;}
  .rowhead{flex-direction:row;align-items:center;gap:.75rem;flex-wrap:wrap;}
  .meta{order:3;}
}

/* detail page */
.crumb{
  font-family:var(--mono);font-size:.6875rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);padding-block:2rem .5rem;
}
.crumb a{color:var(--ink-3);text-decoration:none;}
.crumb a:hover{color:var(--accent);}
.crumb span{margin-inline:.5em;opacity:.5;}
.detail-hero{padding-block:.5rem 2rem;border-bottom:1px solid var(--rule);}
.detail-hero h1{
  font-family:var(--mono);font-weight:500;
  font-size:clamp(1.5rem,3.6vw,2rem);letter-spacing:-.02em;margin:0 0 1rem;
}
.detail-hero .question{
  font-size:clamp(1.375rem,3.2vw,1.875rem);margin:0 0 1.5rem;max-width:30ch;color:var(--ink);
}
.hero-meta{display:flex;align-items:center;gap:.85rem;flex-wrap:wrap;margin-bottom:1.75rem;}
.hero-meta .when{font-family:var(--mono);font-size:.75rem;color:var(--ink-3);}
.ctas{display:flex;gap:.75rem;flex-wrap:wrap;}
.cta{
  display:inline-flex;align-items:center;gap:.5rem;
  font-family:var(--mono);font-size:.8125rem;
  padding:.6rem 1rem;border:1px solid var(--rule-strong);border-radius:3px;
  text-decoration:none;color:var(--ink);background:var(--ground);
  transition:border-color .18s,color .18s;
}
.cta:hover{border-color:var(--accent);color:var(--accent);}
.cta.primary{border-color:var(--accent);color:var(--accent);}

.article{padding-block:2.5rem 3rem;}
.article h2{
  font-family:var(--serif);font-weight:400;
  font-size:clamp(1.375rem,2.6vw,1.75rem);line-height:1.25;letter-spacing:-.012em;
  margin:2.75rem 0 1rem;text-wrap:balance;
}
.article h2:first-child{margin-top:0;}
.article p{margin:0 0 1.15rem;color:var(--ink-2);}
.article strong{color:var(--ink);font-weight:600;}
.article em{color:var(--ink);}
.article a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px;}
.article ul{margin:0 0 1.15rem;padding-left:1.25rem;color:var(--ink-2);}
.article li{margin-bottom:.5rem;}
.article code{
  font-family:var(--mono);font-size:.875em;
  background:var(--ground);border:1px solid var(--rule);border-radius:3px;padding:.1em .35em;
}
.article pre{
  background:var(--ground);border:1px solid var(--rule);border-radius:4px;
  padding:1rem;overflow-x:auto;margin:0 0 1.15rem;
}
.article pre code{background:none;border:none;padding:0;font-size:.8125rem;line-height:1.7;}

.nextprev{
  border-top:1px solid var(--rule-strong);padding-block:2rem 1rem;
  font-family:var(--mono);font-size:.8125rem;
}
.nextprev a{color:var(--accent);text-decoration:none;}
.nextprev a:hover{text-decoration:underline;}

.foot{
  border-top:1px solid var(--rule-strong);
  padding-block:2.5rem 3.5rem;
  display:flex;flex-direction:column;gap:.75rem;
  font-family:var(--mono);font-size:.75rem;color:var(--ink-3);
}
.foot .by{max-width:62ch;line-height:1.7;color:var(--ink-2);}
.foot .meta-foot{color:var(--ink-3);}
.foot a{color:var(--ink-2);text-decoration:none;}
.foot a:hover{color:var(--accent);}
@media (prefers-reduced-motion:reduce){*{transition:none !important;animation:none !important;}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 32 32'><text y='25' font-size='24'>%E2%97%88</text></svg>\">")

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


def masthead(prefix):
    return f"""  <header class="masthead">
    <a class="wordmark" href="{prefix}"><span class="mark">◈</span>Evolving Agents Labs</a>
    <nav class="navlinks">
      <a href="{prefix}#experiments">Experiments</a>
      <a href="{prefix}#method">Method</a>
      <a href="https://github.com/EvolvingAgentsLabs">GitHub</a>
    </nav>
  </header>
"""


def build_index(exps):
    rows = []
    for e in exps:
        label, _ = BADGES[e["badge"]]
        rows.append(f"""    <a class="row" href="/experiments/{e['slug']}/">
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
<div class="wrap">

{masthead("/")}
  <section class="hero">
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

    <p class="sectionlabel">2026</p>

{chr(10).join(rows)}

  </main>

{FOOT}

</div>

</body>
</html>
"""


def build_detail(e, prev_e, next_e):
    label, _ = BADGES[e["badge"]]
    ctas = [f'<a class="cta primary" href="{e["repo"]}">GitHub <span aria-hidden="true">→</span></a>']
    if e.get("demo"):
        ctas.insert(0, f'<a class="cta" href="{e["demo"]}">Demo <span aria-hidden="true">→</span></a>')

    body = "\n".join(
        f"    <h2>{title}</h2>{content.rstrip()}\n" for title, content in e["sections"])

    nav = []
    if prev_e:
        nav.append(f'<a href="/experiments/{prev_e["slug"]}/">← {prev_e["name"]}</a>')
    if next_e:
        nav.append(f'<a href="/experiments/{next_e["slug"]}/">{next_e["name"]} →</a>')
    navhtml = ""
    if nav:
        navhtml = f'  <div class="nextprev">{" &nbsp;·&nbsp; ".join(nav)}</div>\n'

    return head(f"{e['name']} — Evolving Agents Labs", e["blurb"], "/assets/site.css") + f"""
<div class="wrap narrow">

{masthead("/")}
  <p class="crumb"><a href="/">Evolving Agents Labs</a><span>/</span><a href="/#experiments">Experiments</a><span>/</span>{e['name']}</p>

  <section class="detail-hero">
    <h1>{e['name']}</h1>
    <p class="question">{e['question']}</p>
    <div class="hero-meta">
      <span class="badge {e['badge']}">{label}</span>
      <span class="when">{e['date']}</span>
    </div>
    <div class="ctas">
      {chr(10).join("      " + c for c in ctas).strip()}
    </div>
  </section>

  <article class="article">
{body}  </article>

{navhtml}{FOOT}

</div>

</body>
</html>
"""


def main():
    exps = sorted(EXPERIMENTS, key=lambda x: x["sort"], reverse=True)

    os.makedirs(f"{OUT}/assets", exist_ok=True)
    with open(f"{OUT}/assets/site.css", "w") as f:
        f.write(CSS)

    with open(f"{OUT}/index.html", "w") as f:
        f.write(build_index(exps))

    for i, e in enumerate(exps):
        d = f"{OUT}/experiments/{e['slug']}"
        os.makedirs(d, exist_ok=True)
        prev_e = exps[i - 1] if i > 0 else None
        next_e = exps[i + 1] if i < len(exps) - 1 else None
        with open(f"{d}/index.html", "w") as f:
            f.write(build_detail(e, prev_e, next_e))

    print(f"wrote index + {len(exps)} detail pages to {OUT}/")


if __name__ == "__main__":
    main()
