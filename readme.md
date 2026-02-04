# LightTaxes – AI Full-Stack Engineer Take-Home Assignment

## Solving Tax Returns Like a Codebase

This repository contains my submission for the LightTaxes AI Full-Stack Engineer take-home assignment.
The goal of this project was not to build a production-ready tax engine in a few days, but to demonstrate that I understood the core idea from *“Perfecting Tax Returns Like Code”* and could translate it into a working, extensible system.

In short: I treated a US tax return the same way I would treat a software system — modular, deterministic where possible, and verified instead of blindly trusted.

---

## How I Interpreted the Assignment

The paper’s main idea clicked for me when I stopped thinking of this as “LLMs doing taxes” and instead thought of it as:

> **A dependency graph of typed modules, with LLMs used only where humans normally read instructions.**

So I made a few clear rules for myself before writing code:

* Every IRS form = its own module (agent)
* Arithmetic and tables must be deterministic
* LLMs are allowed to *explain* and *interpret*, not calculate
* If an LLM fails, the system should still work
* It should be obvious how to add another form later

Everything in this repo follows from those rules.

---

## What’s Implemented

### Forms / Agents

I implemented the following form agents:

* **Form 1040** (main return)
* **Schedule B** (interest & dividends)
* **Schedule 1** (additional income & adjustments)

This is the dependency flow:

```
Schedule B
   ↓
Schedule 1
   ↓
Form 1040
```

Each agent:

* Accepts only the inputs it needs
* Produces explicit outputs for downstream agents
* Has no hidden state

The orchestration logic is intentionally simple and explicit so the dependency graph is easy to reason about.

---

## Project Structure (Why It’s Organized This Way)

```
lighttaxes-agent/
├── agents/         # One agent per IRS form
├── tools/          # Deterministic helpers (tax math, PDFs)
├── orchestrator/   # Executes agents in dependency order
├── verifier/       # Cross-form consistency checks
├── llm/            # Gemini client abstraction
├── data/
│   ├── irs_pdfs/   # Official IRS forms & instructions
│   └── testcases/  # TaxCalcBench-compatible inputs
├── tests/          # Unit & integration tests
└── main.py
```

This separation was intentional.
If I wanted to add Schedule C tomorrow, I wouldn’t need to touch Form 1040 logic or the verifier — just add a new agent and wire it into the pipeline.

A small input normalization layer is used to adapt TaxCalcBench inputs to the internal agent schema, keeping form agents decoupled from benchmark-specific formats.

---

## How LLMs Are Used (and Not Used)

### Where LLMs Help

LLMs are used for things humans normally do by reading instructions, for example:

* Deciding whether the standard deduction applies
* Explaining *why* a particular rule was chosen

To avoid hallucination, LLM prompts are grounded in **official IRS instruction PDFs**.
A small PDF navigator searches the instructions and injects relevant excerpts directly into the prompt.

The output is explanatory text with a citation, for example:

> “According to Instructions for Form 1040, Line 12…”

### Where LLMs Are *Not* Used

LLMs never:

* Compute tax amounts
* Look up tax tables
* Perform arithmetic
* Decide numeric outputs

All of that is handled by deterministic Python functions.

This was one of the most important design choices I made.

---

## Deterministic Computation

The following logic is fully deterministic:

* Standard deduction lookup (TY 2024)
* Tax calculation (simplified brackets for demo purposes)
* AGI, taxable income, and total tax math

This means:

* Results are repeatable
* Tests are reliable
* The system still works even if the LLM is unavailable

---

## Verifier Layer

After the pipeline runs, a verifier performs independent checks such as:

* Schedule B income correctly flows into Form 1040
* Total income equals wages + interest
* Taxable income and tax are non-negative

The verifier does **not** recompute tax logic — it only checks consistency.
This is a simplified version of the verifier swarm idea from the paper, scoped to fit the time budget.

---

## Handling LLM Failures (Intentionally)

LLMs are treated as a *non-critical dependency*.

If the Gemini API is unavailable or quota is exceeded:

* The system does not crash
* Deterministic computation continues
* A safe fallback explanation is returned

This was intentional. I wanted to show that correctness does not depend on model availability.

---

## Testing

I added both:

* **Unit tests** (e.g., Schedule B interest aggregation)
* **Integration tests** (full `single-w2` pipeline)

Tests can be run with:

```powershell
pytest
```

This helped catch mistakes early and made refactoring safer.

---

## Test Data & Benchmarking

* The TaxCalcBench repository is included as a vendored dependency
* I focused on the `single-w2` case as a “hello world” end-to-end test
* XML comparison tooling is included as a bonus for validating outputs

I did not attempt all 51 benchmark cases due to time constraints, which felt consistent with the assignment guidance.

---

## How to Run (Windows)

```powershell
python main.py data\testcases\single-w2\input.json
```

This command runs the full pipeline end-to-end, from `input.json` through Schedule B, Schedule 1, and Form 1040, producing computed Form 1040 values.

The output includes:

* Computed numeric values
* An explanation of deduction choice grounded in IRS instructions

---

## Tradeoffs & Limitations

Some things were intentionally simplified:

* Tax brackets are simplified rather than a full IRS table
* Only three forms are implemented
* No web UI or API layer

These were conscious tradeoffs to focus on architecture, correctness, and extensibility rather than surface area.

---

## What I’d Build Next

If I had more time:

* 1 week: Add Schedule C → Schedule SE and expand verifier checks
* 1 month: Full TaxCalcBench coverage, more precise tax tables
* 3 months: Web UI, multi-year support, audit-grade traceability

---

## Closing Thoughts

This project convinced me that tax preparation really *can* be treated like software:

* Modular instead of monolithic
* Deterministic instead of probabilistic
* Verified instead of assumed correct

That mindset is what I wanted to demonstrate with this submission.

---