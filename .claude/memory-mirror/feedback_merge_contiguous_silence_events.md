---
name: feedback-merge-contiguous-silence-events
description: silencedetect can split one dead-air join into several back-to-back events; reading only the first makes a 0.52s pause pass as 0.15s — merge events closer than ~0.03s before measuring any join residual
metadata:
  type: feedback
---

The Phase 6 join gate measures each join's residual from the `silencedetect` event
nearest the join. On edit-45 the `E2 → F1` join emitted **three back-to-back
events** — `50.46→50.60`, `50.60→50.75`, `50.75→50.93` — whose ends and starts
touch exactly. Taking the nearest single event gave **0.148 s** and a clean "OK",
while a 20 ms `astats` RMS track showed the audio sat below −44 dB continuously
from 50.38 to 50.90: a **0.52 s** dead-air join, more than double the 0.25 s defect
line.

**Why:** `silencedetect` re-arms on a single supra-threshold sample, so one long
quiet stretch containing a stray tick is reported as a chain of adjacent intervals
rather than one. Every automated residual check that does `min(|midpoint − join|)`
then reads whichever fragment happens to be closest, and fragments are by
construction *shorter* than the truth — so the failure mode is always a false PASS,
never a false alarm. The underlying cause on edit-45 was
[[feedback-silence-start-lags-speech-end]] in an extreme form: `silence_start`
reported 168.88 against a true acoustic speech end of **168.52** — a **0.36 s** lag,
four times the 0.09 s documented on edit-40 — so `silence_start + 0.10` retained
0.46 s of tail instead of 0.10 s.

**How to apply:** before matching events to joins, **coalesce the event list** —
merge any two intervals separated by less than ~0.03 s into one — and measure the
residual on the merged span. A merged span ≥ ~0.25 s is the defect, regardless of
how the fragments looked. Any join whose match came from a merged run deserves a
20 ms RMS track across it ([[feedback-onset-probe-anchor-artifact]] for how to read
the shape) before you accept the number. Re-place the offending edge from that
track — true speech end + 0.10 — never from the reported `silence_start`. On
edit-45 that took the join to 0.173 s and all 12 joins to 0.173–0.203 s. This
compounds with [[feedback-scribe-word-end-swallows-pause]]: Scribe's `word.end`
hid the same pause on the transcript side, so neither source flagged it alone.
