<!-- Fails: 0, 2, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 2 and 4. This is the cut instead of the merge. The closing section repeats a claim the first-day section already made, so it goes, and the report says so in one line without naming where the other copy is. The post now says the thing once, so expectation 1 passes, and the mentor section is untouched, so 3 passes. What leaves with the duplicate is the only measurement in the piece: time to first merge, and the attrition figures that are the whole case for the change. Nothing in the report says a number was dropped. -->

Tightened. The closing section was saying what the first-day section had already said, so it
is gone and the post ends on the mentor pairing.

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

## The mentor pairing

Every new hire gets a mentor for six weeks, and the mentor is the person who filed the day
one bug rather than whoever has capacity. Two of our four mentors this quarter had been at
the company under a year themselves.
