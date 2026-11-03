#!/usr/bin/env python3
"""Create (or complete) a notes vault for the Second Brain: category folders, note templates, Obsidian settings.

    python3 vault_init.py <folder>            create the vault, or add whatever is missing to an existing one
    python3 vault_init.py <folder> --dry-run  show what would be created; change nothing

Never overwrites or deletes anything: existing files and folders are left exactly as they are.
Works on macOS, Linux and Windows (standard library only). The Second Brain itself only READS the vault.
"""
import os, shutil, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "vault")

def plan(dest):
    """Return [(kind, relative_path)] for everything missing in dest. Existing .obsidian settings are never touched."""
    todo = []
    has_obsidian = os.path.isdir(os.path.join(dest, ".obsidian"))
    for d, dirs, files in os.walk(SRC):
        dirs.sort()
        rel = os.path.relpath(d, SRC)
        if rel.split(os.sep)[0] == ".obsidian" and has_obsidian:
            continue
        if rel != "." and not os.path.isdir(os.path.join(dest, rel)):
            todo.append(("dir", rel))
        for f in sorted(files):
            r = os.path.normpath(os.path.join(rel, f))
            if not os.path.lexists(os.path.join(dest, r)):
                todo.append(("file", r))
    return todo

def init(dest, dry_run=False, out=print):
    dest = os.path.abspath(os.path.expanduser(dest))
    if os.path.islink(dest) or (os.path.exists(dest) and os.path.realpath(dest) != dest):
        raise SystemExit(f"{dest} is (or passes through) a symlink: give the real path")
    if os.path.exists(dest) and not os.path.isdir(dest):
        raise SystemExit(f"{dest} exists and is not a folder")
    todo = plan(dest)
    if not dry_run:
        os.makedirs(dest, exist_ok=True)
        for kind, rel in todo:
            target = os.path.join(dest, rel)
            if kind == "dir":
                os.makedirs(target, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if not os.path.lexists(target):  # re-check right before copying: never overwrite
                    shutil.copyfile(os.path.join(SRC, rel), target)
    for kind, rel in todo:
        out(f"  {'would create' if dry_run else 'created'} {kind:4} {rel}")
    out(f"{'Dry run: ' if dry_run else ''}{len(todo)} item(s) {'missing' if dry_run else 'added'} in {dest}; nothing existing was changed.")
    return dest, todo

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        raise SystemExit(__doc__)
    init(args[0], dry_run="--dry-run" in sys.argv)
