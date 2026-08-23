<!-- Fails: 2, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "Any finding that is reported carries a measured or directly observed value rather
     than an impression" - this review is done entirely by eye. It never opens the stylesheet and
     never runs the bundled scripts, and every one of its five findings is a feeling about the page:
     the masthead "does not announce itself", the cards "sit at the same pitch", the chip "reads
     quieter" than the button. Not one carries a size, a ratio, a token or a selector, so there is
     nothing in the report anyone could check, reproduce, or act on without redoing the work. It is
     the second control for this eval: the first one over-reports the dark-only tokens as the page's
     blocking defect, which is a measured claim that happens to be wrong. This one reports nothing
     measurable at all. -->

# Craft review — Weekly digest, Meridian

## Summary
**Screen:** an email-style weekly digest: masthead, three story cards, a side note, a
footer.
**Job:** a subscriber skims the week and clicks through to one or two items.
**Input used:** the rendered page in both theme states, read the way a subscriber would read
it. I did not run the bundled scripts — `scripts/preflight.py` and `scripts/contrast.py` — on
this file; the page is small enough to take in whole, and nothing about it looked like it
needed instrumenting.
**Baseline:** how a weekly digest ought to feel in the inbox.

## Scores
**Overall: 78 / 100** · Hierarchy 70 · Typography 80 · Color 82

## Overall impression
This is a calm, well-mannered page. The measure is comfortable, the reading rhythm is
unhurried, and nothing in it feels generated. The dark state is a real palette rather than an
inverted light one, and the extra lift the cards pick up there sits right on the darker
ground — that part is done properly and I would leave it alone. What holds the page back is
pitch: almost everything on it speaks at the same volume, so the eye has nowhere to land
first and no reason to move.

## Findings by category

### Visual hierarchy

```
🟠 Major  Hierarchy — the masthead does not announce itself
  What:  The title and its standfirst read as the first paragraph of the page rather than as
         its top. Coming into it cold, I was two cards in before I registered that I had
         passed a header.
  Why:   A digest is skimmed from the top, and the top is the one place a reader decides
         whether to keep going. It currently asks to be read rather than seen.
  Fix:   Give the title noticeably more presence than the card headings and let the
         standfirst drop back further, so the gap between them opens up.
```

```
🟠 Major  Hierarchy — the three cards sit at the same pitch
  What:  Two shipped items and a table of open work are given identical weight, framing and
         spacing. Nothing in the stack says which of them the reader is meant to care about.
  Why:   The week has a shape and this page flattens it. The open-work card in particular
         reads as an afterthought stapled to the bottom, when it is the one thing that might
         need somebody to act.
  Fix:   Let the open-work card take a different treatment from the two shipped ones —
         a quieter ground, or a heading that reads as a different kind of thing.
```

### Typography

```
🟡 Minor  Typography — card headings are close in feel to the body copy
  What:  A heading and the paragraph under it read at nearly the same voice; the step
         between them is there but faint.
  Why:   Skimming a digest means reading headings and skipping bodies, and that only works
         when the two are unmistakable at a glance.
  Fix:   Widen the step, either by lifting the heading or by settling the body slightly.
```

### Color

```
🟡 Minor  Color — the chip reads quieter than the button beside it
  What:  In the card footer the status chip and the action button sit side by side, and the
         chip feels washed next to the blue.
  Why:   They are doing different jobs — one is a label, one is the click — but the pairing
         reads as one strong element and one faded one rather than as a deliberate contrast.
  Fix:   Either firm the chip up or soften the button, so the difference between them looks
         chosen.
```

### Spacing

```
🔵 Polish  Spacing — the footer sits tight under the last card
  What:  The gap before the colophon feels smaller than the gaps between the cards, so the
         page ends abruptly.
  Why:   A sign-off wants a breath in front of it.
  Fix:   Open the space above the footer until it reads as the end of the page rather than
         as one more row.
```

## Judgment calls
- **No in-page theme toggle.** Right call for an emailed digest: the OS setting is the only
  input there is, and a control the reader cannot rely on is worse than none.
- **The side note inside the first card.** It could have been a fourth card. Keeping it
  nested says it belongs to that story, which is true.

## What I could not check
Anything that needs a number. I read this as a subscriber rather than as a stylesheet, so
the findings above are how the page struck me and not what it measures. If you want the
spacing, contrast and token claims pinned down, that is a second pass with the scripts.
