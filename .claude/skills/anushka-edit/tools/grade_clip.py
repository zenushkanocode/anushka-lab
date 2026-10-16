#!/usr/bin/env python3
"""Colour grade a D-Log M clip with one of the studio looks, optionally switching from log on a given frame.

Usage:
  PY grade_clip.py <in> <out.mp4> --look ghibli|dreamy [--switch 3.60] [--end 7.04] [--start 0]
                   [--glow 0.42] [--grain 5] [--sfx click-soft@3.50:0.55 sparkle@3.60:0.35 ...] [--fade-out 0.2]

--switch  keep the log footage before this time, graded after it (the "lens" effect). Omit to grade everything.
--glow    dreamy halation: blurred highlights screened on top (0 = off; 0.42 is the K-drama setting).
--grain   16mm-style luma grain strength (0 = off).
--sfx     name@time:volume, names from video-edit/assets/template/assets/sfx (click, click-soft, pop, sparkle,
          whoosh-short, impact-bass-1). Times are in the trimmed clip.
Writes an H.264 master (crf 14, Rec.709 tagged). Make shareable copies with deliver.sh.
"""
import argparse
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))
SFX_DIR = os.path.join(SKILLS, 'video-edit', 'assets', 'template', 'assets', 'sfx')

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--look', required=True, choices=['ghibli', 'dreamy'])
ap.add_argument('--switch', type=float, default=None)
ap.add_argument('--start', type=float, default=0.0)
ap.add_argument('--end', type=float, default=None)
ap.add_argument('--glow', type=float, default=None)
ap.add_argument('--grain', type=float, default=5)
ap.add_argument('--sfx', nargs='*', default=[])
ap.add_argument('--fade-out', type=float, default=0.0)
a = ap.parse_args()

lut = os.path.join(os.path.dirname(HERE), 'grades', f'{a.look}_dlogm.cube')
if not os.path.exists(lut):
    subprocess.run(['python3', os.path.join(os.path.dirname(HERE), 'grades', 'make_lut.py'), a.look, lut], check=True)
glow = a.glow if a.glow is not None else (0.42 if a.look == 'dreamy' else 0.0)
w, h = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', a.src],
                      capture_output=True, text=True).stdout.strip().split(',')[:2]
dur = (a.end if a.end else float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.src],
                                                capture_output=True, text=True).stdout)) - a.start
sw = a.switch if a.switch is not None else 0.0

g = f"lut3d=file='{lut}':interp=tetrahedral,format=gbrp"
if glow > 0:
    g += (f",split[base][hi];[hi]scale=iw/4:ih/4,curves=all='0/0 0.55/0 0.8/0.45 1/1',gblur=sigma=14,scale={w}:{h},format=gbrp[glow];"
          f"[base][glow]blend=all_mode=screen:all_opacity={glow},eq=saturation=1.02")
fc = (f"[0:v]format=gbrp16le,split[raw][gr];[gr]{g}[gd];[raw]format=gbrp[rw];"
      f"[rw][gd]blend=all_expr='if(gte(T,{sw}),B,A)',format=yuv420p")
if a.grain > 0:
    fc += f",noise=c0s={a.grain}:c0f=t+u:enable='gte(t,{sw})'"
fc += '[v];'
inputs, mix = ['-ss', str(a.start), '-t', f'{dur:.3f}', '-i', a.src], ['[0:a]']
for k, spec in enumerate(a.sfx, start=1):
    name, rest = spec.split('@'); t, vol = (rest.split(':') + ['0.4'])[:2]
    inputs += ['-i', os.path.join(SFX_DIR, name + '.mp3')]
    ms = int(float(t) * 1000)
    fc += f'[{k}:a]adelay={ms}|{ms},volume={vol}[s{k}];'
    mix.append(f'[s{k}]')
fc += f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0"
if a.fade_out > 0:
    fc += f',afade=t=out:st={dur - a.fade_out:.3f}:d={a.fade_out}'
fc += '[a]'
cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}',
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
       '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', a.out]
subprocess.run(cmd, check=True)
print('wrote', a.out)
