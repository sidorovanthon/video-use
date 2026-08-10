---
name: feedback_scribe_product_name_mishears
description: "Scribe mangles the same three product names in every video of this channel (Claude Code or Codex, Wispr Flow, Glaido) — check them by default at the SRT gate"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0d4496d2-5130-4a78-acb8-1653830a82ef
  modified: 2026-08-10T01:33:18.616Z
---

Scribe gets the same proper nouns wrong in this user's videos, video after video,
because they are brand spellings that do not exist in its lexicon. Four consecutive
edits produced the same three mishears:

| Spoken | Scribe returned | Seen in |
|---|---|---|
| `Claude Code or Codex` | `Cloud Coder` / `Coder` / `Cloud Caller` | edit-33, edit-34, edit-36 |
| `Wispr Flow` | `Whisperflow` / `Whisper` | edit-35, edit-36 |
| `Glaido` | `Glider` | edit-35, edit-36 |

Note the token-count trap in the first row: `Claude Code or` is **three** words and
Scribe collapses it to **two**, so the fix is not a text override — you must retime
the run and insert the missing `or` token (edit-36: Claude 106.96–107.24, Code
107.25–107.50, or 107.51–107.55).

**Why:** these are the mismatches most likely to be waved through as "obviously just
the transcript being wrong about a brand" — and that instinct is right, but only for
the *spelling*. `Whisper`→`Wispr` is purely orthographic (identical phonemes, nothing
to measure). `Cloud Caller`→`Claude Code or` and `Glider`→`Glaido` are NOT: they change
the phoneme sequence, so they still need the probe that
[[feedback_word_identity_spectral_probe]] mandates — and on edit-36 both probes
confirmed the script, via a −45 dB stop closure and via F3 respectively.

**How to apply:** before the Phase 6 gate even runs, grep the transcript copy for
`Cloud`, `Coder`, `Caller`, `Whisper`, `Glider` and expect to fix each one. Treat the
pure-spelling cases as free; probe the ones that alter phonemes. Both `Wispr Flow` and
`Glaido` are dictation tools the user names together in one breath, so they almost
always appear as a pair.

Related: [[feedback_word_identity_spectral_probe]],
[[feedback_srt_full_script_reconcile]],
[[feedback_script_txt_reflects_shipped_adlib]]
