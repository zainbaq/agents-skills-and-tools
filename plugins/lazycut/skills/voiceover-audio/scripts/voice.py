#!/usr/bin/env python3
"""Generate one WAV per voiceover line with Kokoro (local TTS).
usage: voice.py LINES.json OUTDIR [--voice am_michael] [--speed 1.0] [--models tts]
LINES = [{"id": 1, "t0": 0.2, "slot": 3.6, "text": "..."}]   t0 = start in the video, slot = seconds available
Prints each line's duration and whether it fits its slot.
"""
import argparse, json, os, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ap = argparse.ArgumentParser()
ap.add_argument("lines"); ap.add_argument("out")
ap.add_argument("--voice", default="am_michael"); ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--models", default="tts", help="folder holding kokoro-v1.0.onnx and voices-v1.0.bin")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
k = Kokoro(os.path.join(a.models, "kokoro-v1.0.onnx"), os.path.join(a.models, "voices-v1.0.bin"))
ok = True
for ln in json.load(open(a.lines)):
    audio, sr = k.create(ln["text"], voice=a.voice, speed=a.speed, lang="en-us")
    # trim leading/trailing silence so the line starts exactly at t0
    idx = np.where(np.abs(audio) > 0.01)[0]
    audio = audio[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.08 * sr)] if len(idx) else audio
    path = os.path.join(a.out, f"line_{ln['id']:02d}.wav")
    sf.write(path, audio, sr)
    dur = len(audio) / sr
    fits = dur <= ln["slot"]
    ok &= fits
    print(f"{ln['id']:2d} {dur:5.2f}s / slot {ln['slot']:.1f}s {'ok ' if fits else 'OVER'} {ln['text']}")
sys.exit(0 if ok else 2)
