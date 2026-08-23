# Order export backlog, 11 February

Team,

The export backlog cleared at 04:20 this morning. It ran 61,000 rows behind at the peak,
the largest gap since the March cutover, and it drained in about ninety minutes once we
raised the worker count from 4 to 12.

The backlog is associated with the nightly vacuum job, which takes an ACCESS EXCLUSIVE lock
on order_export for the length of its run. Rina Okonkwo pulled the timings from the last six
nights and they line up to the minute.

The risk is real. A second backlog during the quarter-end run would push invoices past the
14-day window our contracts commit to, and finance has no manual path for that.

One thing to carry forward. The worker count is still at 12 and the autoscaler will not pull
it back down on its own, so someone has to set it to 4 before Friday or we pay for eight idle
workers over the weekend.

- Ola
