Generate a structured commit message based on the current git changes.

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

7. Generate the commit message and present it for review.

## Commit Message Format

**With task:**
```
[TYPE] #<task_id> | module[version], module[version]: <Short description>

- <Functional bullet point>
- <Functional bullet point>

Task #<task_id>, <Task Name>
```

**Without task:**
```
[TYPE] module[version], module[version]: <Short description>

- <Functional bullet point>
- <Functional bullet point>
```

## Rules

**Subject line:**
- Keep it short — one clear line, under 72 characters. Do not wrap to a second line unless absolutely unavoidable.
- Functional first — describe the outcome, not the mechanism.
- Good: `Allow optional components to be driven by compatibility rules`
- Bad: `Add is_optional field to cpq.component.configuration and update apply_component_rules method`

**Bullet points:**
- Write what the user or system can now do — not what code was touched.
- A non-technical person should be able to read it and understand what changed.
- Never mention: method names, field names, model names, file names, Python/JS syntax.
- Exception: if the change is purely technical with no functional equivalent (e.g. a performance fix or internal refactor), one technical bullet is acceptable — keep it plain English.
- Good: `Components hidden from the CPQ screen are now also removed from the BoM when a rule hides them`
- Bad: `Updated action_done override to call super() before setting exclude_from_cpq_screen`

**General:**
- **Never use em dashes (`—`)** anywhere in the commit message. Use `:` or `-` instead.
- Module versions come strictly from `__manifest__.py` — never modify them.
- Omit the `Task #` footer line entirely if no task ID is provided.
- If multiple modules are affected, list all with their versions separated by `, `.
- When in doubt between functional and technical: always choose functional.
- Length: keep it short when the change is simple. When a feature has multiple distinct behaviors or options, explain each clearly — do not artificially shorten. Quality over brevity.
