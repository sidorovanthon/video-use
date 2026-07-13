# Edit settings reference

Approved settings for OBS talking-head captures on dark backgrounds (1080×1920@60, subject on navy/teal backdrop).

**Sessions:**
- 2026-05-06 (edit-01) — initial recipe, grade v4a
- 2026-05-13 (edit-05) — grade v4a rejected as too dark **twice**; v6 approved (see Color grade section)

Use v6 as the **default starting point** for any new session on this footage class.

## Source profile

- 1080×1920 vertical, 60 fps, h264, AAC stereo 48 kHz
- OBS desktop capture, single-take monologue
- Subject: talking head, dark navy/teal backdrop, neutral indoor lighting (slightly cool)

## Output spec

- 1080×1920 @ **60 fps** (preserved from source)
- libx264, preset `fast`, CRF 20, yuv420p
- AAC 192 kbps, 48 kHz
- `+faststart` for streaming

## Color grade (approved v6 — 2026-05-13)

Bright warm. Significantly lifted midtones for skin presence; background stays deep but never crushed.

> **READ FIRST — pick the grade by SOURCE exposure (added 2026-06-10):** v6 below LIFTS brightness and only suits a DIM source. If the capture is already bright (measure the face crop with `signalstats` — YAVG ≳ 115 / little highlight headroom), do NOT use v6 — it burns the face flat. Use **v7-contrast (grade E)** instead — see the dedicated block below. On edit-11 the user rejected both v6 and a softened v6 as "выжженным / overexposed"; v7-contrast was approved as the template.

```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.05:gm=-0.01:bm=-0.07:rh=0.06:bh=-0.08,
curves=master='0/0.08 0.25/0.32 0.5/0.72 0.85/0.95 1/1'
```

| Stage | Param | Value | Why |
|---|---|---|---|
| `eq` | `contrast` | 1.08 | Mild — leaves room for the curves to do the lifting without crushing |
| `eq` | `saturation` | 0.97 | Slight desat keeps skin natural under added brightness; warm shift below already adds chroma |
| `colorbalance` | `rm` / `bm` | +0.05 / −0.07 | Warm midtones (skin, hair) — **unchanged from v4a, don't touch** |
| `colorbalance` | `gm` | −0.01 | Tiny green pull-back (kills slight teal cast in background) |
| `colorbalance` | `rh` / `bh` | +0.06 / −0.08 | Warm highlights (hair edge, cheek) |
| `curves` | `0 → 0.08` | black floor lift | Background dark but readable (~20/255), no banding |
| `curves` | `0.25 → 0.32` | shadow lift | **Key v6 change** — lifts lower-mid skin shadows; without this the face brightens only on highlights and still reads "dark" |
| `curves` | `0.5 → 0.72` | aggressive midtone bump | **Primary v6 lever** — face forward, skin readable on small phone screens |
| `curves` | `0.85 → 0.95` | highlight lift | Specular skin highlights stay bright, hair edge punches |
| `curves` | `1 → 1` | white anchor | Whites not blown |

**Tuning lever if user says "still too dark":**
1. Push mid `0.5 →` higher (0.72 → 0.78 → 0.82)
2. Raise shadow anchor (0.25 → 0.35 → 0.40)
3. Drop contrast more (1.08 → 1.05)
4. Keep `colorbalance` warm-shift values fixed — they are correct for this subject/backdrop

## Color grade — v7-contrast (grade E, APPROVED 2026-06-10, edit-11) — DEFAULT for BRIGHT sources

**This is the approved template the user asked to keep for future bright-source videos.** Use it whenever the source is already bright (OBS capture with well-lit face). The whole "lift midtones for brightness" idea of v6 is WRONG here — a bright source needs the opposite: **do not raise brightness at all; add contrast, deepen shadows, hold the white point in place** so face detail/modelling comes back instead of washing out.

```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'
```

| Stage | Param | Value | Why |
|---|---|---|---|
| `eq` | `contrast` | 1.08 | Adds punch; the curve does the rest |
| `eq` | `saturation` | 0.97 | Natural skin |
| `colorbalance` | warm | rm+0.04 bm−0.05 rh+0.03 bh−0.04 | **Milder warm than v6** — bright skin needs less push; gm−0.01 kills teal cast |
| `curves` | `0 → 0` | true black | Black point to zero (v6's 0→0.08 floor lift was part of the "washed" look on bright footage) |
| `curves` | `0.25(→0.28) → 0.17` | **deepen shadows** | Pulls shadows DOWN (the key move) — restores depth/contrast under the bright face |
| `curves` | `0.5 → 0.46` | mids slightly DOWN | **No lift** — a hair down so the face stops looking blown |
| `curves` | `0.72 → 0.69` | pull bright face zone down | Recovers detail on the forehead/cheek that was burning out, separating it from the speculars |
| `curves` | `1 → 1` | **white point held** | Keep speculars/whites exactly in place — do not pull the ceiling down (that flattens), do not lift |

**Tuning:** want more punch → deepen shadows (`0.28→0.17` → `0.30→0.14`) and/or pull the bright-face point lower (`0.72→0.69` → `0.72→0.66`); want warmer → nudge rm/rh up a touch. **Never lift mids on a bright source** — that is the exact mistake that made it look "выжженным".

### v6 (2026-05-13) — only for DIM sources
Keep v6 (the lifted curve at the top) ONLY when the face reads dark in the raw source. On edit-11's bright source v6 (and even a softened v6 with mid 0.5→0.64) were rejected as overexposed/burned. Decision rule: **bright source → v7-contrast; dim source → v6 (push mids further if still dark).** Always measure the source face luma + eyeball a graded frame before committing.

> **UPDATE 2026-06-23 (edit-16, "...Part 5") — APPROVED GRADE = "v7-lift" (v7's neutral balance + a lifted curve). This is now the DEFAULT for this "How to Avoid Losing Context" OBS series.** edit-16 measured dim (face YAVG ≈ 81). v6 was rejected — skin "снова уходит в жёлтый" (v6's warm colorbalance bm−0.07/bh−0.08 + heavy mid-lift 0.5→0.72 reads YELLOW). Then **pure v7-contrast was rejected as too dark** on this dim source. The user approved a middle ground from a 4-up comparison (frames in `edit-16/verify/cmp_*`): keep v7's **neutral colorbalance** (kills the yellow) but **lift the curve back up** for brightness. Approved "v7-lift" grade (variant D, mid 0.66):
> ```
> eq=contrast=1.08:saturation=0.97,
> colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
> curves=master='0/0.04 0.28/0.30 0.5/0.66 0.72/0.82 1/1'
> ```
> **Workflow rule for this series: do NOT auto-pick v6 just because the source measures dim. Build a comparison sheet (v6 / pure-v7 / v7-lift mid 0.60 / v7-lift mid 0.66) and let the user pick — they want neutral skin AND adequate brightness, which neither v6 (too yellow) nor pure v7 (too dark) gives.** Brightness lever within v7-lift = the mid point (0.60 ↔ 0.66 ↔ 0.70); keep the neutral colorbalance fixed. **Always show comparison frames before the full render** (explicit user request, edit-16). v6 is retired for this footage.

> **UPDATE 2026-06-29 (edit-19, "Migrating Knowledgebase With AI Part 3") — SERIES CONTINUITY IS A DEFAULT, NOT A RULE. A brighter source needs v7-contrast even mid-series.** Parts 1/2 (edit-17/18) shipped v7-lift 0.66 on dim sources (face YAVG ≈72). I shipped Part 3 with 0.66 too (continuity) and the user rejected it: **"очевидно лицо пересвечено"** — forehead/cheek blown, detail lost. Part 3's source measured BRIGHTER (face-crop RAW YAVG ≈90–94), so the 0.66 mid-lift burned it exactly like edit-11. Approved fix = **pure v7-contrast** (the edit-11/14 grade): mid 0.46, shadows 0.28→0.17, black→0, white held, neutral colorbalance:
> ```
> eq=contrast=1.08:saturation=0.97,
> colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
> curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'
> ```
> Output face luma dropped from ~120+ (blown) to ≈68–73, detail recovered, skin neutral, deep black bg. User: "Да, так супер." **Two workflow rules this enforces:**
> 1. **ALWAYS measure the source face crop and pick the grade by exposure — never auto-ship the earlier part's grade.** Within one series the source brightness varies part to part (this series: 72 dim → v7-lift 0.66; 90–94 bright → v7-contrast).
> 2. **Build the comparison sheet as a FACE CROP (~660×860) at the BRIGHTEST/leaned-in frame** (scan YAVG across the clip to find it), laddering raw / v7-contrast(0.46) / lift52 / lift58 / lift66. A small full-frame still (esp. eyes-closed) HIDES blow-out — that mistake on edit-19 let an overexposed render reach the user. Decision rule restated: **bright source → v7-contrast; dim source → v7-lift (mid 0.60–0.70).**

> **UPDATE 2026-07-06 (edit-21, "Migrating Knowledgebase With AI Part 5") — v7-contrast again.** Source measured dim overall but face-skin crop ~92–106 (brightest t=100 ≈106) — same band as Part 3/4. Built the 5-up face-crop sheet (raw/v7-contrast/lift52/lift58/lift66); output face luma raw 106 / v7-contrast 85 / lift52 98 / lift58 110 / lift66 125. User picked **v7-contrast** (deep shadows, neutral warm skin, modelling) — lift66 (~125) reads blown/flat exactly as on Part 4. This footage class keeps converging on v7-contrast; still measure + show the sheet every time.

> **UPDATE 2026-07-06 (edit-22, "Migrating Knowledgebase With AI Part 6") — v7-contrast again.** Face-crop raw YAVG ≈88–96 (brightest t=68 ≈96), same band as Parts 3/4/5. 5-up sheet output luma: raw96 / v7-contrast72 / lift52-84 / lift58-95 / lift66-110; user picked **v7-contrast**, lift66 blew the forehead as before. Pre-made isolated.mp3 + transcript.json were supplied → muxed clean audio over video, no ElevenLabs re-run. The whole "Migrating Knowledgebase" sub-series (Parts 3–6) has landed on v7-contrast every time.

> **UPDATE 2026-07-06 (edit-23, "Migrating Knowledgebase With AI Part 7 - Grand Finale") — v7-contrast again (BRIGHTEST source of the sub-series).** Face-crop raw YAVG split by half: front ≈107–119 (brightest kept t=23 ≈114), back ≈78–81 — noticeably brighter than Parts 3–6 (88–106). 5-up sheet at t=23 output luma: raw114 / **v7-contrast96** / lift52-111 / lift58-123 / lift66-138; user picked **v7-contrast** (lift58/66 blow the forehead hard on this bright front half). Pre-made isolated.mp3 + transcript.json → muxed clean audio, no ElevenLabs re-run. Parts 3–7 have ALL landed on v7-contrast. SRT script fixes this part: "AA"→"AI" (The AA agent), "run"→"ran" (itself run), inserted "a" (written by a human being).
> **BUT the exposure DRIFTS within this take** (front raw ~108–114, back ~78–83) — a uniform v7-contrast left the back half at graded face Y≈47–56 vs front ≈87 and the user flagged the 44.98s cut as "significantly darker, like a different grade." Fix = **per-segment gamma exposure-match**: pre-normalize each darker segment with `eq=gamma=G` before v7-contrast so all faces land ~85–93. Gammas B3 1.08 / B4 1.42 / B5 1.33 / B6 1.32 / B7 1.30 / OUTRO 1.33 (front segments unchanged). render.py now supports a per-range `"grade"` field for this. See the per-segment-exposure-match memory. **Lesson: measure face luma of EVERY kept segment, not just the brightest — this footage can have a mid-clip exposure step.**

**Anti-patterns / rejected variants:**
- **v4a (2026-05-06)** contrast 1.18, mid 0.5→0.55, shadow 0.25→0.25 → user feedback: too dark, twice (sessions edit-01 retry, edit-05 retry)
- **v5 (2026-05-13 intermediate)** contrast 1.15, mid 0.5→0.62, shadow 0.25→0.25 → still too dark
- Contrast > 1.20 + shadow crush at 0.15→0.10 → plasticky
- Saturation ≤ 0.93 with curve lift → zombie-pale skin
- Black floor at 0 → backdrop noise floor + banding in compression

Apply per-segment during extraction (Hard Rule — never post-concat, doubles re-encode).

## Audio

Two-pass loudnorm targeting **social-media spec**:

```
I=-14 LUFS
TP=-1 dBTP
LRA=11 LU
linear=true
```

- Source measured at −26.10 LUFS / TP −6.91 / LRA 2.90 → +12 dB gain applied
- 30 ms `afade` in/out at every segment boundary (prevents pops at cuts)
- Output AAC 192 kbps stereo 48 kHz

## Cuts

- Working pad window: 30–200 ms past word boundaries
- **Speech-edge padding:** ~50 ms head, ~80 ms tail
- **Dead-air trim padding (when cutting silence within a take):** 100 ms head, 200 ms tail → leaves ~300–400 ms residual silence at the join (natural breath, not robotic)
- Snap edges to word `start`/`end` from Scribe verbatim transcript
- Prefer silence gaps ≥ 400 ms as cut targets
- **Always pre-scan for retakes:** if the speaker stutters or false-starts mid-monologue and re-attempts the same line, drop the false start and keep the clean retake. Look for repeated phrase openings ("And then you watch as, and then you watch as…", "You check and the task turns…" followed later by a clean "You check and the task turns out to be…").
- **Always pre-scan for dead-air pauses ≥ ~1.5 s inside otherwise-kept regions** and split the segment to remove them. The OBS take usually has 1–3 such pauses that need trimming.

## Subtitles

- File-only deliverable (`master.srt`), no burn-in
- 2-word UPPERCASE chunks, break on punctuation
- Generated via `build_master_srt(edl, edit_dir, out)` from per-source transcripts using output-timeline offsets: `out_t = word.start − seg_start + seg_offset`
- **EDL source key must match transcript filename basename.** `build_master_srt` resolves the transcript via `transcripts/<source_key>.json`. If using a short alias like `S0` in the EDL, copy the long-filename transcript to `transcripts/S0.json` so the lookup hits.
- **Always cross-check against the user's script if provided.** Scribe mishearings to fix on this subject have included: `CLOUD` → `CLAUDE`, `CO-WORK` → `COWORK`, `A-A-A` → `AI` (stutter/mishearing of "AI", edit-14). Apply as plain `str.replace` on the rendered SRT.

If burn-in is wanted later for vertical 9:16:
```
FontName=Helvetica, FontSize=18, Bold=1
PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000
BorderStyle=1, Outline=2, Shadow=0
Alignment=2, MarginV=90   # safe-zone for TikTok / Reels / Shorts UI
```

## Output location (updated 2026-06-23)

**The ENTIRE `edit-NN/` working folder lives INSIDE the source/prep folder** — i.e. `M:/videos/OBS/prep/<dated stem>/edit-NN/`, NOT `M:/videos/OBS/edit-NN/`. Everything (edl.json, S0.mp4, master.srt, transcripts/, clips_graded/, verify/, progress.md, AND the deliverables final.mp4 + final.srt) sits in that one folder, right next to the originals. The prep folder root keeps only the untouched originals (`<source>.mp4`, `isolated.mp3`, `transcript.json`) plus the `edit-NN/` subfolder. EDL `sources` paths are absolute and include the prep stem.

## Render command

```bash
# work dir = <source_dir>/edit-NN ; final lands in the SAME edit-NN folder
uv run helpers/render.py "<source_dir>/edit-NN/edl.json" \
  -o "<source_dir>/edit-NN/final.mp4" \
  --no-subtitles \
  --fps 60
# then: cp "<source_dir>/edit-NN/master.srt" "<source_dir>/edit-NN/final.srt"
```

To rebuild SRT only:
```python
from helpers.render import build_master_srt
build_master_srt(json.loads(open('edl.json').read()), Path('<edit>'), Path('<edit>/master.srt'))
```

## Pipeline order (do not deviate)

1. Per-segment extract with grade + 30 ms audio fades baked in
2. Lossless `-c copy` concat → `base.mp4`
3. Composite overlays (PTS-shifted) — none in this session
4. Subtitles LAST in filter chain — skipped here
5. Two-pass loudnorm → `final.mp4`
