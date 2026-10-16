"""Studio reel template: the approved v2 build of "my AI accountability team" (Oct 2026), house style built in.

Copy into a video-edit project as build.py (next to segments.json, assets/aroll.mp4, assets/subject.webm) and copy
ST/tools/vendor/gsap.min.js to <project>/assets/vendor/gsap.min.js.

Keep (machinery): dude_words(), grades(), audio(), CSS, SAFE_GUIDE, build(), cut times from segments.json.
Rewrite (content):
  CHUNKS            (start, [(appear, text, classes, style)]); each chunk replaces the previous one; the assert
                    enforces <= 3 words on screen. Classes: c (100px line), p (170px yellow punch), n (220px name),
                    h / h2 (300 / 220px stacked numbers), y = yellow, w = white, back = behind the head.
                    Positions: WC/WP/WN on wide shots (text on the wall above the head), ZC/ZP/ZN on punch-ins,
                    CHEST under the chin, LST/RST = left/right stacks for the slide-and-stack move.
  SHIFT_R, SHIFT_L  times of the slide-right / slide-left beats; the shot they live in is the 'books' key in
                    grades(): rename it to the segment id you use the move on (or delete the branch).
  SFX               name, time, volume. Keep the CTA clean.
Measure head tops with VE/scripts/headpos.py and adjust WC/WP/WN/ZC/ZP/ZN if her framing differs.
Run with PY build.py [--safe].
"""
import json
import os
import shutil
import subprocess
import sys

SAFE = '--safe' in sys.argv or bool(os.environ.get('SAFE'))
DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, encoding='utf-8', errors='replace').stdout.strip().split(',')[0])
YEL = '#FAE67A'
with open('segments.json', encoding='utf-8') as _f:
    SEG = {s['id']: s for s in json.load(_f)}
T = {k: s['frame'] / 30 - .002 if s['frame'] else 0.0 for k, s in SEG.items()}
CUTS = [t for k, t in T.items() if k != 'hook']
BOLD_F = 'contrast(1.07) saturate(.9) brightness(.97)'
TW_, TH_ = 190, 338

# Instagram Reels safe zone: top 220, bottom 450 (nothing below y=1470), sides 35, right 100 from y~1155.
# v2 rules from Anushka: max 3 words on screen, use the empty wall above the head, motion in the frame.
C = 'left:0;right:0;text-align:center;'
WC, WP, WN = C + 'top:372px', C + 'top:318px', C + 'top:445px'      # wide shots: head top ~565
ZC, ZP, ZN = C + 'top:246px', C + 'top:300px', C + 'top:290px'      # punch-ins: head top ~410
CHEST = C + 'top:1010px'
LST = 'left:40px;width:540px;text-align:center;'     # left stack (frame shifted right)
RST = 'left:700px;width:345px;text-align:center;'    # right stack (frame shifted left)
t = T
SHIFT_R, SHIFT_L = 23.95, 25.00                       # "i read" / "by the end"
CHUNKS = [  # (start, [(appear, text, classes, style)])  each chunk replaces the last; <= 3 words on screen
    # hook (wide)
    (0.00, [(0.00, 'but this time,', 'c', WC)]),
    (0.54, [(0.54, "i'm building", 'c', WC)]),
    (0.92, [(0.92, 'a team', 'p', WP)]),
    (1.24, [(1.24, 'to keep me', 'c', WC)]),
    (1.70, [(1.70, 'accountable', 'p', WP)]),
    (2.10, [(2.10, 'using', 'c', WC)]),
    (2.48, [(2.48, 'grok bot', 'n back', WN)]),
    (2.96, [(2.96, 'by spacex ai', 'c', WC)]),
    # friend (punch-in)
    (t['friend'], [(t['friend'], 'and i can', 'c', ZC)]),
    (4.30, [(4.30, 'literally', 'c', ZC)]),
    (4.58, [(4.58, 'text them', 'c', ZC)]),
    (5.00, [(5.00, 'like a friend.', 'c y', ZC)]),
    # each bot (wide)
    (t['eachbot'], [(t['eachbot'], 'each bot has', 'c', WC)]),
    (6.18, [(6.18, 'a specific', 'c', WC)]),
    (6.68, [(6.68, 'goal', 'p', WP)]),
    (6.92, [(6.92, 'and has access', 'c', WC)]),
    (7.52, [(7.52, 'to all of', 'c', WC)]),
    (8.00, [(8.00, 'my tools.', 'p', WP)]),
    # tyler (punch-in)
    (t['tyler'], [(t['tyler'], 'tyler', 'n back', ZN), (8.80, 'is my', 'c', CHEST)]),
    (9.16, [(9.16, 'trainer.', 'p back', ZP)]),
    (9.60, [(9.60, 'he tracks all', 'c', ZC)]),
    (10.20, [(10.20, 'of my workouts', 'c', ZC)]),
    (10.78, [(10.78, 'and meals,', 'c y', ZC)]),
    # apple watch (wide)
    (t['watch'], [(t['watch'], 'has access to', 'c', WC)]),
    (12.28, [(12.28, 'my apple watch,', 'c y', WC)]),
    (13.16, [(13.16, 'knows my personal', 'c', WC)]),
    (13.76, [(13.76, 'food preferences', 'c y', WC)]),
    (14.48, [(14.48, 'and makes sure', 'c', WC)]),
    (15.16, [(15.16, "i'm eating", 'c', WC)]),
    (15.54, [(15.54, 'healthy.', 'p', WP)]),
    # sabrina (punch-in)
    (t['sabrina'], [(t['sabrina'], 'sabrina', 'n back', ZN), (16.40, 'handles my', 'c', CHEST)]),
    (16.92, [(16.92, 'finances.', 'p back', ZP)]),
    # money (wide)
    (t['money'], [(t['money'], 'she tracks', 'c', WC)]),
    (17.86, [(17.86, 'how much', 'c', WC)]),
    (18.12, [(18.12, "i'm making", 'c', WC)]),
    (18.50, [(18.50, 'through my startup', 'c', WC)]),
    (19.14, [(19.14, 'and my content', 'c', WC)]),
    (19.78, [(19.78, 'and exactly where', 'c', WC)]),
    (20.70, [(20.70, "i'm spending", 'c', WC)]),
    (21.08, [(21.08, 'this money.', 'p', WP)]),
    # rory (punch-in)
    (t['rory'], [(t['rory'], 'rory', 'n back', C + 'top:232px'), (21.98, 'is my', 'c', CHEST)]),
    (22.34, [(22.34, 'nerd bot.', 'p back', ZP)]),
    # books (wide): frame slides right, stack on the left; then slides left, stack on the right
    (t['books'], [(t['books'], "she's making sure", 'c', WC)]),
    (SHIFT_R, [(SHIFT_R + .12, 'i read', 'c', LST + 'top:600px')]),
    (24.30, [(24.30, '26', 'h y', LST + 'top:520px'), (24.65, 'books', 'p w', LST + 'top:810px')]),
    (SHIFT_L, [(SHIFT_L + .05, 'by the', 'c', RST + 'top:560px'), (25.18, 'end', 'p w', RST + 'top:660px')]),
    (25.42, [(25.42, 'of', 'c', RST + 'top:500px'), (25.50, '20', 'h2 y', RST + 'top:590px'), (25.60, '26.', 'h2 y', RST + 'top:800px')]),
    # goodreads (punch-in)
    (t['goodreads'], [(t['goodreads'], 'has access', 'c', ZC)]),
    (26.60, [(26.60, 'to my goodreads', 'c y', ZC)]),
    (27.18, [(27.18, 'and gives', 'c', ZC)]),
    (27.52, [(27.52, 'the best book', 'c', ZC)]),
    (28.40, [(28.40, 'recommendations.', 'c y', ZC)]),
    # group chat (wide)
    (t['group'], [(t['group'], 'to make sure', 'c', WC)]),
    (30.00, [(30.00, "that i'm", 'c', WC)]),
    (31.32, [(31.32, 'on track,', 'p', WP)]),
    (31.84, [(31.84, 'i put all', 'c', WC)]),
    (32.30, [(32.30, 'of my bots', 'c', WC)]),
    (32.78, [(32.78, 'in a', 'c', WC)]),
    (33.06, [(33.06, 'group chat.', 'p', WP)]),
    # lock-in score (punch-in)
    (t['lockin'], [(t['lockin'], 'and every day', 'c', ZC)]),
    (34.18, [(34.18, 'they give me', 'c', ZC)]),
    (34.58, [(34.58, 'a daily', 'c', ZC)]),
    (34.90, [(34.90, 'lock-in score', 'c y', ZC)]),
    (35.46, [(35.46, 'based on how', 'c', ZC)]),
    (36.00, [(36.00, 'close i am', 'c', ZC)]),
    (36.62, [(36.62, 'to my', 'c', ZC)]),
    (36.88, [(36.88, 'goals.', 'p back', ZP)]),
    # cta (wide)
    (t['cta'], [(t['cta'], 'and if you', 'c', WC)]),
    (37.84, [(37.84, 'want to', 'c', WC)]),
    (38.14, [(38.14, 'lock in', 'n back y', WN)]),
    (38.44, [(38.44, 'with me,', 'c', WC)]),
    (38.82, [(38.82, 'comment', 'c', WC)]),
    (39.02, [(39.02, 'BOT', 'p', WP)]),
    (39.34, [(39.34, "and i'll send", 'c', WC)]),
    (39.72, [(39.72, 'you the link.', 'c', WC)]),
]
for _i, (_s, _els) in enumerate(CHUNKS):
    assert sum(len(x[1].split()) for x in _els) <= 3, _els


def dude_words():
    html, tw = [], []
    starts = [c[0] for c in CHUNKS] + [DUR]
    for g, (a, els) in enumerate(CHUNKS):
        b = starts[g + 1]
        for k, (tt, txt, cls, st) in enumerate(els):
            wid = f'w{g}-{k}'
            html.append(f'<div id="{wid}" class="dw {cls}" style="{st}">{txt}</div>')
            tw.append(f"gsap.set('#{wid}',{{autoAlpha:0}});")
            tw.append(f"tl.fromTo('#{wid}',{{autoAlpha:0,scale:1.22,filter:'blur(22px)'}},{{autoAlpha:1,scale:1,filter:'blur(0px)',"
                      f"duration:.2,ease:'power3.out',immediateRender:false}},{max(a, tt - .05):.3f});")
            if b < DUR - .01:
                tw.append(f"tl.to('#{wid}',{{autoAlpha:0,scale:.96,filter:'blur(16px)',duration:.1,ease:'power2.in'}},{b - .1:.3f});")
                tw.append(f"tl.set('#{wid}',{{autoAlpha:0}},{b:.3f});")
    return html, tw


def grades():
    """punch on every cut, then a slow push-in across the shot; the books shot slides right, then left"""
    tw = [f"gsap.set('.g',{{filter:'{BOLD_F}'}});"]
    order = sorted(T.items(), key=lambda kv: kv[1])
    for i, (k, c) in enumerate(order):
        n = order[i + 1][1] if i + 1 < len(order) else DUR
        tw.append(f"tl.set('#stage',{{x:0}},{c:.3f});")
        if k == 'books':
            tw += [f"tl.fromTo('#stage',{{scale:1.05}},{{scale:1,duration:.32,ease:'power2.out',immediateRender:false}},{c:.3f});",
                   f"tl.to('#stage',{{scale:1.3,x:150,duration:.5,ease:'power3.inOut'}},{SHIFT_R - .1:.3f});",
                   f"tl.to('#stage',{{x:-136,duration:.5,ease:'power3.inOut'}},{SHIFT_L - .1:.3f});"]
            continue
        if c > 0:
            tw.append(f"tl.fromTo('#stage',{{scale:1.06}},{{scale:1,duration:.3,ease:'power2.out',immediateRender:false}},{c:.3f});")
        tw.append(f"tl.fromTo('#stage',{{scale:1}},{{scale:1.045,duration:{n - c - .3:.3f},ease:'none',immediateRender:false}},{c + .3:.3f});")
    return tw


SFX = [('whoosh-short', .10, .22), ('pop', 1.70, .16), ('whoosh-short', T['tyler'], .2), ('pop', 12.28, .14),
       ('whoosh-short', T['sabrina'], .2), ('whoosh-short', T['rory'], .2),
       ('whoosh-short', SHIFT_R - .15, .26), ('pop', 24.30, .16), ('whoosh-short', SHIFT_L - .15, .26), ('pop', 25.40, .16),
       ('pop', 33.06, .14), ('pop', 34.90, .14)]   # nothing under the CTA: the voice stays clear
SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .3, 'click-soft': .37}
SFX_GAIN = 0.75


def audio():
    out, lanes = [], []
    for k, (name, tt, vol) in enumerate(sorted(SFX, key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - tt)
        lane = next((i for i, e in enumerate(lanes) if e <= tt), None)
        if lane is None:
            lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = tt + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{tt:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol * SFX_GAIN:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:58% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0}}
#cwin{{position:absolute;left:40px;top:230px;width:1000px;height:720px;z-index:2;filter:drop-shadow(0 30px 60px rgba(60,35,25,.35))}}
#cwin video{{width:1000px;height:720px;display:block}}
.dw.back{{z-index:3}}
#cutwrap{{position:absolute;inset:0;z-index:4}}
.orb{{position:absolute;left:0;top:0;width:{TW_}px;height:{TH_}px}}
.orb.b{{z-index:3;filter:brightness(.75)}}
.orb.f{{z-index:6}}
.pop{{width:100%;height:100%}}
.tile{{width:100%;height:100%;border-radius:28px;overflow:hidden;background:#111;border:5px solid rgba(255,248,239,.92);
  box-shadow:0 26px 60px rgba(0,0,0,.45),0 6px 16px rgba(0,0,0,.25)}}
.tile video{{width:100%;height:100%;object-fit:cover;display:block}}

/* opening creator cards */
.ccard{{position:absolute;z-index:8;width:260px}}
.ctile{{width:260px;height:462px;border-radius:30px;overflow:hidden;background:#111;border:5px solid #fff;box-shadow:0 30px 70px rgba(0,0,0,.5)}}
.ctile video{{width:100%;height:100%;object-fit:cover;display:block}}
.chandle{{margin:14px auto 0;width:max-content;max-width:330px;padding:8px 16px;border-radius:99px;background:rgba(10,10,12,.78);
  color:#fff;font:600 24px Inter;letter-spacing:-.2px}}

/* look overlays */
.fx{{position:absolute;inset:0;pointer-events:none}}
#dtone{{z-index:7;background:linear-gradient(180deg,rgba(20,55,75,.16),rgba(60,40,20,.08));mix-blend-mode:soft-light}}
#dvig{{z-index:7;background:radial-gradient(95% 62% at 50% 46%,rgba(0,0,0,0) 55%,rgba(0,0,0,.42) 100%)}}
#dgrad{{z-index:7;background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,.18) 22%,rgba(0,0,0,0) 34%,rgba(0,0,0,0) 58%,rgba(0,0,0,.30) 100%)}}
#gwarm{{z-index:7;background:linear-gradient(180deg,rgba(255,226,200,.10),rgba(255,196,170,.16));mix-blend-mode:soft-light}}
#gvig{{z-index:7;background:radial-gradient(120% 70% at 50% 45%,rgba(255,255,255,0) 52%,rgba(60,35,25,.34) 100%)}}
#ggrad{{z-index:7;background:linear-gradient(180deg,rgba(60,35,25,.30) 0%,rgba(60,35,25,0) 30%,rgba(60,35,25,0) 66%,rgba(40,24,18,.45) 100%)}}
#ktone{{z-index:7;background:linear-gradient(180deg,rgba(15,45,70,.30),rgba(10,20,35,.30));mix-blend-mode:soft-light}}
#kvig{{z-index:7;background:radial-gradient(80% 55% at 50% 44%,rgba(0,0,0,0) 40%,rgba(0,0,0,.5) 100%)}}
#kgrad{{z-index:7;background:linear-gradient(180deg,rgba(0,0,0,0) 66%,rgba(0,0,0,.38) 100%)}}

/* base type */
.dw{{position:absolute;z-index:8;color:#fff;font-family:'Inter Tight';font-weight:900;letter-spacing:-.05em;line-height:.9;
  text-shadow:0 8px 34px rgba(0,0,0,.6),0 2px 6px rgba(0,0,0,.55);transform-origin:50% 60%;white-space:nowrap}}
.sm{{font-size:84px;font-weight:800;letter-spacing:-.04em}}
.md{{font-size:150px}}
.big{{font-size:236px}}
.xl{{font-size:220px}}
.huge{{font-size:300px}}
.y{{color:{YEL}}}

/* cool girl type */
.gcap{{position:absolute;left:0;right:0;z-index:8;text-align:center;color:#FFF8EF;text-shadow:0 2px 26px rgba(60,30,20,.55)}}
.gcap .s{{font:500 64px Inter;letter-spacing:-1px}}
.gcap .e{{font:italic 400 200px 'Instrument Serif';line-height:.92;color:{YEL};margin:4px 0 8px}}
.gcap.low .e{{font-size:150px;white-space:nowrap}}
.gw{{display:inline-block}}
.spark{{position:absolute;z-index:8;color:{YEL};line-height:1;text-shadow:0 0 18px rgba(250,230,122,.5)}}

/* cool dude section: tracked caps + serif punch words */
.track{{position:absolute;left:70px;right:70px;z-index:8;text-align:center;color:#F2EFE9;font:500 34px Montserrat;
  text-shadow:0 2px 12px rgba(0,0,0,.6);white-space:nowrap}}
.track.spread{{display:flex;justify-content:space-between;right:110px}}
.track .tw{{display:inline-block;letter-spacing:.32em;margin:0 .1em;transform-origin:50% 50%}}
.serif{{position:absolute;left:0;right:0;z-index:8;text-align:center;color:#F7F4EE;font-family:'DM Serif Display';font-weight:400;
  line-height:1.12;letter-spacing:-.02em;white-space:nowrap;text-shadow:0 12px 40px rgba(0,0,0,.45)}}
.serif.it{{font-style:italic}}
.serif .mk{{display:inline-block;overflow:hidden;padding:0 .02em .14em;margin-bottom:-.14em;vertical-align:bottom}}
.serif .ch{{display:inline-block}}
#sweep{{z-index:7;mix-blend-mode:screen;background:linear-gradient(105deg,rgba(255,240,220,0) 38%,rgba(255,240,220,.22) 50%,rgba(255,240,220,0) 62%);
  background-size:260% 100%;background-repeat:no-repeat}}

/* skill.md card on "a well-written skill" */
/* scaled to .72 so the card ends above the y=1470 safe line */
#skillw{{position:absolute;left:110px;top:745px;width:860px;height:1000px;z-index:9;transform:perspective(1800px) rotateX(7deg) scale(.72);
  transform-origin:50% 0%;filter:drop-shadow(0 40px 80px rgba(0,0,0,.55))}}
#skillw video{{width:860px;height:1000px;display:block}}

/* cta instagram: scaled to .7 (532x700), sits under his chin and ends at the y=1470 safe line */
#igw{{position:absolute;left:274px;top:770px;width:760px;height:1000px;z-index:9;transform:scale(.7);transform-origin:0 0;
  filter:drop-shadow(0 40px 80px rgba(0,0,0,.55))}}
#igw video{{width:760px;height:1000px;display:block}}
.mds{{font-size:100px}}
.c{{font-size:100px;font-weight:900}}
.p{{font-size:170px;color:{YEL}}}
.p.w{{color:#fff}}
.n{{font-size:220px}}
.h{{font-size:300px;line-height:.85}}
.h2{{font-size:220px;line-height:.85}}
.sm2{{font-size:56px;font-weight:800;letter-spacing:-.03em}}
'''


# PY build.py --safe: draws the Instagram safe zone (red = UI covers it) for snapshot checks, never for renders
SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;width:35px;top:220px;height:1250px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:35px;top:220px;height:935px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:100px;top:1155px;height:315px;background:rgba(255,0,0,.28)"></div></div>')


def build():
    w_html, w_tw = dude_words()
    back = [h for h in w_html if 'back' in h.split('class="')[1].split('"')[0]]
    front = [h for h in w_html if h not in back]
    tweens = grades() + w_tw
    nl = '\n'
    return f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio())}
  <div id="stage">
    <video id="bgv" class="full g" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(back)}
    <div id="cutwrap"><video id="cut" class="full g" src="assets/subject.webm" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="1"></video></div>
  </div>
  <div id="dtone" class="fx dudefx"></div><div id="dvig" class="fx dudefx"></div><div id="dgrad" class="fx dudefx"></div>
{nl.join(front)}
{SAFE_GUIDE if SAFE else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tweens)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s  cuts {[round(c, 3) for c in CUTS]}')
