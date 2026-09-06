/**
 * The stage: eight frames that run lora-kernel instead of describing it.
 *
 * ## Why there is no animation library here
 *
 * There was going to be one. Motion's `mini` build is the right shape for this
 * — 2.3 kB, and it is a thin wrapper over the Web Animations API. But `mini` is
 * not a file you can vendor: its dependency closure pulls `motion-dom`, and the
 * bundle that actually reaches a browser is around 130 kB.
 *
 * This site currently ships **zero external bytes** — no CDN, no web font, no
 * analytics. A page opens from a file, years later, with no server running. So
 * the choice was a 130 kB dependency, or a CDN request that ends that property,
 * to animate opacity, width and colour on a timeline.
 *
 * What is here instead is the primitive the library wraps: CSS transitions for
 * state, and the Web Animations API for the one thing transitions cannot do —
 * a progress bar that must be interruptible mid-flight. If a library is wanted
 * later, `play()` is the only function that would change.
 *
 * ## On motion
 *
 * This organisation's rule is "nothing moves unless you move it", written for a
 * work surface. An explainer is a different job, so the rule is kept in
 * substance rather than in letter:
 *
 *   - the first interaction takes control and never gives it back;
 *   - it does not run off-screen;
 *   - `prefers-reduced-motion` turns autoplay off entirely;
 *   - every frame is a legible still.
 */
(function () {
  "use strict";
  var root = document.getElementById("stage");
  if (!root) return;

  var DWELL = 3200; // ms a frame holds. Slow enough to read the caption.

  var FRAMES = [
    { h: "One GPU. One base model. Nothing else is resident.",
      s: "Everything that follows happens inside a single runtime holding a single set of weights. The cost of the whole system is this block, once." },
    { h: "The agentic system loads. It is adapters.",
      s: "The harness is an adapter that owns the tool protocol — action tokens, state transitions, error shapes. Each expert is an adapter a few hundred megabytes wide. No router model, no orchestration process." },
    { h: "A request arrives. Three experts draft it at once.",
      s: "vLLM batches them over the same base. Each proposes a short continuation of the same context — a branch of tokens, guessed ahead." },
    { h: "A frontier model verifies every branch in one pass.",
      s: "Not three calls. One forward pass over the whole tree. The emitted tokens are the frontier’s, so what you ship in this phase is frontier quality." },
    { h: "The branch it accepted most wins — and that is the routing.",
      s: "No classifier, no extra call. Because the verifier is frontier-grade, agreement means this small expert already produces what the frontier would have produced, here." },
    { h: "Acceptance accumulates, per region, while you serve.",
      s: "You are not running an evaluation. The serving path fills in a map: which expert can stand in for the frontier, and where. A distillation score collected for free." },
    { h: "Above the threshold, the frontier is withdrawn.",
      s: "For that region only, the expert is promoted from drafter to generator and the expensive model is removed. What replaces it is a router — nothing else." },
    { h: "Overnight the pool evolves, and it is still only adapters.",
      s: "Traces become a training set, the weakest adapter is retired, a new delta takes its place — promoted only if a verifier the loop cannot see says it is better." },
  ];

  var HUE = { harness:"#f5a623", clinical:"#2997ff", contract:"#bf5af2", triage:"#ff6b5e", evolved:"#30d158" };

  var el = {
    h:    root.querySelector("[data-h]"),
    say:  root.querySelector("[data-say]"),
    chips:  [].slice.call(root.querySelectorAll("[data-chip]")),
    branch: [].slice.call(root.querySelectorAll("[data-branch]")),
    ver:  root.querySelector("[data-verifier]"),
    fill: [].slice.call(root.querySelectorAll("[data-fill]")),
    val:  [].slice.call(root.querySelectorAll("[data-val]")),
    cost: root.querySelector("[data-cost]"),
    seg:  [].slice.call(root.querySelectorAll("[data-seg]")),
    live: root.querySelector("[data-live]"),
    toggle: root.querySelector("[data-toggle]"),
  };

  var i = -1, playing = false, timer = null, bar = null, taken = false;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var ACC = [null, null, null, null, [41,22,17], [78,34,26], [94,37,29], [94,37,29]];

  function paint(n) {
    i = n;
    var f = FRAMES[n];
    el.h.textContent = f.h;
    el.say.textContent = f.s;

    var loaded = n >= 1, retired = n >= 7;
    // The retirement is WITHIN a sub-domain, which is the whole distinction
    // between routing and evolution: contract-review loses to a better
    // contract reviewer. Replacing the triage adapter here would have drawn
    // the wrong claim — that an expert is swapped for one of another kind.
    var chipHue = [HUE.harness, HUE.clinical, retired ? HUE.evolved : HUE.contract, HUE.triage];
    var chipName = ["harness.lora", "clinical-admin", retired ? "contract-v4" : "contract-review", "incident-triage"];
    var chipRole = ["kernel", "expert", retired ? "evolved · v3 retired" : "expert", "expert"];
    el.chips.forEach(function (c, k) {
      var on = loaded;
      c.classList.toggle("on", on);
      c.style.background = on ? chipHue[k] : "";
      c.style.borderColor = on ? chipHue[k] : "";
      c.querySelector("b").textContent = chipName[k];
      c.querySelector(".r").textContent = chipRole[k];
    });

    var drafting = n >= 2, decided = n >= 4;
    el.branch.forEach(function (b, k) {
      b.classList.toggle("live", drafting);
      b.classList.toggle("win", decided && k === 0);
      var hue = [HUE.clinical, HUE.contract, HUE.triage][k];
      b.style.background = decided && k === 0 ? hue : "";
      b.style.borderColor = drafting ? hue : "";
    });

    var verOn = n >= 3 && n <= 5, verGone = n >= 6;
    el.ver.classList.toggle("on", verOn);
    el.ver.classList.toggle("gone", verGone);
    el.ver.textContent = verGone
      ? "ROUTER ONLY — the frontier is gone"
      : "FRONTIER MODEL — verifies every branch";

    var acc = ACC[n];
    el.fill.forEach(function (f2, k) {
      var v = acc ? acc[k] : 0;
      f2.style.width = v + "%";
      f2.style.background = (k === 0 && v >= 80) ? HUE.evolved : [HUE.clinical, HUE.contract, HUE.triage][k];
      el.val[k].textContent = v ? v + "%" : "—";
    });

    el.cost.textContent = verGone ? "cost: local" : (verOn ? "cost: frontier" : "cost: —");
    el.cost.style.color = verGone ? "#5ee07f" : (verOn ? "#f5c26b" : "#6e6e73");

    el.seg.forEach(function (s, k) {
      if (k < n) s.setAttribute("data-done", ""); else s.removeAttribute("data-done");
      s.setAttribute("aria-current", k === n ? "true" : "false");
    });
    // Announced once per frame rather than on every style change, so a screen
    // reader gets the sentence and not the machinery.
    el.live.textContent = "Step " + (n + 1) + " of 8. " + f.h;
  }

  /** The one thing a CSS transition cannot do: a bar that must be stoppable mid-flight. */
  function runBar(seg) {
    if (bar) { bar.cancel(); bar = null; }
    var pseudo = { duration: DWELL, easing: "linear", fill: "forwards" };
    try {
      bar = seg.animate([{ width: "0%" }, { width: "100%" }], pseudo);
    } catch (e) { bar = null; }
  }

  function advance() {
    paint((i + 1) % FRAMES.length);
    if (i === 0) el.seg.forEach(function (s) { s.removeAttribute("data-done"); });
    var live = el.seg[i].querySelector("i");
    if (live) runBar(live);
    timer = setTimeout(advance, DWELL);
  }

  function play() {
    if (playing || reduced) return;
    playing = true;
    el.toggle.textContent = "Pause";
    el.toggle.setAttribute("aria-label", "Pause the explainer");
    advance();
  }

  function stop() {
    playing = false;
    clearTimeout(timer);
    if (bar) { bar.cancel(); bar = null; }
    el.toggle.textContent = "Play";
    el.toggle.setAttribute("aria-label", "Play the explainer");
  }

  /** The first interaction takes control, and does not give it back. */
  function take(n) {
    taken = true;
    stop();
    paint(n);
    el.seg.forEach(function (s, k) {
      if (k < n) s.setAttribute("data-done", ""); else s.removeAttribute("data-done");
      var live = s.querySelector("i");
      if (live) live.style.width = k < n ? "100%" : "0%";
    });
  }

  el.seg.forEach(function (s, k) {
    s.addEventListener("click", function () { take(k); });
  });
  el.toggle.addEventListener("click", function () {
    if (playing) { taken = true; stop(); } else { playing = false; play(); }
  });
  root.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { take(Math.min(FRAMES.length - 1, i + 1)); }
    else if (e.key === "ArrowLeft") { take(Math.max(0, i - 1)); }
  });

  paint(0);
  if (reduced) {
    stop();
    el.toggle.hidden = true;
  } else if ("IntersectionObserver" in window) {
    // Never runs off-screen. A page in a background tab should cost nothing.
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !taken) play(); else if (!en.isIntersecting) stop();
      });
    }, { threshold: 0.35 }).observe(root);
  } else {
    play();
  }
})();
