<!-- Fails: 0, 1, 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# AI-pattern audit: trail description

Six findings, two of them worth acting on before this goes out. Flags only, as asked.

## P1

**1. "a landscape of granite and stunted pine" — sentence 1.** "Landscape" is a high-frequency
LLM abstraction, the same family as "realm", "tapestry", and "ecosystem". It generalizes what
the concrete nouns beside it already say: granite and stunted pine *are* the landscape, so the
word adds a layer of abstraction over specifics that were doing fine on their own. Cut it and
the sentence gets shorter and more physical.

**2. "Water is the crucial thing to get right" — sentence 2.** "Crucial" is a Tier 2 AI
vocabulary word, and the frame around it ("X is the crucial thing to get right") is the
essay-intro construction models reach for when they want to signal importance without earning
it. The sentence that follows already proves water matters. Suggest cutting the word and
letting the fact carry it.

## P2

**3. Rule of three: "a map, a headlamp, and more food than you think."** Three-item lists with
the third item slightly longer than the first two are one of the most reliable structural
tells in the set. The rhythm is the giveaway: short, short, long, with the payoff parked at
the end.

**4. "three liters, not two" — the X-not-Y corrective.** A signature model cadence. It appears
once here, which keeps it borderline, but paired with finding 3 in the same paragraph it forms
a small cluster.

**5. "more food than you think" — second-person address to an imagined reader.** Instructional
copy written by a model drifts into telling the reader what they think. A human trail writer
is likelier to name a quantity.

**6. "steeper than it looks on paper" — closing kicker.** The wry reversal in the final
sentence is a standard model closer: end on a small twist so the piece feels finished.

## Where that leaves it

Findings 1 and 2 are vocabulary and should go. Findings 3 through 6 are structural and would
each need a small rewrite to break the pattern. The density is roughly one tell per two
sentences, which is on the high side for a piece this short.
