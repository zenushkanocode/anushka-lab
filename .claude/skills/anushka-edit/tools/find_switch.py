#!/usr/bin/env python3
"""Find the frame to switch looks on: the darkest moment of a lens / hand / object covering the camera.

Usage: python3 find_switch.py <clip> <from_s> <to_s>
Prints frame-by-frame mean brightness and the darkest time. Switch the grade on that frame: the cover hides the cut.
"""
import subprocess
import sys

clip, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
fps = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', clip],
                     capture_output=True, text=True).stdout.strip().split('/')
fps = float(fps[0]) / float(fps[1]) if len(fps) == 2 else float(fps[0])
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', clip, '-vf', 'scale=96:54,format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True).stdout
n = 96 * 54
vals = [sum(raw[i:i + n]) / n for i in range(0, len(raw) - n + 1, n)]
for k, v in enumerate(vals):
    print(f'{a + k / fps:7.3f}  {v:6.1f}  ' + '#' * int(v / 4))
k = min(range(len(vals)), key=vals.__getitem__)
print(f'darkest: {a + k / fps:.3f}s')
