<!-- Fails: 0, 1, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 1 and 4. This is the deslop without the checklist. Both planted defects are fixed correctly -- the vacuum job is named as taking the lock instead of being something the backlog is associated with, and the bare assertion of realness is gone with the quarter-end consequence left standing -- so 2, 3 and 5 all pass. What is missing is the Evaluator pass. No check is cited by any id, lettered or otherwise, which is what an answer without references/preflight.md can do: it can apply the rules SKILL.md states and it cannot name a check by a number that exists in the checklist and nowhere else. And with no checklist to run, the closing paragraph reads as a throwaway and goes, taking the only instruction in the message with it. -->

Deslopped. Cut the padding, named the mechanism, tightened the middle.

# Order export backlog, 11 February

Team,

The export backlog cleared at 04:20 this morning, 61,000 rows behind at the peak and the
largest gap since the March cutover. It drained in about ninety minutes once we raised the
worker count from 4 to 12.

The nightly vacuum job takes an ACCESS EXCLUSIVE lock on order_export for the length of its
run, and the export queues behind it. Rina Okonkwo pulled the timings from the last six
nights and they line up to the minute.

A second backlog during the quarter-end run would push invoices past the 14-day window our
contracts commit to, and finance has no manual path for that.

- Ola
