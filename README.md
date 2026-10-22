# claude-product-flow

Claude Code skills for the Aktiv team working on Odoo projects. Each skill is a slash command (`/aktiv-project-start`, `/aktiv-project-dev`, `/aktiv-git-commit` ...) that walks Claude through one part of the job in the same way for everyone on the team.

This README is the user manual: how to install, the ideas the skills share, and a page per skill with what it asks, an example and what you get back.

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [Concepts](#concepts)
- [Which skill when](#which-skill-when)
- [Skill manual](#skill-manual)
  - Starting work: [/aktiv-project-start](#aktiv-project-start) · [/aktiv-project-scaffold](#aktiv-project-scaffold) · [/aktiv-guide](#aktiv-guide)
  - Doing a task: [/aktiv-project-dev](#aktiv-project-dev) · [/aktiv-market-research](#aktiv-market-research) · [/aktiv-feature-flow](#aktiv-feature-flow) · [/aktiv-module-sync](#aktiv-module-sync) · [/aktiv-module-compatible](#aktiv-module-compatible)
  - Finishing work: [/aktiv-project-doc](#aktiv-project-doc) · [/aktiv-git-commit](#aktiv-git-commit) · [/aktiv-git-release](#aktiv-git-release) · [/aktiv-pms-timesheet](#aktiv-pms-timesheet)
  - Discovery and specs: [/aktiv-project-scope-analysis](#aktiv-project-scope-analysis) · [/aktiv-project-user-story](#aktiv-project-user-story)
  - Odoo Online: [/aktiv-studio-module](#aktiv-studio-module)
  - Talking to the client: [/aktiv-client-query](#aktiv-client-query)
- [A day with the skills](#a-day-with-the-skills)
- [Skill names](#skill-names)
- [Contributing a skill](#contributing-a-skill)

---

## Install

```bash
git clone https://github.com/aktiv-isufi-kapasi/claude-product-flow ~/.claude/claude-product-flow
cd ~/.claude/claude-product-flow && ./install.sh
```

Restart Claude Code. Type `/aktiv` in Claude Code to see the skills.

Some skills build Word and Excel files (`/aktiv-project-user-story`, `/aktiv-project-scope-analysis`). They need a Python with `python-docx`, `openpyxl` and `Pillow`, which an Odoo virtualenv usually has.

### Update

```bash
cd ~/.claude/claude-product-flow && git pull
```

A post-merge hook re-runs the install after every pull: new skills are added, and links for renamed or deleted skills are removed. Restart Claude Code if a skill was added.

### Uninstall

```bash
find ~/.claude/skills ~/.claude/commands -maxdepth 1 -lname '*claude-product-flow*' -delete
rm -rf ~/.claude/claude-product-flow
```

---

## Quick start

```
New chat
  → /aktiv-project-start      load module context

Have a task
  → /aktiv-project-dev        describe your task, AI clarifies if needed, then builds

Done with task
  → /aktiv-project-doc        update context file
  → /aktiv-git-commit         generate commit message

End of day
  → /aktiv-pms-timesheet      write up the day's work
```

Anything you type after a command is passed to it, so `/aktiv-project-dev hide rule ignores optional components` or `/aktiv-pms-timesheet yesterday` work in one line.

---

## Concepts

### Context files

The skills work from a short markdown file that describes how a module works **right now**: its flow, models and behaviour. Claude reads this instead of the whole module, which keeps sessions focused and cheap. Two layouts are supported, checked in this order:

**New structure** (created by `/aktiv-project-scaffold`), one folder per feature:
```
ak_odoo_cpq_custom/
  _overview.md                  module purpose, dependencies, feature list
  rules/
    hide/
      context.md                what the feature does, trigger, models, edge cases
      interface.md              inputs, outputs, guarantees to other features
      tests.md                  test scenarios for QA
```

**Old structure**: one `.md` file named after the module, e.g. `ak_odoo_cpq.md`. `README.md` and `CHANGELOG.md` are never treated as context files.

Rules every skill follows:
- A found context file is always confirmed with you before it is used.
- One module, one context file. Content is never mixed across modules.
- Context files hold current behaviour only: no history, changelog or bug-fix notes. `/aktiv-project-doc` keeps them that way.

### Core compatibility marker

A sub-module that extends a core module records which core version it was last made compatible with, as one line in its context file:

```
Core compatibility: ak_odoo_cpq 18.0.5.18.11
```

`/aktiv-module-compatible` reads it to know which core changes to check. `/aktiv-module-compatible` and `/aktiv-project-doc` update it once the work is done.

### How skills talk to you

- Questions come with numbered answers. Reply with the number (`1`) or type your own answer.
- Where a question shows **Enter** as an option (e.g. "Press Enter to use current directory"), an empty reply takes that default.
- Skills ask only for what they can't find themselves, and never write files without showing you what they will do first.
- Module versions always come from `__manifest__.py`. No skill bumps a version.

---

## Which skill when

| You want to... | Use |
|---|---|
| Start a new chat on a module | `/aktiv-project-start` |
| Set up context files for a module that has none | `/aktiv-project-scaffold` |
| Build a feature, fix a bug or make a change | `/aktiv-project-dev` |
| Explore an idea before deciding to build it | `/aktiv-market-research` |
| See how a decided feature fits the product, before building | `/aktiv-feature-flow` |
| Bring a feature from v18 to v19 (or any version to another) | `/aktiv-module-sync` |
| Update a sub-module after its core module changed | `/aktiv-module-compatible` |
| Record what the module does now, after development | `/aktiv-project-doc` |
| Write the commit message | `/aktiv-git-commit` |
| Release a task from dev to staging or production | `/aktiv-git-release` |
| Fill in your timesheet | `/aktiv-pms-timesheet` |
| Ask the client for something that blocks you | `/aktiv-client-query` |
| Turn client material (SOW, spec, wireframes) into a gap analysis | `/aktiv-project-scope-analysis` |
| Write a user story document for a customization | `/aktiv-project-user-story` |
| Build a module for Odoo Online (no custom Python) | `/aktiv-studio-module` |
| Remember which skill to use | `/aktiv-guide` |

**`/aktiv-market-research` vs `/aktiv-feature-flow` vs `/aktiv-project-dev`**
- Still exploring, haven't decided: `/aktiv-market-research`
- Decided, want to see how it fits the product: `/aktiv-feature-flow`
- Know what to build: `/aktiv-project-dev`

**`/aktiv-project-scope-analysis` vs `/aktiv-project-user-story` vs `/aktiv-feature-flow`**
- Client sent material, need to know what is standard, an app, custom or not possible: `/aktiv-project-scope-analysis`
- A customization is agreed and needs a formal story document: `/aktiv-project-user-story`
- Just want the user journey for a feature, in chat: `/aktiv-feature-flow`

**`/aktiv-module-sync` vs `/aktiv-module-compatible`**
- Same feature, another version of the same module: `/aktiv-module-sync`
- Core module moved on, the module that depends on it must catch up: `/aktiv-module-compatible`

---

## Skill manual

### Starting work

#### /aktiv-project-start

Loads the context for the module you're about to work on, so Claude knows the module before you describe the task.

**Use it:** at the start of every new chat.

**It asks:**
1. Development directory (Enter = current directory).
2. What you're working on (optional). If it matches a feature folder, that feature's `context.md` is read first.
3. Confirms the module context file it found.
4. Whether there is a reference or dependency module to load too. Reference modules are read-only. You can add as many as you need.

**Example:**
```
You:    /aktiv-project-start
Claude: What is the development directory? (Press Enter to use current directory: /home/odoo/v18/ak_odoo_cpq_custom)
You:    ⏎
Claude: What are you working on? (e.g. "hide rule", "assignment flow"). Press Enter to skip
You:    hide rule
Claude: Feature context: rules/hide/context.md
        - Hides components on the CPQ screen when a rule's conditions match
        - Runs on every attribute change in the configurator
        Found: `_overview.md` — is this the right context file? 1. Yes 2. No 3. Don't have a context file
You:    1
Claude: Is there a reference or dependency module I should also be aware of? 1. Yes 2. No
You:    1 → /home/odoo/v18/ak_odoo_cpq
Claude: ak_odoo_cpq (read-only reference): ... Context loaded. What are we working on?
```

**Tip:** no context file yet? Say "Don't have a context file" and run `/aktiv-project-scaffold` after.

#### /aktiv-project-scaffold

Creates the new-structure folders and empty template files for a module. It only writes the headings; you or `/aktiv-project-doc` fill in the content.

**Use it:** once per module, when it has no context files yet. Run it again to add new features.

**It asks:**
1. Module directory, module name and version.
2. Whether it depends on a base module. If so, the base module gets an `interface.md` only, because it is read-only.
3. The features, grouped by area.
4. Shows the tree it will create and waits for your OK.

**Example:**
```
You:    /aktiv-project-scaffold
Claude: Module name and version? (e.g. ak_odoo_cpq_custom v19)
You:    ak_odoo_cpq_custom v18
Claude: Does this module inherit from or depend on another module? 1. Yes 2. No
You:    1, ak_odoo_cpq
Claude: List the features to scaffold, grouped by area.
You:    rules: hide, block, warning
        pricing: formula
Claude: Will create:
          ak_odoo_cpq_custom/_overview.md
          ak_odoo_cpq_custom/rules/hide/{context,interface,tests}.md
          ... 
          ak_odoo_cpq/interface.md
        Proceed? 1. Yes 2. Adjust
```

**You get:** the folder tree, then next steps: fill `_overview.md`, fill `context.md` for the features you're working on, and fill `tests.md` before QA.

#### /aktiv-guide

Prints the quick reference of all skills and when to use each one, then asks if you want more detail on any of them. Use it when you're not sure which skill fits.

---

### Doing a task

#### /aktiv-project-dev

The single entry point for development. Give it anything, from one line to a full spec. It checks both what should happen (functional) and where in the code (technical), asks only what's missing, then does the work.

**Use it:** for any feature, bug or change.

**What happens:**
1. It sorts the task into Feature, Bug, Research or Sync.
2. It checks for gaps. For a bug, for example: expected vs actual behaviour, where it breaks, any traceback. Anything already in the loaded context is not asked again.
3. If something is missing, it asks at most 3 one-line questions in one message. If nothing is missing, it starts straight away.
4. It does the work: features are mapped functionally first, then built. Bugs are diagnosed from both angles and a fix is proposed.

**Example (thin input):**
```
You:    /aktiv-project-dev hidden components still show in the BoM
Claude: 1. Does it happen on sale order confirmation or when the BoM is generated from the configurator?
        2. Any error, or just the wrong lines?
You:    on SO confirm, no error
Claude: (diagnoses, proposes the fix, implements after you agree)
```

**Example (enough detail, no questions):**
```
You:    /aktiv-project-dev When a hide rule hides a component in the CPQ screen, also exclude it from the BoM created on SO confirmation. Module ak_odoo_cpq_custom.
Claude: (goes straight to the functional flow and implementation)
```

**Tip:** run `/aktiv-project-start` first so `/aktiv-project-dev` doesn't need to ask about the module.

#### /aktiv-market-research

A brainstorming partner for product ideas. It searches the web live (app stores, competitor sites, reviews, forums, demos) and never answers from memory, because products change all the time.

**Use it:** before deciding what to build.

**Three ways in:**
- **Specific idea:** "Would a guided wizard for first-time configuration help?" It checks how others do it, what works and what doesn't.
- **A direction:** "Something to reduce quoting errors." It surveys what exists and gives options to react to.
- **Blank slate:** "What are we missing?" It reads the product context, then looks for features that similar products have and this one doesn't.

**It asks:** the development directory or a product description, and confirms the context file. Without one, it asks 2 to 3 questions about what the product does and who uses it.

**You get:** a conversation, not a report. Every answer ends with a question to narrow or widen the search. Ask for a deep dive and it runs several targeted searches and checks each claim against more than one source.

#### /aktiv-feature-flow

Shows where a decided feature fits in the product, from the user's side only: no code, no model names.

**Use it:** after deciding, before building, when you want to agree on the user experience first (with the team or the client).

**It asks:** the directory, confirms the context file, and the feature to map.

**You get:** a numbered user journey covering where the feature appears, what triggers it, what the user does step by step, what changes in existing screens, and the outcome.

**Example output:**
```
Feature: Save configuration as template
1. On the CPQ configurator, after choosing options, the user sees a new "Save as template" button
2. Clicking it asks for a template name
3. Next time, on a new quotation, "Start from template" lists saved templates
4. Choosing one pre-fills all options; the user can still change any of them
Changes to existing flow: the configurator's first step gains a "Start from template" choice
```

#### /aktiv-module-sync

Brings a feature from one version of a module to another. It works feature-first: it understands what the feature does, then builds it the way the target version is built. It does not copy code across.

**Use it:** for example, when a feature built in v18 is needed in v19.

**It asks:**
1. Source directory (where the feature exists).
2. Target directory (where it should go).
3. A feature reference: commit hash, commit message or plain description.
4. Confirms the context file in each directory, and the feature context if you use the new structure.

**You get:** an implementation plan for the target version, and no code until you confirm it. It reads code only where the two versions really differ, and asks you before reading more.

**Example:**
```
You:    /aktiv-module-sync
        Source: /home/odoo/v18/ak_odoo_cpq   Target: /home/odoo/v19/ak_odoo_cpq
        Feature: 3f2a91c
Claude: Plan for v19: ... Proceed?
```

#### /aktiv-module-compatible

Checks a sub-module against an updated core module and fixes what broke. It covers technical changes (methods it overrides that changed or were removed, new parameters) and functional ones (changed flows, new rules).

**Use it:** after the core module (e.g. `ak_odoo_cpq`) is updated and a module built on it must catch up.

**It asks:**
1. Sub-module directory and core module directory.
2. Confirms both context files.
3. Uses the `Core compatibility:` marker to suggest the version range to check. Without a marker, it asks for a commit reference or a description.

**You get** a report, then a choice: fix breaking issues now, decide per item, or keep only the report.
```
Compatibility Report
──────────────────
Breaking:
- Core renamed the BoM line builder: sub-module override no longer runs → re-point override
Risk:
- Core added a company check on rule evaluation → review multi-company rules
Informational:
- Core added rule priorities → sub-module can expose them later
```

After the fixes, it offers to update the marker to the current core version, so the next check starts from there. Each fix is proposed and confirmed before it is written.

---

### Finishing work

#### /aktiv-project-doc

Brings the module's context file up to date after development. It describes how the module works now, never what changed.

**Use it:** after finishing a feature or fix, before `/aktiv-git-commit`.

**What happens:**
1. Asks for the directory and confirms the context file.
2. Finds the last commit that touched the context file and suggests "changes since then" as the range. You can give another commit or describe the changes yourself.
3. Shows which sections it will update and how, and waits for your OK.
4. Writes only those sections, in the file's existing style.
5. Offers to update the `Core compatibility:` marker, or to add one if the module depends on a core module.

**Example proposal:**
```
I'll update these sections:
- Hide rule: hidden components are also excluded from the BoM on SO confirmation
- Edge cases: add optional components hidden by a rule
Proceed? 1. Yes 2. No (adjust)
```

#### /aktiv-git-commit

Writes a structured commit message from your changes, in the team format, so anyone can read from the log what the problem was and how it behaves now.

**Use it:** when the work is ready to commit.

**It asks:** change type (it suggests one), task ID and task name. Press Enter to skip the task. If the behaviour before the change isn't clear from the diff, it asks what happens today.

**Format:**
```
[TYPE] #<task_id> | module[version], module[version]: <Short description>

Current Behaviour:
- <What happens before this change>

Expected Behaviour:
- <What happens after this change>

Task #<task_id>, <Task Name>
```

**Types:** `[ADD]` new feature · `[IMP]` improvement · `[FIX]` bug fix · `[HOTFIX]` urgent production fix · `[REL]` release (may list released items instead of the two sections).

**Example:**
```
[FIX] #4521 | ak_odoo_cpq_custom[18.0.1.4.2]: Remove hidden components from the BoM

Current Behaviour:
- Components hidden by a rule still appear in the BoM after the sale order is confirmed

Expected Behaviour:
- Components hidden by a rule are removed from the BoM as well as from the CPQ screen

Task #4521, CPQ hide rule fixes
```

**Rules it follows:** subject under 72 characters and about the outcome. Bullets in plain language a non-developer understands, with no method, field, model or file names. No em dashes. Versions taken exactly from `__manifest__.py`.

#### /aktiv-git-release

Releases one task or user story from dev to staging or production **through git only**, so nothing is copied by hand and no file gets left behind. Only the commits for that task are released, even if dev has other unreleased work.

**Use it:** every time code goes from dev to staging or production. Never copy module folders between branches or servers.

**It asks:**
1. Repository directory. It stops if there are uncommitted changes.
2. Source branch (Enter = `dev`), target branch, and the task ID(s) or user story number(s), e.g. `4521` or `US-05`.
3. Whether the target is staging (merge only) or production (rebase onto latest production, then merge).

**What happens:**
1. **Finds the task's commits** on dev that aren't on the target yet, by the task ID in the commit message (`#4521` in the subject or `Task #4521` in the footer, as `/aktiv-git-commit` writes them) or the user story number. Commits already released are skipped.
2. **Checks dependencies:** it lists other dev commits that touch the same files. These are the files that would otherwise go missing. You choose to include them, leave them out, or stop.
3. **Shows the plan** (commits, files, versions) and waits for your OK.
4. **Builds `release/<target>-<id>`** from the latest target and applies only those commits, each one recording the dev commit it came from. If there's a conflict, it stops and asks; it never resolves conflicts silently.
5. **Production only:** rebases the release branch onto the latest production. **Staging:** no rebase.
6. **Verifies:** every task file is identical to dev, no other files changed, module versions look right, and Python and XML files load.
7. **Merges** the release branch into the target with `--no-ff` and a `[REL]` message.

**You get:** the release merged on your local target branch, **not pushed**. Review it, then push yourself:
```
Release ready on local `production` (not pushed).
Review, then push yourself:
  git push origin production
After pushing, the release branch can be deleted:
  git branch -d release/production-4521
```

**Example plan:**
```
Release #4521 → production (from dev)

Commits (oldest first):
- a1b2c3d [FIX] #4521 | ak_odoo_cpq_custom[18.0.1.4.2]: Remove hidden components from the BoM
- d4e5f6a [FIX] #4521 | ak_odoo_cpq_custom[18.0.1.4.2]: Keep optional components visible

Files (5): models/sale_order.py, views/cpq_views.xml, data/hide_rule_data.xml, __manifest__.py, security/ir.model.access.csv

Other dev commits touching these files (not included):
- 9f8e7d6 [IMP] #4498 | ...: Rule priorities  → touches models/sale_order.py

1. Release these commits  2. Also include the others  3. Adjust  4. Stop
```

**Tip:** release works best when every commit carries its task ID, so always use `/aktiv-git-commit` with the task number.

#### /aktiv-pms-timesheet

Turns a day's work into timesheet entries: one per feature, written for a reviewer.

**Use it:** at the end of the day, or later for a past day.

**How to call it:** `/aktiv-pms-timesheet`, `/aktiv-pms-timesheet today`, `/aktiv-pms-timesheet yesterday`, `/aktiv-pms-timesheet 13th october`.

**What happens:**
1. It reads your commits for that day across all branches and uses the task ID and name from the commit footers.
2. It adds work from the session that has no commit, such as testing, investigation or data loading. It never invents work.
3. It groups several commits for one feature into one entry, and builds each entry from the commit's Expected Behaviour.
4. If you paste a screenshot of what you have already logged, it produces only the missing entries.
5. It shows the entries with commit IDs so you can check them, and offers to save `~/Desktop/timesheet_<YYYY-MM-DD>.txt` as plain text without commit IDs.

**Example (saved file):**
```
13 October 2026 - Task #4521, CPQ hide rule fixes

1. Removed hidden components from the BoM:
Components hidden by a rule on the CPQ screen are now also left out of the BoM when the sale order is confirmed. Tested on S00046 to S00049.

2. Investigated pricing difference on SO0052:
Traced the difference to an outdated price list on the customer; no code change needed.
```

---

### Discovery and specs

#### /aktiv-project-scope-analysis

Reads what the client sent (SOW or RFQ spreadsheets, requirement documents, wireframes, brand PDFs, email threads) and works out, for every requirement, whether Odoo already does it, an app covers it, it must be built, or it cannot be done as written. Verdicts are proved against the Odoo source for the target version and apps.odoo.com, never from memory.

**Use it:** in pre-sales, at the start of a new build, or when a change request comes in.

**It asks** five things before opening anything:
1. The input files, and whether only part is in scope ("only sheet 17").
2. Version, edition and hosting (Online, Odoo.sh, on-premise). All three change the verdicts.
3. Stage: pre-sales, new build or change request.
4. Whether it's an existing project. If so, give it the module context file that `/aktiv-project-doc` maintains, so things already delivered show as in scope instead of as gaps.
5. Where to write the output, and whether it's for the team, the client or both.

**Every requirement gets one verdict:** Standard · Config · App · Custom · Not feasible as specified · Unclear. Each one comes with evidence: a module name, `file.py:line`, an app URL with price and version, or the constraint that blocks it.

**You get:**
- `<name>_gap_analysis.docx`: the written analysis, with the markdown draft kept alongside for the next round
- `<name>_requirements.xlsx`: one row per requirement, colour-coded by verdict, with a summary tab
- a numbered question list for the client, blocking questions first, ready to paste into an email (or hand to `/aktiv-client-query`)

It doesn't estimate hours (only S / M / L / XL bands) and doesn't design the solution.

#### /aktiv-project-user-story

Writes a user story as a `.docx` in the Aktiv format: Poppins font, navy headings, maroon feature headings, field tables with a Type column, and screenshots annotated with red arrows.

**Use it:** when a customization is agreed and needs a story document, e.g. "write US-05 for the international invoice", or to turn a client spec or PDF into a story.

**What happens:**
1. **It asks first.** It collects every open question (scope, screen layout, field types, what can be reused, what is deferred) and doesn't start until they're answered. It also checks standard Odoo and our modules, so the story reuses existing fields instead of duplicating them.
2. **It writes the story only.** It never builds the feature to get a screenshot. Screenshots come from standard Odoo, from a project that already has the customization, or are left as placeholders.
3. **It builds the document** with the bundled builder, so every story looks the same.

**Document structure:**
```
User Story 5: International Invoice
1. Business Requirements      context, need, value
2. Functional Specifications  Modules Impacted, then per feature 2.x:
                              Description · UI Elements (field table + annotated screenshot) · Behavior
3. Success Criteria           testable bullets per feature
4. Change Log                 1.0 | Original user story drafted and finalized.
```

**You get:** `user_stories/US-05_International_Invoice.docx` in the project (extra stories: `Extra-US05_...`), opened again after saving to check it.

Stories are written only for customizations, never for standard or configuration features.

---

### Odoo Online

#### /aktiv-studio-module

Builds or extends a module for **Odoo Online (SaaS)**, where custom Python can't run and modules are installed through Apps → Import Module. The module is data only: Studio-style models and fields, backend screens, website pages, access rules, scheduled jobs and server actions in sandboxed code, translations and styling.

**Use it:** when the client is on Odoo Online. On Odoo.sh or self-hosted it stops and tells you to write a normal Python module instead.

**It asks:**
1. Module directory and technical name.
2. Odoo Online or Odoo.sh / self-hosted, and the version.
3. What the module needs. You pick from a list: new models, fields on existing models, backend screens, a new website page, changes to existing pages, access rights, scheduled job, button logic, translations, styling.
4. The prefix for custom fields, e.g. `x_ex_`.
5. For website pages: who edits the text after go-live. This decides whether the page keeps taking module updates or freezes after the client's first edit, so it is never guessed.
6. Languages, if translations were picked.

**You get:** a file plan in the correct load order to approve, then the module. It checks against a list of platform traps that fail silently, then gives you a verification checklist, the zip command and notes for the client.

---

### Talking to the client

#### /aktiv-client-query

Drafts one message to the client asking for the information or decisions that are holding work up. It is written for someone who doesn't use Odoo.

**Use it:** when you're blocked on the client, or had to assume something they should confirm.

**How to call it:** `/aktiv-client-query` (uses the open questions from this session) or `/aktiv-client-query fonts and photography` (one topic).

**What happens:**
1. It collects open questions from what you named, from the session, and from project notes.
2. It drops anything we can answer ourselves by checking the code, database or site first.
3. It flags questions already asked ("asked on 3 Oct, no reply yet") instead of asking again.
4. More than five questions? It groups them by topic and asks which group to send.
5. It asks who the message is for and what must not go in.
6. It shows the draft, ready to paste, and offers to save `~/Desktop/query_<YYYY-MM-DD>_<topic>.txt`.

**Example:**
```
Subject: Fonts and photos for the homepage

We are finishing the homepage design and need two decisions to complete it this week.

1. Which font should we use for headings?
   Why we need it: all page titles use it.
   If we do not hear back: we will use Poppins, which matches your logo.
   Options: Poppins, Montserrat or Lato.

2. Do you have your own product photos, or should we use stock images?
   Why we need it: this is a blocker for the product section.
   If we do not hear back: we will use stock images and swap them later.

We will finish the homepage once we have these; an answer by Thursday keeps us on schedule.
```

Every question has a recommended default, so silence doesn't stop the work. No field names, internal URLs, credentials or staff names go in.

---

## A day with the skills

```
09:00  /aktiv-project-scope-analysis    → client's new SOW tab scored against what is built; 4 questions found
09:30  /aktiv-project-start             → load ak_odoo_cpq_custom, feature "hide rule", core ak_odoo_cpq as reference
09:35  /aktiv-project-dev hidden components still show in the BoM
                                        → 2 questions, diagnosis, fix
11:00  /aktiv-client-query hide rule scope
                                        → message asking whether optional components count, sent to client
11:10  /aktiv-project-doc               → context file updated for the new behaviour
11:15  /aktiv-git-commit                → [FIX] message with Current / Expected Behaviour
11:30  /aktiv-git-release               → #4521 released dev → staging, every task file verified against dev
14:00  /aktiv-market-research           → "how do other CPQ tools handle configuration templates?"
15:00  /aktiv-feature-flow              → template feature mapped as a user journey
16:00  /aktiv-project-user-story        → US-06 Configuration Templates written for client sign-off
18:00  /aktiv-pms-timesheet today       → entries for the day, saved to Desktop
```

---

## Skill names

Every skill is named `aktiv-<area>-<skill>`, so typing `/aktiv` lists them all and the area tells you what it's about:

| Area | Covers | Skills |
|---|---|---|
| `project` | the module or project you're working on | `start`, `scaffold`, `dev`, `doc`, `scope-analysis`, `user-story` |
| `feature` | one feature's place in the product | `flow` |
| `market` | what other products do | `research` |
| `module` | one module against another version or its core | `sync`, `compatible` |
| `studio` | Odoo Online data-only modules | `module` |
| `git` | version control | `commit`, `release` |
| `pms` | project management system | `timesheet` |
| `client` | messages to the client | `query` |

`/aktiv-guide` has no area because it covers all skills.

Earlier names (`/start`, `/doc`, `/commit` ...) were removed. The install deletes their old links automatically on the next pull.

---

## Contributing a skill

Each skill is a folder in `skills/` with a `SKILL.md`, plus optional `references/` (detail loaded only when needed) and `scripts/` or `assets/` (helpers the skill runs). `install.sh` links each folder into `~/.claude/skills/`, so edits to an existing skill take effect right away for anyone who installed from the repo.

```
skills/aktiv-<area>-<skill>/
  SKILL.md          frontmatter (name, description) + instructions
  references/       optional
  scripts/          optional
```

To add a skill:

1. Create `skills/aktiv-<area>-<skill>/SKILL.md`. Start with frontmatter: `name` (same as the folder) and `description` (one sentence on what it does and when to use it; Claude Code shows it in the list and uses it to decide when the skill applies). Follow the conventions in [`CLAUDE.md`](CLAUDE.md).
2. Add it to [Which skill when](#which-skill-when), [Skill names](#skill-names) and Contents, and write its section in the [Skill manual](#skill-manual): what it does, when to use it, what it asks, an example and what you get.
3. Add it to `skills/aktiv-guide/SKILL.md`, which `/aktiv-guide` prints word for word.
4. Run `./install.sh`, restart Claude Code and try it.
5. Commit with `/aktiv-git-commit` and push. The team gets it on their next `git pull`.

When you change how an existing skill behaves, update its manual section in this README in the same commit.
