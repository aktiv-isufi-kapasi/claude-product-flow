# Reading the inputs

Clients send what they have, not what you need. The job is to get every requirement out
with its provenance intact, and to notice what is missing from the pile.

## Before opening anything

Ask what is scoped. A client who sends a 20-tab workbook usually means one tab — being
told "only sheet 17" after you have read all twenty is a wasted pass. Record what you
were told to ignore, and say so in the analysis: *"Sheets 1-16 and 18-20 were not
analysed, on instruction."* That sentence protects you when something surfaces later.

## Spreadsheets — SOW responses, RFQs, requirement lists

The highest-value material and the easiest to misread.

- Enumerate the sheets first, with row counts, and show the user that list before
  reading in depth.
- Find the client's response columns. A returned SOW usually has your original text plus
  their verdict — Agreed / Not agreed / Changed / Comment. **The response columns are the
  scope, not your original text.**
- Read merged cells and their neighbours together. A comment three columns right of a
  requirement is still that requirement's answer.
- Note the empty cells. A requirement the client did not answer is a gap, and it is
  invisible unless you look for it specifically.
- Watch for strikethrough, colour coding and comments — clients signal removal that way
  rather than deleting rows.
- Cite as `<file> · sheet <name> · row <n>` (add the column when the sheet is wide).

If the session offers a spreadsheet skill, use it. Otherwise `openpyxl` with
`data_only=True` reads the cached values rather than formula text.

## Requirement documents and SOWs

- Number every requirement, even if the document does not. Your numbering is what the
  matrix and the questions refer to.
- A paragraph that contains "and" often contains two requirements. Split them.
- Watch the modal verbs: *must* / *should* / *may* are different commitments, and
  clients use them deliberately more often than developers expect.
- Record anything stated as already agreed — that is current scope, not new scope.

## Wireframes and design comps

- Read them as images and describe what is actually drawn, section by section, top to
  bottom. Do not summarise into "a homepage".
- Every distinct band, panel, carousel or repeated card is a requirement.
- Note what is drawn but never mentioned in writing — and what is written but never
  drawn. Both are gaps.
- Placeholder content is a supply question, not a design decision: greeked text means
  copy is owed, grey boxes mean images are owed, a named brand face means a font licence
  is owed.
- Count repetitions. "Three testimonials" drawn and "a testimonial carousel" written are
  not the same requirement.

## Brand and style material

- Pull out the concrete deliverables: typeface names and weights, hex values, logo
  variants, spacing rules.
- Every named typeface is a licence question. Ask whether webfont files exist and
  whether the licence permits self-hosting, before anyone plans around it.
- Logos need the variants the design actually uses — reversed, transparent, monochrome.
  A single JPEG with a white background will not survive a dark band.

## Email and chat threads

- The most recent instruction wins, but say when it contradicts a document, and which
  document.
- A decision made in a thread and never written into the SOW is a scope change nobody
  has priced. Flag it as one.

## The project content file — existing development

On an existing project this is the single highest-value input, and it should be read
**before** the client's new material. It is the module context `.md` that `/aktiv-project-doc`
maintains: a current-state description of what the module does, with no changelog and no
history. Read it in full.

What to pull out of it:

| Pull out | Becomes |
|---|---|
| What the module does now | **Current scope** — the baseline every new requirement is a delta against |
| The data model and fields | Where a new requirement lands, or why it does not fit |
| Documented constraints and platform limits | Feasibility verdicts, already proven once |
| Placeholders and known blockers | Client-supplied dependencies, already known and still open |
| Conventions the module follows | Whether a new requirement breaks one, which is a finding |

Then treat it as a **claim, not a fact**. It describes the module as of its last update.
Before relying on it:

- Check its date against the module's last change. A context file older than the code is
  a finding in itself — say so, and verify anything load-bearing against the source.
- Spot-check two or three specifics. If it names a field, a file or a menu path, confirm
  that it still exists before a verdict rests on it.
- Where the file and the code disagree, the code wins and the disagreement is reported.

If there is no context file, say so and fall back to the module directory and the live
instance — but record that current scope was reconstructed rather than read, because
anything reconstructed can be incomplete.

Requirements that this file shows are already delivered are **In scope**, not gaps. Where
existing work partly covers a new requirement, state how far it goes; that delta is the
estimable unit, and it is usually far smaller than the requirement reads.

## Screenshots of a live system

- These usually show current behaviour the client wants changed. Record what is on
  screen and what they said about it separately.
- Check the version and edition visible in the UI against what the user told you.

## What to record for every requirement

| Field | Why |
|---|---|
| Source | Document, sheet, row, page. Enables anyone to re-check the row. |
| The client's words | Verbatim, trimmed. Never paraphrased into the matrix. |
| Your reading | What you take it to mean. Kept separate so a misreading is visible. |
| Stated or inferred | Inferred requirements are real, but they must be labelled. |

## When the pile is incomplete

Say so explicitly and early. The common absences:

- No acceptance criteria anywhere
- A wireframe with no content, or content with no wireframe
- An integration named with no API, no credentials and no sample payload
- A migration named with no source system, format or volume
- No statement of who maintains the content after go-live
- No languages, currencies, companies or websites stated — all of which multiply work

These belong in the analysis as findings, not as footnotes.
