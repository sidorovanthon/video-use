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
3. **Tools:** `ffmpeg -version` and `ffprobe -version` must work. If they report
   "command not found" they are almost certainly **installed but not on this
   shell's PATH** (winget put them in User PATH, but the tool shell's parent
   predates that entry — `setx`/registry edits do NOT fix the live session).
   Do NOT reinstall: prepend the winget bin to `PATH` in every ffmpeg-using
   command (and helpers that shell out — render.py, grade_sheet.py — inherit the
   shell PATH). Path + exact snippet: memory `reference_ffmpeg_path`. Only if the
   binary genuinely isn't installed: `winget install --id Gyan.FFmpeg -e`.
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
  audio over video (`-c copy`) and cut from that (memory:
  feedback-premade-isolated-audio). The mux target is **`<edit>/source_clean.mp4`
  inside the Phase 2 edit dir**, so create that dir FIRST (do Phase 2 before the
  mux) — writing it to the prep-folder root leaves it in the wrong place and it
  must be moved (per the edit-dir convention, everything lives inside `edit-NN/`).
- Missing transcript → `helpers/transcribe.py` (Scribe; costs money — say so).

## Phase 2 — working dir

Global numbering: find max `edit-*` N across `M:/videos/OBS/edit-*` AND
`M:/videos/OBS/prep/*/edit-*`; create `<prep>/edit-(N+1)/` with
`transcripts/ clips_graded/ verify/`. Stage the transcript as
`transcripts/S0.json` so the EDL key `S0` matches. Everything, including
`final.mp4` + `final.srt`, stays inside this folder.

## Phase 3 — cut plan

`helpers/pack_transcripts.py --edit-dir <edit>` → read `takes_packed.md`.
Drop entirely: false starts / retakes (keep the clean retake) and any big
dead-air gap. Then **split at EVERY `silencedetect` gap ≥ ~0.3 s and trim it to
~0.15 s residual** — pad ~0.075 s into the silence on each side (never clips
speech). A single visually continuous take is **NOT** an exception: its
inter-phrase / inter-sentence pauses (0.4–1.1 s) are joins to trim too, not
"breaths to keep" — preserving them gets flagged as a defect (memory:
feedback-trim-pauses-tight; edit-24 was recut for exactly this). There is no
"only pauses ≥ 1.5 s" threshold — that reading caused the edit-24 miss.
Derive the split points mechanically from `silencedetect` on
`source_clean.mp4`; also verify each segment START (Scribe onset tokens are
degenerate after silences) and tail against the waveform (word.end drifts both
ways). Build `edl.json` (absolute source paths). Cross-check kept text against
the user's script.

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
