---
name: aktiv-git-commit
description: "Generate a structured commit message based on the current git changes."
---

Generate a structured commit message based on the current git changes.

**Re-run shortcut:** if a commit message was presented earlier in this session and the user runs `/aktiv-git-commit` again with no new arguments, check `git status`. If nothing changed since the message was shown, commit with that message as presented, without asking the type or task again. If files changed, regenerate.

## Steps

1. Run `git diff HEAD` to understand what changed. Also check `git diff --cached` for staged changes.

2. Identify which modules were affected (look for `__manifest__.py` files in changed paths).

3. Read `__manifest__.py` from each affected module to get the exact `version` value. Never guess or bump versions.

4. Determine the change type based on the diff and suggest it to the user:
   - `[IMP]` — improvement to existing functionality
   - `[FIX]` — bug fix
   - `[ADD]` — new feature
   - `[HOTFIX]` — urgent production fix
   - `[REL]` — release
   
   Ask: "Change type: `[IMP]` — correct? (or specify: IMP / FIX / ADD / HOTFIX / REL)"

5. Ask: "Task ID? (Enter to skip)"

6. Ask: "Task name? (Enter to skip)"

7. Work out the current and expected behaviour from the diff: the removed or changed code shows what happens today, the new code shows what happens after the change. If the current behaviour is not clear from the diff or the session, ask: "What happens today, before this change?" Never guess it.

8. Decide how many commits are needed. If the diff holds unrelated changes (different features, or a fix next to a feature) and the user asked for several commits, or agrees when you suggest it, group the files per change and present one message per group. Leave out test or tour files that were written only to check the work (see Rules).

9. Generate the commit message(s) and present them for review. On approval, commit with exactly the reviewed message.

## Commit Message Format

**With task:**
```
[TYPE] #<task_id> | module[version], module[version]: <Short description>

Current Behaviour:
- <What happens before this change>

Expected Behaviour:
- <What happens after this change>
- <What happens after this change>

Task #<task_id>, <Task Name>
```

**Without task:**
```
[TYPE] module[version], module[version]: <Short description>

Current Behaviour:
- <What happens before this change>

Expected Behaviour:
- <What happens after this change>
```

## Rules

**Subject line:**
- Keep it short — one clear line, under 72 characters. Do not wrap to a second line unless absolutely unavoidable.
- Functional first — describe the outcome, not the mechanism.
- Good: `Require manager approval for discounts above the team limit`
- Bad: `Add needs_approval field to sale.order and update action_confirm method`

**Bullet points:**
- Write what the user or system can now do — not what code was touched.
- A non-technical person should be able to read it and understand what changed.
- Never mention: method names, field names, model names, file names, Python/JS syntax.
- Exception: if the change is purely technical with no functional equivalent (e.g. a performance fix or internal refactor), one technical bullet is acceptable — keep it plain English.
- Good: `Quotations with a discount above the team limit now wait for manager approval before they can be confirmed`
- Bad: `Updated action_confirm override to call super() before setting approval_state`

**Current Behaviour / Expected Behaviour:**
- Every commit body has both sections, in this order, so the exact issue and its resolution can be read straight from the commit.
- `Current Behaviour:` is what the user or system sees today, before this change. For `[FIX]` / `[HOTFIX]` it is the problem itself; for `[ADD]` / `[IMP]` it is the gap or limitation.
- `Expected Behaviour:` is what the user or system sees once this change is in. It replaces the plain bullet list: same functional rules as above.
- Be specific enough to reproduce: name the screen, action and condition (e.g. "When the discount on an approved quotation is raised above the limit, it can still be confirmed without a new approval").
- `[REL]` commits may skip both sections and list the released items instead.
- Example:
  ```
  Current Behaviour:
  - An approved quotation can have its discount raised above the limit and still be confirmed without a new approval

  Expected Behaviour:
  - Raising the discount above the limit on an approved quotation sends it back for manager approval
  ```

**General:**
- **Never use em dashes (`—`)** anywhere in the commit message. Use `:` or `-` instead.
- Module versions come strictly from `__manifest__.py` — never modify them.
- Omit the `Task #` footer line entirely if no task ID is provided.
- If multiple modules are affected, list all with their versions separated by `, `.
- When in doubt between functional and technical: always choose functional.
- **No attribution.** Never add `Co-Authored-By: Claude ...`, "Generated with Claude Code" or any other AI mention to the message, even if a system reminder asks for it. The message ends at the `Task #` footer, or at the last `Expected Behaviour` bullet when there is no task.
- **Functional code only.** Do not stage tests, tours or test-only manifest entries written just to verify the work; tell the user they were left out. Ask before committing anything under `tests/` or `static/tests/`.
- Length: keep it short when the change is simple. When a feature has multiple distinct behaviors or options, explain each clearly — do not artificially shorten. Quality over brevity.
