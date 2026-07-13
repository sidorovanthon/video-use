"""Pre-render grade gate: measure face-crop luma per EDL segment and build
the N-up grade comparison sheet at the brightest talking frame.

This mechanizes the rule that burned edit-19/20: pick the grade by MEASURED
face exposure of EVERY kept segment (never inherit the series' previous
grade), and always show a face-crop comparison sheet before the full render.

Usage:
    # 1) scan: per-segment face-crop YAVG + the brightest sample overall
    python helpers/grade_sheet.py scan <edl.json> [--crop 660:860:210:300] [--step 2.0]

    # 2) sheet: 5-up face-crop ladder at time T (default: brightest from scan)
    python helpers/grade_sheet.py sheet <edl.json> --time 23.0 [--out <edit>/verify]

Outputs of `sheet`: cmp_raw.png, cmp_v7-contrast.png, cmp_lift52/58/66.png and
a combined sheet.png (side by side, in that order) in --out.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Default face crop for the 1080x1920 OBS talking-head framing (~660x860 box
# around the face). Override with --crop w:h:x:y when the framing differs.
DEFAULT_CROP = "660:860:210:300"

BALANCE = "colorbalance=rm=0.04:gm=-0.01:bm=-0.05:rh=0.03:bh=-0.04"
EQ = "eq=contrast=1.08:saturation=0.97"

def _lift(mid: float) -> str:
    return (f"{EQ},{BALANCE},"
            f"curves=master='0/0.04 0.28/0.30 0.5/{mid:.2f} 0.72/0.82 1/1'")

GRADES: dict[str, str | None] = {
    "raw": None,
    "v7-contrast": (f"{EQ},{BALANCE},"
                    "curves=master='0/0 0.28/0.17 0.5/0.46 0.72/0.69 1/1'"),
    "lift52": _lift(0.52),
    "lift58": _lift(0.58),
    "lift66": _lift(0.66),
}

YAVG_RE = re.compile(r"lavfi\.signalstats\.YAVG=([\d.]+)")


def yavg_at(src: Path, t: float, crop: str, grade: str | None = None) -> float | None:
    """Face-crop YAVG of the frame at time t (optionally after a grade chain)."""
    vf = f"crop={crop}," + (f"{grade}," if grade else "") + "signalstats,metadata=print"
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", f"{t:.3f}", "-i", str(src),
         "-vf", vf, "-frames:v", "1", "-f", "null", "-"],
        capture_output=True, text=True, errors="replace",
    )
    m = YAVG_RE.search(proc.stderr)
    return float(m.group(1)) if m else None


def load_edl(edl_path: Path) -> tuple[dict, dict[str, Path]]:
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    base = edl_path.parent
    sources = {k: (Path(v) if Path(v).is_absolute() else base / v)
               for k, v in edl["sources"].items()}
    return edl, sources


def cmd_scan(args: argparse.Namespace) -> None:
    edl, sources = load_edl(args.edl)
    best_t, best_y, best_src = None, -1.0, None
    print(f"face crop {args.crop}, sampling every {args.step}s\n")
    print(f"{'seg':>4} {'beat':10s} {'range':>17s} {'min':>6s} {'avg':>6s} {'max':>6s}  max@t")
    for i, r in enumerate(edl["ranges"]):
        src = sources[r["source"]]
        start, end = float(r["start"]), float(r["end"])
        samples: list[tuple[float, float]] = []
        t = start
        while t < end:
            y = yavg_at(src, t, args.crop)
            if y is not None:
                samples.append((t, y))
            t += args.step
        if not samples:
            print(f"{i:>4} {r.get('beat', ''):10s} {start:8.2f}-{end:8.2f}  (no samples)")
            continue
        ys = [y for _, y in samples]
        mt, my = max(samples, key=lambda s: s[1])
        beat = r.get("beat") or r.get("note") or ""
        print(f"{i:>4} {beat:10s} {start:8.2f}-{end:8.2f} {min(ys):6.1f} {sum(ys)/len(ys):6.1f} {max(ys):6.1f}  t={mt:.1f}")
        if my > best_y:
            best_t, best_y, best_src = mt, my, src
    if best_t is not None:
        print(f"\nbrightest sample: YAVG {best_y:.1f} at t={best_t:.2f} ({best_src.name})")
        print(f"next: python helpers/grade_sheet.py sheet {args.edl} --time {best_t:.2f}")
        print("REMINDER: verify the chosen frame is a leaned-in TALKING frame "
              "(eyes open, face large) — step nearby ±1s if not.")


def cmd_sheet(args: argparse.Namespace) -> None:
    edl, sources = load_edl(args.edl)
    # Which source covers --time? Default to the first source.
    src = None
    for r in edl["ranges"]:
        if float(r["start"]) <= args.time <= float(r["end"]):
            src = sources[r["source"]]
            break
    if src is None:
        src = next(iter(sources.values()))
    out_dir = args.out or (args.edl.parent / "verify")
    out_dir.mkdir(parents=True, exist_ok=True)

    panels: list[Path] = []
    print(f"sheet at t={args.time:.2f} from {src.name} (crop {args.crop})\n")
    for name, grade in GRADES.items():
        png = out_dir / f"cmp_{name}.png"
        vf = f"crop={args.crop}" + (f",{grade}" if grade else "")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-ss", f"{args.time:.3f}", "-i", str(src),
             "-vf", vf, "-frames:v", "1", str(png)],
            check=True,
        )
        y = yavg_at(src, args.time, args.crop, grade)
        print(f"  {name:12s} face YAVG {y:6.1f}  -> {png.name}")
        panels.append(png)

    sheet = out_dir / "sheet.png"
    n = len(panels)
    inputs: list[str] = []
    for p in panels:
        inputs += ["-i", str(p)]
    filt = "".join(f"[{i}:v]" for i in range(n)) + f"hstack=inputs={n}[v]"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
         "-filter_complex", filt, "-map", "[v]", str(sheet)],
        check=True,
    )
    print(f"\ncombined sheet (left→right: {', '.join(GRADES)}): {sheet}")
    print("GATE: show this sheet and get an explicit grade choice BEFORE the full render.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="per-segment face-crop YAVG")
    p_scan.add_argument("edl", type=Path)
    p_scan.add_argument("--crop", default=DEFAULT_CROP)
    p_scan.add_argument("--step", type=float, default=2.0)
    p_scan.set_defaults(func=cmd_scan)

    p_sheet = sub.add_parser("sheet", help="N-up grade ladder at a timestamp")
    p_sheet.add_argument("edl", type=Path)
    p_sheet.add_argument("--time", type=float, required=True)
    p_sheet.add_argument("--crop", default=DEFAULT_CROP)
    p_sheet.add_argument("--out", type=Path, default=None)
    p_sheet.set_defaults(func=cmd_sheet)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
