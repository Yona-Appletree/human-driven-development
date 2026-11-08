# HDD skills

The skills defined in this directory implement the human-driven-development process.

Concepts shared acoss the skills are defined here.

## Change slug and id

The `<change-slug>` is a short `kebab-cased` identifier for a change.
Examples: `add-profile-page`, `rework-navbar`, `fix-loading-animation`, `redact-secrets`

The `<change-id>` is the current local timestamp plus the slug: `YYYY-MM-DD-hhmm-<change-slug>`
Example: `2026-11-07-0030-intent-skills`

## Change directory

The `<change-dir>` is a directory that holds ephermeral content related to that change.

The standard location is: `<repo>/.changes/<change-id>`

It is gitignored.

It is managed by agents.

## Change worktrees

Worktrees are where the work on a change happens.

The standard location is: `<repo>/.worktrees/<change-id>`

Agent harnesses and IDEs sometimes supply the worktrees.
If provided, use it, but symlink it to `<repo>/.worktrees/<change-id>` for consistency and easy lookup.