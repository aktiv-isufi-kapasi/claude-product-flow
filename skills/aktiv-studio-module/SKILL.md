---
name: aktiv-studio-module
description: Build or extend an Odoo module that installs on a strict Odoo Online (SaaS) database through Apps > Import Module. Data-only — the manifest is the only Python and holds no logic. Use when the target instance is Odoo Online / odoo.com hosted and custom Python cannot be installed. Covers Studio-style models and fields, backend screens, public website pages, editable content, access rules, scheduled jobs, translations and packaging.
---

# Odoo Online (SaaS) module

Odoo Online will not run your Python. A module still installs, through **Apps → ⋮ → Import Module**, but only as data: XML, CSV and static files. This skill builds that kind of module.

If the target is Odoo.sh or self-hosted, stop and say so — write a normal Python module instead. Everything here exists to work around a constraint you would not have.

## Step 1 — Ask

Ask these before writing anything. Answer several at once is fine. If the module already exists, read it first and ask only what the code does not already answer.

**1. Where and what**
```
Module directory? (Press Enter for current: <cwd>)
Module technical name? (e.g. website_example_home)
```

**2. Platform** — this decides whether the skill applies
```
Target instance:
  1. Odoo Online (SaaS) — no custom Python, Import Module only
  2. Odoo.sh / self-hosted — Python allowed
Odoo version? (e.g. 18.0)
```
On **2**, stop and recommend a normal Python module.

**3. What the module has to do** — multi-select, comma separated. These answers become the file plan.
```
  1. New models and fields         — Studio-style x_ records
  2. Fields on existing models     — e.g. a flag on product.template
  3. Backend screens               — form/list views, action, menu
  4. A new public website page     — website.page + QWeb view
  5. Change existing website pages — template inheritance
  6. Access rights / record rules  — groups, ir.model.access, ir.rule
  7. Scheduled job                 — ir.cron, sandboxed code
  8. Button-triggered logic        — ir.actions.server, sandboxed code
  9. Translations                  — .pot + .po
 10. Frontend styling / JS         — SCSS or JS via the assets key
```

**4. Field prefix** — only if 1 or 2 was chosen
```
Prefix for custom fields? (e.g. x_ex_)
Manual fields must start with x_. A project prefix after it keeps them apart
from Studio's own fields and from other modules'.
```

**5. Editing model** — only if 4 or 5 was chosen. This is the most consequential
decision in the module. Do not guess it.
```
After go-live, who edits the page text and how?
  1. Backend only     — client edits records, the page reads them
  2. On the page      — client clicks Edit and types over the text
  3. Both             — same records, editable either way  (recommended)
  4. Free-form blocks — client drags website building blocks in

1-3 use t-field: writes go to records, the view is never pinned, the page keeps
taking module updates. 4 needs an oe_structure, which pins its view on the first
save — that region stops taking updates permanently.
```
On **4**, the oe_structure goes in its own view pulled in with `t-call`, so the pinning cannot reach the rest of the page. Never put one in the main page view.

**6. Languages** — only if 9 was chosen
```
Which languages? (e.g. Spanish)
```

## Step 2 — Confirm the plan

Present the file layout and get a yes before writing.

```
<module>/
  __init__.py                    (empty — never executed, but expected)
  __manifest__.py                (the only Python; a plain dict, no logic)
  data/01_models.xml             (models and fields — load first)
  security/ir.model.access.csv
  views/<module>_views.xml       (backend screens)
  views/<module>_website.xml     (page and templates)
  data/02_<name>.xml             (seed records — load after the views)
  i18n/<lang>.po
  static/src/scss/<name>.scss
```

Load order is not cosmetic: models before security, security before views, seed records after the views that read them.

## Step 3 — Build

Read `references/constraints.md` before writing the first file — it is what the platform enforces silently. Use `references/patterns.md` for the record shapes.

House rules:

- Manual models and fields need `<field name="state">manual</field>` and an `x_` name. Custom models take `x_name` as `_rec_name` — define it or breadcrumbs read as ids.
- Set `<field name="translate">1</field>` **at field creation**. Turning it on after the client has entered content means migrating that content.
- Field labels are the client's words, not the developer's — `Show in Product Carousel`, not `Featured flag`. For a boolean the label is the entire UI.
- Wire a field or do not ship it. A field on a form that nothing reads is a support ticket.
- `noupdate="0"` for what the module owns and should keep correcting on upgrade. `noupdate="1"` for what the client owns after the first install.
- Never write to a core view the client may have edited in the builder. An edited page has a website-specific copy-on-write fork; your module lands on the generic view while the site keeps serving the fork. Ship your own page and point the client's configuration at it.
- Comment the *why*. These files are read by whoever imports the next version.

## Step 4 — Verify, package, hand over

Follow `references/handover.md`. Do not assert that it works — check it.

## References

- `references/constraints.md` — what the platform enforces, and the traps that fail silently
- `references/patterns.md` — copy-paste record shapes for every capability in step 3
- `references/handover.md` — verification checklist, zip command, what to tell the client
