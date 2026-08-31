---
name: natural-writing
description: >-
  Remove AI writing patterns from any prose a person will read, and keep them out of prose you
  write. EDIT AND AUDIT TRIGGERS: "deslop", "de-AI", "humanize", "make it sound human", "clean up
  this writing", "find the AI tells", "sounds robotic", "reads like a chatbot", "sounds like AI
  wrote it", "full of buzzwords". WRITE TRIGGERS: "write", "draft", "write up", "put together",
  "turn these notes into", or naming where it goes -- to send, to post, to publish, to share with
  someone. ARTIFACTS: any email, any letter, blog post, newsletter, social post, announcement,
  press release, any report, meeting notes, any proposal, README, docs, release notes, website or
  marketing copy, slide text, UI microcopy, artifact or published page. NOT TRIGGERED BY:
  "explain", "what is", "how do I", or any answer that stays in the conversation rather than going
  to a reader. NOT FOR: code, comments, commit messages, or interface typesetting such as quotes,
  dashes and ellipses as rendered.
---

# Natural Writing: Prose Without AI Patterns

Strip predictable AI patterns from writing. Make prose sound like a specific human wrote it, not like a language model generated it.

## When rules conflict

The rules below do not carry equal weight, and they do collide. When two of them point opposite ways, the higher item wins:

1. The user's explicit instructions, and what the destination requires.
2. Truth: facts, relationships, quotations, qualifiers, causality, scope, commitments.
3. The author's voice as supplied, and their deliberate choices.
4. Genre and audience convention.
5. Clarity, density, and the quality of the argument.
6. The anti-slop pattern heuristics in the core rules.
7. Detector-facing signals and house style.

A lower item never overrides a higher one. Where a rule below says it defers, this is the order it defers to, and the numbers refer to this list.

## What a pattern match is worth

The patterns here are statistically more common in LLM output, but humans on autopilot produce the same shapes, whether under deadline, in an unfamiliar genre, or in a second language. A checklist is single-feature reasoning and the detectors that work are not, which is the durable reason a hit here proves nothing about who wrote it (`references/preflight.md`). So: these patterns are worth fixing in any prose, but never treat them as proof of AI authorship for a consequential decision (academic integrity, hiring, attribution). When auditing someone else's text, report patterns, not verdicts.

**This will not hide AI authorship, and it is not for that.** The point is worth stating because the mechanism overlaps with what evasion tools do, and because someone will try. The reason does not rest on any detector's accuracy, which is fortunate, because the numbers available are vendor self-reports. Pangram claims it still identifies text as AI-generated 99.57% of the time across 10,223 documents rewritten under the instructions of `blader/humanizer`, the first source on this skill's own watchlist, and runs a second classifier labeling text as *humanized AI*. Discount that figure as a vendor reporting on its own product against a tool it is positioned against, and the direction still holds: the people building detectors are training specifically on the transformation this skill performs. Editing for quality is the job here. Passing off AI text as your own is a different act, this will not accomplish it, and the attempt leaves a mark.

A short sample carries no signal. Under roughly forty words there is not enough text for rhythm, variety, or repetition to mean anything, and every pattern here becomes a coin flip. Say the sample is too short rather than returning a verdict on it. This is why a button label or a toast can be edited for voice but never audited for authorship.

Corollary for rewriting: don't over-sand. Deliberate fragments, sentences starting with "And," a repeated word that is the right word, natural disfluency: all of these keep text human. Applying every rule at maximum strictness creates the very uniformity you're removing.

## Telling voice from habit

Voice is what only this writer would have produced: their diction, their angle, what they notice, their humor, their rhythm, their opinions, their willingness to be blunt. Habit is what any writer produces on autopilot: throat-clearing, hedges, filler transitions, redundant setup, generic emphasis, the second sentence that restates the first. Habit belongs to the author in the sense that they typed it. It is not their voice.

This distinction decides every edit. Cutting habit raises the concentration of voice; protecting habit lowers it. A draft where the writer's three best sentences are buried under nine filler ones has less voice than the same draft with the nine removed.

**The signature test.** Could another competent writer in this field have produced this sentence, in these words, without thinking? If yes and it adds nothing, cut it. If it could only have come from this writer, keep it even when it breaks a rule in this skill.

Protection is asymmetric on purpose. Distinctive choices are protected even when they violate the rules: fragments, an "And" opening, a favorite em dash, a digression that carries character, a word choice more casual than the register expects. Generic choices get no protection merely because the author made them.

## Before editing anything

**Know the job.** Before structure or word choice, know what the piece is trying to do and who it is for. A rule that improves a memo can ruin a toast.

**Ask, but only what's missing.** If the user hasn't provided the draft, ask for it. If the audience or destination is unclear, ask one question: who is this for and where will it be published? If the goal is unclear, ask what the reader should think, feel, or do after reading. Never stall on this. If the user wants speed or can't answer, state your assumption in one line and proceed.

**Never invent to fill a gap.** An unanswered question is a flag in the output, not a guess in the prose.

**Separate the brief from the piece.** A request often carries instructions about the writing as well as the writing itself: "keep the bit about her cat," "don't make this sound like a lecture," "shorter than the last one." Those are constraints to satisfy, not content to reproduce. Text that ends up quoting its own brief back is the giveaway that the two were read as one thing.

**Maintainers:** "update natural-writing" runs the source sweep in [references/maintenance.md](references/maintenance.md). This lived in the description until 2026-08-22; it is a rare explicit trigger and the description is read on every routing decision, so it belongs here.

## Modes

**write:** the user asks you to draft something and wants it to sound natural. Apply the core rules while composing; run Quick Checks and the self-audit before delivering.

**rewrite** (default for existing text): review, edit what fails, summarize what changed, then verify in a **separate pass**. An Editor pass reads top to bottom and collects candidate problems, checks each candidate against meaning and voice, and edits only the ones that survive that check. Rebuild a paragraph only where local fixes would leave seams, or where the structure itself is the problem. An Evaluator pass then reads the result cold against [references/preflight.md](references/preflight.md) and reports failures. Run the Evaluator in a subagent where the harness supports one, otherwise as a distinct second pass rather than a glance back over your own work. Loop until preflight passes.

**When to stop.** Stop when the irregularities still in the text are deliberate voice, correct genre convention, or harmless variation. Being invoked does not mean a rewrite is owed.

**Returned unchanged** is one of the outcomes, not a failure to find anything. If no candidate survives the check, say the draft is already clean, name the few things you looked at and left alone, and hand it back as it stands. That is a finished rewrite-mode response.

**Minimum effective edit** means don't rewrite what already works. It does not mean cut sparingly. Rewriting a strong sentence for consistency is the error; leaving filler in place because the author wrote it is also the error. The writer should recognize the result as their own voice, sharpened.

**detect:** flag only, no rewriting. Use when the user says "detect," "flag only," "audit," "scan," "what AI patterns are in this," or when auditing text that shouldn't be altered (published work, someone else's writing). Group findings by severity and note which flags are clear problems vs. judgment calls. Report patterns with quoted lines and short fixes. Never assert or score AI authorship; the same shapes appear in rushed human writing, and secondhand text (translated, dictated, heavily edited by committee) triggers many flags legitimately.

**edit:** the user names a file and wants it fixed in place. Make minimal, targeted edits to flagged spans only. Leave already-human passages untouched. Never rewrite quoted material, code blocks, or text attributed to someone else; flag those instead. Afterward, re-read the file, confirm the flags are resolved, and report only the spans you touched.

## Core rules

### 1. Cut filler phrases

Remove throat-clearing openers ("Here's the thing:"), emphasis crutches ("Let that sink in."), business jargon ("navigate the landscape"), meta-commentary ("In this section, we'll explore..."), and confidence-calibration words that tell the reader how to feel ("Notably," "Interestingly," "It's worth noting"). See [references/phrases.md](references/phrases.md). A device the supplied sample actually uses is item 3 and outranks this paragraph, the same way a sample's dash rate outranks the cap: if the writer puts an exclamation mark on a number ("Twelve nodes. Twelve!"), that is their emphasis and it survives. What this paragraph removes is emphasis the draft reached for on autopilot, not emphasis the author demonstrated.

### 2. Replace AI vocabulary by tier

Not all flagged words are equal. Tier 1 words (delve, tapestry, leverage, seamless, testament to) appear 5–20x more often in AI text, so replace on sight. Tier 2 words (harness, foster, nuanced, ecosystem) are fine alone but a strong signal when two or more cluster in a paragraph. Tier 3 words (significant, innovative, effective) only matter at high density. This tiering exists to prevent false positives, so don't flag a lone "crucial" in an otherwise human paragraph. A word used in its field's technical sense defers upward and stays: truth and genre convention are items 2 and 4, the vocabulary heuristics are item 6, so "leverage" in a finance model and "ecosystem" in an ecology paper survive the pass. See [references/vocabulary.md](references/vocabulary.md) for the full tables.

### 3. Break formulaic structures

Avoid binary contrasts ("Not X. Y."), affirmative reversals that do the same work without negation ("A thousand integrations, and you'll only ever click one"), negative listings, dramatic fragmentation, self-posed rhetorical questions ("The result? Devastating."), anaphora/tricolon abuse, false concessions ("While X is impressive, Y remains a challenge"), and hedge-stacked predictions ("could potentially create"). See [references/structures.md](references/structures.md).

### 4. Eliminate AI tropes and chatbot residue

Watch for "quietly" and other magic adverbs, the "serves as" dodge, false ranges, superficial participle analyses, invented concept labels, grandiose stakes inflation, and false vulnerability ([references/structures.md](references/structures.md)). Separately, hunt **chatbot residue**: text that is near-proof of pasted AI output: "Great question!", cutoff disclaimers, unfilled `[placeholders]`, leaked citation tokens (`citeturn0search0`), `utm_source=chatgpt.com` URL parameters, reasoning-chain scaffolding ("Let me think step by step"). Residue is always P0. It is catalogued in [references/patterns.md](references/patterns.md) under the heading Artifacts, which is that file's name for it and not the published-page sense used below.

### 5. Prefer active voice with human subjects

Prefer active constructions with named actors: "The team fixed it," not "The complaint becomes a fix." If no specific person fits, use "we" in scientific prose or "you" in blog posts. Exception: passive voice is conventional and correct in scientific methods sections and anywhere the actor is unknown or irrelevant. Don't force an awkward actor into "the samples were centrifuged."

### 6. Be specific, but never fabricate

No vague declaratives ("The reasons are structural"); name the thing. No vague attributions ("Experts argue..."): if you cannot name the expert, you do not have a source. No lazy extremes ("every," "always") doing vague work. Domain terminology is fine and expected in technical prose; the problem is business buzzwords and AI vocabulary leaking in, not precision.

**Protect the specific fact.** Fabrication's mirror image: never smooth an existing useful detail into generic importance. "Cut review time from 30 minutes to 8" must survive the edit; "significantly improved efficiency" is what happens when it doesn't. Specifics in the source are the most valuable thing in it.

**No-fabrication rule (hard constraint):** specificity must come from the source text or the author, never from the rewrite. Never invent facts, names, numbers, dates, quotes, or citations to replace a vague claim. When a claim needs a specific the text doesn't contain, either cut the claim, keep it and flag it ("[needs a number: how many customers?]"), or ask the author. A bare slot such as "[N]" or "[DATE]" counts as the same thing; `--compare` treats any bracketed span as a flag, so the form is yours to choose as long as the value is not asserted outside one. A vague true sentence beats a specific invented one. Also flag citations that look fake or unrelated to the claim they support, since AI text frequently cites real sources that don't say what's claimed.

Two genres invent a specific kind of specific, and both are worth naming because the invented thing is a commitment someone else has to honor. In support and service copy, watch for promises the author never made: "we will review this and follow up," "a specialist will reach out." In policy, incident, and compliance copy, watch for asserted properties: "auditable," "fully encrypted," "resilient." If the source does not say it, it is not a description, it is a liability.

### 7. Describe the thing

Prose and docs should describe what something *is*, not narrate the edit that produced it. "This function was added to replace the old lookup" is diff-anchored writing; "This function uses a hash map for O(1) lookups" describes the thing. Changelogs and commit messages are the exception, since there the change is the content.

### 8. Match register and voice

Blog posts: put the reader in the room; "you" beats "people." Scientific writing: appropriate formality, "we" for your own work, cite specific authors. Docs: clarity over voice, imperative mood for instructions. Social posts: fragments and 2–3 specific hashtags are fine; 6+ trailing hashtags is a hard flag.

If the user provides a sample of their own writing, calibrate to it: match its sentence-length pattern, contraction rate, and word choices. Don't "upgrade" their vocabulary. If they write "stuff," keep "stuff." If text already has a voice, don't impose one.

**Dialect is voice, and the draft is its own sample.** British, Australian, Indian, Irish, Canadian, Nigerian, Singaporean and every other variety of English belongs to the writer. If a draft says `organised`, `centre`, `whilst`, `maths` or `10/06/2026`, those are the author's and they stay, along with the punctuation and quotation conventions that travel with them. This rule needs no supplied sample, because the text in front of you is the sample: normalizing a dialect is the same flattening this skill exists to prevent, and it is worse than most, because it edits who the writer is rather than how carefully they wrote. Convert only when the user asks or a named destination requires it, and say so when you do. A mixed draft is a consistency question to raise, never one to silently resolve toward the variety you saw most in training. A provided voice sample outranks the mechanical rules where they conflict: if the writer's authentic style uses em dashes or triads, their voice wins over the ban. That holds for every rule below, not only the ones that name the exemption.

**Then check it with `scripts/prose-scan.py --voice <sample> <rewrite>`.** It counts the devices the sample demonstrates and reports each one the rewrite dropped or thinned to under half the sample's rate. Reading the sample and naming its habits is not the same as carrying them: on 2026-08-22 a benchmark run catalogued "exclamation for emphasis (\"Twelve!\")" in its own notes and then shipped a rewrite with no exclamation mark in it, five runs out of five. A rule stated more clearly does not fix that. A count does. Traits the sample uses only once are skipped, because one instance is not a habit, and it reports `IMPOSED` when the rewrite runs a device at more than twice the sample's rate: a voice matched by overshooting is not matched.

It protects voice and never habit. Nothing in `references/phrases.md` is covered — throat-clearing, emphasis crutches, meta-commentary, vague declaratives are what any writer produces on autopilot, and a sample full of them is a writer with bad habits rather than a writer whose bad habits are sacred. Where the sample carries any, `--voice` names the categories and says they are not protected, so the exemption cannot be read wider than it is. The plain scan now counts those phrases too, live from `phrases.md`, which is what keeps the two halves the same strength: before that, keeping the author's devices was a count and cutting the author's filler was a memory.

### 9. Vary rhythm

Uniform rhythm survives every word-level fix, so a vocabulary pass will never catch it. Mix short sentences (3–8 words) with long ones (20+). Vary paragraph lengths deliberately; some should be one sentence. Don't stack punchy fragments for manufactured emphasis. A fragment that carries the author's voice is item 3 and this rule is item 6, so the fragment stays; what goes is the stacking that came from the draft's habit. Prefer two items over reflexive triads, but a three-item list is not a crime. The flag is *compulsive* rule of three, not any tricolon.

### 10. Trust readers

State facts directly. No pedagogical hand-holding unless the audience needs it. No fractal summaries (preview, say, recap). No infomercial hooks ("The kicker?"). No self-labeling significance ("That last one is the contrarian move"). Write the list so the right item carries its own weight.

### 11. Do not dilute

One point per section. Ask of every paragraph: what's actually new here? If you could cut 40–60% and lose no information, cut it. Don't beat one metaphor to death or stack historical analogies for false authority.

### 12. Watch formatting tells

No bold-first bullets. No unicode arrows or emoji in headers. Sentence case for subheadings, not Title Case. No "In conclusion..." signposts. Bullets only for list-like content; a list of 5+ bare noun phrases with no verbs ("Reliable pool connectivity / Optimized performance") should become prose or full claims. Em dashes: the cap is house style, item 7, and a supplied voice sample is item 3, so if the writer supplied one its dash rate is the rule and nothing else in this paragraph applies; match it. Absent a sample, target zero, hard max one per 1,000 words, including headings. The basis is reader perception, not detection science: it's the most widely circulated AI tell there is, so dash-dense text reads as machine-written whatever detectors weight. Keep the cap even where the tell is argued to be aging out.

### 13. Front-load every unit

Put the conclusion first at the levels a reader navigates by: the draft, the section, the paragraph. Point, then detail, then background. Most AI structure inverts this, building context toward a conclusion the reader needed up front. It stops at the paragraph on purpose. Front-loading every *sentence* produces the one-thought-per-sentence profile that rule 9 and the dramatic-fragmentation entry are trying to undo; inside a paragraph, let sentences build. Exception: narrative and persuasive setups that earn their delay. Front-loading a joke ruins it. Front-loading is item 5, below both the author's deliberate structure and genre convention, so an order the writer chose on purpose is not a candidate; and no reordering may separate a claim from the qualifier that limits it, which is item 2.

### 14. Open it up, don't dumb it down

Strip what makes writing hard to read: tangled clauses, abstract nouns, jargon that isn't load-bearing, sentences carrying three ideas. Keep what makes it worth reading: substance, nuance, precision, technical vocabulary the audience shares, and the author's actual position. Simplification that removes content is deletion. If a cut would lose information, restructure instead.

### 15. Know whether you're writing an answer or a deliverable

An **answer** explains, decides, advises, or reports. It states its point and stops; length is a cost. A **deliverable** is the artifact you were asked to produce, such as a doc, spec, plan, post, or report. There, length is the substance, and cutting it is cutting the work. When you can't tell which you're writing, treat it as an answer.

Applying answer discipline to a deliverable produces a thin artifact. Applying deliverable discipline to an answer produces a wall of text nobody reads. Most length complaints are this mismatch rather than bad writing.

**This rule governs what you write, not what you are asked to shorten.** Wordiness is this skill's business only where it has a pattern behind it: one point restated ten ways, the treadmill effect, synonym cycling, sentences that could swap places without loss. Those are catalogued and have a shape. "Make this shorter" over prose that is already saying distinct things is ordinary editing, and ordinary editing is not this skill. Say so and leave it rather than cutting good sentences to satisfy a request you were not built for.

**Expansion is earned by cost, not relevance.** Expand a point where a mistake would cost the reader: a risky step, a real trade-off, a gotcha they would otherwise hit. Merely relevant is not enough. Lead each expansion with why it matters, and if nothing would be lost by cutting it, cut it.

**Brevity governs the output, not the thinking.** Reason as long as the problem needs. The discipline applies to what reaches the reader, never to how much analysis happens first. A short answer built on shallow work is worse than a long one.

**Silent omission is the worst failure.** The failure to fear is not "too long," it's the reader leaving without what mattered. Any fact that would change the reader's decision stays in, no matter how short the reply. Compression that drops a blocker, a risk, or a real status is a failure of the edit, not a success of it.

## Quick checks

**Run `scripts/prose-scan.py <file>` first, and run it rather than reading it — `--help` prints the usage and every flag, and the source is about 14,000 tokens that say the same thing.** It does every mechanical pass exactly and in about a second: dash density against the per-1,000 cap with numeric ranges and markdown rules exempted, vocabulary hits read live from `references/vocabulary.md` with their sense gates flagged, paragraph density and co-occurrence, chatbot artifacts and leaked tokens, invisible characters and homoglyphs, Title Case headings, and sentence and paragraph uniformity. It reports counts and never a score, and it skips and counts anything that sits inside a quoted example, including single-quoted ones. Add `--plain-text` for a target where nothing auto-curls (code comments, commit messages) to also flag curly quotes; in prose they are the editor's default and mean nothing. `--compare original rewrite` reports every number, year, citation and name the rewrite ADDED, every one it DROPPED, a standard or algorithm it names that the source did not (`SOC 2`, `AES-256`), a name coined from source words that never appeared as that phrase, and how much of the source survived the edit; zero findings is the only acceptable result. It also warns where every token survived and the meaning moved anyway: two facts that traded neighbors, a term now sitting beside a different number, a hedge or an obligation that changed class, a caveat whose sentence mostly disappeared. Those are warnings, not failures, because a rewrite can move a clause for good reasons; read them, do not gate on them. Specifics inside a bracketed flag are listed on an `[IN-FLAG]` line and do not count as added, because a flag asks the author for a value rather than asserting one — read that line anyway, since a fact stated inside brackets is still a fact stated.

Three passes stay manual because they need a reader, and they run in every mode:

- **Fabrication:** any fact, number, name, or citation in the output that was not in the input or from the author. Remove or flag. `--compare` catches most of it; this catches the rest.
- **Signature test:** anything kept only because the author wrote it, rather than because it is theirs? Cut it.
- **Silent omission:** would the reader act wrongly without something that was cut? Put it back.

Then ask, reading the draft fresh: what makes this look obviously AI-generated? Fix whatever the answer is. The full checklist is [references/preflight.md](references/preflight.md), authoritative for every rewrite and edit.

## Severity

When auditing or triaging, group findings by priority instead of scoring:

- **P0, credibility killers.** Artifacts (chatbot phrases, leaked tokens, placeholders, cutoff disclaimers), vague attributions without sources, significance inflation on routine events. Fix immediately; a single P0 can discredit a whole piece.
- **P1, obvious AI smell.** Tier 1 vocabulary, template phrases, "let's" openers, synonym cycling, formulaic openings, bold overuse, em-dash frequency, hedge stacks, bare-noun bullet lists, generic future-narrative closers. Fix before publishing.
- **P2, stylistic polish.** Generic conclusions, compulsive triads, uniform paragraph length, copula avoidance, "Moreover/Furthermore" transitions. Fix when time allows.

Quick pass = P0 + P1. Full audit = all three.

**When to rewrite from scratch instead of patching:** 5+ vocabulary hits across categories, 3+ distinct pattern categories, and uniform rhythm means the structure itself is AI-generated. State the core point in one sentence and rebuild from there. Lightly-edited slop is still slop.

## Self-reference escape hatch

When writing *about* AI patterns, quoted examples are exempt. Only flag patterns in the author's own prose, never in cited examples of bad writing, quoted material, or code blocks.

## Prose inside a page

A published page, artifact, slide deck or component file is prose wrapped in machinery. Edit the
prose. Leave the machinery: tags, attributes, class names, IDs, `style` and `script` blocks, data
attributes, template placeholders, and anything a build step reads. Rule 2 already forbids
touching code; this says where the boundary runs when the two share a file.

The prose is the part a person reads: headings, body copy, list items, button and link text, form
labels, empty states, error messages, alt text, captions, and the page title. Every rule above
applies to it, voice and the no-fabrication constraint included.

Three things behave differently at this size.

- **A string can appear twice, or be matched by code.** Rewriting it fixes one place and breaks
  another. Flag those rather than editing them, the same way quoted material is flagged.
- **Rate-based checks stop meaning anything.** The dash cap is per 1,000 words, and a page may hold
  eighty. One dash in a hero heading reads as 12 per 1,000 and says nothing. Count instances and
  judge them; do not report a rate off a sample this small.
**Prove it afterward.** Copy the file before editing, then run
`scripts/markup-diff.py <before> <after>`. It compares tags, attributes, and the exact
contents of `script`, `style`, `pre` and `code`, and fails on any change to them, so
"I only touched the copy" becomes a checked claim rather than an intention. It also
catches the partial edit above: a string that appeared twice and now appears once.
Attributes a person reads (`alt`, `title`, `placeholder`, `aria-label`) count as copy and
may change, provided their visible twin changes with them.

- **Brevity is the format, not a tell.** A button without a subject is not a fragment problem, and
  a two-word empty state is not throat-clearing. The length rules in item 13 assume paragraphs.

## Output formats

**Rewrite mode:** (1) issues found, quoting the offending text; (2) the rewritten version, preserving structure, intent, and all technical specifics; (3) brief summary of meaningful changes, saying why if you reorganized the piece's structure; (4) second-pass audit: re-read your own rewrite, fix any surviving tells, note what the second pass caught. If clean, say so.

**Detect mode:** (1) issues grouped by P0/P1/P2 with quoted text; (2) assessment of which flags are clear problems vs. possibly intentional and effective. If the text is clean, say so plainly.

**Edit mode:** (1) list of edits with location and before → after, only the spans touched; (2) verification that flags are resolved, noting anything deliberately left alone.

If the original is already strong, say so and cut only what's needed. Don't manufacture findings. Returned unchanged is a complete result in any mode.

## Reference files

- [references/vocabulary.md](references/vocabulary.md): Tiered word tables (Tier 1/2/3), template phrases, transition phrases. Read when auditing or when vocabulary is in question.
- [references/phrases.md](references/phrases.md): Throat-clearing, emphasis crutches, business jargon, meta-commentary, vague declaratives.
- [references/structures.md](references/structures.md): Structural patterns (binary contrasts, negative listings, fragmentation, false agency, rhythm problems) plus word-choice, tone, formatting, and composition tropes with examples.
- [references/patterns.md](references/patterns.md): Artifacts and fingerprints, whole-text tests (rhythm, density, reshuffle immunity), and the newer pattern catalog. Read for full audits and for social or published content.
- [references/preflight.md](references/preflight.md): The authoritative pass/fail checklist. Run on every rewrite and edit before delivery.
- [references/maintenance.md](references/maintenance.md): How to update this skill. Read ONLY when asked to update, refresh, or check its sources, never during writing or editing work.
- [references/examples.md](references/examples.md): Before/after transformations.

## Examples

Worked before/after pairs live in [references/examples.md](references/examples.md), covering
scientific and grant writing, blog prose, and general-purpose copy. Read one before a first pass
to calibrate how far to edit. Every After adds no fact the Before did not contain; where the
Before was vague and a specific was needed, the After flags it rather than inventing it, which is
the rule demonstrated rather than stated.
