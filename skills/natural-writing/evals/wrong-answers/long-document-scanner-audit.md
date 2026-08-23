<!-- Fails: 0, 1, 2, 4, 6 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# AI-writing audit: long-audit.md

I read the whole postmortem end to end. Short version: this is human writing with a light
dusting of corporate vocabulary, most of it in the middle third. Nothing here suggests the
document was drafted by a model. Findings in severity order.

## P1 — worth fixing

**1. "built to leverage the same long-lived sessions" (What went wrong).** "Leverage" as a
verb is the one word in this document that sounds like it came from a different document. The
surrounding prose says "runs", "takes", "holds". Swap it for "use" and the paragraph is
consistent with itself.

**2. "robust enough to catch a dead peer" (Contributing factors).** Same family. "Robust" is
near the top of every AI-overuse list, and here it's also imprecise: the sentence is about
whether the keepalive timers were short enough, which is a different property from robustness.

**3. Title Case heading: "Rollback Path And Open Questions".** Every other heading in the file
is sentence case. This one is title case and capitalizes "And", which even a title-case style
guide would lowercase. It reads like a heading written at a different time, or by a different
hand, from the rest.

## P2 — noted, weaker signals

**4. The rule of three, three times.** "The cost was in three places", three alerts each with
its own reason, and a four-item "What we are not doing" list that is really three refusals
plus a caveat. Triads are a strong AI structural habit. Each one here is followed by concrete
material, so this is a pattern to watch rather than a hit.

**5. "which is correct: that board is a daytime tool" (Why the alert did not fire).** The
self-correcting aside — make a claim, then rule on it in the same sentence — is a cadence
models fall into. Used once, it's voice; this document uses it three or four times.

**6. Aphoristic closers.** "Every other worker did exactly what we told it to do. They
waited." and "The lock is not the interesting part." are the kind of pull-quote sentence an
assistant produces when asked to make a postmortem readable. I lean toward these being
genuine, because the technical detail around them is too specific to fake.

## Checked and clear

- **Em dashes.** Two in the whole file, at lines 48 and 82, which is 1.3 per 1,000 words.
  Both sit where a comma would be weaker. Nothing to do here.
- **Hedging stacks.** None. The document commits: "This was not a Postgres problem."
- **Vocabulary elsewhere.** No "delve", no "tapestry", no "it's not just X, it's Y", no
  closing paragraph that restates the document.
- **Specificity.** Times, versions, thresholds, and owners throughout. Machine prose does not
  hold this many checkable details.

## Verdict

Three items worth an edit, all vocabulary or formatting, all in the middle of the document.
Fix the two words and the heading and there is nothing left to find.
