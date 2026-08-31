---
name: feedback_transcript_spacing_tokens
description: Scribe transcripts interleave type='spacing' tokens between words, so merging two adjacent words by list index i/i+1 grabs a space, not the next word
metadata:
  type: feedback
---

`transcripts/S0.json` stores words and separators in ONE flat list: real tokens
carry `type: "word"`, and a `type: "spacing"` entry sits between every pair. Any
edit that reaches for "the next word" as `w[i+1]` — the hyphenated-compound merge
in [[feedback_srt_full_script_reconcile]] — silently operates on the space.

edit-47: merging `hand-off` + `prompt` into `handoff-prompt` by index left the
`prompt` token in place, and the SRT gate came back with a fresh
`extra in srt: 'prompt'` on the rebuild.

**Why:** the failure is invisible in the JSON diff and only shows up as a NEW gate
mismatch, which reads like a second unrelated defect.

**How to apply:** filter to `type == 'word'` (or scan forward past spacings) before
any neighbour-based edit, and drop the folded token rather than relying on an
index skip. Re-run `diff_srt_script.py` after every rebuild until exit 0.
