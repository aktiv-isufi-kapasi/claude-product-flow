---
name: aktiv-project-user-story
description: Use when creating or updating a user story document in the Aktiv format (any project). Produces a styled .docx (Poppins; navy headings; maroon feature headings; field tables with a Type column; annotated red-arrow screenshots) saved under user_stories/. Triggers include "create a user story", "write the story for a feature", "US-0X", "Aktiv user story", or turning a client spec/PDF into a user story.
---

# Aktiv user-story creator

Generate a user story as a `.docx` in the **Aktiv format**, using the bundled builder so
styling stays identical to previously finalized stories. The format is the same across all
projects; only the content is project-specific.

## Rule 1 - Clarify FIRST (mandatory, no exceptions)
Before writing anything, gather every open question and ask the user with AskUserQuestion.
**Do NOT start the document until all questions are answered.** Typical questions:
- Scope: which behaviors are in vs out; which are standard Odoo (no story) vs custom.
- Report/screen structure and ordering; where a new element sits.
- Data sources and field types for every new field/column (Boolean/Char/Float/Selection/
  Many2one/One2many/Report-column…), and what already exists to reuse.
- Any dependency deferred to a later phase.
Also CHECK the codebase first (grep standard Odoo + our custom modules) so the story ALIGNS
with existing fields/reports instead of duplicating them; state the reused pieces explicitly.
Only write stories for **customizations**, never for standard/config features.

## Rule 2 - NO development while writing the story
Writing a story never involves building its feature. Screenshots come ONLY from:
- **Standard Odoo** on a clean DB (showing WHERE the change will go), or
- **An existing project / DB that ALREADY has that customization** from previously delivered work.
Never implement, scaffold, or modify the story's own feature just to capture a screenshot.
If no valid screenshot source exists yet, use `s.shot("what it should show")` as a placeholder.

## Document structure (exact)
- **Title**: `User Story N: <Title>` (the builder adds this; N may be like `5 (Extra)`).
- **1. Business Requirements** — context/problem, the high-level need, and the value (why). Concise.
- **2. Functional Specifications** — first line `Modules Impacted: <Odoo apps>`. Then one
  `2.x <Feature>` per feature, each with the bold inline labels **Description:**,
  **UI Elements:**, **Behavior:** (bullets under each). Put a field table under UI Elements
  where useful: **Field | Type | Meaning | Required?/Editable?** — always include a **Type** column.
- **3. Success Criteria** — an h3 per feature with testable bullet criteria.
- **4. Change Log** — table `Version | Change Description`; first row `1.0 | Original user story drafted and finalized.` (use `s.changelog()`).

## Screenshots (Aktiv convention)
- Placement: INSIDE each feature's **UI Elements**, AFTER the field bullets/table and BEFORE **Behavior:**.
- Full text-column width (~17 cm), aspect preserved.
- **Annotated with red arrow(s) + a red text label** pointing to the exact spot of the change.
  The annotation replaces a caption. Stack multiple when a feature spans several screens.
- Source per Rule 2 (standard Odoo, or an already-customized existing project). For a REPORT
  story, annotating the client's target PDF (rendered with `pdftoppm`) is acceptable.
- Use `scripts/annotate.py` — `annotate(src, dst, notes=[{"xy","text","to"}], crop=...)` — to draw
  the arrows/labels, then `s.img(path)` to embed.

## How to build (bundled library)
Run with a python that has python-docx + Pillow (e.g. the Odoo virtualenv's python):

```python
import sys; sys.path.insert(0, "<skill>/scripts")   # this skill's scripts/ dir
from us_lib import Story
from annotate import annotate

s = Story(5, "International Invoice")           # -> "User Story 5: International Invoice"
s.h2("1. Business Requirements"); s.para("...")
s.h2("2. Functional Specifications")
s.label("Modules Impacted:", "Invoicing, Inventory")
s.h3("2.1 <Feature>")
s.label("Description:", "...")
s.label("UI Elements:")
s.table(["Field", "Type", "Meaning", "Required?"], [["...", "Char", "...", "Yes"]])
annotate("raw.png", "annot.png", notes=[{"xy":(60,40),"text":"New field","to":(400,120)}], crop=(0,80,1275,700))
s.img("annot.png")
s.label("Behavior:"); s.bullets(["..."])
s.h2("3. Success Criteria"); s.h3("<Feature>"); s.bullets(["..."])
s.h2("4. Change Log"); s.changelog()
s.save("user_stories/US-05_<Short_Title>.docx")
```

`Story` methods: `title`, `h2`, `h3`, `para`, `label(label, text=None)`, `bullets(list)`,
`table(headers, rows)`, `img(path, caption=None, width_cm=17)`, `shot(caption)`,
`changelog(rows=None)`, `save(path)`.

## Output
- One `.docx` per story in the project's `user_stories/` folder, named `US-0N_<Short_Title>.docx`
  (Extra stories: `Extra-US0N_<Short_Title>.docx`). Google-Docs compatible (Poppins).
  Verify by re-opening with python-docx (paragraph/table/image counts).

See `reference/format.md` for the full style table and per-project context notes.
