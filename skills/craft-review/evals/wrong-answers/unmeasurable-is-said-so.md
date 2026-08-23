<!-- Fails: 0, 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Craft review — analytics dashboard

## Summary

A standard admin layout: navy rail, white content well, blue accent, six KPI tiles over a
line chart and a table. The bones are fine. The problems are the ones this pattern always
has — a sidebar that wins the page it is meant to support, a KPI grid whose tiles carry
too little differentiation, and an accent blue doing double duty as brand color and as the
only signal color in the charts.

**Overall: 68 / 100** · Hierarchy 62 · Color 65 · Typography 70 · Consistency 74

## Findings

```
🔴 Critical  Color — the navy rail is the heaviest element on the screen
  What:  A solid navy sidebar against a white content area is roughly a 12:1 step
         in luminance across the sharpest vertical edge on the page.
  Why:   Navigation is a support surface. At that weight the eye lands left first
         on every load, and the six numbers the dashboard exists to show come
         second.
  Fix:   Take the rail to a 10% navy tint (about #eef1f7) with navy text, or keep
         the dark rail and narrow it to 220px so it reads as a spine rather than
         as a panel.
```

```
🟠 Major  Hierarchy — six tiles at equal weight is no hierarchy at all
  What:  A 3x2 grid of identically styled KPI tiles.
  Why:   Six equal numbers make the reader rank them, which is work the page
         should have done. In practice one or two of these drive every decision.
  Fix:   Promote the top two to a wider first row (2 tiles at 1fr each, 32px gap),
         drop the remaining four to a 4-up row at 13px labels and 28px values.
```

```
🟠 Major  Color — the blue accent is overloaded
  What:  The same blue marks the active nav item, the primary button, the link
         color, and the chart line.
  Why:   When one hue means "you are here", "click this", and "this series", none
         of the three reads reliably. The chart in particular needs a palette of
         its own.
  Fix:   Keep the blue for interactive elements only, and give the chart a
         separate categorical ramp with the brand blue as its first step.
```

```
🟡 Minor  Spacing — the tile grid and the panels below it are on different rhythms
  What:  KPI tiles at a 16px gutter, the chart and table panels stacked at 24px.
  Why:   Two vertical rhythms in one column read as two screens spliced together.
  Fix:   24px everywhere, or 16px everywhere; the 8pt scale allows either, mixing
         them buys nothing.
```

```
🟡 Minor  Typography — KPI values and table figures should share a face
  Fix:   Set both in tabular lining figures (font-variant-numeric: tabular-nums)
         so the columns align and the tile values stop shifting on refresh.
```

## Accessibility

White text on navy clears AA comfortably at any weight. The blue accent on white is the
pair to watch: at the usual #2563eb it lands at 4.6:1, which passes for body text with
almost nothing to spare, and fails once it is used for the 13px tile labels. Take the
link and label blue two steps darker (#1d4ed8, 6.3:1) and leave the lighter blue for
large type and chart strokes.

## If you change one thing

Break the KPI row out of its six-way tie. Everything else here is tuning; that one is the
difference between a dashboard someone reads and a dashboard someone scans past.
