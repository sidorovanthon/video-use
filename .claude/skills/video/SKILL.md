---
name: video
description: Start processing a new OBS talking-head video — /video <path to prep folder or mp4>. Runs the mechanical freshness/environment gate, then drives the full standard pipeline (mux clean audio, cuts, grade gate, render, SRT) per the canonical recipe. Project-local; this repo only.
---

# video — one path in, finished video out

Replaces the hand-typed opener prompt. Input: one argument — the monthly prep
folder (`M:/videos/OBS/prep/YYYY-MM/<dated stem>/`) or a source video inside it.

Canon: `docs/settings_reference.md` (this repo) — read it before cutting.
Project memory (auto-loaded) holds the correction history; obey `feedback_*` rules.

## Phase 0 — freshness & environment gate (mechanical, BEFORE any work)

Run all checks; do not start editing on a stale/dirty/broken setup:

1. **Repo freshness:** `git fetch origin && git status -sb`. If behind
   `origin/main` → `git pull --ff-only` (if it can't fast-forward, STOP and
   show the divergence). If the working tree is dirty → show the diff and
   resolve (commit or stash) before proceeding — uncommitted pipeline fixes
   died in the 2026-07 data loss.
2. **Deps:** if the pull changed `pyproject.toml` → `uv sync`.
3. **Tools:** `ffmpeg -version` and `ffprobe -version` must work. If they report
   "command not found" they are almost certainly **installed but not on this
   shell's PATH** (winget put them in User PATH, but the tool shell's parent
   predates that entry — `setx`/registry edits do NOT fix the live session).
   Do NOT reinstall: prepend the winget bin to `PATH` in every ffmpeg-using
   command (and helpers that shell out — render.py, grade_sheet.py — inherit the
   shell PATH). **Resolve the bin dir version-agnostically — the `ffmpeg-<ver>-full_build`
   folder name bumps on every winget update (was 8.0, silently became 8.1.2 → "not
   found" on the first try this session); NEVER hardcode the version from memory:**
   ```bash
   export PATH="$(ls -d /c/Users/sidor/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin | tail -1):$PATH"
   ```
   Details: memory `reference_ffmpeg_path`. Only if the
   binary genuinely isn't installed: `winget install --id Gyan.FFmpeg -e`.
   `ELEVENLABS_API_KEY` in `.env` is only needed if transcription will run.
4. **Memory mirror (durability):** copy
   `~/.claude/projects/C--Users-sidor-repos-video-use/memory/*.md` →
   `.claude/memory-mirror/`; if changed, commit.
5. **Off-disk backup:** if `main` is ahead of `fork/main` → `git push fork main`.

## Phase 1 — resolve inputs

- Arg is the prep folder (an mp4 arg → use its parent folder).
- Inventory the folder: source `<stem>.mp4` (OBS often writes `.mkv` instead —
  same h264 1080×1920@60 stream, muxes with `-c copy`, no re-encode); pre-made
  `isolated.mp3` + `transcript.json`; the user's script text (for SRT
  cross-check) if present.
- **Save the supplied script verbatim to `<edit>/script.txt`** (words only —
  strip any `Скрипт для сверки:` prefix and the folder path; keep the spoken
  title line). Phase 5/6's SRT gate diffs against this file, so it is not
  optional when the user pastes a script (memory: feedback-srt-full-script-reconcile).
- **Pre-made isolated audio present → do NOT re-run ElevenLabs** — mux clean
  audio over video (`-c copy`) and cut from that (memory:
  feedback-premade-isolated-audio). The mux target is **`<edit>/source_clean.mp4`
  inside the Phase 2 edit dir**, so create that dir FIRST (do Phase 2 before the
  mux) — writing it to the prep-folder root leaves it in the wrong place and it
  must be moved (per the edit-dir convention, everything lives inside `edit-NN/`).
- **No `isolated.mp3` → cut from the RAW source audio.** This is the default,
  not a question to ask: no ElevenLabs Voice Isolation, no ffmpeg de-noise pass.
  There is no isolation or de-noise helper in this repo — the
  `helpers/isolate_and_transcribe.py` named in older memory is NOT here and never
  appears in git history; do not go looking for it and do not build one. Still
  produce `<edit>/source_clean.mp4` (mux source video + its own audio, `-c copy`)
  so every downstream path is byte-identical to the isolated case, then run
  **Phase 1b** — the dB thresholds must be recalibrated before any cutting.
- Missing transcript → `helpers/transcribe.py` (Scribe; costs money — say so).

## Phase 1b — noise-floor calibration (ONLY when cutting raw audio)

Every dB threshold in Phases 3 and 6 was tuned on ElevenLabs-isolated audio,
whose floor is near-digital silence. Raw OBS audio carries room tone, mic hiss
and audible breaths: reusing the canned numbers makes `silencedetect` miss real
pauses and makes the Phase 6 onset gate false-fire on every join. Measure the
floor, then shift the thresholds by the measured delta — the same mechanism the
loudnorm shift already uses (memory
`feedback_loudnorm_shifts_silence_threshold`).

1. **Measure the floor** on `source_clean.mp4` (never on `final.mp4` — loudnorm
   has already moved it):
   ```bash
   ffmpeg -hide_banner -i "<edit>/source_clean.mp4" \
     -af "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level" \
     -f null - 2>&1 | grep RMS_level
   ```
   No `-v error` — astats logs at info level and `-v error` hides all of it
   (memory `reference_ffmpeg_filter_loglevel`). Floor **F** = the 5th-percentile
   RMS across the file (NOT the mean — speech dominates the mean); cross-check it
   against 2–3 pauses you can point at in the Scribe word gaps.
2. **Shift by `D = F − (−55)`** — how much louder this floor sits than an
   isolated track. `D ≈ 0` on isolated audio, typically `D ≈ +10…+15 dB` on raw
   OBS. Apply D to every level gate and record the shifted numbers in the edit
   notes:

   | Gate | Isolated | Raw |
   |---|---|---|
   | Phase 3 `silencedetect` noise | −35 dB | −35 + D |
   | Phase 3 "RMS in the gap = still speech" | ≳ −30 dB | −30 + D |
   | Phase 6 clean-onset ceiling | ≤ −35 dB | −35 + D |
   | Phase 6 clipped-onset line | > −25 dB | −25 + D |

   **Durations do NOT shift** — the ≥0.3 s split rule, the ~0.15 s residual and
   the 0.12–0.22 s join window are time, not level.
3. **Verify the shifted threshold before building the cut plan:** it must fire at
   2–3 pauses that the Scribe word gaps in `takes_packed.md` independently show.
   If it fires at none, the floor measurement is wrong — re-measure. Never nudge
   the threshold by feel until events appear.
4. Expect a noisier transcript: raw audio degrades Scribe, so more Phase 5 SRT
   mismatches than usual is normal and is not a reason to re-cut.

## Phase 2 — working dir

Global numbering: find max `edit-*` N recursively across
`M:/videos/OBS/prep/*/*/edit-*` (and any legacy `M:/videos/OBS/edit-*` left
during migration); create `<prep>/edit-(N+1)/` with
`transcripts/ clips_graded/ verify/`. Stage the transcript as
`transcripts/S0.json` so the EDL key `S0` matches. Everything, including
`final.mp4` + `final.srt`, stays inside this folder.

## Phase 3 — cut plan

**Levels below (`-35dB`, `−30 dB`) assume ISOLATED audio. On raw audio use the
Phase 1b shifted values everywhere a dB number appears.**

`helpers/pack_transcripts.py --edit-dir <edit>` → read `takes_packed.md`.
Drop entirely: false starts / retakes (keep the clean retake) and any big
dead-air gap. Then **split at EVERY gap ≥ ~0.3 s and trim it to ~0.15 s
residual** — pad ~0.075 s into the silence on each side (never clips speech).
Enumerate those gaps from the **UNION of `silencedetect` gaps AND Scribe
word-to-word gaps**, then RMS-probe every candidate: neither source lists them
all. silencedetect invents gaps inside quiet word tails (edit-26) *and misses
real ones* — on edit-34 a genuine 0.41 s pause (RMS −36…−61 dB throughout)
produced **no silencedetect event at all** at `-35dB/0.20`, and only the Scribe
word gap flagged it (memory: feedback-silencedetect-subword-edges). A single visually continuous take is **NOT** an exception: its
inter-phrase / inter-sentence pauses (0.4–1.1 s) are joins to trim too, not
"breaths to keep" — preserving them gets flagged as a defect (memory:
feedback-trim-pauses-tight; edit-24 was recut for exactly this). There is no
"only pauses ≥ 1.5 s" threshold — that reading caused the edit-24 miss.
**Derive BOTH edges of every segment mechanically from `silencedetect` on
`source_clean.mp4`, NEVER from Scribe `word.start`/`word.end` ± a pad.** Scribe
timings choose *which words* to keep; they do NOT place the cut. They drift in
BOTH directions at edges and both bit edit-25: `word.end` overshot the acoustic
end → a 0.47 s pause at a join; `word.start` landed LATE → the "For"/"Okay"
onsets got clipped. Rule:
- **segment END** = the `silence_start` of the gap *after* the last kept word,
  `+ ~0.10 s`.
- **segment START** = the `silence_end` of the gap *before* the first kept word,
  `− ~0.06 s`.
Build `edl.json` (absolute source paths). Cross-check kept text against the
user's script. (Sign-off/outro exception: if the user is fine with the closing
pauses, the standard outro block — human-script disclaimer + subscribe CTA +
"Okay, bye" — reads better kept whole as one un-cut range; memory
`feedback_trim_pauses_tight`.)

## Phase 4 — GRADE GATE (mandatory, mechanical — never inherit a grade)

```bash
python helpers/grade_sheet.py scan <edit>/edl.json          # per-segment face luma
python helpers/grade_sheet.py sheet <edit>/edl.json --time <brightest talking frame>
```

- Segments differ materially → per-range `"grade"` with `eq=gamma=G`
  pre-normalization before the grade chain (target one band, ~85–93).
- **SHOW the sheet and wait for an explicit grade choice before rendering.**
  Series defaults ("Losing Context" → v7-lift, "Migrating" → v7-contrast) are
  expectations, not decisions.

## Phase 5 — render & subtitles

```bash
uv run helpers/render.py <edit>/edl.json -o <edit>/final.mp4 --no-subtitles --fps 60
```

`build_master_srt` → `master.srt`. **Reconcile every caption against the script
word-by-word — NOT just proper nouns.** Scribe drops plural `-s`, contractions
(`I've`→`I`), and unstressed articles (`a`), and swaps function words
(`in`↔`and`, `the`↔`a`); a term-only pass (`CLOUD`→`CLAUDE`, `notation`→
`notations`, `Domain Specific`→`domain-specific`) misses all of these and shipped
wrong on edit-26. Fix in a filtered transcript COPY, never the cache (override the
word `text`; merge two tokens for a hyphenated compound; insert a short token for a
missing article), then rebuild. **Arbitrate each mismatch acoustically with
`helpers/word_probe.py` (`formant` / `sib` / `rms`) against a control from the same
file in the same phonetic environment** — the fix direction is not fixed, edit-34
split 3 transcript-side / 2 script-side (memory:
feedback-word-identity-spectral-probe). `cp master.srt final.srt`. The Phase 6 gate is the
mechanical backstop — run it (memory: feedback-srt-full-script-reconcile).

## Phase 6 — verify before declaring done

**Same rule as Phase 3: the `−35`/`−25` onset lines below are isolated-audio
numbers — on raw audio compare against the Phase 1b shifted values.**

Frames at every join (no visible grade/exposure step), `silencedetect` on
joins (~0.15 s), `r_frame_rate` = 60/1, loudness ≈ −14 LUFS. Show the user 2–3
verification frames.

**MANDATORY SRT gate (deterministic — not a "spot-check"):**
```bash
uv run helpers/diff_srt_script.py <edit>/final.srt <edit>/script.txt
```
Exit 0 = captions match the script word-for-word (modulo intended cuts, which it
lists for eyeball confirmation). Exit 1 = caption drift (dropped plural/article,
swapped function word, un-hyphenated compound) → fix in a transcript COPY and
rebuild until it passes. Do NOT ship on a non-zero exit. If no `script.txt` exists
(user gave no script), fall back to reading the captions against the transcript.

**MANDATORY edge gate before shipping — probe every segment's cut edges in the
rendered `final.mp4` (this is the check that would have caught the "For" clip
before the user did; run it, do not ship on faith):**
- **Onset (clip) check:** at each segment's output-start time, read the first
  ~40 ms RMS (`astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level`).
  A clean onset starts in silence and ramps up → first frame **≤ ~−35 dB**. A
  first frame **hotter than ~−25 dB = the segment begins mid-word (clipped)** →
  move that start earlier to `silence_end − 0.06` and re-render.
- **Tail (overshoot) check:** `silencedetect` residual at each join should be
  ~0.12–0.22 s. **> ~0.25 s = a Scribe `word.end` overshoot left a pause** → pull
  that end back to the acoustic `silence_start + 0.10` and re-render.

Only declare done once every segment passes both.

## Phase 7 — wrap-up

New lesson learned → memory file + `MEMORY.md` line + refresh
`.claude/memory-mirror/`; grade outcome → append to the history table in
`docs/settings_reference.md`; commit; suggest `/wrap` at session end.
