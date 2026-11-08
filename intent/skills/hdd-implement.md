# HDD implement skill

This skill implements changes to the software based on a diff of intent.

It can be applied any time there is an intent to diff, iteratively for small changes or as a long-running task for larger ones.

Before starting, determine what intent diff you're being asked to implement.
Common cases:

1. PR base branch. In this case, everything should be committed and pushed.
2. Bare feature branch. In this case, offer to create the PR. Assume `main` as the base unless there is a reason to use something else (like `dev` on some repos).
3. Uncommitted changes. In this case, offer to commit changes, create the branch, and the PR.

Be flexible on process but firm on human-authorship of intent.

Ensure the `<change-slug>` has been chosen, choose it if not.

Create the `<change-dir>` and `<change-worktree>` if not already done.

## P1. Plan

Plan the changes.
