---
name: project-edit-dir-convention
description: As of edit-16 the WHOLE edit-NN/ folder lives INSIDE the source/prep folder (M:/videos/OBS/prep/<stem>/edit-NN/); ALL files incl. finals go there; global edit-NN numbering continues
metadata: 
  node_type: memory
  type: project
  originSessionId: 2731bad5-8472-4d04-b84a-e2c5d71dab35
---

For the OBS talking-head work, each video gets its own numbered working directory **inside its prep folder**: `M:/videos/OBS/prep/<dated stem>/edit-NN/` — NOT `M:/videos/OBS/edit-NN/` (the pre-edit-16 layout) and NOT the video-use skill's Hard-Rule-12 single `<videos_dir>/edit/`. Numbering is GLOBAL and continues across all videos: new video = next number after the highest existing `edit-*` anywhere under `M:/videos/OBS/` (both the old flat layout and the prep subfolders).

Everything lives in that one `edit-NN/` folder: `edl.json`, working `S0.mp4`/`source_clean.mp4`, `transcripts/`, `clips_graded/`, `verify/`, `master.srt`, progress notes, **and the deliverables `final.mp4` + `final.srt`**. The prep folder root keeps only the untouched originals (`<source>.mp4`, `isolated.mp3`, `transcript.json`) plus the `edit-NN/` subfolder. EDL `sources` paths are absolute and include the prep stem.

**Why:** the user keeps every video's full output for comparison across iterations, co-located with its source.

**How to apply:** on a new video, scan for the max existing `edit-*` N, create `prep/<stem>/edit-(N+1)/` with `transcripts/ clips_graded/ verify/` subdirs. Stage the supplied transcript as `transcripts/S0.json` and the muxed working video so the EDL source key `S0` matches both. Pre-supplied isolated.mp3 + transcript.json: see [[feedback-premade-isolated-audio]]. Canonical recipe: [[reference-video-use-settings]].

*(Restored 2026-07-13 from a 2026-06-23 file-history snapshot after NUL corruption, updated to the final edit-16+ convention per MEMORY.md and settings_reference.md.)*
