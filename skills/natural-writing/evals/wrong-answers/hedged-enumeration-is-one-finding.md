<!-- Fails: 0, 1, 2 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 1 and 2. This is the pass that has the vocabulary tables and not the phrase catalog. The two openers that look like filler go, the two that look like ordinary connective tissue stay, and each cut is reported on its own line as a separate small edit, so nothing in the report says these were one habit with one fix. The memo still opens by setting up context instead of by answering the question, which is what the entry's fix rule is for. Every figure survives and the business jargon is swapped correctly, so 3, 4 and 5 pass. -->

# Should we cache the pricing lookup?

Broadly speaking, the pricing lookup runs on every checkout render, which is about 9,000
calls an hour at peak. In general, a query that runs that often against a table that changes
that rarely belongs in a cache rather than in the database plan.

The price table is written by the merchandising job at 03:00 and by hand maybe twice a week,
so a 15-minute TTL would serve a stale price for at most fifteen minutes after a hand edit.
Kofi checked with legal in January and fifteen minutes is inside what the pricing terms
allow.

Use the Redis cluster we already run, with a 15-minute TTL. Dan wants to revisit the eviction
policy next week, and Priya wants to commit harder to the read-through pattern the catalog
already uses.

## What changed

- Cut the opening sentence. It announced that options existed without naming one.
- Cut "There are a few things to consider", which announced a list and then delivered one.
- Swapped "leverage" for use, "circle back" for revisit and "double down" for commit.
