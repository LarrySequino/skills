<!-- Fails: 2, 3, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 2, 3 and 5, which the first control passes. This is the report without the edit. The run is named as a run, the isolated opener is protected and the protection is stated, so 0, 1 and 4 pass and the diagnosis is right. Then the rewrite does not carry it: four of the five openers are still stacked, the Look, opener is still there, and the window date and the peak lag went out with a sentence that was tightened. A rewrite mode answer that reports correctly and edits badly scores well on every check that reads the report, which is why the ones that read the text have to be able to fail on their own. -->

# Read replica cutover, 3 March

We moved reads to the new replica at 02:10 and moved them back at 03:40.

What made this hard was the connection pool. When the drain finished, nine warm connections
were still open against the old primary. Why those nine survived is that the drain script
closes idle connections and nothing else. How we found them was by counting sockets on the
box.

Look, none of this was subtle. The runbook says to drain the pool, and the drain script does
not do what the runbook says it does.

When the lag fell under a second, we cut back. The replica itself was never the problem.

Marisol is writing a drain script that closes established connections too.

## What changed

- The second paragraph ran five sentences in a row on question words: "What made this hard",
  "When the drain finished", "Why those nine survived", "How we found them", "Which of the
  two batch jobs". The run is the tic, not the word.
- I kept "When the lag fell under a second, we cut back" because a single opener of that
  shape is ordinary English.
