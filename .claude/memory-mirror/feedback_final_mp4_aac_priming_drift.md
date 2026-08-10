---
name: feedback_final_mp4_aac_priming_drift
description: "Decoding final.mp4's audio to PCM yields ~21ms MORE per segment than the container says (AAC priming per re-encoded segment accumulates); every Phase 6 probe drifts progressively unless decoded with aresample=async=1000:first_pts=0"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c56dabbe-d570-4533-9285-1f7eda33fcc5
  modified: 2026-08-10T03:11:57.280Z
---

`render.py` encodes each EDL range separately and concatenates, so **each segment
contributes ~1024 samples (~21 ms) of AAC encoder priming** that a naive decode
emits as real audio. On edit-38 (24 segments) a plain
`ffmpeg -i final.mp4 -ac 1 -ar 16000 -f s16le -` produced **100.992 s against the
container's 100.486 s — +0.506 s ≈ 24 × 1024 samples exactly**, with
`non monotonically increasing dts` warnings at the splices.

Consequence: any Phase 6 probe that decodes final.mp4 to PCM and indexes by time
drifts progressively — early joins read roughly right, late joins land inside the
neighbouring segment. On edit-38 this produced **14 false "HOT onset" flags** and,
worse, *silence floors of −10 dB* (physically impossible inside a detected
silence — that reading is the tell that the timeline, not the audio, is wrong).

`silencedetect` and `ametadata`+`asetnsamples` are **also mutually inconsistent**
on such a file: silencedetect timestamps come from (duplicated) container pts,
while `asetnsamples` renumbers frames sequentially. Neither matches a plain PCM
decode. Cross-checking two of them proves nothing.

**How to apply:** put `aresample=async=1000:first_pts=0` FIRST in every filter
chain that measures `final.mp4`, and use it for the PCM decode too — it restored
edit-38's decode to 100.487 s vs the container's 100.486 s, after which all 23
floors read a plausible −42…−50 dB. Validate the fix before trusting any probe:
decoded length must equal the container duration. `source_clean.mp4` (single
`-c copy` mux) decodes with **zero** drift, so Phase 3 cut-edge analysis needs no
such correction — only post-render measurement does.

This is NOT an A/V defect: video 100.450 s vs audio 100.486 s is one frame apart,
the container pts are correct and the file plays fine. Do not "fix" the render.

Extends [[feedback_join_offsets_from_silencedetect]] — locating joins from
silencedetect is necessary but not sufficient; the probe's own timeline must be
corrected too. See also [[feedback_onset_probe_anchor_artifact]] and
[[feedback_loudnorm_shifts_silence_threshold]].
