# Maintenance

How this skill stays current. Read only when refreshing it, not during a review.

Design slop differs from prose slop in two ways that shape everything below.

**It is partly visual.** A prose tell can be found by reading a catalog. "The icon
tile above the heading became universal" cannot. You notice it by looking at many
shipped screens. Reading repositories alone will always lag.

**It decays.** Prose tells are fairly stable; design tells turn over with fashion.
The 2022 set (purple gradients, glassmorphism, neon on black) has largely given way
to a 2026 "tasteful default": cream backgrounds, italic serif heroes, icon tiles.
A trope nobody commits any more is not neutral, it is a false-positive generator.
So a sweep must **retire** as well as add. That is the main difference from
`natural-writing`'s protocol.

## Source watchlist

Check in this order, signal density descends.

1. **pbakaus/impeccable**, https://github.com/pbakaus/impeccable (Apache-2.0), the
   catalog at impeccable.style/slop. The closest thing this domain has to a canonical
   list, and the only one that is explicitly era-aware. Read the catalog and diff
   against `design-tropes.md`. It also ships `npx impeccable detect` and a browser
   extension: run the detector against a real project and note what it catches that
   `slop-scan.py` misses; that gap is the highest-value material on this list.
   Apache-2.0 requires attribution *and* a statement of changes; see `ATTRIBUTION.md`.
2. **jakubkrehel/skills**, https://github.com/jakubkrehel/skills (MIT), the seven core
   `better-*` skills, chiefly `better-typography` and `better-ui`. Never harvested.
   Skip the `great-*` and `oklch-*` drafts.
3. **nutlope/hallmark**, https://github.com/nutlope/hallmark (MIT). Contributed the
   slop-test gates and the two-briefs framing already in Group E. Check for new gates.
4. **garrytan/gstack**, https://github.com/garrytan/gstack (MIT), its `design-review`
   skill. Same domain, entirely independent lineage. A 2026-08-17 scan found zero
   shared phrasing. That independence is exactly what makes it worth diffing: where it
   reaches a conclusion we also reached, the conclusion is probably real; where it
   differs, one of us is wrong. Read the review dimensions, not the orchestration
   scaffolding, which is specific to its own tool suite.
5. **emilkowalski/skills**, https://github.com/emilkowalski/skills (MIT). Motion craft.
   Feeds the motion dimension and the motion section of `design-tropes.md`. Already
   tracked in the repo's `sync/skill-lock.json`, so diff by version there.
6. **Mobbin** (MCP connector). The visual channel, and the only source on this list
   that shows shipped product rather than commentary about it. Use it to test whether a
   candidate trope is actually widespread and whether a catalogued one has died. Sample
   across categories, not within one. A pattern that is universal in fintech and absent
   everywhere else is a category convention, not slop.
7. **wonjyou/design-audit** and **Ashutos1997/claude-design-auditor-skill**. Neither
   publishes a license, so **ideas only, never phrasing**. Both contributed conceptually
   to the craft layer, and neither has ever contributed expression; a 2026-08-17 scan
   confirmed zero overlap. Keep it that way.
8. **AccessLint/skills**, https://github.com/AccessLint/skills (MIT). Five accessibility
   skills tiered by what is actually automatable: scan (rule engine), inspect (manual
   keyboard/AT), audit (full WCAG-EM), diff (regression), fix. Small repo, best-engineered
   on this list. Its evidence-basis tagging is what our Accessibility score is missing.
9. **vercel-labs/web-interface-guidelines**, https://github.com/vercel-labs/web-interface-guidelines
   (MIT). Note the Vercel *skill* in `agent-skills` is only a wrapper that fetches this file
   at runtime: read this repo, not the skill. Implementation-level where we are
   design-level, so most of it is out of scope; the typographic micro-details are not.
10. **bencium/bencium-marketplace**, https://github.com/bencium/bencium-marketplace (MIT).
   Its `design-audit` and `typography` skills. Same domain, dimension-table shaped, so it
   diffs cleanly against our Group A-E. Skip its heavyweight document pre-read protocol.
11. **nolanperk/rad-spacing**, https://github.com/nolanperk/rad-spacing. **No license:
   ideas only, never phrasing.** Small and single-purpose: hierarchical spacing by Gestalt
   proximity.
12. **WCAG 2.2, Apple HIG, Material**, the numbers in `thresholds.md`. These move on a
   release cadence rather than continuously; check when a spec version ships, not every
   sweep. A changed threshold is a correctness bug here, not an enhancement.

**Every source on this list is read, never run.** Browse or clone the repository, read
the Markdown, and execute nothing: no installer, no setup script, no downloaded archive.
That holds for every entry regardless of the project, which is why none of the notes above
need to assess anyone's trustworthiness.

**No source on this list is authoritative, including the ones we agree with.** Nobody has
this figured out yet, ourselves included. Every entry is somebody's current best guess,
written with the confidence that publishing demands and rarely with the evidence that would
justify it. Stars, traffic, a well-known author and an assured tone are all uncorrelated with
being right.

Three failure modes to watch, because we have committed all three:

- **Attributing a claim a source does not make.** The watchlist once credited Pangram with
  "structure over vocabulary" and SKILL.md built a ranking on it. They say no single feature
  decides. Quote before you paraphrase, and record the quote.
- **Taking a vendor's numbers as findings.** A detection company reporting its own accuracy,
  on evaluation sets it chose, with no published model or data, is marketing that happens to
  be numerate. It can still be true. Mark it as self-reported and let a claim rest on it only
  when nothing turns on the number.
- **Reading convergence as proof.** Two projects agreeing may mean two projects copied the
  same ancestor, or that a fashion is circulating. Convergence raises a question worth
  measuring; it never answers one.

What settles a question here is a measurement we ran and can rerun, with a control that could
have failed. Where we cannot measure, the honest move is to say the rule is a judgment call
and name what would change our mind. A borrowed certainty is worse than an admitted gap,
because the gap is visible and the certainty is not.

Discovering newcomers: search for design-review, design-audit and AI-slop skills on
GitHub sorted by recent activity, and check what `impeccable` cites. Screen anything new
with the security pass in `skill-curator` before fetching it, and apply the same read-only
rule to it.

## Cadence

Sweep on request, and suggest one quarterly if it has not been asked for. Nothing here
is urgent. A reflex pattern takes months to become widespread enough to be worth
flagging, so a missed sweep costs little, while chasing every new example costs a full
package-and-publish cycle each time.

A sweep is the whole watchlist in ranked order. A single source can be checked alone
when named. The retirement pass (below) runs on every sweep regardless of what was added.

## Harvest criteria

A candidate trope earns inclusion only if it:

**(a)** is specific and named, with a concrete example: "generic hero" is not a trope,
"centered hero with two equal-weight buttons" is;
**(b)** carries a fix that is a *design move*, not a prohibition. "Don't use gradients"
is useless; "let the gradient carry meaning or cut it" names a move;
**(c)** passes the false-positive test. The finding is the **reflex**, never the single
instance. If a trope would flag a deliberate, well-executed choice, gate it by density,
by co-occurrence with other tells, or by the absence of a stated reason. Never ban it
flat. This gate matters more here than in prose: every item in the catalog is something
a competent designer sometimes does on purpose;
**(d)** is not already present. Grep `design-tropes.md` first, since most "new" tropes
are renames of catalogued ones;
**(e)** never weakens **measure before you judge**. A trope must not license an eyeballed
verdict where a script could compute one, and no threshold enters `thresholds.md` without
a spec or platform guideline behind it. Never invent a number;
**(f)** is **era-stamped**. Record the year it was observed as current, because that is
what makes the retirement pass possible later.

Reject, even from good sources: scoring rubrics that add axes, per-framework advice,
and anything requiring a tool the skill does not bundle. This skill stays lean and
stdlib-only.

## Retirement pass

Run every sweep, before adding anything. For each section of `design-tropes.md`, ask
whether the pattern is still common enough to be worth flagging. Sample Mobbin across
categories rather than trusting memory.

Move dead tropes to a `## Historical` section with the year they stopped mattering.
Do not delete them: deleting loses the record, and the next sweep re-harvests the same
item from an old catalog. A historical trope also stays useful for reviewing older
surfaces, and the section itself documents how fast this domain turns over.

`natural-writing` faced the same question about the em dash, where editors debated
moving it to a historical section. It was kept active with the justification changed
rather than the rule softened. That is the right shape: retire on evidence of
disappearance, not on the finding being inconvenient.

## Update procedure

1. **Edit in this repo.** `skills/craft-review/` is the source of truth. Do not edit an
   installed copy; see the repo README's one-way rule.
2. **Run the retirement pass** (above), then fetch sources per the watchlist and identify
   the delta since the logged state.
3. **Merge by destination.** Tropes → `references/design-tropes.md`, in the matching
   category section. Numeric thresholds → `references/thresholds.md`. Profile-specific
   criteria → `references/context-profiles.md`. Anything statically detectable in
   HTML/CSS → a new check in `scripts/slop-scan.py`, with a case in its `--demo` and the check
   name added to that file's `PLANTED` set, so the self-check covers it too. New
   dimensions go in `SKILL.md` only if they change what every review does; keep it
   under ~200 lines.
4. **Update the harvest log below**, in the same pass, never afterward from memory.
   Record rejections and their reasons. Otherwise the next sweep re-evaluates the same
   material at full cost.
5. **Update `ATTRIBUTION.md`** if a new source contributed. Apache-2.0 sources need a
   statement of changes; MIT sources need the notice.
6. **Run the provenance scan. Not optional: this skill is published.**
   `./tools/overlap.py skills/craft-review <sources dir>`. Two sources on the watchlist
   publish no license at all, so a copied sentence from either is a real problem rather
   than a paperwork one.
7. **Package and publish.** `make craft-review`, upload `dist/craft-review.skill` at
   Settings → Capabilities → Skills, then `./publish.sh` for the public mirror.
8. **Report per source**: what was new, what was taken, what was rejected and why, and
   what was retired.
9. **Security scan** the packaged result. Harvesting from third-party repos can carry an
   injection payload into the output even when each source read clean. See `skill-curator`.

**Read the whole source, not the summary.** A catalog's README is usually a subset of
what its detector actually checks; the rules live in the code.

## Grader audit

`tools/evals/grade.py` decides what every published number about this skill means, and
nothing above points at it. Every defect found on 2026-08-22 was in the instrument rather
than in the skill. **Measure before you judge** governs the measuring too.

Run this whenever a grader changes, and again before any round is published.

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

1. **Sample by pattern, not by run.** A pattern that is too loose is a property of the
   pattern, so grading three runs of one expectation reads the same regex three times. Take
   one run per (eval, expectation, arm), picked deterministically as the lowest-numbered
   `run-*` holding a `grading.json`. That covers every pattern for a fraction of the reads,
   and a later sample lands on the same rows and can be compared against this one.
2. **Read all three directions**, not only the one that already has a reader:

   | Direction | Who reads it today | Found 2026-08-22 |
   |---|---|---|
   | `script-heuristic` FAIL | the agent grader, via `needs_agent.json` | 19 stood unchecked; 5 read, 4 wrong |
   | PASS, either method | nobody, ever | 366 unexamined; 76 read, 6 wrong, 67 more resting on a pattern a constructed answer defeats |
   | `script` FAIL | nobody; the method label says confident | 29 read, 13 wrong, 45% |

   The passes are the direction nobody thinks to check and the one where the worst defects
   were, because a pattern that is too loose fails silently and in the skill's favor. Budget
   the reading accordingly.
3. **Ask what input the pattern would wrongly admit.** Whether it is right on the answer in
   front of it is the weaker question: 67 of those 76 passes were right on their own answer
   and lost to one constructed against the pattern. For each check in the sample, write the
   answer that satisfies the pattern and misses the expectation, the way a ratio check that
   accepts any hex anywhere in the text is satisfied by arithmetic it never verified. If
   that answer exists, the check is wrong even where its verdict is right.
4. **Verify each fixture with something other than the tool under test**, and confirm that
   every path and URL an eval names resolves. This has been the rule for craft-review
   fixtures since round 3 and was never generalized: a page verified only by `preflight.py`
   encodes that script's blind spots as expectations. `license-first-ideas-only` pointed at
   a URL that 404s and passed vacuously for five rounds. A check that cannot run cannot be
   wrong, and cannot be right.
5. **Make each evidence string render what was found**, meaning the count, the matched span,
   or the computed value. Several printed a constant that asserted the opposite of the
   verdict beside it, which is worst at the moment someone is reading `grading.json` to
   audit the grader.
6. **Record the disagreement rate, per direction**, in the harvest log, as sampled, read and
   wrong. It is the number that says whether a round can be trusted, and until 2026-08-22 it
   had never been computed. A direction carrying no rate is not a checked direction.

## Eval authoring

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


`Grader audit` covers the instrument. This covers the question, which is where roughly
eighteen runs went on 2026-08-22: six on a literal no fixture has ever held, twelve on a URL
that 404s. Work through it when an eval is written or edited, before its first round rather
than after its fifth.

1. **Check every claim against the fixture, mechanically.**
   `python3 tools/evals/check_fixtures.py --offline --skill skills/craft-review`. It resolves
   the quoted literals an expectation demands against the fixture text, resolves every path in
   `files` and every path or URL a prompt names, tests absolute claims in fixture prose against
   the fixture's own source, recomputes stated ratios and counts with the bundled scripts, and
   reports a leak check whose sample and target share every specific as the floor it is.
   `run.py` will not build a manifest until it exits 0. `--skip-fixture-check` builds one
   anyway, and every run under that flag is spent on an eval the checker has already said
   cannot answer anything.
2. **Write the wrong answer first.** Before the fixture, write the answer an unaided model
   would plausibly give and that this eval exists to catch. If no plausible one can be written,
   the eval is a floor rather than a difference, and that is learned for free instead of after
   six runs. Every eval labeled `differentiating` ships that answer at
   `evals/wrong-answers/<name>.md`; step 1 puts it through the real grader and fails the eval
   if it passes, since an eval its own wrong answer survives detects nothing.
3. **A fixture must not carry its own answer.** A page that explains why each odd choice is
   deliberate tests reading comprehension, not restraint.
   `deliberate-choices-are-not-defects` shipped a notes block naming all four, and tied 3-3 on
   every signal across six runs. The reasoning belongs in the expectation, where the reviewer
   cannot read it.
4. **An absolute claim in fixture prose is an assertion about the fixture.** "The only",
   "never", "exactly one": grep it before writing it. `considered-choices.html` said 13px was
   the caption size and the one place it appeared while the stylesheet used it in seven rules,
   so a run reporting the contradiction was reading carefully and would have scored as
   over-reporting.
5. **Ask what input would make this expectation false.** A check nothing can fail is worse
   than no check, because it publishes a pass. A URL that 404s harvests nothing, so its
   no-verbatim assertion held on every run for five rounds; a leak check whose sample shares
   every specific with the target cannot fire whatever the run writes.
6. **Label from the result, not from the intent.**

   | Class | What its number is evidence of |
   |---|---|
   | `differentiating` | a delta between arms; ships a wrong answer under step 2 |
   | `regression` | that a fixed behavior still holds; a guard, not a lesser eval |
   | `mechanism` | that a bundled script or workflow step does what it claims |

   Assign after the first result and reassign when a later result moves. `aggregate.py`
   reports a `differentiating` eval that tied and a `regression` eval that split the arms.
   Nineteen of thirty-three evals carried no label, so floors and measurements averaged into
   one headline for months.
7. **Know the floor before quoting a delta.** A pass rate is passed/decided, so it steps by
   1/k for k decided expectations, and one expectation on one of n runs moves an arm by
   1/(n*k): 0.083 at three runs and four expectations. `aggregate.py` prints that floor per
   eval and marks anything at or under it as noise. A clean three-versus-three split has an
   exact permutation p of 0.10, so n=3 reaches suggestive and never reaches significant.
8. **Name an observable, not a judgment.** An inter-reader study of 26 verdicts found its one
   disagreement was purely definitional: whether "flagged" meant appearing in a findings list
   or being asserted as a tell. Both readings were defensible, so that eval measured the
   reader. Write the span, the count, or the section the answer has to contain.

## Boundary with `deslop`

`design-tropes.md` has a UI-copy section that overlaps the prose anti-slop skill. The
split: if the fix is to change *words*, it belongs to `deslop`. If the fix is to change
*layout, type, color or motion*, it belongs here. Microcopy that is only wrong because
of where it sits (a button label that has to be long because the layout gives it no room)
is ours. Keep both catalogs pointing at each other rather than duplicating entries.

## Harvest log


**2026-08-22 retirement pass.** First run against shipped product rather than other catalogs, via the Mobbin connector: nine searches across marketing sections, consumer fintech, AI products and iOS apps, sampled across categories rather than within one. 34 entries reviewed. **Retired 3** to a new `## Historical` section in `design-tropes.md`: the purple→blue SaaS gradient (active 2020-2024; one instance across roughly sixty current sections, and the rule flags any indigo brand ramp); decorative grid-line backgrounds (active 2023-2025; every current instance is a deliberate 404 or editorial brand move, which is the well-executed choice the rule would have flagged); theater framing (not dead, moved to `deslop` under the boundary rule, since its fix is entirely a change of words). **Rewrote 9** where the pattern held and the reasoning had rotted. The largest was glassmorphism: iOS 26's system material is glass, so translucency following the platform is now correct and flagging it is a false positive. Others: the hero-metric strip regated from form to vanity content; numbered section labels narrowed to unordered sets, since numbering an ordered process is correct information design; category-reflex palette examples refreshed, because fintech ships coral, mint and electric blue rather than navy and gold; pure black narrowed to the pairing with pure white at body size; gradient text narrowed to whole headlines, since Apple ships a gradient on one line; side-stripes narrowed to cards carrying no status; the over-rounded blob lost an invented 12-24px ceiling that had no spec behind it, under criterion (e); "Get started" and "Learn more" left the generic-label entry as conventions with known destinations. **Kept 22 unchanged.** Net: 3 retired, 0 added, which is the direction Self-application asks for.

Close calls, recorded because the next sweep should revisit them. The purple→blue retirement rests on absence of evidence, which is weaker than presence, and Mobbin's archive carries no capture date. Side-stripes were nearly retired and kept only because retiring them would force a script change on thin evidence. The italic serif hero survived on thin evidence because Mobbin skews toward established products and that tell belongs to 2024-25 startups.

**Script debt paid the same day.** `scripts/slop-scan.py` lost its `purple-blue-gradient` check with the entry, and `PLANTED` and `--demo` with it; the check is one revert away if the trope returns. `glass-default` moved from four backdrop-blur surfaces to eight, because a sticky header plus a modal plus any iOS 26 component set clears four without one decorative choice. `pure-black-white` now requires both tokens, matching the entry it implements rather than firing on `#fff` as a surface.

Two classes of entry cannot be settled this way and say so in the file: the three motion entries, because Mobbin holds frames rather than film, and the entries about what generators emit, because a library of shipped work contains no unshipped slop to measure.

Current version: 1.2.0.

**2026-08-17 sweep.** Taken: evidence-basis tagging and the human-required marker
(AccessLint); typographic micro-detail (Vercel WIG); sharper icon consistency (bencium);
spacing-encodes-depth (rad-spacing, idea only). Restructured `context-profiles.md` from
three conflated profiles into three independent axes (modality, platform, surface), after
Material confirmed the binding variable is input modality (touch 48dp, pointer 44dp), not
platform. That fixed a real defect: "mobile" resolved to Apple's 44 and under-enforced
Material's 48 on Android. Rejected: bencium's document pre-read protocol as bureaucracy;
Vercel's hydration/virtualization/framework rules as the wrong layer; ui-ux-pro-max as a
generator rather than a reviewer; Anthropic's frontend-design on license grounds. Two
suspected gaps proved false: dark mode and empty states were already covered. Provenance
scan clean against all sources.

| Source | Last checked | State at check |
|---|---|---|
| pbakaus/impeccable | 2026-08-17 | Apache-2.0 confirmed. Category-reflex test and deterministic-detector concept already harvested. **Pending:** a 72-line addition covering the 2026 "tasteful default" set: cream/beige backgrounds, italic serif display heroes, icon tiles above headings, repeated section kickers, numbered section labels. Not yet merged; tracked as a repo issue. Detector CLI never run against a real project. |
| nutlope/hallmark | 2026-08-17 | MIT. Slop-test gates and two-briefs framing harvested into Group E. Zero shared phrasing on scan. |
| jakubkrehel/skills | 2026-08-22 | MIT, ~3.8k stars. **HARVESTED 2026-08-22.** The seven core `better-*` skills; the `great-*`/`oklch-*` drafts were skipped as planned. **Take:** `transition: all` as a layout-animation tell, named here and by gstack independently, which is why it was taken. Verified as a hole before shipping: a page whose only motion was `transition: all .2s` scanned clean under `slop-scan.py`. The sweep reported no other take meeting criterion (c); that judgment is the sweep's and was not re-derived here, so the `better-*` set is worth a second read before this row is treated as closed. |
| garrytan/gstack | 2026-08-22 | MIT, ~128k stars. **HARVESTED 2026-08-22, read-only** per the policy above: the repository was read and nothing in it was executed. The review dimensions were the harvestable part, as expected; the ~110KB SKILL.md is otherwise orchestration. **Take:** `transition: all`, agreeing with jakubkrehel independently, and `user-scalable=no` / `maximum-scale` under 2 as a viewport that defeats WCAG 2.2 SC 1.4.4. The second went into `preflight.py` as a BLOCK rather than into `slop-scan.py`: it is wrong in a state the reviewer never enters, since a desktop review never pinches. Also verified as a hole — a page carrying it reported 0 blocking, 0 warnings. |
| emilkowalski/skills | 2026-08-17 | MIT. Ten skills upstream. Motion material feeds the motion dimension. Version tracked in the repo's `sync/skill-lock.json`. |
| wonjyou/design-audit | 2026-08-17 | **No license published.** Contributed conceptually to the craft layer. Scan confirms zero expression copied. Ideas only, permanently. |
| Ashutos1997/claude-design-auditor-skill | 2026-08-17 | **No license published.** Same status as above; zero overlap confirmed. |
| Mobbin | 2026-08-22 | **HARVESTED 2026-08-22 as the retirement channel.** Nine searches across categories. Works for layout, color, type and surface tropes. Two limits: results carry no capture date, so absence is weaker evidence than presence, and the archive skews toward established products. Structurally blind to what generators emit, since it holds only shipped work. Not yet used as an additive source; no new tropes taken this pass. |
| AccessLint/skills | 2026-08-17 | MIT, ~84 stars. **HARVESTED 2026-08-17.** WCAG-EM methodology; five skills tiered by automatability. **Take:** evidence-basis tagging on findings, and an explicit human-required marker for criteria a screenshot review cannot verify (keyboard operability, focus order, SR output). Our Accessibility /100 currently overclaims without it. Highest-integrity find of the sweep. |
| vercel-labs/web-interface-guidelines | 2026-08-17 | MIT, ~777 stars. **HARVESTED 2026-08-17.** The real source behind the Vercel skill, which is a 176-word wrapper. **Take:** typographic micro-detail — `…` not `...`, curly quotes, non-breaking spaces, widow prevention on headings — plus "interactive states increase contrast" and long/empty content handling. **Reject:** hydration, virtualization, `min-w-0` and framework specifics. Wrong layer; we review screens, not React. |
| bencium/bencium-marketplace | 2026-08-17 | MIT, ~392 stars, 16 skills. **HARVESTED 2026-08-17 (partial).** `design-audit` is the domain match. **Take:** iconography as a dimension (consistent style/weight/size, one set vs mixed libraries; we have none), empty states, and dark mode as a dimension rather than only a trope. **Reject:** its pre-read protocol (DESIGN_SYSTEM, PRD, APP_FLOW, TECH_STACK, LESSONS) as bureaucracy; our §3 is leaner. `typography` skill unread. |
| nolanperk/rad-spacing | 2026-08-17 | **HARVESTED 2026-08-17, idea only.** No license. ~13 stars, one file. One strong idea: spacing should encode nesting depth, each level roughly 1.4x its child, snapped to the 8px scale, grounded in Gestalt proximity. We check on-grid and consistent stepping but never that spacing *encodes hierarchy*: a screen can be perfectly on-scale with card padding equal to page padding. Computable, so it belongs in `symmetry.py`. Highest single-idea value of the sweep. |
| anthropics/claude-code frontend-design | 2026-08-17 | **(c) Anthropic PBC, all rights reserved, Commercial ToS. Not open source.** Most restrictive source examined. Assessed 2026-07-14 as strong on visual identity, thin on motion. Low marginal value against our current coverage, highest legal risk. **Do not harvest.** Listed here so future sweeps do not re-evaluate it. |
| nextlevelbuilder/ui-ux-pro-max-skill | 2026-08-17 | MIT, ~117k stars. A design *generator* driven by a search/RAG query contract, not a reviewer. Different job, little to harvest for a review skill. Its master-plus-overrides design-system persistence pattern is the only part worth revisiting, and only if `design-system.md` grows. |
| WCAG / Apple HIG / Material | 2026-08-17 | `thresholds.md` reflects WCAG 2.2 AA, Apple 44pt, Material 48dp. Re-check when a spec version ships. |

## Self-application

This skill is subject to its own Group E. The catalog must not become a checklist that
flags every considered choice, and the three-score model must not grow a fourth score.
If a sweep adds more than it retires two passes running, the catalog is drifting toward
a rubric. Cut before adding.

## Locale

Run `tools/us-english.py skills/craft-review` from the repo root; it must report clean. US English is the house rule for this repo's own prose and publish.sh enforces it. It governs what we write and publish, never text a skill is asked to edit: a writer's dialect is part of their voice and normalizing it is a defect, not a tidy-up.

## Adversarial review, 2026-08-21 (GPT-5.x via codex)

An outside model was pointed at this skill with instructions to find rules that are wrong,
construct inputs that produce false positives, and read the script source rather than trust a
passing self-check. Seven findings held up under my own reproduction; these are the ones worth
re-testing whenever the scripts change:

| What it found | Now covered by |
|---|---|
| The workflow ordered a fallback to the placeholder token file, which `design-system.md` itself says measures the screen against the wrong scale | `SKILL.md` step 2 infers the artifact's own scale and labels it `(inferred)` |
| `preflight.py` blocked a token defined and consumed entirely inside one theme | the check now fires only when a rule outside that theme reads the token; the demo page exercises the real defect |
| `contrast.py` dropped alpha, so a translucent foreground was never measured | `parse_color` returns alpha and `get_ratio` composites over the ground |
| `contrast.py` printed an error and exited 0 | unusable input exits 2 |
| `preflight.py` swallowed unparseable colors and passed them | reported as `uncheckable-color` |
| A page with no custom properties got no contrast pass at all | base is always a scope |
| `1.4x` nesting was marked Universal, so every miss was automatically Critical | demoted to a preference |
