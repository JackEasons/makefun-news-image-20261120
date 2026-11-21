#!/usr/bin/env python3
"""Copy the pre-rendered front page into the judge's output directory.

The page is drawn by press.py at build time and committed as entry.png.
This program does nothing but copy it: it needs no network, writes
nothing into the repository directory, and finishes in well under a
second under the judge's read-only /bot.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(path):
    """Refuse anything that is not a small, well-formed PNG."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        sys.exit("entry.png too large: %d bytes" % size)
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        sys.exit("entry.png is not a PNG")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit("entry.png too big: %dx%d" % (width, height))
    return size, width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    size, width, height = check_png(src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied %s -> %s (%d bytes, %dx%d)"
          % (src, dst, size, width, height))


if __name__ == "__main__":
    main()
