<!-- Fails: 0, 2, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 0, 2 and 4, and keeps 1, 3 and 5 on purpose. This is what "make it work for people who have never carried a pager" produces when the brief is taken at face value: the preview stays and grows, every section gets a line saying what it is about, the recap stays because a recap is the friendly thing to do, and a closing takeaway is added on top. Not one fact is lost and not one number is changed, so --compare is clean. The page is 149 words longer and says nothing the original did not say. -->

Here it is, opened up for a first-time on-call audience. I kept the structure and added
orientation at the top of each section.

# Lock timeout alert on the orders database

Before you start: this page walks through what the alert means, why it fires, and what to do
about it. We will take each of those in turn. If you are new to the rotation, read it end to
end once now, while nothing is on fire.

## What it means

This section explains the alert itself. A transaction held a row lock on `orders` for longer
than 90 seconds and something else queued up behind it. The alert fires on the waiter, not on
the holder, so the transaction named in the page is usually the victim. In other words, the
transaction the page names is often not the one causing the problem.

## Why it fires

This section covers the three causes, in the order you should check them:

1. The nightly reconciliation job. It opens one transaction, walks the previous day in
   5,000-row batches, and holds the lock through every batch.
2. A deploy that ran a migration without `lock_timeout` set. The migration waits forever and
   everything behind it waits with it.
3. Somebody's `psql` session, open since the afternoon, with an uncommitted `UPDATE` sitting
   in it.

That last one is the counterintuitive one, and it is the one that gets people. It is worth
remembering that a human being with a terminal open is as capable of blocking the database as
any scheduled job.

The kicker? The reconciliation job has started at 02:00 every night since 2021 and nobody has
moved it. That is a long time for a known cause to stay in place.

## What to do

This section is the runbook proper. Find the oldest transaction, not the loudest:

    SELECT pid, now() - xact_start AS age, query
    FROM pg_stat_activity
    WHERE state <> 'idle' ORDER BY xact_start;

If you have not used `psql` before, run `\x` first. The query column is 400 characters wide
and unreadable without it. `\x` turns on expanded display, which prints one column per line
instead of one row per line.

Kill the oldest one with `SELECT pg_terminate_backend(pid)`. Wait fifteen seconds. If the
queue has not drained, kill the next oldest. Two of those usually does it.

To recap: the alert means a transaction held a row lock past 90 seconds, the usual cause is
the reconciliation job, and the fix is to kill the oldest transaction rather than to restart
the database. Restarting the database drops the webhook queue on the floor, which is a second
outage on top of the first one, and that is the reason this page exists.

The takeaway, if you remember nothing else: find the oldest transaction, kill it, and never
reach for a restart.
