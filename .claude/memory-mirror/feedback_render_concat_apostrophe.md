---
name: feedback-render-concat-apostrophe
description: "render.py concat_segments breaks when the edit-dir path contains an apostrophe (e.g. \"couldn't\"); fixed by escaping ' as '\\'' in the concat list"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a34afa00-c6b3-47e2-baf2-bd301b7a3193
---

`helpers/render.py` `concat_segments` writes the ffmpeg concat-demuxer list as `file '<path>'`. When the path contains a literal apostrophe — which the user's English video titles routinely do (e.g. `…What else I couldn't yet do…`) — the `'` prematurely closes the quoted string and ffmpeg's concat step fails with a non-zero exit (saw 4294967294 / -2 on Windows). The per-segment extracts succeed; only the concat dies.

**Why:** concat-demuxer line format requires a literal `'` inside a single-quoted path to be written as `'\''` (close quote, escaped quote, reopen quote).

**How to apply:** fixed on 2026-06-01 by escaping in `concat_segments`: `str(p.resolve()).replace("'", "'\\''")`. Submitted as **PR #54** (branch `fix/concat-apostrophe-escaping` on the user's fork `sidorovanthon/video-use` → `browser-use/video-use`). Not merged yet — local `main` still hits the bug until it lands. If render.py concat fails on a path with an apostrophe and the PR is gone/unmerged, re-add the escaping. Pairs with [[feedback-render-fps-default]] (PR #55).

**Contribution workflow that worked (reuse it):** user's clone has `origin`=browser-use/video-use and `fork`=sidorovanthon/video-use; `gh` is authed as sidorovanthon. Branch off `main`, commit, `git push fork <branch>`, then `gh pr create --repo browser-use/video-use --base main --head sidorovanthon:<branch>`. Use `git commit -F <file>` and `gh pr ... --body-file <file>` — PowerShell here-strings mangle apostrophes in commit messages.
