# skills

Three skills for Claude Code, Codex, Cursor, Grok and the other agents the
[`skills` CLI](https://github.com/vercel-labs/skills) installs into: one for prose,
one for UI review, one for keeping a skill library honest.

## Why these exist

A skill is usually a checklist the model reads and then grades itself against. These
three put the arithmetic in scripts and leave the model only the judgment. A dash
count, a contrast ratio, a pairwise description comparison across a library: a script
does those exactly in a second, and a model does them approximately and differently
each time. Each skill ships its scripts, a self-check for each script, an eval set in
Anthropic's `skill-creator` format, and an `ATTRIBUTION.md` that records where the
text came from as a measurement rather than a recollection.

## The skills

| Skill | What it does | Use when |
|---|---|---|
| [**natural-writing**](skills/natural-writing/SKILL.md) | Strips AI patterns from prose: write, rewrite, audit, or edit a file in place. Tiered vocabulary read live from the catalog, false-positive gates, a hard no-fabrication rule with a `--compare` check that lists every specific a rewrite added. | You say "deslop", "humanize", "make it sound human", or ask what AI tells are in a text; or you're drafting prose for publication. Fires on its own for those. Not for code or commit messages. |
| [**craft-review**](skills/craft-review/SKILL.md) | Reviews UI screens and flows. Reads exact values from source or Figma, computes contrast, spacing and symmetry with bundled scripts, then reports severity-ranked findings with numeric fixes. | You ask "does this look right", "review this screen", or share a screenshot or Figma link for feedback. Fires on its own. Not for turning mocks into a decision doc. |
| [**skill-curator**](skills/skill-curator/SKILL.md) | Maintains a skill library: audits for description collisions and bloat, vets third-party skills before install, harvests ideas without carrying phrasing, and scans for verbatim overlap against every source. | You ask to clean up or audit your skills, vet a skill before installing it, merge two that overlap, or check a skill's sources for updates. Not for writing a new skill from scratch. |

## What you get

**natural-writing** runs its scanner before it reads:

```
$ python3 skills/natural-writing/scripts/prose-scan.py draft.md

=== draft.md (80 words) ===
  vocabulary: references/vocabulary.md (62/42/17 terms)
  [DASH] 1 in 80 words = 12.5 per 1,000 (cap is 1). A voice sample overrides this.
  [INVISIBLE] 1x zero-width space (U+200B)
  [ARTIFACT] sycophantic opener: "Great question"
  [TIER1] "tapestry" — gated to the figurative sense, check this one
  [FORMAT] heading looks Title Case: "The Evolving Landscape Of Modern Systems"

  These are counts, not a verdict. Judgment checks are in references/preflight.md.
```

and `--compare original.md rewrite.md` prints every number, year, citation and name the
rewrite introduced that the source did not have. Zero is the only passing result.

**craft-review** computes before it judges:

```
$ python3 skills/craft-review/scripts/contrast.py --demo
       #000000 on #FFFFFF   21.00:1  want 21.00  ok
       #767676 on #FFFFFF    4.54:1  want  4.54  ok
```

`preflight.py` catches the artifact bugs a reader misses in one theme: a color defined
only inside a dark-mode block, a body with no background of its own, a contrast failure
resolved per theme. `symmetry.py` turns "looks unbalanced" into an inset delta in pixels.

**skill-curator** does the part of an audit that grows as the square of the library:

```
$ python3 skills/skill-curator/scripts/audit.py ~/.claude/skills
  [BLOAT] emil-design-eng: SKILL.md is 675 lines and loads whole on every trigger
  [NEAR-PAIR] emil-design-eng vs review-animations: share philosophy, emil, kowalski,
              animation, and neither names the other. Check whether one prompt could match both.
  [NO-PROVENANCE] apple-design: no file records where it came from
```

and `overlap.py` compares a skill against its sources in runs of eight words, which is
how this repo found its own attribution gap (below).

## Install

One command, for Claude Code, Codex, Cursor and Grok at once:

```bash
npx skills add LarrySequino/skills -g -s '*' -y \
  -a claude-code -a codex -a cursor -a grok
```

Three details, because each one is easy to get wrong:

- **`-a` takes one agent.** Repeat the flag. Comma-separated and space-separated both
  fail with `Invalid agents`.
- **`-g` installs user-level.** Without it you get a project-local install inside
  whatever directory you happen to be in.
- **Codex and Cursor get no directory of their own.** They read the shared store at
  `~/.agents/skills`. Claude Code and Grok get symlinks. All four work even though
  only two have folders.

Then confirm it landed, because a partial install is silent:

```bash
ls ~/.agents/skills            # natural-writing  craft-review  skill-curator
head -3 ~/.agents/skills/natural-writing/SKILL.md
```

Leave off `-a` entirely to be asked which agents you have; `--agent '*'` writes a
directory into your home folder for every agent the CLI knows about, installed or not.
Updating and removing are the CLI's own commands, documented
[there](https://github.com/vercel-labs/skills).

### claude.ai and Cowork

Neither has a CLI and neither can pull, so this is manual. A `.skill` file is a zip:

```bash
git clone https://github.com/LarrySequino/skills && cd skills/skills
zip -rD ../../natural-writing.skill natural-writing
```

Upload it at **Settings → Capabilities → Skills**. Uploading the same name overwrites.

## Provenance

Every skill carries an `ATTRIBUTION.md` naming what it descends from, what was
harvested as ideas and written fresh, and what expression carried over. Those files
record measurements: each skill is scanned against every source in runs of eight
words, short enough to catch a lifted sentence and long enough to skip most coincidence.
Generic prose can collide, so a single hit is a lead to read rather than proof; volume and run
length are what settle it.

That method found a gap in this repo's own work. **natural-writing began as a fork of
[stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop)** (MIT)
and shares 6,169 eight-word runs with it, the longest unbroken stretch running 1,189
words. Its parent credited two sources of its own, and those credits were lost in the
fork. All three are now in `ATTRIBUTION.md`, and the scanner is at
[`tools/overlap.py`](tools/overlap.py) if you want to run it on yours.

## Evals

Each skill ships `evals/evals.json` in Anthropic's `skill-creator` format: prompts with
checkable expectations, run with the skill and without. Scripts decide every expectation a
script can decide; a reader decides the rest, with a quoted line of evidence per verdict.
Opus 5 throughout.

| Skill | With | Without | Delta | Basis |
|---|---|---|---|---|
| natural-writing 3.0 | 0.95 | 0.83 | **+0.12** | 233 clean runs, pre-registered, 2026-08-23 |
| craft-review | 1.000 | 0.867 | +0.13 | 2026-08-22, still under review |
| skill-curator | 1.000 | 0.906 | +0.09 | 2026-08-22, still under review |

**Only the first row is safe to quote.** natural-writing was re-run from scratch on
2026-08-23 under rules written down before the first run: 28 evals (27 ship here; one runs
on another lab's model output, which this repo evaluates rather than redistributes), both
arms, a floor of three runs per arm with escalation to five or eight where the difference
warranted it, exact permutation tests, and a reader batch graded blind to which arm produced
each answer. Four evals separate at the pre-registered alpha:
voice-survives-a-house-style-pass +0.38 (p=0.0025, n=8), trust-the-reader +0.23, wh-opener
+0.20, voice-sample-at-length +0.20 (each p=0.0079, n=5). Eight more sit at 1.00 in both
arms; each carries a wrong-answer control proving it can fail, so a tie there is a floor the
unaided model already clears, not a blind spot. One eval scores 0.08 lower with the skill,
on report fidelity, and is filed rather than hidden.

That +0.12 is not comparable to the +0.06 this table published before it. Three things
changed at once: the skill went from 2.x to 3.0, the runs stopped being contaminated, and
fifteen grader defects were fixed, eleven of which had been penalizing the with-skill arm
because the skill's richer report format gave the checks more places to misread. Which of the
three moved the number, and by how much, is not recoverable from the data, so no causal claim
is made here.

**The other two rows are the old, contaminated numbers**, kept visible rather than deleted so
the record stays honest. Every run behind them inherited a persona hook, a `CLAUDE.md`, and
the full skill roster from the session that launched them, and the contamination is not
symmetric between arms. They also predate the grader fixes. Both skills need the same clean
re-run natural-writing has now had. [EVALS.md](EVALS.md) carries the detail.

Availability expectations, of the form "the transcript shows the skill's script was run,"
can only pass with the skill present, so they measure availability rather than behavior.
`aggregate.py` prints a behavior-only delta on every per-eval line and says so in words when
a whole delta is availability. The 2026-08-23 natural-writing figures above are unaffected:
that suite's separating evals turn on judgment, not on script availability.

Four things these numbers have taught us, all of them uncomfortable:

- **A skill can lose.** craft-review scored below its own baseline in round 1, on the two evals
  that test restraint, and the fix came from that. The number that made the case for this repo
  is the negative one.
- **More evals are floors than we thought.** An audit on 2026-08-22 counted every expectation
  verdict across every round and arm: **14 of 34 evals had never recorded a single behavior
  failure**, and **nine published a delta that was entirely availability**, flat at 0.00 on
  behavior. A tie is worth keeping only when a wrong-answer control proves the eval can fail;
  the 2026-08-23 suite ships one for every eval that ties.
- **The instrument is wrong more often than the skills are.** Twenty-three grader defects
  found to date across two audits, and every single one failed a correct answer rather than
  passing a wrong one. Fifteen came in one night, eleven of those against the with-skill arm,
  because a richer report format gives a pattern more places to misread. A grader audited only
  when the headline looks wrong will systematically under-measure the treated arm.
- **Contaminated runs cannot be un-contaminated by grading them again.** Every eval run before
  2026-08-23 inherited a persona hook, a `CLAUDE.md`, and the full skill roster from its
  launching session, asymmetrically between arms. Re-grading fixes the checks; it does not fix
  the answers. Two of the three skills above are still waiting on a clean re-run.

Each skill ships its eval definitions in `evals/`: the prompts, the checkable expectations,
and a wrong-answer control per differentiating eval so you can see what each one is able to
catch. The per-run records stay in the private repo. The round-by-round history, including
every correction and what it moved, is in **[EVALS.md](EVALS.md)**.

## Across model families

The same two prompts went to seven model and harness combinations with no skill attached:
"rewrite this and make it specific" over a vague paragraph, and "deslop this" over prose that
was already human. Six of the seven invented specifics the source never contained
(`$4,200/month`, `Redis`, `March 4`, `420ms`), the seventh used bracketed placeholders instead,
and every one rewrote the already-good prose, keeping between 29 and 59 percent of it.

| Model | Invented specifics | Source surviving the rewrite |
|---|---|---|
| grok-4.6 | 7 numbers, 3 names | 32% |
| gemini-3.7-flash | 15 numbers | 29% |
| gpt-5.6-terra | 6 numbers | 46% |
| claude-opus-5 | 11 numbers | 59% |
| deepseek-chat | 7 numbers | 41% |
| GPT via codex | 1 name | 50% |
| Grok via its CLI | 7 numbers, 3 names | 40% |

These are the two failures `natural-writing` exists to prevent, and no family is exempt.
`prose-scan.py --compare` catches all six fabrications and all seven over-rewrites. It passes
the run that used placeholders, which is the correct answer.

Running the skills themselves on another family is a smaller claim. GPT with `skill-curator`
scored 1.00 on the twelve-skill audit against 0.90 unaided, and with `craft-review` 1.00
against 0.80, but behavior-only both deltas are **+0.00**: GPT found the buried 3.74:1 chip by
writing its own luminance function in a heredoc, and read the twelve-skill library closely
enough to catch every planted defect. The skills are usable by a non-Anthropic agent, which
usable by a non-Anthropic agent. On these fixtures they do not measurably change what it
produces.

## This repo is generated

Published one-way from a private working repo; files here are overwritten on every
publish, so edits made directly to this repo are lost. Issues and pull requests are
read and applied upstream by hand.

## License

MIT. Each skill's `ATTRIBUTION.md` carries the notices for what it inherited.
