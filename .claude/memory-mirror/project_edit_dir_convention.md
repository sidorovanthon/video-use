---
name: project-edit-dir-convention
description: As of edit-16 the WHOLE edit-NN/ folder lives INSIDE the source/prep folder (M:/videos/OBS/prep/YYYY-MM/'YYYY-MM-DD[-NN] - <title> [REC YYYY-MM-DD]'/edit-NN/, script month, truncated title); ALL files incl. finals go there; global edit-NN numbering continues
metadata: 
  node_type: memory
  type: project
  originSessionId: 2731bad5-8472-4d04-b84a-e2c5d71dab35
---

For the OBS talking-head work, each video gets its own numbered working directory **inside its prep folder**: `M:/videos/OBS/prep/YYYY-MM/YYYY-MM-DD[-NN] - <title> [REC YYYY-MM-DD]/edit-NN/` — the month level is part of the path.

**Folder naming (renamed 2026-08-24, second pass):** the month is the **SCRIPT** month, not the recording month; the leading `YYYY-MM-DD[-NN]` is the script/publication date with `-NN` ordering several videos written for the same script date; `[REC YYYY-MM-DD]` carries the recording date. `<title>` is **truncated to ~22 chars with a trailing `...`** (`Организация базы знан...`, `Не допускай Codex к к...`), so NEVER resolve a folder by its full title — glob the date prefix or `*edit-NN*`. Consequence: `edit-NN` numbering no longer runs in month order (edit-01..27 under `2026-02`, edit-28..30 under `2026-03`, edit-39..42 under `2026-04`, while `2026-05` holds unedited videos and `2026-06`/`2026-07` are now empty). A month's `_STATUS_EDITED_EXTERNALLY.md` marks only the videos whose **REC month equals that marker's month**, not everything physically in the folder. Legacy `YYYY-MM-DD <title>` recording-date names may still linger on active jobs. The pre-edit-16 flat layout `M:/videos/OBS/edit-NN/` is gone; every edit, edit-01 through edit-45, now sits under `prep/YYYY-MM/`, so scan recursively (`prep/*/*/edit-*`) and never expect a flat `edit-NN`. Also NOT the video-use skill's Hard-Rule-12 single `<videos_dir>/edit/`. Numbering is GLOBAL and continues across all videos: new video = next number after the highest existing `edit-*` anywhere under `M:/videos/OBS/prep/*/*/edit-*` (highest as of 2026-08-31 = edit-45).

Everything lives in that one `edit-NN/` folder: `edl.json`, working `S0.mp4`/`source_clean.mp4`, `transcripts/`, `clips_graded/`, `verify/`, `master.srt`, progress notes, **and the deliverables `final.mp4` + `final.srt`**. The prep folder root keeps only the untouched originals (`<source>.mp4`, `isolated.mp3`, `transcript.json`) plus the `edit-NN/` subfolder. EDL `sources` paths are absolute and include the prep stem.

**Why:** the user keeps every video's full output for comparison across iterations, co-located with its source.

**How to apply:** on a new video, scan for the max existing `edit-*` N, create `prep/YYYY-MM/<video folder>/edit-(N+1)/` with `transcripts/ clips_graded/ verify/` subdirs. Stage the supplied transcript as `transcripts/S0.json` and the muxed working video so the EDL source key `S0` matches both. Pre-supplied isolated.mp3 + transcript.json: see [[feedback-premade-isolated-audio]]. Canonical recipe: [[reference-video-use-settings]].

*(Restored 2026-07-13 from a 2026-06-23 file-history snapshot after NUL corruption, updated to the final edit-16+ convention per MEMORY.md and settings_reference.md.)*
