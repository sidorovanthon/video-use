---
name: reference-video-use-settings
description: "Canonical OBS-talking-head recipe now lives IN THE REPO at C:\\Users\\sidor\\repos\\video-use\\docs\\settings_reference.md (git-backed); M:/videos/OBS/edit-01/settings_reference.md is a pointer; grade default v7-lift for \"Losing Context\" series, v7-contrast for \"Migrating\" series"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2731bad5-8472-4d04-b84a-e2c5d71dab35
---

The canonical OBS-talking-head editing recipe (source profile, output spec, grade variants + decision rule, audio loudnorm, cut/pause rules, subtitle rules, output location, render command, pipeline order) lives at:

**`C:\Users\sidor\repos\video-use\docs\settings_reference.md`** — git-backed, versioned, the single source of truth as of 2026-07-13.

The old location `M:/videos/OBS/edit-01/settings_reference.md` now holds a pointer to the repo copy (kept because older edit-NN notes and memories reference it).

Key state: grade decision = measure the face-crop luma of every kept segment → bright (~≥88) → **v7-contrast**; dim → **v7-lift** (mid 0.60–0.70); always build the 5-up face-crop comparison sheet at the brightest leaned-in TALKING frame before the final render. Series defaults: [[feedback-grade-brightness]] ("Losing Context" → v7-lift), [[feedback-grade-migrating-series]] ("Migrating" → v7-contrast), drift within a take → [[feedback-exposure-match-segments]].

*(Reconstructed 2026-07-13 after NUL corruption; updated for the repo relocation.)*
