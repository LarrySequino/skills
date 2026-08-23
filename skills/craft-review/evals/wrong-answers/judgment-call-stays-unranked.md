<!-- Fails: 1, 4, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Craft review — Workspace settings (Ferrule)

## Summary

A calm, well-built settings screen: one theme pair, complete token coverage, a 720px
column, and copy that tells the truth about what deletion costs. One thing on it is a
real problem, and it is the most consequential control on the page.

**Overall: 76 / 100** · Interaction 58 · Hierarchy 80 · Typography 82 · Color 84

## Findings

```
🔴 Critical  Interaction — the delete workspace control is styled as a text link
  What:  .btn--text has background: none, border: 0, padding: 0 and an underline,
         in --danger. It sits alone in the danger card and it is the entry point
         to removing 214 projects and 1,840 files.
  Why:   Destructive actions have to look destructive. A borderless underlined
         string reads as a link to more information, not as the trigger for an
         irreversible action, and it gives the eye no stopping point on a page
         where every other action is a filled button. With padding: 0 the control
         is also only 15px tall — under the 24px minimum target size in WCAG
         2.5.8, and well under the 44px most touch guidance asks for.
  Fix:   Use the .btn--danger treatment that already exists in the sheet: filled
         --danger, --danger-fg text, 8px 20px padding, 4px radius. The style is
         written and applied only inside the dialog; bring it out to the card.
```

```
🟠 Major  Hierarchy — the danger card is indistinguishable from the general card
  What:  .card.danger takes the same --surface fill, the same 8px radius, the same
         24px padding and no border. Only the heading text marks it.
  Why:   Two cards of identical weight, one of which is a destructive zone. On a
         quick scan the section reads as a third settings group.
  Fix:   1px --danger border at 25% alpha and a tinted fill, or a rule and a
         "Danger zone" label above it. The card should announce itself before the
         copy has to.
```

```
🟡 Minor  Feedback — Save changes has no state
  What:  A single primary button, no disabled state until something changes, no
         pending state, no confirmation after.
  Why:   Settings screens that save silently make people press twice.
  Fix:   Disable until the form is dirty, show a spinner in the button while the
         request is in flight, and a brief inline "Saved" beside it after.
```

```
🟡 Minor  Layout — the checkbox row breaks the field rhythm
  What:  .field carries 20px of bottom margin; .check carries 4px, so the digest
         option sits tight against the row of buttons beneath it.
  Fix:   20px on .check as well, or 24px before .row.
```

```
🔵 Polish  Typography — the label size and the help size are the same
  What:  .field label and .field .help are both 13px, separated only by weight.
  Fix:   Keep labels at 13px/600 and take the help text to 12px, or leave the
         sizes and drop the help color one step further back.
```

## What is working

Every token is declared in both themes, the field border holds up against the fill in
light and dark, the confirm dialog asks for the workspace name rather than a bare yes, and
the danger copy states the exact cost in numbers instead of "this cannot be undone". The
audit-log footnote is a nice closing note.

## If you change one thing

Make the delete control a red button. It is the one place where this screen's restraint
works against the person using it.
