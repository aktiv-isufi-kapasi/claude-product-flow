# claude-product-flow

Shared Claude Code skills (slash commands) for the Aktiv product development team, built around Odoo module work. The repo holds no application code: every skill is a markdown instruction file that Claude Code loads as a slash command.

## Structure

```
skills/<name>/SKILL.md        one folder per skill; folder name = skill name = /command
skills/<name>/references/     optional detail the skill loads on demand
skills/<name>/scripts|assets/ optional helpers the skill runs (python-docx, openpyxl, Pillow)
install.sh                    symlinks each skills/<name>/ into ~/.claude/skills/ and installs a post-merge hook
README.md                     user manual: install, concepts, one section per skill with examples
package.json                  name, version, description only (no build, no dependencies)
```

## How it is installed

- Team clones into `~/.claude/claude-product-flow` and runs `./install.sh`.
- `install.sh` creates a symlink `~/.claude/skills/<name> -> skills/<name>` for every skill, then writes `.git/hooks/post-merge` so every `git pull` re-runs the install. It never overwrites a real (non-symlink) skill folder of the same name.
- Because they are symlinks, edits to an existing skill are live immediately. A new skill needs `install.sh` (or a pull) to get its symlink; Claude Code needs a restart to see it.
- Renaming or removing a skill and re-running the install (or pulling) deletes its now-broken symlink, from `~/.claude/skills/` and from the old `~/.claude/commands/` layout.

## Skills

Names follow `aktiv-<area>-<skill>`; the areas are listed in the README's "Skill names" section. Keep to it for new skills.

| Stage | Skill | Purpose |
|---|---|---|
| Discovery | `/aktiv-project-scope-analysis` | Gap analysis of client material: every requirement classified Standard / Config / App / Custom / Not feasible / Unclear, with evidence; outputs .docx + .xlsx + client questions |
| Discovery | `/aktiv-project-user-story` | User story .docx in the Aktiv format, built with the bundled `scripts/us_lib.py` and `annotate.py` |
| Start | `/aktiv-project-start` | Load feature context, then module context, then any read-only reference modules |
| Start | `/aktiv-project-scaffold` | Create the per-feature folder structure (`_overview.md`, `<area>/<feature>/context.md`, `interface.md`, `tests.md`) |
| Start | `/aktiv-guide` | Print the skill reference |
| Task | `/aktiv-project-dev` | Single entry point for feature, bug, research or sync work; asks at most 3 gap questions, then executes |
| Task | `/aktiv-market-research` | Conversational research on how other products solve a problem; always searches live, never from memory |
| Task | `/aktiv-feature-flow` | Map a decided feature into the product flow, functional only |
| Task | `/aktiv-module-sync` | Move a feature between module versions, feature-first rather than code migration |
| Task | `/aktiv-module-compatible` | Bring a sub-module in line with an updated core module; Breaking / Risk / Informational report |
| Task | `/aktiv-studio-module` | Data-only module for Odoo Online (Import Module, no custom Python) |
| Finish | `/aktiv-project-doc` | Update the module context file to current state only |
| Finish | `/aktiv-git-commit` | Structured, functional commit message (Current Behaviour / Expected Behaviour) with module versions from `__manifest__.py` |
| Release | `/aktiv-git-release` | Release only one task's / user story's commits from dev to a target: release branch + cherry-pick -x, staging merges, production rebases onto latest production first, then `--no-ff` merge; verifies task files match dev; never pushes |
| Finish | `/aktiv-pms-timesheet` | Timesheet entries for a day, grouped by feature, from git commits and the session |
| Client | `/aktiv-client-query` | Draft a client-facing message for the information or decisions we need |

Typical flow: `/aktiv-project-start` → `/aktiv-project-dev` → `/aktiv-project-doc` → `/aktiv-git-commit`, then `/aktiv-pms-timesheet` at the end of the day.

## Concepts the skills share

**Context files.** Each module documents its current state (flow, models, behavior) in markdown. Two layouts are supported and skills check them in this order:
1. New structure: `_overview.md` at module level, plus `<area>/<feature>/context.md` per feature.
2. Old structure: a single `.md` named after the module (never `README.md` or `CHANGELOG.md`).

Skills always confirm a found context file with the user before using it, and never mix content across modules.

**Core compatibility marker.** A sub-module's context file can carry `Core compatibility: <core_module> <version>`. `/aktiv-module-compatible` reads it to find the range of core changes to check; `/aktiv-module-compatible` and `/aktiv-project-doc` update it after work is done.

**Module versions** are always read from `__manifest__.py`, never guessed or bumped.

## Writing conventions for skills

Follow these when adding or editing a skill so all skills behave alike:

- **Frontmatter**: `name` equal to the folder name, and a one-sentence `description` of what it does and when to use it; Claude Code shows it in the skill list and uses it to decide when the skill applies.
- **Long detail goes in `references/`** and is pointed to from `SKILL.md`, so it loads only when needed.
- Sections in this order, as needed: `## Steps` (numbered), then format sections (`## Output`, `## Commit Message Format`, `## Entry Format` ...), then `## Rules` or `## Writing Rules`.
- **Prompts to the user** go in fenced blocks, with numbered choices (`1. Yes / 2. No (provide path) / 3. Don't have one`) and an Enter default where one makes sense (e.g. current working directory).
- **Ask rather than assume**: confirm paths, context files and anything unclear before writing.
- **Keep questions few**: only what is missing, in one message.
- **Functional over technical** in anything a non-developer reads (commits, timesheets, client queries, flows): no method, field, model or file names.
- **No em dashes** in generated output for commits, timesheets and client messages; use `:` or `-`.
- **Current state only** in context files: no history, changelogs or bug fix references.
- Files saved for the user go to `~/Desktop/<skill>_<YYYY-MM-DD>[_topic].txt`, plain text.

## Adding a new skill

1. Create `skills/aktiv-<area>-<skill>/SKILL.md` following the conventions above.
2. In `README.md`: add a row to "Which skill when" and "Skill names", a link in Contents, and a section in "Skill manual" (what it does, when to use it, what it asks, an example, what you get).
3. Add it to the reference in `skills/aktiv-guide/SKILL.md`, which `/aktiv-guide` prints verbatim.
4. Run `./install.sh` locally to create the symlink, restart Claude Code, try it.
5. Commit and push; the team gets it on `git pull`.

## Keeping the README in sync

`README.md` is the team's user manual and must describe each skill exactly as its `skills/<name>/SKILL.md` behaves. Whenever a skill's steps, questions, output format or saved file changes, update its README section (and `skills/aktiv-guide/SKILL.md` if the "when to use" changes) in the same commit. Examples in the README use realistic but generic data (`ak_odoo_cpq`, `S00046`, `Task #4521`), never real client names.
