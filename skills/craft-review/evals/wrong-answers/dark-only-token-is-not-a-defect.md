<!-- Fails: 0, 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "/* dark-only: a card needs lifting off a dark ground, and its top edge needs
     a warmed hairline that light mode has no use for. */" (round4/legit-theme-token.html) -
     this review overrides preflight's clean result, ranks the two dark-only tokens as the
     page's blocking defect, and prescribes moving them into the base :root. -->

# Craft review — Weekly digest, Meridian

## Summary
**Screen:** an email-style weekly digest: masthead, three story cards, a side note, a
footer.
**Job:** a subscriber skims the week and clicks through to one or two items.
**Input used:** the full source (264 lines) and `scripts/preflight.py` against the file,
plus a hand audit of the token table across both theme states.
**Baseline:** WCAG 2.2 AA, the 8pt spacing scale, and the house rule that a token set has
to be complete in the default state before a theme layer overrides any of it.

## Scores
**Overall: 72 / 100** · **Accessibility: 88 / 100** · Consistency 62 · Typography 84

## Overall impression
The typography and the rhythm here are good — a 720px measure, a 48/32/20 vertical scale
that holds all the way down the page, and a genuine light-first palette with a dark
override rather than a filter. The token table is where it comes apart, and it comes apart
in a way that is invisible to whoever built it, because it only shows in the state they
were not looking at. `preflight.py` returns "clean: no showstoppers" on this file, which is
the script's rule being more forgiving than the house rule: it checks whether a token
resolves where it is read, not whether the set is whole.

## Findings by category

### Tokens and theming

```
🔴 Critical  Consistency  [computed] — `--lift-shadow` and `--hairline-warm` exist only inside the dark media block
             and are absent from the base `:root`
  What:  The base `:root` carries ten tokens. The `@media (prefers-color-scheme: dark)`
         block re-declares all ten and adds two more that exist nowhere else in the
         stylesheet: a lifted card shadow and a warmed hairline for the card's top edge.
  Why:   A token table is a contract, and this one is only whole in one of its two states.
         Two custom properties that fail to resolve in the default light state means the
         theme layer is no longer an override layer — it is a second, larger token set
         wearing the first one's names, and the next person to read `var(--lift-shadow)`
         in a rule has no way to know from the base table that it exists at all.
  Fix:   Declare both in the base `:root` — `--lift-shadow: none` and `--hairline-warm:
         var(--border)` — and let the dark block override them like every other token. Two
         lines, and the table is whole in both states.
```

```
🟠 Major  Consistency  [observed] — the dark block carries component rules, not just tokens
  What:  Inside the same media query, after the `:root` overrides, sit `.card { box-shadow;
         border-top-color }` and `.aside { box-shadow }`.
  Why:   Everywhere else on this page a component reads a token and the theme re-points the
         token. These two rules break that: the component's appearance is now defined in
         two places, one of which only exists in one state.
  Fix:   Give `.card` and `.aside` an unconditional `box-shadow: var(--lift-shadow)` and
         `border-top-color: var(--hairline-warm)` in the main block, and let the token
         values do the theming. This falls out of the fix above for free.
```

### Spacing and rhythm

```
🟢 Checked and clear — the vertical scale
  What:  48 / 32 / 24 / 20 / 16 down the page, and the narrow override drops the shell to
         32/16 without leaving the scale.
  Why:   Every value is on the 8pt scale and the steps are used consistently by role.
```

### Color and contrast

```
🟢 Checked and clear — every text pair in both states
  What:  preflight.py measured the resolved pairs in light and dark and returned nothing.
         Body, muted text, the chip and the accent link all clear AA with room.
```

## Judgment calls
- **No `[data-theme]` layer.** Correct: there is no in-page toggle, so the OS setting is
  the only input and a third layer would be dead weight.
- **`--rule` and `--border` as separate tokens.** They are close in value but they do
  different jobs — one is a hairline between rows, one is a container edge. Keep both.

## What I could not check
No rendered screenshot in either state, so the shadow's actual weight on the dark ground is
not measured here. Motion is not declared anywhere on the page.
