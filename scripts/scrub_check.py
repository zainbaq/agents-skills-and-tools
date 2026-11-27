#!/usr/bin/env python3
"""Fail if a blocked term appears in anything that could be pushed.

usage: python scripts/scrub_check.py [REPO_ROOT]

Blocked terms are read from `.scrub-blocklist` in the repository root. That file is
listed in .gitignore and is never committed, because the terms themselves are private.

Blocklist format, one entry per line:
    some client name        a literal term, matched case-insensitively as a whole word or phrase
    re:acme[- ]?corp        a regular expression, matched case-insensitively
    # a comment             blank lines and lines starting with # are ignored

What is scanned: every file git tracks or would add (so files ignored by .gitignore are
skipped, since they cannot be pushed), plus each file's path. Without git, every file
outside .git/ is scanned. The blocklist file itself is never scanned.

Exit codes: 0 = no match, or no blocklist file (a warning is printed); 1 = at least one match.
Standard library only.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

BLOCKLIST = ".scrub-blocklist"


def load_patterns(path):
    patterns = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            source = line[3:].strip()
        else:
            source = r"(?<![A-Za-z0-9])" + re.escape(line) + r"(?![A-Za-z0-9])"
        try:
            patterns.append((n, re.compile(source, re.I)))
        except re.error as e:
            sys.exit(f"{BLOCKLIST} line {n}: bad pattern ({e})")
    return patterns


def candidate_files(root):
    try:
        r = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                           capture_output=True, check=True)
        names = [n for n in r.stdout.decode("utf-8", "replace").split("\0") if n]
        return [root / n for n in names], "files git tracks or would add"
    except (OSError, subprocess.CalledProcessError):
        found = []
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d != ".git"]
            found.extend(Path(base) / f for f in files)
        return found, "every file outside .git/"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent).resolve()
    blocklist = root / BLOCKLIST
    if not blocklist.is_file():
        print(f"WARNING: no {BLOCKLIST} file in {root}; nothing was checked. "
              "Create it (one blocked term per line) to make this check real.")
        return 0
    patterns = load_patterns(blocklist)
    if not patterns:
        print(f"WARNING: {BLOCKLIST} has no terms; nothing was checked.")
        return 0

    files, scope = candidate_files(root)
    hits = 0
    for path in sorted(files):
        if path.name == BLOCKLIST or not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        # Matches are reported by blocklist line number, so the private terms are never printed.
        for n, pat in patterns:
            if pat.search(rel):
                print(f"MATCH {rel}: file path matches blocklist line {n}")
                hits += 1
        try:
            text = path.read_bytes().decode("utf-8", "replace")
        except OSError as e:
            print(f"WARNING: could not read {rel}: {e}")
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for n, pat in patterns:
                if pat.search(line):
                    print(f"MATCH {rel}:{lineno}: blocklist line {n}")
                    hits += 1
    print(f"{len(files)} file(s) scanned ({scope}), {len(patterns)} term(s), {hits} match(es)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
