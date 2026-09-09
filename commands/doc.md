Update the module context file after development is completed. Current state only — no changelogs, no history, no bug fix references. Only how the module works right now.

## Steps

1. Ask for the development directory:
   ```
   Development directory? (Press Enter for current: <cwd>)
   ```

2. Find the context file for this module:
   - Look for a single `.md` file matching the module name. Ignore `README.md`, `CHANGELOG.md`.
   - Always confirm before using:
     ```
     Found: `<filename>` — is this the right context file for this module?
     1. Yes
     2. No (provide correct path)
     3. Don't have one (create new)
     ```
   - Never assume a file belongs to this module. Each module has its own context file — do not mix content across modules.

3. Auto-detect the change range:

   Run `git log --oneline -1 -- <context_file>` to find the last commit that updated the context file.

   - **If a commit is found** — suggest it as the default range:
     ```
     Context file was last updated at:
     `<commit_hash>` — <commit_message>

     Show changes since that commit?
     1. Yes — use this as starting point
     2. No — I'll provide a different reference
     3. Describe changes manually
     ```
     - **1** — run `git diff <commit_hash>..HEAD -- <module_files>`
     - **2** — ask: "Provide commit ID or range:" then run `git diff <ref>..HEAD`
     - **3** — ask user to describe what changed; treat that as the source of truth

   - **If no commit found** (context file is new or untracked) — fall back to asking:
     ```
     What should I use to identify changes?
     1. git diff — uncommitted changes in working tree
     2. Commit reference — provide a commit ID or range
     3. I'll describe the changes manually
     ```

4. Read the current context file fully.

5. Identify which sections are affected by the changes. If a section mapping is unclear — ask the user, do not guess.

6. Present proposed changes before writing:
   ```
   I'll update these sections:
   - <section>: <what changes>
   - <section>: <what changes>

   Proceed?
   1. Yes
   2. No (adjust)
   ```

7. On confirmation, write only the updated sections.

8. Check if the context file has a `Core compatibility:` line:
   - **If found** — read the current core module version from its `__manifest__.py` and ask:
     ```
     Update core compatibility version?
     Core compatibility: <core_module> <old_version> → <current_version>
     1. Yes
     2. No
     ```
     Update the line on confirmation.
   - **If not found** — ask:
     ```
     Does this module depend on a core/base module?
     1. Yes — I'll add the compatibility marker
     2. No
     ```
     If yes: ask for the core module directory, read its version from `__manifest__.py`, and add the line:
     ```
     Core compatibility: <core_module_name> <version>
     ```

## Writing Rules

- **Current behavior only** — describe how the module works right now. Never write "previously", "changed from", "fixed", or "was broken".
- **No bug fix references** — a fix changes behavior; describe the resulting behavior, not the fix itself.
- **No assumptions** — if a file path, directory, or section mapping is unclear, ask the user before writing anything.
- **Module isolation** — each module has its own context file. Never write content about module A into module B's context file, even if they are related.
- **Functional + technical** — what it does and how at a high level. No line-by-line code detail.
- **Same style as existing file** — match tone, structure, depth. Do not add new sections unless genuinely needed.
- **No changelog, no version notes, no issue references.**
- **If already accurate, leave it untouched** — only update what actually changed.
