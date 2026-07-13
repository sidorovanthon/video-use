---
name: feedback-exposure-match-segments
description: "Source face luma can drift mid-take (edit-23 front ~114 vs back ~80); uniform grade leaves a visible brightness step at the cut — pre-normalize darker segments with eq=gamma=G before the grade via render.py per-range \"grade\" field"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2731bad5-8472-4d04-b84a-e2c5d71dab35
---

Within a single OBS take the source face luma can DRIFT between halves — edit-23 ("Migrating… Part 7") measured front segments raw YAVG ~107–114 vs back segments ~78–83. A uniform v7-contrast grade left the back-half graded face at Y≈47–56 vs ≈87 up front, and the user flagged the 44.98s cut: "significantly darker, like a different grade."

**Why:** grade selection was done on the brightest frame only; the exposure step mid-take made one grade wrong for half the video.

**How to apply:**
1. Measure the face-crop luma of **EVERY kept segment**, not just the brightest frame.
2. If segments differ materially, pre-normalize each darker segment with `eq=gamma=G` **before** the grade chain so all faces land in the same band (~85–93 on edit-23). Approved edit-23 gammas: B3 1.08 / B4 1.42 / B5 1.33 / B6 1.32 / B7 1.30 / OUTRO 1.33 (front segments unchanged).
3. `helpers/render.py` supports a per-range `"grade"` field in the EDL for exactly this — give the darker ranges `eq=gamma=G,<grade chain>` while the rest use the EDL-level grade.

See [[feedback-grade-migrating-series]] and [[reference-video-use-settings]] (settings_reference.md edit-23 UPDATE block has the full log).

*(Reconstructed 2026-07-13 from settings_reference.md + MEMORY.md after NUL corruption of the original.)*
