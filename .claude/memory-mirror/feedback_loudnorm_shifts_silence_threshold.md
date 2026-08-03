---
name: feedback_loudnorm_shifts_silence_threshold
description: "Phase 6 join/onset gates run on the NORMALIZED final.mp4, where loudnorm has already added ~+10 dB — probing it at -35dB reports phantom 'no silence at this join'"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9deb673e-40f2-4dfd-86b1-867436a38dfc
  modified: 2026-08-03T02:57:09.313Z
---

`render.py` ends with a two-pass loudnorm to −14 LUFS. On edit-35 the pre-norm
measurement was **I = −23.75 LUFS**, so the whole track — including the room
tone inside every trimmed join — was lifted by **≈ +9.7 dB** before `final.mp4`
was written.

The Phase 6 verification numbers in `SKILL.md` (`silencedetect=noise=-35dB`,
onset "clean ≤ −35 dB / clipped hotter than −25 dB") are **source-side**
thresholds, calibrated on `source_clean.mp4`. Applied unchanged to `final.mp4`
they mis-read:

- `silencedetect -35dB` on edit-35's output found **no event at all** at 3 of
  the 11 joins — including the two whose source gaps had been probed and
  confirmed as real silence. The joins were fine; the risen noise floor simply
  never crossed −35 dB. Re-running at **−26 dB** surfaced all 11.
- The same offset applies to the onset gate: measured onsets ran −30 to −50 dB
  in the output, which would look "hot" against a −35 dB pass criterion while
  actually corresponding to −40 … −60 dB at the source.

**Why:** a missing `silence_start` at a join reads exactly like a defect ("the
cut has no gap"), and the reflex is to re-place the cut. Chasing that on a
correct edit wastes a re-render — the same failure shape as
[[reference_ffmpeg_filter_loglevel]], where `-v error` made a working
measurement look empty.

**How to apply:** read the loudnorm pass-1 line that `render.py` prints
(`measured: I=…`), take `gain = -14 − I`, and shift BOTH output-side thresholds
by it — for edit-35, −35 → −26 dB for `silencedetect` and −35 → −25 dB for the
onset pass. Alternatively run the gates on `final.prenorm.mp4`, which is still
at source level. Compare onset values against each other and against the
segment's own source probe, never against a bare absolute number.

Related: [[feedback_silencedetect_subword_edges]],
[[reference_ffmpeg_filter_loglevel]]
