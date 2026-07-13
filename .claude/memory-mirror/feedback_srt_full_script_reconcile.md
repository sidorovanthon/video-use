---
name: feedback_srt_full_script_reconcile
description: "SRT text must be reconciled WORD-BY-WORD against the user's supplied script, not just term/proper-noun spot-checked — Scribe drops plurals, contractions, articles and mis-hears function words"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcb26f67-1934-4e93-91eb-0c79d77a7c03
---

The master SRT is built from the Scribe transcript, so it reflects what was
*heard*, not the user's written script. On edit-26 I only spot-checked proper
nouns/terms (BPMN/DSL/XML/Claude/Bizagi) and shipped — the user caught real
text drift: "notation"→ should be "notations", "Domain Specific"→ "domain-specific",
plus "I already"→"I've already", "diagrams and"→"diagrams in", "that the"→"that a",
"by human being"→"by a human being".

**Why:** Scribe reliably drops trailing plural -s, contraction 've/'ll, unstressed
articles ("a"), and swaps short function words (in/and, the/a). A term-only check
misses all of these. The user supplies the script "для сверки" (for cross-check)
precisely so captions match the written version verbatim.

**How to apply (Phase 5):** after building master.srt, diff EVERY segment's caption
text against the user's prompt script token-by-token (lowercased, punctuation-agnostic),
list ALL discrepancies, and fix them in a transcript COPY, then rebuild — never edit
the Scribe cache ([[feedback_srt_stutter_token]]). Mechanics that worked:
- substitutions/plurals/contractions → override the word token's `text`;
- hyphenated compounds ("domain-specific") → merge the two Scribe tokens into one
  (set text w/ hyphen, extend `end` to the 2nd token's end, drop the 2nd) so the
  2-word chunker shows it as one unit;
- a script word Scribe never emitted ("a") → insert a short word token in the
  inter-word gap (borrow ~0.08s between neighbors);
- build via `build_master_srt(edl, <scratch_dir_with_corrected_S0>, master.srt)`.
Only word-forms need fixing — captions are UPPERCASE 2-word chunks, so pure comma/
dash/paren differences don't show; do NOT inject parens/dashes into caption text.
Captions are a sidecar .srt, so text fixes need NO re-render of final.mp4.

**Deterministic gate (added 2026-07-13):** Phase 1 saves the pasted script verbatim
to `<edit>/script.txt`; the mandatory Phase 6 gate is
`uv run helpers/diff_srt_script.py <edit>/final.srt <edit>/script.txt` — it tokenizes
both (lowercase, punctuation-agnostic, hyphen/apostrophe kept intra-word), aligns with
difflib, prints every MISMATCH (substitution / short insert-delete = drift) and exits
1, while long script-only runs list as intended CUTs (info, exit stays 0 if only cuts).
Ship only on exit 0. This turns the old prose "spot-check" into a real gate. SKILL.md
Phase 5/6 updated to match. Keep going until the gate is green.
