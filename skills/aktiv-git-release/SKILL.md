---
name: aktiv-git-release
description: "Release one task or user story from a dev branch to a target branch (staging or production) through git only: picks exactly the commits for that task, builds a release branch, merges it (staging: plain merge; production: rebase onto latest production first), and verifies no file was missed. Never copies folders, never pushes."
---

Release one task or user story from a source branch (usually dev) to a target branch through git, so nothing is copied by hand and no file is left behind. Only the commits for the given task or user story are released.

## Steps

1. Ask for the repository and check it is safe to start:
   ```
   Repository directory? (Press Enter for current: <cwd>)
   ```
   Run `git status --porcelain`. If anything is uncommitted, stop:
   ```
   There are uncommitted changes. Commit or stash them first, then run the release again.
   ```
   Never stash, reset or discard on the user's behalf. Note the current branch so you can return to it at the end or on abort.

2. Ask the release details in one message:
   ```
   Source branch? (Enter for dev)
   Target branch? (e.g. staging, production)
   Task ID(s) or user story number(s)? (e.g. 4521, or US-05; comma separated for several)
   ```
   Then confirm the release type from the target name:
   ```
   Releasing to `<target>` as:
   1. Staging: merge only, no rebase
   2. Production: rebase onto latest production, then merge
   ```

3. Fetch and check both branches:
   - `git fetch origin`
   - Target: work from `origin/<target>`. If a local `<target>` has commits that are not on `origin/<target>`, stop and show them; someone has unpushed work on the target.
   - Source: use the local `<source>`. If it is behind `origin/<source>`, say so and ask whether to update it first (`git merge --ff-only origin/<source>`). If it is ahead, warn that unpushed commits are being released.

4. Find the commits for the task. Commits follow the `/aktiv-git-commit` format, so the task ID is in the subject (`#4521`) and the footer (`Task #4521, ...`):
   ```
   git log --reverse --no-merges -E -i --format='%h %ad %an %s' --date=short \
     --grep='#<id>([^0-9]|$)' --grep='US-?0*<n>([^0-9]|$)' origin/<target>..<source>
   ```
   - Run `git cherry -v origin/<target> <source>` and drop commits marked `-`: their change is already on the target (e.g. released earlier). List them as "already released".
   - If nothing matches, stop and say so. Do not guess commits from dates or authors.
   - If a matched commit also mentions another task ID, flag it.

5. Check for dependencies. This is the step that catches missed files:
   - Collect every file the task commits touch: `git show --name-status --format= <hash>` for each.
   - Find commits on the source branch that are **not** part of the task but touch the same files: `git log --no-merges --format='%h %s' origin/<target>..<source> -- <files>` minus the task commits.
   - Those commits change the same files, so the task may depend on them. Releasing without them means those files on the target will not match dev.

6. Present the release plan and wait for confirmation:
   ```
   Release #4521 → production (from dev)

   Commits (oldest first):
   - a1b2c3d 2026-10-20 Dev Name  [FIX] #4521 | ak_odoo_cpq_custom[18.0.1.4.2]: Remove hidden components from the BoM
   - d4e5f6a 2026-10-21 Dev Name  [FIX] #4521 | ak_odoo_cpq_custom[18.0.1.4.2]: Keep optional components visible

   Files (5):
   M ak_odoo_cpq_custom/models/sale_order.py
   M ak_odoo_cpq_custom/views/cpq_views.xml
   A ak_odoo_cpq_custom/data/hide_rule_data.xml
   M ak_odoo_cpq_custom/__manifest__.py
   M ak_odoo_cpq_custom/security/ir.model.access.csv

   Already released: (none)
   Other dev commits touching these files (not included):
   - 9f8e7d6 [IMP] #4498 | ...: Rule priorities  → touches models/sale_order.py

   1. Release these commits
   2. Also include the other commits listed above
   3. Adjust (add or remove commits by hash)
   4. Stop
   ```

7. Build the release branch from the up-to-date target:
   ```
   git checkout -b release/<target>-<id> origin/<target>
   git cherry-pick -x <hashes, oldest first>
   ```
   `-x` records the original dev commit in each message, so every released change can be traced back. If the branch name exists, ask before reusing or renaming it.

   **On a conflict:** stop. Show the conflicted files and both sides. Do not resolve it by guessing:
   ```
   Conflict in <file> while applying <hash> <subject>.
   This usually means the task depends on a change that is not being released.
   1. Resolve it together (I show both sides, you decide)
   2. Abort the release
   ```
   On abort: `git cherry-pick --abort`, return to the original branch, delete the release branch, and report what blocked it.

8. **Production only:** rebase the release branch onto the latest production, in case production moved while you were preparing:
   ```
   git fetch origin
   git rebase origin/<target>
   ```
   Same conflict handling as step 7. Rebase only the release branch, never the target or any shared branch.

   **Staging:** no rebase. Go straight to verification.

9. Verify before merging. Show the result of each check:
   - **Nothing missed:** `git diff <source> release/<target>-<id> -- <task files>`. Empty means every task file matches dev exactly. If a file differs, explain each difference: either it comes from a dev commit that was deliberately left out in step 6, or it is unexplained. Unexplained → stop.
   - **Nothing extra:** `git diff --name-only origin/<target> release/<target>-<id>` lists only task files.
   - **Versions:** for each module touched, show the `version` in `__manifest__.py` on the target now and after the release. If dev has a higher version that came from a commit not being released, say so.
   - **Files load:** `python3 -m py_compile` on changed `.py` files, and `xmllint --noout` on changed `.xml` files if xmllint is installed.

10. Merge into the target:
    ```
    git checkout <target>                 # create from origin/<target> if it does not exist locally
    git merge --ff-only origin/<target>   # bring local target level with remote; stop if this fails
    git merge --no-ff release/<target>-<id> -F <message file>
    ```
    Merge message, in the `/aktiv-git-commit` `[REL]` format:
    ```
    [REL] #<id> | module[version]: Release <short task description> to <target>

    Released:
    - <subject of each released commit>

    Task #<id>, <Task Name>
    ```
    Ask for the task name if it is not in the commit footers. Omit the footer when there is no task ID (user story only).

11. Final check and hand-over:
    - Repeat the "nothing missed" diff, this time against `<target>`.
    - Show `git log --oneline origin/<target>..<target>`.
    - Do **not** push. End with:
    ```
    Release ready on local `<target>` (not pushed).
    Review, then push yourself:
      git push origin <target>
    After pushing, the release branch can be deleted:
      git branch -d release/<target>-<id>
    ```
    Return to the branch the user started on.

## Rules

- **Git only.** Never copy files or folders between branches, checkouts or servers, and never use `git checkout <branch> -- <path>` to bring code across. Every released change comes through a commit.
- **Only the task.** Release only the commits found for the given task or user story numbers, plus any the user explicitly adds in step 6.
- **Staging merges, production rebases first.** Staging: release branch merged as is. Production: release branch rebased onto the latest `origin/<target>`, then merged. In both cases the merge is `--no-ff`, so the release shows as one merge in the history.
- **Never push.** Never force anything. Never `reset --hard`, rebase or amend the target branch or any shared branch.
- **Stop on doubt.** Uncommitted changes, unpushed target commits, an empty match, a conflict, or an unexplained difference in verification each stop the release with a clear reason. Never resolve conflicts silently.
- **Leave things clean.** On abort or finish, return to the original branch, with no half-finished cherry-pick, rebase or merge left behind.
- **Never use em dashes** in the merge message. Use `:` or `-`.
