---
name: feedback_script_txt_reflects_shipped_adlib
description: "When the only clean take of a line includes an approved ad-lib that diverges from the written script, update script.txt to the shipped wording so the SRT gate passes"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 70b1abbf-38ec-41f8-9228-d4783b44fb44
  modified: 2026-07-20T03:16:26.991Z
---

On edit-27 the sentence-4 back-half ("Not quite full-fledged yet, since we still
have the IDEF0 challenge ahead of us") had only two takes: the script-exact one
was flubbed (stutter "a- ahead us", dropped "of"), and the clean one added an
ad-lib "Okay, maybe" that is NOT in the user's written script. User chose to keep
"Okay, maybe" (clean audio, natural self-irony). Captions must match the AUDIO,
so the caption reads "Okay, maybe not quite…" — which then diffs against the
original script.txt and the mandatory gate (`diff_srt_script.py`) exits 1.

**Why:** `script.txt` is the ground truth the SRT gate diffs against; its job is
to catch Scribe mis-hearings, not to enforce the pre-recording script over an
ad-lib the user explicitly approved. Leaving script.txt stale makes the
deterministic gate red on an intended difference.

**How to apply:** when the user approves keeping spoken words that diverge from
the written script (re-recorded fixes, ad-libs), edit `script.txt` to the
SHIPPED wording BEFORE running the gate, then reconcile captions to that. The gate
should exit 0 on the delivered content. Confirm the change with the user (edit-27:
asked via the cut-plan question, then updated script.txt). Related: the outro
ad-lib "Okay, maybe" also flowed straight into the outro in one continuous take,
so it was structurally clean to keep. See [[feedback_srt_full_script_reconcile]]
and [[feedback_exposure_match_segments]].
