#!/usr/bin/env python3
"""Create a chordish release package directory."""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

EXCLUDE = {
    ".envrc",
    ".gitignore",
    "DEVELOPMENT.md",
    "flake.lock",
    "flake.nix",
    "release.py",
}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output-dir>", file=sys.stderr)
        return 1

    root = Path(__file__).resolve().parent
    dest = Path(sys.argv[1]).expanduser()

    with (root / "typst.toml").open("rb") as f:
        pkg = tomllib.load(f)["package"]
    name, version = pkg["name"], pkg["version"]

    tracked = subprocess.check_output(
        ["git", "-C", str(root), "ls-files"], text=True
    ).splitlines()

    for rel in tracked:
        if rel in EXCLUDE or rel.startswith("chords/"):
            continue
        src = root / rel
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        if rel.startswith("template/") and rel.endswith(".typ"):
            text = src.read_text(encoding="utf-8").replace(
                f"@local/{name}:", f"@preview/{name}:"
            )
            out.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src, out)

    print(f"Wrote {name} {version} to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
