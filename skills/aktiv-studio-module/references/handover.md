# Verify, package, hand over

## Verify

Do not assert that it works. Check it.

**1. Every XML file parses**
```bash
python3 -c "
import sys, glob, xml.etree.ElementTree as ET
bad = 0
for f in sorted(glob.glob('<module>/**/*.xml', recursive=True)):
    try:
        ET.parse(f)
    except ET.ParseError as e:
        bad += 1; print('FAIL', f, '->', e)
print('%s files, %s bad' % (len(glob.glob('<module>/**/*.xml', recursive=True)), bad))
sys.exit(1 if bad else 0)"
```
Python's parser, not `xmllint` — `xmllint` is not installed by default on most machines,
and a missing binary makes a shell loop print a pass for every file it never checked.
This is where a `--` inside a comment shows up, and nowhere else useful.

**2. The manifest is a plain dict with no logic**
```bash
python3 -c "
import ast,sys
src = open('<module>/__manifest__.py').read()
tree = ast.parse(src)
assert len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr), 'manifest has statements'
ast.literal_eval(tree.body[0].value)
print('manifest ok')"
```

**3. Every data file exists and has a loadable extension**
```bash
python3 -c "
import ast, os, sys
m = ast.literal_eval(ast.parse(open('<module>/__manifest__.py').read()).body[0].value)
bad = 0
for f in m.get('data', []) + m.get('demo', []):
    p = os.path.join('<module>', f)
    ok = os.path.exists(p) and f.rsplit('.', 1)[-1] in ('xml', 'csv', 'sql')
    if not ok: bad += 1
    print(('ok  ' if ok else 'FAIL'), f)
sys.exit(1 if bad else 0)"
```
A file listed here that is not `.xml`, `.csv` or `.sql` is skipped at import with no error,
so this check is the only thing standing between you and a module that installs and does
nothing.

**4. Every `ref=` resolves.** Grep each one and confirm it is defined in this module or in
a declared dependency. An unresolved ref fails the install with a message that names the
ref but not the file.

**5. Every field a view mentions exists** — either in `01_models.xml` or on the core model.

**6. Install it on a scratch database and open the page.** If a browser is available,
render it headless and look at the result rather than reasoning about it.

To install the zip the way Odoo Online does — rather than via `-i` on an addons path, which
does not exercise the import rules — use `base_import_module` from `odoo-bin shell`:

```python
from io import BytesIO
with open('<module>.zip', 'rb') as f:
    buf = BytesIO(f.read())
print(env['ir.module.module']._import_zipfile(buf))   # -> ('', ['<module>'])
env.cr.commit()
```

The method is `_import_zipfile` and it takes a file object, not base64. A non-empty first
element of the tuple is the error report.

Templates are compiled and cached per worker, so an edit made from `odoo-bin shell` while a
server is running will not show up until that server restarts. Restart before concluding a
render is wrong.

**7. Re-import with a bumped version** and confirm nothing the client owns was reset —
the `noupdate="1"` records, the homepage setting, their translations.

## Package

```bash
cd <parent-dir> && rm -f <module>.zip && \
zip -r <module>.zip <module> -x '*/__pycache__/*' '*.pyc' '*/.git/*'
```

Exclude by path, never by extension. `static/` carries fonts and images that an extension
filter will quietly swallow — and the import will succeed anyway, with the fonts missing.

Then prove they are in there:
```bash
unzip -l <module>.zip | grep -c 'static/' && unzip -l <module>.zip | tail -30
```

Check the size against the 100 MB ceiling.

## Hand over

Give the client four things, in this order:

1. **The zip and the install path** — Apps → ⋮ → Import Module → upload. One line.
2. **Every manual step the module cannot do for itself**, each as a single sentence with
   the menu path. Pointing a homepage, activating a language, ticking the first records.
   If a `<function>` ran on first install only and the module is already installed, that
   step is now manual — say so.
3. **What is still placeholder** — demo content that must be replaced before go-live,
   fonts and photography not yet supplied, invented testimonials. Be specific about which
   file and which records.
4. **What you need from them** — licences, real assets, URLs, decisions. A list they can
   action, not a paragraph.

State plainly what the module does not do. A price hidden in the markup is not a price
that cannot be fetched; a presentation-level change should never be handed over as a
security control.
