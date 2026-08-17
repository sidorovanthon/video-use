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
