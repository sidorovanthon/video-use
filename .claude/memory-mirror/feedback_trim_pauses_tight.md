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

**Recurrence 2026-07-13, edit-24:** treated a single uninterrupted take (the whole BODY, one speaker, no retakes) as "one continuous segment" and kept its 0.4–1.1s inter-phrase pauses (after "on its own", "straightforward", "not minified"). User flagged them. A visually continuous take is **NOT** an exception — split it at every ≥~0.3s phrase/sentence pause and trim each to ~0.15s, exactly as if they were separate takes. Recut into 16 phrase segments (67.8s from 73.4s).

**Exception the user called out (2026-07-13, edit-25) — the OUTRO/sign-off block:** after everything was trimmed tight, the user asked to drop the trimming on the closing lines and keep them WHOLE: "The script for this video was written by a human being. For more AI tips like this, subscribe. Okay, bye!" — merged those three phrases into ONE continuous range with their natural ~0.24–0.38s pauses preserved ("там пауза приемлемая"). So: trim-tight is still the default for the BODY, but the standard outro (human-script disclaimer + subscribe CTA + "Okay, bye") reads better as one unbroken take — offer to keep it whole, and it also removes onset-clip risk on those short closing words. Don't over-generalize this to body pauses.

**How to apply:**
- Default to one segment **per kept phrase** with tight pads; only merge if there is genuinely no inter-phrase gap. Derive the split points mechanically: run `silencedetect` on `source_clean.mp4` and cut at every silence ≥ ~0.3s, padding ~0.075s into the silence on each side (never clips speech).
- After rendering, run `ffmpeg -ss A -to B -i final.mp4 -af silencedetect=noise=-40dB:d=0.15 -f null -` at each join to objectively confirm gaps are <~0.2s (don't pixel-read the waveform image).
- Watch for Scribe end-timestamp **overshoot on the last word of a kept phrase** (not just the closing word of the whole video) — it bundles trailing silence and creates a pause at the join; cut to the audible energy end. See [[feedback_scribe_tail_overshoot]].

Pairs with the OBS recipe [[reference_video_use_settings]] (its Cuts section should be read as "trim tight" for this user) and [[feedback_srt_stutter_token]].
