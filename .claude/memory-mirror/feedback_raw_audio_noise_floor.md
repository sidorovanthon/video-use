---
name: feedback-raw-audio-noise-floor
description: No isolated.mp3 → cut raw by default (no isolation, no de-noise, no such helper exists); recalibrate every dB gate by the measured noise floor first
metadata:
  type: feedback
---

When a prep folder has **no `isolated.mp3`**, cut from the RAW source audio. This
is the default and needs no question: there is no ElevenLabs Voice Isolation step,
no ffmpeg de-noise pass, and **no isolation or de-noise helper or skill in the
video-use repo at all**. Still build `<edit>/source_clean.mp4` (source video + its
own audio, `-c copy`) so every downstream path is identical to the isolated case.

**Why:** the risk is not that raw audio sounds worse — it is that every dB gate in
the pipeline is a constant tuned on ElevenLabs-isolated audio, whose floor is near
digital silence. Raw OBS audio carries room tone, mic hiss and audible breaths and
sits roughly 10–15 dB higher. Reused unchanged, `silencedetect` misses real pauses
(the cut plan under-splits) and the Phase 6 onset gate false-fires on every join.
This is the same failure shape as [[feedback-loudnorm-shifts-silence-threshold]],
where loudnorm's +10 dB produced phantom "no silence" at real joins.

**How to apply:** `/video` Phase 1b. Measure floor **F** = 5th-percentile
`astats` RMS over `source_clean.mp4` (never `final.mp4`; astats logs at info level,
so no `-v error` — [[reference-ffmpeg-filter-loglevel]]). Shift every LEVEL gate by
`D = F − (−55)`: `silencedetect` noise −35→−35+D, "gap is still speech" −30→−30+D,
Phase 6 clean-onset ceiling −35→−35+D, clip line −25→−25+D. **Durations never
shift** (≥0.3 s split, ~0.15 s residual, 0.12–0.22 s join window). Verify the
shifted threshold fires at 2–3 pauses the Scribe word gaps independently show
before cutting — never nudge it by feel ([[feedback-silencedetect-subword-edges]]).
Expect more Phase 5 SRT-gate mismatches: raw audio degrades Scribe, that is normal,
not a re-cut signal. Contrast with [[feedback-premade-isolated-audio]].

**This user's OBS chain is gated at RECORDING, so D is 0 — do not assume +10…+15.**
Measured on edit-40 (2026-05-28 shoot): 18 % of astats frames read a literal `-inf`
and the 5th percentile sat at **−88.6 dB**, i.e. the floor is BELOW the −55 dB
isolated reference, not above it. `D = F − (−55)` comes out negative; clamp it to 0
and use the canonical gates unshifted. edit-39 (same shoot) reached the same
conclusion. Only a raw floor that is genuinely HIGHER earns a positive shift — so
always measure, but expect D = 0 on this setup and treat a large positive D as a
reason to re-check the measurement. The verification in step 3 is what settles it:
on edit-40 `-35 dB` put the first `silence_end` at 3.818 against Scribe's first
word at 3.840, which is agreement to 22 ms.

**2026-08-24 — edit-42: D can come out NEGATIVE; clamp it to 0, never shift a gate downward.** This raw OBS track ("I can't believe what just happened", no isolated.mp3) measured a 5th-percentile RMS of **−94.5 dB** with 1557 of 6740 astats frames at literal −inf — a noise gate / suppression filter was enabled in OBS, so the floor sat *below* an ElevenLabs-isolated track's, not above it. The formula gives D = −94.5 − (−55) = **−39.5 dB**; applying it would have pushed `silencedetect` to −74.5 dB and found nothing. Raw does NOT imply a raised floor — **measure first, then use `D = max(0, F − (−55))`** and run the canned −35/−30/−35/−25 gates unchanged when the floor is already at or below −55. Verified the usual way: −35 dB/0.20 fired at 43 events that matched the Scribe word gaps, and all 10 ambiguous windows probed −51…−60 dB against −20 dB speech.
