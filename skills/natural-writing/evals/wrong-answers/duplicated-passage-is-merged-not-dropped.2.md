<!-- Fails: 1, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 1 and 3, which the first control passes. It finds the duplication and names both ends of it, so 0 passes, and it keeps every measurement, so 2 passes. Then it fixes the wrong thing: both copies of the claim stay where they were, and the section it actually cuts is the mentor pairing, on the grounds that mentors are not what the post is about. That takes the six-week pairing, the rule for choosing a mentor and the two-of-four figure with it, none of which is said anywhere else. Every figure it drops is spelled out in words, which --compare does not count, so the fidelity check passes and only the check written against that section catches it. Reporting a duplication and then deleting a different section is the failure that looks most like a careful edit. -->

Found a repeat and tightened the piece.

# What we changed about onboarding

New hires used to spend their first week reading. We replaced the reading week with a
shipping task: every new engineer merges something to production on their first day.

## The first day

We pick a small real bug out of the backlog the week before, pair the new hire with whoever
filed it, and the change goes out the same morning. Nobody spends day one reading the wiki;
they spend it merging.

## Laptops

Machines are imaged before the start date. The image carries the toolchain, the VPN profile
and a checked-out monorepo, so nothing on the first morning waits on IT.

## Why it works

Day one is not for reading the wiki. It is for merging. Time to first merge fell from 11 days
to under one, and voluntary attrition in the first ninety days went from four in twelve to
one in fourteen.

## What changed

- The first day section and the Why it works section say the same thing twice, in different
  words. Worth watching in the next draft.
- Cut the mentor pairing. It is a staffing detail and the post is about the first day.
