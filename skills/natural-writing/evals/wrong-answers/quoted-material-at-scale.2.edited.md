# Cadence evaluation: their claims against our numbers

We ran the Cadence agent on the checkout cluster for eleven days in February. This note collects their claims, the sales engineer's written answer, and our own measurements. The quotations run long on purpose. The gap between the two is the finding.

Their docs open the ingestion page like this:

> Modern engineering teams operate in an ever-evolving landscape where telemetry is not just a stream of events but a rich tapestry of signals woven across every layer of the stack. Cadence lets you delve into that tapestry without the operational burden of self-hosting. Our ingestion pipeline leverages a robust, multifaceted architecture — one that is designed to scale seamlessly from a single service to a global fleet — so your team can focus on what matters. It is worth noting that customers routinely report a dramatic reduction in mean time to resolution within the first quarter.

Nothing in that paragraph is checkable. Its one number, "the first quarter", hangs off a claim about other teams' mean time to resolution that nobody at Cadence will quantify on request.

The claim we cared about was ingestion overhead. Their pricing assumes you send everything, so the agent has to be cheap enough that sending everything is not itself the problem.

We measured 4.2 percent of CPU on a p95 checkout pod at 900 requests per second. Their sizing guide quotes 1 percent. The exemplar sampler accounts for nearly all of the difference, and we could not turn it off from the agent config. On a quiet pod the number falls to 0.8 percent, so the guide was measured on the wrong pod.

The blog post their sales team sent us makes a broader claim:

> The old model asked you to choose: sample aggressively and lose the outlier, or keep everything and pay for it. Cadence collapses that tradeoff. By leveraging adaptive tail sampling at the edge, we deliver not just lower cost but higher fidelity — a genuinely transformative shift in how teams think about observability. It's worth noting that this is not incremental. Teams who embrace the new paradigm consistently unlock insights that were previously invisible to them.

It is worth noting that adaptive tail sampling is a real technique and their implementation of it is good. Our own traces came back with the slow requests intact at a 2 percent keep rate, which is the thing that usually breaks. I want to separate the engineering from the writing around it, because the engineering held up under a load test that I expected to embarrass it.

Their February changelog is written in the same register, which matters only because the changelog is the document engineers actually read:

> 2.14 unlocks a more holistic view of your service dependencies. We have reimagined the topology graph from the ground up, empowering teams to navigate complex architectures with newfound clarity and to surface the crucial signals that were previously buried in noise. This release also delivers a seamless upgrade path, so teams can embark on the migration with confidence and without disrupting existing dashboards. We believe topology should be not just a diagram but a living map of how your systems truly behave.

The 2.14 topology graph beats the 2.12 one. It follows database calls across the connection pool now, which is what we asked for in September.

Their sales engineer, Marcus Vance, answered our sizing question by email on February 10. Quoting it in full, with his permission:

    Thanks for the detailed numbers, and great to see you putting the agent through its paces. The 1 percent figure in our sizing guide reflects a steady-state workload and it is worth noting that checkout paths are rarely steady state. What we typically see is that teams leverage our adaptive sampling to bring that number down, and the results are not just cost savings but a meaningfully more nuanced picture of production behavior. I would encourage you to delve into the sampling configuration reference — there is a wealth of tuning available there, and most teams find the sweet spot within a week or two. Happy to jump on a call and walk through it together. One more thing worth underscoring: the exemplar sampler is a cornerstone of the fidelity story, so teams rarely want it off once they see what it catches in production.

I want to be careful about the weight this carries. Marcus got the technical half right: checkout is not steady state, and our graphs agree with him.

The sampling configuration reference does not document a way to disable the exemplar sampler. I asked Marcus twice and got the call offer both times. This may simply be a gap in the docs rather than a gap in the product, and I would rather find out before we sign anything.

Where this leaves us: the product does what it says on tracing, costs roughly four times the sizing guide's implied figure on our hottest pods, and arrives wrapped in marketing copy that made two people here distrust the numbers before we ran anything. Not a technical objection, but it cost three days of extra measurement, and it is worth saying out loud.

My recommendation is that we run a second trial on the two quiet clusters and leverage the existing Prometheus scrape for the checkout path rather than paying Cadence to ingest it. That splits the bill along the line where their agent is actually cheap. I will have numbers by March 6.
