---
name: feedback_srt_stutter_token
description: "A stutter/false-start token (e.g. 'f-') that Scribe timestamps just inside a kept segment's start window produces a phantom subtitle cue even when the audible stutter is before the cut and absent from the rendered audio — filter the token from an SRT-build transcript COPY, never edit the cached JSON."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46b25452-23e9-41f2-9456-0d50ffec27fe
---

When a segment starts mid-flow to drop a stutter/false-start (e.g. cut from the clean "And" and drop the leading "f-"), Scribe may have timestamped that stutter token (`"f-"`) at a time that falls **inside** the kept `[start,end]` window even though the audible sound is before the cut. `build_master_srt` reads the transcript by word time, so it emits a phantom cue like `"F- AND"` for audio that has no "f-".

**Why:** Observed 2026-06-09, edit-10. seg started at 252.00; clean "And" at 252.05; the "f-" stutter was tagged 252.04–252.05 (degenerate near-zero duration, real sound was ~251.7 on the waveform, before 252.00). The 2-word chunker grouped `f- And` → cue "F- AND".

**How to apply:** rebuild `master.srt` from a **filtered copy** of the transcript (drop tokens whose `text.strip().lower()` is the stutter, e.g. `"f-"`, plus ellipsis `...` and any trailing-hyphen token) written to a temp `transcripts/` dir, then call `build_master_srt(edl, tmp_dir, out)` and re-apply any script-correction `str.replace`s. **Never edit the cached `transcripts/S0.json`** — keep it immutable (see [[feedback_premade_isolated_audio]]). Pairs with the OBS recipe [[reference_video_use_settings]] subtitles section.

**CAUTION — the SRT filter does NOT fix audible leaks (edit-12, 2026-06-15):** filtering the token only cleans the *subtitle*. If the false-start fragment's audio falls inside the kept window (e.g. a segment tail pad of +0.08 reaching past `enough.` into the next take's `How` onset at 94.877 → 42 ms of audible "H-"), the listener hears a real stutter ("H-How"). That must be fixed in the **EDL/audio** by tightening the segment edge to stop *before* the fragment's RMS onset — removing the SRT token alone leaves the stutter in the render. Always check whether a flagged "duplicate word" is an audio leak (trim the EDL) vs a transcript artifact (filter the SRT).
