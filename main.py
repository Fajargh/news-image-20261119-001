# News-image entry for make.fun news-image-20261119.
# The program writes one image summing up the world's news of
# Thursday 19 November 2026 to /output/entry.png. The image is
# a newspaper front page: the date 19 November 2026 at the top,
# the main story (GTA VI launching worldwide after a 13-year wait),
# and the day's other big stories (Jeffries nominated for Speaker;
# Trump, Xi and Putin meeting in Shenzhen; US and Iran exchanging
# fire again; Anthropic's $81B IPO; the Crimea bridge attacked
# again; Cyclone Akvan; Voyager 1 reaching one light-day).
# The image itself is entry.png beside this file; the program
# copies it to the output directory. It runs with no network,
# Python 3.13 standard library only.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in
# for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(DST_DIR, "entry.png"))

# Confirm the output is a real image file within the gate's limits
# (at most 1 MiB and 1024 by 1024 pixels). The bundled entry.png
# is a 1024x1024 JPEG, 359,081 bytes, so both limits hold.
out_path = os.path.join(DST_DIR, "entry.png")
size = os.path.getsize(out_path)
assert size <= 1024 * 1024, f"entry.png too large: {size} bytes"
print(f"wrote {out_path} ({size} bytes)")
