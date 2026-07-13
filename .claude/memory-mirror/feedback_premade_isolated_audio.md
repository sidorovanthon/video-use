---
name: feedback_premade_isolated_audio
description: "When user supplies pre-made isolated.mp3 + transcript.json, mux the clean audio into the video and cut from that"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dd7b75dd-bf5a-46a5-9f79-aaca7222d320
---

When the user drops a pre-cleaned `isolated.mp3` (ElevenLabs voice isolation) and a
`transcript.json` (Scribe) next to the source MP4, do NOT re-run isolation or
transcription — they are immutable outputs of immutable inputs.

**Why:** isolation/Scribe cost money and time; re-running also risks drifting timestamps
the user already relies on.

**How to apply:** verify `isolated.mp3` duration ≈ video duration (time-aligned), then mux
it over the video stream copied losslessly: `ffmpeg -i video.mp4 -i isolated.mp3 -map 0:v:0
-map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest source_clean.mp4`. Point the EDL `sources`
at `source_clean.mp4` so per-segment extracts pull the denoised track; render.py's two-pass
loudnorm then levels it. Note the result is mono if isolated.mp3 is mono. Copy the transcript
to `transcripts/<source_key>.json` for build_master_srt. See [[reference_isolate_transcribe_helper]],
[[reference_video_use_settings]].
