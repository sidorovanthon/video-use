# OBS talking-head edit settings — canonical reference

Approved settings for anticodeguy's OBS vertical talking-head captures (1080×1920@60, subject on dark navy/teal backdrop, single-take monologue). **This git-backed copy is the single source of truth as of 2026-07-13** (relocated from `M:/videos/OBS/edit-01/settings_reference.md`, which now holds a pointer here). The full append-only history of that file is preserved in this repo's git history.

## Source profile

- 1080×1920 vertical, 60 fps, h264, AAC stereo 48 kHz
- OBS desktop capture, single-take monologue with false starts/retakes
- Subject: talking head, dark navy/teal backdrop, neutral indoor lighting (slightly cool)

## Output spec

- 1080×1920 @ **60 fps** (preserved from source — render.py now preserves source fps by default; `--fps 60` forces it)
- libx264, preset `fast`, CRF 20, yuv420p
- AAC 192 kbps, 48 kHz, `+faststart`

## Color grade — decision rule (the part that matters)

**Measure first, never inherit.** For every new video — even mid-series:

1. **Measure the face-crop luma (`signalstats` YAVG) of EVERY kept segment**, not just one frame — exposure can step mid-take (edit-23: front ~107–114, back ~78–83).
2. **Build a 5-up FACE-CROP comparison sheet (~660×860) at the brightest leaned-in TALKING frame** (scan YAVG across the clip to find it): raw / v7-contrast / lift52 / lift58 / lift66. A small full-frame still — especially eyes-closed — hides blow-out (that mistake let an overexposed render reach the user on edit-19).
3. **Show the sheet and let the user pick before the full render.** Explicit user request (edit-16). Series continuity is a default, never a rule (edit-19 lesson: "очевидно лицо пересвечено").

Decision rule: **bright source (face YAVG ≳ 88) → v7-contrast; dim source → v7-lift (mid 0.60–0.70).**

Series defaults (both still get the sheet):
- **"How to Avoid Losing Context …"** (dim sources, YAVG ~72–81) → **v7-lift mid 0.66**
- **"Migrating Knowledgebase With AI"** (bright sources, YAVG ~88–114) → **v7-contrast** — Parts 3–7 landed on it every time; any mid-lift blows the forehead

### v7-contrast (grade E — approved 2026-06-10 edit-11; default for BRIGHT sources)

No brightness lift: add contrast, deepen shadows, hold the white point.

```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'
```

Key moves: true black (0→0), shadows pulled DOWN (0.28→0.17), mids a hair down (0.5→0.46), bright-face zone pulled down (0.72→0.69) to recover forehead/cheek detail, white point held (1→1). Neutral-warm colorbalance (milder than v6) kills the teal cast without yellowing skin.
Tuning: more punch → shadows 0.30→0.14 and/or face point 0.72→0.66; warmer → nudge rm/rh up a touch. **Never lift mids on a bright source.**

### v7-lift (variant D — approved 2026-06-23 edit-16; default for DIM sources)

v7's neutral colorbalance (kills v6's yellow skin) + a lifted curve for brightness.

```
eq=contrast=1.08:saturation=0.97,
colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04,
curves=master='0/0.04 0.28/0.30 0.5/0.66 0.72/0.82 1/1'
```

Brightness lever = the mid point (0.60 ↔ 0.66 ↔ 0.70); keep the neutral colorbalance fixed.

### Per-segment exposure match (edit-23 rule)

If kept segments' face luma differs materially, pre-normalize each darker segment with `eq=gamma=G` **before** the grade chain so all faces land in one band (~85–93). Use render.py's per-range `"grade"` field in the EDL: darker ranges get `eq=gamma=G,<grade chain>`, the rest use the EDL-level grade. Edit-23 approved gammas: B3 1.08 / B4 1.42 / B5 1.33 / B6 1.32 / B7 1.30 / OUTRO 1.33. A uniform grade on drifting exposure reads as "a different grade after the cut" (user flagged the 44.98s join).

### Retired / anti-patterns

- **v6** (2026-05-13, lifted warm grade: colorbalance rm+0.05/bm−0.07/rh+0.06/bh−0.08, curve 0/0.08 0.25/0.32 0.5/0.72 0.85/0.95 1/1) — retired 2026-06-23: warm balance + heavy mid-lift reads YELLOW on skin; only historical.
- v4a (contrast 1.18, mid 0.55) and v5 (contrast 1.15, mid 0.62) — rejected as too dark (edit-01/05, twice).
- Contrast > 1.20 + shadow crush 0.15→0.10 → plasticky. Saturation ≤ 0.93 with curve lift → zombie-pale skin. Black floor at 0 on dim/lifted grades → banding.
- Mid-lift (lift58/lift66) on bright faces (YAVG ≳ 88) → blown forehead, rejected on edit-11/19/20/21/22/23.

Apply the grade per-segment during extraction (Hard Rule — never post-concat, doubles re-encode).

## Audio

Two-pass loudnorm, social-media spec: `I=-14 LUFS, TP=-1 dBTP, LRA=11 LU, linear=true`. Typical source ≈ −26 LUFS → ~+12 dB gain. 30 ms `afade` in/out at every segment boundary (prevents pops). AAC 192 kbps stereo 48 kHz.

## Cuts

- Snap edges to Scribe word `start`/`end`; working pad 30–200 ms past word boundaries; speech-edge padding ~50 ms head / ~80 ms tail.
- **Trim every join tight (~0.15 s residual)** — this user flags preserved 400–600 ms breaths as defects; verify joins with `silencedetect`.
- Prefer silence gaps ≥ 400 ms as cut targets.
- **Always pre-scan for retakes** (repeated phrase openings → drop the false start, keep the clean retake) and for dead-air pauses ≥ ~1.5 s inside kept regions (split and trim; usually 1–3 per take).
- Scribe caveats: verify segment STARTs with `silencedetect` (onset tokens after long silences are degenerate); read the waveform tail for closing words (word.end drifts both ways); see the project memory for the full list.

## Subtitles

- File-only deliverable (`final.srt` from working `master.srt`), no burn-in. 2-word UPPERCASE chunks, break on punctuation.
- Generated via `build_master_srt(edl, edit_dir, out)`; output time = `word.start − seg_start + seg_offset`; membership is start-based (`seg_start ≤ word.start < seg_end`) to avoid double-captioning a word straddling a split.
- **EDL source key must match the transcript filename**: with alias `S0`, copy the transcript to `transcripts/S0.json`.
- **Always cross-check against the user's script if provided.** Known Scribe fixes on this subject: `CLOUD`→`CLAUDE`, `CO-WORK`→`COWORK`, `A-A-A`/`AA`→`AI`, tense/article slips ("run"→"ran"). Apply as plain `str.replace` on a filtered transcript COPY — never edit the cached transcript.
- Burn-in spec, if ever wanted (9:16 safe-zone): FontName=Helvetica, FontSize=18, Bold=1, PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000, BorderStyle=1, Outline=2, Shadow=0, Alignment=2, MarginV=90.

## Output location (edit-16+ convention)

**The ENTIRE `edit-NN/` working folder lives INSIDE the source/prep folder**: `M:/videos/OBS/prep/<dated stem>/edit-NN/`. Everything — edl.json, working video, transcripts/, clips_graded/, verify/, master.srt, progress notes, AND deliverables `final.mp4` + `final.srt` — sits there. The prep folder root keeps only untouched originals (`<source>.mp4`, `isolated.mp3`, `transcript.json`). EDL `sources` paths are absolute with the prep stem. Numbering `edit-NN` is global across all videos.

Pre-supplied `isolated.mp3` + `transcript.json` in the prep folder → do NOT re-run ElevenLabs; mux clean audio over video (`-c copy`) into `source_clean.mp4` and cut from that.

## Render command

```bash
uv run helpers/render.py "<prep>/edit-NN/edl.json" \
  -o "<prep>/edit-NN/final.mp4" \
  --no-subtitles \
  --fps 60
# then: cp "<prep>/edit-NN/master.srt" "<prep>/edit-NN/final.srt"
```

SRT-only rebuild:

```python
from helpers.render import build_master_srt
build_master_srt(json.loads(open('edl.json').read()), Path('<edit>'), Path('<edit>/master.srt'))
```

## Pipeline order (do not deviate)

1. Per-segment extract with grade + 30 ms audio fades baked in
2. Lossless `-c copy` concat → `base.mp4`
3. Composite overlays (PTS-shifted) — usually none
4. Subtitles LAST in filter chain — usually skipped (file-only SRT)
5. Two-pass loudnorm → `final.mp4`

## Grade history (compact per-part log)

| Date | Edit | Video | Outcome |
|---|---|---|---|
| 2026-05-06 | edit-01 | (first) | v4a initial; rejected too dark |
| 2026-05-13 | edit-05 | — | v4a rejected twice → **v6** approved |
| 2026-06-10 | edit-11 | Losing Context | v6 + softened v6 rejected "выжженным" on bright source → **v7-contrast** approved |
| 2026-06-23 | edit-16 | Losing Context P5 | dim (YAVG≈81); v6 yellow, pure v7 too dark → **v7-lift 0.66** from 4-up sheet; v6 retired |
| 2026-06-29 | edit-19 | Migrating P3 | brighter (90–94); auto-shipped 0.66 rejected "пересвечено" → **v7-contrast** |
| 2026-06-29 | edit-20 | Migrating P4 | wrong (unchosen) grade shipped, flagged → **v7-contrast**; lift66 blows forehead |
| 2026-07-06 | edit-21 | Migrating P5 | face 92–106; 5-up sheet → **v7-contrast** (lift66 output ~125 = blown) |
| 2026-07-06 | edit-22 | Migrating P6 | face 88–96; **v7-contrast**; pre-made isolated audio muxed |
| 2026-07-06 | edit-23 | Migrating P7 finale | brightest front (~114) + mid-take exposure drift → **v7-contrast + per-segment gamma match** |
| 2026-07-13 | edit-24 | Bubble/AI (standalone) | very dim, uniform (face YAVG ~43–45, no per-seg match) → **v7-lift 0.66** from 5-up sheet; dropped 2 false starts. First pass left inter-phrase pauses in the continuous body take → user flagged → recut into 16 phrase segments, every ≥0.3s pause trimmed to ~0.15s (73.4→67.8s) |
