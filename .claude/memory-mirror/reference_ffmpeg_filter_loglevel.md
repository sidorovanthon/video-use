---
name: reference_ffmpeg_filter_loglevel
description: "silencedetect/astats/ebur128 print at ffmpeg INFO level — `-v error` hides all their output, looks like \"no silence found\""
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7539b9d2-0df0-4c10-b714-7ed0e5e2fe78
  modified: 2026-07-20T04:01:01.243Z
---

The `silencedetect`, `astats`/`ametadata`, and `ebur128` filters emit their
measurements (`silence_start`/`silence_end`, `RMS level dB`, integrated
loudness) on ffmpeg's **info** log stream, NOT stderr-error. Running them with
`-v error` (or `-loglevel error`) silences every measurement line — the command
returns cleanly with EMPTY output, which reads exactly like "the file has no
silence / no audio stats" and sends you debugging the wrong thing.

edit-28: probed `silencedetect` on source_clean.mp4 with `-v error` and got zero
gaps for a 2m13s monologue that obviously had pauses; wasted a couple of rounds
suspecting the isolated audio before realizing the flag ate the output.

Rule: for ANY filter whose job is to PRINT a measurement, invoke with
`-hide_banner` and NO `-v error` (default/info level), then `grep` the lines you
want. Keep `-v error` only on ffmpeg calls that ENCODE/produce a file where you
just want errors surfaced. The onset-RMS edge gate, the join-residual
silencedetect, and the loudness check all depend on this. Related:
[[reference_ffmpeg_path]], [[feedback_silencedetect_subword_edges]].
