---
name: feedback-silence-start-lags-speech-end
description: "silencedetect's silence_start can fire ~0.09s AFTER speech actually stops, so the silence_start+0.10 pad silently leaves a 0.28s join instead of the designed 0.16s — measure join width in the render, not just at cut time"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: aed6c520-39f9-4b3f-8496-dd4eb5b3c5d8
  modified: 2026-08-17T04:27:06.749Z
---

Phase 3 places a segment END at `silence_start + 0.10` and the next START at
`silence_end − 0.06`, which is supposed to leave a **0.16 s** residual at the join.
That arithmetic is only as good as `silence_start`, and on edit-40 it was **0.09 s
late**: at the `agent.` → `The script` join, an RMS probe showed the tail crossing
−35 dB at ~149.62 and reaching −50 dB by 149.635, while `silencedetect` reported
`silence_start: 149.713`. The pads then trimmed 0.16 s out of a 0.49 s
speech-free window and shipped a **0.284 s** pause. The same thing, smaller, hit
the `everyone else.` → `But only the admin` join (0.250 s).

**Why:** `silencedetect` integrates over a window before declaring silence, so its
`silence_start` is a lagging indicator of where the speech energy actually ended —
the opposite bias from [[feedback-silencedetect-subword-edges]], where it fires too
EARLY inside a quiet word tail. Both biases exist in the same file. Because the pad
is a constant added to a drifting anchor, the error passes straight through to the
output, and nothing at cut time reveals it — the EDL looks correct. The user has
flagged preserved pauses as a defect before ([[feedback-trim-pauses-tight]], edit-24
was recut for it), so a silent +0.12 s inflation on every long gap is a real risk.

**How to apply:** treat the designed residual as a *prediction*, then verify it in
the render. Run `silencedetect` on the pre-loudnorm concat (`base.mp4` — zero shift,
unlike `final.mp4`, cf. [[feedback-loudnorm-shifts-silence-threshold]]) and read
every join's width, locating joins by the detected events and never by summing EDL
durations ([[feedback-join-offsets-from-silencedetect]]). Joins that land at
0.17–0.21 s are correct — the ~0.03 s over the designed 0.16 is render.py's 30 ms
edge fades. **A join reading ≥ ~0.25 s means the anchor lagged**: re-place that edge
from an RMS probe as `true speech end + 0.075` / `true speech start − 0.075`,
reading "true" as the last frame above about −40 dB, and re-render. On edit-40 that
took the two bad joins to 0.177 s and 0.207 s.
