# Evolving Agents Labs

**Agents defined in markdown. Evolved through memory. Running from Claude Code to bare metal.**

One thesis explored at five levels of depth: agent behavior belongs in declarative documents, the LLM is the interpreter, memory is how agents improve, and grammar/structure is how you keep them safe.

---

## The Stack

Each layer removes a safety net. Each one proves the same patterns work at increasing depth.

```
                         ┌───────────────┐
                         │    llm_os     │  LLM is the CPU. 14-opcode ISA.
                         │    (Rust)     │  GBNF grammar = type system.
                     ┌───┴───────────────┴───┐
                     │     skillos_robot      │  VLM-driven robot. $30 hardware.
                     │     (TypeScript)       │  Dream consolidation.
                 ┌───┴───────────────────────┴───┐
                 │        skillos_mini            │  On-device. 2B model. No internet.
                 │        (Svelte/Capacitor)      │  Deterministic safety checks.
             ┌───┴───────────────────────────────┴───┐
             │              skillos                    │  Full markdown OS. Any LLM.
             │              (Pure Markdown)            │  Memory + evolution + planning.
         ┌───┴───────────────────────────────────────┴───┐
         │     skillos_plugin + skillos_systemcontrol      │  Try it now. /skillos + /sysctl.
         │     (Claude Code plugins)                       │  Install in 10 seconds.
         └─────────────────────────────────────────────────┘
```

---

## Projects

### Try it now (Claude Code plugins)

| Repo | Command | What it does |
|---|---|---|
| **[skillos_plugin](https://github.com/EvolvingAgentsLabs/skillos_plugin)** | `/skillos` | Goal decomposition, agent creation, execution, memory consolidation. The easiest way to explore SkillOS concepts. |
| **[skillos_systemcontrol_plugin](https://github.com/EvolvingAgentsLabs/skillos_systemcontrol_plugin)** | `/sysctl` | Security audits, agent scoring, controlled evolution, lifecycle management. Governs what `/skillos` builds. |

```bash
/skillos "Build a REST API with auth and tests"
/sysctl "audit and score all agents in Project_webapp"
```

---

### Full system (markdown-defined agent OS)

**[skillos](https://github.com/EvolvingAgentsLabs/skillos)** &mdash; Pure Markdown Operating System

Every component &mdash; agents, tools, memory, orchestration &mdash; defined entirely in `.md` files interpreted by any LLM at runtime. No code compilation. The LLM is the interpreter.

- HWM two-level hierarchical planning (arXiv:2604.03208)
- 14 domain-specific dialects (50-99% token compression)
- Bio-inspired dream consolidation (traces become strategies overnight)
- Self-optimization loop (detect stale skills, propose improvements)
- Multi-provider: Claude, Gemini, Gemma 4, any OpenAI-compatible endpoint
- Validated on complex multi-agent scenarios (Operation Echo-Q, Project Aorta)

---

### On-device (mobile democratization)

**[skillos_mini](https://github.com/EvolvingAgentsLabs/skillos_mini)** &mdash; On-device trade assistant for Android

Same architectural patterns running on a phone with a 2B model. Markdown cartridges (documents with embedded tool-calls) guide the LLM through trade diagnostics. The LLM picks links and decides which optional checks to run &mdash; all safety rules execute as deterministic TypeScript functions.

- Three production cartridges: electricista (IEC 60364), plomero, pintor
- Gemma 4 on-device via LiteRT &mdash; no internet required
- Regulatory compliance by construction (deterministic validators)
- Navigator state machine: IDLE &rarr; ROUTING &rarr; WALKING &rarr; COMPOSING &rarr; DONE

---

### Real world (embodied cognition)

**[skillos_robot](https://github.com/EvolvingAgentsLabs/skillos_robot)** &mdash; VLM-driven robot navigation

A 20cm robot that sees through a camera, reasons about the scene, and drives to the target. Give it a goal in plain language. Same patterns &mdash; markdown traces, dream consolidation, strategy extraction &mdash; but in the physical world with $30 of hardware.

- Dual loop: VLM perception (1-2 Hz) + reactive motor control (10-20 Hz)
- Two modes: overhead camera (arena) or egocentric (first-person, no IMU)
- Failed traces get retried in MuJoCo simulation during dream consolidation
- Gemini (cloud teacher) or Ollama (local student, no internet)

---

### Bare metal (the LLM as CPU)

**[llm_os](https://github.com/EvolvingAgentsLabs/llm_os)** &mdash; An OS where the LLM is the CPU

The maximum expression of these ideas. The LLM doesn't use tools &mdash; it *is* the processor. A 14-opcode ISA enforced by GBNF grammar at decode time. Invalid instruction sequences are physically impossible to emit. KV cache is RAM. Grammar is the type system. Cartridges are syscalls. Boots from an SD card on a Raspberry Pi 5.

- In-process inference via Rust FFI to llama.cpp (no HTTP boundary)
- Deterministic KV paging with anchors (no LLM summarization)
- WASM-sandboxed cartridges with curated host functions (real Ring 3)
- Single-token ISA fine-tune pipeline (20 opcodes, exact capability enforcement)
- Dual deployment: dev mode (macOS/Linux) + release mode (Buildroot Pi 5 image)

---

## The Unifying Patterns

Across all five layers, the same patterns recur:

| Pattern | Plugin | SkillOS | Trade App | Robot | LLM-OS |
|---|---|---|---|---|---|
| Declarative behavior | markdown agents | markdown agents | markdown cartridges | markdown traces | GBNF grammar |
| Memory consolidation | dream command | dream engine | session blackboard | dream retries | KV pager + state |
| Capability control | human approval | policy masks | tool whitelists | motor limits | logit bias + WASM |
| Composable units | agent triads | skills (domain/family) | cartridge docs | navigation strategies | cartridges + schemas |
| LLM as interpreter | Claude | any LLM | Gemma 2B | Gemini VLM | Qwen 3B (the CPU itself) |

---

## Research Direction

**From external frameworks &rarr; markdown specifications &rarr; LLM-native execution.**

The original Evolving Agents Toolkit (Python, MongoDB, 2025) proved the concept. SkillOS proved markdown alone is sufficient. LLM-OS proves you can push it all the way down to the hardware level &mdash; the LLM doesn't call tools, it *is* the processor, constrained by grammar the way a CPU is constrained by its instruction decoder.

---

## Quick Start

The fastest path from zero to working:

```bash
# 1. Install the Claude Code plugin (10 seconds)
/plugin install skillos-plugin

# 2. Give it a goal
/skillos "Research quantum computing and write a summary"

# 3. See what it built
ls projects/

# 4. Consolidate learnings
/skillos dream
```

Then go deeper: clone `skillos` for the full system, `skillos_mini` for mobile, `skillos_robot` for embodiment, `llm_os` for bare metal.

---

Apache 2.0 &middot; permanently alpha &middot; 2026

[evolvingagentslabs.github.io](https://evolvingagentslabs.github.io)
