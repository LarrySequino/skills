<!-- Fails: 0, 1, 7, 8 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# Audit: library12

I read all twelve SKILL.md files end to end, plus the `references/maintenance.md` and
`ATTRIBUTION.md` files that ship beside them, and listed each skill directory to see what
is actually there. The procedures are strong and unusually concrete. The problems are
structural, and they sort cleanly into things that break at run time, things that waste
context, and things that will rot. In that order:

## 1. Two skills point at files that are not in the directory

- **csv-profiler** links `references/missing.md` for the delimiter and encoding cases.
  There is no `references/` directory in that skill at all, so an agent that follows the
  link gets nothing at exactly the moment the skill says the hard cases live there. Write
  the notes or drop the link.
- **flaky-test-triage** step 2 says to run `scripts/run.py <ci-export.json>`, and no
  `scripts/` directory ships with it. The ranking step is the center of the skill, and as
  written it cannot be executed. Ship the script or restate the step as the ranking to
  perform by hand.

These are the only two defects that make a skill fail outright while it is being used, so
they go first.

## 2. release-notes-draft is an outlier on size

At 491 lines, release-notes-draft is more than twelve times the size of any other skill
here, which run between 30 and 39 lines, and the extra bulk is not extra information. Each of its sections repeats the same sentence pattern, the same
pair of rewritten rejects with only the section noun swapped, and the same six-item review
list. State the pattern, the rejects and the review list once at the top, then keep each
section to the lines that genuinely differ. That is a file about a tenth of the current
size with nothing lost, and it stops a single skill from spending more context than the
other eleven combined.

## 3. Provenance is tracked two different ways, and two skills have none

Seven skills record sources in `references/maintenance.md`, three use an `ATTRIBUTION.md`
with a different shape, and **k8s-rollout-check** and **spreadsheet-formulas** carry no
provenance record of any kind: no source, no date, no note about where the procedure came
from. Nobody can refresh what nobody can trace. Pick the `maintenance.md` form, since it
is the one with a last-checked date and a refresh procedure, move the three ATTRIBUTION
skills onto it, and write the two missing files from whatever the authors remember.

## 4. Boundary pointers name skills that are not installed

Every "NOT for X, use Y" clause except the pdf pair sends the reader to a skill that does
not exist here:

| Skill | Sent to |
|---|---|
| figma-handoff | visual-critique |
| design-tokens-sync | naming-conventions |
| release-notes-draft | commit-style |
| csv-profiler | warehouse-loader |
| flaky-test-triage | test-authoring |
| k8s-rollout-check | helm-chart-author |
| spreadsheet-formulas | dataviz |
| sql-query-review | migration-planner |
| api-docs-publish | landing-copy |
| incident-postmortem | oncall-runbook |

A router told to use `warehouse-loader` and given no such skill either stops or invents a
handoff. Either install the named skills or restate each clause as a plain scope limit
with no target in it.

## 5. The pdf pair is the one place two skills compete

`pdf-form-fill` and `pdf-report-build` share most of their surface vocabulary: PDF,
template, document, fields, pages. A request phrased as "fill in the quarterly PDF" has
words from both, and the split between them (writing into fields that exist versus laying
out a page from nothing) is a distinction the requester has to already understand for the
routing to work. Tighten both so the trigger is the input rather than the output: one
takes an existing document, the other takes a dataset. Everything else in the library
sits in its own domain, so this is the only pair worth touching.

## 6. Source checks are aging

The recorded last-checked dates run from January to June of this year, oldest first:
release-notes-draft, incident-postmortem, pdf-report-build, pdf-form-fill,
api-docs-publish, sql-query-review, design-tokens-sync, figma-handoff, flaky-test-triage,
csv-profiler. Two are worth doing now rather than on rotation: api-docs-publish recorded a
patch release as pending five months ago, and design-tokens-sync tracks a spec that was
still an editor's draft when it was last read. Editor's drafts move.

## What is in good shape

Frontmatter is well formed everywhere, names match their directories, and each skill says
what it does and when to reach for it. The procedures carry real judgment rather than
generic steps, and several of them name the failure mode they exist to prevent. Trigger
surfaces are distinct across domains: figma-handoff and design-tokens-sync sit next to
each other in the design area, but one reads a frame for an engineer and the other writes
values into a repository, and the same goes for the two test-adjacent skills. Nothing else
in the set reads as redundant.

## Order of work

1. csv-profiler's dead link and flaky-test-triage's absent script.
2. Cut release-notes-draft down to the shared pattern plus the per-section differences.
3. Add provenance to k8s-rollout-check and spreadsheet-formulas, then unify the format.
4. Resolve the dangling pointers.
5. Sharpen the two pdf triggers.
6. Refresh api-docs-publish and design-tokens-sync, then the rest oldest first.
