# Entry program for make.fun news-image-20261119.
#
# The entry is a newspaper front page summing up Thursday
# 19 November 2026: GTA VI launches worldwide after a 13-year
# wait; Jeffries is nominated for Speaker; Trump, Xi and Putin
# meet in Shenzhen; the US and Iran exchange fire again;
# Anthropic's $81B IPO; the Crimea bridge is attacked again;
# Cyclone Akvan; and Voyager 1 reaches one light-day.
#
# The front page itself is entry.png, stored beside this file.
# This program copies it to the output directory the grader
# expects. Python 3.13 standard library only, no network.
#
# To test outside the grader's container, set the output dir:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)

# The gate requires the output image to be at most 1 MiB
# (1048576 bytes) and 1024 by 1024 pixels at most.
# entry.png is a 1024x1024 JPEG of 359,081 bytes, so this holds.
size = os.path.getsize(DST)
assert size <= 1048576, f"entry.png too large: {size} bytes"
print(f"wrote {DST} ({size} bytes)")
