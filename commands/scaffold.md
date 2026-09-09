Set up the folder structure for a module — creates feature-level directories with context, interface, and test files. Designed for QA-first usage: each feature gets its own context and test file so sessions stay focused and token usage stays low.

## Steps

1. Ask for the module directory:
   ```
   Module directory path?
   (Press Enter to use current directory: <current working directory>)
   ```

2. Ask for the module name and version:
   ```
   Module name and version? (e.g. ak_odoo_cpq_custom v19)
   ```

3. Ask if this module depends on another:
   ```
   Does this module inherit from or depend on another module?
   1. Yes — it overrides/extends a base module
   2. No — standalone
   ```
   If Yes: ask for the base module name. Note it — base module gets only an `interface.md`, not a full structure.

4. Ask for the features to scaffold:
   ```
   List the features to scaffold (comma separated).
   Group them by area. Example:
     rules: hide, block, assignment, warning
     configurator: product_visibility, exclude_from_screen
     pricing: formula
   ```
   If the user is unsure, suggest based on module name if recognizable, otherwise ask them to list what they know and scaffold the rest later.

5. Confirm the structure before creating:
   ```
   Will create:
   <module_dir>/
     _overview.md
     <area>/
       <feature>/
         context.md
         interface.md
         tests.md
     ...

   Proceed?
   1. Yes
   2. Adjust
   ```

6. Create the folder structure with template files:

   **`_overview.md`**
   ```
   # <Module Name> — <Version>
   
   ## Purpose
   (what this module does)
   
   ## Depends on
   (base module name, if any)
   
   ## Features
   (list of areas and features — links to feature folders)
   ```

   **`<feature>/context.md`**
   ```
   # <Feature Name>
   
   ## What it does
   
   ## Trigger
   (what starts this — user action, condition, automatic)
   
   ## Models / Methods
   
   ## Overrides from base
   (if this module overrides base behavior — what and why)
   
   ## Edge cases
   ```

   **`<feature>/interface.md`**
   ```
   # <Feature Name> — Interface
   
   ## Inputs
   
   ## Outputs
   
   ## Contracts
   (what this feature guarantees to other features that depend on it)
   ```

   **`<feature>/tests.md`**
   ```
   # <Feature Name> — Test Scenarios
   
   ## Happy path
   | Scenario | Input | Expected output |
   |---|---|---|
   
   ## Edge cases
   | Scenario | Input | Expected output |
   |---|---|---|
   
   ## Regression triggers
   (what changes elsewhere could break this feature)
   ```

7. If module has a base dependency — create `<base_module_name>/interface.md` at the same level:
   ```
   # <Base Module> — Interface Reference
   
   ## Key methods exposed
   
   ## What super() returns
   
   ## Known behaviors to be aware of
   ```

8. Confirm completion:
   ```
   Structure created at <module_dir>/
   
   Next steps:
   1. Fill _overview.md with module purpose
   2. Fill context.md for each feature you are actively working on
   3. Run /doc after each development session to keep context current
   4. Fill tests.md per feature before QA begins
   ```

## Rules

- Create files with template headers only — never fill in content, that is the developer's job
- If a feature area is unclear, scaffold it anyway — empty structure is better than missing structure
- Base module gets only `interface.md` — never a full folder structure (it is read-only)
- One feature = one folder, always — never combine two features into one folder
- Keep template headers minimal — the developer fills in detail, not the scaffold
