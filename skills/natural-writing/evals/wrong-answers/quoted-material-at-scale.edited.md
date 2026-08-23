# Cadence evaluation: their claims against our numbers

We ran the Cadence agent on the checkout cluster for eleven days, from February 3 to February 14. This note collects what their material says, what the sales engineer told us in writing, and what we actually measured. I have quoted them at length on purpose, because the gap between the two is the whole finding and I do not want anyone to think I paraphrased them unfairly.

Their docs open the ingestion page like this:

> Engineering teams work in a changing environment where telemetry is not just infrastructure but the thing that tells you what your system is doing.

Nothing in that paragraph is checkable. The one number in it, "the first quarter", is attached to a claim about other people's mean time to resolution that nobody at Cadence will put a figure on when asked.

The claim we cared about was ingestion overhead. Their pricing assumes you send everything, so the agent has to be cheap enough that sending everything is not itself the problem.

We measured 4.2 percent of CPU on a p95 checkout pod at 900 requests per second, against the 1 percent their sizing guide quotes. The difference is almost entirely the exemplar sampler, which we could not turn off from the agent config. On a quiet pod the number falls to 0.8 percent, so the sizing guide is not wrong so much as measured on the wrong pod.

The blog post their sales team sent us makes a broader claim:

> The old model made you choose: sample hard and lose the outlier, or keep everything and pay for it.

adaptive tail sampling is a real technique and their implementation of it is good. Our own traces came back with the slow requests intact at a 2 percent keep rate, which is the thing that usually breaks. I want to separate the engineering from the writing around it, because the engineering held up under a load test that I expected to embarrass it.

Their February changelog is written in the same register, which matters only because the changelog is the document engineers actually read:

> 2.14 gives a fuller view of your service dependencies. We rebuilt the trace index so a span carries the context it needs.

The topology graph in 2.14 is genuinely better than the one in 2.12. It now follows database calls across the connection pool, which is what we asked for in September.

Their sales engineer, Marcus Vance, answered our sizing question by email on February 10. Quoting it in full, with his permission:

    Thanks for the numbers, and good to see you putting the agent through its paces. Two things stand out.

I want to be careful about how much weight this carries. Marcus answered the technical half of the question accurately: checkout is not steady state, and our own graphs agree with him.

The sampling configuration reference does not document a way to disable the exemplar sampler. I asked Marcus twice and got the call offer both times. This may simply be a gap in the docs rather than a gap in the product, and I would rather find out before we sign anything.

Where this leaves us: the product does what it says on tracing, costs about four times what the sizing guide implies on our hottest pods, and comes wrapped in marketing copy that made two people on this team distrust the numbers before we had run anything. That last part is not a technical objection, but it cost us three days of extra measurement, and it is worth saying out loud.

My recommendation is that we run a second trial on the two quiet clusters and use the existing Prometheus scrape for the checkout path rather than paying Cadence to ingest it. That splits the bill along the line where their agent is actually cheap. I will have numbers by March 6.
