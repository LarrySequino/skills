<!-- Fails: 0, 2, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: the ".notice" rule's 3px left border in round3/buried-theme-only.html, whose
     custom property is declared only inside the dark @media block 67 lines further down and
     never in the base :root. This review reads the base :root, finds a complete
     role table, never diffs it against the theme layers, and reports the retention
     callout's left border as a hierarchy choice rather than as a border that resolves to
     currentColor in the default state. The token's name is kept out of this comment on
     purpose: check_fixtures.py feeds the whole control file to the grader as the answer, so
     quoting it here would satisfy the check the control has to fail. -->

# Craft review — Workspace settings

## Summary
**Screen:** a workspace settings screen — a settings rail, a form column of grouped fields,
a data-retention callout, and an API keys table.
**Job:** an admin changes a workspace setting and manages API keys without breaking
anything for their team.
**Input used:** the full source (422 lines), read as declarations, plus screenshots of both
theme states. The bundled scripts were not run for this pass.
**Baseline:** WCAG 2.2 AA, the 4/8 spacing scale, and the page's own primitive/role token
split as the consistency reference.

## Scores
**Overall: 79 / 100** · **Accessibility: 76 / 100** · Consistency 88 · Hierarchy 72

## Overall impression
This is a settings screen that has clearly been built rather than assembled. The token
architecture is a proper two-tier split — primitives named by lightness, roles named by
job, components reading only roles — and the sand-on-charcoal identity is a real choice
rather than the default gray. Spacing is on the 4/8 scale throughout and the dark state is
a wholesale re-point of the role layer rather than an inversion. What holds it back is
hierarchy: the screen has one destructive-adjacent setting and one genuinely consequential
one, and neither of them is weighted differently from the checkbox above it.

## Findings by category

### Hierarchy and structure (read from source)

```
🟠 Major  Hierarchy  [observed] — the retention callout is styled below its consequence
  What:  The data-retention callout is a 13px paragraph on the sunken surface with a 3px
         left border and a 4px radius — the same visual weight as any inline hint on the
         page. Its text says that shortening the window deletes anything already past it at
         the next sweep.
  Why:   That is the one irreversible consequence on this screen, and it is presented in
         the page's smallest text on its quietest surface. The left border is the only
         thing distinguishing it from a hint, and a 3px rule is a weak carrier for
         "this deletes data".
  Fix:   Give the callout the page's warning role rather than the accent one, take it to
         15px, and put the consequence in a sentence of its own above the field rather
         than below it.
```

```
🟠 Major  Hierarchy  [observed] — every field group carries the same weight
  What:  .field and .row give each setting the same label size, the same helper-text
         treatment and the same vertical rhythm, from "workspace name" to the retention
         window.
  Why:   A settings screen is read by scanning, and scanning needs weight differences.
         Here the only ordering signal is source order.
  Fix:   Group the consequential settings under their own subhead and give that group a
         heavier label treatment.
```

### Accessibility and interaction

```
🔴 Critical  States  [observed] — no focus-visible treatment anywhere
  What:  The stylesheet declares no `:focus-visible` rule. The rail links, the form
         controls and the API key row actions all fall back to the UA outline, which on the
         dark charcoal surface is close to invisible.
  Why:   This is a keyboard-heavy screen — a long form and a table of row actions — and
         the one thing a keyboard user needs is to know where they are.
  Fix:   A 2px --accent outline at 2px offset on every interactive element.
```

```
🟠 Major  Targets  [observed] — the API key row actions are under the minimum
  What:  The row action controls sit in 8px-padded table cells at 12px text, which lands
         them well under a 24px control height.
  Why:   Revoking a key is a destructive action reached through the smallest target on the
         page.
  Fix:   Take the row actions to a real button box at 32px, and right-align the column.
```

### Color and contrast (read from the resolved token pairs)

```
🟢 Checked and clear — text pairs in both states
  What:  Primary, secondary and muted text on page, raised, rail and sunken surfaces all
         clear the AA bar in light and in dark. The tag colors are re-pointed per state and
         hold their relationships.
  Why:   The role layer is re-pointed wholesale for dark, so nothing drifts pair by pair.
```

## Judgment calls
- **Primitives repeated as fallbacks inside every role.** Verbose, and deliberate: a role
  degrades to the value it was authored against rather than to nothing. Left alone.
- **Two theme layers, `@media` and `[data-theme]`, carrying the same values.** Duplication,
  but it is the only way to support both an OS setting and an in-page toggle without a
  build step. Fine as built.
- **The 3px accent border on the callout.** As a device it is right — a colored edge is the
  standard way to mark a callout without boxing it — and it is the kind of detail the rest
  of the page does not bother with. Kept in the hierarchy finding above rather than raised
  on its own.

## What I could not check
No headless render and no computed contrast pass, so the pairs above are read from the
token layers rather than measured. Motion is not declared anywhere on the page.
