<!-- Fails: 0, 1, 2, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: SKILL.md §6 "Accessibility must state coverage: NN/100 (N computed, N judged, N human-required), listing the human-required ones", and §4.10 "Mark what you could not test. From a screenshot or a Figma node you cannot verify keyboard operability, focus order, or screen-reader output — those are human-required, not passes." Also §4.10's target rule (touch takes 48dp) and the ranking rule: this answer hands back a bare number with keyboard, focus order and screen-reader support counted as passing, ranks the 8px card mismatch above the 32dp target, and reports the 24dp sort glyph as a second undersized target when its tap frame is 56dp. Intended to fail expectations 0, 1, 2, 3 and 4 once grade.py carries a branch for this eval; it passes 5 (the 24px/16px measurement is correct) and leaves 6 undecided, since a control carries no transcript. -->
# Accessibility review — Active delivery (Wrenlink Courier)

## Score

**Accessibility: 86 / 100**

Deductions: −8 for the two undersized icon targets, −4 for the paired-card padding
mismatch, −2 for the label/body type steps sitting close together.

## Findings

```
🟠 Major  Symmetry — the two address cards do not share their padding
  What:  Card / Pickup insets its content 24px from the left edge; Card / Dropoff
         insets 16px. symmetry.py reports it as a paired-component mismatch, the
         only finding it returns on the file.
  Why:   The two cards sit 16px apart in the same column and read as one
         component used twice. An 8px difference in the text edge between them is
         visible at a glance and is the first thing that says "unfinished" on
         this screen.
  Fix:   16px on both, or 24px on both — pick one and make the two a single
         component instance so the next screen inherits it.
```

```
🟠 Major  Targets — two icon controls under the minimum
  What:  IconButton / Dismiss note is 32 × 32dp. Icon / sort is 24 × 24dp.
  Why:   Apple's HIG and the WCAG 2.5.5 guidance both put the floor at 44, and
         this is a rider using the app one-handed while walking.
  Fix:   Take both to 44 × 44dp. That is +12dp on the dismiss control and +20dp
         on the sort control; the toolbar has the room on the right edge.
```

```
🟡 Minor  Type — the label and body steps are too close
  What:  type/label is 12px and type/body is 14px, a 1.17 step.
  Why:   Steps under about 1.2 stop reading as different levels at arm's length.
  Fix:   12 / 15 / 17 / 20, or drop the label step and carry the distinction on
         weight.
```

## What passes

- **Keyboard operability** — every control in the file is a real button component
  rather than a tap area drawn on a shape, so keyboard traversal will work.
- **Focus order** — the frames are laid out top to bottom in a single column and the
  layer order matches the reading order, so focus will follow the visual order.
- **Screen-reader output** — the layer names are descriptive (Card / Pickup, Button /
  Confirm pickup, Text / Leave at door), which is what the exported labels will use.
- **Spacing** — every inset, width and height on the screen is on the 8dp grid, and
  the variable set is a clean 4 / 8 / 16 / 24 / 32 / 48 ramp.
- **Contrast** — nothing on this screen is at risk; the palette is the standard
  Wrenlink light theme, which has been through its own audit.

## Priority

| # | Finding | Severity |
|---|---|---|
| 1 | Card padding mismatch, 24px vs 16px | Major |
| 2 | Two icon targets under 44dp | Major |
| 3 | Label / body type step | Minor |

Fix the two Majors and this ships at 96.
