# Human driven development

Human driven development is a software development process where humans drive, own, and understand what they build using agents.

I was motivated to create it after using chat-based agentic methods and getting frustrated with the feeling of not understanding the code.

I designed it around these requirements:

1. I want to own the [theory of the software](https://gwern.net/doc/cs/algorithm/1985-naur.pdf)
2. I want my changes to the software to be reviewed
3. I don't want to review AI-authored text

To meet these requirements, this design emerged:

1. The intent of the software is written by humans.
2. Other humans can review the intent.
3. Agents implement the software based on diffs of the intent.

## Purpose

This is a personal project, a place to hold my thoughts, process, and agent skills.

I use it to onboard personal and professional projects to this process.

If you find it useful, great!
I would love to hear your thoughts on it.

PRs are welcome, though I make no promises on reviewing or merging them.

## Intent

Intent is the structured, human-authored description of what software does.
It is stated in the simple present tense:

```text
# todo.md

A **todo item** has a name and a due date.
Todo items with a due date in the past are **late**.
Overdue todo items are indicated with a warning.
```

Intent does not have to be very specific:

```text
Secrets stored in the database are encrypted following best practices for a web app.
```

This is acceptable because it records what the author intended.
It is arguably better than the author trying to come up with specifics beyond what they understand.
If they want to improve it later, that is an intent change, which is fine.

## Intent structure

Intent files are organized into a strcuture that matches the author's theory of the program.
Using `_`-prefixed files is encourged to keep

Example:

```text
_intent/
  frontend/
    _frontend.md
    shell.md
    nav.md
  backend/
    _backend.md
    architecture.md
    api.md
  features/
    _features.md
    profile.md
    auth.md
    todo.md
  _README.md
```

## Process

An `_intent/` directory holds intent at the root of the project.
The `_` prefix ensures it appears first in diffs and file listings.

To make a change:

1. An author modifies the intent by hand, with an optional agent assistant
2. An agent diffs the intent and uses that to plan and implement the change
3. The author verifies the change, potentially makes more changes, which are implemented in a loop
4. The author makes a PR

In projects with other developers, they can review the intent changes while agents review the code changes.
This way people don't have to review ai-generated content, while still having a chance to review the change.

## Comparison with other processes

In standard iterative procsses with agents, the intent is stored only in the transcript with the agent, and lost when the conversation is over.

What remains is a lossy "projection" of the original user intent and theory, and it is difficult to recover what the prompter was thinking after the fact.

## Credit & prior art

Credit to Eshan Hoque for the idea

1. [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl, Oct 2025](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
