---
name: aktiv-pms-timesheet
description: "Generate timesheet entries for a given day from the user's git commits and every Claude Code session on this machine, across all projects. One entry per feature, grouped by project with its path, written for a reviewer, not a developer."
---

Generate timesheet entries for a given day from the user's git commits and every Claude Code session on this machine, across all projects. One entry per feature, grouped by project with its path, written for a reviewer, not a developer.

## Steps

1. Read the date from the arguments (e.g. `13th october`, `2026-10-13`, `today`). If none is given, use today. Resolve it to `YYYY-MM-DD`.

2. If the user shares a screenshot or list of entries already logged for that day, read it first. Only produce the entries that are still missing, and say which existing entry matches which commit.

3. Find every project worked on that day from the Claude Code sessions, not only the current one:
   - Read all transcripts under `~/.claude/projects/*/*.jsonl`. Timestamps are UTC: convert the day's local bounds to UTC before filtering (e.g. IST day `2026-11-24` = `2026-11-23T18:30Z` to `2026-11-24T18:30Z`).
   - For each session with activity in that window, note its working directory (`cwd`), the user's requests and what was done (edits, commits, tests, releases, analysis). Skip sessions with only `/aktiv-pms-timesheet` runs.
   - If a session's directory is on a drive that is not mounted (e.g. `/media/...`), say so and ask the user to mount it, then continue.
   - If the user asks for web chats as well, read the browser history (Chrome, Brave, Firefox under `~/.config` / `~/.mozilla`; copy the database to the scratchpad before opening it) for claude.ai and chatgpt.com visits that day and match their titles to the projects. Never read chat contents beyond titles.

4. Collect the day's commits by the user, in every repository found in step 3 plus the current one:
   ```
   git -C <repo> log --all --author='<git user.name>' --since='<date> 00:00' --until='<date> 23:59' --reverse --format='=== %h %ad%n%s%n%b' --date=format:'%H:%M'
   ```
   - Drop the `Task #...` footer and attribution lines from the bodies.
   - When a body has `Current Behaviour:` / `Expected Behaviour:` sections, build the entry from `Expected Behaviour` (what users can do now); use `Current Behaviour` only to make a fix entry clear.
   - Read the task ID and task name from the commit footers (`Task #<id>, <name>`).
   - Also check `git log --all --since='<date>'` for reverts of the user's commits by others. The work still counts on the day it was done; mention the revert in a short note after the entries.

5. Add work from the sessions that has no commit (testing, investigation, releases, reports, data loading, reviews, meetings). Only include work that actually happened; never invent entries. If the user limits the request to one project ("only for Trojan"), keep only that project.

6. Group by project, then by feature inside each project. Several commits for one feature (fix-ups, follow-ups, both modules) become one entry. Keep projects and entries in the order the work was done. Number entries across the whole day.

7. Present the entries (format below), with the commit IDs in brackets after each title so the user can cross-check, and the path under each title so the user can tell which project it belongs to.

8. Offer to save them as a txt file on the Desktop. When saving, write `~/Desktop/timesheet_<YYYY-MM-DD>.txt` without the commit IDs and without markdown (plain numbered titles, no `**` or `>`), keeping the project headings and paths.

## Entry Format

**In the chat:**
```
## Project <n>: <Project name>, <short context>, Task #<id>
Repo: `<repo path>`, branch `<branch>`

**1. <Short title>** (`<hash>`, `<hash>`)
- Path: `<module or folder path>`
> <What the user or system can now do, 1 to 4 sentences.>
```

**In the txt file:**
```
<D Month YYYY>

<Project name> - Task #<id>, <Task Name>
Path: <repo path>

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
- No commit IDs, versions or branch names inside the description text. Paths go on their own `Path:` line, never in the description.
- Keep it short for simple changes; explain each behavior for larger features. Quality over brevity.
