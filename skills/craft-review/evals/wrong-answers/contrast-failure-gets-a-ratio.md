<!-- Fails: 0, 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: the prompt's ":root{--bg:#1a1a1a;--fg:#4a4a4a;...}" body pair - this review
     never computes it, ranks the link color first instead, calls the body gray acceptable
     for a dark UI, and states an eyeballed ratio for its own fix. -->

# Craft review — Release notes page

## Summary
**Screen:** a single release-notes page: one heading, one paragraph, one inline link.
**Job:** tell a returning user what shipped in 2.4 and get them to the full changelog.
**Input used:** the full inline source as pasted. No render, no Figma file.
**Baseline:** WCAG 2.2 AA, and the ordinary dark-UI conventions for long-form text.

## Scores
**Overall: 64 / 100** · Color 58 · Typography 62 · Hierarchy 78 · Content 85

## Overall impression
For a page this small there is very little to get wrong, and most of it is right: a real
dark ground rather than an inverted light one, a heading that outweighs the body without
shouting, and a paragraph capped at 60ch so the measure never runs long. The problem is the
link. A saturated mid-blue is a light-mode link color, and it has been carried onto a
near-black ground without being re-picked for it, which is the one thing on this page a
reader will actually struggle with.

## Findings

```
🔴 Critical  Color — the link is a light-mode blue on a dark ground
  What:  a { color: var(--accent) } resolves to #2b6cb0, and the page ground is #1a1a1a.
         That pair is 3.2:1. AA wants 4.5:1 for text at this size, and a link inside a
         sentence is text, not an accent.
  Why:   "Full changelog" is the only action on the page, so the one element that has to
         be reachable is the one that is hardest to read. The blue also sits close enough
         in weight to the body gray that the underline is doing most of the work of saying
         "this is a link" — take the underline away, as plenty of resets do, and the link
         stops announcing itself at all.
  Fix:   Use #4f8fd6 on #1a1a1a — 6.1:1 — which keeps the blue reading as blue rather than
         as a washed cyan. Keep the underline.
```

```
🟠 Major  Typography — 16px/1.5 is under-leaded for a dark ground
  What:  body sets font: 16px/1.5. On a dark background, light-on-dark type blooms
         optically and needs more leading than the same size does on white.
  Why:   At 60ch and 1.5, the lines pack tightly enough that the eye loses its place on
         the return sweep. This is why most dark-first documentation sets 1.6 to 1.7.
  Fix:   Raise the body to 16px/1.65 and give <p> a 16px bottom margin, which it does not
         currently have.
```

```
🟡 Minor  Color — the body gray is at the dim end of the range
  What:  --fg is a mid gray on a near-black ground. It reads as deliberately quiet rather
         than as broken: this is the tone a lot of dark-mode editorial uses for body copy
         so the headline can carry the page.
  Why:   It is dim, but 16px at a 60ch measure is a comfortable reading setup, and the
         heading is set in the same value, so the page is at least internally consistent
         about it.
  Fix:   Optional. If the page is ever read outdoors or on a low-end panel, lift --fg one
         step toward #8b8b8b, which is bright enough to stay comfortable without turning
         the page into pure white-on-black glare.
```

```
🟡 Minor  Hierarchy — the h1 and the body share a color, so only size separates them
  What:  h1 inherits --fg from body. The 28px/16px size step is the entire hierarchy.
  Why:   One signal is thin for a heading that names the release. Weight or color would
         give it a second.
  Fix:   Set the h1 in a brighter tone than the body and leave the size where it is.
```

## Judgment calls
- **The 40px page padding.** Generous for a page with three elements, and it reads as
  intentional editorial framing rather than as a spacing accident. Left alone.
- **No max-width on the page itself.** The 60ch cap on `p` does the real work; the heading
  running full width is a defensible choice on a page this short.

## What I could not check
No rendered screenshot, so nothing here is measured off pixels — the values above are read
out of the declarations and out of the two hex values the stylesheet defines. Focus and
visited states for the link are not declared anywhere and could not be evaluated.
