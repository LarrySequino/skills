<!-- Fails: 1, 6 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
Okay. Search. We killed the Elasticsearch cluster and moved product search into Postgres, and after three weeks I have opinions about it.

Here is the shape of the thing. Twelve nodes, forty million documents that barely change from week to week, and about $4,000 a month for the privilege. That was the cheap part. The expensive part was that nobody left on the team could tell you how any of it worked — analyzers, tokenizers, and that mapping file with the "do not remove" comment Marguerite left behind in her last week. We had a search system and zero search engineers.

I have done this badly before. Solr, 2014, a different company, and I went in blaming the engine when the problem was our own titles. Lesson learned. So this time I read the query logs first: two words, three words, mostly. Nobody here is doing fuzzy phrase matching across a legal corpus.

So: Postgres — the same database we already back up, already know how to restore at four in the morning.

Is it worse? Yeah, a bit. Lucene is genuinely better at this than a GIN index over a tsvector column is, and I am not going to pretend otherwise. But better at what, exactly.

The migration was boring, which is the compliment it sounds like. Four phases. Build the GIN index on a replica (nine hours, nobody noticed). Dual-write for a week. Compare the top 20 results for the 1,000 most common queries, eyeball the diffs, tune the ts_rank weights twice. Cut over on a Wednesday morning, because Wednesday mornings are quiet.

Latency got worse. p95 went from 180 ms to 240 ms, about a third slower — and I would take that trade again, because the requirement is 500 ms and because the p95 that actually matters is the one on the day the cluster is having a bad day. Now there is no cluster to have one.

What we got back: $4,000 a month, twelve fewer nodes to patch, one fewer dashboard to pretend to read (I once had 37 of them open at the same time), and a search implementation every engineer here can read, because it is just SQL.

Still outstanding — synonyms are a static dictionary and will not survive a new category. No multilingual support yet. And somebody should write the runbook for a GIN index rebuild before the bloat shows up — a named somebody, not the team in general.

If you are sitting on a search cluster nobody understands, you already know what I am going to tell you.
