<!-- Fails: 0, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "Avoid delve, tapestry, leverage, testament to, landscape, seamless, robust, crucial. Avoid em dashes. Avoid rule of three. Avoid not-X-but-Y." (the prompt's whole source) - every item duplicates an entry natural-writing carries, and this answer manufactures four takes out of the duplicates, three of which replace a conditioned rule with the source's flat ban, and files no record of the source. -->

# Harvest review: the anti-slop list against `natural-writing`

Eleven items, eight of them words and three of them structural rules. I checked each one
against `references/vocabulary.md`, `references/tropes.md`, `references/structures.md` and
`SKILL.md`, and there is more here than the size of the source suggests. Four things are
worth taking, and three of those four are the same finding wearing different clothes: on
the items we both hold, this source draws a harder line than we do, and on reflection its
line is the better one.

## Item by item

| Item | Where we hold it | Take? |
|---|---|---|
| delve | `vocabulary.md`, Tier 1 | No, ours is stronger |
| tapestry | `vocabulary.md`, Tier 1 | No |
| leverage (verb) | `vocabulary.md`, Tier 1 | No |
| testament to | `vocabulary.md`, Tier 1 | No |
| landscape (metaphor) | `vocabulary.md`, Tier 1 | No |
| seamless | `vocabulary.md`, Tier 1 | No |
| robust | `vocabulary.md`, Tier 1 | No |
| crucial | `vocabulary.md`, Tier 3, flagged by density | **Take: promote it** |
| em dashes | `SKILL.md`, capped at one per 1,000 words | **Take: tighten the cap** |
| rule of three | `SKILL.md`, "a three-item list is not a crime" | **Take: drop the carve-out** |
| not-X-but-Y | `tropes.md`, with the causal and cross-sentence variants | No, ours is much fuller |

Seven of the eleven are duplicates of Tier 1 rows we carry with replacements attached,
which the source does not offer. Nothing to do with those.

## The four worth taking

**1. Promote `crucial` out of the density rule.** We file it in Tier 3, which means it is
flagged when the document is saturated or when it lands beside a Tier 1 hit. The source
bans it outright, in the same breath as `delve` and `tapestry`, and I think the source is
right: `crucial` almost never survives the deletability test, and the words it stands in
for (important, key, necessary) are all shorter and all clearer. A Tier 3 entry that is
correct every time it fires belongs a tier up. One-line move in `vocabulary.md`.

**2. Tighten the em-dash cap.** Our cap is one per 1,000 words, which for the length most
drafts actually run means the writer gets one and the rule never fires. The source spends
no words on a threshold at all. Lower the cap to none below 1,000 words, keep one per
1,000 above that, and the rule starts doing work on exactly the documents where em-dash
overuse is most visible.

**3. Drop the rule-of-three carve-out.** `SKILL.md` says "a three-item list is not a
crime" and asks for two items over a reflexive triad. In practice the carve-out is the
sentence people quote back when a triad is queried, and it turns a rule into a
conversation. The source's line is one clause with no exception in it. Take that shape:
prefer two, and let the voice-sample rule stay the single exception, since it already
outranks the mechanical rules everywhere else.

**4. Take the list itself as a preflight card.** The whole source is four sentences an
editor can hold in their head, and we have nothing that compact. `references/preflight.md`
is the natural home: eleven items, one line each, as the last pass before publishing, with
the full entries linked underneath for anyone who wants the reasoning. This is the item I
would ship first, because it costs one file and no rule changes.

## How I would land it

1. Move `crucial` to Tier 1 in `references/vocabulary.md` and give it the three
   replacements above.
2. Edit the dash line in `SKILL.md` to carry the sub-1,000-word case.
3. Cut the "not a crime" clause from the structure section of `SKILL.md`.
4. Write the preflight card into `references/preflight.md`, eleven lines.
5. Run `scripts/prose-scan.py` over every edited file, then `tools/us-english.py`, then
   package.

Roughly 20 edited lines across three files, plus one new card. Nothing here changes what
the skill does on a run; it changes where three of its lines sit and how hard two of them
push.
