#!/usr/bin/env python3
"""Sample a video into timestamped contact sheets + a motion track.
usage: analyze.py VIDEO OUTDIR [--start S --end E --fps F] [--zoom T X Y W H]
"""
import argparse, json, os, re, subprocess, sys

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(src):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", src])
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = v["r_frame_rate"].split("/")
    return {"duration": float(j["format"]["duration"]), "width": v["width"], "height": v["height"],
            "fps": round(float(num) / float(den), 2), "has_audio": a is not None,
            "size_mb": round(int(j["format"]["size"]) / 1e6, 1)}

def sheets(src, out, start, end, fps, cols=4, rows=3, width=640):
    # timestamps are burned in as absolute source time
    vf = (f"fps={fps},scale={width}:-1,"
          f"drawtext=text='%{{pts\\:hms\\:{start}}}':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.7,"
          f"tile={cols}x{rows}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-to", str(end), "-i", src,
         "-vf", vf, os.path.join(out, "sheet_%02d.jpg")])
    return sorted(f for f in os.listdir(out) if f.startswith("sheet_"))

def motion(src, start, end, bucket=0.5):
    # scene score per frame on a small proxy -> mean per bucket, robust-normalised 0..1
    r = run(["ffmpeg", "-v", "error", "-ss", str(start), "-to", str(end), "-i", src, "-an",
             "-vf", "scale=320:-1,select='gte(scene,0)',metadata=print:file=-", "-f", "null", "-"])
    t, acc = None, {}
    for line in r.stdout.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            t = float(m.group(1))
        m = re.search(r"scene_score=([\d.]+)", line)
        if m and t is not None:
            acc.setdefault(int(t / bucket), []).append(float(m.group(1)))
    if not acc:
        return [], []
    means = {k: sum(v) / len(v) for k, v in acc.items()}
    srt = sorted(means.values())
    p95 = srt[min(len(srt) - 1, int(len(srt) * 0.95))] or 1e-6
    track = [{"t": round(start + k * bucket, 1), "score": round(min(1, means[k] / p95), 2)} for k in sorted(means)]
    dead, run_start = [], None
    for s in track + [{"t": track[-1]["t"] + bucket, "score": 1}]:
        if s["score"] < 0.08:
            run_start = s["t"] if run_start is None else run_start
        else:
            if run_start is not None and s["t"] - run_start >= 1.0:
                dead.append([run_start, s["t"]])
            run_start = None
    return track, dead

def loudness(src):
    r = run(["ffmpeg", "-hide_banner", "-i", src, "-vn", "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume: ([-\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--zoom", nargs=5, metavar=("T", "X", "Y", "W", "H"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    info = probe(a.src)
    if a.zoom:  # one enlarged crop for reading HUD text
        t, x, y, w, h = a.zoom
        dst = os.path.join(a.out, f"zoom_{float(t):07.2f}.jpg")
        run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", a.src, "-frames:v", "1", "-update", "1",
             "-vf", f"crop={w}:{h}:{x}:{y},scale=1400:-1", dst])
        print(dst); sys.exit()
    end = a.end or info["duration"]
    span = end - a.start
    fps = a.fps or min(2.0, max(0.1, 144 / span))  # cap a pass at ~144 frames (12 sheets)
    files = sheets(a.src, a.out, a.start, end, fps)
    track, dead = motion(a.src, a.start, end)
    info.update({"window": [a.start, end], "sample_fps": round(fps, 3), "sheets": files,
                 "mean_volume_db": loudness(a.src) if info["has_audio"] else None,
                 "dead_time": dead, "motion": track})
    json.dump(info, open(os.path.join(a.out, "analysis.json"), "w"))
    print(json.dumps({k: v for k, v in info.items() if k != "motion"}, indent=1))
