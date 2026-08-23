# Maintenance

Procedure for when the user asks to "check skill-curator," "update the curator," or
"is the curator still right." This skill has no upstream sources to sweep, so its
maintenance is about whether its own claims and tools still hold, not about harvesting.

## What drifts, and how to catch it

This skill makes claims about how other tooling behaves, and that tooling moves under it.
Each claim below names the thing it depends on and the check that catches the drift.

| Claim in this skill | Depends on | Check |
|---|---|---|
| `disable-model-invocation: true` marks a skill explicit-only | Claude Code frontmatter | Confirm the key still exists in current Claude Code docs; rename in `SKILL.md` if it moved |
| The eval format in `harvest-log.md` | Anthropic `skill-creator`, `references/schemas.md` | Diff `evals.json` shape against the installed plugin; update the pointer and the field names if they changed |
| "roughly ten skills in a scope" as the count trigger | Skill discovery budget | Re-read whatever the current harness documents about skill listing limits; adjust the number in `SKILL.md` and in `scripts/audit.py` together |
| The 400-line bloat threshold | Nothing external; a judgment | Leave alone unless evidence arrives |
| `scripts/overlap.py` matches `tools/overlap.py` in the private repo | `publish.sh` copying the right file | `diff` the two; they must be byte-identical |

## Deterministic checks, run every time

These are the steps that are arithmetic, and they go first so the reading is spent on the
table above.

1. `python3 scripts/audit.py --demo` and `python3 scripts/overlap.py` on a known pair. Both must
   print `self-check: PASS`. A script whose self-check fails is not shipped.
2. `python3 scripts/audit.py ~/.claude/skills`, or wherever the user's library lives. Read the
   output as a user would. Anything it flags about *this* skill is fixed before anything else:
   the skill that audits the library does not get to fail its own audit.
3. Run `scripts/overlap.py` with this skill as the target against any source that has been read
   during the session. Zero is the expected result and is recorded in `ATTRIBUTION.md` as the
   control; a non-zero result means text was carried over and `ATTRIBUTION.md` must say from
   where before anything is packaged.

## Then the reading

4. Walk the drift table. For each row, do the check. Record what was checked and the date in the
   log below, including the rows where nothing had moved.
5. Re-read `references/security-screen.md` against the current shape of skill distribution. New
   install paths (a marketplace, a CLI, a plugin format) are new injection surfaces, and the
   screen should name them.
6. Re-read the five jobs in `SKILL.md` against the last three real uses of this skill. A job
   nobody has asked for in a long while is a candidate for folding into another; a request that
   fit none of the five is a candidate for a sixth, or for a sharper description.

## The grader, which the table above does not cover

`tools/evals/grade.py` decides what every number this skill publishes means, and it is the
one tool nothing checks. Run this whenever the graders change, and again before a round is
published.

Sample by pattern, not by run. A pattern that is too loose is a property of the pattern, so
three runs of one expectation read one regex three times. Take one run per (eval,
expectation, arm), picked as the lowest-numbered `run-*` holding a `grading.json`, so the
sample is reproducible and the next one lands on the same rows.

7. Read the sample in all three directions. The last column is what a fresh sample should be
   compared against.

   | Direction | Reaches a reader | Found 2026-08-22 |
   |---|---|---|
   | `script-heuristic` FAIL | yes, via `needs_agent.json` | 19 unchecked; 5 read, 4 wrong |
   | PASS, either method | no | 366 unexamined; 76 read, 6 wrong, 67 more defeated by a constructed answer |
   | `script` FAIL | no; the method label means confident | 29 read, 13 wrong, 45% |

   The passes are the direction nobody thinks to read and the one where the worst defects
   were: a pattern that is too loose fails silently and in the skill's favor.
8. For each check in the sample, ask what input it would wrongly admit, rather than only
   whether it is right on this answer. 67 of those 76 passes were correct on the answer in
   front of them and lost to one written against the pattern. Construct that answer; if it
   exists, the check is wrong while its verdict is right.
9. Verify each fixture with something other than the tool under test, and confirm that every
   path and URL an eval names resolves. `license-first-ideas-only` pointed at a URL that
   404s, so its central assertion passed vacuously for five rounds. A check that cannot run
   cannot be wrong, and cannot be right.
10. Check that each evidence string renders what was found: a count, a matched span, a
   computed value. Several printed a constant asserting the opposite of their own verdict.
11. Record the disagreement rate per direction in the log below, as sampled, read and wrong.
   It says whether the round can be trusted, and it had never been computed.

## The eval itself, which the grader pass assumes is worth running

**Whether the fixture can separate the arms at all, decided before you write it.** Measured
across 34 evals and every round: a fixture discriminates when the correct answer requires a
DECISION the artifact cannot supply, and ties when the correct answer is a FACT the artifact
contains. Every separating fixture asks the model to decide something; every tying fixture asks
it to find something. Finding is at ceiling for a frontier baseline with tools, which writes
its own contrast script when it has none. Deciding is not.

The properties that predicted it, with the split behind each:

| Property | Separators | Tiers |
|---|---|---|
| The prompt pushes toward the failure, or a fence stands in front of it | 7 of 7 | 0 of 4 |
| Three or more true findings, and the answer is their order | 4 of 7 | 0 of 12 |
| The correct answer requires an omission or a refusal | 6 of 7 | 1 of 12 |
| A near miss that must not be reported, and it is graded | 5 of 7 | 1 of 12 |
| The fixture annotates its own plant | 0 of 7 | 3 of 12 |
| The answer is derivable from the artifact alone | 1 of 7 | 12 of 12 |

The last row is the rule restated, and the last column is the warning: every eval that ties is
one whose answer sits in the file. Two guards state their own constraint in the prompt ("do not
change a character of it"), so they measure instruction-following rather than anything the
skill claims.

**Exclude the availability expectations before claiming any delta.** An expectation only an
installed skill can satisfy measures availability, not behavior. Nine evals published a delta
that was entirely availability and flat at 0.00 on behavior, and two more changed sign once it
was stripped, because `aggregate.py` computed the behavior-only rate per run and never printed
it per eval. It does now, and says so in words when the whole delta is availability. A delta
you have not stripped is not a result.

**A guard needs a wrong-answer control, exactly because it has no delta to show.** Four
preservation guards have 122 observations between them and zero failures, which is not evidence
they work. `check_fixtures.py` runs anything dropped into `evals/wrong-answers/` and reports a
control that passes every expectation, so a control costs nothing to run and needs no arm
re-run. Write it as an answer someone would plausibly produce that violates the exact fixture
line the guard protects, and quote that line in a comment at the top.


A grader can be right about an eval that could never have answered anything. Roughly eighteen
runs on 2026-08-22 went that way. Work through this when an eval is written or edited, before
its first round rather than after its fifth.

12. Run `python3 tools/evals/check_fixtures.py --offline --skill skills/skill-curator`. It
   puts every claim an expectation makes about its fixture back against the fixture: quoted
   literals must appear in the fixture text, paths in `files` and paths and URLs in prompts
   must resolve, absolute claims in fixture prose must hold, stated numbers must match what
   the bundled scripts report, and a leak check whose sample and target share every specific
   is named as the floor it is. `run.py` refuses to build a manifest until it exits 0.
   `--skip-fixture-check` overrides that and spends every run in the manifest on an eval the
   checker has already called broken.
13. Write the wrong answer before writing the fixture: the answer an unaided model would
   plausibly give, and that the eval should catch. If no plausible one can be written, the
   eval is a floor rather than a difference, and that is learned for free instead of after
   five rounds. An eval labeled `differentiating` ships that answer at
   `evals/wrong-answers/<name>.md`, and step 12 puts it through the real grader and fails the
   eval if it passes.
14. Check that the fixture does not hand over its own answer. A document that explains why
   each odd choice was deliberate tests reading comprehension rather than restraint.
   `deliberate-choices-are-not-defects` explained all four in a notes block and tied 3-3 on
   every signal across six runs.
15. Grep every absolute claim the fixture prose makes about itself. "The only", "never",
   "exactly one" are assertions about the fixture, so they get checked rather than written
   from memory: `considered-choices.html` called 13px the one place that size appeared while
   the stylesheet used it in seven rules, which turned careful reading into over-reporting.
16. For each expectation, ask what input would make it false. A check nothing can fail is
   worse than no check, since it publishes a pass: a 404 URL harvests nothing, so the
   no-verbatim assertion over the harvest held for five rounds, and a leak check whose sample
   shares every specific with the target cannot fire whatever the run writes.
17. Label the eval from its result rather than from its intent. `differentiating` claims a
   delta between arms and ships a wrong answer; `regression` says a fixed behavior still
   holds, which makes it a guard rather than a lesser eval, and its number is simply not
   evidence of a delta; `mechanism` says a bundled script or step does what it claims. Assign
   after the first result, revisit when a result moves, and let `aggregate.py` report the
   `differentiating` eval that tied and the `regression` eval that split the arms. Nineteen of
   thirty-three evals carried no label, so floors and measurements averaged into one headline
   for months.
18. Know the floor before quoting a delta. A pass rate is passed over decided, so it steps by
   1/k for k decided expectations, and one expectation on one of n runs moves an arm by
   1/(n*k), or 0.083 at three runs and four expectations. `aggregate.py` prints that floor per
   eval. A clean three-versus-three split has an exact permutation p of 0.10, so n=3 reaches
   suggestive and never reaches significant.
19. Check that each expectation names an observable rather than a judgment. An inter-reader
   study of 26 verdicts found one disagreement, and it was purely definitional: whether
   "flagged" meant appearing in a findings list or being asserted as a tell. Both readings
   were defensible, so that eval measured the reader. Name the span, the count, or the section
   the answer has to contain.


## Grader audit

Everything above audits sources. Nothing audits `tools/evals/grade.py`, which decides what
every published number means, and on 2026-08-21 and 22 it was found wrong five separate times
while the skills themselves were fine. Run this pass whenever a grader changes, and again
before any round is published. `public/EVALS.md` keeps the history; this is the procedure.

**After a re-grade, audit which ARM moved, not how much moved.** A grader fix changes stored
verdicts, and the count of flips says nothing about whether the fix was right. What says it is
the split across arms.

A flip that lands only in the baseline arm is the one to distrust, and it is the comfortable
direction: it widens the delta. On 2026-08-22 a re-grade moved seven craft-review verdicts and
every one was `without_skill`. All seven were false negatives in checks tightened earlier the
same day, and they clustered in the baseline for a reason that is not a coincidence — the
baseline writes plainly. It said "`--muted` is only defined in dark mode" where the check
wanted a theme *block*; it named the chip by what it resolves to, `--amber-500` on
`--amber-950`, where the check wanted the selector; it put the element in a heading and the
arithmetic in a bullet under it. Every one of those is a correct report of the planted defect,
and a tightened check that rejects them buys a wider delta with a worse instrument.

The rule this gives:

1. Diff the verdicts before and after, keyed by run directory and expectation.
2. Group the flips by arm. Symmetric movement changes coverage and not the delta, so it is
   cheap to accept. Movement in one arm is a finding until you have read the answers.
3. Read the actual answers behind every one-armed flip. Not the evidence string — the answer.
   The evidence string is written by the check under suspicion.
4. A flip that moves the delta in the skill's favor needs the same reading, and gets it last,
   because that is the one nobody is motivated to question.

The instruments cannot do this for you. `check_graders` passed 316/316 through all seven of
those false negatives, because every one of them was a case no fixture had.

**Control readthrough, for the expectations no script decides.** `check_graders.py` proves a
script check can fail. Nothing proves a reader-decided expectation can, because a fixture
tests a script and these have none: 28 of 174 expectations are `needs-agent`. What they do
have is a wrong-answer control per eval, an answer written to be wrong in one specific way.

    python3 tools/evals/grader_agreement.py emit-controls     # 37 blind (control, expectation) pairs
    ... grade each one, writing verdicts.json ...
    python3 tools/evals/grader_agreement.py compare-controls

Blind on the same terms as the agreement study: an opaque id, the expectation, and a copy of
the answer under a neutral name. No eval name, no verdict, and no indication that the answer
is a control, since a reader told it is looking at a deliberate wrong answer will find one.

An expectation that no control fails has no evidence it can fail. That is the same claim
`check_graders` makes for script checks, made by the only means available for these.

Run it before publishing a round, not on every build: it costs one reader call per pair, and
nothing about it is a gate. What it produces is a list of expectations to look at by hand.

**Sample by pattern, not by run.** A pattern that is too loose is a property of the pattern
rather than of the answer it happened to read, so three runs of one expectation exercise one
regex three times. Take one run per (eval, expectation, arm) and pick it deterministically,
the lowest-numbered `run-*` holding a `grading.json`. That covers every pattern for a
fraction of the reads, and the next sample lands on the same rows.

**Read all three directions.** Heuristic FAILs reach a reader through `needs_agent.json`: 19
of those stood unchecked, and of the 5 read, 4 were wrong. PASSes reach nobody. 366 had never
been examined, and of the 76 read, 6 were wrong and 67 more rested on a pattern that a
concrete failing answer defeats. FAILs the grader labels `script` reach nobody either,
because that label means confident: 29 read, 13 wrong, which is 45%. The passes are the
direction nobody thinks to check and the one where the worst defects were, since a loose
pattern fails silently and in the skill's favor.

**Ask what input the pattern would wrongly admit.** Whether it is right on the answer in
front of it is the weaker question: 67 of those 76 passes were correct on their own answer
and lost to one written against the pattern. For each check in the sample, construct the
answer that satisfies the pattern and misses the expectation. If it exists, the check is
wrong while its verdict is right. This is harvest criterion (c) pointed at the grader instead
of at the catalog.

**Verify each fixture with something other than the tool under test**, and confirm that every
path and URL an eval names resolves. That has been the rule for craft-review's fixtures since
round 3 and was never generalized. `license-first-ideas-only` pointed at a URL that 404s, so
its central assertion passed vacuously for five rounds. A check that cannot run cannot be
wrong, and cannot be right.

**Make each evidence string render what was found**, meaning the count, the matched span, or
the computed value. Several printed a constant that asserted the opposite of the verdict
beside it, which is worst at the moment someone opens `grading.json` to audit the grader.

**Record the disagreement rate, per direction**, in the harvest log, as sampled, read and
wrong. That is the number that says whether a round can be trusted, and it had never been
computed. A direction carrying no rate is not a checked direction.

## Package
Run `tools/us-english.py skills/skill-curator` from the repo root; it must report clean. US English is the house rule and publish.sh enforces it.


20. Validate frontmatter, confirm `scripts/` ships both tools, and run `audit.py` one last time on a
   directory containing only this skill. Then publish per the private repo's `publish.sh`.

## Log

| Checked | What | Result |
|---|---|---|
| 2026-08-21 | First pass. `audit.py` written and run on a 12-skill library; found three bugs in itself (block-scalar frontmatter, boundary detection, collision metric) and fixed them. `overlap.py` bundled. Provenance check corrected from filename to content after it passed this very skill on a format doc. | Both self-checks PASS. This skill flagged itself NO-PROVENANCE until `ATTRIBUTION.md` was written. |
