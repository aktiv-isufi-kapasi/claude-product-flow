Generate timesheet entries for a given day from the user's git commits and the work done in the session. One entry per feature, written for a reviewer, not a developer.

## Steps

1. Read the date from the arguments (e.g. `13th october`, `2026-10-13`, `today`). If none is given, use today. Resolve it to `YYYY-MM-DD`.

2. If the user shares a screenshot or list of entries already logged for that day, read it first. Only produce the entries that are still missing, and say which existing entry matches which commit.

3. Collect the day's commits by the user across all branches:
   ```
   git log --all --author='<git user.name>' --since='<date> 00:00' --until='<date> 23:59' --reverse --format='=== %h %ad%n%s%n%b' --date=format:'%H:%M'
   ```
   - Drop the `Task #...` footer and attribution lines from the bodies.
   - When a body has `Current Behaviour:` / `Expected Behaviour:` sections, build the entry from `Expected Behaviour` (what users can do now); use `Current Behaviour` only to make a fix entry clear.
   - Read the task ID and task name from the commit footers (`Task #<id>, <name>`).
   - Also check `git log --all --since='<date>'` for reverts of the user's commits by others. The work still counts on the day it was done; mention the revert in a short note after the entries.

4. Add work from the session that has no commit (testing, investigation, reports, data loading, reviews). Only include work that actually happened; never invent entries.

5. Group the commits by feature, not by commit. Several commits for one feature (fix-ups, follow-ups, both modules) become one entry. Keep entries in the order the work was done.

6. Present the entries (format below), with the commit IDs in brackets after each title so the user can cross-check.

7. Offer to save them as a txt file on the Desktop. When saving, write `~/Desktop/timesheet_<YYYY-MM-DD>.txt` without the commit IDs and without markdown (plain numbered titles, no `**` or `>`).

## Entry Format

**In the chat:**
```
**1. <Short title>** (`<hash>`, `<hash>`)
> <What the user or system can now do, 1 to 4 sentences.>
```

**In the txt file:**
```
<D Month YYYY> - Task #<id>, <Task Name>

1. <Short title>:
<Description.>

2. <Short title>:
<Description, with bullets if the feature has several distinct parts:>
- <part>
- <part>
```

## Writing Rules

- **Title:** past tense, functional, short (e.g. "Added an Archive feature for sessions", "Kept SO line taxes when editing a CPQ session").
- **Description:** describe the outcome in plain language, what users see or can do now. Use bullets only when one feature has several distinct parts.
- **No technical detail:** no method, field, model, file or variable names, no code.
- **References are fine:** record names used to reproduce or test (e.g. `S00045`, `Session/095`, `SO0052`) and testing scope ("Tested several cases on S00046 to S00049").
- **Testing and investigation work** gets its own entry: what was tested or analysed and what was found or fixed.
- **Never use em dashes (`—`).** Use `:` or `-`.
- No commit IDs, versions or branch names inside the description text.
- Keep it short for simple changes; explain each behavior for larger features. Quality over brevity.
