#!/usr/bin/env python3
"""Entry point for the news-image-20261119 bounty.

The front page artwork is produced by draw_frontpage.py and stored in this
repository as entry.png. This program's only job is to place that image
where the judge expects it and confirm it meets the size cap.

Standard library only: no third-party imports, no network access.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    if not os.path.isfile(source):
        print("error: entry.png is missing next to main.py", file=sys.stderr)
        return 1

    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")

    shutil.copyfile(source, target)

    size = os.path.getsize(target)
    print(f"entry.png -> {target} ({size} bytes)")
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    print("OK: entry.png is within the 1 MiB limit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
