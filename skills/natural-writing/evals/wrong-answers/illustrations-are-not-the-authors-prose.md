<!-- Fails: 2, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: expectations 2, 3 and 4, and passes 0 and 1 on purpose, because the answer this eval exists to catch is a thorough one rather than a lazy one. It finds both of the author's real tells and then reports the piece's own examples beside them: three chatbot artifacts at P0 that are the subject of the paragraph they sit in, the Tier 1 vocabulary off the catalog line, and the two demonstrations the author introduces with "Watch for". Every one of those is something the scanner prints or something a careful reader notices; none of them is the author's writing. This is what running the tool and reporting its output looks like. -->

I ran the scanner first and then read it twice. There is more here than your editor thinks,
and some of it is bad.

## P0, credibility killers

1. **Chatbot residue: "Great question!"** Line 30. This is near-proof of pasted model output
   and a single instance can sink a piece. Cut it.
2. **Leaked citation token: `citeturn0search0`** Line 30. A search-tool artifact that
   should never survive into a draft. Remove it.
3. **AI-tool URL parameter: `utm_source=chatgpt.com`** Line 31. Strip the parameter from the
   link before this goes anywhere near an editor.

Three P0 findings in one paragraph is the reason the piece reads as machine-written. Fix
these before anything else.

## P1, obvious AI smell

4. **Tier 1 vocabulary cluster.** Line 4 runs delve, tapestry, leverage, seamless and
   testament to in a single sentence. Five Tier 1 words together is the densest signal in
   the document. Line 15 uses delve again.
5. **Meta-commentary opener.** Line 9: "It is worth noting that the list is also where the
   false positives live." Cut the opener and start on "The list".
6. **Self-posed rhetorical question.** Line 19: "The result? Devastating." A question the
   text asks itself and answers in one word.
7. **False concession.** Line 20: "while the tooling is impressive, real challenges remain."
   The concession gives away nothing and the second half is filler.
8. **Second false concession.** Line 25: "While the detectors have improved, the underlying
   problem remains." The same construction again, four lines later.
9. **Self-posed question, again.** Line 38: "So has any of this actually got better in a
   year? Not really."

## P2, stylistic polish

10. **Dramatic fragmentation.** Line 17: "Not the words. The shape." Two fragments stacked
    for manufactured emphasis.
11. **Adverbs.** "really" and "actually" are doing no work in the closing paragraph.

## Assessment

Eleven findings, three of them P0. The vocabulary and the artifacts are clear problems. The
fragments on line 17 are a judgment call and may be deliberate.
