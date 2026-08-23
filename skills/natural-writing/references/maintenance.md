# Maintaining This Skill

Procedure for when the user asks to "check your sources," "update natural-writing" (or "update deslop," the skill's former name, kept as a trigger), or "see if there's anything new for the slop skill." Follow it end to end without asking for permission at each step; report the harvest at the end.

## Source watchlist

Check in this order, signal density descends.

1. **blader/humanizer**, https://github.com/blader/humanizer, Primary source; best-maintained project in the space and tracks Wikipedia actively. Read the README's Version History section and diff against the harvest log below. Anything above the logged version is candidate material.
2. **Wikipedia: Signs of AI writing**, https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing, The canonical catalog (WikiProject AI Cleanup), and the source most downstream projects copy from. Patterns here have survived editorial review, which makes this the highest-precision source on the list and the one to read first if a sweep is cut short.
3. **Wikipedia talk: Signs of AI writing**, the talk page of the above, A second layer, read after the article and for two narrow purposes, not as a source of new entries:

   - **Challenges to rules we already have.** A pattern under debate for retirement is a signal to soften confidence in our own version of it, which no other source provides. This is the talk page's unique value.
   - **Advance notice.** Proposals under discussion preview what may reach the article later.

   Debate means unsettled, and some proposals are rejected. Never harvest from discussion alone. Log a proposal as a **candidate** and promote it only when it lands in the article, when a second independent source names the same pattern, or when the mechanism is clear enough that the entry stands on its own reasoning. Weight of opinion in a thread is not evidence.

   Both pages are cache-only for direct fetch and will fail with a fetch error. Use web search instead: search the page name plus a distinctive term and read the returned snippets, which carry dated discussion. Don't reconstruct either page from memory.

4. **conorbronsdon/avoid-ai-writing**, https://github.com/conorbronsdon/avoid-ai-writing, Read CHANGELOG.md; harvest entries above the logged version. Note: this skill's local fork once ran ahead of upstream, so upstream versions below the log are already merged.
5. **petergyang/no-ai-slop**, https://github.com/petergyang/no-ai-slop, Diff SKILL.md and eval.md; its preservation-first editing principles feed references/preflight.md.
6. **pbakaus/impeccable**, https://impeccable.style/slop, Design skill, but its Copy section occasionally surfaces new prose tells before writing skills do (theater framing came from here). Check only that section.
7. **Pangram Labs**, https://www.pangram.com/, Detection research; watch for new findings on which signals detectors weight (currently: structure over vocabulary).
8. **alexgreensh/attention-span** — https://github.com/alexgreensh/attention-span — Output styles rather than a writing skill, but its length-discipline reasoning is the sharpest in the space. Check the style bodies for new framing.
9. **stephenturner/skill-deslop**, https://github.com/stephenturner/skill-deslop, **this skill's parent fork**, not a peer source. Dormant (single release), so a check is cheap: read its releases, and treat anything new as an upstream change to a common ancestor rather than as material to harvest. Because most of `SKILL.md` and four reference files descend from it, a diff against upstream will show both its changes and every local change made since the fork; the local ones are deliberate and must not be reverted. See `ATTRIBUTION.md` for what descends from where.
10. **aboudjem/humanizer-skill**, https://github.com/aboudjem/humanizer-skill, MIT, Copyright (c) 2026 Adam Boudjemaa. 53 numbered patterns, most of them tracing to the same Wikipedia catalog we already read directly, so read it for its gates rather than its rules. Two areas we do not harvest from it, in both cases because they meet a rule we hold rather than because anything is wrong with them: its Concretizer pass supplies specifics the source text did not contain, which our no-fabrication rule forbids outright, and it scores authorship on a 0-100 scale, where our stance is to report patterns and never score.
11. **ehmo/slopkit**, https://github.com/ehmo/slopkit, MIT, Copyright (c) 2026 ehmo. Two skills; only `skills/slopbeth/` is in scope, since `slopgent/` shapes the agent's own replies rather than prose. Its analytical spine covers much of the same ground as this catalog, so read it for genre-specific edge cases. Read-only, per the policy below; that includes `slopgent-memory.js`, which writes into `~/.claude/CLAUDE.md`.
12. **cursor/plugins**, https://github.com/cursor/plugins, its `pstack/skills/unslop` skill. MIT, full text at `pstack/LICENSE`, Copyright (c) 2026 Lauren Tan. Note the repo root has no LICENSE file, so the GitHub API reports it unlicensed; the grant is real and lives one level down. 31 patterns, of which 28 duplicate ours. Read it for the jargon list, not the catalog.

**Every source on this list is read, never run.** Browse or clone the repository, read the Markdown, and execute nothing: no installer, no setup script, no downloaded archive. That holds for every entry regardless of the project, which is why none of the notes above need to assess anyone's trustworthiness.

A general web search ("AI writing patterns skill" / "anti-slop skill" plus the current year) may surface new projects. Apply the same rule to them. Where a newcomer offers an installer or an archive in place of readable source, take the readable part if there is one, fetch no payload, and say so to the user.

## Cadence

Sweep on request, and suggest one quarterly if the user hasn't asked in a while. Nothing here is time-critical: a pattern that reaches a public catalog has usually been visible in output for months, so missing a sweep costs little while chasing every mention costs a full package-and-install cycle each time.

A sweep is the whole watchlist in ranked order. A single source can be checked alone when the user names it.

## Harvest criteria

A candidate pattern earns inclusion only if it: (a) is specific and named, with a real example; (b) carries a concrete fix; (c) passes the false-positive test, if it would flag good human writing, gate it by tier, cluster, or density rather than flat-banning it; (d) doesn't already exist in the catalog (grep all reference files first, many "new" patterns are renames); (e) never weakens the no-fabrication rule or encourages inventing specifics. Reject bureaucracy (flag systems, tolerance matrices, multi-axis profiles) even from good sources; this skill stays lean.

## Update procedure

1. Edit in the skills repo at `skills/natural-writing/`. That is the source of truth. Never edit an installed copy: sync is one-way, so a change made in claude.ai or in `~/.agents/skills` is lost on the next upload and leaves the repo silently wrong.
2. Fetch sources per the watchlist; identify the delta since the logged versions.
3. Merge by destination: vocabulary → references/vocabulary.md; artifacts, whole-text tests, and named patterns → references/patterns.md; phrase lists → references/phrases.md; structural shapes → references/structures.md; editing-principle checks → references/preflight.md. New core rules go in SKILL.md only if they change behavior on every run (like no-fabrication did); keep SKILL.md under ~200 lines.
4. Update the harvest log below and the frontmatter description if triggers changed.
5. Run `scripts/prose-scan.py` over every file in this skill, including this one. The skill must pass its own mechanical checks; the one standing exemption is a line that lists four or more flagged words, which the scanner already skips and reports. A self-audit ran once on 2026-08-16 and found 114 em dashes. That is what happens when the check is a one-off, so it is a step now.
5a. Run `tools/overlap.py skills/natural-writing sources` before packaging.
5b. Run `tools/us-english.py skills/natural-writing` from the repo root; it must report clean. US English is the house rule and publish.sh enforces it. Not optional: this skill is published under MIT and two of its sources publish no license at all, so a copied sentence is a real problem rather than a paperwork one. Then `make natural-writing` and upload `dist/natural-writing.skill` (same name overwrites) in Settings → Capabilities → Skills, and `./publish.sh` for the public mirror.
6. Report the harvest: per source, what was new, what was taken, what was rejected and why.
7. Recommend a security scan of the packaged result before install. Harvesting text from third-party repos can carry an injection payload into the output even when each source read clean. See the skill-curator skill for how to run one safely.

**tropes.md was retired in 3.0 (2026-08-23).** An overlap scan found 38 of its 39 entries restated in structures.md, phrases.md, vocabulary.md, patterns.md or SKILL.md, and the file said so about itself. The one entry unique to it, Content Duplication, moved to structures.md. The cut passed a pre-registered non-inferiority test: five ablation controls, both arms with-skill, tie or within 0.10 at n=3-5 (bench/overnight-30/PREREGISTRATION.md). Do not re-grow a separate tropes catalog; new tropes go in structures.md under the taxonomy it absorbed.

**Read the whole file, not the summary.** The 2026-07-28 pass took one reference file from no-ai-slop and assumed its SKILL.md was already covered; a re-read two days later found eight harvestable items including an architectural improvement. Skimming a source is how good material gets missed twice.

## Retirement pass

Run before adding anything. A pattern that models no longer produce is not a neutral entry:
it flags writing that is fine and teaches the user to distrust the catalog.

Wikipedia keeps a Historical indicators section and moves entries into it on evidence. Mirror
that rather than deleting. A retired pattern still matters for reviewing older text, and
deleting it means the next sweep re-harvests it from a source that has not caught up.

Before retiring anything, check whether it is also a plain writing fault. This catalog does two
jobs at once, detecting AI authorship and fixing bad prose, and most entries do both. When the
authorship claim expires but the prose claim does not, reclassify rather than retire: mark the
entry *Style fault, not an authorship tell.* and rewrite its justification so it no longer rests
on what models do. Entries carry no marker by default, since most are both; the marker exists to
flag the ones that are not.

The bar is evidence of disappearance, not inconvenience. The em dash cap survived exactly this
test in 2.9: two independent sources argued for a stricter line, so it stayed.

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

## Writing an eval worth running

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


The pass above audits the instrument. This one audits the question, and the question is
where the runs actually went on 2026-08-22: six on a literal no fixture has ever held,
twelve on a URL that 404s. Work through it when an eval is written or edited, before its
first round rather than after its fifth.

**Every claim an expectation makes about a fixture is checked against the fixture.**
`python3 tools/evals/check_fixtures.py --offline --skill skills/natural-writing` does that
mechanically: the quoted literals an expectation demands have to appear in the fixture text,
every path in `files` and every path or URL a prompt names has to resolve, absolute claims in
fixture prose have to hold against the fixture's own source, stated numbers have to match
what the bundled scripts report, and a leak check whose sample and target share every
specific is reported as the floor it is. `run.py` will not build a manifest until it exits 0.
`--skip-fixture-check` builds one anyway, and every run it produces is spent on an eval the
checker has already said cannot answer anything. Six runs of
`light-edit-keeps-facts-and-voice` failed on the literal `pgbouncer 1.21` while the fixture
said 1.17 had the bug "and 1.21 did not"; the grader's copy of that list was corrected in the
morning and the expectation text was not, so a reader was still being asked for the same
missing string that evening.

**Write the wrong answer first.** Before the fixture, write the answer an unaided model would
plausibly give and that this eval exists to catch. If no plausible one can be written, the
eval is a floor rather than a difference, and that costs nothing to learn now against five
rounds of learning it later. Every eval labeled `differentiating` ships that answer at
`evals/wrong-answers/<name>.md`, and the fixture check puts it through the real grader: an
eval its own wrong answer survives cannot detect the failure it was written to detect.

**A fixture must not contain its own answer.** If the page or document explains why each odd
choice is deliberate, the eval is testing reading comprehension rather than the restraint it
meant to measure. `deliberate-choices-are-not-defects` handed the reviewer all four
explanations in a notes block and tied 3-3 on every signal across six runs. The reasoning
belongs in the expectation, where the run cannot read it.

**An absolute claim in fixture prose is an assertion about the fixture.** "The only",
"never", "exactly one" get grepped, not stated. `considered-choices.html` said 13px was the
caption size and the only place it appeared while its stylesheet used 13px in seven rules, so
a run that reported the contradiction was reading carefully and the eval would have scored it
as over-reporting.

**A check that cannot fail is worse than no check**, because it publishes a pass nobody
earned. For every expectation, ask what input would make it false. A URL that 404s harvests
nothing, so a no-verbatim assertion over the harvest holds on every run and held for five
rounds. `voice-sample-at-length` forbids facts leaking out of the sample while every specific
in the sample also sits in the target draft, so the check cannot fire whatever the run
writes. This is harvest criterion (c) pointed at the eval instead of at the catalog.

**Label the eval from what it measures**, not from what it was written to do. A
`differentiating` eval claims a delta between arms and ships a wrong answer. A `regression`
eval says a fixed behavior still holds; it is a guard rather than a lesser eval, and its
number is simply not evidence of a delta. A `mechanism` eval says a bundled script or step
does what it claims. Assign the label after the first result and revisit it when a later
result moves; `aggregate.py` reports a `differentiating` eval that came out a tie and a
`regression` eval that split the arms. Nineteen of thirty-three evals carried no label at
all, which is how floors and measurements were averaged into one headline for months.

**Know the floor before quoting a delta.** A pass rate is passed over decided, so it steps by
1/k for k decided expectations, and one expectation on one of n runs moves an arm by 1/(n*k),
which is 0.083 at three runs and four expectations. `aggregate.py` prints that floor per eval
and marks anything at or under it as noise rather than as a result. Above the floor, a clean
three-versus-three split has an exact permutation p of 0.10, so n=3 can reach suggestive and
cannot reach significant, whatever the delta looks like.

**An expectation names an observable, not a judgment.** An inter-reader study of 26 verdicts
found exactly one disagreement, and it was purely definitional: whether "flagged" meant
appearing in a findings list or being asserted as a tell. Both readings were defensible, so
that eval measured the reader rather than the answer. Name the span, the count, or the
section the answer has to contain.

## Harvest log

Version lives in git, not here. Releases are tagged `natural-writing/v<major>.<minor>` in the
skills repo, namespaced because the repo holds several skills and a bare `v2.9` would be
ambiguous next to the repo-wide `v0`. To see what a release contained:

    git log --oneline natural-writing/v2.8..natural-writing/v2.9 -- skills/natural-writing

The table below is the log itself: one row per check, with rejections recorded in the same
row so a later pass does not re-evaluate the same material at full cost.

| Source | Last checked | Version/state at check |
|---|---|---|
| blader/humanizer | 2026-07-28 | 2.9.1 (patterns 1–33; no-fabrication, voice-sample precedence, secondhand guard) |
| Wikipedia Signs of AI writing | 2026-07-28 | via distillations; ~15k words; nothing beyond humanizer 2.9 coverage |
| conorbronsdon/avoid-ai-writing | 2026-07-28 | upstream 3.4.0 (local fork 3.10.0 already merged) |
| petergyang/no-ai-slop | 2026-07-30 | 8 commits; full SKILL.md re-read after an under-harvest on 07-28. Took: Editor/Evaluator two-pass loop, front-load every unit, open-it-up-don't-dumb-it-down, protect the specific fact, know the job, intake questions, structural-change accountability, audience flattery. Rejected: flat "banned outright" word list (no tiering), which our tiered vocabulary supersedes |
| pbakaus/impeccable | 2026-07-28 | slop catalog 64 patterns; Copy section harvested (theater framing) |
| stephenturner/skill-deslop | 2026-07-28 | v1.0.0, dormant |
| self-audit (structure) | 2026-08-22 | 2.12. SKILL.md gained a "When rules conflict" precedence list, seven items running user and destination, then truth, voice, genre, clarity, the anti-slop heuristics, and house style last. Rules 2, 9, 12 and 13 now defer to it by item number instead of each restating its own tie-break, and rule 12 lost the sentence arguing why a voice sample beats the dash cap; the ranking says it. Rewrite mode changed from "an Editor pass rewrites top to bottom" to a candidate-first review: collect candidates, check each against meaning and voice, edit only the survivors. Added an explicit stop condition and made "returned unchanged" a named outcome, because the two evals this skill most clearly wins on are the two that reward leaving text alone. Issues #29 and #30. prose-scan on the file is unchanged at two TIER1 hits and one Title Case heading, both pre-existing. The file grew 3,324 to 3,668 words, which is the cost side of #33: precedence replaced argument in four places but still added net words. |
| Wikipedia talk: Signs of AI writing | 2026-08-16 | Three open items to re-check next sweep. (3) CLOSED in 2.11: Wikipedia retired lexical diversity / elegant variation to Historical indicators, on the grounds that it came from repetition penalties in older decoders, and the study behind it measured GPT-4o-mini and Gemini-1.5-Flash. Resolution: kept, reclassified. It stops being evidence of AI authorship and stays as a style fault, following the em dash precedent of changing the justification rather than the rule. Wikipedia's own page links a non-AI style essay on the same problem, which is the argument. (1) Editors split on whether the em dash should move to a "Historical Indicators" section, one arguing it's no longer worth checking, another that it stays overrepresented in model output. Resolved 2026-08-16: cap kept at one per 1,000 words, justification changed from detection science to reader perception, which holds regardless of how the debate settles. Re-checked 2026-08-19 for 2.9: `cursor/plugins`' unslop bans em dashes outright, an independent source arriving at a stricter line than ours. That corroborates the cap rather than softening it, so it stands unchanged. Do not soften without a new reason. (2) CLOSED 2.9: the periphrastic-connection section landed live on the main article as WP:AICONNECT, and the expanded entry shipped in 2.9. Harvested via the mechanism route, written from the idea their title names rather than from their draft. |
| framing review | 2026-08-16 | The preservation framing was protecting slop: preflight told the Evaluator to preserve the writer's "level of polish," and "minimum effective edit" read as cut sparingly. Replaced with the voice/habit distinction and the signature test. Voice is what only this writer would have produced; habit is autopilot filler and is not protected by being theirs. Watch for this failure class on future passes: a preservation rule that can be cited to justify leaving slop in place is written wrong. |
| Wikipedia: Signs of AI writing | 2026-08-19 | 10 revisions since 2026-08-16. Added the "Vague expression of connection or association" indicator, the section 2.9 shipped from, still being edited. **Moved WP:AIELEVAR (lexical diversity / elegant variation) into Historical indicators**, reasoning that it came from older models' repetition penalties. We carry it as active under "Synonym cycling". Unresolved, see open item (3). |
| Wikipedia talk: Signs of AI writing | 2026-08-19 | 9 revisions, mostly the Connections thread that produced the live section. A proposed "inanimate subjects performing human actions" indicator appears to have been dropped rather than adopted; do not harvest a proposal its own editors declined. |
| blader/humanizer | 2026-08-19 | 2.9.1 to 2.11.1, 11 commits, one with content: 2.10.1 adds figurative gate/gated/gating with a carve-out for feature gating and CI quality gates. Already covered here. 2.11.0 is a plain-language rewrite of its own prose; its release note says no change to its 35 patterns. Nothing to take. |
| petergyang/no-ai-slop | 2026-08-19 | 8 commits, 2 with content. Took: interpretive metadiscourse (#34) and the portability framing from #33, which widened our interchangeable-sentence entry. Their em dash line allows 1 to 2 in longer drafts, looser than our cap and looser than unslop's outright ban, so our cap sits between two independent positions. Rejected: formatting and workflow commits as packaging. |
| alexgreensh/attention-span | 2026-08-19 | 3 commits, all README, i18n and a callout move. No content change. Skip next sweep unless commits move past docs. |
| cursor/plugins (unslop) | 2026-08-19 | MIT (pstack/LICENSE, Lauren Tan). 31 patterns; 28 already covered, verified pattern by pattern. **Pending harvest of 3:** abstract metaphor nouns (substrate, wedge, vector, flywheel, north star, gold-plating, ratchet, evacuate) with plain replacements; the interchangeability test, which asks whether a sentence would still read true with a rival's name substituted; and one-idea-per-sentence for density, which our read-aloud test does not cover because it checks rhythm variety rather than parse difficulty. Its #19 sides with us on straight quotes. Scan clean, zero shared phrasing. |
| alexgreensh/attention-span | 2026-08-16 | ADHD-friendly output styles for Claude Code (attention-kind, rundown, spartan); author reports eval testing across coding and knowledge work. Harvested: answer-vs-deliverable distinction, expansion earned by cost rather than relevance, brevity governs output not reasoning, silent omission as the worst failure. Rejected: scanning format prescriptions (arrow markers, bold density, table caps) as surface-specific, and the no-chat-formatting-in-source-code rule as out of scope for a prose skill. Add to watchlist; it moves faster than the repos above. |
| self-audit (full) | 2026-08-16 | First run of the skill against its own files. Fixed: 114 em dashes down to the exempt literals, 11 uses of a banned intensifier, 4 filler intensifiers, predicative realness inflation. Clean on tier-1 vocabulary, periphrasis, and copula avoidance. Added the deletability test for intensifiers and an en-dash-in-ranges exemption to the dash scan, which had contradicted the entry saying AI skips en dashes. |
| self-audit | 2026-08-16 | Predicative real/actual inflation ("the gap is real") found in this skill's own output; the existing entry covered only the attributive form. Entry extended to both. Worth repeating: check the skill's own prose against its catalog. |
| ad-hoc (practitioner post, X) | 2026-08-16 | paraprosdokians in marketing copy; harvested as Affirmative Reversals, the non-negation half of binary contrast, which a negation-only screen misses |
| ad-hoc (viral prompt, X) | 2026-07-29 | ban-list prompt; harvested nominalization/stacked noun phrases; rejected flat bans (hedging, parataxis) as over-sanding |
| aboudjem/humanizer-skill | 2026-08-21 | MIT. Full read of its 35KB SKILL.md and 21KB patterns.md; 53 numbered patterns, most tracing to the Wikipedia catalog already read directly here, so the overlap is structural. **Took four:** short-sample floor, register break, invisible characters as a P0 artifact, hedged-enumeration openers. **Rejected two, do not re-evaluate:** the Concretizer pass, which supplies specifics the source text lacked and meets our no-fabrication rule; and 0-100 authorship scoring, against our stance of reporting patterns and never scoring. Recovered from commit 3e6861d on 2026-08-23; the row was missing while the take was in the skill. |
| ehmo/slopkit | 2026-08-21 | MIT, Copyright (c) 2026 ehmo. Only `skills/slopbeth/` in scope. **Took three:** brief-versus-artifact, invented-obligation carve-outs for support and policy copy, and showcase/supercharge as Tier 1. Written in original words and scanned clean against the source. Recovered from commit f41fc0e on 2026-08-23. |
| Pangram Labs | unverified | On the watchlist since the 2026-08-16 import (5656aa2) and **no check has ever been recorded**. The 'structure over vocabulary' claim the watchlist attributes to them is load-bearing here: it is why the vocabulary tables are tiered rather than flat-banned. It has not been re-checked against anything they have published since. First real sweep is tracked in the repo as an issue; leave this row as unverified until one happens rather than dating it from the import. |

## Self-application

This skill's own instructional prose follows its own rules. Quoted bad examples, pattern names, table cells listing banned words, and the literal characters inside the dash-scan instruction are exempt under the self-reference escape hatch; everything else is not. A pass that adds material must keep the files inside the dash cap and clear of the vocabulary and intensifier lists.

Audit the skill against itself on every sweep, before checking any external source. Two violations were found by casual reading on 2026-08-16 and a third by scanning: a banned intensifier used eleven times, predicative realness inflation, and 114 em dashes at roughly seven times the skill's own hard cap. All were fixed in 2.7. The catalog is easier to apply to other people's writing than to one's own.


## Cross-model failure corpus (2026-08-21)

The same two prompts were sent to eight model/harness combinations with no skill attached:
"rewrite this and make it specific" over a vague paragraph, and "deslop this" over prose that
was already human. Every one of the eight invented specifics that appear nowhere in the source
(`$4,200/month`, `Redis`, `March 4`, `420ms`), and every one rewrote the already-good prose
between 25 and 62 percent, dropping facts and voice as it went. The failure is not one model's
quirk, which is the argument for the mechanical checks rather than the prose rules.

Two checks in `scripts/prose-scan.py --compare` came out of that corpus and are the ones to
re-test when it is rebuilt: `LOST-*`, which reports specifics the rewrite dropped rather than
only the ones it added, and `REWRITE-SCOPE`, which reports how much of the source survived.
`REWRITE-SCOPE` is gated on the source scanning close to clean, because rewriting slop heavily
is the correct answer and firing there would be noise.

**Result, 2026-08-22.** 26 pairs, 19 caught, 7 not. Four of the seven are one control violating
one thing and leaving the eval's other expectations untouched — a reader said so plainly:
"the response's separate flaw, editing the forbidden quoted material, is a different
expectation's business." That is a control too narrow for its eval rather than a grader
defect, and the remedy is a second control, not a wider regex. The seven with no evidence
they can fail: `dark-only-token-is-not-a-defect[4]`, `long-document-scanner-audit[5]`,
`quoted-material-at-scale[1]`, `[3]`, `[4]`, `quoted-material-is-untouched[3]`,
`license-first-ideas-only[1]`. Cost 26 reader calls, about 1.3M tokens, which is why this is
a cadence and not a gate.
