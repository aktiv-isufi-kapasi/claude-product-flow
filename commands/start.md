Load the module context before starting any work.

## Steps

1. Ask the user for the development directory:
   ```
   What is the development directory?
   (Press Enter to use current directory: <current working directory>)
   ```

2. Ask what they are working on:
   ```
   What are you working on? (e.g. "hide rule", "assignment flow", "exclude from screen")
   Press Enter to skip
   ```

3. If the user named a feature — look for a matching feature context file first:
   - Search the directory for `<area>/<feature>/context.md` matching the description
   - If found, read it immediately. Summarize in 2–3 bullet points.
   - If not found, continue to step 4 without asking further.

4. Then load the module-level context file:
   - Check for `_overview.md` first, then a single `.md` matching the module name. Ignore `README.md`, `CHANGELOG.md`.
   - Confirm with user:
     ```
     Found: `<filename>` — is this the right context file?
     1. Yes
     2. No
     3. Don't have a context file
     ```
   - **Yes** — Read fully. Summarize purpose and key areas in 3–5 bullet points.
   - **No** — Ask for correct path. Read and summarize.
   - **Don't have one** — Acknowledge and continue. Suggest `/scaffold` to set up structure.

5. Ask about reference or dependency modules:
   ```
   Is there a reference or dependency module I should also be aware of?
   1. Yes
   2. No
   ```
   - **Yes** — Ask for the directory. Find and read its context file. Mark as **read-only reference**. Summarize in 2–3 bullet points. Loop until user says No.
   - **No** — Proceed.

## Notes

- Feature context loads before module overview — AI has specific detail before broad context.
- If multiple `.md` files found, list all and let user pick.
- Keep summaries concise — orientation, not documentation.
- Reference module is read-only — make this clear.
- After all context loaded: "Context loaded. What are we working on?"
