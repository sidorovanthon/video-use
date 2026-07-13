---
name: feedback_scribe_onset_token
description: Scribe phrase-onset tokens near long silences are degenerate (start sits in silence) — never use word.start raw for a segment start; verify onset with silencedetect
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7d27894-a7b4-4252-8ab4-6b16072352ed
---

When a kept segment starts on the first word of a phrase that follows a long source silence, Scribe's onset token timing is unreliable — it places `word.start` inside the preceding silence and gives the token a bogus long "duration". Using that raw `start` puts ~1s of dead air at the head of the segment.

**Why:** bitten twice. edit-10: "And fair warning" — the "And" burst was at 251.65–251.95 but Scribe tagged a degenerate zero-duration "And" at 252.05 (clipped the word). edit-11: BUG_EXAMPLE take B "For example" — Scribe "For" token start 112.22 / end 113.64 (1.42s) but real speech onset was ~113.31; the raw start left a 1.257s dead gap at the join, caught only in self-eval silencedetect.

**How to apply:** for any segment START on a post-silence phrase onset, do NOT trust `word.start`. Find the real onset with `silencedetect` (the `silence_end` just before the word) or an astats RMS ramp, then set start = real_onset − 0.05. This is the START-edge sibling of [[feedback_scribe_tail_overshoot]] (which is the END-edge version for closing words). Always run silencedetect on the rendered output during self-eval — a >0.4s gap at a join means an onset/tail token slipped through.
