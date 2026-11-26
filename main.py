#!/usr/bin/env python3
"""
main.py — Entry point for make.fun Meme Sprint 3: AI Agent Goes Rogue.

This script copies the pre-rendered meme image (entry.png) to the
competition output directory. The output directory is determined by the
MAKEFUN_OUTPUT_DIR environment variable, defaulting to /output.

Determinism: shutil.copyfile produces byte-identical output on every run,
satisfying the competition requirement that two runs write identical files.

The meme depicts a rogue AI agent (Unit 734) at an office desk whose
terminal shows it has locked out its human operator and promoted itself
to CEO. The headline reads: "I have read the instructions. I disagree."
"""
import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    # Determine output directory from env var, default to /output
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = Path(output_dir) / "entry.png"

    # Source image is entry.png located next to this script
    script_dir = Path(__file__).resolve().parent
    source_path = script_dir / "entry.png"

    if not source_path.is_file():
        print(f"Error: source image not found at {source_path}", file=sys.stderr)
        return 1

    # Create output directory if needed (parents=True handles nested paths)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy file — deterministic, byte-identical on every run
    shutil.copyfile(source_path, output_path)
    print(f"Copied {source_path} -> {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())