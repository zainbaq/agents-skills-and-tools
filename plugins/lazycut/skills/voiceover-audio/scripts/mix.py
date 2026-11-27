#!/usr/bin/env python3
"""Lay voiceover lines onto a video at exact start times and duck the original audio under them.
usage: mix.py VIDEO LINES.json VODIR OUT [--bed 0.5]
Video stream is copied untouched; only audio is rebuilt.
"""
import argparse, json, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("lines"); ap.add_argument("vodir"); ap.add_argument("out")
ap.add_argument("--bed", type=float, default=0.5, help="original audio level when nobody is speaking (0-1)")
a = ap.parse_args()
lines = json.load(open(a.lines))
cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.video]
parts, labels = [], []
COMP = "acompressor=threshold=-24dB:ratio=4:attack=3:release=100"
TARGET_DB = -16.0   # mean level every spoken line is brought to, so short and long lines sound equally loud

def mean_db(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", COMP + ",volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(re.search(r"mean_volume: ([-\d.]+) dB", r.stderr).group(1))

for i, ln in enumerate(lines, start=1):
    path = f"{a.vodir}/line_{ln['id']:02d}.wav"
    cmd += ["-i", path]
    ms = int(ln["t0"] * 1000)
    gain = TARGET_DB - mean_db(path)
    parts.append(f"[{i}:a]{COMP},volume={gain:.1f}dB,alimiter=limit=0.9,"
                 f"aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
    labels.append(f"[v{i}]")
n = len(lines)
graph = ";".join(parts) + (
    f";{''.join(labels)}amix=inputs={n}:normalize=0,apad[vo];"
    f"[vo]asplit[vo1][vo2];"
    # original audio drops while a line is spoken, recovers over 0.4 s after it
    f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={a.bed}[bed];"
    f"[bed][vo1]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400[duck];"
    f"[duck][vo2]amix=inputs=2:normalize=0:duration=first,volume=3dB,alimiter=limit=0.95[a]")
cmd += ["-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr[-2000:])
print(a.out)
