---
name: feedback-render-fps-default
description: "helpers/render.py extract default was -r 24, which broke the OBS 60fps \"preserve from source\" recipe — patched to -r 60"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a786288-dde3-481e-ad3a-fd43bbda0a9a
---

`helpers/render.py` per-segment extract framerate defaults to 24fps, which silently downsamples OBS 1080×1920@60 talking-head sources unless overridden.

**Git is authoritative, not this memory** — the user corrected an earlier false claim here. The published `browser-use/video-use` repo had `-r "24"` hardcoded and **no** `--fps` flag; the prior "patched 24→60 on 2026-05-25" note was simply wrong (no such patch ever existed in the repo). The skill docs (SKILL.md Output spec) say "Match the source unless asked" — so the hardcoded 24 is a real bug, not just a missing flag.

Fixed 2026-06-01 as **PR #55** (branch `fix/preserve-source-fps` on the user's fork → browser-use/video-use): `probe_source_fps()` reads `r_frame_rate` and the render **preserves source fps by default** (falls back to 24 only if unprobeable); `--fps N` is an optional override. Not merged yet — local `main` still has the hardcoded 24 until the PR lands.

**Review iteration:** the `cubic-dev-ai` bot flagged a valid P2 — resolving fps *per segment* would make a multi-source EDL mixing rates (30+60fps) produce heterogeneous segments that break the `-c copy` concat (Hard Rule 2 needs uniform fps). Fixed in commit `ae0e6af`: resolve **one** rate in `extract_all_segments` (explicit `--fps` else first source's rate) and pass it to every segment; `extract_segment` now takes a resolved `rate` str. Lesson: when adding per-source behavior, check it doesn't break the uniform-stream assumption the lossless concat depends on.

**Re-confirmed 2026-06-02 (Bubble video session):** local `main` render.py still had `-r "24"` hardcoded and no `--fps` flag (PR #55 still unmerged). Re-added a minimal `--fps` arg threaded through `extract_all_segments`→`extract_segment` and rendered with `--fps 60`; verified `r_frame_rate=60/1`. This local edit is uncommitted and will be lost on the next clean checkout until #55 lands.

**How to apply:** once PR #55 merges, default behavior already preserves 60fps for OBS — no flag needed. Until then, on a fresh checkout either cherry-pick the branch or pass an explicit rate. Always verify `r_frame_rate=60/1` on the rendered output before declaring done. See [[feedback-render-concat-apostrophe]] (PR #54) for the other render.py fix submitted the same session.
