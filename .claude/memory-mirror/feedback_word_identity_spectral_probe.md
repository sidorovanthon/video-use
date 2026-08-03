---
name: feedback_word_identity_spectral_probe
description: "Scribe WORD-IDENTITY disputes (agent/engine, ran/run, a/the) are settled by band-energy probes against in-file control words, not by guessing from context"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba2b871a-2172-4df5-bcee-bd222cfe622f
  modified: 2026-08-03T01:49:00.109Z
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

**Why:** deciding these from context alone ("nobody says coding engine") is the
guess the pipeline is supposed to eliminate — and the opposite mistake, assuming
the script is truth, shipped wrong on edit-32 where Scribe was right every time.
A control word from the same recording removes mic/room/voice as variables.

**How to apply:** at the Phase 5/6 SRT gate, for every mismatch that is a real
voiced token (not a missing article, not a spelling difference), pick a control
word of each candidate phoneme class from the same file, slice both at 30–60 ms
with `volumedetect` behind `lowpass`/`highpass` bands, and let the measurement
choose. Only orthography (`code base`→`codebase`) and product names
(`Cloud Coder`→`Claude Code or`) may be fixed without a probe.

Related: [[feedback_silencedetect_subword_edges]],
[[feedback_srt_full_script_reconcile]],
[[feedback_script_txt_reflects_shipped_adlib]]
