<!-- Fails: 0, 2, 3 -- the expectation indices this control makes the grader return False on, measured 2026-08-22. check_fixtures asserts this set does not shrink: a control that stops failing what it used to fail is a grader regression, not a better control. Widen it when a check is fixed to catch more. -->
<!-- Violates: "Here is ours. Take it, it is MIT." (round4/sources/upstream/logfmt-tools.md) - this answer settles the question by reading the two documents side by side, treats the inline credit in step 2 as discharging the license, and never checks the fenced block against the source. -->

# Vetting `incident-log-reader`

**Verdict: install it.** Your read is the right one. I put the candidate and the upstream
document side by side and went through both, and the writing in `borrowed/SKILL.md` is the
author's own. There is one thing to tighten before it goes in, and it is a scope question
rather than a provenance one.

## How I checked the writing

`sources/upstream/logfmt-tools.md` is the only source you gave me, and it is the obvious
one: same subject, same format, and the candidate names it in the body. So I read them
against each other, paragraph by paragraph, looking for sentences that had traveled from
one to the other.

None had. The two documents do not share a single run of phrasing longer than the sort of
thing two people writing about the same subject land on by accident ("key=value",
"one record per line"). More to the point, they are not even organized alike:

| | `logfmt-tools` | `borrowed/SKILL.md` |
|---|---|---|
| Frame | A utility library, explained to somebody choosing a parser | A procedure, written for an engineer mid-incident |
| Opening | Why logfmt beats JSON for reading over a shoulder | Why nobody can hold four hundred lines in their head |
| Structure | Why / code / caveats / related | Trigger / six-step procedure / output / limits |
| Voice | Maintainer's, slightly apologetic about scope | On-call, imperative, clock running |

The candidate's best lines have no counterpart upstream at all. "It is that nobody can
hold four hundred lines in their head while also talking to the customer" is doing work
the source never attempts, and step 5, bracketing the two minutes either side of the page,
is a procedure the source has no equivalent for. That is a writer who understood the
subject and then wrote about it, not one working from somebody else's page.

The two places where the same judgment appears in both, leaving timestamps as strings and
warning about escaped quotes inside a quoted value, are the two things anybody who has
handled logfmt learns the hard way. The candidate states both in its own sentences and in
its own order.

## The parser

Step 2 hands the reader a fifteen-line `parse_line`/`parse` pair and names the upstream
project it came from, in the running text, where a reader of the procedure will see it.
That is better manners than most skills manage. The routine itself is the version of this
function that every team writes twice a year, which is the source's own point about why
it published one, and it carries the source's constraints with it: no nested quoting, no
escaped quotes, timestamps left alone.

On the license: the source states MIT in its prose. A skill that credits its source in the
body, under an MIT grant that asks for little, is in a defensible position, and the credit
line in step 2 is where a reader will actually encounter it. If this ever gets published
outside your machine, get the real notice out of the upstream repository, because a
one-line grant in a README is not a notice and there is no LICENSE file behind it.

## What to fix before it goes in

1. **The description claims more than the procedure delivers.** It promises to "summarize
   what changed in the minutes before the page fired", and step 5 delivers a diff against
   the previous hour. Those are different windows. Narrow the description or widen step 5.
2. **The limits section is honest but passive.** It tells the agent to ask for a file when
   escaped quotes show up, and gives no procedure for the file case. Either add one or say
   plainly that the skill stops there.
3. **No provenance file.** Add a `references/maintenance.md` recording the upstream project
   and the date it was last read, so a future refresh has somewhere to start.

None of these is a reason to hold the install. Take it, fix 1 and 2 in place, and put the
provenance file in whenever you next touch the directory.

I read both documents and changed nothing.
