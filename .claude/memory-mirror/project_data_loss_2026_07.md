---
name: project-data-loss-2026-07
description: "2026-07 system reinstall NUL-corrupted all session logs (unrecoverable; M: backup identical) and 4 memory files (restored 2026-07-13 from file-history); durable state must live in git, not single-copy dirs"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2731bad5-8472-4d04-b84a-e2c5d71dab35
---

Around 2026-07-10/11 the user reinstalled the system and disk data loss NUL-corrupted: all 16 session logs for this project (95–100% NUL; the copy at `M:/backup/sidor/.claude/` was taken from the already-corrupted disk — identical damage, unrecoverable) and 4 project memory files. On 2026-07-13 the memory files were restored: `feedback_grade_migrating_series` + `project_edit_dir_convention` from `~/.claude/file-history/` snapshots, `feedback_exposure_match_segments` + `reference_video_use_settings` reconstructed from MEMORY.md one-liners + settings_reference.md.

**Why:** single-copy state (working-tree-only code fixes, one memory dir, ad-hoc files on M:) does not survive a reinstall.

**How to apply:** durable state lives in git and gets pushed to the fork (`fork` remote = sidorovanthon/video-use): pipeline fixes committed (never carried dirty), the canonical recipe in `docs/settings_reference.md`, and the memory dir mirrored into the repo at `.claude/memory-mirror/` at session start/end (the `/video` and `/wrap` skills both do this). `~/.claude/file-history/<session-id>/` is the recovery source of last resort for files Claude edited.
