# Looks

All looks start from **D-Log M** (DJI Osmo Pocket 3). The conversion to Rec.709 was measured on Anushka's footage
(grey wall, soft daylight), since DJI's official LUT isn't reachable from the cloud. On footage shot in Rec.709
(not log), don't use these LUTs as they are: grade with a lighter touch instead.

| look | reference | what it does | render |
|---|---|---|---|
| `ghibli` | Megan Tan, "How To Color Grade like Ghibli" (well-exposed recipe) | creamy wall, peachy natural skin, pastel hair, soft contrast, slight green tint, 16mm grain | `--look ghibli` |
| `dreamy` | "One Day Off" K-drama (Pinterest) | greener tint, golden sunlit highlights, olive shadows, lifted blacks, soft highlight glow | `--look dreamy` (glow 0.42 by default) |

Node order inside `make_lut.py` follows the tutorial: CST → correction (highlights, contrast/pivot, temp, tint) →
saturation in HSV channel 2 → curves (G highlights/mids down, R mids down) → film look (fade, warm highlights,
tinted shadows) → hue vs hue (greens toward yellow, oranges softened so skin and hair stay pastel).

Regenerate: `PY make_lut.py ghibli ghibli_dlogm.cube` (optional 3rd arg: strength 0-1).
Add a look: copy a preset in `PRESETS`, change tint / fade / warm / cool, test on stills, commit.

The `.cube` files also work in CapCut and DaVinci Resolve (colour only; add glow and grain there separately).
