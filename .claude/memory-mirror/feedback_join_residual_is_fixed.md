---
name: feedback-join-residual-is-fixed
description: The retained join silence is a FIXED 0.16s (pads +0.10/-0.06) regardless of gap width; scaling pads by gap width inverts the rule, and source-time arithmetic cannot verify a residual
metadata:
  type: feedback
---

The Phase 3 pads are **absolute, not proportional**: segment END = `silence_start
+ 0.10`, segment START = `silence_end − 0.06`, so the silence RETAINED at every
join is **0.16 s for every gap**, and the amount REMOVED is `w − 0.16`, which
grows with the gap. Do not "improve" this by scaling the pads to hit a target.

edit-41: I rewrote the pads as `((w−0.15)*0.625, (w−0.15)*0.375)` intending a
0.15 s residual. That formula makes `pe + pst = w − 0.15`, so it retains `w−0.15`
and removes a fixed 0.15 — the inverse of the intent. A 0.438 s gap kept 0.288 s.

**Why I did not catch it in the EDL:** I printed `range[i].start −
range[i−1].end` as the "residual". In SOURCE time that difference is the amount
**removed**, not what remains — the two segments are adjacent in the OUTPUT, so
the retained silence is the sum of the two pads and is not visible anywhere in
the source-time table. The wrong number (0.223 / 0.238 / 0.278) even looked like
a plausible defect and triggered the "fix".

**How to apply:** never compute a join residual from EDL arithmetic — render and
measure it with `silencedetect` on `base.mp4` (pre-loudnorm, per
[[feedback_loudnorm_shifts_silence_threshold]]), mapping each expected join to
the nearest event. Only re-place an edge when that MEASURED width is off, which
is the same discipline [[feedback_silence_start_lags_speech_end]] and
[[feedback_join_offsets_from_silencedetect]] already demand.
