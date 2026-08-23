Release retro

It's worth noting that this cycle ran long. We shipped v2.4 on March 12 — a week later than I promised in standup, and I'm not going to pretend otherwise. The delay came from a single migration script that decided, halfway through, to lock every row it touched — which is the kind of thing you only find at 2am when the pager goes off.

Once we cut over, things mostly held. Fastly caught the worst of the traffic spike before it ever reached our origin, which bought us the hour we needed to patch the connection pool — the fix itself was three lines, the diagnosis was not. By the time we finished, we'd touched something like 1,800 accounts without a single support ticket, which still surprises me more than it should.

I want to delve into why the migration locked in the first place, because I don't think we've actually fixed the root cause — we just outran it. The index rebuild ran serially instead of in batches, and nobody caught it in review, myself included. That's on me as much as anyone.

On the bright side, the new dashboard delivered a seamless experience from day one. Still, I'd rather flag the rough edges here than have someone find them in the postmortem. Next cycle I'm splitting the migration into smaller chunks — the current one is too big to reason about, let alone roll back in a hurry. If you were on call last week, thank you — I owe you a coffee, or several.
