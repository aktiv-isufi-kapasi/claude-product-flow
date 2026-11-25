---
name: aktiv-project-dev
description: "Single entry point for any development task. Accepts any input — detailed or thin — and ensures all required information is captured before work begins. Validates both functional and technical completeness. Reduces back-and-forth by asking only what is missing, in one shot."
---

Single entry point for any development task. Accepts any input — detailed or thin — and ensures all required information is captured before work begins. Validates both functional and technical completeness. Reduces back-and-forth by asking only what is missing, in one shot.

## Steps

1. Receive the user's input — feature idea, bug description, change request, anything.

2. Identify the task type:
   - **Feature** — adding or changing functionality
   - **Bug** — something broken or behaving incorrectly
   - **Research** — exploring options before deciding
   - **Sync** — moving a feature between versions

3. Check for critical gaps — both functional and technical — based on task type:

   **Feature gaps to check:**

   Functional:
   - What triggers it? (user action, condition, automatic?)
   - What is the expected behavior / outcome?
   - Any edge cases or optional flows?

   Technical:
   - Which model or module is affected?
   - Any specific method, view, or field to modify?
   - Any dependency on another module or external data?

   **Bug gaps to check:**

   Functional:
   - What was expected to happen?
   - What is actually happening?
   - Where in the flow does it break? (screen, action, condition)

   Technical:
   - Is there an error message or traceback?
   - Which model or method is involved?
   - Did it ever work before, or is this new behavior?

   **Research gaps to check:**

   Functional:
   - What decision will this research inform?

   Technical:
   - Any technical constraints to factor in? (version, module, performance)

   **Sync gaps to check:**

   Functional:
   - What does the feature do? (brief description)

   Technical:
   - Source version and target version?
   - Are there known structural differences between versions in this area?

4. Cross-check what is already known from the loaded context — do not ask for anything already covered there.
   If new folder structure is in use: check `_overview.md` for module-level facts and `<area>/<feature>/context.md` for feature-level facts before asking.

5. If critical information is missing — ask only the missing pieces, maximum 3 questions, in one message, one line each. Prioritize the most blocking gaps first.

6. If nothing is missing — proceed directly without asking anything.

7. Find the Odoo version before touching code: read the series from the module's `__manifest__.py` (`18.0.1.2.0` → `18.0`). If it is missing, or the module targets several versions, ask. Every view, field, API call and data record must use that version's syntax; check `references/odoo-versions.md` for what changed between versions, and the server source of that version for anything not listed there. Never write code from memory of another version.

8. Once input is complete, execute based on task type:
   - **Feature** → map the functional flow first. When the feature changes what users see or do, present a numbered user journey grounded in the real screens from the context file: where it appears, what triggers it, what the user does step by step, what changes on existing screens, and the outcome. Plain language only: no code, model or field names. Wait for OK, then implement. If the user asked for the flow only ("flow only", "just the journey"), stop after presenting it.
   - **Bug** → diagnose root cause from both functional and technical angle, propose fix
   - **Research** → search live, never answer from training data, present findings
   - **Sync** → read source version behavior and technical implementation, map to target version, implement

9. Before writing code for a Feature, Bug fix or Sync, weigh the options:
   - Look for what already exists first: standard Odoo, an installed module, or a helper in the project that can be reused or extended instead of new code.
   - When there is more than one reasonable way to build it (e.g. override vs. new hook, computed vs. stored field, server action vs. Python, extend core vs. client module), show them in one short message and recommend one:
     ```
     Options for <goal>:
     1. <approach> (recommended): <why: effort, upgrade safety, performance>
     2. <approach>: <trade-off>
     Proceed with 1? (Enter for yes, or pick another)
     ```
     If only one approach makes sense, say so in one line and continue without asking.

10. After implementing, review the change for optimisation before handing it over:
   - **Database work:** no search, read or write inside a loop where one batched call works; prefetch related records; use the version's grouped read (see `references/odoo-versions.md`) instead of counting in Python; avoid stored computed fields that recompute on every write unless they are needed for search or grouping.
   - **Reuse:** no duplicated logic that already exists in the module or core; call `super()` instead of copying core code.
   - **Front end:** no repeated RPC calls in a loop; load data once per screen.
   - **Simplicity:** remove dead code, unused imports, fields and views added during trial and error.
   Fix what you find, and list in the hand-over any trade-off that is left (e.g. "kept stored field for grouping on the list view").

## Rules

- Always validate both functional AND technical completeness before starting
- Never assume a gap and proceed silently — ask if something critical is missing
- Never ask more than 3 questions at once — prioritize the most critical gaps
- Never ask for what is already in the loaded context file
- If the user gave enough detail on both sides, skip questions entirely and go straight to work
- Keep questions short — one line each, no explanation needed
- The goal is faster execution, not interrogation
- **Version-correct code.** Code for the module's own Odoo version only; never mix syntax from another version (e.g. `<list>` on 17.0, `attrs` on 17.0+, `groups_id` on 19.0+).
- **Never change the `version` in `__manifest__.py`.** The developer bumps it at commit time. If the change needs a module upgrade (new field, new data), say so in the hand-over.
- **No migration scripts unless asked.** Unreleased development needs none. If a model change affects existing data, mention the impact instead.
- **Core modules are hands-off in client repos.** Do not copy, sync or edit core/base modules (e.g. a shared base module such as `ak_sale_approval` that the client's `ak_sale_approval_custom` extends) inside a client repository unless the user asks for that step. Comparing against core to understand compatibility is fine. Extend core through overrides that call `super()`, never by patching its internals.
- **Tests written only to check the work stay out of commits.** Keep them in the working tree or scratchpad and tell the user they are uncommitted. Ask before committing anything under `tests/` or `static/tests/`, or test-only manifest entries.
- **Do not update the context file on your own.** Stop at the code and a short summary; the user runs `/aktiv-project-doc` when the task is done.
- **Bring a branch up to date with rebase, not merge or pull** (`git rebase origin/<base>`). Check first whether the branch is already pushed, since rebasing rewrites its commits. Never push.
- **Short hand-over.** When done, say what changed and anything the user must act on (upgrade, decision, caveat) in a few lines. No long reports.
