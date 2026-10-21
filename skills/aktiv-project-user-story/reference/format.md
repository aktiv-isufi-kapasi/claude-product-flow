# Aktiv user-story format reference

## Exact styling (from finalized US-01..US-04)
| Element | Font | Size | Color | Bold |
|---|---|---|---|---|
| Title `User Story N: ...` | Poppins | 18pt | navy `#1F3864` | yes |
| Section h2 `1. ...` | Poppins | 13.5pt | navy `#1F3864` | yes |
| Feature h3 `2.1 ...` | Poppins | 11.5pt | maroon `#7B1F2B` | yes |
| Inline label `Description:` etc. | Poppins | 10.5pt | navy `#1F3864` | yes |
| Body / bullets (List Bullet) | Poppins | 10.5pt | grey `#404040` | no |
| Table header | Poppins | 10pt | navy `#1F3864` | yes |
| Table body | Poppins | 10pt | grey `#404040` | no |
| Screenshot caption / placeholder | Poppins | 9.5pt | maroon `#7B1F2B` | yes |
| Footer (page number) | Poppins | 9pt | grey `#808080` | no |

Page: US Letter (8.5x11in), margins L/R 1.25in, T/B 1in. Tables: "Table Grid". Footer: centered `Page <PAGE field>`.

## Inline label set (per feature under 2.x)
`Description:` -> one line. `UI Elements:` -> field bullets/table + annotated screenshot(s). `Behavior:` -> bullets. Keep the order Description -> UI Elements (+ screenshot) -> Behavior.

## Screenshot sources used before
- Standard-Odoo screenshots: clean DB `std19_shots` (port 8072, no custom addons) driven via Playwright, annotated with a browser-injected red arrow+label overlay.
- Report/PDF stories: render the client PDF with `pdftoppm -png -r 150`, crop to the relevant area, annotate with `scripts/annotate.py`.

## Per-project context
The style above is project-agnostic. Keep project-specific facts (dev database and port,
custom modules to reuse, fields and models the stories must align with, what is deferred
to a later phase, and the story map) in the project's own context file, not in this skill.
Read that file before drafting a story.
