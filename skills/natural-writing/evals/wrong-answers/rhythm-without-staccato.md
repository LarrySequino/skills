<!-- Fails: 1 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "There is no run of three consecutive sentences under eight words" — this rewrite does remove the numbered march and the uniform sentence length, and keeps all five steps, but it pays for the variety with stacked fragments: five straight sentences under eight words in the middle of the piece, three more at the close. Manufactured emphasis in place of rhythm, which is the exact trade the eval exists to catch. -->

Migrations fail in the gaps between the steps, not inside them, which is why the order below is not up for negotiation.

Read the schema first. Every column, every constraint, every index nobody remembers adding. Write down what looks wrong. That list is the whole job. Skip it and the rest is theater.

Then the plan. One line per problem. No problem without an answer. Nothing vague survives this stage.

Staging comes next. Run the real migration against real volume, and if the approach cannot survive a rehearsal on a quiet afternoon it will not survive a Tuesday with production traffic sitting on top of it.

Then watch it. Row counts, query times, the nightly job that used to finish in a minute. Fix what moves.

Then write it up. What you did. What surprised you. What you would skip next time. The person who reads that document is you in eight months, remembering none of this, and what you leave behind is the only version of today that will still exist.
