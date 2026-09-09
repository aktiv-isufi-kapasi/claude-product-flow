Map a decided feature into the existing product flow — functionally only. No technical implementation details. The goal is a clear functional picture of where the feature fits and how it changes the user experience.

## Steps

1. Ask for the development directory:
   ```
   What is the development directory?
   (Press Enter to use current directory: <current working directory>)
   ```

2. Find the product context file — check for `_overview.md` first (new structure), then look for a single `.md` matching the module name (old structure). Confirm with user:
   ```
   Found: `<filename>` — is this the right context file?
   1. Yes
   2. No (provide path)
   3. Don't have a context file
   ```

3. Ask: "What is the feature we are mapping?"
   If the user already mentioned it, confirm: "Are we mapping: `<feature>`?"

4. Read and understand the existing product flow from the context file — key screens, user journey steps, entry and exit points.

5. Map the feature into the flow:
   - **Where does it fit?** — At which point in the existing user journey does this feature appear?
   - **What triggers it?** — What action or condition brings the user to this feature?
   - **What does the user do?** — Step-by-step functional flow from the user's perspective.
   - **What changes in existing flow?** — Does any current screen, step, or journey need to change to accommodate this?
   - **What is the outcome?** — What has changed for the user after interacting with this feature?

6. Present the functional flow clearly — use a simple numbered user journey or flow description. No code, no model names, no technical terms.

## Rules

- **Functional only** — describe what the user sees and does, not how it is built.
- If the feature touches an unclear area, ask the user rather than assuming.
- Keep it grounded in the actual product — reference real screens and flows from the context file, not generic patterns.
- Once the functional flow is agreed, the implementation is handled separately by Claude Code.
