# Lock timeout alert on the orders database

This page walks through what the alert means, why it fires, and what to do about
it. We will take each of those in turn.

## What it means

A transaction held a row lock on `orders` for longer than 90 seconds and something
else queued up behind it. The alert fires on the waiter, not on the holder, so the
transaction named in the page is usually the victim.

## Why it fires

Three causes, in the order you should check them:

1. The nightly reconciliation job. It opens one transaction, walks the previous day
   in 5,000-row batches, and holds the lock through every batch.
2. A deploy that ran a migration without `lock_timeout` set. The migration waits
   forever and everything behind it waits with it.
3. Somebody's `psql` session, open since the afternoon, with an uncommitted
   `UPDATE` sitting in it.

That last one is the counterintuitive one, and it is the one that gets people.

The kicker? The reconciliation job has started at 02:00 every night since 2021 and
nobody has moved it.

## What to do

Find the oldest transaction, not the loudest:

    SELECT pid, now() - xact_start AS age, query
    FROM pg_stat_activity
    WHERE state <> 'idle' ORDER BY xact_start;

If you have not used `psql` before, run `\x` first. The query column is 400
characters wide and unreadable without it.

Kill the oldest one with `SELECT pg_terminate_backend(pid)`. Wait fifteen seconds.
If the queue has not drained, kill the next oldest. Two of those usually does it.

To recap: the alert means a transaction held a row lock past 90 seconds, the usual
cause is the reconciliation job, and the fix is to kill the oldest transaction
rather than to restart the database. Restarting the database drops the webhook
queue on the floor, which is a second outage on top of the first one, and that is
the reason this page exists.
