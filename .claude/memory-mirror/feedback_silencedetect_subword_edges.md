---
name: feedback_silencedetect_subword_edges
description: silencedetect silence_start/end fire INSIDE quiet sibilant word tails and pre-onset breaths — cross-check every edge against word.end + a 40ms RMS probe before splitting or placing a cut
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcb26f67-1934-4e93-91eb-0c79d77a7c03
  modified: 2026-07-20T04:28:46.088Z
---

On this dim/noisy OBS source, `silencedetect` (noise=-30dB) marks a "gap" that is
actually **inside** a still-voiced word or **before** the real word onset. Both bit
edit-26 and would have produced clipped/loose cuts if trusted blindly:

- **Sub-word sibilant/nasal tails:** "processes." spans 75.28–76.54, but silence_start
  fired at 75.79 (the quiet "-cesses" fade drops below −30 dB while still audible —
  RMS there is −24 dB = speech, not silence). "notation." (word→30.18, silence@29.81)
  and "structure," (word→50.75, silence@50.38) did the same. Splitting at these
  `silence_start`s clips the word tail. → NOT splittable gaps; leave the phrase whole.
- **Faint pre-onset breaths:** phrase "So" onset is 43.15, but silence_end came early
  at 42.95 (a −43 dB breath rose above the floor). START = silence_end−0.06 = 42.89
  left a 0.26 s over-long head → join residual overshot to ~0.35 s (tail-gate flagged it).

**INVERSE case (edit-29) — silencedetect right, Scribe overshot:** the disagreement
can also go the OTHER way. On 3 sibilant/nasal endings silence_start fired 0.4–0.6 s
BEFORE Scribe's word.end ("safe." Scribe→18.66 vs silence@18.16; "attention." →84.70
vs 84.06; "files." →60.64 vs 60.18). Trusting Scribe there, I almost OVERRODE the
silence edge and kept a ~0.5 s pause. The 40 ms RMS probe of the disputed span read
**−50 to −57 dB = true silence → silencedetect was the truth, Scribe's word.end was
tail-overshoot** ([[feedback_scribe_tail_overshoot]]) → kept the mechanical edge and
trimmed the real pause. So the RMS probe is the arbiter in BOTH directions: −24 dB in
the "gap" = still speech, don't cut (edit-26); −55 dB = real gap, DO cut / edge is real
(edit-29). Never override a silence edge toward Scribe's word.end on faith — probe first.

**Why:** silencedetect's own boundaries are peak/threshold artifacts, not word edges;
they drift INTO words (quiet consonant tails) and END early (breaths). Scribe word.start/
word.end have their own drift ([[feedback_scribe_tail_overshoot]],
[[feedback_scribe_onset_token]]), so neither source alone is authoritative — the RMS
probe breaks the tie.

**How to apply:** before treating a `silence_start`/`silence_end` as a splittable pause
or a segment edge, cross-check it against the nearest word.end/word.start AND a 40 ms
RMS probe (`astats=metadata=1:reset=0.04,ametadata=print:key=lavfi.astats.Overall.RMS_level`):
if RMS in the "gap" is ≳ −30 dB the word is still sounding → don't cut there. A real
splittable gap needs word.end ≈ silence_start with the next word starting ≥0.3 s later.
When silence_end sits well before the true onset (breath), clamp START to
word.start − 0.075 instead of silence_end − 0.06. The Phase 6 onset RMS gate + tail-
residual gate catch both failures post-render — always run them.
Extends [[feedback_trim_pauses_tight]] and the edit-25 cut-edge rules.
