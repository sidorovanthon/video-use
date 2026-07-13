#!/usr/bin/env python3
"""Deterministic word-by-word diff of a rendered SRT against the user's script.

Why this exists: the master SRT is built from the Scribe transcript, so it
reflects what was *heard*, not the user's written script. Scribe reliably drops
trailing plural -s, contractions ('ve/'ll), unstressed articles ("a"), and swaps
short function words (in/and, the/a). A proper-noun/term spot-check misses all of
these — edit-26 shipped "notation" (want "notations"), "Domain Specific" (want
"domain-specific"), "I already" (want "I've already"), etc., and the user caught
it. This turns the Phase 5/6 "cross-check against the script" step from prose into
a gate that exits non-zero on real drift.

Handles intentional cuts: the script contains false starts / retakes that were
deliberately dropped, so a naive full-script vs SRT diff is all noise. We align
with difflib and classify:

  * MISMATCH  — a substitution, or a short (< CUT_MIN token) insert/delete. This is
                transcription drift you must fix in the caption text. → exit 1.
  * CUT       — a long (>= CUT_MIN token) contiguous run present in the script but
                not the SRT. Almost always an intended cut (dropped false start /
                trimmed tail). Printed for eyeball confirmation; does NOT fail.

Usage:
    python helpers/diff_srt_script.py <edit>/final.srt <edit>/script.txt
    python helpers/diff_srt_script.py <edit>/final.srt -   # read script from stdin

Save the spoken script (the words only — strip any "Скрипт для сверки:" prefix and
folder path) to <edit>/script.txt in Phase 1 so this can run in Phase 5/6.
"""
from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# A script-only run of at least this many consecutive tokens reads as an
# intentional cut (false start / trimmed tail), not word drift.
CUT_MIN = 3


def normalize(tok: str) -> str:
    """Lowercase; strip surrounding sentence punctuation; keep internal
    apostrophes and hyphens so "domain-specific" and "I've" are single tokens
    that compare equal regardless of case."""
    tok = tok.lower().strip()
    # drop everything except letters, digits, internal ' and -
    tok = re.sub(r"^[^0-9a-z]+", "", tok)
    tok = re.sub(r"[^0-9a-z]+$", "", tok)
    return tok


def tokenize(text: str) -> list[str]:
    return [n for n in (normalize(t) for t in text.split()) if n]


def srt_caption_text(srt: str) -> str:
    """Strip SRT index lines and timestamp lines, keep caption text."""
    out: list[str] = []
    for line in srt.splitlines():
        s = line.strip()
        if not s or s.isdigit() or "-->" in s:
            continue
        out.append(s)
    return " ".join(out)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    srt_path = Path(sys.argv[1])
    srt_text = srt_caption_text(srt_path.read_text(encoding="utf-8"))
    if sys.argv[2] == "-":
        script_text = sys.stdin.read()
    else:
        script_text = Path(sys.argv[2]).read_text(encoding="utf-8")

    a = tokenize(script_text)  # script = reference
    b = tokenize(srt_text)     # srt    = what we shipped
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)

    mismatches: list[str] = []
    cuts: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        script_run = " ".join(a[i1:i2])
        srt_run = " ".join(b[j1:j2])
        if tag == "delete" and (i2 - i1) >= CUT_MIN:
            cuts.append(f"  CUT  script-only ({i2 - i1} words): …{script_run}…")
        elif tag == "replace":
            mismatches.append(f"  MISMATCH  script:{script_run!r}  →  srt:{srt_run!r}")
        elif tag == "delete":
            mismatches.append(f"  MISMATCH  dropped from srt: {script_run!r}")
        elif tag == "insert":
            mismatches.append(f"  MISMATCH  extra in srt (not in script): {srt_run!r}")

    if cuts:
        print(f"intended cuts (verify these were deliberate) — {len(cuts)}:")
        print("\n".join(cuts))
        print()
    if mismatches:
        print(f"CAPTION DRIFT vs script — {len(mismatches)} (FIX in a transcript copy, rebuild):")
        print("\n".join(mismatches))
        print(f"\nFAIL: {len(mismatches)} caption mismatch(es). Reconcile before shipping.")
        return 1
    print(f"OK: captions match the script word-for-word (modulo {len(cuts)} intended cut(s)). "
          f"{len(b)} srt / {len(a)} script tokens.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
