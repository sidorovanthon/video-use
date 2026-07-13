---
name: feedback-srt-straddle-dup
description: Splitting a take to trim an internal pause makes build_master_srt emit a phantom duplicate caption for the word straddling the cut; rebuild SRT with start-based word membership
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fef016ec-4a7a-4892-8001-6f4bde9dfc27
---

When you SPLIT one continuous take into two EDL segments to trim an internal dead-air pause (the standard tight-join move on this user's OBS monologues, see [[feedback-trim-pauses-tight]]), a word whose audio STRADDLES the split gets captioned twice.

Concrete case (edit-21 / Part 5): "API." spanned 140.56–141.94. SEG8a was cut at 140.96 and SEG8b started at 141.90. `helpers/render.py::build_master_srt` uses INTERSECTION membership (`_words_in_range`: include if `not (word.end <= seg_start or word.start >= seg_end)`), so "API." fell inside BOTH segments → a real "…THE OTHER API." cue in SEG8a plus a phantom ~40ms "API." cue at the head of SEG8b.

**Why:** Scribe also tends to stretch a word's `end` well past its real audio (here word.end 141.94 vs real audio end ~140.87), which widens the straddle and makes this more likely right where you cut.

**How to apply:** As of 2026-07-13 (edit-26 wrap) `helpers/render.py::_words_in_range` now IMPLEMENTS start-based membership in code (`if not (t_start <= ws < t_end): continue`) — the phantom is fixed at the source, no manual workaround needed. Rule for reference: a word belongs to a segment iff `seg_start <= word.start < seg_end`, so every word lands in exactly one segment. The rest is unchanged (2-word UPPERCASE chunks, punct break, output-timeline offsets `out_t = start - seg_start + seg_offset`, build from a CORRECTED transcript COPY per [[feedback-srt-stutter-token]]). Still eyeball the join region for a near-zero-duration repeated cue as a backstop, and if you ever touch `_words_in_range`, keep it start-based.
