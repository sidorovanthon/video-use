#!/usr/bin/env python3
"""Reorganize OBS prep folders by script date while retaining record date.

The default mode is a read-only dry-run. Pass --apply only after reviewing the
generated plan. Matching is based on the recorded transcript against dated
Obsidian script notes, with folder-title matches used as supporting evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


DATE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?P<rest>.*)$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?", re.IGNORECASE)
VIDEO_EXTENSIONS = {".mkv", ".mp4", ".mov"}


@dataclass(frozen=True)
class Note:
    path: Path
    date: str
    stem: str
    normalized_text: str
    trigrams: frozenset[tuple[str, str, str]]


@dataclass
class PlanItem:
    source: str
    destination: str | None
    recording_date: str
    script_note: str | None
    script_date: str | None
    score: float
    runner_up_score: float
    confidence: str
    protected: bool
    reason: str


def normalize(text: str) -> str:
    return " ".join(WORD_RE.findall(text.lower().replace("’", "'")))


def trigrams(text: str) -> frozenset[tuple[str, str, str]]:
    words = normalize(text).split()
    return frozenset(zip(words, words[1:], words[2:]))


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_transcript(folder: Path) -> str:
    transcript = folder / "transcript.json"
    if transcript.exists():
        payload = read_json(transcript)
        if isinstance(payload, dict) and isinstance(payload.get("text"), str):
            return payload["text"]
    packed = sorted(folder.rglob("takes_packed.md"))
    if packed:
        return packed[0].read_text(encoding="utf-8-sig", errors="replace")
    return ""


def folder_video_time(folder: Path) -> float:
    videos = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS]
    if not videos:
        return folder.stat().st_mtime
    return min(p.stat().st_mtime for p in videos)


def parse_old_folder(folder: Path) -> tuple[str, str]:
    match = DATE_RE.match(folder.name)
    if not match:
        raise ValueError(f"Unexpected prep folder name: {folder}")
    recording_date = match.group("date")
    title = match.group("rest").strip()
    return recording_date, title


def load_notes(posts_root: Path) -> list[Note]:
    notes: list[Note] = []
    for path in sorted(posts_root.rglob("*.md")):
        match = DATE_RE.match(path.stem)
        if not match:
            continue
        date = match.group("date")
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        normalized = normalize(text)
        notes.append(Note(path, date, path.stem, normalized, trigrams(text)))
    return notes


def score_note(title: str, transcript: str, note: Note) -> float:
    title_normalized = normalize(title)
    transcript_grams = trigrams(transcript)
    overlap = 0.0
    if transcript_grams:
        overlap = len(transcript_grams & note.trigrams) / len(transcript_grams)

    title_exact = bool(title_normalized and title_normalized in note.normalized_text)
    title_words = title_normalized.split()
    title_grams = trigrams(title)
    title_overlap = 0.0
    if title_grams:
        title_overlap = len(title_grams & note.trigrams) / len(title_grams)
    elif title_words:
        title_overlap = sum(word in note.normalized_text.split() for word in title_words) / len(title_words)

    # Transcript agreement dominates. A unique literal headline is powerful,
    # but generic boilerplate headlines cannot beat a transcript mismatch.
    return overlap * 0.82 + title_overlap * 0.13 + (0.05 if title_exact else 0.0)


def confidence_for(best: float, second: float) -> str:
    gap = best - second
    if best >= 0.72 and gap >= 0.12:
        return "high"
    if best >= 0.45 and gap >= 0.08:
        return "medium"
    return "review"


def discover_folders(prep_root: Path) -> list[Path]:
    folders: list[Path] = []
    for month in sorted(p for p in prep_root.iterdir() if p.is_dir() and MONTH_RE.match(p.name)):
        folders.extend(sorted(p for p in month.iterdir() if p.is_dir() and DATE_RE.match(p.name)))
    return folders


def build_plan(prep_root: Path, posts_root: Path, protected_paths: set[str]) -> list[PlanItem]:
    notes = load_notes(posts_root)
    if not notes:
        raise RuntimeError(f"No dated Markdown notes found under {posts_root}")

    raw_matches: list[tuple[Path, str, str, Note | None, float, float, str]] = []
    for folder in discover_folders(prep_root):
        recording_date, title = parse_old_folder(folder)
        transcript = read_transcript(folder)
        ranked = sorted(((score_note(title, transcript, note), note) for note in notes), reverse=True, key=lambda x: x[0])
        best_score, best_note = ranked[0]
        second_score = ranked[1][0] if len(ranked) > 1 else 0.0
        title_normalized = normalize(title)
        literal_matches = [note for note in notes if title_normalized and title_normalized in note.normalized_text]
        if len(literal_matches) == 1:
            best_note = literal_matches[0]
            best_score = score_note(title, transcript, best_note)
            second_score = max((score_note(title, transcript, note) for note in notes if note != best_note), default=0.0)
            confidence = "high"
        else:
            confidence = confidence_for(best_score, second_score)
        if confidence == "review":
            candidate_note = best_note
            best_note = None
        else:
            candidate_note = best_note
        raw_matches.append((folder, recording_date, title, best_note, best_score, second_score, confidence, candidate_note))

    # More than one capture can belong to one script. Keep the folders separate
    # and add deterministic TAKE numbers in recording order.
    groups: dict[str, list[tuple[Path, str, str, Note | None, float, float, str, Note]]] = {}
    for row in raw_matches:
        note = row[3]
        if note is not None:
            groups.setdefault(str(note.path).lower(), []).append(row)
    take_number: dict[str, tuple[int, int]] = {}
    for rows in groups.values():
        if len(rows) <= 1:
            continue
        ordered = sorted(rows, key=lambda row: (folder_video_time(row[0]), str(row[0]).lower()))
        for index, row in enumerate(ordered, start=1):
            take_number[str(row[0]).lower()] = (index, len(ordered))

    plan: list[PlanItem] = []
    for folder, recording_date, _title, note, best, second, confidence, candidate_note in raw_matches:
        protected = os.path.normcase(str(folder.resolve())) in protected_paths
        if protected:
            plan.append(PlanItem(str(folder), None, recording_date, str(note.path) if note else None,
                                 note.date if note else None, best, second, confidence, True,
                                 "explicitly protected active edit"))
            continue
        if note is None:
            plan.append(PlanItem(str(folder), None, recording_date, str(candidate_note.path), candidate_note.date, best, second,
                                 "review", False, "ambiguous or low-confidence match"))
            continue

        suffix = f" [REC {recording_date}]"
        take = take_number.get(str(folder).lower())
        if take:
            suffix += f" [TAKE {take[0]:02d}]"
        destination = prep_root / note.date[:7] / f"{note.stem}{suffix}"
        reason = "matched by transcript and title"
        plan.append(PlanItem(str(folder), str(destination), recording_date, str(note.path), note.date,
                             best, second, confidence, False, reason))
    return plan


def preflight(plan: list[PlanItem], prep_root: Path) -> None:
    actionable = [item for item in plan if item.destination]
    destinations: dict[str, str] = {}
    for item in actionable:
        source = Path(item.source)
        destination = Path(item.destination or "")
        source.resolve().relative_to(prep_root.resolve())
        destination.resolve().relative_to(prep_root.resolve())
        if not source.is_dir():
            raise RuntimeError(f"Move source is missing: {source}")
        key = os.path.normcase(str(destination.resolve()))
        if key in destinations:
            raise RuntimeError(f"Duplicate destination: {destination} (also from {destinations[key]})")
        destinations[key] = str(source)
        if destination.exists() and source.resolve() != destination.resolve():
            raise RuntimeError(f"Destination already exists: {destination}")
        if len(str(destination)) >= 240:
            raise RuntimeError(f"Destination path is too long ({len(str(destination))}): {destination}")


def replace_edl_paths(folder: Path, old_root: str, new_root: str) -> list[str]:
    updated: list[str] = []
    spellings = (
        (old_root.replace("\\", "\\\\"), new_root.replace("\\", "\\\\")),
        (old_root.replace("\\", "/"), new_root.replace("\\", "/")),
        (old_root, new_root),
    )
    for edl in folder.rglob("edl*.json"):
        original = edl.read_text(encoding="utf-8-sig")
        changed = original
        for old, new in spellings:
            changed = changed.replace(old, new)
        if changed != original:
            edl.write_text(changed, encoding="utf-8", newline="")
            updated.append(str(edl))
    return updated


def validate_edls(prep_root: Path) -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    for edl in prep_root.rglob("edl*.json"):
        try:
            payload = read_json(edl)
            sources = payload.get("sources", {}) if isinstance(payload, dict) else {}
            if not isinstance(sources, dict):
                continue
            for key, value in sources.items():
                if not isinstance(value, str):
                    continue
                source = Path(value) if Path(value).is_absolute() else edl.parent / value
                if not source.is_file():
                    broken.append({"edl": str(edl), "key": str(key), "source": value})
        except Exception as exc:  # validation must report all failures together
            broken.append({"edl": str(edl), "key": "<parse-error>", "source": str(exc)})
    return broken


def apply_plan(plan: list[PlanItem], prep_root: Path) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    completed: list[dict[str, object]] = []
    for item in [row for row in plan if row.destination]:
        source = Path(item.source)
        destination = Path(item.destination or "")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        updated_edls = replace_edl_paths(destination, str(source), str(destination))
        completed.append({"source": str(source), "destination": str(destination), "updated_edls": updated_edls})
    return completed, validate_edls(prep_root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prep-root", type=Path, default=Path(r"M:\videos\OBS\prep"))
    parser.add_argument("--posts-root", type=Path,
                        default=Path(r"S:\badead\creation\Anticode\content creation\Content\Posts\2026"))
    parser.add_argument("--protect", action="append", type=Path, default=[])
    parser.add_argument("--plan", type=Path, default=Path("script_date_migration_plan.json"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    protected = {os.path.normcase(str(path.resolve())) for path in args.protect}
    plan = build_plan(args.prep_root, args.posts_root, protected)
    preflight(plan, args.prep_root)

    summary = {
        "timestamp": dt.datetime.now().astimezone().isoformat(),
        "mode": "apply" if args.apply else "dry-run",
        "total": len(plan),
        "actionable": sum(bool(item.destination) for item in plan),
        "protected": sum(item.protected for item in plan),
        "review": sum(item.confidence == "review" and not item.protected for item in plan),
        "high": sum(item.confidence == "high" for item in plan),
        "medium": sum(item.confidence == "medium" for item in plan),
    }
    output: dict[str, object] = {"summary": summary, "plan": [asdict(item) for item in plan]}
    if args.apply:
        completed, broken = apply_plan(plan, args.prep_root)
        output["completed_moves"] = completed
        output["broken_edl_sources"] = broken
    args.plan.parent.mkdir(parents=True, exist_ok=True)
    args.plan.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Plan written to {args.plan.resolve()}")
    if args.apply and output.get("broken_edl_sources"):
        print("Migration completed, but EDL validation found broken sources.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
