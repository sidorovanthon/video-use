# CLAUDE.md — anticodeguy's video-use working copy

Fork of browser-use/video-use used to edit the user's OBS vertical talking-head
videos (1080×1920@60). The general pipeline mechanics live in the root
`SKILL.md`; everything user-specific lives in:

- **`docs/settings_reference.md`** — the canonical edit recipe (grade decision
  rule, audio, cuts, subtitles, output convention, pipeline order). Single
  source of truth; update it here, not on M:.
- **Project memory** (auto-loaded) — correction history; `feedback_*` rules are
  binding. Mirrored to `.claude/memory-mirror/` for durability.

## Commands

- **`/video <prep folder or mp4>`** — start processing a new video. Always use
  this instead of an ad-hoc prompt: it runs the mechanical freshness gate
  (repo up to date, clean tree, ffmpeg present, memory mirrored, fork pushed)
  before any editing starts.
- **`/wrap`** — end-of-session retro + hygiene (commit, mirror memory,
  push to fork, handoff).

## Hard local rules

- Before editing, run `python helpers/check_repo_freshness.py` and require PASS.
  `origin` is upstream; `fork` is our backup. Preserve local commits by merging
  upstream changes into main, testing, and pushing to fork; see `/video` Phase 0.
- Working dir convention: every video lives under its script month at
  `M:/videos/OBS/prep/YYYY-MM/YYYY-MM-DD[-NN] - <title> [REC YYYY-MM-DD]/`.
  The leading date and optional sequence are the script chronology; `REC` is
  the recording date. `<title>` is truncated to ~22 chars with a trailing
  `...` — resolve folders by the date prefix, never by full title. Script-date
  grouping means the month folder ≠ the REC month and `edit-NN` numbering no
  longer runs in month order. Active jobs may temporarily retain the legacy
  `YYYY-MM-DD <title>` recording-date name until their edit is complete. The WHOLE `edit-NN/` folder,
  including `final.mp4` + `final.srt`, lives inside that video folder;
  `edit-NN` numbering is global. (Overrides root SKILL.md's
  `<videos_dir>/edit/` rule.)
- `_STATUS_EDITED_EXTERNALLY.md` marks videos whose `REC` month matches the
  marker's month as finished external edits (for example, Premiere Pro), even
  if script-date grouping places those video folders under another month.
- Grade is chosen by measurement via `helpers/grade_sheet.py` (scan → sheet →
  explicit user choice). Never auto-ship a previous part's grade.
- Pre-made `isolated.mp3` + `transcript.json` in the prep folder → never re-run
  ElevenLabs; mux and cut from `source_clean.mp4`.
- Never leave pipeline fixes uncommitted at session end; push `main` to `fork`
  (sidorovanthon/video-use) — single-copy state already died once (2026-07).
