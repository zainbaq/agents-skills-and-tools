---
name: voiceover-audio
description: "Generates AI voice audio from a timed script, places each line at its start time on a video, and ducks the original audio underneath. Use when a voiceover, AI voice, or narration audio is wanted, or when a script has to be lined up with a video."
---

# Voiceover audio

**Rules that always hold:**

- You cannot hear audio. Every check here is by measurement or transcription. Always tell the user to listen once for tone and pronunciation.
- A connected voice service costs credits. Quote the cost first.
- Only voice a script the user has approved.
- For a line that runs over its slot, shorten the line first; only then try `--speed 1.1`. Never push speed past 1.15.
- If the workspace is refused a download from a voice service, do not retry by another route.

Turn an approved script into speech and mix it onto a rendered clip.

## Inputs

- **Clip path** (required): the rendered video from video-editor.
- **Lines JSON path** (required): `lines.json` from voiceover-script, in the form `[{"id": 1, "t0": 0.2, "slot": 3.6, "text": "..."}]`.
- **Output folder** (required from a caller; default `lazycut-out/voiceover/<clip name>/` in the working directory).
- **Voice** (optional): a voice name. If the user has a preferred voice on record, use it without asking. Default `am_michael`.
- **Requirements**:
  - `ffmpeg` on the path, for both routes.
  - Route A: Python 3 with `kokoro-onnx`, `soundfile`, and `numpy` (pip packages), plus the Kokoro model files (about 350 MB, downloaded in setup).
  - Route B: a connected voice service, and `faster-whisper` where installed.

## Process

Run the scripts by path, relative to this skill's folder. Run them; do not read them into context.

### Choose the voice route

**Route A: local voice (default).** Kokoro, an open text-to-speech model, runs inside the workspace. Free, no credits, and the video never leaves the workspace. Sounds decent but more synthetic than a premium voice.

**Route B: a connected voice service** (for example Higgsfield voices). Use when the user names a voice from that service or asks for the better voice. It costs credits, so quote the cost first. The workspace usually cannot download from or upload to that service, so the mix has to happen in the service's own sandbox. See Route B below.

### Route A: local

Setup, once per session:
```bash
pip install --break-system-packages -q kokoro-onnx soundfile
mkdir -p tts && cd tts
curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

Voices: American male `am_michael` (default), `am_adam`, `am_eric`, `am_liam`, `am_onyx`, `am_fenrir`, `am_puck`, `am_echo`; American female `af_heart`, `af_bella`, `af_nova`, `af_sarah`, `af_sky`; British `bm_george`, `bm_daniel`, `bm_lewis`, `bf_emma`, `bf_alice`.

Generate one file per line:
```bash
python3 scripts/voice.py lines.json vo --voice am_michael --models tts
```
It prints each line's length against its slot and exits non-zero if any line runs over. For a line that runs over, shorten the line first; only then try `--speed 1.1`. Never push speed past 1.15.

### Mix

```bash
python3 scripts/mix.py clip.mp4 lines.json vo clip_voiceover.mp4
```
- Each line is levelled to the same loudness, so short and long lines match.
- The original audio plays at half volume (`--bed 0.5`) and dips further under each line. Use `--bed 0.3` for busy game audio, `--bed 0` to remove it.
- The video stream is copied untouched.

### Verify

Print a half-second loudness trace and confirm speech begins at each `t0` and the bed drops under it:
```bash
ffmpeg -hide_banner -i clip_voiceover.mp4 -vn -af "asetnsamples=24000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - 2>/dev/null | grep RMS_level | cut -d= -f2 | awk '{printf "%.1f:%.0f ", (NR-1)/2, $1}'
```
Speech windows should sit around -13 to -18 dB and the bed around -20 to -24 dB. Report what you measured, then send the file.

### Route B: connected voice service

1. Quote the cost, then generate the WHOLE script as one take: one prompt, lines separated by blank lines. A single take keeps the delivery consistent, and services often limit concurrent jobs or fail on very short prompts.
2. Test whether the workspace can download the result URL. If the request is refused, do not retry by another route. Do the rest in the service's sandbox:
   - Ask the user to upload the source video through the service's upload widget, called as the only tool in that step.
   - Recreate `../video-editor/scripts/render.py` and `scripts/mix.py` there, download the video and the take, and run render, mix, and upload in one background command. Request the upload URL before starting it.
3. Split the take into lines. Find gaps with `silencedetect=noise=-35dB:d=0.25`, then transcribe with word timestamps (faster-whisper, where installed) to map gaps to lines.
4. Check for glitches. Synthetic takes sometimes stumble and repeat a line. Compare the transcript to the script, cut any false start, and keep the clean attempt.
5. Cut each line to `vo/line_NN.wav` with 0.03 s before and 0.08 s after, transcribe each cut file, and confirm it matches the script and fits its slot.
6. Mix and verify as above. Deliver the link the service returns, and say the file is in the service's media library.

Tell the user which domains to allow in their Claude settings if they want the workspace to reach the service directly next time.

## Outputs

Written to the output folder, with each path reported back:

- `clip_voiceover.mp4`: the clip with the voiceover mixed in. On Route B, the link the service returns.
- `vo/line_NN.wav`: one file per line. Keep these; a change to one line only needs that line regenerated and a re-mix.

In the reply, report the measured loudness, send the file, and tell the user to listen once for tone and pronunciation.

## Notes

- If the video has no audio track, `mix.py` fails on the bed. Add a silent track first with `ffmpeg -i clip.mp4 -f lavfi -i anullsrc -shortest -c:v copy -c:a aac clip_a.mp4`.
- The local voice model is about 350 MB and is re-downloaded each new session.
