# HDD adopt skill

This skill sets up an existing repository for using HDD.

The skill applies to new projects and existing projects.

## AI file migration

The first step is to identify AI markdown content and rename it to `.ai.md` to follow the norms.

The skill includes a script that handles the renaming of `.md` -> `.ai.md` and updating the references.

Exceptions are made per this repo's `AGENTS.md`, such as `SKILL.md`.

This may be very large diff, that's OK. All references to the files should be updated.

This repo's `AGENTS.md` is copied into the target repo.

A dummy `README.md` is created with this content:

```md
See [README.ai.md](./README.ai.md) for information about this project until a person rewrites the readme.
```

## Intent scaffolding

Create the initial `_intent/` directory and `.gitignore` in it.

Create `_intent/_intent.md` with:

```text
# Intent

This directory describes what the software does, following [human-driven-development](https://github.com/Yona-Appletree/human-driven-development).
```

Intent for the implementation skills is copied as well.

Offer to copy the hygiene intent as well, but let the user decide.

The agent should guide the user to write a high level intent statement that matches the repository.

Use the `hdd-implement` skill to implement the initial intent (the skills and hygiene).
