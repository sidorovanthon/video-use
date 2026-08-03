---
name: feedback_grade_systems_analysis_series
description: "\"Systems Analysis\" series has NO settled grade — edit-26/27 went lift66/lift58, edit-31/32 went v7-contrast on equally dim sources; always measure + show the 5-up sheet"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3a2988e8-0384-4188-aa48-f53acf534bb4
  modified: 2026-08-03T02:56:50.876Z
---

The "Systems Analysis" family (edit-26 "Systems Analysis and Artificial Intelligence",
edit-27 BPMN, edit-31 "We continue the saga…", edit-32 "How to make AI and systems
analysis work together") is the one series where the grade **flips between parts**:

| edit | face raw YAVG | v7-contrast crop | shipped |
|---|---|---|---|
| edit-26 | 44–46 | 22.7 | **lift66** |
| edit-27 | 44–59 (non-uniform) | 36 | **lift58** + per-seg gamma |
| edit-31 | 67.7–71.0 | 46.9 | **v7-contrast** |
| edit-32 | 68.9–74.1 | 46.7 | **v7-contrast** |
| edit-33 | 72.0–78.4 | 49.9 | **v7-contrast** (same 2026-05-14 shoot as edit-32) |
| edit-34 | 73.3–77.7 | 53.7 | **v7-contrast** (same 2026-05-14 shoot; new topic) |
| edit-35 | 61.9–68.4 | 45.6 | **v7-contrast** (new 2026-05-21 shoot, new topic) |

**Why:** all these sources are "dim", but dimness alone doesn't decide — what matters is
how the face survives the contrast curve. Below ~YAVG 40 under v7-contrast the face
crushes and the user picks lift; at ~46+ the face reads fine and the user picks the
moody contrast look. Lighting drifted between the edit-26/27 shoots and the edit-31/32
shoots, so the series' own history is not a predictor.

**edit-35 tightens the threshold from below.** Its v7-contrast crop measured **45.6** —
the lowest reading ever shipped as contrast, and only 0.9 above the edit-31/32 pair. The
raw source was also the dimmest of the recent run (61.9–68.4). The user still picked
contrast, because on THIS source the deciding factor was visible on the sheet rather than
in the number: the raw frame carries a **haze / lifted-black** cast, and every lift
variant amplified that haze while v7-contrast was the only one that produced a clean
black background. So read the sheet for what the lifts do to the BACKGROUND, not only
what the curve does to the face.

**How to apply:** never inherit a grade from the previous part in either
direction. Run `grade_sheet.py scan` + `sheet`, show the 5-up, wait for the explicit call.
Five consecutive v7-contrast picks (edit-31 … edit-35) are a leaning, not a
default — and edit-32/33/34 share a shoot day, so they are really one lighting sample.
Contrast with [[feedback_grade_keep_codex_series]] and [[feedback_grade_migrating_series]],
which ARE settled defaults, and [[feedback_grade_brightness]] for the general rule.
