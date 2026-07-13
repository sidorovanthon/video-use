---
name: user-role
description: User produces short-form vertical talking-head videos via OBS for social platforms; iterates closely on grade/cut taste and expects exact-quality outputs
metadata: 
  node_type: memory
  type: user
  originSessionId: 455fd3f5-1750-4237-ba1c-36f545d36179
---

The user (anticodeguy / Anton Sidorov, a@preencipium.com) captures **single-take talking-head monologues via OBS** at 1080×1920@60, primarily for social-media short-form (TikTok / Reels / Shorts). Subject: himself in front of a dark navy/teal backdrop, neutral indoor lighting.

He works in **Russian** when conversing with the assistant, English in the videos themselves.

He uses the `video-use` skill in `C:/Users/sidor/repos/video-use` and outputs land in `M:/videos/OBS/edit-NN/` (incrementing per session — edit-01 through edit-05 used as of 2026-05-13).

**Working style:**
- Provides the source video, a settings reference, and the script for SRT verification in one shot — expects the assistant to drive end-to-end.
- Iterates on taste calls (grade brightness, pause trimming) — be ready to re-render multiple times.
- Approves output by feel, not by numbers. When he says "still too dark" or "несколько пауз не вырезаны", he means visible/audible — not metric.
- Wants memory and settings updated after each refinement so the next session inherits the new baseline.

Related: [[reference-video-use-settings]], [[feedback-grade-brightness]]
