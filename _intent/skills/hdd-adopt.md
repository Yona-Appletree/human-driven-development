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

An agent can create the intial `_intent/_intent.md` directory and file (without content).

Intent for the implementation skills can be copied from this repo and the skills built.

The agent should guide the user to write a high level intent statement that matches the repository.
