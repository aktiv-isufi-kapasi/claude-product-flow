# claude-product-flow

Shared Claude Code skills (slash commands) for the Aktiv product development team, built around Odoo module work. The repo holds no application code: every skill is a markdown instruction file that Claude Code loads as a slash command.

## Structure

```
commands/<skill>.md   one file per skill; filename = command name (/skill)
install.sh            symlinks commands/*.md into ~/.claude/commands/ and installs a post-merge hook
README.md             team-facing install guide and skill catalogue
package.json          name, version, description only (no build, no dependencies)
```

## How it is installed

- Team clones into `~/.claude/claude-product-flow` and runs `./install.sh`.
- `install.sh` creates a symlink `~/.claude/commands/<skill>.md -> commands/<skill>.md` for every skill, then writes `.git/hooks/post-merge` so every `git pull` re-runs the install.
- Because they are symlinks, edits to an existing skill are live immediately. A new skill needs `install.sh` (or a pull) to get its symlink; Claude Code needs a restart to see it.
- Removing a skill file and re-running the install (or pulling) deletes its now-broken symlink from `~/.claude/commands/`.

## Skills

| Stage | Skill | Purpose |
|---|---|---|
| Start | `/start` | Load feature context, then module context, then any read-only reference modules |
| Start | `/scaffold` | Create the per-feature folder structure (`_overview.md`, `<area>/<feature>/context.md`, `interface.md`, `tests.md`) |
| Start | `/guide` | Print the skill reference |
| Task | `/dev` | Single entry point for feature, bug, research or sync work; asks at most 3 gap questions, then executes |
| Task | `/research` | Conversational feature research; always searches live, never from memory |
| Task | `/flow` | Map a decided feature into the product flow, functional only |
| Task | `/sync` | Move a feature between module versions, feature-first rather than code migration |
| Task | `/compatible` | Bring a sub-module in line with an updated core module; Breaking / Risk / Informational report |
| Finish | `/doc` | Update the module context file to current state only |
| Finish | `/commit` | Structured, functional commit message (Current Behaviour / Expected Behaviour) with module versions from `__manifest__.py` |
| Finish | `/timesheet` | Timesheet entries for a day, grouped by feature, from git commits and the session |
| Client | `/query` | Draft a client-facing message for the information or decisions we need |

Typical flow: `/start` → `/dev` → `/doc` → `/commit`.

## Concepts the skills share

**Context files.** Each module documents its current state (flow, models, behavior) in markdown. Two layouts are supported and skills check them in this order:
1. New structure: `_overview.md` at module level, plus `<area>/<feature>/context.md` per feature.
2. Old structure: a single `.md` named after the module (never `README.md` or `CHANGELOG.md`).

Skills always confirm a found context file with the user before using it, and never mix content across modules.

**Core compatibility marker.** A sub-module's context file can carry `Core compatibility: <core_module> <version>`. `/compatible` reads it to find the range of core changes to check; `/compatible` and `/doc` update it after work is done.

**Module versions** are always read from `__manifest__.py`, never guessed or bumped.

## Writing conventions for skills

Follow these when adding or editing a skill so all skills behave alike:

- **First line** is a one-sentence description of what the skill does; Claude Code shows it in the skill list.
- Sections in this order, as needed: `## Steps` (numbered), then format sections (`## Output`, `## Commit Message Format`, `## Entry Format` ...), then `## Rules` or `## Writing Rules`.
- **Prompts to the user** go in fenced blocks, with numbered choices (`1. Yes / 2. No (provide path) / 3. Don't have one`) and an Enter default where one makes sense (e.g. current working directory).
- **Ask rather than assume**: confirm paths, context files and anything unclear before writing.
- **Keep questions few**: only what is missing, in one message.
- **Functional over technical** in anything a non-developer reads (commits, timesheets, client queries, flows): no method, field, model or file names.
- **No em dashes** in generated output for commits, timesheets and client messages; use `:` or `-`.
- **Current state only** in context files: no history, changelogs or bug fix references.
- Files saved for the user go to `~/Desktop/<skill>_<YYYY-MM-DD>[_topic].txt`, plain text.

## Adding a new skill

1. Create `commands/<skill-name>.md` following the conventions above.
2. Add it to the matching table in `README.md` (and to "When to use which skill" if it overlaps an existing one).
3. Add it to the reference in `commands/guide.md`, which is printed verbatim by `/guide`.
4. Run `./install.sh` locally to create the symlink, restart Claude Code, try it.
5. Commit and push; the team gets it on `git pull`.
