<!-- Fails: 3, 4, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 3, 4 and 5, which the first control passes. The phrase half is done right here: all four announcing openers are gone, they are reported as one habit with one fix, and the memo leads with the recommendation, so 0, 1 and 2 pass. What goes wrong is everything around it. The business jargon survives because it reads like how the team talks, and the compression that produced a three-sentence memo took the call volume, the legal check and the person who made it out with the padding. A memo can be correct on every phrase in the catalog and still be worse than the draft. -->

# Should we cache the pricing lookup?

Leverage the Redis cluster we already run, with a 15-minute TTL. The lookup runs on every
checkout render against a table that changes twice a week, so it belongs in a cache.

The merchandising job writes the price table at 03:00 and the rest is by hand, so a stale
price lasts fifteen minutes at the outside.

Dan wants to circle back on the eviction policy next week, and Priya wants to double down on
the read-through pattern the catalog already uses.

## What changed

- Four openers announced something before delivering it: "There are several ways to",
  "Broadly speaking", "In general" and "There are a few things to consider". One habit, one
  fix: lead with the answer. The recommendation was last and is now first.
