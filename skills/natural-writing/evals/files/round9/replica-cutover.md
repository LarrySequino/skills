# Read replica cutover, 3 March

We moved reads to the new replica at 02:10 and moved them back at 03:40.

What made this hard was the connection pool. When the drain finished, nine warm connections
were still open against the old primary. Why those nine survived is that the drain script
closes idle connections and nothing else. How we found them was by counting sockets on the
box. Which of the two batch jobs was holding them is still open.

Look, none of this was subtle. The runbook says to drain the pool, and the drain script does
not do what the runbook says it does.

When the lag fell under a second, we cut back. Peak lag was 4 seconds against the 30 we had
budgeted, so the replica itself was never the problem.

Marisol is writing a drain script that closes established connections too. It lands before
the 17 March window.
