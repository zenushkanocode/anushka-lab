---
name: anushka-edit
description: "Anushka's video editing studio. Use for ANY video request from Anushka: editing a talking-head reel, colour grading a clip (D-Log M, Ghibli, dreamy K-drama look, lens switch), trimming, captions, sound design, or applying notes to an earlier version. Takes Google Drive links, uploads or local files, follows her house style from style/*.md unless she asks for something specific, and delivers phone + full-quality copies. Trigger on 'edit this', 'edit my reel', a Drive link to a video, 'colour grade', 'make it look like this reference', or /anushka-edit."
---

# Anushka's edit studio

Anushka directs; you edit. She points you at footage, maybe a style or a reference, and what she wants. Everything
she doesn't specify comes from her style files. Work end to end without asking unless something is genuinely
ambiguous (which clip, which look when none fits), then ask once, briefly.

`ST` = this skill's folder. `VE` = the engine skill next to it (`../video-edit`), which does the heavy lifting for
reels (ingest, takes, assemble, cutout, HyperFrames render, cut checks).

## 0. Every time, before touching footage
1. Read **every** `.md` in `ST/style/`. `house-style.md` is the default; any other file there overrides it where
   they disagree; her message in the chat overrides all of them.
2. Engine ready: if `VE/.platform.json` is missing or its `python` path doesn't exist, run
   `python3 "VE/scripts/setup.py"` (the session-start hook normally does this). `PY` = that python.
3. `VE/config.json` holds her name, handle and default look. It's committed, so no first-run questions.

## 1. Get the footage
- Google Drive link: `sh ST/tools/fetch_drive.sh "<link>" ~/Downloads <short-name>` (any size; the connector can't
  carry big videos). Several links: fetch each.
- Uploaded in chat or a local path: use it as is. Never modify originals.
- References: Pinterest / screenshots she pastes are images, look at them. YouTube: try
  `PY -m yt_dlp --js-runtimes node --extractor-args "youtube:player_client=android"` for the description,
  transcript (`--write-auto-subs --skip-download`) and storyboard frames (`-f sb0`); the video stream itself is
  usually blocked by YouTube's bot check, so say so and work from transcript + frames.
- Look before deciding: contact sheet (`ffmpeg -vf "fps=2,scale=480:-1,tile=5x4"`), `ffprobe` for format, log vs
  Rec.709 (D-Log M looks flat and grey; 10-bit HEVC from the Pocket 3 is usually log).

Blocked host? The environment's network allowlist needs: `drive.google.com`, `drive.usercontent.google.com`,
`huggingface.co`, `*.hf.co`, `youtube.com`, `www.youtube.com`, `*.googlevideo.com`, `i.ytimg.com`. Tell her the
exact host to add (environment menu > Edit > Network access > Custom > Allowed domains) and carry on with what
doesn't need it.

## 2. Pick the job

### A. Talking-head reel (she speaks to camera, wants a reel)
Follow `VE/SKILL.md` steps 1-8, with these studio rules on top:
1. After writing `edl.json`, run `PY ST/tools/find_repeats.py <project>` and move any `in` past repeated starts.
   Do this BEFORE assemble + cutout (the cutout takes ~10 min on CPU; redoing it costs a lot).
2. Frame punch-ins from a test frame first (measure her face position) before the cutout runs.
3. Build from `ST/tools/reel_template.py` instead of the engine's template: it already has the house style
   (3-word CHUNKS, wall-space placement, push-ins, slide-and-stack, no SFX under CTA, local GSAP). Copy it to the
   project as `build.py`, keep `grades()` / `dude_words()` / `audio()`, rewrite `CHUNKS`, `SHIFT_R/SHIFT_L`, `SFX`.
   It needs `assets/vendor/gsap.min.js`: copy `ST/tools/vendor/gsap.min.js` (the session hook fetches it; if it's
   missing: `npm pack gsap@3` and take `package/dist/gsap.min.js`).
4. Snapshot with the safe guide, fix, render, `check_cuts.py`, then deliver.

### B. Colour grade / cinematic clip
1. Find any switch moment (lens, hand over camera): `python3 ST/tools/find_switch.py <clip> <from> <to>`.
2. Pick the look from her request or style files (`ghibli` or `dreamy`, see `ST/grades/README.md`). A new
   reference: add a preset to `ST/grades/make_lut.py`, test on 2-3 stills side by side
   (`ffmpeg ... -vf "split[a][b];[b]lut3d=...[g];[a][g]hstack"`), iterate, then commit the new preset.
3. Render: `PY ST/tools/grade_clip.py <in> <out> --look <name> [--switch t] [--end t] [--glow x] [--sfx ...]`.
4. Check the switch frames and a 100% crop for grain before delivering.

### C. Both
Grade the source first with grade_clip.py (no switch), then run it through A as the clip.

## 3. Deliver
- `sh ST/tools/deliver.sh <master> <scratchpad-dir>` makes a full-res copy under 30 MB (+ 720p phone copy for
  vertical). Send both with SendUserFile. Keep masters in `~/reel-edits/<project>/renders/`.
- Report in plain words: what changed, anything that needs her call. No jargon dumps.

## 4. Notes and memory
- Every round of notes: apply exactly what she asked, re-render, re-deliver as vN+1.
- If a note is a general preference ("never more than 3 words", "no SFX under the CTA"), add it to
  `ST/style/house-style.md` under "Learned from feedback", commit and push it, so every future edit follows it.
- New looks, presets or tool fixes: commit them too. The studio should get better with every video.
