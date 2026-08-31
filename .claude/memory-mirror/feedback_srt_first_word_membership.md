---
name: feedback_srt_first_word_membership
description: build_master_srt drops a segment's FIRST word when Scribe word.start sits a few ms before the EDL segment start, even though the audio contains the word
metadata:
  type: feedback
---

`build_master_srt` uses start-based membership (`seg_start ≤ word.start < seg_end`,
see [[feedback_srt_straddle_dup]]). Segment starts are placed acoustically
(`silence_end − 0.06`), and Scribe's `word.start` routinely fires 20–100 ms
BEFORE the real onset ([[feedback_scribe_onset_token]]). When the Scribe value
lands just outside the segment, the word is spoken in the render but never
captioned — and the SRT gate reports it only as `dropped from srt: '<word>'`,
with no hint that it is a timing problem rather than a mis-hearing.

edit-47: outro segment start 167.180, Scribe `you` at 167.160, true acoustic
onset 167.240. The audio was fine; only the caption was missing.

**Why:** a "dropped word" at a segment BOUNDARY is a membership artifact, not a
Scribe mis-hear, so the usual text override does nothing.

**How to apply:** when the gate reports a dropped word, first check whether it is
the first (or last) word of a segment. If it is, RMS-probe the real onset and set
that word's `start` in the transcript COPY to the acoustic onset — never widen the
EDL segment, which would re-introduce the pause the cut removed.
