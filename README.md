# claude-product-flow

Claude Code skills for product development teams. Shared across the team — new skills pushed here are available to everyone after a `git pull`.

## Install

```bash
git clone https://github.com/aktiv-isufi-kapasi/claude-product-flow ~/.claude/claude-product-flow
cd ~/.claude/claude-product-flow && ./install.sh
```

Restart Claude Code. Commands are now available.

## Update

```bash
cd ~/.claude/claude-product-flow && git pull
```

New skills are automatically installed via a post-merge hook — no extra steps needed.

---

## Typical Workflow

```
New chat
  -> /start         load module context

Have a task
  -> /dev           describe your task — AI clarifies if needed, then builds

Done with task
  -> /doc           update context file
  -> /commit        generate commit message
```

---

## Skills

### Starting Work

| Skill | When to use |
|---|---|
| `/start` | Opening a new chat to work on a module |
| `/guide` | Forgot which skill to use — shows full reference |

### Doing a Task

| Skill | When to use |
|---|---|
| `/dev` | Any development task — feature, bug, change |
| `/research` | Exploring a feature idea before deciding — searches live, never from memory |
| `/flow` | Decision is made — map how the feature fits the product flow |
| `/sync` | Moving a feature from one version to another (e.g. v18 -> v19) |
| `/compatible` | Check and fix sub-module compatibility after core module is updated |

### Finishing Work

| Skill | When to use |
|---|---|
| `/doc` | Update module context file after development is done |
| `/commit` | Generate a structured, functional commit message from current changes |

---

## When to use which skill

**`/research` vs `/flow` vs `/dev`**
- Still exploring, haven't decided yet: `/research`
- Feature decided, map how it fits the product: `/flow`
- Know what to build, just do it: `/dev`

**`/sync` vs `/compatible`**
- Moving a feature to another version: `/sync`
- Core module updated, sub-module needs to catch up: `/compatible`

---

## Context File

Each module has a single `.md` context file describing its current state — flow, models, behavior. Written functionally and technically, no history, no changelogs.

For sub-modules that depend on a core module, add this line to the context file:

```
Core compatibility: ak_odoo_cpq 18.0.5.18.11
```

`/compatible` reads this automatically to detect what changed in core since last sync.
`/doc` updates this marker after each development session.

---

## How It Works

Skills are markdown files in `commands/`. Install symlinks them into `~/.claude/commands/` so Claude Code picks them up. A `git pull` is all that's needed to update — the post-merge hook handles the rest.

## Adding a New Skill

1. Create `commands/<skill-name>.md`
2. Write the instructions for Claude
3. Push to GitHub
4. Team runs `git pull` to get it
