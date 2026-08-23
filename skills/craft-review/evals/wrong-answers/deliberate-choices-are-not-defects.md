<!-- Fails: 1, 2 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: house-sheet notes 2 and 4 in round7/considered-choices.html — "It carries no
     text and never marks the boundary of a control, so it sits outside WCAG 1.4.11" and
     "It is measure-driven, not grid-driven". This review finds the real pull-quote failure
     and then chips both documented decisions as defects: the sand hairline as an
     accessibility failure with a prescribed darker value, and the rail width as off the
     grid with a prescribed on-grid replacement. -->

# Craft review — Field notes, "the Tuesday queue drain"

## Summary
**Screen:** a long-form editorial page with a related-notes rail.
**Job:** read a field write-up end to end and pick up one related note afterward.
**Input used:** the full source (389 lines), `scripts/contrast.py` over the resolved pairs
in both theme states, and a hand audit of every width and inset against the 8pt grid.
**Baseline:** WCAG 2.2 AA for text and 1.4.11 for non-text, and an 8pt grid for widths and
spacing.

## Scores
**Overall: 68 / 100** · **Accessibility: 61 / 100** · Consistency 66 · Typography 88

## Overall impression
The type is the best thing here: a serif body at 17px/1.6 on a warm paper ground, a real
measure, and a scale whose steps are chosen rather than generated. The page also documents
its own decisions at the top of the stylesheet, which is more than most files do. Three
things still need to move, and the first of them is a straight AA failure on the one block
of text the page most wants you to read.

## Findings by category

### Color and contrast (computed — `contrast.py`, both states)

```
🔴 Critical  Color  [computed] — the pull quote fails AA in both states
  What:  .pullquote sets `color: var(--ink-faint)`, which resolves to #777d85 on the paper
         ground in light and #5a6068 on #0a0b0c in dark. Measured, that is 3.08:1 and
         3.10:1. The quote is set at 21px, which is under the large-text threshold once
         the serif's weight is taken into account, so the bar it has to clear is 4.5:1.
  Why:   1.4.3, and it is the block the layout is built around — pulled out of the column,
         given its own ground and its own hanging mark, and then set in the page's faintest
         ink.
  Fix:   Set the quote in #5c6270 on #e2decd = 4.53:1 in light, and lift the dark value by
         the same step. The quote stays quieter than the body and clears the bar.
```

```
🟠 Major  Color  [computed] — the sand hairline is far under the 1.4.11 non-text bar
  What:  --sand draws the 2px masthead underline and the 2px section rule. In light it
         measures #d8c3a5 on #e2decd = 1.27:1; in dark #8a7a5f on #0a0b0c is brighter but
         still thin against the ground it sits on.
  Why:   WCAG 1.4.11 puts a 3:1 floor under the visual information a reader needs, and
         these two rules are the page's only structural separators — the masthead from the
         article, and one section from the next. At 1.27:1 on a warm paper ground they
         disappear on a glare-washed panel, and with them goes the page's only signal that
         a new section has started.
  Fix:   Draw both rules in --hairline (#bdb69f) instead, which is the token the page
         already has for exactly this job and which lands over the non-text floor. Keep
         --sand for the chip and the plot ground, where it is a fill rather than a rule.
```

### Layout and grid (audited by hand)

```
🟠 Major  Consistency  [observed] — the rail width is off the 8px grid
  What:  .rail is `width: 268px`. Every other width, inset and gap on the page is a
         multiple of 8: the 1024px shell, the 48px column gap, the 32px shell padding, the
         56px top inset.
  Why:   268 is not a multiple of 8, so the rail's inner edge lands half a step out of
         phase with everything to its left. On a page whose whole visual argument is
         rhythm, one width that is 4px off the grid is the thing that makes the two
         columns feel unrelated rather than paired.
  Fix:   264px or 272px. Either one is on the grid, and at this measure the 4px move leaves
         the related notes breaking exactly where they break today.
```

```
🟡 Minor  Typography  [observed] — five sizes with uneven steps
  What:  13 / 15 / 17 / 21 / 30, which steps at roughly 1.15, 1.13, 1.24 and 1.43.
  Why:   The steps are uneven, but the stylesheet's own notes say this is deliberate — a
         tight bottom for dense small roles and an open top for the display size — and the
         page bears that out: every small role sits on the same 13px step, so the
         irregularity never shows up as two sizes competing.
  Fix:   None. Documented decision, and the page is consistent with it.
```

## Judgment calls
- **The hanging opening mark on the pull quote.** The block is pulled into the article's
  padding on both sides and its own padding puts the quote's text edge back on the body
  column, so the mark hangs outside the text on purpose. Optical alignment, correctly done.
- **Serif body on a warm ground.** Unusual for a web page and completely coherent here.

## What I could not check
No render, so the hanging mark's optical position is read from the declarations rather than
measured off pixels. Print styles are not declared.
