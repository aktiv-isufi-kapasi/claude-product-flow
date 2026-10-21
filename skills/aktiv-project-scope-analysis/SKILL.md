---
name: aktiv-project-scope-analysis
description: Analyse client-supplied material for an Odoo project — SOW and RFQ spreadsheets, requirement documents, wireframes, brand PDFs, email threads — and produce a gap analysis. Classifies every requirement as standard Odoo, an existing app, configuration, custom work or not feasible, verified against the actual Odoo source for the target version and against apps.odoo.com. Flags scope gaps and drafts the questions to put to the client. Use at the start of a project, on a change request, or when scoping an estimate, for any Odoo version and any hosting — Odoo Online, Odoo.sh or on-premise.
---

# Odoo scope and gap analysis

Turn what the client sent into a decision the team can act on: what is already standard, what an app covers, what must be built, what cannot be done as specified, and what nobody has answered yet.

The output is a written analysis plus a requirement matrix, and a numbered list of questions for the client. Not a plan and not an estimate — those come after the client answers.

## Step 1 — Ask

```
1. Input files
   Paths or a folder. Spreadsheets, requirement docs, wireframes, brand PDFs,
   email threads, screenshots — list everything you have.

   Is any of it scoped? (e.g. "only sheet 17", "section 4 onward", "ignore the
   pricing tab")  Clients send whole workbooks when one tab is the answer.

2. Target platform — all three change the verdict
   Version:  17.0 / 18.0 / 19.0 / other
   Edition:  Community / Enterprise
   Hosting:  Odoo Online (SaaS) / Odoo.sh / on-premise

3. Stage
   1. Pre-sales — estimating before anything is committed
   2. New build — scope agreed, working out what it means
   3. Change request — client has come back on delivered work

4. Is this an existing project?
   1. Yes — there is development already done
      Upload or point me at the project content file — the module context .md
      that /aktiv-project-doc maintains (e.g. ak_odoo_cpq.md). That file is the
      fastest and most reliable statement of what is already built.
      Also useful if you have them: the module directory, and a live instance.
   2. No — nothing built yet

   On an existing project this is what "current scope" means. Skipping it
   produces a gap list full of things already delivered, which is worse than
   no analysis at all.

5. Output
   Where should the analysis be written?  (Enter = alongside the inputs)
   Audience: internal team / client-facing / both

   The analysis goes out as a Word document and the matrix as a spreadsheet.
   Say so if you want a different format.
```

Ask these before opening anything. If the answer to 2 is not known, say so in the
output rather than guessing — the hosting answer alone flips whole requirements
between "routine" and "not possible as written".

## Step 2 — Read the inputs

Follow `references/intake.md`. It covers what to pull out of each material type and
what to record about provenance, because every row of the matrix has to cite where it
came from.

Read everything the user pointed at, in full, before classifying anything. A
requirement that looks custom in isolation is often three rows of a spreadsheet that
together describe standard behaviour.

## Step 3 — Establish the platform baseline

Follow `references/verification.md`. Before judging any requirement, write down what
the target platform does and does not allow — that is the frame every verdict sits in,
and it is version and edition and hosting specific.

Never answer "is this standard in Odoo" from memory. Grep the source for the target
version. Cite `module/file.py:line` or the module name.

## Step 4 — Classify every requirement

One row per requirement in the matrix, with these verdicts:

| Verdict | Means |
|---|---|
| **Standard** | Odoo already does this. Cite the module. The client may not know. |
| **Config** | Standard, but needs setting up. No development. |
| **App** | An existing app on apps.odoo.com covers it. Cite the URL, price, version and maintainer. |
| **Custom** | Has to be built. Note whether the hosting allows it. |
| **Not feasible as specified** | Cannot be done as written. Always name the nearest thing that can. |
| **Unclear** | Not enough information to judge. Every one of these produces a client question. |

Never leave a requirement unclassified and never merge two requirements to make one
verdict fit. If the client wrote it as one line but it is three decisions, it is three
rows.

## Step 5 — Hunt the gaps

Follow `references/questions.md`. It carries the gap taxonomy — the categories that
actually bite on Odoo projects — and the rules for writing questions a client will
answer rather than ignore.

A gap is not only a missing requirement. It is also a requirement that is stated but
unanswerable, one that assumes something the platform will not do, one that depends on
something the client has to supply, and one that duplicates what Odoo already ships.

## Step 6 — Produce the deliverables

Follow `references/deliverable.md`:

- **`<name>_gap_analysis.docx`** — the written analysis, as a Word document
- **`<name>_requirements.xlsx`** — the matrix, one row per requirement
- The client questions, numbered, inside the analysis and repeated as a plain list
  that can be pasted into an email without editing

Show the classification summary and the question list before writing the files.

## Rules

- **Cite everything.** Every row names its source — document, sheet, cell, page or
  paragraph. A requirement with no citation is something you invented.
- **Separate what was said from what you concluded.** The client's words go in one
  column, your reading in another. Where you assumed, label it an assumption.
- **A verdict without evidence is an opinion.** "Standard in Odoo" needs a module
  name. "There is an app" needs a URL. "Not feasible" needs the constraint that stops it.
- **Do not estimate.** Effort bands (S / M / L / XL) are for triage. Hours come after
  the client answers, not before.
- **Do not solve it.** This skill decides what the work is, not how to build it. The
  design happens after the scope is agreed.
- **Blocking beats complete.** Mark which questions stop the estimate and which can
  wait. A client given thirty equal questions answers none.

## References

- `references/intake.md` — reading each material type, and provenance
- `references/verification.md` — proving standard vs app vs custom, per version and hosting
- `references/questions.md` — the gap taxonomy and how to write client questions
- `references/deliverable.md` — the analysis structure and the matrix columns
- `assets/build_matrix.py` — turns the rows into a formatted xlsx
- `assets/build_analysis.py` — renders the drafted analysis as a .docx
