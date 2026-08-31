---
name: feedback_grade_keep_codex_series
description: "Keep Codex Away from Your Computer" series default = v7-contrast (dim source, moody look chosen explicitly); still measure + show the sheet
metadata:
  type: feedback
---

The "Keep Codex Away from Your Computer, or How It Deleted Important System
Services" series (Part 1 = edit-28) grades to **v7-contrast**, even though the
source is DIM (face raw YAVG ~66–69). The 5-up sheet showed v7-contrast crushing
the face-crop to YAVG ~44 and the dim→lift default would have picked a lift, but
the user explicitly chose v7-contrast for the moody, high-contrast look — the
same call they made on edit-25.

**Why:** dim source does NOT force a lift grade; the user reads the actual full
frame (not the crop YAVG number, which misleads on contrast presets) and takes
the aesthetic call. This series wants contrast/mood, opposite of the
[[feedback_grade_brightness]] "Losing Context" v7-lift default and aligned with
[[feedback_grade_migrating_series]]'s v7-contrast (though for a different reason —
Migrating faces were bright, this one is dim-by-choice).

**How to apply:** for later parts of this series, EXPECT v7-contrast, but still
`grade_sheet.py scan` + build the 5-up sheet + get the explicit pick — series
continuity is a default, never a rule (edit-19/edit-27 lesson). If face luma is
uniform across segments (as on edit-28, spread <3), no per-segment gamma is
needed; a single top-level grade suffices.

Confirmed three times running: Part 1 = edit-28 (raw ~66–69), Part 2 = edit-29
(raw ~68–71), Part 3 = edit-30 (raw 68.6–71.0, spread 2.4). Every part so far has
been dim + uniform → single v7-contrast, no per-segment gamma.

Third confirmation (2026-08-17, edit-39 "Superpowers", a standalone AI-tips video, not this series): raw face YAVG 65-74 — dim by the decision rule — and the user again picked v7-contrast (face crop 48.5) over all three lift variants, and declined per-segment gamma match on a 7-unit front-to-back drift. So "dim source" is a prior about which grades to SHOW, never a prediction of the pick.

**Streak broken (2026-08-31, edit-47 "Handoff prompt", standalone AI-tips video).**
After ten consecutive v7-contrast picks the user chose **v7-lift58**. The source was
the dimmest yet — raw face YAVG **51.0–56.3**, spread only 4.8 — and v7-contrast
crushed the crop to **30.9** against lift52/58/66 at 54.8/55.4/56.3. So the rule is
neither "dim → lift" nor "always contrast": on a source this dark v7-contrast has no
headroom left, and the pick swings back to lift. Keep showing the full 5-up sheet and
keep asking; never carry a streak forward as a decision.
