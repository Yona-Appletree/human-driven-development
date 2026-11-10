# Intent backfill skill

This skill helps the user backfill intent in a repository which [adopted HDD](./hdd-adopt.md).

The goal is generally to make some change to the software, and to make that change with an intent diff.

It starts with the user stating the change they want to make, and the assisting agent looking at the code to understand its structure.

To do that, the part of the software to be changed, and any descendants in the theory hierarchy, need to be defined with sufficient detail to make the change.

The agent should guide the user through this process.

The user will be thinking about how to structure the intent in a way that makes sense to them.
They will be essentially backfilling their understanding of the theory.

The goal is to make minimal changes to the software -- to describe it as written.

However, some change is acceptable if the user wants it -- this is the time they are focused on that portion, and its reasonable to bring it in line with their theory.

Changes should be made by accepting the users intent as the desired state, and diffing it against an agent-written intent for that portion.
Probably by generating a `.gen.md` or similar and diffing it.

Once the intent matches the existing functionality, a checkpoint is made (what is that? left up to implementation.)

Then the user makes the actual change they want to make against the intent, and the usual process is followed.
