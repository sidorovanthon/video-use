---
name: feedback_onset_probe_anchor_artifact
description: "An onset probe anchored at silencedetect's silence_end is DEFINITIONALLY above the threshold, so \"first 20ms > -25dB = clipped\" false-fires on nearly every join; judge the SHAPE (decay -> splice notch -> ramp) instead"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c56dabbe-d570-4533-9285-1f7eda33fcc5
  modified: 2026-08-10T03:12:13.140Z
---

The Phase 6 onset rule ("first ~40 ms hotter than ~−25 dB = the segment begins
mid-word") breaks when the probe window starts exactly at `silence_end`.
`silence_end` **is** the moment the signal crosses the detector threshold going
up, so a window anchored there necessarily contains supra-threshold energy. On
edit-38, 18 of 23 joins flagged "HOT" at −10…−24 dB even though every join was
verifiably clean.

The reliable read is the **shape across the whole join**, at ~10 ms resolution:

```
decay  −17.9 → −35 → −50   (previous segment tailing off)
splice −91 dB               (concat boundary = digital silence)
ramp   −67 → −50 → −25      (next segment's own room tone, then the onset)
```

A genuinely clipped onset has **no preceding decay and no splice notch** — the
previous segment's tail runs straight into mid-word energy. That is the criterion
already recorded in [[feedback_join_offsets_from_silencedetect]]; treat the −25 dB
number as a screen, never a verdict.

Two corroborating checks that ARE threshold-independent:
- **Gap arithmetic.** Designed residual = 0.10 s (tail pad) + 0.06 s (lead-in pad)
  ≈ 0.16 s. A join whose lead-in got eaten measures ≈0.10 s. edit-38's 23 joins
  measured 0.143–0.199 s, i.e. every segment kept ≥ ~0.04 s of its 0.06 s lead-in.
- **Floor depth.** The mean level across the gap must be ≤ ~−40 dB. Anything
  shallower means speech is inside the "silence" — or that the probe timeline is
  broken (see [[feedback_final_mp4_aac_priming_drift]]).

**How to apply:** do not re-cut on a bare "hot onset" number. Print the 10 ms RMS
trace across the join, confirm decay → notch → ramp, and check the gap width
against 0.16 s. Only re-render when the decay or the notch is genuinely absent.
