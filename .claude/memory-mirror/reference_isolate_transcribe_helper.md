---
name: reference-isolate-transcribe-helper
description: helpers/isolate_and_transcribe.py DOES NOT EXIST in the video-use repo (not in the tree, not in git history) — only the ElevenLabs cost/quota facts below survive
metadata:
  type: reference
---

**Status (verified 2026-08-17): the script is gone.** `helpers/isolate_and_transcribe.py`
is NOT in the working tree and `git log --all -- helpers/isolate_and_transcribe.py`
returns nothing — it was never committed to this fork, so it most likely died
uncommitted in [[project-data-loss-2026-07]]. Do not reference it in a plan, do not
go looking for it. There is no isolation and no de-noise tooling in the repo; a prep
folder without `isolated.mp3` is cut raw ([[feedback-raw-audio-noise-floor]]).
`helpers/transcribe.py` (single-file Scribe) and `helpers/transcribe_batch.py` do
exist and are unrelated to isolation.

The ElevenLabs facts it was written against are still true and are the reason to
keep this file:

- Voice Isolator ≈ **661 credits/min**; Scribe is ~5× cheaper, so transcribe-first
  and isolate-later is the cheaper play when budget is tight.
- API key needs **User → Read** scope for `/v1/user/subscription` to report
  workspace usage; without it only error-text credit detection works.
- The per-API-key Monthly cap is in the same Credits unit as the workspace figure
  and counts cumulative month-to-date usage on that key. An early `quota_exceeded`
  in a fresh run usually means prior month-to-date spend on the key, not this run.
  Check `/v1/user/subscription` (workspace) AND the dashboard per-key cap before a
  large batch.
- Errors that mean stop, not retry: `quota_exceeded`, HTTP 402, or "insufficient" /
  "credit" / "quota" in the message.
