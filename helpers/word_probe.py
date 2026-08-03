#!/usr/bin/env python
"""Acoustic arbitration for SRT-gate word-identity disputes.

The Phase 6 SRT gate reports mismatches between the captions (what Scribe heard)
and `script.txt` (what was written). Memory `feedback_word_identity_spectral_probe`
binds us to settle each one by MEASUREMENT against control words from the SAME
recording — never by context or by assuming the script is truth.

Three modes, matching the three kinds of dispute:

  formant  LPC formant track (F1/F2/F3). The general vowel-identity tool.
           Use for vowel-quality pairs: in/on, ran/run, a/the, the/this.
           Read F1 (height: low vowel = high F1) and F2 (frontness).
  sib      Sibilant-fraction (4-8 kHz) track. Use when a candidate adds or
           removes an /s/ — "this structure" vs "the structure" differ only in
           whether the frication before "structure" is one /s/ or two.
  rms      Plain RMS track. Silence-vs-speech, gap probing, plosive-blip levels
           (see `feedback_silencedetect_subword_edges`).

CRITICAL — crude band-energy ratios are NOT enough for reduced function words.
On edit-34 the in/on dispute was fully reduced and nasalized in BOTH candidates;
the 300-700/700-1100/1500-2700 band ratios overlapped completely and the first
two probe rounds were inconclusive. What resolved it was (a) LPC formants and
(b) a control in the MATCHED phonetic environment (same neighbouring sounds,
same stress). Pick controls by environment, not just by word.

Usage:
  uv run helpers/word_probe.py <media> formant 67.02 67.14 --label "disputed"
  uv run helpers/word_probe.py <media> sib     110.00 110.40
  uv run helpers/word_probe.py <media> rms     140.30 141.10
  uv run helpers/word_probe.py <media> batch   probes.json

`probes.json` is a list of ["mode", "label", start, end] entries so a disputed
token and all its controls print in one pass (the way you actually want to read
them).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LPC_SR = 10000     # 10 kHz -> order 12 resolves F1..F4 for a male voice
LPC_ORDER = 12
WIDE_SR = 16000    # sibilant work needs the full 4-8 kHz band


def _ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    # winget layout; the version folder bumps on every update, so glob it
    root = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    hits = sorted(root.glob("Gyan.FFmpeg_*/ffmpeg-*-full_build/bin/ffmpeg.exe"))
    if hits:
        return str(hits[-1])
    sys.exit("ffmpeg not found (see memory reference_ffmpeg_path)")


def grab(media: str, t0: float, t1: float, sr: int) -> np.ndarray:
    p = subprocess.run(
        [_ffmpeg(), "-v", "error", "-ss", f"{t0:.4f}", "-t", f"{max(t1 - t0, 0.001):.4f}",
         "-i", media, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
        capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float64) / 32768.0


def _lpc(x: np.ndarray, order: int):
    x = x * np.hamming(len(x))
    r = np.correlate(x, x, "full")[len(x) - 1:][:order + 1]
    if len(r) <= order or r[0] <= 0:
        return None
    a = np.zeros(order + 1)
    a[0], err = 1.0, r[0]
    for i in range(1, order + 1):
        acc = r[i] + sum(a[j] * r[i - j] for j in range(1, i))
        k = -acc / err
        prev = a[1:i].copy()
        for j in range(1, i):
            a[j] = prev[j - 1] + k * prev[i - j - 1]
        a[i] = k
        err *= (1 - k * k)
        if err <= 0:
            return None
    return a


def formants(seg: np.ndarray) -> list[float]:
    seg = np.append(seg[0], seg[1:] - 0.97 * seg[:-1])       # pre-emphasis
    a = _lpc(seg, LPC_ORDER)
    if a is None:
        return []
    out = []
    for rt in np.roots(a):
        if np.imag(rt) <= 0.01:
            continue
        f = np.arctan2(np.imag(rt), np.real(rt)) * LPC_SR / (2 * np.pi)
        bw = -0.5 * (LPC_SR / (2 * np.pi)) * np.log(abs(rt) + 1e-12)
        if 200 < f < 4500 and bw < 700:
            out.append(f)
    return sorted(out)


def _frames(media: str, t0: float, t1: float, sr: int, step: float, win: float):
    pad = 0.05
    x = grab(media, max(t0 - pad, 0.0), t1 + pad, sr)
    n = int(win * sr)
    t = t0
    while t < t1:
        i = int((t - (t0 - pad)) * sr)
        seg = x[i:i + n]
        if len(seg) < n:
            return
        yield t, seg
        t += step


def run_formant(media, label, t0, t1, step=0.015, win=0.030):
    print(f"\n[formant] {label}  [{t0:.3f}-{t1:.3f}]")
    print("      t      rms      F1     F2     F3     F4")
    for t, seg in _frames(media, t0, t1, LPC_SR, step, win):
        rms = 10 * np.log10(np.mean(seg ** 2) + 1e-20)
        fs = formants(seg)
        print(f"  {t:8.3f} {rms:7.1f}  " + "  ".join(f"{f:5.0f}" for f in fs[:4]))


def run_sib(media, label, t0, t1, step=0.010, win=0.020):
    print(f"\n[sib] {label}  [{t0:.3f}-{t1:.3f}]   fraction of 50-8k energy in 4-8 kHz")
    for t, seg in _frames(media, t0, t1, WIDE_SR, step, win):
        X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        f = np.fft.rfftfreq(len(seg), 1.0 / WIDE_SR)
        e = lambda lo, hi: X[(f >= lo) & (f < hi)].sum()
        frac = e(4000, 8000) / (e(50, 8000) + 1e-20)
        rms = 10 * np.log10(np.mean(seg ** 2) + 1e-20)
        print(f"  {t:8.3f} rms={rms:7.1f}  sib={frac:.3f} {'#' * int(frac * 50)}")


def run_rms(media, label, t0, t1, step=0.010, win=0.040):
    print(f"\n[rms] {label}  [{t0:.3f}-{t1:.3f}]")
    for t, seg in _frames(media, t0, t1, WIDE_SR, step, win):
        rms = 10 * np.log10(np.mean(seg ** 2) + 1e-20)
        print(f"  {t:8.3f} rms={rms:7.1f} {'#' * max(int((rms + 70) / 2), 0)}")


MODES = {"formant": run_formant, "sib": run_sib, "rms": run_rms}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", help="source_clean.mp4 / final.mp4")
    ap.add_argument("mode", choices=[*MODES, "batch"])
    ap.add_argument("args", nargs="*", help="start end  |  probes.json (batch)")
    ap.add_argument("--label", default="probe")
    ap.add_argument("--step", type=float)
    ap.add_argument("--win", type=float)
    a = ap.parse_args()

    kw = {k: v for k, v in (("step", a.step), ("win", a.win)) if v is not None}

    if a.mode == "batch":
        for item in json.loads(Path(a.args[0]).read_text(encoding="utf-8")):
            mode, label, t0, t1 = item[0], item[1], float(item[2]), float(item[3])
            MODES[mode](a.media, label, t0, t1, **kw)
        return

    if len(a.args) != 2:
        ap.error(f"{a.mode} needs: start end")
    MODES[a.mode](a.media, a.label, float(a.args[0]), float(a.args[1]), **kw)


if __name__ == "__main__":
    main()
