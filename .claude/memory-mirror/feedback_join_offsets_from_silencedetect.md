---
name: feedback-join-offsets-from-silencedetect
description: "Phase 6 onset checks must locate joins via silencedetect on final.mp4, never by summing EDL segment durations — re-encode rounding drifts the output timeline and fakes \"hot onset\" failures"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 627a5318-3ffb-4218-a43f-81f3ac4d973e
  modified: 2026-08-10T02:30:27.904Z
---

The Phase 6 onset (clip) check probes the first ~40 ms of each segment in the
rendered `final.mp4`. Computing that probe position by **summing EDL segment
durations is wrong** — each segment is re-encoded to a whole number of frames at
60 fps and AAC adds frame padding, so the output timeline drifts from the
arithmetic. On edit-37 the drift reached **~0.13 s** by mid-file.

The failure is silent and misleading: the probe lands in the *previous* segment's
still-decaying speech tail instead of the new segment's silent lead-in, and reads
hot. Two of edit-37's 21 joins falsely reported −19.4 dB and −24.1 dB "clipped /
warn" onsets. Both were clean — a fine RMS track showed the correct shape every
time: **decay → −100 dB digital-silence splice marker → ramp up**.

**Why:** the check exists to catch segments that begin mid-word ([[feedback_scribe_onset_token]]);
a false positive here costs a pointless re-render, and worse, teaches you to
distrust a gate that is actually working.

**How to apply:** get join positions from `silencedetect` on `final.mp4` (with the
loudnorm-shifted threshold — [[feedback_loudnorm_shifts_silence_threshold]]) and
probe relative to the reported `silence_end`, or find the exact splice by scanning
for the −100 dB digital-silence frame. If a join does read hot, re-probe it with a
0.2 s lead-in RMS track before concluding anything: a real clipped onset starts hot
with no preceding decay, a false one sits on the tail of the previous segment.
Related: [[feedback_silencedetect_subword_edges]].
