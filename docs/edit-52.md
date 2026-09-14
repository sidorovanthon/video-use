# edit-52: Video disaster — 2026-09-14

Folder: `M:/videos/OBS/prep/2026-05/2026-05-01 - Video disaster [REC 2026-06-25]/edit-52/`.

User chose **v7-lift58** after a fresh five-way comparison. Face-crop raw YAVG was 54.9–61.2 across the twelve retained segments, with no exposure drift requiring per-segment gamma. Source was an H.264 1080×1920@60 MKV with cached Scribe `transcript.json` and no `isolated.mp3`; video and raw AAC audio were remuxed losslessly to `source_clean.mp4`. Noise-floor calibration gave p05 = −87.66 dB, so `D = 0` and the standard audio gates remained valid.

Original 124.017 s becomes 59.562 s in twelve segments. Removed three abandoned partial takes, the duplicated Wednesday/Thursday continuation, the inferior `what I wanted` closing wording, and the long empty-chair retake gap. Body pauses were tightened while the preferred closing sentence, human-script disclaimer, CTA, and sign-off remain continuous. The first QC pass found two long joins at 0.336 s and 0.267 s; 20 ms RMS tracks showed that the silence detector lagged the true ends of `No` and `automated`, and moving only those tails produced final join widths of 0.163–0.182 s.

Deliverables: `final.mp4` (1080×1920, 60 fps) and `final.srt` (109 cues, 195 words). Captions match every retained transcript word exactly; no independent user script was supplied. Integrated loudness is −14.09 LUFS with −0.69 dBTP. Every segment onset is at or below −66.4 dBFS on `base.mp4`; all eleven join frame pairs and beginning/middle/end frames passed with no clipped attacks or visible exposure flashes. Evidence is stored under `edit-52/verify/`.
