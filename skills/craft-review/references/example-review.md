# Worked Example — Gold-Standard Review

This is the depth, specificity, and format every review should match. (Subject: a "Sleep" alarm
screen — a dark bottom-sheet with a header, AM/PM toggle, a large 7:00 AM display, a time scrubber,
and two bottom action cards.) Note how every finding names its evidence class, how the one taste
call is offered rather than ranked, and how the WCAG failure ranks above craft findings the same
pass measured elsewhere.

---

## Summary
**Screen:** Sleep — alarm set / bedtime sheet. **Job:** set an alarm time and start a sleep session.
**Assumed user:** someone in bed, low light, one hand, wants this fast. **Input:** Figma frame via MCP
(`get_metadata` geometry + `get_variable_defs` → no tokens defined, measured against fallback scale).
**Confidence:** high on the computed and observed findings, medium on the judgment call.

## Scores
**Overall: 78 / 100**  ·  **Accessibility: 82 / 100 (3 computed, 0 judged, 4 human-required)**  ·
**Distinctiveness: 74 / 100 (judged)**

Human-required, untested here and not scored as passes: keyboard operability, focus order,
assistive-tech labels and announcements, and reduced-motion behavior on the scrubber. A screenshot
cannot test any of the four.

Distinctiveness sub-ratings: Intentionality 8 · Distinctiveness 7 · Hierarchy 8 · Restraint 8 ·
Coherence 6. Above the 70 rework line.

## Overall impression
The composition has a clear hero (the 7:00 AM time) and a calm dark palette that fits a bedtime
context. But one text pair fails AA, and the screen is undermined by pervasive **asymmetry** — the
two bottom cards in particular have mismatched internal padding that reads as broken — and by a
**vertical rhythm that isn't on any consistent scale**. Fix the contrast, the symmetry and the grid
and this jumps a full tier.

## Findings by category

### Color & contrast
```
🔴 Critical  Contrast  [computed] — secondary labels fail AA for body text
  What:  "Sleep Aid" / "Alarm Settings" subtitles measure 3.81:1 on the card fill (contrast.py),
         at 14px/regular. The AA floor for that size is 4.5:1.
  Why:   Below the floor the label is unreadable for low-vision users in exactly the low-light
         context this screen is designed for. A WCAG failure is not a polish note.
  Fix:   Lighten to #B3A6C9 (5.12:1 on the same fill), or size them 18px semibold to move under
         the 3:1 large-text rule. The first is the smaller change.
```

### Symmetry, balance & alignment  (highest-signal — 4 findings)
```
🟠 Major  Symmetry  [computed] — bottom action cards have mismatched internal padding
  What:  "GO / Sleep Aid" card: left pad 12px, top pad 24px. "Loud Ring / Alarm Settings" card:
         left pad 20px, top pad 16px. The pair should be identical. (symmetry.py, paired-component
         mismatch.)
  Why:   Paired/repeated components must share padding; unequal padding on side-by-side cards is the
         single most common "unpolished" tell and the eye catches it instantly.
  Fix:   Set both to 16px all sides (spacing/md). Make one a component instance so they can't drift.
```
```
🟡 Minor  Symmetry  [observed] — AM/PM control not balanced within its track
  What:  Selected "AM" pill sits with ~4px inset on the left but ~10px of empty track on the right.
  Why:   A segmented control should be symmetric around its divider; the extra right gap reads as a
         layout bug.
  Fix:   Equalize track padding to 4px both sides; center the two segments on the divider.
```
```
🟡 Minor  Symmetry  [observed] — time scrubber not centered on the current value
  What:  The ruler shows more range to the right of 7:00 (to 8:00) than to the left (stops ~5:30);
         the 7:00 marker isn't the visual center.
  Why:   The selected value is the screen's subject; off-center, the scrubber reads as scrolled
         rather than settled.
  Fix:   Balance the visible range around the selected value (e.g., ±90min), so "now" is centered.
```
```
🔵 Polish  Alignment  [observed] — "AM" unit not baseline-aligned to "7:00"
  What:  The "AM" label rides ~4px above the numerals' baseline.
  Why:   A unit reads as part of the number it modifies; off-baseline it reads as a separate label.
  Fix:   Baseline-align "AM" to "7:00" (or set a deliberate cap-height alignment); it should sit on
         the same line the eye reads.
```

### Spacing, grid & rhythm
```
🟠 Major  Grid  [computed] — vertical band heights aren't on a consistent scale
  What:  Header 48 · AM/PM 56 · scrubber 72 · actions 84. Steps of 8, 16, 12 — no rhythm; 84 isn't
         on an 8pt grid. (symmetry.py, off-grid values.)
  Why:   Inconsistent rhythm makes the screen feel loose even when each part looks fine alone.
  Fix:   Snap to the scale: e.g. 48 / 56 / 72 / 80, or a cleaner 48 / 64 / 72 / 80. Bind heights to
         spacing tokens.
```
```
🔵 Polish  Grid  [computed] — inter-card gap off-scale
  What:  Gap between the two bottom cards is 12px; horizontal side margins are 16px.
  Why:   A gap that matches no other measure on the screen is the kind of near-miss that reads as
         carelessness rather than as a choice.
  Fix:   Use 16px (spacing/md) for the gap to match the margins, or 8px for a tighter pair — either
         is on-scale; 12 is the odd one.
```

## Judgment calls
Not ranked and not deducted: these are taste, offered so you can take them or leave them.

- **Header icon weight against the hero.** The two circular header icons are heavy solid fills. I
  would reduce them to a ghost or tonal fill so the squint test leaves only the 7:00 time standing.
  On a bedtime screen the controls are secondary to the time by intent, but if the icons are the
  primary way users reach alarm settings, the current weight is defensible.

## Priority table
| # | Sev | Category | Issue |
|---|---|---|---|
| 1 | 🔴 | Contrast | Subtitle labels fail AA at 3.81:1 |
| 2 | 🟠 | Symmetry | Bottom cards' mismatched padding |
| 3 | 🟠 | Grid | Inconsistent band-height rhythm |
| 4 | 🟡 | Symmetry | AM/PM not balanced in track |
| 5 | 🟡 | Symmetry | Scrubber not centered on value |
| 6 | 🔵 | Alignment | "AM" baseline |
| 7 | 🔵 | Grid | Inter-card gap 12px |

## Top 3 quick wins
1. Lighten the two subtitle labels to #B3A6C9 — one token, clears the only AA failure on the screen.
2. Make the two bottom cards one component with 16px padding — fixes the most visible craft problem
   in one move.
3. Snap the four band heights to the spacing scale.

## Strengths to preserve
- Strong, unambiguous hero (the 7:00 AM time) — don't let fixes dilute it.
- Calm, low-light-appropriate dark palette.
- Good use of a single accent; the screen isn't noisy.
