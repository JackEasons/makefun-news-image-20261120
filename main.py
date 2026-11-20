#!/usr/bin/env python3
"""News-image entry: copy the built entry.png to the output directory.

Runs with no network, Python 3.13 standard library only. The image itself
is drawn by draw.py (PIL, run locally); this program only copies the bytes,
so both grader runs write byte-identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size > 1048576:
        print(f"entry.png too large: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
