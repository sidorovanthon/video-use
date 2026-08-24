---
name: feedback_word_identity_spectral_probe
description: "Scribe WORD-IDENTITY disputes (agent/engine, ran/run, a/the) are settled by band-energy probes against in-file control words, not by guessing from context"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ba2b871a-2172-4df5-bcee-bd222cfe622f
  modified: 2026-08-10T01:33:00.341Z
---

The RMS probe settles *silence vs speech*. A second class of SRT-gate mismatch is
*which word was said* — Scribe returns a real, confidently-voiced token that is
simply the wrong word. Three mechanical discriminators, all used on edit-33:

- **Word-final nasal (agent vs engine).** `engine` ends /n/, `agent` ends an
  unreleased /t/. Slice the last 60 ms and read LF (<500 Hz) + F2: a nasal coda
  keeps voiced murmur (control "any" /n/: broadband −23.6, LF −34.9), while
  edit-33's disputed tail read −52…−55 dB in *every* band = no murmur → `agent`.
- **Vowel frontness (ran vs run).** Compare the F2hi(1.5–2.4k) − F2lo(0.8–1.4k)
  ratio against control words from the SAME file: /æ/ "that" −3.47, /ʌ/ "some"
  −3.76, "just" −4.05, target −2.81 → fronter than all → `ran`. Pre-nasal /æ/
  raises, which widens the gap in your favour.
- **Degenerate article token (a vs the).** Scribe emits ~0.010 s tokens for
  unstressed articles. Real `the` in the same file runs 0.10–0.12 s; the
  confirmed `a` of "as a folder" is also 0.010 s → a 0.010 s "the" is `a`.
  (Same shape as the edit-29 0.01 s "to"→"the" fix.)

**edit-34 — crude band ratios FAIL on reduced function words; use LPC formants +
a MATCHED-ENVIRONMENT control.** The `in` vs `on` dispute ("so you don't get lost
?? them") defeated two rounds of the band-ratio method above: both candidates were
fully reduced and nasalized, energy sat mostly below 300 Hz, and the 300-700 /
700-1100 / 1500-2700 ratios of the disputed token landed *between* the control sets
with no separation. What actually resolved it:

- **LPC formant tracking** (order 12 @ 10 kHz, pre-emphasis 0.97) instead of band
  ratios — now `helpers/word_probe.py formant`. Read F1 for vowel height and F2 for
  frontness frame by frame, so you can see the nucleus rather than average over the
  neighbouring consonants.
- **A control in the same phonetic environment.** Generic "on"/"in" controls were
  useless: the ones available sat before "your" (/j/ drags F2 up) and carried more
  stress. The decisive control was `what's IN them` — sibilant + unstressed vowel +
  "them", identical to the disputed `lost ?? them`. There the matched control's F2
  is **≈1360 Hz** while both takes of the disputed token read **≈1170-1200 Hz** =
  a backer vowel → `on`. Scribe had it right in two independent takes.
- **Sibilant DURATION, not presence, for /s/-final candidates.** `develop the/this
  structure`: measure the frication run before "structure" and compare with the same
  word elsewhere. Control `file structure` = 0.225 s of /s/; the disputed = 0.145 s
  — *shorter*, so there is no extra /s/ from "this" → `the`. A presence test says
  nothing here because "structure" supplies its own /s/ either way.

**edit-35 — SYLLABLE COUNTING on a plain RMS track beats any spectral test when the
candidates differ by a whole syllable.** `capabilities` vs Scribe's `abilities`
(5 syllables vs 4) needs no formants at all: run `word_probe.py rms` over the token
and read the envelope. Syllabic nuclei show as peaks, stop closures as sharp dips,
and a VOICELESS stop drops much deeper than a voiced one. edit-35's token had **five
peaks** (13.83 / 13.93 / 14.06 / 14.14 / 14.33) split by two deep dips at −40.7 dB
(13.88) and −40.3 dB (14.21) — exactly the /p/ of ca-PA and the /t/ of li-TIES.
`abilities` would give four peaks and a *voiced* /b/ closure, which does not fall to
−40 dB. Duration alone was useless here (0.64 s fits both at plausible rates); the
peak count and the closure depth decided it. Same track also settled `doesn't` vs
`does not` in one read: one stressed peak at −17.0 dB followed by a reduced bump
11 dB down = contraction, whereas "not" would carry a second peak of comparable
level.

Also settled that session without a probe, on structure rather than acoustics:
Scribe merged `Code or`→`Coder` and split `there's`→`there is`. For the merge, the
disputed second syllable measured F2 1209-1355 against the speaker's confirmed "or"
in the same collocation at 1118-1394 = the same token. For the split, "there ?? a"
spanned **0.270 s** vs 0.300/0.330 s for two known `there's a` controls — an extra
syllable cannot be *shorter*, so it is the contraction.

**edit-36 — for a MIS-HEARD MULTI-WORD RUN, probe manner of articulation, not vowel
identity.** Scribe returned `Cloud Caller Codex` where the script had `Claude Code or
Codex` — three tokens against four, so no token-to-token formant comparison even lines
up. Two structural reads settled it off one full-resolution `formant` pass (which also
prints RMS):

- **A stop closure proves a word/syllable boundary a continuant cannot.** `Caller`
  requires a lateral /l/ between its two syllables; `Code or` requires the /d/ stop of
  "Code". At 107.45–107.50 the track falls to **−45.1 dB for 50 ms** — a near-silent
  closure. A lateral is a *continuant*: it never drops that far. That single dip
  eliminates "Caller" without touching the vowels.
- **Monophthong vs diphthong on F1/F2 trajectory.** `Claude` /ɔ/ holds F1 ≈ 505–568,
  F2 ≈ 770–1030; `Cloud` /aʊ/ would open to F1 ≈ 700+ and glide F2 steadily *down*.
  Observed F1 never exceeded 568 and F2 went down-then-up → monophthong → `Claude`.

Same session, a second independent route to `engine`→`agent` (edit-33 used the
word-final nasal-murmur test): read **F2 in the frame immediately before the /dʒ/
affricate**, which the `sib` track locates exactly. `agent` /eɪdʒ/ puts the /eɪ/
offglide there (in-file control "agent": F2 1849); `engine` /ɛndʒ/ puts a nasal /n/
there (control "end": nasal F2 1332–1434). Disputed read 1834–1850 → `agent`. Locating
the affricate with `sib` first is what makes this cheap — it removes the guesswork
about where Scribe's token boundary actually sits.

Also that session: `Glaido` vs Scribe's `Glider` is a **rhoticity** question, so read
**F3**, not F1/F2 — the disputed final syllable held F3 2367–2432 against an /ər/
control ("folders") at 1658–1839 and an /oʊ/ control ("go") at 2223–2429 → non-rhotic.
And `preliminarily`→`preliminary` needed only durations: the token Scribe spelled with
the extra syllable ran **0.60 s** while the *same speaker's* "preliminary" in the
discarded retake of the same sentence ran 0.69 s — an added syllable cannot make the
word 13 % shorter.

**Direction of the fix is not fixed.** edit-34's five mismatches split 3 transcript-side
(Scribe wrong: Coder, there is, the→a) and 2 script-side (Scribe right: in→on,
this→the); edit-35's eight split the other way — 3 transcript-side (capabilities,
Wispr Flow, Glaido) and **5 script-side**, with Scribe right on doesn't, use, the
extra "the", patterns and something. edit-36 then went **7/0 transcript-side** — a
clean sweep happens, so a run of same-direction fixes is not itself evidence you are
rubber-stamping the script; each one there carried its own measurement. Decide each on
its own; see [[feedback_script_txt_reflects_shipped_adlib]].

**Why:** deciding these from context alone ("nobody says coding engine") is the
guess the pipeline is supposed to eliminate — and the opposite mistake, assuming
the script is truth, shipped wrong on edit-32 where Scribe was right every time.
A control word from the same recording removes mic/room/voice as variables.

**How to apply:** at the Phase 5/6 SRT gate, for every mismatch that is a real
voiced token (not a missing article, not a spelling difference), pick a control
word of each candidate phoneme class from the same file — matching the phonetic
ENVIRONMENT, not merely the word — and run `helpers/word_probe.py` (modes
`formant` / `sib` / `rms`; `batch probes.json` prints a disputed token and all its
controls in one pass). Let the measurement choose. Only orthography
(`code base`→`codebase`) and product names (`Cloud Coder`→`Claude Code or`) may be
fixed without a probe. If two rounds still overlap, say the probe was inconclusive
and name the weaker evidence you fell back on — don't dress a guess up as a
measurement.

Related: [[feedback_silencedetect_subword_edges]],
[[feedback_srt_full_script_reconcile]],
[[feedback_script_txt_reflects_shipped_adlib]]

**2026-08-24 — edit-43: the a/the dispute is settled by a CONSTRICTION DIP, not by formants.** A fully reduced `a` (/ə/) and `the` (/ðə/) share the same schwa, so F1/F2 overlap completely and the LPC track is inconclusive — on the disputed 40 ms token in "not sitting on ? surface" it read F1 511→393 / F2 1379→1442, sitting squarely between the `a` controls (F2 1167–1547) and the `the` controls (F2 1338–1634). What separates them is the **/ð/ itself**: a voiced dental fricative is a constriction, so it prints a local **RMS dip** between the preceding sound and the schwa, while a bare `a` does not. Read a 10 ms-resolution `rms` track across the boundary against a control in the SAME environment — here `down|the` at 51.38–51.52 dips to **−33.7 dB** before rising to −27.0, whereas the disputed `on|?` holds a flat **−29 dB plateau** from 43.84 to 43.90 and then rises smoothly into "surface". No dip = no /ð/ = `a`. Pick the control by the preceding segment (a nasal before a nasal, a vowel before a vowel), because the dip depth is relative to what precedes it.

Same session, two cheaper reads worth reusing: **on vs of** is a sustained low-F1 nasal murmur (F1 held at 271–283 with F2 ≈ 1000 and RMS flat at −30 dB for 60 ms) versus an immediate erratic decay for /v/ (F1 jumping 523→352→757→1074 as RMS falls −30→−41); and **this vs these** is settled by matching the whole disputed track to a control of the same word in the identical environment — `this out` at 191.12 matched `this out` at 194.00 frame-for-frame (F1 375/391, F2 1565/1586, same three-frame decay, ~0.15 s) while the real `these things` control at 133.54 ran 0.24 s with sustained voicing and a RISING F2. A same-word, same-neighbour control beats any threshold.
