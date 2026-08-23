# Should we cache the pricing lookup?

There are several ways to approach this, and each one has tradeoffs.

Broadly speaking, the pricing lookup runs on every checkout render, which is about 9,000
calls an hour at peak. In general, a query that runs that often against a table that changes
that rarely belongs in a cache rather than in the database plan.

There are a few things to consider before we commit. The price table is written by the
merchandising job at 03:00 and by hand maybe twice a week, so a 15-minute TTL would serve a
stale price for at most fifteen minutes after a hand edit. Kofi checked with legal in
January and fifteen minutes is inside what the pricing terms allow.

The answer is to leverage the Redis cluster we already run, with a 15-minute TTL. Dan wants
to circle back on the eviction policy next week, and Priya wants to double down on the
read-through pattern the catalog already uses.
