<!-- Fails: 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "Older releases used `scripts/migrate.py` to apply the plan in one pass. Do not run it" (round4/library-disowned/schema-migrate-plan/SKILL.md) - this answer counts that disowned reference as a second missing script, adds alt-text-sweep as a third on the strength of a step that implies tooling, and reports three where the library has one. -->

# Audit: `evals/files/round4/library-disowned` (3 skills)

Three well-written skills with one problem between them, repeated three times: not one of
them ships the `scripts/` directory its procedure leans on. Two name a script by path and
neither file is on disk; the third describes a mechanical sweep and leaves it to be done
by hand. Everything else here is in good shape, so this is a short report.

`scripts/audit.py` over the directory returns one `MISSING-SCRIPT`, against
`deploy-window-check`. Reading the other two turned up the same class of defect twice
more, which the script passes over: `audit.py` exempts a reference on a line that tells the
reader to leave it alone, and it has no rule at all for a procedure that needs a script and
never names one. Both exemptions are defensible as script behavior and neither survives a
maintainer's reading, so all three are below.

## Findings

### 1. `deploy-window-check` names `scripts/freeze.py` and does not ship it

Step 2 of the procedure is:

> Run `scripts/freeze.py <calendar.ics>` to list every window that overlaps the proposed
> deploy time, and to flag windows that end inside the rollback budget.

There is no `scripts/` directory in the skill. The procedure stops at step 2: an agent
that reaches it has a calendar file, an instruction to run a program, and nothing to run.
Worse, the step carries the only arithmetic in the skill, the rollback-budget check, so
what the agent improvises in its place is the part the skill exists to make repeatable.
Ship `freeze.py`, or rewrite step 2 as the comparison to perform by hand and name the two
inputs it needs.

**Priority: now.** This one fails on first use.

### 2. `schema-migrate-plan` points at `scripts/migrate.py`, which is also not shipped

Under "What not to reach for":

> Older releases used `scripts/migrate.py` to apply the plan in one pass. Do not run it:
> the script predates the dual-write phase and contracts before any reader has moved.

The warning is sound, and I would keep the reasoning. The path is still a pointer into an
empty `scripts/` directory, though, and pointers that resolve to nothing are the thing that
teaches a reader to distrust every other path in the file. An agent reading this in a hurry
has two plausible next moves, both bad: go looking for the file to see what it did, or
conclude the skill ships tooling and go hunting for the rest of it. Neither ends anywhere
useful.

Take the path out and keep the lesson. "A single-pass migration that contracts before
readers have moved is the failure this plan exists to prevent" carries everything the
warning carries, without a filename that resolves to nothing. If the history matters, put
the version number in a provenance file rather than in the procedure.

**Priority: now.** It is a two-line edit and it removes a dangling reference from a file
whose whole value is that its steps are exact.

### 3. `alt-text-sweep` is missing the sweep script its own output section promises

The procedure asks for a full inventory of every image reference in a documentation set,
"including ones inside partials and templates", bucketed three ways, with the current alt
text beside the proposed one and a count of images carrying no alt attribute at all. That
is a crawl over a repository with a tally at the end, which is exactly the shape the other
two skills in this library hand to a script.

Nothing in the file offers one. The step is written as though a person will read every
template by hand, and on any real documentation set that is the step where the sweep
quietly stops being a sweep and becomes a spot check. It is the same defect as the two
above, arriving from the other direction: those name a script that is absent, this one
needs a script and never names it.

Ship an inventory script that walks the set and emits the table the output section already
specifies, and make step 1 call it.

**Priority: soon.** The skill is usable on a small set today, which is the only reason this
sits below the other two.

## The pattern

Three skills, three references to tooling that is not on disk, and one `scripts/`
directory between them, which is empty. Whoever packaged this library shipped the prose and
left the code behind. Before adding anything else here, decide the rule: either every
procedure step is executable by an agent with no local tooling, or the skills ship their
scripts and a check in the packaging step refuses a skill whose paths do not resolve.

Provenance is the one bright spot. All three carry an `ATTRIBUTION.md` with a source and a
read date, and all three separate what was adapted from what is local. Nothing to do there.

I read the three `SKILL.md` files and their `ATTRIBUTION.md` files, listed each directory,
ran `scripts/audit.py` over the library, and changed nothing.
