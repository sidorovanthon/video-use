---
name: feedback_trim_pauses_tight
description: "For this user's OBS talking-head monologues, trim natural inter-sentence/inter-phrase pauses TIGHT (~0.15s residual) — do NOT preserve 400-600ms 'breaths' by merging adjacent kept phrases; the user reviews and flags preserved pauses as defects."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46b25452-23e9-41f2-9456-0d50ffec27fe
---

On this user's OBS vertical talking-head monologues, do **not** preserve natural pacing pauses between kept sentences/phrases. Cut them tight — aim for ~0.10–0.20s residual at every join (the standard 50/80ms pads + 30ms fades land there naturally). Merging adjacent kept phrases into one segment "to keep the breath" is the WRONG default here.

**Why:** Observed 2026-06-09, edit-10. I merged adjacent clean phrases to preserve ~1.4s natural pauses (after "actually doing", after "work with") and left a Scribe-overshot tail after "cognitive toolkit". User reviewed and flagged all three preserved pauses as defects to remove. This contradicts the generic skill guidance ("speaker handoffs benefit from 400–600ms air") and the recipe's dead-air note — for THIS footage class the user wants snappy pacing.

**How to apply:**
- Default to one segment **per kept phrase** with tight pads; only merge if there is genuinely no inter-phrase gap.
- After rendering, run `ffmpeg -ss A -to B -i final.mp4 -af silencedetect=noise=-40dB:d=0.15 -f null -` at each join to objectively confirm gaps are <~0.2s (don't pixel-read the waveform image).
- Watch for Scribe end-timestamp **overshoot on the last word of a kept phrase** (not just the closing word of the whole video) — it bundles trailing silence and creates a pause at the join; cut to the audible energy end. See [[feedback_scribe_tail_overshoot]].

Pairs with the OBS recipe [[reference_video_use_settings]] (its Cuts section should be read as "trim tight" for this user) and [[feedback_srt_stutter_token]].
