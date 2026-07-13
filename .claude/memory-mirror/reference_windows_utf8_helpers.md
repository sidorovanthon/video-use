---
name: reference-windows-utf8-helpers
description: video-use python helpers crash on Windows cp1251 console when printing the → char; run with PYTHONIOENCODING=utf-8 PYTHONUTF8=1
metadata: 
  node_type: memory
  type: reference
  originSessionId: a34afa00-c6b3-47e2-baf2-bd301b7a3193
---

On this Windows box the console is cp1251. `helpers/pack_transcripts.py` and `helpers/render.py`'s `build_master_srt` print a `→` (U+2192) in their success message, which raises `UnicodeEncodeError: 'charmap' codec can't encode character '→'` and exits non-zero.

**Key fact:** the output files (`takes_packed.md`, `master.srt`) are written *before* the crashing print, so the artifacts are correct even when the command reports failure. Don't assume the file is missing.

**How to apply:** run these helpers with `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` prefixed to avoid the crash entirely. When calling `build_master_srt` inline, also read/write SRT with `encoding='utf-8'`.
