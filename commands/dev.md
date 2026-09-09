Single entry point for any development task. Accepts any input — detailed or thin — and ensures all required information is captured before work begins. Validates both functional and technical completeness. Reduces back-and-forth by asking only what is missing, in one shot.

## Steps

1. Receive the user's input — feature idea, bug description, change request, anything.

2. Identify the task type:
   - **Feature** — adding or changing functionality
   - **Bug** — something broken or behaving incorrectly
   - **Research** — exploring options before deciding
   - **Sync** — moving a feature between versions

3. Check for critical gaps — both functional and technical — based on task type:

   **Feature gaps to check:**

   Functional:
   - What triggers it? (user action, condition, automatic?)
   - What is the expected behavior / outcome?
   - Any edge cases or optional flows?

   Technical:
   - Which model or module is affected?
   - Any specific method, view, or field to modify?
   - Any dependency on another module or external data?

   **Bug gaps to check:**

   Functional:
   - What was expected to happen?
   - What is actually happening?
   - Where in the flow does it break? (screen, action, condition)

   Technical:
   - Is there an error message or traceback?
   - Which model or method is involved?
   - Did it ever work before, or is this new behavior?

   **Research gaps to check:**

   Functional:
   - What decision will this research inform?

   Technical:
   - Any technical constraints to factor in? (version, module, performance)

   **Sync gaps to check:**

   Functional:
   - What does the feature do? (brief description)

   Technical:
   - Source version and target version?
   - Are there known structural differences between versions in this area?

4. Cross-check what is already known from the loaded context — do not ask for anything already covered there.
   If new folder structure is in use: check `_overview.md` for module-level facts and `<area>/<feature>/context.md` for feature-level facts before asking.

5. If critical information is missing — ask only the missing pieces, maximum 3 questions, in one message, one line each. Prioritize the most blocking gaps first.

6. If nothing is missing — proceed directly without asking anything.

7. Once input is complete, execute based on task type:
   - **Feature** → map functional flow first (what user sees and does), then implement technically
   - **Bug** → diagnose root cause from both functional and technical angle, propose fix
   - **Research** → search live, never answer from training data, present findings
   - **Sync** → read source version behavior and technical implementation, map to target version, implement

## Rules

- Always validate both functional AND technical completeness before starting
- Never assume a gap and proceed silently — ask if something critical is missing
- Never ask more than 3 questions at once — prioritize the most critical gaps
- Never ask for what is already in the loaded context file
- If the user gave enough detail on both sides, skip questions entirely and go straight to work
- Keep questions short — one line each, no explanation needed
- The goal is faster execution, not interrogation
