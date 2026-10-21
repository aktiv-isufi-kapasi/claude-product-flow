Show all available skills and when to use each one.

## Output

Display the following reference guide exactly:

---

## Skills Reference

### When starting work
| Situation | Skill |
|---|---|
| Opening a new chat to work on a module | `/start` |
| Module has no folder structure yet | `/scaffold` |

### When doing a task
| Situation | Skill |
|---|---|
| Any development task — feature, bug, change | `/dev` |
| Exploring a feature idea before deciding | `/research` |
| Mapping how a decided feature fits the product | `/flow` |
| Moving a feature from one version to another | `/sync` |
| Core module updated, sub-module needs to catch up | `/compatible` |

### When finishing work
| Situation | Skill |
|---|---|
| Generating a commit message | `/commit` |
| Updating context files after development | `/doc` |
| Writing up the day's work for a timesheet | `/timesheet` |

### When you need something from the client
| Situation | Skill |
|---|---|
| Drafting a message asking the client for information or a decision | `/query` |

### When you forget
| Situation | Skill |
|---|---|
| Not sure which skill fits | `/guide` |

---

## Typical workflow

```
New chat
  → /start          load module context

Have a task
  → /dev            describe your task — AI clarifies if needed, then builds

Done with task
  → /doc            update context file
  → /commit         generate commit message
```

---

## When to use /flow vs /dev

- `/flow` — you have an idea but want to map it functionally first, before any implementation
- `/dev` — you know what to build, just start doing it

## When to use /research vs /flow

- `/research` — you're still exploring, haven't decided what to build yet
- `/flow` — decision is made, now map how it fits the product

## When to use /query

- Work is blocked on something only the client can answer, or an assumption had to be made and they should confirm it
- Collects the open questions from the session, drops anything we can answer ourselves, and drafts one message in the client's language

---

Display this and ask: "Anything you want more detail on?"
