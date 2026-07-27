---
name: feedback_silencedetect_subword_edges
description: silencedetect silence_start/end fire INSIDE quiet sibilant word tails and pre-onset breaths — cross-check every edge against word.end + a 40ms RMS probe before splitting or placing a cut
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcb26f67-1934-4e93-91eb-0c79d77a7c03
  modified: 2026-07-27T03:38:23.858Z
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

**edit-31 — the dismissal failure mode: probe at CUT time, not only when in doubt.**
At Phase 3 I saw silence 102.640–102.990 (0.350 s) sitting inside Scribe's "meetings"
(102.20–103.00) and dismissed it as another sub-word tail *by pattern-match on this very
memory*, without probing. It was a **real 0.35 s pause** (RMS −43…−56 dB) — Scribe's
word.end had overshot by 0.36 s (the edit-29/30 inverse case). It only surfaced in Phase 6
because the SRT gate asked a *different* question ("was `(calls)` spoken here?") and that
probe exposed the silence → segment had to be split and the video re-rendered. The two
cases are indistinguishable from timings alone: "Scribe's word spans the gap" is the
signature of BOTH a sibilant tail and a word.end overshoot.

**How to apply (hardened):** probe EVERY silencedetect gap ≥ 0.3 s that falls inside a
kept range — including (especially) the ones a Scribe word appears to span. Never resolve
one by reasoning; the 40 ms RMS probe is cheap and is the only arbiter. Doing this during
Phase 3 costs seconds; skipping it costs a full re-render.

**edit-32 — two adjacent silences split by a sub−40 dB blip = an INAUDIBLE plosive
release; cut BEFORE it, not after.** At the "But that's not it." → outro join,
silencedetect reported two back-to-back gaps, 183.299–183.552 and 183.552–183.788,
separated by a single loud-enough sample at 183.552. I read that blip as the /t/
release (i.e. the word still ending) and placed END at the *second* silence_start
+0.10 = 183.650. The rendered join measured **0.40 s** of quiet — the tail gate fired.
The RMS probe shows why: the vowel of "it" ends at 183.29 (−24.7 → −38 → −55 dB) and
the "release" at 183.552 peaks at only **−44.9 dB** — 20 dB below the quietest audible
speech here, i.e. inaudible. Correct END = first silence_start + 0.10 = 183.39.

**How to apply:** when silencedetect emits two adjacent gaps separated by one blip,
probe the blip's level before deciding which `silence_start` is the word's end.
≳ −35 dB = a real release, keep it (cut after); ≲ −40 dB = an inaudible plosive burst,
treat the FIRST silence_start as the acoustic end and cut before the blip. Word-final
/t/ /k/ /p/ after an unstressed vowel is the usual producer. Timings alone can't tell
this from a real release — same "probe, don't reason" rule as the edit-31 case above.

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
