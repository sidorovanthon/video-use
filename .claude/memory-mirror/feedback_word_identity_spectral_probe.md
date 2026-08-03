---
name: feedback_word_identity_spectral_probe
description: "Scribe WORD-IDENTITY disputes (agent/engine, ran/run, a/the) are settled by band-energy probes against in-file control words, not by guessing from context"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba2b871a-2172-4df5-bcee-bd222cfe622f
  modified: 2026-08-03T02:31:11.297Z
---

The RMS probe settles *silence vs speech*. A second class of SRT-gate mismatch is
*which word was said* — Scribe returns a real, confidently-voiced token that is
simply the wrong word. Three mechanical discriminators, all used on edit-33:

- **Word-final nasal (agent vs engine).** `engine` ends /n/, `agent` ends an
  unreleased /t/. Slice the last 60 ms and read LF (<500 Hz) + F2: a nasal coda
  keeps voiced murmur (control "any" /n/: broadband −23.6, LF −34.9), while
  edit-33's disputed tail read −52…−55 dB in *every* band = no murmur → `agent`.
- **Vowel frontness (ran vs run).** Compare the F2hi(1.5–2.4k) − F2lo(0.8–1.4k)
  ratio against control words from the SAME file: /æ/ "that" −3.47, /ʌ/ "some"
  −3.76, "just" −4.05, target −2.81 → fronter than all → `ran`. Pre-nasal /æ/
  raises, which widens the gap in your favour.
- **Degenerate article token (a vs the).** Scribe emits ~0.010 s tokens for
  unstressed articles. Real `the` in the same file runs 0.10–0.12 s; the
  confirmed `a` of "as a folder" is also 0.010 s → a 0.010 s "the" is `a`.
  (Same shape as the edit-29 0.01 s "to"→"the" fix.)

**edit-34 — crude band ratios FAIL on reduced function words; use LPC formants +
a MATCHED-ENVIRONMENT control.** The `in` vs `on` dispute ("so you don't get lost
?? them") defeated two rounds of the band-ratio method above: both candidates were
fully reduced and nasalized, energy sat mostly below 300 Hz, and the 300-700 /
700-1100 / 1500-2700 ratios of the disputed token landed *between* the control sets
with no separation. What actually resolved it:

- **LPC formant tracking** (order 12 @ 10 kHz, pre-emphasis 0.97) instead of band
  ratios — now `helpers/word_probe.py formant`. Read F1 for vowel height and F2 for
  frontness frame by frame, so you can see the nucleus rather than average over the
  neighbouring consonants.
- **A control in the same phonetic environment.** Generic "on"/"in" controls were
  useless: the ones available sat before "your" (/j/ drags F2 up) and carried more
  stress. The decisive control was `what's IN them` — sibilant + unstressed vowel +
  "them", identical to the disputed `lost ?? them`. There the matched control's F2
  is **≈1360 Hz** while both takes of the disputed token read **≈1170-1200 Hz** =
  a backer vowel → `on`. Scribe had it right in two independent takes.
- **Sibilant DURATION, not presence, for /s/-final candidates.** `develop the/this
  structure`: measure the frication run before "structure" and compare with the same
  word elsewhere. Control `file structure` = 0.225 s of /s/; the disputed = 0.145 s
  — *shorter*, so there is no extra /s/ from "this" → `the`. A presence test says
  nothing here because "structure" supplies its own /s/ either way.

Also settled that session without a probe, on structure rather than acoustics:
Scribe merged `Code or`→`Coder` and split `there's`→`there is`. For the merge, the
disputed second syllable measured F2 1209-1355 against the speaker's confirmed "or"
in the same collocation at 1118-1394 = the same token. For the split, "there ?? a"
spanned **0.270 s** vs 0.300/0.330 s for two known `there's a` controls — an extra
syllable cannot be *shorter*, so it is the contraction.

**Direction of the fix is not fixed.** These five mismatches split 3 transcript-side
(Scribe wrong: Coder, there is, the→a) and 2 script-side (Scribe right: in→on,
this→the). Decide each one on its own measurement; see
[[feedback_script_txt_reflects_shipped_adlib]].

**Why:** deciding these from context alone ("nobody says coding engine") is the
guess the pipeline is supposed to eliminate — and the opposite mistake, assuming
the script is truth, shipped wrong on edit-32 where Scribe was right every time.
A control word from the same recording removes mic/room/voice as variables.

**How to apply:** at the Phase 5/6 SRT gate, for every mismatch that is a real
voiced token (not a missing article, not a spelling difference), pick a control
word of each candidate phoneme class from the same file — matching the phonetic
ENVIRONMENT, not merely the word — and run `helpers/word_probe.py` (modes
`formant` / `sib` / `rms`; `batch probes.json` prints a disputed token and all its
controls in one pass). Let the measurement choose. Only orthography
(`code base`→`codebase`) and product names (`Cloud Coder`→`Claude Code or`) may be
fixed without a probe. If two rounds still overlap, say the probe was inconclusive
and name the weaker evidence you fell back on — don't dress a guess up as a
measurement.

Related: [[feedback_silencedetect_subword_edges]],
[[feedback_srt_full_script_reconcile]],
[[feedback_script_txt_reflects_shipped_adlib]]
