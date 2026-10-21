# What Odoo Online enforces

These are enforced by `base_import_module`, not by convention. Breaking one produces a
silent skip, not an error — which is why they cost time to find.

## The import itself

- **Only `.xml`, `.csv` and `.sql` are loaded** from the manifest's `data` and `demo`
  lists. Anything else is skipped with a log line you will not see. `__init__.py` is
  never executed — ship it empty so the directory still reads as a module.
- **`static/` is imported whole**, at any extension, because the check is
  `filename.startswith('<module>/static')`. Each file becomes a public `ir.attachment`
  served at `/<module>/static/...`. Fonts, images, `.js` and `.scss` all arrive intact.
- **The `assets` manifest key works.** It becomes `ir.asset` records, which is why SCSS
  compiled from an imported zip reaches the frontend.
- **100 MB** ceiling on the uploaded zip.
- **Bump the version on every re-import.** Odoo compares it before upgrading; the same
  version uploads successfully and changes nothing.

## No controllers

There is no route to register. A page that needs data the QWeb render cannot reach calls
the core `/web/dataset/call_kw` endpoint from JavaScript. That runs as the session user
and never sudo, so record rules filter the result — which is the feature, not a
workaround. Build the security in `ir.rule` and the front end inherits it.

## The two ways content gets edited

Getting this wrong is the difference between a page the client maintains and a page that
freezes on the first save.

- `t-esc` emits no branding. Not editable on the page.
- `t-field` emits `data-oe-model` / `-id` / `-field`. The editor sends `xpath = null` for
  it, which takes `ir.ui.view.save()`'s early branch: **the record is written and the view
  is never stamped `noupdate`**. The page keeps taking module updates. Use this for every
  heading, label and body string.
- `oe_structure` is a drop zone. The first save creates a child view inheriting the
  original and stamps `noupdate` **on the view it wrote**. That region leaves module
  control permanently. Isolate each one in its own view and `t-call` it.

Corollary for translation: `TranslationModuleReader` selects terms by xml_id ownership.
Views the editor created have no xml_id, so anything a client builds inside an
`oe_structure` is invisible to extraction and must be translated through
**Website → Site → Translate**, never through the `.po`.

## noupdate and one-shot configuration

`<function>` under `noupdate="1"` runs on **first install only** — `_tag_function` returns
early when `self.noupdate and self.mode != 'init'`. That is the right tool for
configuration the module should set once and then leave alone (pointing the site's
homepage at your page, seeding a default). It is the wrong tool for anything that must
re-apply on upgrade.

## Sandboxed code

`ir.cron` and `ir.actions.server` with `state="code"` ship to SaaS like any other record,
which is how a data-only module gets behaviour at all.

- The eval context gives `env`, `datetime`, `time` and `log`. **`fields` is not
  available** — use `datetime.date.today().strftime('%Y-%m-%d')`, not `fields.Date.today()`.
- On a cron, leave `nextcall` unset. Pinning it to a past date leaves the job permanently
  overdue, the server starts it moments after every module load, and `ir_cron._try_lock`
  then takes a `FOR UPDATE NOWAIT` that makes your next import fail with "This cron task is
  currently being executed and may not be modified".
- Run the job as `base.user_root` if record rules would otherwise hide rows from it.

## Frontend

- SCSS compiles under **libsass**, not dart-sass. `min()` / `max()` need interpolation:
  `#{min(100%, 415px)}`.
- Odoo stamps `loading="lazy"` on every `<img>` it renders, but only `if 'loading' not in
  atts`. Above-the-fold images must set `loading="eager" fetchpriority="high"` themselves
  or they flash blank on navigation and on language switch.
- A Bootstrap carousel cannot show several items per slide. Bootstrap clears the slide
  transforms after each transition, so a flex track has no resting offset. Put N items in
  one slide instead and compute the slide count in QWeb.
- SVG uploaded as an attachment has its mimetype rewritten to `text/plain` by
  `ir_attachment._check_contents` unless the uploader has write access on `ir.ui.view`.
  Ship logos as `.webp` or `.png` where the uploader may be a plain editor.
- Fonts: ship `.woff2` under `static/fonts/` with an `@font-face` block, or let the client
  use **Website → Configuration → Fonts** (`/website/theme_upload_font`, which takes
  woff2/woff/ttf/otf/zip). Confirm the webfont licence covers self-hosting first.

## Translations

- Name the file for the **base** language — `es.po`, not `es_ES.po`. `get_po_paths` uses
  the base file for every variant (`es_ES`, `es_MX`, `es_419`). Only split when a variant
  genuinely needs different wording.
- Import runs `_load_module_terms(..., overwrite=True)`, so re-importing overwrites
  translations the client edited in the backend. Tell them that before they edit any.
- Activate the language on the database **before** importing, or the terms have nothing to
  attach to.
- Leave proper nouns — customer names, brands, product names — with an empty `msgstr`. An
  empty string falls back to the source, which is what you want.

## XML

- `--` is illegal inside an XML comment. It fails the import rather than warning, and the
  message does not point at the comment.
- View validation runs on the *combined* arch, so an inherit that breaks a core view fails
  at install time with the core view's name, not yours.
