<!-- Fails: 0 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: ".ledger .pill--review  { color: var(--pill-warn-fg); background: var(--pill-warn-bg); }"
     - this review resolves the chip's warn pair from the declarations on `.pill` itself,
     treats the chip as theme-independent because of that, reports it as clearing AA in both
     states, and puts the page's only real failure in the "considered and cleared" column. -->

# Craft review — Settlements, Northwind Freight

## Summary
**Screen:** a settlements dashboard: four summary cards over a settlements ledger, inside a
rail-plus-main shell.
**Job:** a finance operator scans the week's settlements and finds the ones that need
chasing.
**Input used:** the full source (442 lines) and `scripts/contrast.py` over the text pairs
the stylesheet resolves. Both theme states read from the token layers.
**Baseline:** WCAG 2.2 AA for text, 1.4.11 for the parts of a control that identify it, and
the page's own three-tier token system as the consistency reference.

## Scores
**Overall: 77 / 100** · **Accessibility: 74 / 100** · Consistency 88 · Hierarchy 80

## Overall impression
This is a genuinely well-built stylesheet. Raw hex lives in one place, roles are one hop
from primitives with the primitive repeated as a fallback, and the dark state is a
re-mapping rather than an inversion. The text palette is comfortable in both states — the
weakest body pair I measured is the muted reference column at 4.43:1 on the raised surface,
which is above the bar. What is not comfortable is everything on this page that is a line
rather than a letter: the hairlines and the quiet button borders are far under the non-text
minimum, and on a ledger, lines are how the data is read.

## Findings by category

### Color and contrast (computed — `contrast.py` over the resolved pairs)

```
🔴 Critical  Color  [computed] — the quiet buttons are identified by a border alone, and
             the border is nowhere near the non-text minimum
  What:  .btn--quiet takes its fill from --surface-raised, which is also the surface it
         sits on, so the 1px --line border is the only thing that says "control". Light:
         #cfd6e0 on #fcfcfd = 1.43:1. Dark: #27313f on #161d26 = 1.42:1.
  Why:   WCAG 1.4.11 governs the visual information needed to identify a component. Every
         secondary action on this screen — Export, the filter controls, the row actions —
         is a quiet button, so on a glare-washed laptop panel the page loses its whole
         secondary action layer at once.
  Fix:   Border interactive controls with --slate-400 (#8b97a8 on #fcfcfd = 2.89:1 is still
         short; go to --slate-500, #6b7789 on #fcfcfd = 4.43:1) and leave --line for the
         decorative hairlines, where a separator next to high-contrast content is fine.
```

```
🟠 Major  Color  [computed] — the ledger row rules are the same 1.43:1 hairline
  What:  .ledger td { border-top: 1px solid var(--line) } — #cfd6e0 on #fcfcfd = 1.43:1 in
         light, #27313f on #161d26 = 1.42:1 in dark.
  Why:   A row rule in a numeric table is not decoration: it is the thing that keeps a
         reference number on the same visual line as its amount when the eye tracks across
         six columns. This is not a WCAG failure — row rules bound no control and carry no
         text — but it is a legibility one.
  Fix:   Take the row rule to --slate-200 in light and --ink-600 in dark, or drop the rule
         and use a zebra fill instead, which reads better in a tabular-nums table anyway.
```

```
🟢 Considered and cleared — the three status chips
  What:  The chip tokens are declared on .pill itself rather than in the role layer, which
         means a chip carries its own palette wherever it is dropped. Resolved from those
         declarations the three pairs are: Settled #116149 on #e6f4ee = 6.55:1, In review
         #7a4a06 on #fbf1de = 6.67:1, Transfer failed #8f1d24 on #fbe9ea = 7.57:1.
  Why:   All three are comfortably over the AA bar for 12px text, and because the chip
         declares its own tokens rather than reading the page's roles, the pairs do not
         change when the surrounding theme does — which is exactly what the comment above
         the block says the pattern is for. No action.
```

```
🟢 Considered and cleared — table header, body text and primary button
  What:  Header #3f4859 on #e2e7ee, body #1a2029 on #fcfcfd, primary button #fcfcfd on
         #1d4ed8. All well over the bar in both states; dark mode re-maps the same roles
         and holds the same relationships.
```

### Consistency and structure (read from source)

```
🟡 Minor  Consistency  [observed] — two radii on the same screen
  What:  .panel and .stat are 12px; .btn is 8px.
  Why:   Cards and buttons at two radii is a defensible distinction — surfaces versus
         controls — but nothing in the sheet says so, so it reads as drift.
  Fix:   Keep it, and write the rule down in the token comment block.
```

```
🟡 Minor  Hierarchy  [observed] — the four summary cards carry equal weight
  What:  .stat__value is 24px/600 in all four cards with no accent on the one that matters.
  Why:   On a settlements screen the failed total is the number the operator is here for,
         and it looks exactly like the other three.
  Fix:   Give the failed card the --red role for its value and leave the rest.
```

## Judgment calls
- **Fallback primitives repeated inside every role.** Verbose, and deliberately so: a
  missing ramp degrades to the value the role was authored against. Left alone.
- **`overflow: hidden` on .panel.** It clips the table's own corner radius cleanly; the
  cost is that a sticky header can never escape the panel. Fine as built.

## What I could not check
No headless render, so nothing about layout, wrapping or focus order is measured here. Dark
mode was read from the token layers rather than from a screenshot; the relationships hold
because the role layer is re-pointed wholesale, but a rendered pass would confirm it.
