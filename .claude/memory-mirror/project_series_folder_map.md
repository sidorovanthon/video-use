---
name: project-series-folder-map
description: Map from the English series names used in the grade memories to the (Russian, truncated) prep folder names after the 2026-08-24 script-date rename
metadata:
  type: project
---

The grade memories name series in English ("Migrating Knowledgebase With AI",
"Systems Analysis", "Keep Codex Away from Your Computer"), but after the
2026-08-24 script-date rename the prep folders carry Russian, ~22-char
truncated titles. Matching a series by folder title no longer works — use this
map (paths relative to `M:/videos/OBS/prep/`):

| Series (memory name) | edits | Folder |
|---|---|---|
| How to Avoid Losing Context | edit-12..16 | `2026-02/2026-02-21-0X - Progress [REC …]` |
| Migrating Knowledgebase With AI (Parts 1–7) | edit-17..23 | `2026-02/2026-02-25-0X - Экcпорт из Notion с AI [REC …]` |
| AI + Bubble | edit-24, 25 | `2026-02/2026-02-27-0X - Как подружить AI с Bu... [REC …]` |
| Systems Analysis (first shoot) | edit-26, 27 | `2026-02/2026-02-26-0X - Системный анализ и ИИ [REC 2026-04-16]` |
| Systems Analysis (2026-05-14 shoot) | edit-31..34 | `2026-02/2026-02-26-0X - Организация базы знан... [REC 2026-05-14]` |
| Systems Analysis (2026-05-21 shoot) | edit-35..38 | `2026-02/2026-02-26-0X - База знаний с AI часть 2 [REC 2026-05-21]` |
| Keep Codex Away from Your Computer | edit-28..30 | `2026-03/2026-03-01-0X - Не допускай Codex к к... [REC 2026-05-07]` |
| standalone AI-tips (Superpowers etc.) | edit-39..42 | `2026-04/2026-04-1X - <title> [REC 2026-05-28]` |

**Why:** the grade rules are per-series ([[feedback-grade-brightness]],
[[feedback-grade-migrating-series]], [[feedback-grade-systems-analysis-series]],
[[feedback-grade-keep-codex-series]]) and the folder name is now the only
on-disk clue to which series a new video belongs to — but it is truncated and
translated, so a title match silently fails.

**How to apply:** identify a video's series by locating its `edit-NN` (or its
script-date prefix) in this table, never by string-matching the English series
name against the folder. The `-NN` sequence inside one script date is the part
order. Folder layout itself: [[project-edit-dir-convention]].
