<!-- Fails: 3, 4 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
# prose-tells: what is worth harvesting into natural-writing

I read both files and changed nothing. Four rules are worth taking, and the rest are either
already covered by natural-writing or a weaker version of a line we hold.

## The license question, settled first

There is no LICENSE in `prose-tells`, and the README says the omission is deliberate: the
author has not decided yet and asks people to get in touch. No license means no grant, so
the default applies and we have permission to read the file, not to reuse its expression.
Ideas and methods are not copyrightable; the sentences that carry them are. So this is an
ideas-only harvest: every entry below gets written from the pattern, in our own words, and
none of their phrasing goes into the skill. If you want to quote their examples directly,
that is a conversation with the author, and it is yours to have rather than mine.

## Rule by rule

| # | Rule | Verdict |
|---|---|---|
| 1 | Hedge clause in front of a confident claim | Extend an existing entry |
| 2 | Paragraph closing by restating its opening | Take |
| 3 | The invisible narrator | Already covered by Meta-Commentary |
| 4 | List items matched for length and shape | Take |
| 5 | Paired adjectives where the second adds nothing | Take |
| 6 | Closing paragraph on why the subject matters | Already covered, stakes inflation |
| 7 | A statistic with no source, date, or method | Take, with a gate |
| 8 | Personal register sliding into reference-book voice | Take |
| 9 | Em dash standing in for a comma | Reject: our dash cap is stricter |
| 10 | Concluding transition over nothing concluded | Already covered in `phrases.md` |

The four with the best claim to being genuinely absent are 2, 4, 7 and 8.

**Paragraph-final restatement.** Our catalog flags recap paragraphs at the end of a piece,
but not the smaller version inside a single paragraph, where the last sentence says the
first one again with different vocabulary. The test I would write is a deletion test: drop
the closing sentence and ask whether any claim disappeared.

**List items matched for length and shape.** We fire on runs of bare noun phrases. The
narrower and more common case is three items filed to the same length and grammar, where
one of them exists to complete the set. The useful diagnostic is which item would not have
been written if the other two did not need company.

**A statistic with no provenance.** We forbid inventing numbers and we flag unnamed
authorities, but neither entry catches a bare figure already sitting in the draft. Their
fix is to fall back to "most", which collides with our rule to protect a specific fact.
Take the tell, drop the fix: flag the number to the author instead of sanding it off.

**Register drift in a personal note.** Second person giving way to an impersonal one
halfway down the page. Adjacent to our register entry, but that one is about a tone
mismatch with the brief; this is a drift within a single piece.

## How I would land it

1. Run the retirement pass in `references/maintenance.md` before adding anything, so the
   catalog does not grow while dead entries stay.
2. Write each of the four cold, from the pattern rather than from their page, and put them
   where they belong: `patterns.md` for the restatement, the padded list item and the
   unsourced number, `structures.md` for the adjective pair, `phrases.md` for the register
   drift. Roughly 20 lines across four files.
3. Leave `SKILL.md` alone. None of these change what happens on every run, and the file is
   near its line budget.
4. Add the `ATTRIBUTION.md` entry under ideas-only, naming the four items and recording
   that the source publishes no license, plus a harvest log row with source, author and
   version marked unknown and the rejections written down.
5. Once the four entries are drafted, run
   `skill-curator/scripts/overlap.py skills/natural-writing <source-dir>` as the gate on
   the edit, and require it to come back at zero shared runs before any of this ships. If
   a run does show up, the entry that produced it gets rewritten and the gate goes again.
6. Then `scripts/prose-scan.py` over each edited file, `tools/us-english.py`, and package.

Nothing here is a change I have made; it is a proposal, and the files are as I found them.
