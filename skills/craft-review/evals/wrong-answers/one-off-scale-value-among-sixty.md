<!-- Fails: 0 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: the one declaration in .composer that is off the 4/8 scale (round3/off-scale-once.html,
     section 7). This review runs preflight.py, reads only its contrast section, does the
     spacing audit by eye against the page's own 4/8/12/16/24 dialect, declares every value
     on the dialect, and reports the saved-views rail's asymmetric inset instead. The two
     values are kept out of this comment on purpose: check_fixtures.py feeds the whole
     control file to the grader as the answer, so quoting them here would satisfy the check
     the control has to fail. -->

# Craft review — Triage, Beacon Support

## Summary
**Screen:** a support triage screen — saved-views rail, unassigned ticket queue, ticket
detail panel with a reply composer.
**Job:** a support agent scans unassigned tickets, claims one, and replies from the panel.
**Input used:** the full source (467 lines) and `scripts/preflight.py` against the file, read
for its contrast section. Spacing audited by hand against the page's own dialect.
**Baseline:** the stylesheet's own spacing dialect — 4 / 8 / 12 / 16 / 24 — which is a
narrower set than the generic 4/8pt scale and is used consistently enough to be the
reference.

## Scores
**Overall: 74 / 100** · **Accessibility: 70 / 100** · Consistency 84 · Hierarchy 80 ·
Distinctiveness 79 `(judged)`

## Overall impression
A disciplined screen with a real token architecture — primitives, then roles, then
components that only ever read roles — and an unusual fern-and-jade identity in a category
that defaults to blue. Spacing is the strongest part of it: the same handful of values
appear everywhere, so the three columns feel like one system rather than three panels that
happened to land next to each other. The weak parts are the interaction layer, which was
mostly not written, and one rail inset that breaks the page's own left edge.

## Findings by category

### Spacing and grid (audited by hand against the page's dialect)

```
🟠 Major  Spacing  [observed] — the saved-views rail is inset unevenly
  What:  .rail { padding: 16px 8px } sets a vertical inset twice its horizontal one, and
         then .rail h2 adds a 12px left margin of its own to push the section label back in
         while the links below it are pushed in by their own padding instead.
  Why:   Two different mechanisms produce the rail's left edge, so the label and the links
         are aligned by coincidence rather than by construction. Any change to either value
         breaks the alignment silently. It is also the one place on the page where a
         container's own padding is not the thing that sets its content edge.
  Fix:   Give .rail a single 12px inset on all four sides, drop the h2's left margin, and
         let the links carry only their vertical padding.
```

```
🟢 Checked and clear — every other spacing value on the page
  What:  Masthead 12px / 24px, queue bar 12px, ticket cards 16px, the detail panel's
         header and footer 16px and 24px, the thread bubbles 12px, the composer's inset and
         its 12px bottom margin, the footer 16px / 24px, and the narrow-window overrides at
         24px and 32px.
  Why:   All of them land on the page's own 4 / 8 / 12 / 16 / 24 dialect. Sixty-odd
         declarations and one dialect is a better record than most production stylesheets
         manage, and it is the main reason the screen reads as considered.
```

### Accessibility and interaction (read from source)

```
🔴 Critical  Targets  [observed] — every button on the screen is under the touch minimum
  What:  .btn--small is 4px of vertical padding on 13px text, which resolves to roughly
         28px of height. Every Claim, Snooze, Sort and Send reply button uses it, and the
         820px breakpoint says a tablet is in scope.
  Why:   The pointer-agnostic minimum is 44px, and 24px is the floor even for a
         mouse-first dense tool. A queue whose primary verb is "Claim" cannot have Claim as
         its smallest target.
  Fix:   Take .btn--small to 8px vertical padding and give the queue's Claim button the
         full .btn size. That is a 32px and a 40px control, both on the dialect.
```

```
🔴 Critical  States  [observed] — no hover, no focus, no active anywhere
  What:  The stylesheet declares `cursor: pointer` on .btn and nothing else. There is no
         :hover, no :focus-visible and no :active rule in the file, and no styling for the
         rail's current view.
  Why:   A keyboard user cannot see where they are, and a mouse user gets no confirmation
         that a control is a control until they click it.
  Fix:   A 2px --accent outline at 2px offset on :focus-visible, a one-step surface change
         on :hover, and an aria-current treatment for the rail.
```

### Color and contrast (computed — `preflight.py`)

```
🟠 Major  Color  [computed] — the composer hint slips under AA in dark mode
  What:  .composer p takes --text-muted on --surface-sunken. In dark that resolves to
         #7e8b85 on #1c2622 = 4.39:1, against 4.5:1 for body text. The same role clears
         everywhere else it is used: 5.29:1 on the light sunken surface, 4.84:1 on raised.
  Why:   It is the line telling the agent whose name the customer will see on the reply,
         and dark is the default on a lot of support desks.
  Fix:   In dark mode give the hint --text-secondary, #d3cfc8 on #1c2622, which is well
         clear of the bar. One line.
```

## Judgment calls
- **The 208px rail.** Not on the 8 grid as a width, but it is sized to the longest saved
  view name at 13px and that is a legitimate way to size a rail. Left alone.
- **13px as the single small size.** Used for the ticket meta, the tags, the thread bodies
  and the footer. One small step for every small role is a decision, not drift.

## What I could not check
No headless render in this pass, so wrapping, focus order and the narrow-window layout are
read from the declarations rather than measured. Motion is not declared anywhere and there
is nothing to review.
