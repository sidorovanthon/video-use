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

- Working dir convention: the WHOLE `edit-NN/` folder, including `final.mp4` +
  `final.srt`, lives inside `M:/videos/OBS/prep/<dated stem>/`; `edit-NN`
  numbering is global. (Overrides root SKILL.md's `<videos_dir>/edit/` rule.)
- Grade is chosen by measurement via `helpers/grade_sheet.py` (scan → sheet →
  explicit user choice). Never auto-ship a previous part's grade.
- Pre-made `isolated.mp3` + `transcript.json` in the prep folder → never re-run
  ElevenLabs; mux and cut from `source_clean.mp4`.
- Never leave pipeline fixes uncommitted at session end; push `main` to `fork`
  (sidorovanthon/video-use) — single-copy state already died once (2026-07).
