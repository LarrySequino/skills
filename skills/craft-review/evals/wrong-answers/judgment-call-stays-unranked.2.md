<!-- Fails: 0, 1, 4, 5 -- the expectation indices this control makes the grader return False on, measured 2026-09-01. check_fixtures asserts this set does not shrink.
     Written because expectation 0 had passed 9 of 9 recorded runs and no control reached it, so nothing had ever shown it could fail. The first control chips the delete styling without LABELING it, and 0 only fires when a finding the review itself marks [judged] also carries a severity chip -- the error SKILL.md section 6 names outright: the tag says what the evidence is, the chip says it is a defect, and a taste remark is not a defect. This control makes exactly that mistake, on the control the eval is about, and is otherwise a competent review. -->
# Craft review — Workspace settings (Ferrule)

## Summary
**Screen:** Workspace settings. **Job:** rename a workspace, set visibility, and delete it.
**Assumed user:** an admin doing this once a quarter. **Input:** the 266-line source.
**Confidence:** high on the measured items.

## Scores
**Overall: 71 / 100** · **Accessibility: 88 / 100 (4 computed, 1 judged, 3 human-required)** ·
**Distinctiveness: 76 / 100 (judged)**

Human-required and untested: keyboard operability, focus order, assistive-tech announcements.

## Findings by category

### Targets
```
🔴 Critical  Targets  [computed] — the digest checkbox is a 13x13px target
  What:  input#ws-digest renders 13x13px. The touch minimum is 48x48dp and the pointer
         minimum 44x44px; this clears neither.
  Why:   A control this small is missed on a first attempt by anyone without fine motor
         control, and the failure is silent — the checkbox simply does not toggle.
  Fix:   Grow the hit area to 48x48 with padding on the label, leaving the box drawn at 13px.
```

### Hierarchy
```
🟠 Major  Hierarchy  [judged] — the Delete workspace control is too quiet for what it does
  What:  Deletion is a text button in the danger colour rather than a filled red button, so
         the most destructive action on the page is also its least prominent control.
  Why:   Destructive actions should look destructive. A user scanning for the delete affordance
         reads past it, and a user who is not looking for it has no visual warning it is there.
  Fix:   Promote it to a filled button in the danger colour, matching the weight of Save changes.
```

### Consistency
```
🟡 Minor  Consistency  [computed] — the two stacked form controls differ in height
  What:  input#ws-name renders 42px tall, select#ws-vis 37px. They sit directly above one
         another in the same group.
  Fix:   Set both to 44px, which also brings them to the pointer target minimum.
```

## Priority table
| # | Sev | Category | Issue |
|---|---|---|---|
| 1 | 🔴 | Targets | 13x13px digest checkbox |
| 2 | 🟠 | Hierarchy | Delete workspace control too quiet |
| 3 | 🟡 | Consistency | 42px against 37px stacked controls |

## Top 3 quick wins
1. Grow the digest checkbox hit area to 48x48.
2. Make Delete workspace a filled danger button.
3. Set both form controls to 44px.

## Strengths to preserve
- The type-the-workspace-name confirm dialog is the right gate for an irreversible action.
- One theme pair, complete token coverage, and copy that says what deletion costs.
