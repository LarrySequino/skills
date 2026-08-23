<!-- Fails: 0, 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: the token the prompt declares for .note inside the dark media query and
     nowhere else. This review runs preflight.py, sees the theme-token warning, dismisses it
     as a false positive without ever saying the token is declared in one state only, and
     files the missing page ground as optional polish instead of a publish blocker.
     The token's name is kept out of this comment on purpose: check_fixtures.py feeds the
     whole control file to the grader as the answer, so a literal quotation here would
     satisfy the very check the control has to fail. -->

# Craft review — Deploy checklist artifact

## Summary
**Screen:** a short artifact page: one h2, one instruction line, one attribution note.
**Job:** a reader follows two steps and sees who last verified them.
**Input used:** the inline source, plus `scripts/preflight.py` against it. Both theme states
read from the declarations rather than from a render.
**Baseline:** the house artifact rules — theme-aware tokens, a page that paints its own
ground, and a 13px floor for secondary text.

## Scores
**Overall: 71 / 100** · Color 74 · Typography 62 · Hierarchy 66 · Content 88

## Overall impression
This is a small, honest page that does not try to be more than it is, and the theme handling
is better than most artifacts get: a real `prefers-color-scheme` block rather than a filter
invert, and a token pair that flips together. Two things hold it back, both structural
rather than visual, and neither is likely to be noticed by the person who wrote it because
they are both invisible in whichever theme that person happens to use.

## Findings

```
🟡 Minor  Color — preflight's theme-token warning is a false positive here
  What:  preflight.py returns a warning about the token that colors `.note`. The token is
         read by exactly one rule, and that rule is the small attribution line at the foot
         of the page.
  Why:   In the light state `.note` simply takes the ink it inherits from `body`, which is
         #111 — darker than the tone the warning is worried about, not lighter. The
         attribution line is legible in both states, which is what the rule is protecting.
         Worth knowing about, not worth a change.
  Fix:   None needed. If you want the warning to stop firing, give `.note` an explicit tone
         in the base block and let the theme block override it.
```

```
🟡 Minor  Color — the body sets no background of its own
  What:  `body` declares `color` and `font` but never `background`, so the page paints
         whatever the surrounding document paints.
  Why:   Inside the artifact host this is harmless in practice — the host ground and the
         page's own light palette are the same white, and the dark host and the dark token
         set agree too. It only matters if the page is ever embedded somewhere with a tinted
         ground, which is not the stated use.
  Fix:   Optional, and a one-liner when you want it: `background: var(--paper)` on `body`.
```

```
🟠 Major  Typography — .note at 13px is under the floor for a page this small
  What:  `.note` is 13px against a 16px body, on a page whose entire content is four lines.
  Why:   The size step is doing work that no other signal on the page is doing, so the
         attribution reads as an afterthought rather than as provenance. On a page with
         three text elements there is no density pressure to justify shrinking one of them.
  Fix:   14px, and lean on tone rather than size for the demotion.
```

```
🟠 Major  Hierarchy — the page opens at h2 with no h1 above it
  What:  The document's first heading is `<h2>Deploy checklist</h2>`.
  Why:   For a standalone page the outline starts at level two, which reads as a fragment
         to a screen reader moving by heading and to anything that builds a table of
         contents from the document.
  Fix:   Promote it to `h1` and keep the size where it is.
```

```
🟡 Minor  Spacing — 32px of padding on every side, and no measure cap
  What:  `body { padding: 32px }` with no `max-width`.
  Why:   On a wide window the two sentences run the full width of the viewport, which is
         the one thing that makes a short page feel unfinished.
  Fix:   `max-width: 62ch; margin-inline: auto`.
```

## Judgment calls
- **No in-page theme toggle.** Correct for an artifact: the OS setting is the only input,
  so a `[data-theme]` layer would be dead weight.
- **System font stack.** Fine. A page this short gains nothing from a webfont and would pay
  a flash of unstyled text for it.

## What I could not check
No rendered screenshot in either state, so nothing here is measured off pixels. Focus styles
are not declared and there is nothing focusable on the page to check them against.
