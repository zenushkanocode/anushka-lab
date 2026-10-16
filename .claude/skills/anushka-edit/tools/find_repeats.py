#!/usr/bin/env python3
"""Find restarts inside chosen takes ("each bot... each bot... each bot has a specific goal").

Whisper on a whole segment merges repeated starts into one line, so this splits every EDL segment at its tiny
pauses (silencedetect -35dB, 80ms) and transcribes each piece on its own with medium.en. If a segment shows the same
opening twice, move its "in" to the pause before the last clean start.

Usage: PY find_repeats.py <project_dir>      (needs sources.json + edl.json from the video-edit workflow)
"""
import json
import os
import subprocess
import sys
import tempfile

from faster_whisper import WhisperModel

proj = sys.argv[1]
src = json.load(open(os.path.join(proj, 'sources.json')))
edl = json.load(open(os.path.join(proj, 'edl.json')))
m = WhisperModel('medium.en', device='cpu', compute_type='int8')
wav = os.path.join(tempfile.mkdtemp(), 'c.wav')
for s in edl:
    f, a, b = src[s['clip']], s['in'], s['out']
    err = subprocess.run(['ffmpeg', '-hide_banner', '-ss', str(a), '-to', str(b), '-i', f, '-vn', '-af',
                          'silencedetect=n=-35dB:d=0.08', '-f', 'null', '-'], capture_output=True, text=True).stderr
    marks = []
    for line in err.splitlines():
        if 'silence_start' in line:
            marks.append(('s', a + float(line.split('silence_start: ')[1])))
        if 'silence_end' in line:
            marks.append(('e', a + float(line.split('silence_end: ')[1].split(' ')[0])))
    cuts = [a] + [(x + y) / 2 for (k1, x), (k2, y) in zip(marks, marks[1:]) if k1 == 's' and k2 == 'e'] + [b]
    print('##', s['id'])
    for x, y in zip(cuts, cuts[1:]):
        if y - x < .25:
            continue
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(x), '-to', str(y), '-i', f, '-ac', '1', '-ar', '16000', wav])
        segs, _ = m.transcribe(wav, condition_on_previous_text=False, vad_filter=False, beam_size=5)
        print(f'  {x:7.2f}-{y:7.2f}  ' + ' '.join(t.text.strip() for t in segs))
