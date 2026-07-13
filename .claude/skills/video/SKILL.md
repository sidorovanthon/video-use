---
name: video
description: Start processing a new OBS talking-head video — /video <path to prep folder or mp4>. Runs the mechanical freshness/environment gate, then drives the full standard pipeline (mux clean audio, cuts, grade gate, render, SRT) per the canonical recipe. Project-local; this repo only.
---

# video — one path in, finished video out

Replaces the hand-typed opener prompt. Input: one argument — the prep folder
(`M:/videos/OBS/prep/<dated stem>/`) or the source mp4 inside it.

Canon: `docs/settings_reference.md` (this repo) — read it before cutting.
Project memory (auto-loaded) holds the correction history; obey `feedback_*` rules.

## Phase 0 — freshness & environment gate (mechanical, BEFORE any work)

Run all checks; do not start editing on a stale/dirty/broken setup:

1. **Repo freshness:** `git fetch origin && git status -sb`. If behind
   `origin/main` → `git pull --ff-only` (if it can't fast-forward, STOP and
   show the divergence). If the working tree is dirty → show the diff and
   resolve (commit or stash) before proceeding — uncommitted pipeline fixes
   died in the 2026-07 data loss.
2. **Deps:** if the pull changed `pyproject.toml` → `uv sync`.
3. **Tools:** `ffmpeg -version` and `ffprobe -version` must work (fresh shells
   get them from PATH; if missing: `winget install --id Gyan.FFmpeg -e`).
   `ELEVENLABS_API_KEY` in `.env` is only needed if transcription will run.
4. **Memory mirror (durability):** copy
   `~/.claude/projects/C--Users-sidor-repos-video-use/memory/*.md` →
   `.claude/memory-mirror/`; if changed, commit.
5. **Off-disk backup:** if `main` is ahead of `fork/main` → `git push fork main`.

## Phase 1 — resolve inputs

- Arg is the prep folder (an mp4 arg → use its parent folder).
- Inventory the folder: source `<stem>.mp4`; pre-made `isolated.mp3` +
  `transcript.json`; the user's script text (for SRT cross-check) if present.
- **Pre-made isolated audio present → do NOT re-run ElevenLabs** — mux clean
  audio over video (`-c copy`) into `source_clean.mp4` and cut from that
  (memory: feedback-premade-isolated-audio).
- Missing transcript → `helpers/transcribe.py` (Scribe; costs money — say so).

## Phase 2 — working dir

Global numbering: find max `edit-*` N across `M:/videos/OBS/edit-*` AND
`M:/videos/OBS/prep/*/edit-*`; create `<prep>/edit-(N+1)/` with
`transcripts/ clips_graded/ verify/`. Stage the transcript as
`transcripts/S0.json` so the EDL key `S0` matches. Everything, including
`final.mp4` + `final.srt`, stays inside this folder.

## Phase 3 — cut plan

`helpers/pack_transcripts.py --edit-dir <edit>` → read `takes_packed.md`.
Pre-scan retakes (drop false starts, keep clean retakes) and dead-air pauses
≥ ~1.5 s inside kept regions. Verify segment STARTs with `silencedetect`
(Scribe onset tokens are degenerate after silences) and tails against the
waveform (word.end drifts both ways). Trim every join to ~0.15 s residual —
preserved breaths get flagged as defects. Build `edl.json` (absolute source
paths). Cross-check kept text against the user's script.

## Phase 4 — GRADE GATE (mandatory, mechanical — never inherit a grade)

```bash
python helpers/grade_sheet.py scan <edit>/edl.json          # per-segment face luma
python helpers/grade_sheet.py sheet <edit>/edl.json --time <brightest talking frame>
```

- Segments differ materially → per-range `"grade"` with `eq=gamma=G`
  pre-normalization before the grade chain (target one band, ~85–93).
- **SHOW the sheet and wait for an explicit grade choice before rendering.**
  Series defaults ("Losing Context" → v7-lift, "Migrating" → v7-contrast) are
  expectations, not decisions.

## Phase 5 — render & subtitles

```bash
uv run helpers/render.py <edit>/edl.json -o <edit>/final.mp4 --no-subtitles --fps 60
```

`build_master_srt` → `master.srt`; apply script fixes (`CLOUD`→`CLAUDE` etc.)
on a filtered transcript COPY, never the cache; `cp master.srt final.srt`.

## Phase 6 — verify before declaring done

Frames at every join (no visible grade/exposure step), `silencedetect` on
joins (~0.15 s), `r_frame_rate` = 60/1, loudness ≈ −14 LUFS, SRT spot-check
against the script. Show the user 2–3 verification frames.

## Phase 7 — wrap-up

New lesson learned → memory file + `MEMORY.md` line + refresh
`.claude/memory-mirror/`; grade outcome → append to the history table in
`docs/settings_reference.md`; commit; suggest `/wrap` at session end.
