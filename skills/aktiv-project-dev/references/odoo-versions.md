# Odoo version differences

Skills work on any Odoo version. Never assume one: read it from the module's
`__manifest__.py` (`'version': '18.0.1.2.0'` → series `18.0`), or from `odoo/release.py`
in the server source. Write code, XML and data for that series only. When the series is
unknown or the module targets several, ask.

Verified against the Odoo 16.0 to 20.0 sources. For a version not listed, or anything
not in this table, check that version's source before writing code, never memory.

## Syntax and API that changed

| Area | 16.0 | 17.0 | 18.0 | 19.0 | 20.0 |
|---|---|---|---|---|---|
| List view root tag | `<tree>` | `<tree>` | `<list>` | `<list>` | `<list>` |
| `view_mode` in actions | `tree,form` | `tree,form` | `list,form` | `list,form` | `list,form` |
| Conditional visibility / readonly / required in views | `attrs="{'invisible': [...]}"`, `states=` | `invisible="<python expr>"` (`attrs` and `states` removed) | same as 17 | same as 17 | same as 17 |
| QWeb output | `t-out` (`t-esc` deprecated) | same | same | same | same |
| `ir.cron` repeat | `numbercall` = `-1` required for a repeating job | same as 16 | `numbercall` / `doall` removed | removed | removed |
| Groups on `res.users` | `groups_id` | `groups_id` | `groups_id` | `group_ids` | `group_ids` |
| Grouping groups in settings | `res.groups.category_id` | same | same | `res.groups.privilege_id` (privilege holds `category_id`) | same as 19 |
| Grouped reads in Python | `read_group(domain, fields, groupby)` | `_read_group(domain, groupby, aggregates)` returns tuples; `read_group` kept for UI | same as 17 | `read_group` deprecated: use `_read_group` in backend code, `formatted_read_group` for UI-shaped results | same as 19 |

## How to use this table

- **Writing code** (`/aktiv-project-dev`, `/aktiv-studio-module`): use the column for the
  module's series.
- **Moving a feature between versions** (`/aktiv-module-sync`): check every row between
  source and target; each one the feature touches is part of the plan.
- **Core updates** (`/aktiv-module-compatible`): a core module moving series hits these
  rows; treat a changed row the sub-module relies on as Breaking.
- **Manifest version**: always `<series>.<x>.<y>.<z>` (e.g. `17.0.1.0.0`). The series
  must match the server; never change it (or any part of the version) on the user's behalf.
- **Odoo Online** runs SaaS releases (e.g. `saas~18.3`) between major versions. Read
  the database's exact version from Settings > About, or ask, and follow the nearest
  major version at or below it; verify anything uncertain on the database itself.
