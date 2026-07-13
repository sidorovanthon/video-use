---
name: feedback-grade-brightness
description: "OBS talking-head grade: as of edit-16 (2026-06-23) DEFAULT to v7-contrast for the 'How to Avoid Losing Context' series even on dim sources — v6's warm mid-lift reads YELLOW and was rejected. v7-contrast = add contrast + deepen shadows, NO brightness lift, hold white point, neutral skin. If too dark, lift mids within v7, never revert to v6."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 455fd3f5-1750-4237-ba1c-36f545d36179
---

> **TL;DR (current rule, 2026-06-10):** the grade depends on SOURCE exposure — measure the face crop with `signalstats` first. **Dim source → v6** (lift mids, below). **Bright source → v7-contrast** (add contrast, deepen shadows, NO brightness lift, hold white point — see UPDATE at bottom). The "always wants brighter" history below is the DIM-source case only; do not apply it to an already-bright face.

For OBS talking-head captures (dark navy/teal backdrop, single subject) where the face reads **dark in the raw source**, the user asks for **brighter skin / more midtone lift** than the original `warm_cinematic v4a` recipe produces.

**Why:** Two iterations on the 2026-05-13 session both came back as "still too dark". The reference grade in `edit-01/settings_reference.md` (v4a: contrast 1.18, curves `0/0.06 0.25/0.25 0.5/0.55 0.85/0.92 1/1`) leaves skin sitting too low for the user's taste. Even v5 (mids 0.5→0.62, contrast 1.15) was rejected.

**Approved v6 starting point** (2026-05-13):
```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.05:gm=-0.01:bm=-0.07:rh=0.06:bh=-0.08,
curves=master='0/0.08 0.25/0.32 0.5/0.72 0.85/0.95 1/1'
```

Key levers when user says "skin too dark":
1. **Mid-curve point** is the primary tool (0.5 → 0.62 / 0.72 / higher). Each +0.05 is a visible lift.
2. **Drop contrast** in parallel (1.18 → 1.15 → 1.08) so squeezing doesn't fight the lift.
3. **Lift shadow anchor** (0.25 → 0.32) to bring lower-mid skin shadows up too — important, otherwise only highlights of the face brighten.
4. **Lift highlight roll-off** (0.85 → 0.95) to keep skin specular highlights from looking dull.
5. **Nudge saturation up slightly** (0.95 → 0.97) — added mid brightness can wash skin pasty otherwise.

**How to apply:** Start from v6 (above) for any new OBS talking-head on dark backdrop. If user pushes back as too dark again, push mids further (0.72 → 0.78) and consider raising shadow anchor to 0.35. The colorbalance warm-shift values are not the problem — leave them alone. Related: [[reference-video-use-settings]]

**UPDATE 2026-06-10 (edit-11) — the "always lift brightness" premise is WRONG for a bright source. Match the grade to source exposure.** edit-11's source was already very bright (well-lit face). v6's lift (mid 0.5→0.72, highlight 0.85→0.95, black floor 0→0.08) burned the face flat — user rejected it as "пересвеченным" then "выжженным, все детали с лица потеряны". A softened v6 (mid 0.5→0.64, "v6-soft") was ALSO rejected — too subtle, still washed. What the user actually wanted (and approved): **do NOT raise brightness at all; add contrast, deepen shadows, hold the white point.** Approved grade = **v7-contrast (grade E):**
```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'
```
Black point→0, shadows pulled DOWN (0.28→0.17), mids slightly DOWN (0.5→0.46, no lift), the bright face zone pulled down (0.72→0.69) to recover forehead/cheek detail, **white point held at 1→1** (do NOT pull the ceiling down — that flattens). Milder warm than v6 (bright skin needs less push). User: "идеально", asked to keep it as the template. **Decision rule going forward: measure source face luma first — bright source → v7-contrast (this block); dim source → v6 (lift mids). NEVER lift mids on an already-bright face — that is what makes it look burned.** Full writeup now in `edit-01/settings_reference.md` (v7-contrast section).

**UPDATE 2026-06-23 (edit-16, "...Part 5") — APPROVED GRADE = "v7-lift": v7's neutral colorbalance + a lifted curve. v6 retired for this series.** Sequence of rejections on edit-16 (dim source, face YAVG ≈ 81): (1) v6 (dim→v6 rule) rejected — skin "снова теперь уходит в жёлтый" (v6's warm bm−0.07/bh−0.08 + mid-lift 0.5→0.72 reads YELLOW; recurring complaint, also edit-11). (2) pure v7-contrast (the edit-14 grade) rejected — "очень темно" on this dim source. (3) User asked to **see comparison frames before rendering**; from a 4-up (v6 / pure-v7 / v7-lift mid 0.60 / v7-lift mid 0.66) they picked **v7-lift mid 0.66 (variant D)**:
```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
curves=master='0/0.04 0.28/0.30 0.5/0.66 0.72/0.82 1/1'
```
= v7's NEUTRAL balance (kills yellow) + the curve lifted back up for brightness (mid 0.66, near v6's luminance, NOT v6's warmth). **Rules going forward for this series: (a) do NOT auto-pick v6 on a dim measurement — it yellows; (b) do NOT use pure v7-contrast on a dim source — too dark; (c) use v7-lift, brightness lever = mid point 0.60↔0.66↔0.70 with colorbalance held neutral; (d) ALWAYS render a comparison sheet and show the user before the full render (explicit request).**

**UPDATE 2026-06-29 — v7-lift mid 0.66 is now the established default ACROSS series, not just "How to Avoid Losing Context".** Used for the "Migrating Knowledgebase With AI" series too: Part 1 = edit-17, Part 2 = edit-18 (both dim sources, face YAVG ≈72). For Part 2 I showed a raw / 0.66 / 0.70 sheet and the user picked **0.66 for continuity with Part 1** — when a video is part N≥2 of a series, default to the SAME grade the earlier part shipped (still show the comparison, but recommend matching). edit-NN numbering is now global past edit-16 (edit-17, edit-18 live inside each part's prep folder).

**2026-06-29 — Part 3 = edit-19 BROKE the series-continuity assumption: source was BRIGHTER, 0.66 blew the face.** I rendered with v7-lift 0.66 (series default) and the user rejected it: "очевидно лицо пересвечено" — forehead/cheek blown out, detail lost. Part 3's source measured face-crop RAW YAVG ≈90–94 (vs ≈72 for Parts 1/2) — i.e. a BRIGHTER source, so the 0.66 mid-lift burned it exactly like edit-11. Approved fix = **pure v7-contrast** (mid 0.46, shadows 0.28→0.17, black→0, white held): `curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'` (neutral colorbalance unchanged). Output face luma dropped from ~120+ (blown) to ≈68–73, detail recovered.

**2026-06-29 — Part 4 = edit-20 SHIPPED v7-contrast, NOT 0.66 — a STILL face-crop sheet still under-sold lift's in-MOTION brightness.** The wide 660×860 crop measured ~64 (dimmer than Parts 1/2's ~72), tight face-skin ~104–108 with leaned-in peak 119.8. By the dim-source rule I built the still 5-up at the brightest frame (t=140, in a DROPPED gap) and recommended v7-lift 0.66; user picked it, I rendered. **User then rejected it: "использовал другой грейдинг, не выбранный" — the render LOOKED brighter/flatter than the lift66 still suggested.** It was faithfully lift66 (verified: final YAVG 114.4 vs intended 113.4 at a matched frame) — but on the TALKING / leaned-in frames that dominate the video, lift66 pushes the face to ~130 and reads washed/flat. I then built an **in-motion 3-up at a bright KEPT talking frame** (t=72, raw ~99: v7-contrast / lift60 / lift66) and the brightness/flatness was obvious; user chose **v7-contrast** (the Part 3 grade): `curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'`, neutral colorbalance. Output face luma dropped to ~76–82, modelling restored. **New workflow lesson: a still face-crop sheet — even at the brightest frame — UNDER-SELLS how a lift grade reads in motion on a talking head whose face is usually mid-lit and leaning in. For this subject, build the comparison at a bright KEPT *talking* frame (mouth open / leaned in), not a neutral/dropped still, AND bias the recommendation toward v7-contrast: he has now chosen contrast-over-brightness on BOTH a bright source (Part 3) and a dim-measuring one (Part 4). "Dim measurement → lift" is weaker than assumed when the subject keeps rejecting flat/bright.** Series so far: Parts 1/2 → 0.66; Part 3 (bright) → v7-contrast; Part 4 (dim-measuring but rejected lift) → v7-contrast.

**2026-07-13 — edit-25 ("We keep making AI and Bubble work better together", Bubble/AI standalone, dim): user again chose v7-contrast on a DIM source.** Source measured face-crop RAW YAVG ≈66–71 (dim, uniform across all 13 segments → no per-seg match). 5-up face-crop sheet at a leaned-in talking frame (t=15): raw 69 / v7-contrast 45.5 / lift52 70 / lift58 71.5 / lift66 73.6. By the dim→lift default I expected lift66; user picked **v7-contrast**. The face-crop YAVG 45.5 looks alarmingly dark, but the FULL FRAME reads fine — face clearly modelled, deep-black background, moody/cinematic (the 660×860 crop averages in a lot of hair/shadow, so its number under-reports facial-skin exposure on this framing). Lesson: **"dim source → v7-lift" is only a DEFAULT/expectation, NOT a rule — this subject now prefers contrast-over-brightness even when the measurement is dim (edit-20 Part 4, and now edit-25 standalone). Always show the sheet AND a full-frame of the top candidate, take the explicit call, do not auto-ship lift on a dim reading.**

**Two hard lessons (do NOT repeat):**
1. **Series continuity is a DEFAULT, never a rule.** Within one series the source brightness varies part to part (this series: Parts 1/2 ≈72 dim → 0.66; Part 3 ≈90–94 bright → v7-contrast). ALWAYS measure the face crop and pick by exposure; do not auto-ship the earlier part's grade.
2. **Build the comparison sheet as a FACE CROP at a leaned-in/brightest frame, never a small full-frame.** My first edit-19 sheet was a small full-frame at t=60 (eyes closed) and it HID the blow-out — the user caught it only after the full render. Pick the brightest face frame (scan YAVG across the clip), crop ~660×860 to the face, and ladder several variants (raw / v7-contrast / lift52 / lift58 / lift66) so over/under-exposure is obvious before rendering.
