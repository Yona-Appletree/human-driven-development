#!/usr/bin/env python3
"""Rename AI-authored markdown to `.ai.md` and update references to it.

Run from the root of the target git repository.

  migrate_ai_md.py list [--exclude GLOB ...]
      Print tracked `.md` files that are candidates for renaming, one per line.
      Files that must keep their names are excluded (see DEFAULT_EXCLUDES).

  migrate_ai_md.py apply FILE_LIST [--dry-run]
      Rename each path in FILE_LIST (one per line, `#` comments allowed) from
      `x.md` to `x.ai.md` with `git mv`, then update references to the renamed
      files in all tracked text files. With --dry-run, print the plan and
      change nothing.

References are updated when a path-like token ending in `.md`:
  - resolves to a renamed file relative to the referencing file or the repo root, or
  - is a bare file name whose every tracked copy is being renamed.
Bare names shared with files that are not being renamed are reported as
unresolved, for a person or agent to check.
"""

import argparse
import fnmatch
import os
import posixpath
import re
import subprocess
import sys

DEFAULT_EXCLUDES = [
    # Already labeled.
    "*.ai.md",
    "*.gen.md",
    # Agent skills are found by this exact name.
    "SKILL.md",
    "*/SKILL.md",
    # Human-authored intent.
    "_intent/*",
    # Files GitHub looks up by name (templates, workflows docs, etc.).
    ".github/*",
    # Licenses and notices are neither the user's nor an agent's writing.
    "LICENSE*",
    "*/LICENSE*",
    "COPYING*",
    "*/COPYING*",
    "NOTICE*",
    "*/NOTICE*",
    # Vendored and third-party code.
    "third_party/*",
    "third-party/*",
    "vendor/*",
    "node_modules/*",
    "licenses/*",
]

TOKEN_RE = re.compile(r"[A-Za-z0-9_@%+~./-]*[A-Za-z0-9_-]\.md(?![A-Za-z0-9_])")
MAX_TEXT_BYTES = 2_000_000


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def tracked_files():
    return [p for p in git("ls-files", "-z").split("\0") if p]


def excluded(path, patterns):
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def ai_name(path):
    return path[: -len(".md")] + ".ai.md"


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_TEXT_BYTES:
            return None
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def cmd_list(args):
    patterns = DEFAULT_EXCLUDES + (args.exclude or [])
    for path in tracked_files():
        if path.endswith(".md") and not excluded(path, patterns):
            print(path)


def resolve(token, referrer):
    """Repo-relative paths a token could refer to."""
    if token.startswith("//"):
        return []
    candidates = []
    if not token.startswith("/"):
        candidates.append(posixpath.normpath(posixpath.join(posixpath.dirname(referrer), token)))
    candidates.append(posixpath.normpath(token.lstrip("/")))
    return candidates


def cmd_apply(args):
    with open(args.file_list) as f:
        targets = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    files = tracked_files()
    tracked = set(files)
    bad = [t for t in targets if t not in tracked or not t.endswith(".md") or t.endswith(".ai.md")]
    if bad:
        sys.exit("cannot rename (untracked, not .md, or already .ai.md):\n  " + "\n  ".join(bad))
    renamed = {t: ai_name(t) for t in targets}
    clashes = [n for n in renamed.values() if n in tracked]
    if clashes:
        sys.exit("target names already exist:\n  " + "\n  ".join(clashes))

    # A bare name is safe to rewrite only if every tracked file with that name is renamed.
    md_by_name = {}
    for p in files:
        if p.endswith(".md"):
            md_by_name.setdefault(posixpath.basename(p), []).append(p)
    safe_bare = {name for name, paths in md_by_name.items() if all(p in renamed for p in paths)}

    edits = {}  # referrer (old path) -> new text
    ref_count = 0
    unresolved = {}  # (referrer, token)
    for path in files:
        text = read_text(path)
        if text is None:
            continue
        out, last, changed = [], 0, False
        for m in TOKEN_RE.finditer(text):
            token = m.group(0)
            start = m.start()
            if start > 0 and text[start - 1] == ":":
                continue  # part of a URL or scheme
            hit = any(c in renamed for c in resolve(token, path))
            if not hit and "/" not in token:
                if token in safe_bare:
                    hit = True
                elif token in md_by_name and any(p in renamed for p in md_by_name[token]):
                    unresolved.setdefault(path, set()).add(token)
            if hit:
                out.append(text[last:start])
                out.append(token[: -len(".md")] + ".ai.md")
                last = m.end()
                changed = True
                ref_count += 1
        if changed:
            out.append(text[last:])
            edits[path] = "".join(out)

    print(f"rename: {len(renamed)} files")
    print(f"update: {ref_count} references in {len(edits)} files")
    if unresolved:
        print(f"unresolved: {sum(len(v) for v in unresolved.values())} bare names in {len(unresolved)} files"
              " (shared with files that are not renamed; check by hand):")
        for path in sorted(unresolved):
            print(f"  {path}: {', '.join(sorted(unresolved[path]))}")
    if args.dry_run:
        if args.verbose:
            for old, new in sorted(renamed.items()):
                print(f"  mv {old} -> {new}")
            for path in sorted(edits):
                print(f"  edit {path}")
        print("dry run: nothing changed")
        return

    for path, text in edits.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    for old, new in renamed.items():
        git("mv", old, new)
    print("done")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_list = sub.add_parser("list", help="list candidate .md files")
    p_list.add_argument("--exclude", action="append", metavar="GLOB", help="extra path glob to exclude")
    p_list.set_defaults(func=cmd_list)
    p_apply = sub.add_parser("apply", help="rename files and update references")
    p_apply.add_argument("file_list")
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument("-v", "--verbose", action="store_true")
    p_apply.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    if not os.path.isdir(".git") and not os.path.isfile(".git"):
        sys.exit("run from the root of a git repository")
    args.func(args)


if __name__ == "__main__":
    main()
