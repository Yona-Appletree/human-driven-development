# Human driven development

Human driven development is a software development process where humans drive, own, and understand what they build using agents.

In HDD, humans build [the theory of the software](https://gwern.net/doc/cs/algorithm/1985-naur.pdf) in their minds, write their **intent** for its implementation, and agents built it.

It is a [spec-driven-development](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) process that emphasizes human authorship.

## Purpose

This project is place for me to define my personal take on SDD and reuse for my personal and professional projects.

If you find it useful, great!
I would love to hear your thoughts on it.

PRs are welcome, though I make no promises on reviewing or merging them.

## Intent

Intent is the structured, human-authored words that descibe what a program does.
When interactivly coding with an agent, the prompts are the intent. 

In this process, intent is a series of statements about what the application does, usually in the simple present tense:

```text
# todo.md

A **todo item** has a name and a due date.
Todo items with a due date in the past are **late**.
Overdue todo items are indicated with a warning.
```

Intent files are organized into a strcuture that matches the author's theory of the program.
Using `_`-prefixed files is encourged to keep 

Example:

```text
intent/
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

An `intent/` directory holds intent at the root of the project.

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

Prior art includes anchored spec-driven development methods