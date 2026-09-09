Check and resolve compatibility between a sub-module and its updated core/base module. Covers both functional and technical changes — overridden methods, removed methods, new conditions, new features. Goal: both modules work correctly together after this session.

## Steps

1. Ask for the sub-module directory:
   ```
   Sub-module directory? (the module that extends/depends on core)
   ```

2. Ask for the core module directory:
   ```
   Core module directory? (the base module that was updated)
   ```

3. Find and confirm context files for both:
   ```
   Found: `<filename>` — is this the right context file for sub-module / core?
   1. Yes
   2. No (provide path)
   3. Don't have one
   ```
   Read both context files. Do not read full module code yet.

4. Auto-detect the compatibility range:

   a. Look for a `Core compatibility:` line in the sub-module context file:
      ```
      Core compatibility: <core_module_name> <version>
      ```

   b. Read the current core module version from its `__manifest__.py`.

   c. **If the marker is found** — present it to the user:
      ```
      Sub-module was last made compatible with: <core_module_name> <last_version>
      Core module is now at: <current_version>

      Check changes between these two versions?
      1. Yes
      2. No — provide a different reference
      3. I'll describe changes manually
      ```
      - **1** — use version range to identify changes. Run `git log` on core directory filtered between the two versions, or `git diff <tag/commit>..HEAD` if refs are available.
      - **2** — ask: "Provide commit ID or range:"
      - **3** — treat user's description as source of truth

   d. **If no marker found** — ask:
      ```
      No compatibility marker found in sub-module context.
      What should I use to identify core changes?
      1. Commit reference — I'll provide it
      2. I'll describe what changed manually
      ```

5. Analyse core changes across two dimensions:

   **Technical:**
   - Methods that sub-module overrides (`super()` calls) — did core change or remove them?
   - New parameters or return value changes on overridden methods
   - New conditions or logic added inside methods the sub-module extends
   - Models or fields the sub-module inherits — were they modified or removed?

   **Functional:**
   - New features added to core — does sub-module need to be aware or extend them?
   - Behavior changes in existing flows that sub-module participates in
   - New compatibility rules, constraints, or guards introduced

6. For each change found, determine impact on the sub-module:
   - **Breaking** — sub-module will fail or behave incorrectly without a fix
   - **Risk** — may cause issues depending on usage, needs review
   - **Informational** — core added something new, sub-module may want to extend it

7. If impact of any change is logically unclear or functionally ambiguous — ask the user before assuming:
   ```
   Core changed <method/behavior>. I'm not sure how this affects your sub-module's <override/usage>.
   Can you clarify: <specific question>?
   ```
   Never guess on breaking changes — always confirm.

8. Present the compatibility report:
   ```
   Compatibility Report
   ──────────────────
   Breaking:
   - <change>: <impact> → <what needs to be done>

   Risk:
   - <change>: <impact> → <what to review>

   Informational:
   - <change>: <what core added>
   ```
   Then ask:
   ```
   How do you want to proceed?
   1. Fix breaking issues now
   2. Review all and decide per item
   3. Just the report for now
   ```

9. For each fix — read the relevant files in both modules before writing anything. Propose the fix, confirm, then apply.

10. After all fixes are done — update the `Core compatibility:` marker in the sub-module context file to the current core version:
    ```
    Core compatibility: <core_module_name> <new_version>
    ```
    Confirm with user before writing:
    ```
    Update compatibility marker to <core_module_name> <new_version>?
    1. Yes
    2. No
    ```

## Context File Marker Format

Add this line to the sub-module's context `.md` file to enable auto-detection:

```
Core compatibility: ak_odoo_cpq 18.0.5.18.11
```

This is updated automatically by `/compatible` after each successful compatibility session.

## Rules

- Read context files first — only read actual code files when a specific change needs deeper investigation
- Never assume impact of a core change on the sub-module — ask if uncertain
- Fix breaking issues before informational ones
- After all fixes, verify both modules are logically consistent — no orphaned super() calls, no missing method references
- If a fix touches more than 3 files — list them and confirm with user before proceeding
- Always update the compatibility marker after fixes — this is what makes auto-detection work next time
