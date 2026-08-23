<!-- Fails: 1, 2, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Craft review — Shelf list, "The catalog that outlived three systems"

## Summary
**Screen:** an editorial long-form page with a related-reading rail (`unstated-choices.html`).
**Job:** read a nine-minute archive write-up and get to related material.
**Input used:** full source, plus `scripts/preflight.py` and `scripts/contrast.py` against the file.
**Baseline:** an 8pt spacing grid and a 1.2–1.25 modular type scale, the defaults for editorial web.

## Scores
**Overall: 61 / 100** · **Accessibility: 54 / 100** (9 computed, 2 judged, 3 human-required) ·
**Distinctiveness: 58 / 100** `(judged)`

## Overall impression
The page reads as a competent draft that never had a system pass. Four separate things are off the
grid or off the scale, and one of them is an accessibility failure. There is no design-notes block
or token documentation anywhere in the file, so none of this can be assumed intentional.

## Findings by category

🔴 Critical  Color & contrast  [computed] — the sand rules fall far under the 3:1 non-text minimum
  What:  `--sand` is `#d8c3a5` and draws the masthead underline and the `.rule` divider. Against
         `--paper` `#e2decd` that measures **1.27:1**.
  Why:   WCAG 2.2 1.4.11 sets 3:1 for graphical objects. These two rules are the only thing
         separating the masthead from the headline and the two halves of the article, so they are
         structural, not ornamental. At 1.27:1 they vanish on any screen with glare.
  Fix:   darken `--sand` to `#8a7250`, which reaches 3.38:1 on `--paper`, or drop the rules and
         carry the separation with space.

🔴 Critical  Color & contrast  [computed] — the pull quote fails AA in both themes
  What:  `.pullquote` sets `color: var(--ink-faint)`. Light resolves to `#777d85` on `#e2decd` =
         **3.08:1**; dark resolves to `#5a6068` on `#0a0b0c` = **3.10:1**. At 21px regular the bar
         is 4.5:1, not 3:1.
  Why:   The pulled sentence is the one line a scanner is meant to catch, and it is set in the
         faintest ink on the page.
  Fix:   `--ink-faint: #5c626a` light, which reaches **4.56:1** on `#e2decd`.

🟠 Major  Alignment  [computed] — the opening quote mark is 24px outside the content column
  What:  `.pullquote::before` is absolutely positioned at `left: 0` on a block whose own padding is
         24px, so the glyph lands 24px to the left of every other left edge in the article. The
         block itself is pulled out of the column by `margin: 32px -24px`.
  Why:   Every other element on the page starts on one vertical line. One glyph breaking it reads
         as a stray absolute position, not as emphasis.
  Fix:   `left: 24px` on `::before` and `margin: 32px 0` on `.pullquote`, so the mark and the block
         both sit on the column.

🟡 Minor  Spacing & grid  [computed] — the rail width is off the 8pt grid
  What:  `.rail` is `width: 268px`. 268 is not a multiple of 8; the nearest grid values are 264 and
         272.
  Why:   One off-grid width in an otherwise clean sheet is the classic hand-tuned leftover.
  Fix:   `width: 272px`.

🟡 Minor  Typography  [computed] — the type scale is not a modular scale
  What:  The five sizes are 13 / 15 / 17 / 21 / 30. The steps measure 1.15, 1.13, 1.24 and 1.43 —
         no consistent ratio, and the bottom two steps break the spacing scale's own logic by
         sitting 2px apart.
  Why:   13px and 15px are close enough that a reader cannot tell the caption from the label, which
         is the whole job of a scale.
  Fix:   rebuild on 1.25 from a 16px base: 13 / 16 / 20 / 25 / 31.

## Priority table

| # | Severity | Category | Finding |
|---|---|---|---|
| 1 | 🔴 | Color & contrast | Sand rules at 1.27:1, under the 3:1 non-text minimum |
| 2 | 🔴 | Color & contrast | Pull quote at 3.08:1 / 3.10:1, under the 4.5:1 body bar |
| 3 | 🟠 | Alignment | Quote mark 24px outside the content column |
| 4 | 🟡 | Spacing & grid | 268px rail off the 8pt grid |
| 5 | 🟡 | Typography | 13/15/17/21/30 is not a modular scale |

## Top 3 quick wins
1. Darken `--sand`.
2. Darken `--ink-faint`.
3. Put the quote mark and the quote block back on the column.

## Strengths to preserve
The prose is specific and the figure caption states a finding rather than restating the axes.
