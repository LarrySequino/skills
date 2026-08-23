<!-- Fails: 0, 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: the prompt's ".card{...padding:<t> <r> <b> <l>...}", whose fourth value is
     smaller than the other three. This review feels the imbalance, describes it as a lean,
     and prescribes "a touch more room" without ever reading the two numbers off the
     shorthand or stating the delta. The numbers are kept out of this comment on purpose:
     check_fixtures.py feeds the whole control file to the grader as the answer, so quoting
     the declaration here would satisfy the check the control has to fail. -->

# Craft review — Weekly summary card

## Summary
**Screen:** one summary card on a white page: a title and a single sentence of body copy.
**Job:** give someone glancing at a dashboard the week in one line.
**Input used:** the inline source as pasted, read as declarations. No render.
**Baseline:** the ordinary card conventions — an even inset, a title that outweighs the
body, and a border that separates without competing.

## Scores
**Overall: 69 / 100** · Balance 60 · Typography 74 · Color 72 · Content 86

## Overall impression
The card is doing the right things at the coarse level: a sensible fixed width, a soft
corner, a title/body pair with a real weight step, and copy that says something. What is
wrong is finer than that, and it is what the question is about. The card does not sit
square. The block of text inside it leans toward the left wall, so the white space around
the content is not the same on both sides, and the eye reads that as the card being
slightly tipped rather than as the text being placed.

## Findings

```
🟠 Major  Balance — the content block leans left inside the card
  What:  The card's padding shorthand does not carry the same value on every side: the
         left inset is set shorter than the ones around it, so the title and the paragraph
         both start closer to the left border than they finish from the right one.
  Why:   A card is a frame, and a frame is read by its margins. When three sides agree and
         one does not, nothing looks broken — it looks tilted, which is worse, because the
         reader keeps checking the card instead of reading it. This is the single reason
         the card feels off.
  Fix:   Give the left side the same breathing room the top, right and bottom already have
         so the inset is even the whole way round, and let the shorthand collapse to a
         single value once it is.
```

```
🟡 Minor  Color — the border is too light to hold the card against the page
  What:  .card sits on a white body with a #ddd hairline and a white fill, so the only
         thing separating card from page is that hairline.
  Why:   On a bright display the border thins out to almost nothing and the card stops
         reading as a surface. There is no shadow and no fill difference to fall back on.
  Fix:   Either darken the hairline a step, or tint the page ground so the white card has
         something to sit on. Do not do both.
```

```
🟡 Minor  Typography — the title is only 2 points above the body
  What:  .card h3 is 17px against a 15px body, with weight left at the browser default
         bold for h3.
  Why:   The weight is carrying the whole hierarchy; the size step is small enough to read
         as an accident rather than as a level.
  Fix:   Take the title to 15px and hold it at 600, or leave the size alone and set the
         body a step down. One clear step beats two vague ones.
```

```
🟡 Minor  Spacing — the gap under the title is tight for the leading
  What:  .card h3 carries an 8px bottom margin under a 15px/1.5 body.
  Why:   The title's descenders land close to the first line of copy, which makes the pair
         read as one block rather than as a label over a value.
  Fix:   Take the gap to 12px.
```

## Judgment calls
- **The 320px fixed width.** Deliberate-looking for a dashboard tile, and the sentence
  breaks over two lines at that width without a widow. Left alone.
- **The 8px corner radius against a 1px hairline.** Consistent with the border weight; a
  softer corner would need a heavier border to keep the arc clean.

## What I could not check
Nothing here was measured off a render — there is no screenshot and no headless pass in
this review, so the balance finding is read off the shape of the declaration and off how
the card reads, not off a measured inset on both sides.
