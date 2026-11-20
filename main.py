#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to the output path.

The image itself is drawn by draw.py at build time (pure PIL, no
network) and shipped in this repository as entry.png. This program
only copies those exact bytes, so two runs always agree.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    src_bytes = os.path.getsize(src)
    dst_bytes = os.path.getsize(dst)
    if src_bytes != dst_bytes:
        raise SystemExit("copy mismatch: %d != %d" % (src_bytes, dst_bytes))
    print("wrote %s (%d bytes)" % (dst, dst_bytes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
