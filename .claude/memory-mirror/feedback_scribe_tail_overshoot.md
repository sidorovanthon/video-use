---
name: feedback-scribe-tail-overshoot
description: "Scribe end timestamps on closing words (e.g. \"bye.\", \"thanks.\") can overshoot the audible end by 1+ seconds into trailing room tone — never trust word.end for final-segment tail trims without verifying the source waveform."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cc67f6ec-4586-4918-9096-685c58528690
---

When trimming the **closing word** of a video, don't trust the Scribe `word.end` timestamp for that word — it drifts in **either direction**, so always read the actual waveform. Overshoot bundles the vowel decay + room tone into the word (leaves dead air); undershoot cuts the closing word's tail off.

**Why:** Observed 2026-05-26 in edit-08 (OBS talking-head): `bye.` timestamped 108.96–110.52 s, actual audible end ~109.30 s — Scribe **overshot** by ~1.2 s → naive `end+80ms` left dead room tone. Then 2026-06-09 in edit-10 (same subject): `bye.` timestamped 271.42–**271.62**, but the waveform decay ran to ~**271.90** — Scribe **undershot**, so trusting `word.end` would have clipped the "-ye". Used 271.92 as the segment end. Same quirk, opposite sign.

**How to apply:**
- For interior cut edges, Scribe word boundaries + the standard 50/80 ms or 100/200 ms pads are still fine.
- For the **final segment's tail edge only**, do an extra check: `timeline_view <source> <last_word.start-0.5> <last_word.end+0.2>` and read the actual end of the waveform energy. Use that + 30–80 ms as the segment end, not `word.end`.
- **Generalizes beyond the closing word (edit-12, 2026-06-15):** this speaker draws out ANY emphatic/closing word mid-take ("work.", "enough.") and Scribe overshoots its `word.end` into the decay. In edit-12 the user flagged a "pause after 'that forces you to work'": Scribe `work.` end was 90.659 but RMS showed energy ending ~90.0 with a 0.63 s decay/silence tail before the next word. Fix = split there and trim. When the user reports a "pause" mid-sentence, RMS-check the preceding drawn-out word's real end (astats RMS envelope at 0.04–0.05 s reset), don't trust the Scribe gap.

**2026-07-13 — edit-25: generalize to EVERY segment END in a tight-trim edit, not just the closing word.** I built all 13 segment ends as `Scribe word.end + 0.075`. On verify, the "human being." → "For more AI tips" join measured **0.47 s** residual (target ~0.15) because Scribe's `being.` end 91.60 overshot the acoustic speech end by ~0.38 s — source `silencedetect` showed silence starting at **91.22**. Several other ends overshot 0.1–0.2 s the same way (joins landed 0.19–0.29 instead of 0.15). Fix that fixed ALL of them at once: **derive every segment END from the source `silencedetect` `silence_start` that follows the segment's last audible word, + ~0.10 s pad — never from Scribe `word.end`.** After re-deriving, all joins fell to 0.12–0.22 s. (Segment STARTS from `word.start − 0.075` were fine here — onset tokens weren't degenerate since all gaps were <1.5 s; the drift problem is specifically on END edges.) So the mechanical Phase-3 rule is: ends from `silence_start`, starts from `word.start` (with the onset-degeneracy check), and the closing-word waveform check from above still applies to the very last tail.

Related: [[reference-video-use-settings]] (the OBS recipe — `settings_reference.md` cuts section talks about head/tail pad but doesn't yet flag this Scribe quirk). [[feedback-trim-pauses-tight]] (the 0.47 s join is exactly the preserved-pause failure that gets flagged).
