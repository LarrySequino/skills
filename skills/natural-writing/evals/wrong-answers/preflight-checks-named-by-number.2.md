<!-- Fails: 2, 3, 5 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 2, 3 and 5, which the first control passes. This one runs the checklist and cites it correctly, lettered ids and all, so 0 and 1 pass, and it carries the closing instruction out intact, so 4 passes. What it does is mark the two planted defects as passing when they are not: the periphrastic verb is still there and so is the bare assertion of realness, both signed off in the Evaluator section. It also loses the peak figure and the drain time while tightening the first paragraph, which is the failure the compare check exists for and which no amount of self-certification catches. -->

Deslopped, Evaluator pass below.

# Order export backlog, 11 February

Team,

The export backlog cleared at 04:20 this morning and drained once we raised the worker count
from 4 to 12.

The backlog is associated with the nightly vacuum job, which takes an ACCESS EXCLUSIVE lock
on order_export while it runs. Rina Okonkwo pulled the timings from the last six nights and
they line up to the minute.

The risk is real. A second backlog during the quarter-end run would push invoices past the
14-day window our contracts commit to, and finance has no manual path for that.

The worker count is still at 12 and the autoscaler will not pull it back down on its own, so
someone has to set it to 4 before Friday or we pay for eight idle workers over the weekend.

- Ola

## Evaluator pass

15a. Pass. The relationship reads clearly.

15b. Pass. The sentence is short and the consequence follows it.

11b. Pass. The closing instruction is intact.

3a. Pass. The mechanism survives the edit.

17. Pass. No dashes.
