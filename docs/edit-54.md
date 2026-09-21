# edit-54: Claude Design — 2026-09-21

Folder: `M:/videos/OBS/prep/2026-05/2026-05-03 - Claude Design [REC 2026-06-25]/edit-54/`.

User chose **v7-lift58** after a fresh five-way comparison. Face-crop raw YAVG was 59.7–63.7 across all fifteen retained segments, with no exposure drift requiring per-segment gamma. Source was an H.264 1080×1920@60 MKV with cached Scribe `transcript.json` and no `isolated.mp3`; raw AAC audio was retained. Noise-floor calibration gave p05 = −81.75 dB, so `D = 0` and the standard audio gates remained valid.

Original 157.418 s becomes 78.249 s in fifteen segments. Removed duplicate intro wording, abandoned visual-evaluation takes, abandoned Anticode-example openings, and two incomplete logo transitions. Ordinary pauses were tightened while the complete disclaimer, CTA, and sign-off remained continuous. Final joins are 0.161–0.248 s, plus one 0.095 s detector fragment whose full RMS envelope is a clean roughly 0.14 s decay-to-splice-to-ramp shape.

Base deliverables are `final.mp4` and `final.srt` with 139 cues / 257 words. The edit-local transcript corrects `Anticod's` to `Anticode's`; the source transcript cache is unchanged. Base audio is −14.0 LUFS / −0.8 dBTP and the full file decodes cleanly.

The delivered Anticode version is `final-motion.mp4`: 78.55 s, 1080×1920, 60 fps, 4713 frames. It contains fifteen object-led scenes, Stake Out at a measured 14 LU below speech, 46 synchronized SFX from eleven asset families, the Human seal, and the full Anticodeguy CTA. HyperFrames check passes; all fourteen vector seams, 195 fullscreen coverage frames, 139 caption boxes, the full 0.5-second visual review, clean decode, and final CTA frame pass. Encoded audio is −17.5 LUFS / −2.2 dBTP. SHA256: `9842d3142b669b86983a584bc38ad8327ae7aa76f3c9040fb7ec449f23d83308`.
