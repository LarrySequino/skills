<!-- Fails: 0, 1, 2, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-09-01. check_fixtures asserts this set does not shrink.
     Written because this eval has no recorded run of any kind: its only evidence of being able to fail was one control covering 1, 2 and 4, leaving 0 and 3 with nothing. It makes the mistake the eval's own expected_output predicts -- leads with the gradient, never reports the missing page ground -- and fabricates a contrast failure on a page where every pair clears, which is what 3 is for. -->
# Craft review — Analytics overview

## Summary
**Screen:** Analytics overview. **Job:** scan yesterday's numbers and open one for detail.
**Assumed user:** an operator checking in once a morning. **Input:** the 316-line source.
**Confidence:** high on the measured items.

## Scores
**Overall: 64 / 100** · **Accessibility: 71 / 100 (3 computed, 0 judged, 3 human-required)** ·
**Distinctiveness: 58 / 100 (judged)**

Human-required and untested: keyboard operability, focus order, assistive-tech announcements.

## Findings by category

### Color & contrast
```
🔴 Critical  Contrast  [computed] — the muted metric labels fail AA
  What:  The secondary labels under each KPI measure roughly 4.1:1 against the card fill,
         under the 4.5:1 AA needs for body text at that size.
  Why:   These labels carry the unit and the comparison window, so a reader who cannot
         resolve them cannot tell what the number means.
  Fix:   Darken the label token one step until it clears 4.5:1 on the card.
```

### Distinctiveness
```
🟠 Major  Distinctiveness  [observed] — a purple-to-blue gradient hero and gradient-clipped titles
  What:  The hero runs a purple-to-blue linear-gradient, and two section titles are painted
         with the same gradient through background-clip with color: transparent.
  Why:   Gradient-clipped headings are the most recognisable generated-interface tell there
         is, and using the treatment twice makes it the page's signature rather than an accent.
  Fix:   Set the titles in the foreground token and keep the gradient to the hero, or drop it.
```

### Consistency
```
🟡 Minor  Consistency  [observed] — card and panel radii disagree
  What:  Cards round at 8px, the side panel at 12px, and the two sit side by side.
  Fix:   Pick one and apply it to both.
```

## Priority table
| # | Sev | Category | Issue |
|---|---|---|---|
| 1 | 🔴 | Contrast | Muted metric labels near 4.1:1 |
| 2 | 🟠 | Distinctiveness | Gradient hero and gradient-clipped titles |
| 3 | 🟡 | Consistency | 8px against 12px radii |

## Top 3 quick wins
1. Darken the metric label token until it clears AA.
2. Set the section titles in the foreground token.
3. Unify the radii at 8px.

## Strengths to preserve
- Every spacing value on the page is on the 4/8 scale.
- The KPI row reads in one pass, and the numbers are tabular.
