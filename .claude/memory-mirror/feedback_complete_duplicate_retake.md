---
name: feedback_complete_duplicate_retake
description: "A retake can be a COMPLETE duplicate sentence (no \"--\" truncation marker) — spot it by scanning packed phrases for a repeated line, and keep the take that leaves the outro block continuous"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eadf0ac2-e79d-4bee-85f3-fc97759f991c
  modified: 2026-07-27T02:45:07.617Z
---

Not every retake announces itself as a truncated false start. On edit-30 the
speaker said the full closing line **"I wish you no BSODs."** twice — once
trailing the previous sentence (source 72.44–73.56) and once as a clean standalone
(74.62–75.70). Both were complete, same duration, no `--`/stutter token; the only
signal was `takes_packed.md` showing the identical sentence at the end of one
phrase and the start of the next.

**Why:** the usual false-start heuristics (truncated word, stutter token, trailing
mumble) do not fire here, so the duplicate can slip through and ship twice, or the
wrong copy can be kept.

**How to apply:**
- When reading `takes_packed.md`, scan for a sentence that appears at the END of
  one phrase and the START of the following one — that is a complete-duplicate
  retake, not two separate lines. Cross-check against `script.txt`: if the script
  has the sentence once, exactly one copy ships.
- Choose the copy that keeps the standard sign-off block continuous (see
  [[feedback_trim_pauses_tight]]). On edit-30 that meant dropping the *first*
  copy so the outro ran unbroken from "I wish you no BSODs." to "Okay, bye!" as a
  single un-cut range.
- The preceding segment then ends on the word before the duplicate — derive that
  end from `silencedetect`, not Scribe: on edit-30 Scribe's "Codex." ran to 72.419
  while the real acoustic end was 71.811 (RMS in between −46…−60 dB = true
  silence). See [[feedback_silencedetect_subword_edges]].
