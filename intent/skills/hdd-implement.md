# HDD implement skill

This skill implements changes to the software based on a diff of intent.

It can be applied any time there is an intent to diff, iteratively for small changes or as a long-running task for larger ones.

Before starting, ensure there is an intent diff to work from.
If it isn't committed yet, offer to commit it for the user and use that.

Be flexible on process but firm on human-authorship of intent.

Ensure the `<change-slug>` has been chosen, choose it if not.

Create the `<change-dir>` and `<worktree>` if not already done.

## P1. Plan

Plan the changes. 