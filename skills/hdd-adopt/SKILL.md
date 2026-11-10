---
name: hdd-adopt
description: Set up a new or existing repository for human-driven development (HDD) — rename AI-authored markdown to `.ai.md` with reference updates, install the HDD agent instructions and skills, scaffold `_intent/`, and guide the user to write their first top-level intent statement. Use when the user wants to adopt HDD or https://github.com/Yona-Appletree/human-driven-development in a repository.
---

# HDD adopt

Set up a repository, new or existing, for human-driven development.

The HDD source repository is <https://github.com/Yona-Appletree/human-driven-development>. Call a local copy of it `<hdd-repo>`: use one the user already has, or clone it to a temporary directory. `<repo>` is the root of the repository being set up.

Work on a change like any other HDD change: branch `change/adopt-hdd`, in a worktree if the harness supports it, with a `<change-dir>` of `<repo>/.changes/YYYY-MM-DD-hhmm-adopt-hdd` (local time) for working files. Tell the user what you're about to do before each step that changes files.

## 1. AI file migration

In HDD, agent-written markdown is named `.ai.md`, so humans can tell it apart from their own writing. The first step is to identify AI-authored markdown and rename it.

### Identify

List the candidates:

```bash
python3 <hdd-repo>/skills/hdd-adopt/scripts/migrate_ai_md.py list > <change-dir>/ai-md.txt
```

The script excludes files that must keep their names: `SKILL.md` files, `.github/` templates, licenses and notices, vendored and third-party code, existing `.ai.md` and `.gen.md` files, and `_intent/`. Add more with `--exclude GLOB`.

Assume the candidates are AI-authored unless the user says otherwise. Show the user a summary (counts by directory, plus every root-level file) and ask which, if any, they wrote themselves. Remove those from the list.

### Rename

Preview, then apply:

```bash
python3 <hdd-repo>/skills/hdd-adopt/scripts/migrate_ai_md.py apply <change-dir>/ai-md.txt --dry-run
python3 <hdd-repo>/skills/hdd-adopt/scripts/migrate_ai_md.py apply <change-dir>/ai-md.txt
```

The script renames each file with `git mv` and updates references to it in every tracked text file: markdown links, paths in code and config, and bare file names when they're unambiguous. It reports bare names it couldn't resolve; check those by hand.

This may be a very large diff. That's OK.

### Key files

Key markdown like `README.md` and `AGENTS.md` is rewritten by the user by hand. Until then, stubs point to the renamed AI versions:

- **`README.md`:** if it was renamed, create a new `README.md` with exactly:

  ```md
  See [README.ai.md](./README.ai.md) for information about this project until a person rewrites the readme.
  ```

- **`AGENTS.md`:** if it was renamed, copy `<hdd-repo>/AGENTS.md` into `<repo>/AGENTS.md`. It tells agents to follow `AGENTS.ai.md` until the user rewrites it.
- **Other agent instruction files** (`CLAUDE.md`, `.cursorrules`, …): ask the user how to handle them. A `CLAUDE.md` can be a stub that points to `AGENTS.md`.

### Verify and commit

Run the repository's build, tests and checks: references in code changed. Fix anything the rename broke, then commit the migration on its own.

## 2. Intent scaffolding

1. Create the `<repo>/_intent/` directory with a `.gitignore` in it, copied from `<hdd-repo>/_intent/.gitignore` (it ignores `*.ai.md` and `*.gen.md`). Make sure the root `.gitignore` ignores `.changes` and `.worktrees`; the HDD skills rely on these.
2. Create `<repo>/_intent/_intent.md` with exactly:

   ```md
   # Intent

   This directory describes what the software does, following [human-driven-development](https://github.com/Yona-Appletree/human-driven-development).
   ```

3. Copy the HDD skill intent from `<hdd-repo>/_intent/skills/` (`_skills.md`, `hdd-change.md`, `hdd-implement.md`, `hdd-backfill.md`) into `<repo>/_intent/skills/`.
4. Offer to copy the hygiene intent (`<hdd-repo>/_intent/hygiene.md`: markdown formatting, spell checking, editor configs) as well. Let the user decide.
5. Commit the copied intent as an intent commit (no co-authorship trailer: it's the HDD authors' intent, copied, not written by you).
6. Implement the initial intent (the skills, and hygiene if chosen) with the `hdd-implement` skill. The repository doesn't have it yet, so follow `<hdd-repo>/skills/hdd-implement/SKILL.md`. `<hdd-repo>/skills/` holds builds of the same skill intent, including their `scripts/`; use them as the reference builds. The skills go in `<repo>/skills/<name>/`, symlinked into `<repo>/.claude/skills/` and `<repo>/.agents/skills/`.

## 3. The first intent statement

Guide the user to write a high-level intent statement in `_intent/_intent.md` that matches the repository. Often one or two sentences describe the whole system accurately, e.g. "LightPlayer is an LED control system for ESP32 that compiles GLSL shaders to native code."

The user writes it; you don't. Ask questions that help them, and check that what they wrote is true of the repository. Vague is fine: detail comes later, where they make changes (see the `hdd-backfill` skill).

Commit it as an intent commit: only intent, no co-authorship trailer, with the statement quoted in the message.

## Next

Tell the user how to make their first change: `hdd-backfill` for an area without detailed intent, then `hdd-change` and `hdd-implement`.
