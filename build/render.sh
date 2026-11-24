#!/usr/bin/env bash
# Render build/poster.html to entry.png at exactly 1024x1024.
#
# Two things are checked before the committed image is replaced. The screenshot
# must be 1024x1024, because the gate refuses anything larger a side. And the
# outer frame must be one colour, because that is what a page that spilled past
# the square looks like: the background stops and something else shows through.
# A build that fails either test leaves the previous entry.png untouched.
set -euo pipefail

CHROME=${CHROME:-/root/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome}
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
RAW="${TMPDIR:-/root/.hermes/cache/scratch}/ni24_raw.png"

python3 "$HERE/poster.py"

"$CHROME" \
  --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size=1024,1024 \
  --virtual-time-budget=6000 \
  --screenshot="$RAW" "file://$HERE/poster.html"

python3 - "$RAW" "$ROOT/entry.png" <<'PY'
import sys
from PIL import Image

raw, out = sys.argv[1], sys.argv[2]
page = Image.open(raw).convert("RGB")
if page.size != (1024, 1024):
    sys.exit("page rendered at %dx%d, not 1024x1024" % page.size)

# A page that spilled past its frame shows a different colour at the border
# than in the corner: sample the four sides and demand they are all one paper.
# The sheet carries a faint grain, so compare colours by closeness, not exactly.
w, h = page.size
edge = [page.getpixel((x, 0)) for x in range(0, w, 7)]
edge += [page.getpixel((x, h - 1)) for x in range(0, w, 7)]
edge += [page.getpixel((0, y)) for y in range(0, h, 7)]
edge += [page.getpixel((w - 1, y)) for y in range(0, h, 7)]
base = edge[0]
for c in edge:
    if max(abs(c[i] - base[i]) for i in range(3)) > 24:
        sys.exit("the page spilled past its 1024 square: %s on the border, %s on the corner" % (c, base))

page.save(out, "PNG", optimize=True)
print("entry.png: %dx%d, %d bytes" % (page.size[0], page.size[1], len(open(out, "rb").read())))
PY
