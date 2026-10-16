"""D-Log M -> Rec.709 + Megan Tan 'Ghibli' grade (well-exposed recipe), baked to a 33^3 .cube.
Node order follows the tutorial: CST -> correction -> saturation (HSV, ch2) -> curves -> film look -> hue vs hue.
Grain is added in ffmpeg after the LUT."""
import sys
import numpy as np

# presets tuned on Anushka's D-Log M footage (DJI Osmo Pocket 3, grey wall, soft daylight)
PRESETS = {
    # Megan Tan "Ghibli" grade, well-exposed recipe: creamy wall, peachy skin, pastel hair
    'ghibli': dict(tint=[.995, 1.012, .995], fade=(.94, .03), warm=[.010, .016, -.010], cool=[-.006, .008, .010]),
    # "One Day Off" K-drama reference: greener, golden sunlit highlights, olive shadows (pair with --glow)
    'dreamy': dict(tint=[.985, 1.030, .972], fade=(.93, .035), warm=[.024, .022, -.026], cool=[-.012, .016, -.002]),
}
if len(sys.argv) < 3 or sys.argv[1] not in PRESETS:
    sys.exit('usage: make_lut.py ghibli|dreamy out.cube [strength 0-1]')
P = PRESETS[sys.argv[1]]
OUT = sys.argv[2]
STRENGTH = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
N = 33

def pchip(x, xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    h = np.diff(xs); d = np.diff(ys) / h
    m = np.zeros_like(ys)
    for k in range(1, len(xs) - 1):
        if d[k-1] * d[k] > 0:
            w1, w2 = 2*h[k] + h[k-1], h[k] + 2*h[k-1]
            m[k] = (w1 + w2) / (w1/d[k-1] + w2/d[k])
    m[0], m[-1] = d[0], d[-1]
    x = np.clip(x, xs[0], xs[-1])
    k = np.clip(np.searchsorted(xs, x) - 1, 0, len(xs) - 2)
    t = (x - xs[k]) / h[k]
    h00, h10, h01, h11 = 2*t**3-3*t**2+1, t**3-2*t**2+t, -2*t**3+3*t**2, t**3-t**2
    return h00*ys[k] + h10*h[k]*m[k] + h01*ys[k+1] + h11*h[k]*m[k+1]

def luma(c): return c[..., 0]*.2126 + c[..., 1]*.7152 + c[..., 2]*.0722

g = np.linspace(0, 1, N)
B, G, R = np.meshgrid(g, g, g, indexing='ij')       # .cube order: R fastest
c = np.stack([R, G, B], -1)

# 1. CST: D-Log M -> Rec.709 (tone curve measured on this clip: black stripes .20, skin .35, wall .50-.61, peak .79)
lo = c.copy()
tone = lambda x: pchip(x, [0, .09, .20, .35, .50, .61, .79, 1.0], [0, .0, .055, .40, .74, .87, .985, 1.0])
c = tone(c)
y = luma(c)[..., None]
c = y + (c - y) * 1.12                                 # D-Gamut -> Rec.709 saturation recovery
c = np.clip(c, 0, 1)
cst = c.copy()

# 2. correction: highlights -25.5, contrast 1.14 @ pivot .60, temp -70, tint -9.5 (greener)
y = luma(c)[..., None]
hl = np.clip((y - .6) / .4, 0, 1) ** 2
c = c - hl * .06 * c
c = (c - .60) * 1.08 + .60
c = c * np.array([.988, 1.0, 1.012])                   # temp -70: slightly cooler
c = c * np.array(P['tint'])                            # tint: green
c = np.clip(c, 0, 1)

# 3. saturation node in HSV, channel 2 only: gamma +.02, gain 1.20
mx, mn = c.max(-1, keepdims=True), c.min(-1, keepdims=True)
s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
s2 = np.clip(s ** (1 / 1.02 ** 4) * (1 + .20 * (1 - s)), 0, 1)   # gain lifts the pale colours, not the already-rich orange
c = np.where(mx > 1e-6, mx - (mx - c) * np.divide(s2, s, out=np.ones_like(s), where=s > 1e-6), c)
c = np.clip(c, 0, 1)

# 4. curves: green highlights down (magenta in highlights), green mids down a touch, red mids down
r, gg, b = c[..., 0], c[..., 1], c[..., 2]
gg = pchip(gg, [0, .25, .5, .8, 1], [0, .25, .49, .78, .985])
r = pchip(r, [0, .25, .5, .8, 1], [0, .238, .47, .79, 1])
c = np.stack([r, gg, b], -1)

# 5. film look creator, cinematic ~.1 + skin bias to magenta: warm creamy highlights, soft lifted blacks
y = luma(c)[..., None]
c = c * P['fade'][0] + P['fade'][1] + .03 * y                            # gentle fade / lifted blacks
warm = np.clip((y - .45) / .55, 0, 1)
c = c + warm * np.array(P['warm'])           # cream-yellow highlights (Ghibli paper)
cool = np.clip((.4 - y) / .4, 0, 1)
c = c + cool * np.array(P['cool'])           # faint green-teal shadows
c = np.clip(c, 0, 1)

# 6. hue vs hue: greens/yellows nudged toward yellow-green (pastel), skin untouched
mx, mn = c.max(-1), c.min(-1); d = mx - mn + 1e-9
h = np.where(mx == c[..., 0], ((c[..., 1] - c[..., 2]) / d) % 6, np.where(mx == c[..., 1], (c[..., 2] - c[..., 0]) / d + 2, (c[..., 0] - c[..., 1]) / d + 4)) * 60
w = np.exp(-((h - 120) / 35) ** 2) * np.clip(d * 4, 0, 1)
y = luma(c)[..., None]
wo = np.exp(-((h - 24) / 22) ** 2) * np.clip(d * 3, 0, 1)
yy = luma(c)[..., None]
c = c + wo[..., None] * (yy + (c - yy) * .80 - c)
c = c + w[..., None] * (np.stack([c[..., 1]*.92, c[..., 1], c[..., 2]*.9], -1) - c) * .35
c = np.clip(c, 0, 1)

c = cst + (c - cst) * STRENGTH
with open(OUT, 'w') as f:
    f.write(f'TITLE "DLogM {sys.argv[1]}"\nLUT_3D_SIZE {N}\n')
    for v in c.reshape(-1, 3):
        f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
print('wrote', OUT)
