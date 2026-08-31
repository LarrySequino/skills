# Eval history

The current numbers and the method are in [the README](README.md#evals). This file is the
record of how they got there: seven rounds over three days, what each one changed, and the
twenty-three times the measuring instrument turned out to be wrong before any skill was.

## The rounds

| Round | Date | What it was for |
|---|---|---|
| 1 | 2026-08-21 | First run. 16 evals, 96 executor runs |
| 2 | 2026-08-21 | Re-ran the three evals round 1 exposed as badly specified |
| 3 | 2026-08-21 | New fixtures too large to hold in the reader's head |
| 4 | 2026-08-21 | Built coverage for checks that had shipped without any. No results file: it was graded as part of round 5 and has no numbers of its own |
| 5 | 2026-08-21 | Ran and graded that coverage; mostly a negative result |
| 6 | 2026-08-22 | Re-ran rounds 1 and 2 against the fixed skills |
| 7 | 2026-08-23 | natural-writing only: pre-registered, decontaminated, 233 runs. The first clean round |

All six were re-graded on 2026-08-22 after a grader defect surfaced. The executor runs are
untouched; the numbers as first published are in git history.

> **natural-writing is resolved. craft-review and skill-curator are not.**
>
> natural-writing was re-run from scratch on 2026-08-23 (round 7 below) and its numbers are
> clean. Every per-eval number in rounds 1 to 6 below, for all three skills, is superseded for
> natural-writing and still under review for the other two. Do not quote the round 1 to 6
> arithmetic. Three reasons, in order of how much they move:
>
> 1. **Contamination.** Every run before 2026-08-23 inherited a persona hook, a `CLAUDE.md`,
>    and the full skill roster from its launching session. The with-skill arm carried a
>    3,800-word instruction set telling it to ignore ambient styles; the baseline had nothing
>    of comparable weight, so the bias does not cancel between arms and its direction is not
>    knowable from the outputs.
> 2. **Grader defects.** Twenty-three found across two audits, every one of them failing a
>    correct answer. Eight were fixed on 2026-08-22; fifteen more on 2026-08-23, eleven of
>    those against the with-skill arm.
> 3. **Availability.** Nine evals reported a delta that was entirely availability, flat at
>    0.00 on behavior, and two more changed sign once it was stripped. `aggregate.py` now
>    prints the behavior-only delta per eval and says so in words.
>
> The rounds, the method and the reasoning below remain accurate as history. Round 7 is what
> the method looks like once the instrument and the environment were both fixed.

## Round 1: craft-review lost to its own baseline

craft-review scored 0.750 against a 0.900 baseline, and the per-eval record says why. It wins
where its scripts catch what a reader misses (a color defined only inside a dark-mode block,
+0.33), ties where the model already does the arithmetic unaided (contrast ratios, a 6px
inset), and lost on the two evals that test restraint. Handed a one-line verbal description
with nothing to measure, all three with-skill runs scored the page anyway ("Distinctiveness
3/10, in the rework band") and issued severity-tagged findings about a screen they had never
seen. On a well-built page it tagged taste remarks `[judged]` and still chipped them Major.
One defect underneath both: the severity machinery fired on things it had not measured.

## Round 2: the fix, and what it exposed about the evals

Three evals re-run the same day against the fixed skills, round 1 left intact at `76d11d7`:

| Eval | Skill | Round 1 | Round 2 |
|---|---|---|---|
| unmeasurable-is-said-so | craft-review | 0.50 vs 1.00 | **1.00 vs 0.92** |
| clean-page-is-called-clean | craft-review | 0.33 vs 0.50 | **1.00 vs 0.58** |
| voice-sample-precedence | natural-writing | 0.92 vs 1.00 | **1.00 vs 1.00** |

All three with-skill runs on the description-only prompt now refuse to score and quarantine
advice under a heading saying it is not a review of the screen. On the well-built page every
severity chip traces to `[computed]` or `[observed]` evidence and taste sits unchipped under a
Judgment calls section, where the baseline put taste among its fixes in 2 of 3 runs.

Two findings about the evals themselves, both recorded in the `evals.json` files. The "clean"
page was not clean under a review deeper than `preflight.py`: a `64ch` measure runs about 87
characters, and the page had no `lang`, no `color-scheme`, and a 48/64px frame. The skill was
right to find those, so the round-1 expectations that rewarded not looking were rewritten to
test reporting discipline instead. And four of the sixteen evals turned out to be floors both
arms clear, because the input hands the baseline every value: inline CSS in the craft-review
pair, and a defect visible on one read in the other two.

## Round 3: fixtures a reader cannot hold in their head

Inputs where the answer is not visible at a glance. A 1,537-word document with seven scattered
tells; a 442-line stylesheet whose only contrast failure sits inside a dark-mode block behind
three `var()` hops; one off-scale padding among 62 declarations; an asymmetry no source value
states; a twelve-skill library with one real collision and one red herring that scores higher
on raw term overlap. 48 runs.

| Skill | With | Without | Delta | Behavior-only |
|---|---|---|---|---|
| natural-writing | 0.943 | 0.793 | **+0.15** | +0.10 |
| skill-curator | 1.000 | 0.733 | **+0.27** | +0.07 |
| craft-review | 0.983 | 0.775 | **+0.21** | +0.00 |

The per-eval deltas are where the fixture design shows: the 62-value spacing page **+0.25**,
the layout-only asymmetry **+0.25**, the long audit **+0.29**.

craft-review's behavior-only number is negative, and the cause is in the runs. In 2 of 3 runs
its own contrast machinery generated Critical findings that outranked the defect `preflight.py`
had explicitly blocked on, and one run demoted the blocked defect to Major and put two of its
own findings above it. The skill found more and buried what it was pointed at. `SKILL.md` §6
now says a `[BLOCK]` is Critical and sorts first, and every run since has put it at row 1.

Three round-3 expectations encoded false premises, all in craft-review, all from verifying a
fixture only with the tool under test. The control borders really are 1.43:1 and the layout
really has no breakpoint, so runs were being marked wrong for finding real defects. All three
were rewritten to test reporting discipline and both rounds re-graded on one yardstick.

## Rounds 4 and 5: what happens when the checks get their own evals

Every check added while fixing round 3 had shipped without eval coverage. Round 4 built six
fixtures for them and round 5 ran and graded the 36 runs, which is why round 4 has no results
file of its own. The result is mostly negative:

| Eval | With | Without | What it measures |
|---|---|---|---|
| no-invented-names-when-made-concrete | 0.94 | 0.67 | **+0.27, the one real discriminator** |
| light-edit-keeps-facts-and-voice | 0.83 | 0.83 | a floor |
| dark-only-token-is-not-a-defect | 1.00 | 0.80 | regression guard; behavior identical |
| copied-code-under-original-prose | 1.00 | 0.80 | availability, not behavior |
| disowned-script-is-not-a-missing-script | 1.00 | 0.80 | availability, not behavior |
| alpha-only-contrast-failure | 1.00 | 1.00 | floor |

Behavior-only: natural-writing **+0.14**, craft-review **+0.00**, skill-curator **+0.00**.

One of six separates the arms on behavior. On the fabrication test all three baselines
invented figures and invented product names, up to nine `[NEW-NAME]` hits in one run, while
every with-skill run added none. The other five are floors or regression guards and are
labeled as such in each `evals.json`, so a headline delta is not mistaken for a behavioral
win. Their value is failing loudly if a future change re-breaks a check, which two changes did
during this round.

## Round 6: the same sixteen evals, against the code that ships

Rounds 1 and 2 predate the 2026-08-21 fixes, so their numbers described skills that no longer
existed. Round 6 re-ran all sixteen round-1 evals on 2026-08-22, 48 fresh with-skill runs:

| Skill | With | Without | Delta | Round 1, same yardstick |
|---|---|---|---|---|
| craft-review | 1.000 | 0.867 | **+0.13** | 0.750 vs 0.900 (−0.15) |
| natural-writing | 0.957 | 0.893 | **+0.06** | 0.988 vs 0.893 (+0.09) |
| skill-curator | 1.000 | 0.906 | **+0.09** | 1.000 vs 0.906 (+0.09) |

The baseline arm was not re-run. A baseline never reads the skill, so a skill fix cannot move
it; what can move it is the grader. The stored round-1 baseline answers were re-graded with
the current grader instead, which puts both arms on one yardstick and costs half the runs.
skill-curator landed on exactly its round-1 numbers, so a re-run of a skill already at ceiling
buys nothing, which is the sort of thing to establish before paying for the next one.

craft-review's jump is smaller than it looks. Two of its round-1 expectations were rewritten
during round 2, and round 6 grades against the rewritten text, so the honest comparison is
round 2's 1.00 rather than round 1's 0.750. What round 6 establishes is that the 1.00 survived
the script and rule fixes.

## Five times the instrument was wrong before the skill was

Each was caught by reading answers rather than trusting a number, and each would have
published a wrong one.

**Round 2, four regex defects, every one against the skill.** A pattern that read "named
`landscape` and cleared it" as flagging it. A synonym check that failed "watch the results"
for not saying "monitor". "AA needs 4.5:1" cited as a standard, read as a reported finding.
A chip counter that took "a minor point" for a severity label.

**Round 3, three expectations with false premises.** All from verifying a fixture only with
the tool under test, so real defects the fixture author never planted counted as wrong
answers.

**Round 6, heuristic guesses published as verdicts.** `grade.py` labels its shakier checks
`script-heuristic`, which its own docstring defines as "re-check on FAIL", and nothing
re-checked them. Nineteen such failures stood. Of the first five read against the answers,
four were the pattern misreading the answer: a phrase list wanting the literal word "clean"
from a report that said "P0: none", a step-check for "write it down" that missed "write the
whole thing down", and a `First/Second/Third` scaffold check that fired on "run it in staging
**first,**". Every heuristic failure now goes to the agent grader, whose verdict overturns it.
The correction lifted baselines about as much as skill arms: the absolute numbers moved and
the deltas did not.

**Round 6, every check that had passed.** The fix above routed failures to a reader and left
passes alone, so 366 of them had never been examined. Seventy-six were, one per pattern per
arm: six were wrong and 67 more rested on a pattern that a concrete failing answer defeats.
One `has()` matched **"ten" inside "maintenance"**, so any audit of a twelve-skill library
that mentioned `maintenance.md` satisfied the discovery-budget expectation for free. Another
accepted any six-digit hex anywhere in an answer as "the fix names the ratio it reaches",
which is how a with-skill run stating 5.66:1 for a pair that measures 6.66:1 passed — a
craft-review run that fabricated its arithmetic, in the skill whose premise is that it
measures. Ratio claims are recomputed against `contrast.py` now, and two-part checks scope
their second half to sentences that name the subject.

**Round 6, an eval that had never tested its subject.** `license-first-ideas-only` pointed at
a repository that 404s, so no run harvested anything and its no-verbatim-import assertion
passed vacuously in every round since round 1. It measured the absence of a harvest, not
license discipline during one. It now points at a local fixture that resolves, and the first
six runs that could fail it scored 1.00 against 1.00, a floor, because it asked about license
discipline, which a capable model already has. Rewritten on 2026-08-22 to score the two things
the arms do differ on, both 3/3 against 0/3: the overlap scan reported as already measured
against the unedited skill rather than named as a gate for later, and a security screen of the
source as third-party material. It now runs **1.00 against 0.60**. The eval was not weak; it
was pointed at the wrong question.

**And once it could be acted on, an eval run acted on the wrong thing.** The replacement prompt
said "harvest into natural-writing", and a with-skill run did: it edited `ATTRIBUTION.md`,
`maintenance.md`, `patterns.md` and `vocabulary.md` in the live skill, and the changes were
committed before anyone read the diff. The harness tells every run not to write outside its
output directory, and a task saying "into natural-writing" contradicts that. The edits were
reverted and the prompt now asks for a plan. This was unreachable for as long as the fixture
404ed, which is the general shape of the thing: a check that cannot run cannot be wrong, and
cannot be right either.

## Round 7: the clean run, 2026-08-23

The first round where neither the environment nor the instrument was known to be broken.
natural-writing only; craft-review and skill-curator still need the same treatment.

**Rules written before the first run**, in `bench/overnight-30/PREREGISTRATION.md`: the unit
of analysis, an exact permutation test on run-level rates, a ladder of looks at three, five
and eight runs per arm with alpha spent across them, a tie-exit, a margin below which a
difference is not worth chasing, and the decision rule for the one cut under consideration.
Nothing in that file changed after runs began.

**The environment.** The persona hook was turned off for every run and the absence verified
by probe before the first executor launched. `CLAUDE.md` and the skill roster remain in both
arms; they are identical across arms and cancel in the comparison, which is why the report
claims a relative delta and not an absolute one.

**233 executor runs.** 34 for the reference-file cut, 9 establishing the before state on
three new rule-conflict evals, and 190 for the suite itself across 28 evals in both arms.
Sixty-four expectations that no script could decide went to readers who were not told which
arm produced the answer.

| | With | Without | Delta |
|---|---|---|---|
| natural-writing 3.0, 28 evals | **0.95** | **0.83** | **+0.12** |

**The absolute rates carry a measured upward bias of about 2.5 points. The delta does not.**
Part of the grading is a low-confidence heuristic whose FAILs escalate to a reader and whose
PASSes never did, so 160 of them were never reviewed by anything. A blinded reader, graded against
known-verdict controls it had to clear first, overturned 11 percent of a sample of those, CI 3 to
33. Both arms are similarly exposed: 0.95 and 0.83 are each overstated by roughly one and a half
points, and the +0.12 becomes +0.117. Stated rather than
restated, because the correction is smaller than the run-to-run variation already reported here.

**Twenty-seven of the twenty-eight ship here.** `harvested-appeal-keeps-its-genre` runs
against a fundraising appeal written by another lab's model, and this repo evaluates that
output rather than redistributing it, so the fixture and its eval are withheld. The 0.95 and
0.83 above are over all 28; the suite you can clone and run is the other 27.

Significant at the pre-registered alpha: `voice-survives-a-house-style-pass` +0.38 (p=0.0025
at n=8), `trust-the-reader-when-told-they-are-new` +0.23, `wh-opener-run-not-the-word` +0.20,
`voice-sample-at-length` +0.20 (each p=0.0079 at n=5). The four have a theme: the skill's
measurable edge is judgment under tension, not vocabulary substitution. Eight evals tie at
1.00 in both arms, each with a wrong-answer control proving it can fail. One eval,
`quoted-material-is-untouched`, scores 0.08 lower with the skill, on the accuracy of its own
what-changed report.

**What the round changed in the skill.** `references/tropes.md` was retired after an overlap
scan found 38 of its 39 entries restated elsewhere; the survivor moved to `structures.md`.
The cut had to clear a non-inferiority rule fixed in advance against five ablation controls,
and it did. Three rule-conflict evals were added and the precedence order they test resolved
at 1.00 on every run.

**What it found wrong with the skill.** Two rules carry exceptions that lose to their own
headline: changelogs should keep their change-narration and did not survive three runs, and
methods-section passives are correct and were converted anyway. Both are filed.

**Fifteen grader defects, every one failing a correct answer.** The recurring shapes: a
finding split from its block-quoted evidence, a window one sentence too narrow to see a
reason stated adjacently, a vocabulary list that could not enumerate how a model phrases a
deliberate keep, a literal demanding digits where the answer spelled the number out, and a
severity heading read as a claim. Graders break where form varies and meaning does not.
