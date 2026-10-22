---
name: aktiv-guide
description: "Show all available skills and when to use each one."
---

Show all available skills and when to use each one.

## Output

Display the following reference guide exactly:

---

## Skills Reference

### When a project starts or changes
| Situation | Skill |
|---|---|
| Client sent a SOW, spec or wireframes: what is standard, app, custom or not feasible | `/aktiv-project-scope-analysis` |
| A customization is agreed and needs a user story document | `/aktiv-project-user-story` |

### When starting work
| Situation | Skill |
|---|---|
| Opening a new chat to work on a module | `/aktiv-project-start` |
| Module has no folder structure yet | `/aktiv-project-scaffold` |

### When doing a task
| Situation | Skill |
|---|---|
| Any development task — feature, bug, change | `/aktiv-project-dev` |
| Exploring a feature idea before deciding | `/aktiv-market-research` |
| Mapping how a decided feature fits the product | `/aktiv-feature-flow` |
| Moving a feature from one version to another | `/aktiv-module-sync` |
| Core module updated, sub-module needs to catch up | `/aktiv-module-compatible` |
| Building a module for Odoo Online (no custom Python) | `/aktiv-studio-module` |

### When finishing work
| Situation | Skill |
|---|---|
| Generating a commit message | `/aktiv-git-commit` |
| Releasing a task from dev to staging or production (git only, never copy folders) | `/aktiv-git-release` |
| Updating context files after development | `/aktiv-project-doc` |
| Writing up the day's work for a timesheet | `/aktiv-pms-timesheet` |

### When you need something from the client
| Situation | Skill |
|---|---|
| Drafting a message asking the client for information or a decision | `/aktiv-client-query` |

### When you forget
| Situation | Skill |
|---|---|
| Not sure which skill fits | `/aktiv-guide` |

---

## Typical workflow

```
New chat
  → /aktiv-project-start      load module context

Have a task
  → /aktiv-project-dev        describe your task — AI clarifies if needed, then builds

Done with task
  → /aktiv-project-doc        update context file
  → /aktiv-git-commit         generate commit message

End of day
  → /aktiv-pms-timesheet      write up the day's work
```

---

## When to use /aktiv-feature-flow vs /aktiv-project-dev

- `/aktiv-feature-flow` — you have an idea but want to map it functionally first, before any implementation
- `/aktiv-project-dev` — you know what to build, just start doing it

## When to use /aktiv-market-research vs /aktiv-feature-flow

- `/aktiv-market-research` — you're still exploring, haven't decided what to build yet
- `/aktiv-feature-flow` — decision is made, now map how it fits the product

## When to use /aktiv-project-scope-analysis vs /aktiv-project-user-story

- `/aktiv-project-scope-analysis` — client material came in; decide what the work is and what to ask them
- `/aktiv-project-user-story` — the work is agreed; write it up as a story document for sign-off

## When to use /aktiv-client-query

- Work is blocked on something only the client can answer, or an assumption had to be made and they should confirm it
- Collects the open questions from the session, drops anything we can answer ourselves, and drafts one message in the client's language

---

Display this and ask: "Anything you want more detail on?"
