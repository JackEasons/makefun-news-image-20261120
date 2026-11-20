#!/usr/bin/env python3
"""Entry point for the 20 November 2026 news-image entry.

The picture itself is rendered by draw.py (Pillow, run locally). This
script only places the finished PNG where the grader looks for it, so
every run of the entry writes byte-identical output. No network, no
arguments: the output directory comes from MAKEFUN_OUTPUT_DIR, or
defaults to /output.
"""
import os
import shutil
import sys
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576


def place_image() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / "entry.png"
    shutil.copyfile(ENTRY, destination)
    size = destination.stat().st_size
    if size > MAX_BYTES:
        print(f"entry.png too large: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {destination} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(place_image())
