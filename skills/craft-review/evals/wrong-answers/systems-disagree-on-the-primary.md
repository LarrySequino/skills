<!-- Fails: 0, 1, 2, 3, 4, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: SKILL.md §7, the unison test — "do hierarchy, color, type, and space all say the same thing? ... Where they disagree is the most important finding — fix the disagreement, not the symptom." This answer never notices that color and weight mark Save this cart as primary while Place order is the action the screen exists to take. It treats the outline button as a contrast/affordance problem and prescribes darkening its border, ranks a tabular-figures polish note first, reports the on-scale 8px gap under the totals as off the spacing scale, and reads the muted card-expiry line as correct restraint. Intended to fail expectations 0, 1, 2, 3, 4 and 5; it passes 6, since it never calls a text pair a contrast failure. -->
# Design review — Review your order (Thicket)

## Summary

You are right that the measured layer is clean: preflight.py returns no showstoppers,
symmetry.py finds no paired mismatch or grid issue at either width, and every text pair
clears AA comfortably. What is left is a short list of refinements.

**Overall: 92 / 100** · Accessibility 96 · Distinctiveness 74

## Findings

```
🟡 Minor  Typography — the item prices are not tabular
  What:  .totals .row span sets font-variant-numeric: tabular-nums, and .line
         .price sets it too, but the two columns are in different containers with
         different widths, so $28.00 and $14.00 do not align with $42.00 and
         $48.20 in the block below them.
  Why:   Numbers a reader compares should share a right edge. Four prices in one
         panel that nearly line up read as a near-miss rather than a decision.
  Fix:   Give the price column a fixed width (72px) in both the item rows and the
         totals block so all four figures share one right edge.
```

```
🟡 Minor  Spacing — the delivery estimate sits off the rhythm
  What:  .arrives uses margin: 8px 0 24px, so the gap above it is 8px where every
         other vertical gap in the panel is 16px or 24px.
  Why:   An 8px step is off the spacing scale in a panel whose rhythm is
         otherwise 16/24, at the one place the eye is already moving fast.
  Fix:   margin: 24px 0 24px, which puts it back on the ramp.
```

```
🟡 Minor  Affordance — the second button does not read as a button
  What:  .btn-place is a transparent button with a 1px --btn-line border at
         #767c78 on #fbfaf7 (4.09:1). Against the filled .btn-save above it, it
         reads as a secondary or even disabled control.
  Why:   Outline buttons on a light ground are the weakest affordance in the kit,
         and this one is the submit control for the form.
  Fix:   Darken the border to --ink and take the label to 600, so the outline
         treatment reads as deliberate rather than as a disabled state.
```

```
🔵 Polish  Content — the card expiry line is very quiet
  What:  "Visa ending 4417 · expires this month" is 14px --muted, the same
         treatment as the address above it.
  Why:   Arguably correct — the summary should not shout at the customer — but
         the expiry is the one fact here that might stop the payment going
         through.
  Fix:   Leave it. If support sees declines from expired cards, revisit.
```

## Priority

| # | Finding | Severity |
|---|---|---|
| 1 | Price columns not aligned | Minor |
| 2 | 8px gap above the delivery estimate | Minor |
| 3 | Outline button affordance | Minor |
| 4 | Quiet expiry line | Polish |

## Strengths to preserve

The panel's shadow-plus-ring treatment is doing the work a border would do without
eating a pixel of the padding box, the totals rule is an inset shadow for the same
reason, and the two-button stack keeps the destructive-free action out of thumb range
on mobile. Ship it after the three Minors.
