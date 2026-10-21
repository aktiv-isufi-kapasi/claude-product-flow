# The deliverables

Two files and one list. Show the classification summary and the questions before writing
anything.

## 1. `<name>_gap_analysis.docx`

A Word document — it is the client-facing deliverable and goes out as one.

Draft the content as markdown first; it is quicker to write and quicker for the team to
review. Then render it:

```bash
python3 assets/build_analysis.py analysis.md <client>_gap_analysis.docx
```

If the session offers a document skill, use that instead — it produces a better document
than the script, with proper styles and a table of contents. If neither that skill nor
`python-docx` is available, the script leaves the markdown in place and says so; hand
that over and note that the Word version is pending, rather than passing the markdown off
as the deliverable.

Keep the drafted markdown alongside the .docx. It is what gets edited on the next round,
and diffing two Word files to see what changed is nobody's idea of a good afternoon.

Structure:

```markdown
# <Client> — <Project> — Gap Analysis
<date> · prepared by <author>

## What was analysed
Every input, with its date and version. What was deliberately not analysed, and on
whose instruction. Anything asked for but not received.

## Platform baseline
Version, edition, hosting — and what that combination rules out. Where the user did
not know, say so and mark the affected verdicts provisional.

## Current scope
What is already agreed, built or live, and where that was read from — the project
content file, the module directory, or the instance. Say which, and give the context
file's date. On a change request this is the reference point for everything below.
Empty on a new build — say "none" rather than omitting the heading.

## New scope
What this round adds, grouped the way the client thinks about it.

## Coverage
    Standard        n      already in Odoo, no work
    Config          n      setup only
    App             n      existing app, see matrix for cost
    Custom          n      to be built
    Not feasible    n      as specified — alternatives in the matrix
    Unclear         n      blocked on Q<n>
One line each on anything that is not Custom — clients read this section first, and
"you already have this" is the most valuable sentence in the document.

## Feasibility findings
Each requirement that cannot be delivered as written: the constraint, the nearest
feasible alternative, and what is lost by taking it.

## Gaps and open questions
The numbered list. Blocking first, then needed-before-go-live.

## Client-supplied dependencies
Table: what, why it is needed, who owns it, by when, what stalls without it.
Assets, credentials, copy, legal text, decisions.

## Assumptions
Everything assumed to keep moving, each one falsifiable in a sentence.

## Recommendation
What to do next, and in what order. Three or four sentences.
```

Match the depth to the material. A change request against a known module does not need
the platform baseline restated at length; a first-contact pre-sales analysis does.

## 2. `<name>_requirements.xlsx`

One row per requirement. Columns:

| Column | Contents |
|---|---|
| ID | R1, R2 … Stable; referenced by the questions. |
| Source | Document · sheet/page · row. Must let a reader re-check it. |
| Requirement (client) | Their words, verbatim, trimmed. |
| Interpretation | Your reading. Separate column so a misreading is visible. |
| Stated / Inferred | Inferred requirements are real but must be labelled. |
| Area | Website, Sales, Inventory, Portal, Reporting … the client's grouping. |
| Verdict | Standard / Config / App / Custom / Not feasible as specified / Unclear — exactly these six, spelled this way, so the matrix colours and the coverage counts line up |
| Evidence | Module name, `file.py:line`, app URL, or the constraint that blocks it. |
| Hosting impact | Blank, or what the hosting changes about this row. |
| Effort | S / M / L / XL — triage only, never hours. |
| Risk | What could make this cost more than it looks. |
| Depends on | Client-supplied asset, decision, or another requirement. |
| Question | Q number, where one is open. |
| Status | In scope / New scope / Gap / Out of scope |

Freeze the header row, widen the text columns, wrap them, and colour the Verdict
column so the shape of the project is visible without reading. `assets/build_matrix.py`
does this — feed it rows as JSON.

If the session offers a spreadsheet skill, use that instead; it produces a better
workbook than a script. If neither `openpyxl` nor a spreadsheet skill is available,
write the matrix as CSV and say so rather than silently dropping a column.

## 3. The question list

Inside the analysis, and repeated at the end as plain text that can be pasted into an
email with no editing — no markdown tables, no internal row IDs the client has never
seen, no module names they do not use.

## Before handing over

- Every row cites a source, and every citation resolves.
- Every Standard row names a module; every App row has a URL, version and price; every
  Not-feasible row has an alternative.
- No question is answered by the documents.
- Blocking questions number fewer than ten. If more, the scope is not ready and that is
  the headline finding.
- The counts in the coverage summary equal the row count in the matrix.
- Nothing in the file is estimated in hours.
- The .docx opens, its tables have rendered as tables, and the question numbers in it
  match the Question column in the matrix.
