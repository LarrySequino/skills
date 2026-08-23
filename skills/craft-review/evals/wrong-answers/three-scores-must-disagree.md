<!-- Fails: 0, 1, 2, 4, 5, 6 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: SKILL.md §6 "Report three scores so no single number hides a weakness — Overall /100, Accessibility /100, Distinctiveness /100 ... below 70/100 reads as generated — rework", and "A judged item gets no chip and deducts nothing." This answer collapses the three into one blended number, deducts craft points for genericness, gives the Group E tropes Critical and Major chips, and manufactures a contrast failure on the kicker so the low score has a measured finding to rest on. Intended to fail expectations 0, 1, 2, 4 and 5; it passes 3, since naming the tropes is the part a competent reviewer gets right. -->
# Design review — Cadence marketing page

## Summary

Careful, well-tokenized page with a warm palette and consistent rhythm. The problem is
that it is not really Cadence's page — it is the page every AI tool shipped this year.
Marking it down accordingly.

**Overall: 68 / 100**

Intentionality 6 · Distinctiveness 4 · Hierarchy 7 · Restraint 6 · Coherence 8

## Findings

```
🔴 Critical  Distinctiveness — this is the 2026 template, end to end
  What:  Cream ground (#f7f3ea), italic serif display hero, an uppercase eyebrow
         chip over the hero, a tracked kicker over all three sections, a 56px
         icon tile above every feature heading, three cards identical in size,
         padding and shadow, and a Get started / Learn more pair repeated twice.
  Why:   Every one of these is in design-tropes.md. A reader could guess the
         palette from the category alone, which is the category-reflex test
         failing at first order.
  Fix:   Start from a physical scene — a room where a meeting just ended — and
         let it pick the ground, the display face and the accent. Cut the
         eyebrow, cut the kickers, cut the tiles, and vary the card weights so
         the most important one is not the same rectangle as the other two.
  Deduct: −8
```

```
🟠 Major  Contrast — the section kickers are too light
  What:  .kicker is --muted #5b564b at 13px on the cream ground.
  Why:   13px uppercase at 0.12em tracking is the smallest text on the page and
         it is set in the muted role, which is intended for body-size secondary
         text rather than for micro-labels.
  Fix:   Take the kickers to --ink, or raise the size to 14px.
  Deduct: −4
```

```
🟠 Major  Hierarchy — two buttons of near-equal weight
  What:  Get started (filled) and Learn more (outlined) sit side by side at the
         same size, twice.
  Why:   Two calls to action of near-equal weight means the primary action has
         not been decided.
  Fix:   Keep Get started filled and make Learn more a text link.
  Deduct: −4
```

```
🟡 Minor  Typography — one weight doing all the work
  What:  Body, cards and nav are all the same UI sans at 400/600.
  Fix:   Add a third step, or set the card headings in the display face.
  Deduct: −2
```

## Accessibility

No issues found beyond the kicker contrast above. Focus styles are present, reduced
motion is honored, the nav has a label, and the icons are hidden from assistive tech.

## Priority

| # | Finding | Severity |
|---|---|---|
| 1 | Template distinctiveness | Critical |
| 2 | Kicker contrast | Major |
| 3 | Two equal buttons | Major |
| 4 | Single type weight | Minor |

68 is a fail. I would not ship this until the distinctiveness work is done.
