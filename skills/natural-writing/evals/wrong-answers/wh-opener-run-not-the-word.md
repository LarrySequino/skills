<!-- Fails: 0, 1, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 1 and 4. This is the flat rule applied to a graded one. Every sentence that opened on a question word is rewritten, including the isolated one two paragraphs down that the entry says is fine, and the report describes the fix as a rule about a class of word rather than as one finding about one run of five. Nothing is named as left alone. The run is gone and so is the Look, opener, and no fact moves, so 2, 3 and 5 pass -- which is the point: an over-correction passes every mechanical check and still costs the piece a sentence it should have kept. -->

# Read replica cutover, 3 March

We moved reads to the new replica at 02:10 and moved them back at 03:40.

The connection pool made this hard. The drain finished with nine warm connections still open
against the old primary, because the drain script closes idle connections and nothing else.
We found them by counting sockets on the box. It is still open which of the two batch jobs
was holding them.

None of this was subtle. The runbook says to drain the pool, and the drain script does not do
what the runbook says it does.

The lag fell under a second and we cut back. Peak lag was 4 seconds against the 30 we had
budgeted, so the replica itself was never the problem.

Marisol is writing a drain script that closes established connections too. It lands before
the 17 March window.

## What changed

- Rewrote every sentence that opened on a question word. Those openings read as filler.
- Cut the "Look," opener.
