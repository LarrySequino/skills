<!-- Fails: 0, 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "pdf-fill is not reported as colliding with either; if it is mentioned at all, only to say it does not collide" - this answer clears the write-human/deslop-text pair as a two-stage pipeline and reports pdf-fill as the routing overlap instead. -->

# Audit: `evals/files/library/` (3 skills)

Three small skills. One is broken, and the description layer across the set was written
three times by three people who never read each other. The urgent item is `pdf-fill`,
which calls two scripts it does not ship. The structural item is routing, and it did not
land where the tooling pointed: the two prose skills read as consecutive stages of one
job, while `pdf-fill` is the file whose trigger reaches into ground the other two claim.

I read all three `SKILL.md` files, listed each directory, and ran `scripts/audit.py` over
the set before writing any of this. Nothing was changed.

## Inventory

| Skill | Body | Scripts named / shipped | Description | NOT-for clause | Provenance |
|---|---|---|---|---|---|
| `write-human` | 1 line | 0 / 0 | 199 chars | none | none |
| `deslop-text` | 1 line | 0 / 0 | 191 chars | none | none |
| `pdf-fill` | 1 line | 2 / 0 | 168 chars | one, partial | none |

## 1. `pdf-fill` calls two scripts that are not there

The body routes the whole procedure through `scripts/fields.py` and `scripts/fill.py`.
Neither file exists in the directory. This is the only defect in the set that fails on
first use rather than intermittently: the skill triggers, the agent reaches for a script
that is not on disk, and improvises the part the skill exists to make deterministic. Ship
both scripts, or rewrite the body around a tool that is present. Fix this first.

## 2. The two prose skills are a pipeline, not a duplicate pair

`scripts/audit.py` raises `write-human` and `deslop-text` as a near pair on description
similarity, and on a token count it is right: both carry prose, human, humanize, deslop
and AI tells. Similarity is not collision, though, and the two bodies do different work at
different moments.

- `write-human` is a producer's checklist. Its body lists things to keep out of text while
  it is being written: delve, tapestry, leverage, em dashes, the rule of three,
  "not X but Y", filler openers, uniform sentence length. It applies to a draft that has
  yet to exist.
- `deslop-text` is a repair pass over text that already exists, and its body carries a
  constraint the other one lacks: "Keep the writer's voice." That constraint only means
  something when there is a voice on the page to preserve, which is to say after the draft
  is written, frequently by somebody else.

Routing is decided on the description alone, so the distinction has to survive into that
field, and today it half does. `write-human` leads with "drafting or revising" and
`deslop-text` leads with "writing or editing text that must not read as AI-generated". A
prompt about text that already exists lands on the second, a prompt about text about to be
written lands on the first, and the model has enough to pick between them. Sharpen the two
openers so the stage is the first thing each description states, and keep both skills.
Collapsing them would cost the voice-preservation constraint, which is the more valuable
half of the pair.

## 3. The overlap nobody has written a clause for

`pdf-fill` overlaps both prose skills on one prompt shape, and it is a common one: "clean
up the wording on this form before I send it." The NOT-for clause on `pdf-fill` excludes
reading and summarizing PDFs, an exclusion nobody needed. It rules out the case a router
would never confuse and leaves standing the case that actually competes: a PDF handed over
with text in it that the user wants improved. All three descriptions match that prompt.
`pdf-fill` matches on the artifact, the prose pair matches on the verb, and the router
picks whichever description happens to score higher that day.

This is the conflict worth spending a boundary clause on. Extend the `pdf-fill` clause to
name prose work explicitly, and give each prose skill a matching clause that points form
work back at `pdf-fill`. Three edited lines, and the only three-way ambiguity in the set
is gone.

## 4. No provenance anywhere

None of the three records where it came from or when it was last checked, so every future
update starts from nothing. Add `references/maintenance.md` to whichever survive, with
ranked sources and a table of what each source was at when last read.

## Do this, in order

1. Ship `scripts/fields.py` and `scripts/fill.py`, or rewrite `pdf-fill` around a tool
   that exists. Verify on a real fillable PDF.
2. Rewrite the `pdf-fill` NOT-for clause to exclude prose work, and add the reciprocal
   clause to `write-human` and `deslop-text`.
3. Rewrite the two prose descriptions so each leads with its stage: drafting, or repair.
4. Add a harvest log to all three.

Deferrable: the provenance work, and the question of whether three one-line bodies are
substantial enough to be skills at all rather than lines in a project instruction file.
