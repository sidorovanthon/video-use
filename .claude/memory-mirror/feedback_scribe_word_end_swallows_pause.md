---
name: feedback-scribe-word-end-swallows-pause
description: Scribe word.end over-extends into a real pause, so enumerating gaps from word-to-word deltas alone misses them; enumerate silencedetect gaps INSIDE each kept block too
metadata:
  type: feedback
---

Enumerating Phase 3 split candidates from **Scribe word-to-word gaps alone misses
real pauses**, because Scribe stretches `word.end` on a phrase-final word right
through the silence that follows it. The word-delta is then ~0, so no candidate
is emitted at all.

edit-41 (raw OBS audio, floor −83 dB): six genuine pauses of 0.29–0.45 s, floors
**−45 to −54 dB**, were invisible to a ≥0.28 s word-gap scan and were found only
by running `silencedetect` on `source_clean.mp4` and intersecting the events with
the kept ranges:

| Scribe token (claimed span) | actual silence |
|---|---|
| `possible,` 34.32–35.10 | 34.786–35.112 |
| `time,` 36.50–37.07 | 36.771–37.064 |
| `simple,` 49.72–50.30 | 50.010–50.358 |
| `me.` 109.96–110.42 | 110.041–110.423 |
| `review,` 115.70–116.36 | 116.048–116.369 |
| `included.` 176.94–177.80 | 177.457–177.819 |

**Why:** this is the exact inverse of [[feedback_silencedetect_subword_edges]] —
there silencedetect invents gaps Scribe knows are speech; here Scribe hides gaps
silencedetect sees. Neither list is complete on its own, which is what the
"UNION" in the skill actually means.

**How to apply:** after picking the kept blocks, iterate the `silencedetect` gap
list (run it at BOTH −35 dB and −30 dB — three of the six above only appeared at
−30) and report every event that falls fully inside a kept range with width
≥ ~0.28 s, independently of the Scribe deltas. RMS-probe each one before
splitting. Related: [[feedback_trim_pauses_tight]].

**2026-08-24 — edit-43: the INVERSE also happens — Scribe word gaps can run WIDER than the acoustic pause, and the acoustic width is what decides the cut.** On this track (raw, gated OBS) five candidates showed a Scribe word-to-word delta of 0.30–0.34 s while `silencedetect` at −35 dB measured only 0.157 / 0.245 / 0.257 / 0.284 / 0.291 s: `operations,|tracking` 0.340→**0.157**, `result,|but` 0.310→0.245, `Opus,|in` 0.340→0.257, `yet,|give` 0.300→0.284, `instructions,|you've` 0.340→0.291. The RMS mid-gap floors were genuinely quiet (−41…−58 dB), so these are real pauses — they are just SHORTER than Scribe claims, because the decaying voiced tail of the preceding word stays above −35 dB for 50–100 ms after Scribe has already stamped `word.end`. Cutting the 0.157 s one would have left a **negative** residual (end = `silence_start+0.10` = 50.700 vs start = `silence_end−0.06` = 50.697); cutting the 0.245–0.291 s ones would have squeezed them to 0.085–0.131 s, tighter than the designed 0.16 s.

**How to apply:** the Scribe delta only nominates a candidate — **the `silencedetect` width is the acoustic truth and is what the ≥0.3 s split rule is measured against.** Split when the *event* is ≥0.30 s wide; leave 0.15–0.29 s events uncut (they are already at or near the target residual, and a 0.25 s inter-clause beat has never been flagged — the edit-24 complaint was about 0.4–1.1 s pauses). Sanity check that catches it every time: if `(silence_start+0.10) ≥ (silence_end−0.06)` the gap is under 0.16 s and must not be cut. Complements the swallowed-pause direction above: intersect BOTH lists, then let the acoustic width arbitrate.
