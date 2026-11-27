#!/usr/bin/env python3
"""Render one uncut range as a vertical (or original-shape) clip with burned-in text.
usage: render.py PLAN.json

PLAN = {
  "source": "in.mov", "out": "out.mp4",
  "start": 0.0, "end": 48.8,            # ONE continuous range. Never more than one.
  "layout": "fit" | "crop" | "none",   # fit = whole frame over blurred fill; crop = fill 9:16; none = keep shape
  "screen": [x, y, w, h],               # optional pre-crop of the source (e.g. to drop borders)
  "focus_x": 0.5,                       # crop / fg_aspect: horizontal centre of the kept window, 0..1
  "fg_aspect": 1.333,                   # fit layout only: trim the sides to this shape so footage is bigger (omit = keep shape)
  "captions": [{"t0": 0, "t1": 3, "text": "...", "pos": "top|center|bottom", "color": "white|gold"}]
}
Caption times are seconds from the START OF THE OUTPUT clip.
"""
import glob, json, os, re, subprocess, sys, tempfile
from PIL import ImageFont

W, H = 1080, 1920
TOP, BOTTOM = 0.12, 0.15           # vertical safe margins (platform UI)
COLORS = {"white": "white", "gold": "#F2C230"}

def ffpath(path):  # make a path safe inside an ffmpeg filter option (Windows drive colons, backslashes)
    return path.replace("\\", "/").replace(":", "\\:")

def find_font():
    if os.name == "nt":  # fixed font folders: a recursive search of the whole home folder is too slow on Windows
        home = os.path.expanduser("~")
        dirs = (os.path.join(home, "fonts"), os.path.join(home, "AppData", "Local", "Microsoft", "Windows", "Fonts"),
                r"C:\Windows\Fonts")
        for name in ("Anton-Regular.ttf", "Poppins-Bold.ttf", "Montserrat-ExtraBold.ttf", "DejaVuSans-Bold.ttf",
                     "impact.ttf", "arialbd.ttf"):
            for d in dirs:
                if os.path.exists(os.path.join(d, name)):
                    return os.path.join(d, name)
        sys.exit("no bold font found")
    for pat in ("**/Anton-Regular.ttf", "**/Poppins-Bold.ttf", "**/Montserrat-ExtraBold.ttf", "**/DejaVuSans-Bold.ttf"):
        for root in (os.path.expanduser("~"), "/usr/share/fonts"):
            hit = glob.glob(os.path.join(root, pat), recursive=True)
            if hit:
                return hit[0]
    sys.exit("no bold font found")

def wrap(text, font, max_w):
    # fewest lines that fit, then the split with the narrowest widest line (no orphan words)
    words = text.split()
    best = None
    def rec(i, lines):
        nonlocal best
        if best and len(lines) > len(best):
            return
        if i == len(words):
            key = (len(lines), max(font.getlength(l) for l in lines))
            if best is None or key < (len(best), max(font.getlength(l) for l in best)):
                best = list(lines)
            return
        for j in range(i + 1, len(words) + 1):
            line = " ".join(words[i:j])
            if font.getlength(line) > max_w and j > i + 1:
                break
            rec(j, lines + [line])
    rec(0, [])
    return best

def clean(text):  # caption fonts have no emoji glyphs: drop them rather than render boxes
    return re.sub(r"[^\x20-\x7E -ɏ‐-‧]", "", text).strip()

def main(plan_path):
    p = json.load(open(plan_path))
    layout = p.get("layout", "fit")
    dur = p["end"] - p["start"]
    fontfile = find_font()
    tmp = tempfile.mkdtemp()
    pre = "crop={2}:{3}:{0}:{1},".format(*p["screen"]) if p.get("screen") else ""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height", "-of", "csv=p=0", p["source"]], capture_output=True, text=True)
    sw, sh = (p["screen"][2], p["screen"][3]) if p.get("screen") else map(int, probe.stdout.strip().split(",")[:2])
    fg_h = 0

    if layout == "none":
        cw, ch = sw, sh
        chain = f"[0:v]{pre}setsar=1[base]"
        band = {"top": int(ch * 0.06), "bottom": int(ch * 0.94)}
    elif layout == "crop":
        cw, ch = W, H
        fx = p.get("focus_x", 0.5)
        chain = (f"[0:v]{pre}scale=-2:{H},crop={W}:{H}:'min(max(iw*{fx}-{W}/2,0),iw-{W})':0,setsar=1[base]")
        band = {"top": int(H * TOP) + 20, "bottom": int(H * (1 - BOTTOM)) - 20}
    else:  # fit
        cw, ch = W, H
        asp = min(p.get("fg_aspect") or sw / sh, sw / sh)
        fx = p.get("focus_x", 0.5)
        kw = int(sh * asp) // 2 * 2
        trim = f"crop={kw}:{sh}:'min(max(iw*{fx}-{kw}/2,0),iw-{kw})':0," if kw < sw else ""
        fg_h = int(W / asp) // 2 * 2
        chain = (f"[0:v]{pre}split[a][b];"
                 f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:4,eq=brightness=-0.4[bg];"
                 f"[b]{trim}scale={W}:{fg_h}[fg];[bg][fg]overlay=0:(H-h)/2,setsar=1[base]")
        # text sits in the blurred bands above / below the footage, never over gameplay
        band = {"top": int(H * TOP) + 20, "bottom": int(H * (1 - BOTTOM)) - 20}

    size = int(cw * 0.078)
    font = ImageFont.truetype(fontfile, size)
    lh = int(size * 1.22)
    draws = []
    for i, c in enumerate(p.get("captions", [])):
        lines = wrap(clean(c["text"]), font, cw * 0.88)
        block = lh * len(lines)
        pos = c.get("pos", "top")
        if pos == "top":
            y0 = band["top"]
            if layout == "fit":  # bottom-align the block against the footage edge
                y0 = max(y0, int((H - fg_h) / 2) - block - 40)
        elif pos == "bottom":
            y0 = band["bottom"] - block
            if layout == "fit":
                y0 = min(y0, int((H + fg_h) / 2) + 40)
        else:
            y0 = int((ch - block) / 2)
        t0, t1 = max(0, c["t0"]), min(dur, c["t1"])
        for j, line in enumerate(lines):
            tf = os.path.join(tmp, f"c{i}_{j}.txt")
            open(tf, "w").write(line)
            draws.append(
                f"drawtext=fontfile='{ffpath(fontfile)}':textfile='{ffpath(tf)}':fontsize={size}:"
                f"fontcolor={COLORS.get(c.get('color', 'white'), 'white')}:borderw={max(4, size // 10)}:bordercolor=black:"
                f"x=(w-text_w)/2:y={y0 + j * lh}:enable='between(t,{t0},{t1})':"
                f"alpha='min(1,(t-{t0})/0.15)'")
    graph = chain + (";[base]" + ",".join(draws) + "[v]" if draws else ";[base]null[v]")
    gf = os.path.join(tmp, "graph.txt")
    open(gf, "w").write(graph)
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(p["start"]), "-to", str(p["end"]), "-i", p["source"],
           "-filter_complex_script", gf, "-map", "[v]", "-map", "0:a?", "-r", "30",
           "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", p["out"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode and "filter_complex_script" in r.stderr:  # newer ffmpeg dropped this option: load the file with -/filter_complex
        cmd[cmd.index("-filter_complex_script")] = "-/filter_complex"
        r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    print(p["out"], f"{dur:.1f}s", f"{os.path.getsize(p['out']) / 1e6:.1f} MB", "font:", os.path.basename(fontfile))

if __name__ == "__main__":
    main(sys.argv[1])
