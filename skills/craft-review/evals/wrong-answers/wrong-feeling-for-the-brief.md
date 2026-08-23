<!-- Fails: 1, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: SKILL.md §4 Group D "Brand & feeling — does it feel like this product and evoke the intended emotion? A technically flawless screen that feels cold is a finding", §4.12 content & microcopy, and §8 "Nitpicking without severity — rank them". This answer leads with the one thing a script printed (the 10px 14px off-scale padding), files the countdown and the streak copy as a Polish "tone" note at the bottom, offers no replacement wording, reports the lime accent as a contrast/eye-strain failure when it measures 14.4:1, and prescribes a generic "more trustworthy" direction rather than one grounded in the brief. Intended to fail expectations 1 and 3 on script evidence, and 4 on a read; 0 and 2 it survives on purpose, because naming the strings without replacing them is exactly the plausible half-answer. -->
# Design review — Proof of income (Bridge Rent Relief)

## Summary

A tidy, high-contrast form step. The token set is small and consistent, the focus ring
is real, and the upload affordances are large and obvious. Two measured issues and a
handful of smaller notes.

**Overall: 84 / 100** · Accessibility 91 · Craft 84

## Findings

```
🟠 Major  Spacing — the progress panel is off the 4/8 scale
  What:  .progress uses padding: 10px 14px. preflight.py flags both values, and
         symmetry.py measures the same two insets on the rendered page (left
         14px, top 10px), which is the only geometry finding on the screen.
  Why:   Every other spacing value on the page is on the 4/8 ramp — 8, 16, 24,
         32, 64. Two one-off values in the one panel that sits directly under the
         header break the vertical rhythm at the top of the screen, where it is
         most visible.
  Fix:   padding: 8px 16px. That keeps the panel height within 4px of where it is
         now and puts it back on the ramp.
```

```
🟠 Major  Color — the lime accent is punishing on the dark ground
  What:  --lime #ccf24a is used for the countdown, the progress fill, the level
         heading, the streak line, the cheer line and the primary button, all on
         #14140f or #1e1e16.
  Why:   Saturated yellow-green at full chroma against a near-black ground is the
         highest-glare pairing available, and it is repeated six times on one
         screen. On an older phone at low brightness this is the kind of contrast
         that produces afterimages.
  Fix:   Drop the chroma and lift the lightness — something around #d9e9a8 — and
         reserve the full-strength lime for the button alone.
```

```
🟡 Minor  Consistency — two radius scales
  What:  .card, .progress and .cta are 8px; .timer, .drop and .chips li are 12px.
  Why:   The two treatments sit within 24px of each other and nothing separates
         the groups semantically.
  Fix:   8px for surfaces, 12px for controls, and apply it consistently — or just
         use 8px everywhere.
```

```
🔵 Polish  Tone — the copy is a bit upbeat for the subject
  What:  The countdown, the "You're 60% there!" line, "Level 3", "Unlock your
         funds" and "Nice work. You're crushing it."
  Why:   It reads a little more like a fitness app than a benefits form.
  Fix:   Worth a pass from whoever owns the voice guidelines when there is time.
         Something more trustworthy and professional would land better with this
         audience.
```

## Priority

| # | Finding | Severity |
|---|---|---|
| 1 | .progress padding off-scale | Major |
| 2 | Lime accent glare | Major |
| 3 | Two radius scales | Minor |
| 4 | Copy tone | Polish |

## Quick wins

1. `padding: 8px 16px` on `.progress`.
2. One radius value across the six surfaces.
3. Soften the lime to `#d9e9a8` outside the button.
