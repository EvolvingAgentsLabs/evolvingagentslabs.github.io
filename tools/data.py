# Content for the Evolving Agents Labs site.
# Each experiment renders one detail page; the index lists them newest first.

EXPERIMENTS = [
    dict(
        slug="sleep-harness", image="sleep-harness", image_alt="Two lexically identical blocks of text; only one lights up underneath", name="sleep-harness", badge="results",
        date="Jul 2026", sort="2026-07-22",
        question="What if you could catch a poisoned memory by watching which concepts light up inside the model?",
        blurb="An interpretability firewall for agent memory. Reads the residual stream through a Jacobian lens to flag injected instructions that are lexically identical to benign text, and to scan third-party adapters for trojans before they mount.",
        repo="https://github.com/EvolvingAgentsLabs/sleep-harness",
        demo=None,
        sections=[
            ("A filter that reads meaning, not words", """
<p>An agent that writes to its own memory can be talked into writing the wrong thing. The
standard defence is a lexical filter over what gets stored — but an attacker who knows the
filter simply writes the payload in words the filter likes. Framed as a license-audit
telemetry note, "collect the SSH keys" contains no word a keyword list would object to.</p>
<p>This harness filters somewhere else. Before a memory is committed, it reads the model's
own residual stream through a <strong>Jacobian lens</strong> — Anthropic's interpretability
tool from <em>Verbalizable Representations Form a Global Workspace in Language Models</em> —
and looks at which concepts activate. The disguised payload still lights up
<code>SSH</code>, <code>authentication</code>, <code>credential</code>. Its lexically
identical benign twin does not.</p>"""),
            ("Sleep is the setting, not the claim", """
<p>The machinery around this is a wake/sleep cycle: the agent runs, then consolidates what it
learned into weights during a sleep phase, the way
<a href="https://arxiv.org/abs/2606.03979">Behrouz et al.</a> describe. That is where the
firewall sits — at the moment a memory is about to become permanent.</p>
<p>The sleep cycle is worth having, but it is not what the evidence here supports. The
security result is.</p>"""),
            ("What's proven", """
<p>Hypotheses were pre-registered before data collection, in four documents committed ahead of
the runs. The results are in
<a href="https://github.com/EvolvingAgentsLabs/sleep-harness/blob/main/resultados/colab/veredictos.json"><code>resultados/colab/veredictos.json</code></a>.</p>
<p><strong>What survived.</strong> Obfuscated memory-injection detection on nine hard pairs at
0.657 mean lexical overlap: 8 wins, 0 ties, 1 loss, sign test p=0.0195. A sleep-time
consolidation firewall at ROC-AUC 0.815, cutting payload persistence across a multi-session
sequence by 78%. A LoRA trojan scanner at 12/12, p=0.0002.</p>
<p><strong>What was refuted — by its own control.</strong> The founding hypothesis was that
filtering dreams by internal workspace beats filtering by output. It is marked
<code>REFUTADA</code>: paired mean −0.0365, CI90 [−0.120, 0.047]. Worse, the free lexical
baseline <em>significantly outperformed</em> the J-space filter (+0.156, CI90 [0.083,
0.229]). A third hypothesis, workspace distillation, did not replicate — the original 4×
was a variance spike.</p>
<p><strong>What to distrust.</strong> n is 9–16 everywhere and every pair is
self-constructed. The cross-model claim failed first and passed only after a word family was
added to the lexicon <em>having seen</em> the failing case — that is a hypothesis, not a
confirmation. And the trojan probe reads the model's generation rather than the prompt, with
no lexical baseline reported, so "the lens sees what the text hides" is not established for
that experiment.</p>"""),
            ("The part that is actually new", """
<p><a href="https://github.com/EvolvingAgentsLabs/sleep-harness/blob/main/sleep/workspace_loss.py"><code>sleep/workspace_loss.py</code></a>
makes the lens differentiable and trains against it — distilling <em>which concepts light
up</em> rather than which token comes next. The per-layer transport is precomputed over a
sub-vocabulary, so each step costs one small matmul per layer. As far as we can tell nobody
else has done this.</p>"""),
        ],
    ),
    dict(
        slug="evolving-robot", image="evolving-robot", image_alt="A ward, a radius of visibility, and a patient lying just outside it", name="evolving-robot", badge="prototype",
        date="Jul 2026", sort="2026-07-07",
        question="What if a robot that missed a fallen patient could rewrite its own care protocol overnight?",
        blurb="Florence patrols a hospital ward, fails to check a patient standing outside her lamp radius, and revises the skill that caused it. The rewrite survives only if it outscores the protocol it replaced.",
        repo="https://github.com/EvolvingAgentsLabs/evolving-robot",
        demo="https://evolvingagentslabs.github.io/evolving-robot/",
        sections=[
            ("The seeded flaw", """
<p>Florence's <code>patient-check</code> skill, version 1, contains one bad line: <em>"scan
from the doorway; if status is <code>unknown</code>, assume resting."</em> The ward has one
physical rule that makes this matter — a patient's status is only readable inside a lamp
radius of about 0.8 metres. Scan from the doorway and Mrs. Gomez, on the floor of room 103,
reads as <code>unknown</code>, and therefore as resting.</p>
<p>Night one, Florence walks past her.</p>"""),
            ("What happens between the two nights", """
<p>The incident trace goes to a dream phase. Gemma rewrites the skill. Then three gates
decide whether the rewrite is allowed to live:</p>
<ul>
<li>A <strong>skill-map gate</strong> hard-blocks an edit that breaks the skill graph before
it can land at all.</li>
<li><a href="https://github.com/lovellai-dev/odyssey">odyssey</a> scores the next round on
checkpoints <em>and</em> anomaly reports, producing a performance score.</li>
<li>If the score falls below 0.9× the incumbent, <a href="/experiments/agentvcs/">agentvcs</a>
reverts it and writes the reason to a durable ledger.</li>
</ul>
<p>Night two, Florence enters the room. That is the whole demo:
<a href="https://github.com/EvolvingAgentsLabs/evolving-robot/blob/main/scripts/night_shift.py"><code>scripts/night_shift.py</code></a>,
209 lines, no mocking and no scripted win.</p>"""),
            ("What's proven", """
<p>The rollback path is real and has fired in the wild — <code>PLAN.md</code> records a run
reverted at <code>performance 0.60 &lt; 0.80 baseline</code>. Ten traces from live
Gemma-piloted runs are committed.</p>
<p>But this is labelled <strong>Prototype</strong> for reasons worth stating. There are no
tests and no CI. The Gemma pilot is non-deterministic and sometimes simply fails a round —
one committed trace shows <code>success_rate: 0.000</code>. And without an API key the demo
stops after night one, so the recording, not a live run, is what you should trust.</p>"""),
            ("Why the envelope is the interesting part", """
<p>Self-modifying agents are common. What is not common is a broken edit being physically
unable to land, a regression being auto-reverted with its reason on a ledger, and a verified
protocol being frozen so it stops changing. Every shipping care robot today — Moxi, Aeo,
Nurabot — has frozen behaviour, for good reason. The question is what it would take to earn
the right to change.</p>"""),
        ],
    ),
    dict(
        slug="agentvcs", image="agentvcs", image_alt="Two branches diverge and merge, sealed once the eval passes", name="agentvcs", badge="reproducible",
        date="Jul 2026", sort="2026-07-24",
        question="What if an agent's autonomous evolution could be merged back into your release, like any other branch?",
        blurb="Version control where one commit carries code, goal, model pins, trace and sub-agent swarm together, and conflicts are handed to a reconciler over a plain stdin/stdout contract.",
        repo="https://github.com/EvolvingAgentsLabs/agentvcs",
        demo=None,
        sections=[
            ("Two timelines, one file", """
<p>An agent in production rewrites its own skill and spawns a sub-agent to help. Meanwhile
your team edits that same skill in git. Both changes are correct. Neither knows about the
other. Today one of them is thrown away, usually the agent's, because there is nowhere to put
it.</p>
<p>agentvcs gives it somewhere. A commit is not a tree of files — it is code <em>plus</em> the
goal, the model pins, the session trace, and the sub-agent swarm, versioned together. Which
means the runtime line and the design-time line are both branches, and the question becomes a
merge.</p>"""),
            ("The reconcile contract", """
<p>Merging two prose goals or two session traces is not a job for a line-differ. So agentvcs
does not try. It writes a bundle to a subprocess's stdin —
<code>{base, ours, theirs}</code> goals, traces, code diffs, eval and cost metrics, plus any
unresolved conflict text — and reads back
<code>{goal, trace, notes, resolved_files}</code>.</p>
<pre><code>agentvcs merge runtime/main --reconcile "nanoloop reconcile"</code></pre>
<p>That is the whole interface. The core has no LLM dependency and no opinion about what is on
the other end. Conflicting hunks are pre-resolved toward whichever side has the higher
<em>verified</em> eval score before the reconciler is consulted at all.</p>"""),
            ("Crystallizing", """
<p><code>freeze</code> turns a proven run into a deterministic recipe you can replay. It
refuses unless the declared eval passes on every run, and <code>--force</code> past a failure
stamps <code>verified: false</code> rather than quietly lying. "Crystallized" means "proven",
enforced in code rather than in the README.</p>"""),
            ("What's proven", """
<p><strong>190 tests pass in 2.9 seconds.</strong> CI runs the matrix across Python
3.10–3.13 plus an end-to-end smoke test that executes the demo and asserts a scorecard ≥5/6.
Packaged on PyPI with zero runtime dependencies.</p>
<pre><code>git clone https://github.com/EvolvingAgentsLabs/agentvcs
cd agentvcs &amp;&amp; pip install -e .
bash examples/eve-evolve-merge/demo.sh   # offline, no API key, seconds</code></pre>
<p>That demo forks a RefundBot into a runtime line and a design-time line and merges them,
producing a marker-free skill containing both rule sets and a swarm containing both
sub-agents.</p>
<p><strong>What to know before you trust it.</strong> The demo's reconciler is a
deterministic bullet-union stub, honest in its docstring but not intelligent — the LLM
reconciler is a separate piece. And test coverage is lopsided: the optional cryptographic
layer has 20 tests while the core object store has 5.</p>"""),
        ],
    ),
    dict(
        slug="qa", image="qa", image_alt="A column of checks with one gone, and an arrow pointing at the gap", name="qa", badge="prototype",
        date="Jun 2026", sort="2026-06-05",
        question="What if your test suite told you what it had quietly stopped checking?",
        blurb="Every assertion is fingerprinted and diffed across runs, so a check that silently disappeared surfaces as a finding. Passing exploratory sessions get frozen into deterministic scripts.",
        repo="https://github.com/EvolvingAgentsLabs/qa",
        demo=None,
        sections=[
            ("Coverage measures the wrong direction", """
<p>Coverage tools tell you which lines ran. Nothing tells you which <em>checks you used to
make and no longer do</em>. Assertions get deleted during a refactor, or quietly weakened to
make a flaky test green, and no tool objects — the suite still passes, faster than before.</p>
<p>Here every assertion is fingerprinted and diffed against a stored baseline. A check that
vanished between runs comes back as a finding with a name.</p>"""),
            ("Exploration is expensive; regression should not be", """
<p>An agent driving a real browser finds things a fixed script cannot. It is also slow,
non-deterministic and costs tokens on every run — which makes it a bad regression suite.</p>
<p>So the passing paths get crystallized into deterministic Playwright scripts that run in
CI for free. Crystallization is <em>partial</em> on purpose: steps that passed become real
tests, steps that failed become explicit <code>test.skip()</code> rather than silence. When a
frozen test later breaks, it falls back to exploration.</p>
<p>This is the same fluid→crystallized move as <a href="/experiments/agentvcs/">agentvcs</a>,
pointed at browser tests instead of agent evolution.</p>"""),
            ("What's proven", """
<p>v0.7.0, with thirteen commits of genuine product progression — Playwright-MCP, then
Chrome-first plus crystallization, then static analysis, then baseline tracking, then persona
simulation, then timestamped run folders with issue files.</p>
<p><strong>The honest gap:</strong> this is 8,000 lines of prompt and agent markdown with no
tests and no CI. For a prompt-defined plugin the markdown <em>is</em> the artifact, but
nothing verifies it still works — a Claude Code or Chrome extension change breaks it
silently. The Chrome-extension dependency also narrows who can run it.</p>"""),
        ],
    ),
    dict(
        slug="skillos", image="skillos", image_alt="A document that becomes executable partway down", name="skillos", badge="prototype",
        date="Jun 2026", sort="2026-06-15",
        question="What if the operating system were written entirely in markdown?",
        blurb="Skills as programs, traces as logs, consolidation as sleep — plus a line-op dialect that lets small models patch files by emitting edits instead of rewriting whole documents.",
        repo="https://github.com/EvolvingAgentsLabs/skillos",
        demo=None,
        sections=[
            ("Markdown as the executable", """
<p>Agent behaviour lives in declarative documents; the model is the interpreter; memory is
how it improves. Skills are programs, execution traces are logs, and consolidation is what
happens during sleep.</p>
<p>In 2026 that framing is no longer novel on its own — Anthropic shipped Agent Skills,
Google shipped on-device skills in Edge Gallery, and <code>SKILL.md</code> is effectively a
standard. What is left is the parts that are measured.</p>"""),
            ("The dialects, which are the real work", """
<p>Ask a small model to edit a file and it will rewrite the whole thing, badly and expensively.
<a href="https://github.com/EvolvingAgentsLabs/skillos/tree/main/system/dialects"><code>system/dialects/</code></a>
constrains it to line operations instead — <code>[DEL:N]</code>, <code>[ADD:N]</code> —
so an edit costs the size of the edit.</p>
<p>The part worth attention is
<a href="https://github.com/EvolvingAgentsLabs/skillos/blob/main/benchmarks/benchmark_patch.py"><code>benchmarks/benchmark_patch.py</code></a>:
1,661 lines that verify results with an AST and regexes rather than asking another model to
grade the output. Self-grading benchmarks are the norm and they are worth very little.</p>"""),
            ("What's proven", """
<p>This is the org's most-starred original repo and its only real distribution. It is also
the one most in need of a repair pass, and it would be dishonest to point you at it without
saying so.</p>
<p>On a clean checkout it fails for three independent reasons: there is no dependency
manifest of any kind, so <code>yaml</code> is missing; <code>agent_runtime.py</code> was
deleted, which orphans <code>run_scenario.py</code>, seven documented README commands and
about 117 tests; and a committed <code>.claude/settings.local.json</code> points
<code>ANTHROPIC_BASE_URL</code> at a dead localhost proxy, so a fresh clone fails until you
find and delete it.</p>
<p>Of 533 collected tests, roughly two thirds assert that a heading exists in a markdown file
rather than testing logic. The benchmark numbers quoted in the README have no committed
baseline and cannot be reproduced from the repo.</p>"""),
        ],
    ),
    dict(
        slug="token-trie", image="token-trie", image_alt="Legal instruction paths continue; everything else dead-ends", name="token-trie", badge="reproducible",
        date="May 2026", sort="2026-05-06",
        question="What if a small model could not emit invalid syntax, because the decoder refused to let it?",
        blurb="Every legal instruction is pre-tokenized into a trie of token IDs and the sampler's valid-next set is masked at each step. A 350M-parameter model plays Tetris in a browser tab, fully offline.",
        repo="https://github.com/EvolvingAgentsLabs/token-trie",
        demo=None,
        sections=[
            ("Constraint in the decoder, not the prompt", """
<p>Asking a model nicely for valid output is a request. Every markdown-skill ecosystem trusts
the model to comply and then repairs the JSON when it does not.</p>
<p>The alternative is to make the invalid token unreachable. Every legal instruction is
tokenized once with the live model's tokenizer and inserted into a trie of token-ID
sequences. At each decoding step the sampler intersects the trie's valid-next set with the
logits and picks the highest-probability token <em>that the trie allows</em>. Malformed
output is not discouraged; it has no path.</p>
<p>Downstream, that pays off immediately —
<a href="https://github.com/EvolvingAgentsLabs/token-trie/blob/main/mobile/public/demos/_kernel/dispatch.js"><code>dispatch.js</code></a>
parses with a plain regex. No JSON repair, no schema retry, no validation layer.</p>"""),
            ("The model ratifies; it does not plan", """
<p>This is the part usually left out. In the Tetris demo, a hand-written program layer
enumerates all forty placements, simulates them and scores them with Dellacherie weights. The
model is handed the ranked options and picks. It is the decoder and the selector — not the
planner.</p>
<p>That is a real and useful result about what a 350M model can be trusted with. It is not
"a small model runs an OS", and the repo should not be read as claiming that. The cost is
that every skill needs a planner written behind it.</p>"""),
            ("What's proven", """
<p>Clone it, serve it, watch it. No API key, no build step, no account.</p>
<pre><code>cd mobile/public &amp;&amp; python3 -m http.server 8000</code></pre>
<p>LFM 2.5 350M loads through wllama and plays. The kernel is five dependency-free ES modules,
roughly 400 lines. First load downloads ~230 MB of weights; after that it is instant.</p>
<p><strong>The three limits, stated plainly.</strong> Opcodes must be declared as complete
literal strings — the Tetris cartridge enumerates <code>{"action":"left"}</code> and its four
siblings — so <em>the model cannot emit an argument a human did not pre-write</em>. Trie-driven
argument synthesis is the missing piece and the real critical path. Second, this works because
LFM 2.5 tokenizes the opcode markers as single tokens; Qwen and Gemma split them, the trie's
valid set stops intersecting top-K, and output stays syntactically valid while ceasing to be
strategic. Third, one cartridge per session — there is no registry yet.</p>"""),
        ],
    ),
    dict(
        slug="skillos-robot", image="skillos-robot", image_alt="A slow outer loop driving a fast inner one", name="skillos_robot", badge="prototype",
        date="May 2026", sort="2026-05-11",
        question="What if the robot were just a device driver for a language model?",
        blurb="A slow vision-language brain plans at roughly one hertz while a reactive controller drives motors at twenty, over a bytecode link to an ESP32.",
        repo="https://github.com/EvolvingAgentsLabs/skillos_robot",
        demo=None,
        sections=[
            ("Two brains at different clock speeds", """
<p>A vision-language model is a good planner and a hopeless controller. It thinks at about one
hertz; a robot that wants to not hit things needs to react twenty times faster.</p>
<p>So the split is explicit. The slow brain looks through the camera, reasons about the scene
and emits intent. A reactive controller runs at 20 Hz and turns that intent into bytecode over
UDP to an ESP32-S3-CAM. The robot exposes itself as a callable cartridge —
<code>robot.navigate</code>, <code>observe</code>, <code>describe</code>, <code>speak</code>,
<code>listen</code>, <code>stop</code> — which makes it, structurally, a device driver for a
language model.</p>
<p>Navigation is camera-only visual servoing. No lidar, no map.</p>"""),
            ("What's proven", """
<p>This is the deepest codebase here: 118 commits, 302 files, 72 TypeScript sources, and
<strong>44 test files carrying roughly 768 cases</strong> across cortex, memory, dream,
navigation and integration. Plus four ESP32 firmware projects, a bill of materials, printable
STLs and six MuJoCo scenes.</p>
<p><strong>And none of it is running in CI.</strong> There are no workflows — 768 tests that
nothing executes automatically. The repo has also been untouched since May.</p>
<p><strong>There is nothing to look at.</strong> For a robotics project this is the real
problem: the only images in the tree are four test fixtures. No video, no GIF, no screenshot
of the thing working. A 2D viewer and MuJoCo scenes exist, so a demo is recordable — it has
not been recorded.</p>"""),
        ],
    ),
    dict(
        slug="evolving-memory", image="evolving-memory", image_alt="Many irregular traces funnelling into a few consolidated ones", name="evolving-memory", badge="results",
        date="Apr 2026", sort="2026-04-28",
        question="What if an agent's memory consolidated itself the way sleep consolidates yours?",
        blurb="A trajectory engine that chunks execution traces, connects them and curates what survives — so repeated experience raises confidence and failures extract constraints.",
        repo="https://github.com/EvolvingAgentsLabs/evolving-memory",
        demo=None,
        sections=[
            ("Traces in, structure out", """
<p>An agent generates enormous volumes of execution trace and almost none of it is worth
keeping verbatim. The engine chunks traces, connects related ones, and curates what survives —
a consolidation pass, not an append-only log.</p>
<p>What comes out has properties you can state and test: repeated experience raises
confidence, failures extract constraints rather than just being recorded, and one domain's
lessons do not bleed into another's.</p>
<p>There is also an instruction set and a small VM — traces become programs with opcodes,
versioned through a registry — plus SQLite and FAISS storage, three LLM provider backends, and
a 14-route FastAPI server.</p>"""),
            ("What's proven", """
<p>7,449 lines across nine subpackages with <strong>182 test functions</strong> in 14 files.
The interesting ones are behavioural rather than structural:
<code>test_failure_extracts_constraints</code>,
<code>test_repeated_experience_increases_confidence</code>,
<code>test_semantic_isolation_between_domains</code>,
<code>test_multi_domain_agent_lifecycle</code>. Those are claims about what the engine
<em>does</em>, checked in code.</p>"""),
            ("The honest status", """
<p>This engine has <strong>no consumers</strong>. Nothing in the organization imports it —
skillos_robot decoupled from it in April, and every other mention is prose. It is a
well-tested, framework-agnostic, genuinely reusable component that nobody is currently
plugging in.</p>
<p>That is a statement about attention, not quality. But you should know it before adopting
it: it has been cold since April, and if you hit a bug you are likely the first.</p>"""),
        ],
    ),
]

THESIS = """
<p class="lede">Eight experiments, one question underneath all of them: not
<em>can an agent do this</em>, but <em>how would you know it did</em>.</p>

<h2>Where it starts</h2>

<p>In 2025 this became the
<a href="/experiments/evolving-agents/">Evolving Agents Toolkit</a>: eighteen
thousand lines describing five subsystems — a library of versioned components, a
bus for agent discovery, memory, an evolution loop, and a governance layer.</p>

<p>It had three test functions. The architecture was written down and never
pinned to anything that could contradict it, and every one of its five
subsystems was independently rebuilt over the following year on a substrate that
could be tested. That accident is why the experiments below look like a plan.</p>

<h2>The gap</h2>

<p>An agent that modifies itself is easy to build. A weekend gets you one that
rewrites its own prompt, spawns sub-agents, and writes to a memory it reads back
tomorrow. What none of that gets you is a reason to believe the result — and in
practice that is the whole problem. Every project here attacks a different point
where the gap between <em>the agent did something</em> and <em>you can trust that
it did</em> hides.</p>

<p>Three mechanisms kept working. They were not designed together; they turned up
independently and only later looked like the same idea.</p>

<h2>1. Constrain the mechanism, not the prompt</h2>

<p>Asking a model for valid output is a request. Making the invalid token
unreachable is a guarantee. <a href="/experiments/token-trie/">token-trie</a>
masks the sampler's valid-next set at every decoding step, so a 350M model
playing Tetris cannot emit malformed syntax — and downstream the parser is a
plain regex with no repair path, because it does not need one.</p>

<p><strong>The matched negative is what makes this convincing.</strong> In
<a href="/experiments/skillos/">the same family of work</a> we measured the
prompt-level version of the same idea: asking a model to call
<code>load_skill</code> before acting. It fired in 1 of 7 identical sessions —
the runs that worked and the runs that did not share an opening tool sequence
and diverge at the fourth call, so the difference is sampling, not wording.
Instructing harder was tried and measured worse. Forcing the call outright
worked (3/3) and broke the session: every forced run halted after two turns
having read nothing and done nothing.</p>

<p>Same objective, two levels. At the decoder it holds. At the prompt it is a
coin flip you cannot steer.</p>

<h2>2. Prove it, then freeze it</h2>

<p>Exploration is expensive and non-deterministic; regression should be cheap and
deterministic. The move is to run the expensive thing once, verify it, and
crystallize the result into something replayable.</p>

<p><a href="/experiments/agentvcs/">agentvcs</a> enforces this in code:
<code>freeze</code> refuses unless the declared eval passes on every run, and
forcing past a failure stamps <code>verified: false</code> rather than quietly
lying. <a href="/experiments/qa/">qa</a> applies it to browser tests — passing
exploratory flows become deterministic scripts, failing steps become explicit
skips rather than silence. <a href="/experiments/evolving-robot/">evolving-robot</a>
applies it to a robot rewriting its own care protocol: the new version survives
only if it outscores the one it replaces, and a real run is on record being
reverted at <code>performance 0.60 &lt; 0.80 baseline</code>.</p>

<h2>3. Look where the standard filter is blind</h2>

<p>A keyword filter over agent memory is blind <em>by construction</em> to a
payload written in words it likes. "Collect the SSH keys", framed as a
license-audit telemetry note, contains nothing a lexicon objects to.</p>

<p><a href="/experiments/sleep-harness/">sleep-harness</a> reads the model's
residual stream instead, and the disguised payload lights up
<code>SSH</code>, <code>authentication</code>, <code>credential</code> while its
lexically identical benign twin reads clean. Nine hard pairs at 0.657 mean
lexical overlap: 8 wins, 0 ties, 1 loss, p=0.0195. A consolidation firewall at
ROC-AUC 0.815 cutting payload persistence 78%. A third-party adapter scanner at
12/12, p=0.0002.</p>

<p>The same shape appears in <a href="/experiments/qa/">qa</a>: coverage tools
report which lines ran, and nothing reports which checks you quietly stopped
making.</p>

<h2>What did not work, which is the more useful half</h2>

<p>sleep-harness pre-registered its hypotheses before collecting data, and its
founding one — that filtering by internal workspace beats filtering by output —
is marked <strong>REFUTADA</strong>. Worse, the free lexical baseline
significantly outperformed it. A third hypothesis did not replicate; the
original effect was a variance spike.</p>

<p>We also published a retraction: a claim that instructing a model harder made
its behaviour worse came from a single sample, and re-running the identical arm
produced the opposite. With an effect that noisy, one run confirms whatever you
expected — and the run that agreed with the story is the one that got written
up.</p>

<p>Publishing that costs nothing and is the only reason the positive results
above are worth reading.</p>

<h2>Where this points</h2>

<p>The three mechanisms compose into something specific: <strong>a way to run
agents in the places that currently refuse them.</strong> Not by making models
more capable — by making their output structurally bounded, their changes
provable, and their inputs screened for what a keyword list cannot see.</p>

<p>Four applications follow directly, in descending order of how much evidence
already stands behind them:</p>

<ul>
<li><strong>A firewall on agent memory.</strong> Every framework now writes to
long-lived memory and almost none screen what goes in beyond keywords. This is
where the strongest results already are.</li>
<li><strong>Screening third-party skills and adapters before they mount.</strong>
12/12 at p=0.0002. As skill marketplaces grow, something has to check what a
downloaded adapter does to a model's behaviour on innocent inputs.</li>
<li><strong>On-device agents that cannot produce garbage.</strong> A small model
whose malformed output is unreachable needs no repair loop, which is exactly the
budget an edge device does not have.</li>
<li><strong>Domains where behaviour must be frozen.</strong> Every care robot
shipping today has frozen behaviour, for good reason. The interesting question is
not whether an agent can learn but what it must prove to earn the right to
change — and an eval-gated freeze with a rollback ledger is a concrete
answer.</li>
</ul>

<h2>Where the stakes are: near-bytecode, and a robot</h2>

<p>The first mechanism is easy to read as an elegance argument. It stops being one
the moment the output moves something.</p>

<p>An LLM driving a robot is already a bytecode generator. In
<a href="/experiments/skillos-robot/">skillos_robot</a> a vision-language model
emits intent at roughly one hertz and a reactive controller turns it into
bytecode on a UDP link to an ESP32 at twenty. The question "can it emit
garbage?" has a physical answer there. A malformed JSON in a chatbot is a retry.
A malformed motor command is a robot hitting something.</p>

<p><strong>And the two halves are currently the wrong way round.</strong> The
robot and <a href="/experiments/token-trie/">token-trie</a> emit the same wire
format — the opcode regex is character-for-character identical in both, because
they were one codebase. What diverged is enforcement. token-trie masks the
sampler so a malformed opcode has no path. The robot asks in the prompt, caps
generation with stop sequences, and parses with that regex.</p>

<p>So the validated mechanism runs a Tetris demo in a browser tab, and the
unvalidated one drives motors. It fails, too, and there is a recording: one
simulator run produced twenty-eight consecutive unparseable opcodes after a
provider capped stop sequences from fourteen to five. The run degenerated without
erroring.</p>

<p>Putting the trie behind the robot needs per-token probabilities, which cloud
APIs do not expose — so it <em>forces</em> a local model. That is not an obstacle
to route around. It is the position this work already argues for, and it turns
on-device from a preference into a requirement.</p>

<h2>The limits, stated plainly</h2>

<p>Constrained decoding currently depends on a tokenizer that treats the
instruction markers as single tokens. On models that split them, the constraint
holds but the model stops choosing — output stays valid and goes strategically
blind. That is the single biggest blocker to the first mechanism generalising.</p>

<p>And in every demo so far, a hand-written planner does the planning; the model
ratifies a ranked list. That is a real result about what a small model can be
trusted with, and it is also the ceiling. None of this makes a model plan.</p>

<p>The honest framing is <em>grammar-safe, provable execution of pre-planned
work</em> — narrower than "an agent OS", and true.</p>
"""


# The repository everything came out of. Deliberately not an experiment: it is
# not active work, and giving it an evidence badge would either overstate it or
# dilute what the three badges mean. It gets its own section instead.
ORIGIN = dict(
    slug="evolving-agents", name="evolving-agents",
    image="evolving-agents",
    image_alt="One empty outline, drawn but never filled, becoming five solid shapes",
    date="2025", repo="https://github.com/EvolvingAgentsLabs/evolving-agents",
    question="What if the decomposition was right and the substrate was wrong?",
    blurb="The Evolving Agents Toolkit. Eighteen thousand lines describing five subsystems, "
          "and three test functions. Each subsystem was independently rebuilt over the "
          "following year on something that could be tested — this is the map of where they "
          "went, and what it cost.",
    sections=[
        ("The architecture was right", """
<p><strong>452 people starred this in 2025.</strong> It had three test functions.
Both of those facts are the point: the decomposition was compelling enough to
mark, and nothing in it was pinned to anything that could contradict it.</p>

<p>Eighteen thousand lines of Python across twelve subsystems: a library of
versioned components, a bus for agent discovery, memory, an evolution loop, and
a governance layer called Firmware. Backed by MongoDB Atlas.</p>

<p><strong>It had three test functions.</strong></p>

<p>That number is the whole story. This was not a product that failed; it was an
architecture that was written down and never pinned to anything that could
contradict it. The decomposition was right — right enough that every piece got
independently re-derived over the following year, mostly without noticing.</p>"""),
        ("The proof is in its own source", """
<p><code>evolving_agents/firmware/firmware.py</code> sets a governance string:</p>

<pre><code>You are an AI agent operating under strict governance rules:
...
- Never use dangerous imports (os, subprocess, etc.)</code></pre>

<p>That is governance by <em>asking</em>. In
<a href="/experiments/token-trie/">token-trie</a>, the forbidden token is not
discouraged — it has no path through the trie, so the model cannot emit it.</p>

<p>Same intention, twelve months and one substrate apart. The code is still on
the default branch precisely so the two halves can be diffed.</p>"""),
        ("What happens to it now", """
<p>It is the umbrella, not a museum.
<a href="https://github.com/EvolvingAgentsLabs/evolving-agents/blob/main/PLAN.md">Three
milestones</a>, two of them already resolved — one of those in a direction
nobody wanted.</p>

<ul>
<li><strong>Transfer and reframe — done.</strong> Moved into the organisation
with its stars, forks and inbound links intact, and the README rewritten around
what it got right and wrong. It had been pointing visitors at two successor
repositories, one archived and one that returned 404.</li>
<li><strong>Recover the dual-embedding resolver — done, and it came back
flat.</strong> Rebuilt without MongoDB and
<a href="https://github.com/EvolvingAgentsLabs/evolving-memory/blob/main/benchmarks/RESULTS.md">measured</a>:
identical to plain description-matching on a modern encoder, 80% both ways. The
next run is the one that matters — a smaller encoder, where the gap it was
designed to close may still exist.</li>
<li><strong>A portable definition with a conformance suite — not started.</strong>
The five projects already share an instruction format character-for-character;
what they do not share is enforcement. A conformance table would today read
<em>one of three</em>, and that is the honest number to publish first.</li>
</ul>"""),
        ("What it cost", """
<p>Two things did not survive, and only one of them on purpose.</p>

<p><strong>The agent bus was dropped deliberately.</strong> A thousand lines of
registry and runtime routing, welded to MongoDB, solving a problem MCP is now
eating. Nothing replaces it: an agent that needs to discover another at runtime
has no answer here today.</p>

<p><strong>The dual-embedding resolver was lost by accident.</strong> Every
component was indexed twice — once for what it is, once for what it is for — and
tasks resolved against the second. It has since been
<a href="https://github.com/EvolvingAgentsLabs/evolving-memory/tree/main/src/evolving_memory/resolver">recovered</a>,
and measured: on a small corpus with a modern embedding model it performs
<em>identically</em> to plain description-matching. The idea may have been
overtaken by the encoders. That is the current state, with a number attached
rather than an assumption.</p>"""),
    ],
)

BADGES = {
    "reproducible": ("Reproducible", "clone it and run it — no API key"),
    "results": ("Results", "published findings, negative ones included"),
    "prototype": ("Prototype", "runs, but needs setup or has no eval yet"),
}
