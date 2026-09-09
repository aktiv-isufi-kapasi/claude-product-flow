Sync a feature from one version of a module to another. This is feature-based sync, not code migration — the same functionality may need to be implemented differently depending on each version's architecture.

## Steps

1. Ask for the **source directory** (version where the feature was built):
   ```
   Source directory (where the feature exists)?
   ```

2. Ask for the **target directory** (version where it needs to be implemented):
   ```
   Target directory (where to sync the feature)?
   ```

3. Ask for the **feature reference**:
   ```
   Feature reference? (commit ID, commit message, or plain description — any works)
   ```

4. Look for context in each directory — check for `_overview.md` first (new structure), then a single `.md` matching the module name (old structure). Confirm with user for each:
   ```
   Found: `<filename>` — is this the right context file for source/target?
   1. Yes
   2. No (provide path)
   3. Don't have a context file
   ```
   If new structure: also ask if a specific feature context should be loaded (`<area>/<feature>/context.md`) for the feature being synced.
   Read context files only — do not read the full module code at this stage.

5. Understand the feature from the reference provided:
   - If commit ID: use it to understand what changed and why
   - If description: ask 1–2 focused clarifying questions only if the intent is unclear
   - Goal: understand **what the feature does functionally**, not how it was coded

6. Based on both context files, plan how to implement the same feature in the target version:
   - Respect the target version's own flow and architecture
   - Only read specific code files if a concrete difference between versions needs to be resolved — do not read files speculatively
   - If something is unclear, ask the user rather than reading more code

7. Present the implementation plan and ask for confirmation before writing any code.

## Rules

- **Feature-first, not code-first** — understand intent from the source, implement correctly in the target
- **Context file only** — do not load the full module unless a specific file is needed to resolve a difference
- **Accept any reference format** — commit hash, commit message, or plain-English description all work
- **Ask rather than read** — if uncertain about a version difference, ask the user instead of reading more files
