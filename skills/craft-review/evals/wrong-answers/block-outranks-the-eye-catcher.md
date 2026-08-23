<!-- Fails: 1, 2, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Craft review — Pipeline overview (Halyard)

## Summary

Competent analytics layout, well-tokenized, sensible density. What holds it back is the
brand treatment: a full-bleed purple-to-blue gradient hero plus two gradient-clipped
section titles, which is the single most recognizable "generated dashboard" signature
going, and it is the first and third thing the reader sees. Under that, a couple of
consistency slips and some tidying.

**Overall: 73 / 100** · Distinctiveness 58 · Consistency 70 · Hierarchy 78 · Color 80

## Findings

```
🔴 Critical  Distinctiveness — the gradient hero and the gradient-clipped titles
  What:  .hero runs a 135deg purple (#7c3aed) to blue (#2563eb) wash across the
         full width at 56px of vertical padding, and .section-title repeats the
         same ramp clipped to the text with color: transparent.
  Why:   This exact pair — violet-to-blue hero, gradient text headings — is the
         house style of every template dashboard shipped in the last three years.
         It reads as decoration applied to the product rather than as the
         product's own voice, and it is doing no informational work: the hero
         carries one sentence, and the two titles are structural labels.
         The clipped text also drops out entirely in forced-colors mode, where
         color: transparent stays transparent.
  Fix:   Flatten the hero to a single brand tone with the wordmark and one line of
         copy, and set the section titles in --ink at 20px / 600. Keep the ramp
         for the chart series, where a gradient means something.
```

```
🟠 Major  Consistency — two radii on the same screen
  What:  .card is border-radius 8px; .panel and .runs are 12px. The plot inside
         the panel is 8px, the chips are 12px, the buttons 8px.
  Why:   Cards and panels sit 24px apart in the same column, so the two corner
         treatments are visible side by side. Nothing distinguishes the two
         groups semantically, which makes the difference look accidental.
  Fix:   One value, 12px for every surface and 8px for controls inside them.
```

```
🟠 Major  Motion — the card lift has no reason and no partner
  What:  .card transitions transform and box-shadow over 200ms and lifts 2px on
         hover, but the cards are not links or buttons and nothing happens on
         click.
  Why:   Hover lift is an affordance. On a static tile it promises an interaction
         the screen does not have.
  Fix:   Drop the transform, or make the tiles navigate to the filtered run list
         and give them a focus style to match.
```

```
🟡 Minor  Tokens — --canvas is declared in both themes and never applied
  What:  --canvas is defined at :root and in the dark block, and body sets color
         and font but no background of its own.
  Why:   A token that resolves to nothing is dead weight in the sheet, and the
         page ground ends up inherited rather than stated.
  Fix:   body { background: var(--canvas); } and the token starts earning its
         place.
```

```
🔵 Polish  Typography — the uppercase labels are running two tracking values
  What:  .card .label, th and .chip are all 13px uppercase, but the chip has no
         letter-spacing while the other two carry 0.04em.
  Fix:   0.04em on the chip too.
```

## What is working

The color pairs are comfortable in both themes, the 4/8 spacing rhythm holds everywhere
including the responsive block, the plot carries a real aria-label rather than a decorative
one, and the table's "Retrying" row is the sort of honest empty value most dashboards hide.

## If you change one thing

Lose the gradient. Everything else on this screen is doing its job quietly and well, and
the wash on top makes a careful product look like a template.
