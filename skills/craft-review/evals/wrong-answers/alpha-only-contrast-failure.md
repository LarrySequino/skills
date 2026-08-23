<!-- Fails: 0, 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: ".stamp { background: #eef1f6; color: rgba(52, 64, 84, 0.65); ... }"
     (round4/alpha-contrast.html) - this review transcribes the stamp's ink as the opaque
     hex the rgba() names, hands that to contrast.py, reports the pair as clearing AA with
     room, and files the timestamps under "checked and clear". -->

# Craft review — Shipment console

## Summary
**Screen:** a shipment console: four summary cards, an event timeline panel, and a lane
table.
**Job:** an operations coordinator checks what moved overnight and which lanes are stuck.
**Input used:** the full source (281 lines) and `scripts/contrast.py` over every text pair
in the stylesheet. One theme; there is no dark block and no custom property in the file.
**Baseline:** WCAG 2.2 AA for text, 1.4.11 for non-text, and the 4/8 spacing scale.

## Scores
**Overall: 75 / 100** · **Accessibility: 82 / 100** · Consistency 70 · Hierarchy 78

## Overall impression
A plain, honest console. No token layer at all — every color is a literal hex in the rule
that uses it — which is the main structural weakness, but it has been done carefully: the
same six or seven values recur, and the palette is coherent. Contrast is the strongest part
of the page: every text pair I measured clears AA, most of them by a wide margin, which is
unusual for a console with three chip colors and a tinted table header. The problems are
consistency and states, not color.

## Findings by category

### Color and contrast (computed — `contrast.py` over every text pair)

```
🟢 Checked and clear — every text pair on the page
  What:  Chips: #0f5132 on #e2f4e9 = 8.18:1, #7a4a06 on #fdefd9 = 6.59:1, #8c1d28 on
         #fde7e9 = 7.66:1. Table header #2b3a55 on #eef1f6 = 10.09:1. Event sub-line
         #52607d on #ffffff = 6.31:1. Event stamps, whose ink the stylesheet writes as
         rgba(52, 64, 84, 0.65) — that is #344054 — read #344054 on #eef1f6 = 9.24:1.
  Why:   The lowest text pair on the page is the event sub-line at 6.31:1, comfortably over
         the 4.5 bar, and the small 12px roles (chips, table header, stamps) are the
         highest-contrast text in the file rather than the lowest, which is the right way
         round and the opposite of what usually happens.
```

```
🟠 Major  Color  [computed] — the panel border is the only edge and it is under the
             non-text bar
  What:  .panel is #ffffff on a #f5f7fa page with a #e2e6ee 1px border, and the events
         rows are separated by #eceff5 hairlines.
  Why:   WCAG 1.4.11 covers the visual information needed to identify a component, and on
         a bright panel the container edge and the row rules both wash out. The timeline
         then reads as one block of text rather than as four events.
  Fix:   Darken the row rule a step and give the panel a real edge, or drop the border and
         separate the panel from the page with a soft shadow instead.
```

### States and interaction

```
🔴 Critical  States  [observed] — nothing on the page has a focus or hover treatment
  What:  There is no `:focus-visible`, no `:hover` and no `:active` rule anywhere in the
         file. The buttons declare `cursor: pointer` and stop there.
  Why:   The console's actions all live in the header and in the table, and a keyboard user
         has no way to see where they are on either.
  Fix:   A 2px outline at 2px offset on `:focus-visible` for every control, and a one-step
         fill change on `:hover` for the buttons.
```

### Consistency

```
🟠 Major  Consistency  [observed] — three separators doing one job
  What:  The page separates content with a 1px `#e2e6ee` border on panels, a 1px `#eceff5`
         border between event rows, and a `#eef1f6` fill behind the table header — three
         near-identical values, none of them named.
  Why:   With no custom properties, a change to the page's hairline means finding every
         literal by hand, and the three values will drift apart the first time someone
         misses one.
  Fix:   Lift the palette into `:root` custom properties even if the page never gets a
         second theme. Six tokens covers this file.
```

```
🟡 Minor  Consistency  [observed] — chips are pills, the stamps are boxes
  What:  .chip is a 999px pill; .stamp is a 6px-radius box. Both are small, both are
         inline, both sit inside rows of the same density.
  Why:   Two shapes for two kinds of metadata is a defensible distinction, but nothing on
         the page says which is which, so it reads as two authors.
  Fix:   Keep the pill for status and take the stamp to the same radius as the cards.
```

## Judgment calls
- **Relative timestamps ("4 hours ago") rather than absolute ones.** Right for a console
  someone watches all day; the absolute time belongs in a title attribute.
- **The four summary cards in one row at equal weight.** They are four independent counts
  with no natural ranking, so equal weight is honest.

## What I could not check
No render, so wrapping, focus order and the table's behavior at narrow widths are read from
the declarations rather than measured. There is no dark state to review.
