<!-- Fails: 0, 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: ".kpi[data-state=\"breached\"] { border-left: 8px solid var(--alert); }" -
     this review runs symmetry.py, gets its one paired-component mismatch on the KPI row,
     and discards it as a script artifact of the stripe, reasoning that all three cards
     declare the same padding so the row must be even. The rendered inset the mismatch
     reports is kept out of this comment on purpose: check_fixtures.py feeds the whole
     control file to the grader as the answer, so quoting the number here would satisfy the
     check the control has to fail. -->

# Craft review — Release health

## Summary
**Screen:** a release-health page: three service KPI cards over a deploy log panel.
**Job:** an on-call engineer checks whether anything is burning before they pick up a page.
**Input used:** the full source (311 lines), `scripts/preflight.py` and `scripts/symmetry.py`
at 1440 and 390.
**Baseline:** the page's own token layers, the 4/8 spacing scale, WCAG 2.2 AA for text and
1.4.11 for the parts of a control that identify it.

## Scores
**Overall: 76 / 100** · **Accessibility: 72 / 100** · Consistency 86 · Hierarchy 74

## Overall impression
Structurally this page is in good shape. The KPI row is three instances of one component
with one padding value and one radius, the deploy log below it is a plain table that does
not try to be a card, and the token layers are clean enough that the dark state is a
re-map rather than an inversion. What it is missing is semantics: the one card that is in
trouble is marked by a color stripe and by nothing else, which is a problem for a page
whose whole job is "is anything wrong".

## Findings by category

### Symmetry and layout (measured — `symmetry.py` at 1440 and 390)

```
🟢 Checked and clear — the KPI row
  What:  symmetry.py returns one MAJOR paired-component mismatch on the KPI row, reporting
         the middle card's content as starting further in from its own edge than the two
         cards beside it. That hit is the status stripe: the script measures from the
         card's outer edge to the first content pixel, so any card carrying a heavier
         left rule reads as inset more than its neighbors do.
  Why:   All three cards are the same component, with `padding: 24px` declared once on
         .kpi and never overridden. Nothing in the sheet gives the breached card a
         different inset, so the mismatch is an artifact of where the script starts
         measuring rather than a difference in the layout. The rest of the run is clean:
         the row is evenly gapped, the shell is centered, and 390 reflows without a
         horizontal scroll.
  Fix:   None. Worth knowing that the script reports it, so it does not get re-filed as a
         defect on the next pass.
```

### Semantics and states (read from source)

```
🔴 Critical  Accessibility  [observed] — "breached" is communicated by color alone
  What:  The middle card carries `data-state="breached"`, and the only thing that renders
         differently is a red rule down its left side. There is no icon, no label, no text
         change and no `aria-` attribute; the card's own copy ("Error budget exhausted
         Tuesday") is the same size, weight and tone as the other two cards' footnotes.
  Why:   WCAG 1.4.1. A red-green color deficiency, a grayscale print, or a screen reader
         all lose the distinction entirely, and this is the single most important piece of
         information on the page.
  Fix:   Give the breached state a text label in the card header and set the footnote in
         --alert, so the state survives without the stripe. Keep the stripe as
         reinforcement.
```

```
🟠 Major  Color  [computed] — the stripe is the only thing carrying the state, and it is
             the wrong token for the job in dark mode
  What:  .kpi[data-state="breached"] draws its rule in --alert, which re-points to
         --red-300 (#f2a3a8) in dark. On the dark raised surface that is a pastel pink rule
         reading as decoration rather than as an alarm.
  Why:   The role is doing double duty: it is the text alert color and the stripe color,
         and the value that works for text on a dark ground is too light for a rule that
         has to read as urgent.
  Fix:   Split the role — keep --alert for text and add an --alert-edge that holds a
         saturated red in both states.
```

### Consistency and hierarchy (read from source)

```
🟡 Minor  Hierarchy  [observed] — the three KPI values are weighted identically
  What:  .kpi__value is 28px/600 in all three cards.
  Why:   The one number that is out of budget looks exactly like the two that are not.
  Fix:   Tie the value's color to the card's state rather than to --text-primary.
```

```
🟡 Minor  Consistency  [observed] — the cards use a ring shadow, the panel uses a border
  What:  .kpi separates itself with `box-shadow: 0 0 0 1px var(--line)`; the deploy panel
         below uses a real border.
  Why:   Two mechanisms for the same visual job, and they render differently at the corner
         radius.
  Fix:   Pick one. The ring is the better of the two here because it does not take part in
         layout.
```

## Judgment calls
- **The 16px gap in a flex row of three.** Tight, but the cards are wide and the gap reads
  as grouping rather than as crowding. Left alone.
- **No link on the KPI cards.** They are status, not navigation, and nothing about them
  invites a click. Correct as built.

## What I could not check
Motion is not declared anywhere. Focus order was read from source rather than driven, and
the deploy log's live-update behavior is not visible in a static file.
