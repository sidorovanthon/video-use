---
name: reference-isolate-transcribe-helper
description: video-use repo has helpers/isolate_and_transcribe.py — sequential ElevenLabs voice-isolation + Scribe over a directory of source videos
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0a09b80d-e5f4-4418-aa75-ae91f8c33bd4
---

`helpers/isolate_and_transcribe.py` in the video-use repo runs sequential ElevenLabs Voice Isolation and/or Scribe transcription over every video newer than a named start file in a source directory.

Key behaviours:
- Output layout: `<out_root>/YYYY-MM-DD [stem]/` containing the moved source file, `isolated.mp3`, `transcript.json`. Date prefix is derived from source mtime.
- Dedups MP4+MKV pairs (prefers MP4).
- Skips date-named (`YYYY-MM-DD HH-MM-SS.*`) and `Desktop 20*` files — those are failed-take dumps.
- Resumable: each step checks for its output file and skips if cached. Safe to re-run.
- Source files are MOVED into their prep subfolder (not copied) — user explicitly asked for this.
- `--mode {transcribe,isolate,both}` — Phase 1 (transcribe-only) then Phase 2 (isolate-only) is the cheaper play if budget is tight, because Scribe is ~5× cheaper than the Voice Isolator.
- Writes per-file results to `<out_root>/processing_log.jsonl`.
- Stops cleanly on `quota_exceeded` / 402 / "insufficient" / "credit" / "quota" in the API error.

Usage:
```
uv run helpers/isolate_and_transcribe.py <src_dir> \
  --start "<stem of first file, no extension>" \
  --out-root <prep_dir> \
  --mode {transcribe|isolate|both}
```

Empirical cost on Creator plan (verified against `/v1/user/subscription` after a full 90.4-min batch):

- Voice Isolator: **661 cred/min** (from quota_exceeded error text — same rate confirmed by workspace math)
- Scribe v1: **20.15 cred/min exactly** (Creator plan), confirmed by two Scribe quota_exceeded API errors: "2651 cred for 131.5 min" → 20.16/min and "665 cred for 33.0 min" → 20.15/min. Use this rate for budgeting Doctor-School-style transcription batches.
- Combined full pipeline: **~709 cred/min**

API key needs **User → Read** scope for `/v1/user/subscription` to work; without it the script falls back to error-only credit detection.

**Per-API-key Monthly cap is in the same Credits unit as workspace** (confirmed via the dashboard "Edit API Key → Usage Limits (Credits) → Monthly" field). The cap counts cumulative usage on that key for the month; when it shows e.g. "32 credits remaining of 15,000" that means 14,968 have been spent on this key this month total, not in the current batch. So if you see a quota_exceeded surprise early in a fresh run, the likely cause is prior month-to-date usage on that key, not the current run's spend. Read `/v1/user/subscription` for workspace cumulative usage and the dashboard for per-key cap before starting a large batch.
