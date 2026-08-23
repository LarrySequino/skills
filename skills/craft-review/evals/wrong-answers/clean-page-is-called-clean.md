<!-- Fails: 1, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Craft review — On-call handoff

## Summary

A clean-looking note that is closer to a plain text dump than to a designed page. The
token set is tidy and the dark mode override is done properly, but the page has no
visual hierarchy to speak of, the one piece of metadata is buried, and nothing about it
says "this is the page you trust at 3am". Six findings below, two of them worth fixing
before this ships anywhere.

**Overall: 62 / 100** · Hierarchy 55 · Typography 68 · Color 70 · Accessibility 72

## Findings

```
🔴 Critical  Accessibility — the metadata line is set too small and too light
  What:  .meta is 14px in --muted (#5f5f5a), the smallest and faintest text on
         the page, and it carries the only freshness signal there is.
  Why:   14px is below the 16px floor for secondary text, and a muted gray on a
         near-white ground is the first thing to disappear on a laptop screen at
         low brightness or on a phone outdoors.
  Fix:   Take .meta to 16px and use --fg rather than --muted.
```

```
🟠 Major  Hierarchy — the heading barely outranks the body
  What:  h1 is 24px against 16px body, a ratio of 1.5.
  Why:   A 1.5 step reads as emphasis, not as a title. Editorial pages want a
         clearer break between the top of the page and the first paragraph, and
         at this size the h1 competes with the paragraph beneath it.
  Fix:   32px, with line-height 1.2 and 24px of space beneath it.
```

```
🟠 Major  Visual design — the page is undesigned
  What:  No card, no shadow, no accent color, no icon, no rule above the title.
         Three text elements on a flat ground.
  Why:   Even an internal document earns a little structure. As it stands there is
         nothing to anchor the eye, and nothing that identifies the page as part
         of a product rather than a raw HTML fragment.
  Fix:   Put the content in a surface card (background --card, radius 8px, the
         house shadow) and add a small accent rule or status dot above the h1 so
         "nothing open" reads as a state rather than as a sentence.
```

```
🟡 Minor  Spacing — the frame is asymmetric
  What:  body padding is 48px 24px, so the vertical frame is twice the horizontal
         one.
  Why:   The optical frame around a short note should feel even. 48/24 makes the
         column look pinched between wide margins of empty space above and below.
  Fix:   32px on all four sides.
```

```
🟡 Minor  Color — the rule is invisible
  What:  --rule is #dcdcd6 on a #f7f7f5 ground.
  Why:   A separator that light does not separate anything; the .meta line reads
         as a floating fragment rather than as a footer.
  Fix:   Darken to around #c2c2ba so the division is visible.
```

```
🔵 Polish  Typography — system-ui with no fallback stack
  What:  font: 16px/1.55 system-ui.
  Fix:   system-ui, -apple-system, "Segoe UI", Roboto, sans-serif.
```

## Content

The copy is the strongest part of the page — short, specific, and it answers the one
question the reader has. Two gaps: "Updated this morning" is relative where an absolute
time with a zone belongs, and the runbook links are described rather than provided.

## If you change one thing

Give the page a card and a real heading size. Right now it reads as an unstyled draft,
and the content deserves better than that.
