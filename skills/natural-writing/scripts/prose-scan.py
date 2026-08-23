#!/usr/bin/env python3
"""Mechanical passes over prose. Counts, never verdicts.

Every check here is one a model does badly and a computer does exactly: counting
dashes across 2,000 words, seeing a zero-width space, working out whether a word
list crosses a density threshold. Run this first so judgment is spent on the
things that need judgment.

It reports findings and never a score. Scoring authorship is a claim this skill
refuses to make; counting characters is not.

    python3 prose-scan.py draft.md
    python3 prose-scan.py --compare original.md rewrite.md   # specifics the rewrite added
    python3 prose-scan.py --demo        # self-check on known input
"""
import difflib, os, pathlib, re, sys, unicodedata, statistics as st

# --- Vocabulary tiers -----------------------------------------------------------
# The catalog lives in references/vocabulary.md. This script READS it rather
# than carrying a copy, because a copy drifted within a day of being written:
# 'robust' was Tier 1 in the catalog and Tier 2 here. The lists below are a
# fallback for running the script outside the skill, and the report says which
# source was used so a drifted fallback cannot pass as the catalog.
_FALLBACK_TIER1 = {
    "delve": None, "tapestry": "figurative", "testament to": None, "underscore": "verb",
    "leverage": "verb", "seamless": None, "multifaceted": None, "realm": None,
    "interplay": None, "pivotal": None, "landscape": "metaphor", "harness": "metaphor",
    "it's worth noting": None, "it is worth noting": None, "in today's": None,
}
_FALLBACK_TIER2 = ["crucial", "foster", "enhance", "showcase", "notably",
                   "moreover", "furthermore", "garner", "bolster", "supercharge"]
_FALLBACK_TIER3 = ["key", "important", "significant", "various", "effective",
                   "valuable", "powerful", "essential", "comprehensive"]

# How thin the fallback is, computed rather than asserted: it has drifted to 34 terms
# against the catalog's 121, and a silent 72% miss reported in the same format as a full
# scan is the failure this whole repo keeps finding. Named in the source line instead.
_FB_N = len(_FALLBACK_TIER1) + len(_FALLBACK_TIER2) + len(_FALLBACK_TIER3)

def load_vocabulary():
    """Parse references/vocabulary.md into (tier1 dict, tier2 list, tier3 list, source)."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "references", "vocabulary.md")
    if not os.path.exists(path):
        return (_FALLBACK_TIER1, _FALLBACK_TIER2, _FALLBACK_TIER3,
                f"!! BUILT-IN FALLBACK: vocabulary.md not found, so this scan covers "
                f"{_FB_N} terms instead of the catalog's full set. Findings below are "
                f"incomplete; fix the path rather than trusting a clean result.")
    t1, t2, t3, tier = {}, [], [], None
    lines = open(path, encoding="utf-8").read().splitlines()
    for i, line in enumerate(lines):
        h = re.match(r"^##+\s*(.+?)\s*$", line)
        if h:
            # ANY heading closes the current tier. Matching only "Tier N" left the
            # parser in Tier 3 through "Abstract metaphor nouns", "Template phrases"
            # and "Transition phrases", loading all of them at the Tier 3 threshold.
            m = re.match(r"^Tier\s*([123])\b(?!\s*phrases)", h.group(1), re.I)
            tier = int(m.group(1)) if m else None
            continue
        m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if not m or tier is None: continue
        # A row whose next line is the |---|---| separator is the header row,
        # whatever it is called. Name-matching headers missed "Reach for".
        if i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?\s*$", lines[i + 1]): continue
        term = m.group(1).strip().strip("`*")
        if not term or set(term) <= set("-: "): continue
        sense = None
        s = re.match(r"^(.*?)\s*\((?:as )?(\w[\w ]*)\)\s*$", term)
        if s:
            term, sense = s.group(1).strip(), s.group(2).strip()
        term = term.lower()
        # Rows list variants joined by "/" ("delve / delve into"). Left unsplit they
        # compile to a literal that matches nothing, so those terms were dead.
        variants = [v.strip() for v in term.split("/") if v.strip()]
        # A one-word tail after a multi-word head belongs to the phrase:
        # "emerging sector / space / category" means "emerging space", never bare
        # "space", which flagged ordinary design prose.
        head = variants[0].split()
        if len(head) > 1:
            variants = [variants[0]] + [" ".join(head[:-1] + [v]) if len(v.split()) == 1 else v
                                        for v in variants[1:]]
        # The matcher appends \w*, so "meticulous" already covers "meticulously".
        kept = []
        for v in sorted(variants, key=len):
            if not any(v.startswith(k) for k in kept): kept.append(v)
        for v in kept:
            if tier == 1: t1[v] = sense
            elif tier == 2: t2.append(v)
            elif tier == 3: t3.append(v)
    if not t1:
        return (_FALLBACK_TIER1, _FALLBACK_TIER2, _FALLBACK_TIER3,
                f"!! BUILT-IN FALLBACK: vocabulary.md parsed empty, so this scan covers "
                f"{_FB_N} terms instead of the catalog's full set. Findings below are "
                f"incomplete; fix the file rather than trusting a clean result.")
    # A term the catalog lists in more than one tier belongs to the strictest one.
    # Keeping it in both double-counts it everywhere downstream.
    t2 = [w for w in dict.fromkeys(t2) if w not in t1]
    t3 = [w for w in dict.fromkeys(t3) if w not in t1 and w not in t2]
    return t1, t2, t3, f"references/vocabulary.md ({len(t1)}/{len(t2)}/{len(t3)} terms)"

TIER1, TIER2, TIER3, VOCAB_SOURCE = load_vocabulary()

def load_phrases():
    """Parse references/phrases.md into {category: (patterns, flat)}.

    Same arrangement as vocabulary.md and for the same reason: the catalog is the file, not
    this script, so adding a phrase there is the whole edit. Until 2026-08-22 nothing read
    this file at all — 15 categories of habit that existed only as judgment while the
    single-word tells were counted. That asymmetry got sharper the day --voice started
    COUNTING the devices a sample demonstrates, because a counted rule beats an uncounted
    one no matter which is more important.

    `flat` comes from the category's own instruction line. A section that says "Remove
    these" / "Delete them" / "Cut them" is enforceable; Adverbs says the test is deletion
    and that a hedge marking real uncertainty is information, so it is reported to be read
    rather than counted against the text.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "references", "phrases.md")
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError:
        return {}, "phrases.md not found"
    cats, cat, instr, items = {}, None, "", []
    def flush():
        if cat and items:
            # Flat by default: the file is titled "Phrases to Remove or Replace" and every
            # category states an imperative. The exception is a category that writes its own
            # test — Adverbs says read the sentence without it, and that a hedge marking real
            # uncertainty is information whose removal would fabricate confidence. Detect the
            # exception, not the rule, or a category phrased "Kill these" reads as optional.
            flat = not re.search(r"the test is|rather than a blanket|what survives|"
                                 r"same test|if nothing is lost|is information", instr, re.I)
            cats[cat] = (items[:], flat)
    for line in raw.split("\n"):
        if line.startswith("## "):
            flush(); cat, instr, items = line[3:].strip(), "", []
        elif line.startswith("- ") and cat:
            m = re.match(r'- "(.+?)"\s*$', line)
            if m:
                lit = m.group(1)
                # "[X]" in the catalog stands for any word the writer drops in.
                pat = re.escape(lit).replace(r"\[X\]", r"\S+").replace(r"\[x\]", r"\S+")
                pat = re.sub(r"\\\[\\w[^\]]*\\\]", r"\\S+", pat)
                items.append((lit, pat))
        elif cat and line.strip() and not line.startswith("#"):
            instr += " " + line.strip()
    flush()
    n = sum(len(v[0]) for v in cats.values())
    return cats, f"references/phrases.md ({len(cats)} categories, {n} phrases)"


PHRASES, PHRASE_SOURCE = load_phrases()
# Categories whose members are the author's HABIT, never their voice. --voice must never
# report one of these as a trait worth preserving: that is the door through which a sloppy
# sample would license a sloppy rewrite.
HABIT_CATEGORIES = set(PHRASES)


# Curly quotes only matter where nothing auto-curls; see patterns.md.
PLAIN_TEXT = "--plain-text" in sys.argv

ARTIFACTS = [
    (r"\b(great|excellent|good) question\b", "sycophantic opener"),
    (r"\bI hope this helps\b", "chatbot closer"),
    (r"\b(certainly|of course)[!,]", "chatbot affirmation"),
    (r"as an AI\b", "assistant disclaimer"),
    (r"\bmy (knowledge |training )?cut[- ]?off\b", "cutoff disclaimer"),
    (r"as of my last update", "cutoff disclaimer"),
    (r"citeturn\d+\w*", "leaked citation token"),
    # patterns.md lists these as P0 credibility killers; the scanner claimed to
    # catch them and did not, so a document full of them reported clean.
    (r"contentReference\[oaicite:\d+\]\{index=\d+\}", "leaked citation token"),
    (r"\boai_citation\b", "leaked citation token"),
    (r"\[attached_file:\d+\]", "leaked attachment token"),
    (r"utm_source=(chatgpt|openai|claude|perplexity)|referrer=grok\.com", "AI-tool URL parameter"),
    (r"\[(TODO|PLACEHOLDER|INSERT[^\]]*|YOUR\s+[^\]]+)\]", "unfilled placeholder"),
    (r"\b(19|20)\d{2}-XX-XX\b", "unfilled date placeholder"),
    (r"<!--\s*(TODO|PLACEHOLDER|INSERT|ADD)\b.*?-->", "unfilled HTML placeholder"),
    (r"let me think step by step", "reasoning-chain leak"),
]
INVISIBLE = {"​": "zero-width space", "‌": "zero-width non-joiner",
             "‍": "zero-width joiner", "­": "soft hyphen",
             "﻿": "byte-order mark", "⁠": "word joiner"}
# Cyrillic/Greek letters that render as Latin
HOMOGLYPH = re.compile(r"[Ѐ-ӿͰ-Ͽ]")

WORD = re.compile(r"\b[\w'-]+\b")
def words(t): return WORD.findall(t)
def paras(t): return [p for p in re.split(r"\n\s*\n", t) if p.strip()]

def sentences(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"^\s*[-*+#>|].*$", " ", t, flags=re.M)      # lists, headings, tables
    return [s for s in re.split(r"(?<=[.!?])\s+", t) if len(words(s)) > 2]

def strip_code(t):
    t = re.sub(r"\A---\n.*?\n---\n", " ", t, flags=re.S)   # YAML frontmatter, whose --- is not a dash
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"<(pre|code)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"`[^`]*`", " ", t)
    # Markdown's other code form: a run of 4-space-indented lines after a blank
    # one. Pasted tool output lives here, and the skill exempts code categorically,
    # so leaving it in charged the writer for a chatbot's own words.
    out, prev_blank = [], True
    for line in t.split("\n"):
        if prev_blank and re.match(r"^(?: {4}|\t)\S", line):
            out.append(" ")
        else:
            out.append(line)
            prev_blank = not line.strip()
    return "\n".join(out)

def find(text):
    out, prose = [], strip_code(text)
    wc = len(words(prose))

    if wc < 40:
        out.append(("FLOOR", f"{wc} words: under the ~40-word floor, report that the sample "
                             "is too short rather than returning a verdict"))
        return out, wc

    # dashes, exempting numeric ranges
    # (?<!-)--(?!-) so a --- rule or a longer run is not counted as two dashes
    dash = [m for m in re.finditer(r"—|(?<!-)--(?!-)|(?<![\d\s])–|–(?!\d)", prose)]
    per1k = 1000 * len(dash) / wc
    if per1k > 1:
        out.append(("DASH", f"{len(dash)} in {wc} words = {per1k:.1f} per 1,000 (cap is 1). "
                            "A voice sample overrides this."))

    # invisible characters and homoglyphs
    for ch, name in INVISIBLE.items():
        n = text.count(ch)
        if n:
            out.append(("INVISIBLE", f"{n}x {name} (U+{ord(ch):04X})"))
    for m in HOMOGLYPH.finditer(text):
        ctx = text[max(0, m.start()-12):m.start()+12].replace("\n", " ")
        if re.search(r"[a-zA-Z]", ctx):     # only flag when embedded in Latin text
            out.append(("HOMOGLYPH", f"{unicodedata.name(m.group(), '?')} in \"{ctx.strip()}\""))
            break

    # An artifact quoted as an example is not an artifact. Skip hits that sit
    # inside quotation marks, in a table row, or in a blockquote, and say how many.
    def quoted(i):
        ls = prose.rfind("\n", 0, i) + 1; le = prose.find("\n", i)
        line = prose[ls:le if le != -1 else None]
        if line.lstrip().startswith(("|", ">", '- "', '* "', '1. "')): return True
        pos = i - ls
        # Typographic single quotes count as an example span too; the old parity
        # test saw double quotes only, so 'I hope this helps' quoted in a style
        # guide was reported as the writer's own artifact. ASCII ' stays out: it
        # is an apostrophe far more often than a quotation mark.
        for a, b in (("\u201c", "\u201d"), ("\u2018", "\u2019")):
            start = line.rfind(a, 0, pos)
            if start != -1 and line.find(b, start + 1) >= pos: return True
        before = line[:pos]
        return before.count('"') % 2 == 1
    art_skipped = 0
    for pat, label in ARTIFACTS:
        for m in re.finditer(pat, prose, re.I):
            if quoted(m.start()):
                art_skipped += 1; continue
            out.append(("ARTIFACT", f'{label}: "{m.group()[:48]}"'))
    if art_skipped:
        out.append(("SKIPPED", f"{art_skipped} artifact hits ignored because they sit inside quotes, "
                               "a table row, or a blockquote, which reads as an example"))

    # Phrase-level habit, read live from references/phrases.md. Reuses quoted() because a
    # style guide quoting "Here's the thing:" as an example is not using it.
    ph_skipped = 0
    for cat, (items, flat) in PHRASES.items():
        hits = []
        for lit, pat in items:
            for m in re.finditer(pat, prose, re.I):
                if quoted(m.start()):
                    ph_skipped += 1; continue
                hits.append(lit)
        if not hits:
            continue
        seen = list(dict.fromkeys(hits))
        label = "PHRASE" if flat else "PHRASE?"
        note = "" if flat else " — this category sets its own test; read them, do not cut on sight"
        out.append((label, f'{cat}: {len(hits)} hit(s), {", ".join(repr(h) for h in seen[:6])}'
                           f'{"..." if len(seen) > 6 else ""}{note}'))
    if ph_skipped:
        out.append(("SKIPPED", f"{ph_skipped} phrase hits ignored as quoted examples"))

    low = prose.lower()
    # A line listing four or more flagged words is a catalog of them, not prose
    # written with them. Text about AI writing quotes its own examples constantly,
    # and the skill exempts quoted examples, so the scan must too.
    _ALL = list(dict.fromkeys(list(TIER1) + TIER2 + TIER3))
    def is_catalogue(line):
        n = sum(1 for w in _ALL if re.search(rf"\b{re.escape(w)}", line, re.I))
        return n >= 4
    lines = prose.split("\n")
    starts, off = [], 0
    for ln in lines:
        starts.append((off, off + len(ln), is_catalogue(ln))); off += len(ln) + 1
    def catalogued(i):
        return any(a <= i <= b and c for a, b, c in starts)

    skipped = 0
    for w, sense in TIER1.items():
        for m in re.finditer(rf"\b{re.escape(w)}\w*", low):
            if catalogued(m.start()):
                skipped += 1
                continue
            note = f" — gated to the {sense} sense, check this one" if sense else ""
            out.append(("TIER1", f'"{prose[m.start():m.end()]}"{note}'))
    if skipped:
        out.append(("SKIPPED", f"{skipped} vocabulary hits ignored on lines that list four or "
                               "more flagged words, which reads as a catalog rather than prose"))

    for p in paras(prose):
        body = "\n".join(l for l in p.split("\n") if not is_catalogue(l))
        hits = [w for w in TIER2 if re.search(rf"\b{w}\w*", body, re.I)]
        if len(hits) >= 2:
            out.append(("TIER2", f"{len(hits)} in one paragraph: {', '.join(hits)}"))

    t3 = [w for w in TIER3 if re.search(rf"\b{w}\b", low)]
    t3n = sum(len(re.findall(rf"\b{w}\b", low)) for w in TIER3)
    if wc and 100 * t3n / wc >= 3:
        out.append(("TIER3", f"{t3n} hits = {100*t3n/wc:.1f}% of text (threshold 3%): {', '.join(t3)}"))
    else:
        for p in paras(prose):
            p = "\n".join(l for l in p.split("\n") if not is_catalogue(l))
            n3 = sum(len(re.findall(rf"\b{w}\b", p, re.I)) for w in TIER3)
            if n3 >= 2 and any(re.search(rf"\b{w}\b", p, re.I) for w in list(TIER1) + TIER2):
                out.append(("TIER3", f"{n3} Tier 3 words in a paragraph that also carries a "
                                     "Tier 1 or 2 hit (co-occurrence gate)"))
                break

    # formatting
    for m in re.finditer(r"^#{1,6}\s+(.*)$", text, re.M):
        h = m.group(1)
        if re.search(r"[\U0001F300-\U0001FAFF←-⇿☀-➿]", h):
            out.append(("FORMAT", f'emoji or arrow in heading: "{h[:44]}"'))
        ws = [x for x in h.split() if x[:1].isalpha()]
        if len(ws) >= 4 and sum(x[:1].isupper() for x in ws) / len(ws) > 0.8:
            out.append(("FORMAT", f'heading looks Title Case: "{h[:44]}"'))
    n_bold = len(re.findall(r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:—-]", text, re.M))
    if n_bold >= 3:
        out.append(("FORMAT", f"{n_bold} bullets open with a bold label plus a colon; "
                              "check they are not restating the line"))
    tags = re.findall(r"(?<!\w)#[a-z]\w+", text)
    if len(tags) >= 6:
        out.append(("FORMAT", f"{len(tags)} hashtags"))
    # patterns.md: curly quotes are meaningful only in plain-text targets, since
    # Word, Docs, macOS and iOS all curl by default. Flagging them everywhere made
    # correctly typeset publication prose fail the mechanical pass, so this is
    # opt-in with --plain-text (code comments, commit messages, anything unstyled).
    if PLAIN_TEXT and re.search(r"[‘’“”]", prose):
        out.append(("QUOTES", "curly quotes in a plain-text target; straight quotes read as typed"))

    # rhythm, reported not scored
    sl = [len(words(s)) for s in sentences(prose)]
    if len(sl) >= 6:
        cv = st.pstdev(sl) / st.mean(sl) if st.mean(sl) else 0
        if cv < 0.35:
            out.append(("RHYTHM", f"sentence lengths are uniform (mean {st.mean(sl):.0f} words, "
                                  f"variation {cv:.2f}). Not a defect on its own; look at whether "
                                  "every sentence has the same shape."))
    pl = [len(words(p)) for p in paras(prose)]
    if len(pl) >= 5 and st.pstdev(pl) / max(1, st.mean(pl)) < 0.3:
        out.append(("RHYTHM", f"paragraphs are near-identical in length (mean {st.mean(pl):.0f} words)"))
    return out, wc

NUM   = re.compile(r"(?<![\w.])\$?\d[\d,]*(?:\.\d+)?\s?(?:%|percent|ms|s|x|k|m|bn|million|billion)?(?![\w])", re.I)
# The "1." of a numbered list is a marker, not a measurement. A rewrite that put its
# reasons in a numbered list was charged with inventing the numbers 1, 2 and 3, so
# --compare could not be passed by any structured rewrite (#43). This matches only the
# marker at the head of a line, so "3 nodes" and "2 seconds" in running prose are still
# figures. One or two digits only, so a line opening "2019. That was the year..." keeps
# its year. Leading [-*+>] and ** cover a nested or bolded item.
LIST_ORDINAL = re.compile(r"(?m)^[ \t]*(?:[-*+>\u2022][ \t]*)*[*_]{0,2}(\d{1,2})[.)](?=[ \t*_]|$)")
MONTH = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December|Q[1-4])\b")
YEAR  = re.compile(r"\b(1[89]\d\d|20\d\d)\b")
CITE  = re.compile(r"\(([A-Z][\w&.\- ]+?),?\s+(?:19|20)\d\d[a-z]?\)")
# A square-bracketed span is a flag or a placeholder, not a claim: "[N] ms",
# "[12] months", "[needs a number: how many customers?]". SKILL.md prescribes exactly
# this format for marking a specific the source does not contain, so the digits and
# words inside one are the opposite of a fabrication, and the scanner used to report
# its own house style as invented. Markdown link text "[Redis](...)" is not a flag,
# hence the lookahead; the trailing/leading digit class keeps "[N]/5" whole.
# The trailing "." only belongs to a decimal ("[N].5"). Letting it match anything ate
# the full stop after a flag, and "Shipped `[ ]`. Supports `[ ]` channels" collapsed
# into one sentence whose "Shipped Supports" was then reported as an invented name.
FLAG = re.compile(r"[\d/x\u00d7.,%$-]*\[[^\]\n]{0,120}\](?!\()(?:\.\d|[\d/x\u00d7,%-])*")
# A flag written in backticks is still a flag. strip_code() removes inline code
# spans before the fact scan, so a rewrite that marked all 68 of its gaps as `[ ]`
# -- the form SKILL.md explicitly allows, since "the form is yours to choose" --
# had every flag deleted before FLAG ever saw it and reported 0 flags (#43).
# Unwrap the backticks around a bracketed span first. [^\S\n] keeps this from
# eating a fenced block's own backticks, so fenced code is still exempt.
BACKTICKED_FLAG = re.compile(r"`([^\S\n]*\[[^\]\n]{0,120}\][^\S\n]*)`")
# Digits inside a standard's name are part of the name, not a measurement: SOC 2,
# AES-256, ISO 27001, TLS 1.3. Reporting them as invented numbers buried the thing
# that actually matters, which is that the rewrite asserted a compliance or
# configuration property (SKILL.md's asserted-properties rule). All-caps acronyms
# never matched PROPER, so these were invisible to the name check too.
STD = re.compile(r"\b[A-Z]{2,}[ -]?\d[\d.A-Za-z-]*")
# The other half of a standard's name: a designator word plus a roman numeral or
# figure. "SOC 2 Type II" was caught as "SOC 2" and then "Type" fell through to the
# name check as an invented entity (#32). Type II is a compliance property in its
# own right, so it belongs in the class that already reports asserted properties,
# not in the class that reports fabricated entities.
DESIG = re.compile(r"\b(?:Type|Class|Level|Tier|Phase|Stage|Grade|Part|Rev|Mark|Category)"
                   r"[ -](?:[IVX]{1,4}|\d+[A-Za-z]?)\b")
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
# [ \t]+ and not \s+ between the tokens: a name does not span a line break. A heading
# sits on its own line, so "## Investigation" plus a body opening "We shipped it" was
# read as the single name "Investigation We" (#46) -- a phrase that exists in neither
# line. Keeping the match on one line also stops the heading exemption below from
# reaching past the heading into the first word of the paragraph under it.
PROPER = re.compile(r"\b(?:[A-Z][a-z]+(?:[-'][A-Z]?[a-z]+)?)(?:[ \t]+(?:[A-Z][a-z]+|&|and|of|de|van|von)){0,3}\b")
# A markdown heading labels a section; it is the document's own furniture, not a claim
# about the world. A rewrite that reorganized into "## Investigation" and "## Remediation"
# was charged with inventing both words (#46), so no restructured rewrite could reach the
# zero findings --compare promises. Same class as LIST_ORDINAL: a check firing on markdown
# structure instead of on content.
HEADING = re.compile(r"(?m)^[ \t]{0,3}#{1,6}[ \t]+.*")
# What separates a section label from a name, since title case tells you nothing: the word
# is ordinary section vocabulary AND the body never uses it mid-sentence as a proper noun.
# Both halves are load-bearing. Without the first, "## Introducing Vault" would be exempt
# and a fabricated product would hide in a heading. Without the second, a rewrite could
# title a section "## Region" and then assert "we moved the fleet to Region" for free.
# The exemption is per-word, so only the structural words drop out of a heading and
# anything else on the line is still reported.
# ponytail: a hand-kept list, like _COMMON_NOUNS below. Extend it when a real heading
# gets flagged; do not put product-shaped words (Finance, Legal, Security) in it.
_SECTION_WORDS = set("""
investigation remediation mitigation resolution recommendation recommendations
cause causes root introduction conclusion conclusions method methods methodology
approach analysis discussion proposal decision decisions alternatives tradeoffs
detection prevention aftermath rollout rollback appendix glossary references
takeaways lessons learned questions what why how who where when recap agenda
abstract purpose objective objectives assumptions constraints
""".split())
_COMMON_CAPS = set("The A An In On At For To Of And But Or If When While Before After "
                   "This That These Those It Its We You They He She I My Our Your Their "
                   "Example Fix Note Step Tier "
                   # verbs and adverbs that open a sentence and read as names to a regex
                   "Is Are Was Were Be Been Being Do Does Did Have Has Had Can Could "
                   "Will Would Should May Might Must Let Here There Now Then Yes No Not "
                   "So Because Since Although Though However Instead Also Still Just".split())
# Words in _COMMON_CAPS are never names. These are the weaker case: ordinary English
# that a name check cannot tell from a product ("Type", "Audit", "Channel", "Median").
# A capitalized token drawn only from this list is reported as POSSIBLE-NEW-TERM, a
# warning, instead of NEW-NAME, a hard failure on what is usually not a fact at all.
# ponytail: a hand-kept list, not a dictionary. It shrinks the false-positive class it
# names and nothing else; swap in a real lexicon if the misses start to matter.
_COMMON_NOUNS = set("""
type types class classes level levels tier tiers phase phases stage stages grade part parts
section sections audit audits build builds channel channels median mean average owner owners
region regions sev severity step steps note notes item items issue issues risk risks blocker
caveat summary overview background context result results finding findings impact outcome
outcomes goal goals scope timeline deadline milestone team teams user users customer customers
client clients member members service services system systems server servers database table
tables index indexes queue queues cache job jobs task tasks process processes request requests
response responses error errors report reports review reviews change changes update updates
release releases version versions policy policies rule rules limit limits target targets metric
metrics number numbers count counts cost costs price time date day week month quarter year hour
minute second status state open closed done pending next previous first third final draft title
name named names label labels value values field fields key keys column columns row rows page pages
file files folder line lines size length width height plan plans design designs test tests check
checks fix fixes bug bugs feature features mode option options config default defaults setting
settings input output none total other others north south east west
""".split())

def facts(text):
    """Specifics a rewrite is not allowed to introduce: numbers, years, citations,
    standard names, and capitalized names that are not sentence-initial function words.

    Bracketed flags are pulled out first and extracted separately into "flagged".
    A flag asks the author for a value instead of asserting one, so it is exempt --
    but the exemption is counted and reported, never silent."""
    t = strip_code(BACKTICKED_FLAG.sub(r"\1", text))
    f = _extract(FLAG.sub(" ", t))
    f["flagged"] = _extract(" ".join(FLAG.findall(t)))
    return f

def _extract(t):
    # Standard names first, so their digits are not also collected as figures.
    stds, spans = set(), []
    for rx in (STD, DESIG):
        for m in rx.finditer(t):
            name = m.group().rstrip(".,;:-")
            stds.add(name); spans.append((m.start(), m.start() + len(name)))
    def in_std(a, b): return any(a < y and x < b for x, y in spans)
    # Kept apart from the standard-name spans above: an ordinal marker exempts only the
    # digit, never a capitalized word that follows it, which is still a name to check.
    ord_spans = [(m.start(1), m.end(1)) for m in LIST_ORDINAL.finditer(t)]
    head_spans = [(m.start(), m.end()) for m in HEADING.finditer(t)]
    # Trailing punctuation made "2019," a different fact from "2019" and reported
    # an unchanged year as newly invented.
    nums = {m.group().strip().rstrip(".,;:)]}") for m in NUM.finditer(t)
            if not any(a <= m.start() < b for a, b in spans + ord_spans)}
    nums |= {m.group() for m in MONTH.finditer(t)}
    years = set(YEAR.findall(t))
    cites = {c.strip() for c in CITE.findall(t)}
    # A capitalized word is a name only if it appears capitalized somewhere that is
    # NOT the start of a sentence, line, list item or table cell. "Encryption at rest"
    # and "Median time to resolution" open sentences; "Redis" and "Postgres" do not.
    # Position-by-position exemptions kept missing cases (after **bold.**, after a
    # semicolon), so this asks the whole document instead.
    # The opening bracket matters as much as the closing one: "[Needs a number...]"
    # and "(Redis is the cache.)" both open a sentence. Allowing only ) and ] promoted
    # the first word of every bracketed flag to a proper name.
    INITIAL = re.compile(r"(?:^|[.!?:;])[\s*_>#|()\[\]-]*$|\n[\s*_>#|()\[\]-]*(?:[-*+\u2022]|\d+[.)])?[\s*_]*$")
    def mid_sentence(word):
        """How often the word is capitalized somewhere that is not the start of a
        sentence, line, list item or table cell.

        Heading lines do not count. A heading is title case throughout, so every word
        after its first one looks mid-sentence to the test above and "## Root Cause"
        made Cause a name on its own evidence (#46). The question this answers is
        whether the body uses the word as a proper noun, so only the body may answer."""
        return sum(1 for mm in re.finditer(rf"\b{re.escape(word)}\b", t)
                   if not INITIAL.search(t[:mm.start()])
                   and not any(a <= mm.start() < b for a, b in head_spans))
    names, maybe = set(), set()
    for m in PROPER.finditer(t):
        s = m.group().strip()
        # A phrase that starts with a function word ("The Build") is that word plus a
        # name, and a phrase that ends with a connector ("Audit and") is a name plus
        # the connector. Trimming both stops PROPER from manufacturing multi-token
        # "names" out of ordinary sentences.
        parts = s.split()
        while parts and (parts[0] in _COMMON_CAPS or parts[0].lower() in
                         ("and", "of", "de", "van", "von", "&")): parts.pop(0)
        while parts and parts[-1].lower() in ("and", "of", "de", "van", "von", "&"): parts.pop()
        if not parts: continue
        # A heading's structural words are a section label, not an invented entity
        # (see HEADING above). Per-word, so "## Introducing Vault" keeps Vault, and
        # only while the body does not use the word mid-sentence as a proper noun.
        if any(a <= m.start() < b for a, b in head_spans):
            parts = [w for w in parts if mid_sentence(w) or not (
                w in _COMMON_CAPS or w.lower() in _SECTION_WORDS
                or w.lower() in _COMMON_NOUNS)]
            if not parts: continue
        s = " ".join(parts)
        if in_std(m.start(), m.end()): continue   # "Type" inside "Type II"
        # A month is already a fact in the numbers class. Reporting "February" a
        # second time as an invented entity is the same defect as "Type": a
        # capitalized common word charged as a fabricated name.
        if len(parts) == 1 and MONTH.fullmatch(s): continue
        if len(parts) == 1 and not mid_sentence(s): continue
        # Confidence, not exemption. An unknown capitalized word is a name; a phrase
        # built only from ordinary English is a name only if the writer keeps using
        # it mid-sentence, which is what distinguishes a product from a common noun.
        unknown = [w for w in parts if w[:1].isupper()
                   and w.lower() not in _COMMON_NOUNS and w not in _COMMON_CAPS]
        (names if unknown else maybe).add(s)
    return {"numbers": nums, "years": years, "citations": cites, "names": names,
            "possible": maybe, "standards": stds, "urls": {u.rstrip(".,;:!?") for u in URL.findall(t)}}

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen twenty").split()
_TENS = {30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
         80: "eighty", 90: "ninety", 100: "hundred", 1000: "thousand"}

def spelled(fact):
    """Word spellings of a numeric fact, so a rewrite that says "twelve nodes" is not
    reported as having dropped "12"."""
    m = re.match(r"^\$?([\d,]+)(?:\.\d+)?\s*(million|billion|thousand)?$", fact.strip(), re.I)
    if not m: return set()
    try: n = int(m.group(1).replace(",", ""))
    except ValueError: return set()
    scale = (" " + m.group(2).lower()) if m.group(2) else ""
    out = set()
    if n < len(_ONES): out.add(_ONES[n] + scale)
    if n in _TENS: out.add(_TENS[n] + scale)
    if n == 1000: out.update({"a thousand", "one thousand"})
    return out

# --- Relationship drift ---------------------------------------------------------
# A rewrite can keep every number, name and citation and still change what the text
# means: swap two versions, move a "not", turn "may" into "will". The fact classes
# above are set comparisons and cannot see any of it. These checks look at what sits
# NEXT TO what, using token windows rather than any attempt at parsing.
#
# Everything here reports as a warning and none of it moves the exit code. The
# grader audit found 13 of 29 confident checks wrong; a window heuristic that fires
# confidently and wrongly would be worse than one that hedges. Promote a class to a
# hard failure when fixtures have earned it, not before.
_STOP = set("""a an the and or but if then than that this these those there here it its it's is
are was were be been being am do does did done have has had having will would shall should can
could may might must of in on at to for from by with without into over under about as so such
we you they he she i me my our your their them his her not no nor only just also still yet
which who whom whose what when where why how all any both each few more most other some very
one two too own same s t don now up down out off again further once because while during before
after above below between through against upon per said says like get got make made take took""".split())
_NEG  = set("not no never cannot can't didn't doesn't don't won't wasn't isn't without none nor "
            "failed fails failing lacked lacks unable neither".split())
_HEDGE = set("may might could maybe perhaps possibly roughly about approximately around nearly "
             "almost some usually often typically generally likely probably proposed draft "
             "tentative estimated planned expected should aim aims hope hopes intend intends".split())
_HARD = set("will must shall always every all guarantee guaranteed guarantees ensure ensures "
            "committed commits commitment required requires confirmed final definitely certainly "
            "never permanently indefinitely".split())
_MARKERS = _NEG | _HEDGE | _HARD
_LIMIT = _NEG | {"however", "but", "although", "though", "caveat", "blocker", "blocked",
                 "risk", "unresolved", "outstanding", "pending", "except", "unless",
                 "only", "until", "missing", "gap", "regression", "caveats"}
_TOK = re.compile(r"[A-Za-z][\w'.-]*|\d[\w.,:%$/-]*")

def _units(text):
    """Sentence-sized token lists. Nothing here looks across a sentence boundary:
    a window that did was reporting paragraph reordering as reassigned facts."""
    t = strip_code(text)
    return [[m.group().strip(".,:;").lower() for m in _TOK.finditer(s)]
            for s in re.split(r"(?<=[.!?])\s+|\n+", t) if s.strip()]

def _cls(ms):
    return frozenset(("neg" if m in _NEG else "hedge" if m in _HEDGE else "hard") for m in ms)

def _windows(units, anchors, w=5):
    """Per term: the one anchor it sits nearest, and the certainty markers governing
    its clause. Terms with no clear nearest anchor are dropped rather than guessed.

    ponytail: O(terms x anchors) inside each sentence. Prose-sized; index the anchor
    positions if this is ever pointed at something book-length."""
    near, marks, seen = {}, {}, {}
    for toks in units:
        pos = [i for i, t in enumerate(toks) if t in anchors]
        for i, t in enumerate(toks):
            if t in _STOP or (len(t) < 3 and t not in anchors): continue
            seen[t] = seen.get(t, 0) + 1
            if t not in _MARKERS and t not in anchors:
                # Markers within arm's reach, not the whole clause. A clause-wide
                # set turned every sentence split into a certainty change, which is
                # the single most common thing an honest rewrite does.
                marks.setdefault(t, set()).add(
                    _cls({x for x in toks[max(0, i-3):i+4] if x in _MARKERS}))
            best, bd, second = None, w + 1, w + 1
            for p in pos:
                d = abs(p - i)
                if not d or d > w or toks[p] == t: continue
                if d < bd: bd, second, best = d, bd, toks[p]
                elif d < second and toks[p] != best: second = d
            # A term wedged between two anchors belongs to neither. Requiring a clear
            # winner is what separates a swap from ordinary reordering: without it,
            # shifting a clause two words reassigned every term inside it.
            if best is None or second - bd < 2: continue
            if t in near and near[t] != best: near[t] = None
            elif t not in near: near[t] = best
    return {k: v for k, v in near.items() if v}, marks, seen

def fidelity(src_text, new_text):
    """Warnings about what moved next to what. Returns [(kind, message)]."""
    su, nu = _units(src_text), _units(new_text)
    st_, nt = [t for u in su for t in u], [t for u in nu for t in u]
    shared = set(st_) & set(nt)
    sf, nf = facts(src_text), facts(new_text)
    anchors = {t for t in shared if re.search(r"\d", t)}
    # A name's own words, minus the connectors PROPER lets through: "Median and
    # Named" made "and" an anchor, and every clause in the document then hung off it.
    anchors |= {w.lower() for f in (sf, nf) for n in f["names"] for w in n.split()
                if w.lower() in shared and w.lower() not in _STOP and len(w) > 2}
    out = []
    if not anchors: return out
    s_near, s_mark, s_n = _windows(su, anchors)
    n_near, n_mark, n_n = _windows(nu, anchors)

    # 1. Which anchor a term sits beside. Reversed on both sides is a swap, which
    #    ordinary rewording almost never produces; one-way movement is looser.
    drift = {t: (s_near[t], n_near[t]) for t in set(s_near) & set(n_near)
             if s_near[t] != n_near[t] and s_near[t] in shared and n_near[t] in shared}
    swaps = sorted({tuple(sorted((a, b))) for t, (a, b) in drift.items()
                    if any(x == b and y == a for x, y in drift.values())})
    for a, b in swaps[:4]:
        moved = sorted(t for t, (x, y) in drift.items() if {x, y} == {a, b})[:6]
        out.append(("FACT-SWAP", f'"{a}" and "{b}" traded neighbors: {", ".join(moved)}. '
                                 "Every token survives; check which one the claim belongs to."))
    paired = {x for s in swaps for x in s}
    one_way = sorted(t for t, (a, b) in drift.items() if not {a, b} <= paired)[:8]
    if one_way:
        out.append(("ANCHOR-DRIFT", "terms that now sit beside a different number, version or "
                    "name: " + ", ".join(f'{t} ({s_near[t]}\u2192{n_near[t]})' for t in one_way)))

    # 2. Certainty around a claim: a lost "not", a "may" that became "will". Scoped
    #    to the words either side of the term, and only for a term used once on each
    #    side, because a repeated term sits in a different clause every time.
    #
    #    Known false positive, found within a day of shipping this by running it over a
    #    real punctuation pass: merging two sentences pulls a marker into the window
    #    without changing what it governs. "Do not delete them. Deleting loses the record"
    #    and "Do not delete them: deleting loses the record" mean the same thing, and this
    #    reports the second as drift. It stays a warning partly for that reason. Narrowing
    #    the window further would start missing the real thing it catches, so the fix is a
    #    reader, not a tighter regex.
    qual = []
    for t in sorted(set(s_mark) & set(n_mark)):
        if s_n.get(t) != 1 or n_n.get(t) != 1 or len(t) < 4: continue
        a = frozenset().union(*s_mark[t]); b = frozenset().union(*n_mark[t])
        if a == b: continue
        qual.append(f'{t} ({"/".join(sorted(a)) or "none"}\u2192{"/".join(sorted(b)) or "none"})')
    if qual:
        out.append(("QUALIFIER-DRIFT", "negation, hedge or obligation changed around: "
                    + ", ".join(qual[:8]) + (" ..." if len(qual) > 8 else "")))

    # 3. A caveat that quietly did not survive, while the headline facts did.
    low = set(nt)
    dropped = []
    for u in su:
        ws = [w for w in u if w not in _STOP and len(w) > 2]
        if len(ws) < 4 or not any(w in _LIMIT for w in u): continue
        if sum(w in low for w in ws) / len(ws) < 0.4:
            dropped.append(" ".join(ws)[:70])
    if dropped:
        out.append(("OMITTED-CAVEAT", f"{len(dropped)} source sentence(s) carrying a limit, "
                    "negation or blocker have largely no counterpart in the rewrite: "
                    + " | ".join(f'"{d}"' for d in dropped[:3])))
    return out

# Traits a writer can demonstrate and a house-style rule can quietly flatten. Each is a
# countable surface feature, because the point is to compare a rate against a rate, not to
# judge whether the rewrite "sounds like" anyone. Deliberately rule-agnostic: it knows
# nothing about which rule suppresses what, so a rule written next year still shows up here.
VOICE_TRAITS = {
    "em dash":            r"—",
    "exclamation":        r"!",
    "parenthetical aside": r"\([^)]{8,}\)",
    "contraction":        r"\b\w+['’](t|s|re|ve|ll|d|m)\b",
    "sentence-initial And/But/So": r"(?:^|[.!?]\s+|\n)(?:And|But|So|Because|Or)\b",
    "first person":       r"\b(?:I|we|my|our|me|us)\b",
    "second person":      r"\b(?:you|your|yours)\b",
    "short sentence (<5 words)": None,   # counted structurally below
    "italic span":        r"(?<!\*)\*[^*\n]+\*(?!\*)|(?<!_)_[^_\n]+_(?!_)",
    "colon pivot":        r"\w:\s+\w",
}


def _short_sentences(text):
    return sum(1 for s in re.split(r"(?<=[.!?])\s+|\n", text)
               if 0 < len(s.split()) < 5)


def voice_rates(text):
    """Per-1,000-word rate for each trait. Rates, so a 500-word sample and a 700-word
    rewrite compare directly."""
    w = max(len(re.findall(r"\S+", text)), 1)
    out = {}
    for name, pat in VOICE_TRAITS.items():
        n = _short_sentences(text) if pat is None else len(re.findall(pat, text))
        out[name] = (n, n / w * 1000)
    return out, w


def voice(sample_path, new_path, floor=0.5):
    """Report every trait the sample demonstrates that the rewrite lost or thinned.

    `--compare` asks whether the rewrite kept the source's FACTS. Nothing asked whether it
    kept the author's VOICE, which SKILL.md ranks item 3 — above every house-style rule in
    items 6 and 7. On 2026-08-22 a benchmark caught the gap: across five runs the skill
    produced zero exclamation marks against a sample that uses two, while the unaided
    baseline kept them in four runs of five. The runs had catalogued the trait in their own
    notes and flattened it anyway, so this is not something a rule can fix by being written
    more clearly. It needs a count.

    DROPPED  the sample uses it, the rewrite does not use it at all.
    THINNED  the rewrite keeps it at under `floor` of the sample's rate.
    IMPOSED  the rewrite uses it at over 2x the sample's rate, or uses one the sample never
             uses. Matching a voice is not maximizing its devices, and a one-sided check is
             a check you can pass by overshooting.

    What this deliberately does NOT protect: anything references/phrases.md lists. Those are
    habit, which SKILL.md separates from voice in as many words — throat-clearing, hedges,
    filler transitions, redundant setup, generic emphasis. A sample full of them is a writer
    with bad habits, not a writer whose bad habits are sacred, and a check that preserved
    them would turn "match the author" into a license for slop. VOICE_TRAITS holds only
    countable structural and register features for that reason, and the habit line below
    says so out loud on every run where the sample carries any.
    """
    sam = open(sample_path, encoding="utf-8").read()
    new = open(new_path, encoding="utf-8").read()
    srates, sw = voice_rates(sam)
    nrates, nw = voice_rates(new)
    findings = []
    for name in VOICE_TRAITS:
        sn, sr = srates[name]
        nn, nr = nrates[name]
        if sn < 2:
            # One instance is not a demonstrated habit, and a rate computed off it is not a
            # rate. The sample's single contraction reported as DROPPED on four runs before
            # this guard, which is noise crowding out the traits it uses a dozen times.
            continue
        if nn == 0:
            findings.append(("DROPPED", name, sn, sr, nn, nr))
        elif nr < sr * floor:
            findings.append(("THINNED", name, sn, sr, nn, nr))
        elif nr > sr * 2:
            findings.append(("IMPOSED", name, sn, sr, nn, nr))
    for name, pat in VOICE_TRAITS.items():
        # A device the sample never uses, appearing in the rewrite, is an imposed voice.
        if srates[name][0] == 0 and nrates[name][1] > 2.0:
            findings.append(("IMPOSED", name, 0, 0.0, *nrates[name]))
    print(f"  sample {sw} words, rewrite {nw} words. Rates are per 1,000 words.\n")
    if not findings:
        print("  no voice trait the sample demonstrates was lost or thinned.")
    for kind, name, sn, sr, nn, nr in findings:
        print(f"  [{kind}] {name}: sample {sn} ({sr:.1f}/1k), rewrite {nn} ({nr:.1f}/1k)")
    if findings:
        print("\n  A supplied sample is item 3 and outranks every house-style rule below it.")
        print("  DROPPED and THINNED are the author's devices the rewrite did not carry.")
        print("  IMPOSED is the opposite error: a voice matched by overshooting is not matched.")
    # The boundary, stated on every run rather than left to be remembered: what the sample
    # does that phrases.md calls habit is NOT protected by anything above.
    habit = []
    for cat, (items, flat) in PHRASES.items():
        if not flat:
            continue
        n = sum(len(re.findall(pat, sam, re.I)) for _, pat in items)
        if n:
            habit.append(f"{cat} ({n})")
    if habit:
        print(f"\n  The sample also carries habit that this check does NOT protect: "
              f"{'; '.join(habit)}.")
        print("  Habit is not voice (SKILL.md). Run the plain scan on the sample to see them.")
    return bool(findings)


def compare(src_path, new_path):
    """Report every specific in the rewrite that the source does not contain.
    Zero is the target. This is the no-fabrication rule as a check instead of
    a promise: a model can say it invented nothing; this shows whether it did."""
    src_text = open(src_path, encoding="utf-8").read()
    new_text = open(new_path, encoding="utf-8").read()
    a, b = facts(src_text), facts(new_text)
    src_tokens = set(re.findall(r"[a-z]+", src_text.lower()))
    print(f"\n=== compare: {new_path} against {src_path} ===")
    total = 0
    hedged = []
    for k, label in (("numbers", "NEW-NUMBER"), ("years", "NEW-YEAR"), ("citations", "NEW-CITATION"),
                     ("standards", "NEW-STANDARD"), ("urls", "NEW-URL"), ("names", "NEW-NAME")):
        new = sorted(b[k] - a[k]) if k != "names" else sorted(
            (b["names"] | b["possible"]) - (a["names"] | a["possible"]))
        if k == "names":
            # A name whose words all appear in the source is usually a recombination
            # ("the red platform" -> "Red Cloud"), which the old filter dropped
            # silently. Drop it only when the source has the phrase intact.
            src_low = " ".join(re.findall(r"[a-z']+", src_text.lower()))
            def coined(n):
                ws = n.split()
                if len(ws) < 2 or ws[0] in _COMMON_CAPS: return False
                # every word capitalized: "Red Cloud" yes, "Elasticsearch and" no
                if not all(w[:1].isupper() for w in ws): return False
                if not all(w.lower() in src_tokens for w in ws): return False
                return " ".join(re.findall(r"[a-z']+", n.lower())) not in src_low
            recombined = [n for n in new if coined(n)]
            new = [n for n in new if not all(w.lower() in src_tokens for w in n.split())]
            # An uncertain single token is a warning, not a hard failure (#32). The
            # hard failure stays with names carrying a word the source never used,
            # with recombined product phrases, and with URLs and identifiers.
            hedged = [n for n in new if n not in b["names"]]
            new = [n for n in new if n in b["names"]]
            if recombined:
                print(f"  [RECOMBINED-NAME] {len(recombined)}: " + ", ".join(recombined[:8])
                      + " — every word appears in the source but not as this phrase; check it names a real thing")
                total += len(recombined)
        total += len(new)
        if new:
            note = (" \u2014 a standard or algorithm the source never names; asserting a compliance "
                    "or configuration property is a commitment someone has to honor"
                    if k == "standards" else "")
            print(f"  [{label}] {len(new)}: " + ", ".join(new[:12]) + (" ..." if len(new) > 12 else "") + note)
    if hedged:
        print(f"  [POSSIBLE-NEW-TERM] {len(hedged)}: " + ", ".join(hedged[:12])
              + (" ..." if len(hedged) > 12 else "")
              + " — capitalized mid-sentence and built from ordinary words, so this is more "
                "often a common noun than an invented entity. Warning, not a failure; read it once.")
    # The bracket exemption reports itself. A flag asks the author for a value, so it
    # is not a fabrication and does not count toward the total, but a reader who never
    # hears about it cannot tell a flag from a fact smuggled inside square brackets.
    exempt = sorted({x for k in ("numbers", "years", "names", "possible", "standards")
                     for x in b["flagged"][k] if x not in a[k] and x not in a["flagged"][k]})
    if exempt:
        print(f"  [IN-FLAG] {len(exempt)} new specifics sit inside bracketed flags and are not "
              f"counted: " + ", ".join(exempt[:8]) + (" ..." if len(exempt) > 8 else "")
              + " \u2014 check each is a slot for the author to fill, not a value stated in brackets")

    # A dropped specific is the same defect facing the other way: the source said
    # nine minutes and the rewrite no longer does.
    new_low = new_text.lower()
    for k, label in (("numbers", "LOST-NUMBER"), ("years", "LOST-YEAR"), ("citations", "LOST-CITATION"),
                     ("standards", "LOST-STANDARD")):
        gone = sorted(a[k] - b[k])
        if k == "numbers":
            gone = [g for g in gone if not any(w in new_low for w in spelled(g))]
        total += len(gone)
        if gone:
            print(f"  [{label}] {len(gone)}: " + ", ".join(gone[:12]) + (" ..." if len(gone) > 12 else ""))
    # How much of the source survived. Every model tested on already-good prose
    # rewrote it wholesale, and nothing in this file could see that happening.
    # Gated: heavy rewriting is the CORRECT answer when the source is full of
    # tells, so this only speaks when the source was already close to clean.
    src_tells = [k for k, _ in find(src_text)[0]
                 if k in ("TIER1", "TIER2", "TIER3", "ARTIFACT", "FORMAT", "STRUCTURE")]
    sw, nw = words(strip_code(src_text).lower()), words(strip_code(new_text).lower())
    if len(sw) >= 40 and len(src_tells) < 2:
        kept = sum(bl.size for bl in difflib.SequenceMatcher(None, sw, nw, autojunk=False).get_matching_blocks())
        pct = kept / len(sw)
        if pct < 0.70:
            total += 1
            print(f"  [REWRITE-SCOPE] {kept}/{len(sw)} source words ({pct:.0%}) survive in matching runs. "
                  "Under 70 percent is a rewrite, not an edit: check that the voice survived and no fact went missing.")
    # Relationship drift. Warnings only: they do not count toward the total and do not
    # move the exit code, so a noisy window heuristic cannot fail a good rewrite.
    rel = fidelity(src_text, new_text)
    if not total and not rel:
        print("  no specifics added or dropped, and the source survived the edit")
    for kind, msg in rel:
        print(f"  [{kind}] {msg}")
    if rel:
        print("  The lines above are warnings about which fact sits next to which. Every token "
              "can survive a rewrite that still changed the meaning; these do not fail the check.")
    print("\n  The rewrite may still be wrong in ways this cannot see; it can only see what changed.")
    return total

def report(name, text):
    out, wc = find(text)
    print(f"\n=== {name} ({wc} words) ===")
    print(f"  vocabulary: {VOCAB_SOURCE}")
    if not out:
        print("  clean on the mechanical passes")
    for kind, msg in out:
        print(f"  [{kind}] {msg}")
    print("\n  These are counts, not a verdict. Judgment checks are in references/preflight.md.")
    return out

def _demo_text():
    """Built from the LOADED tiers, so this self-check tracks the catalog instead of
    a copy of it. Two Tier 2 words in one paragraph; a Tier 3 word repeated past 3%."""
    t2 = [w for w in TIER2 if " " not in w][:2] or ["crucial", "foster"]
    t3 = next((w for w in TIER3 if " " not in w), "key")
    return f"""# The Evolving Landscape Of Modern Systems

We delve into a rich tapestry of ideas here \u2014 and it is worth noting that the
approach is seamless. Great question!

A {t2[0]} finding. The team built a {t2[1]} pipeline over the quarter and shipped
it without incident, which mattered.

The {t3} point is the {t3} point and the {t3} point, a {t3} one, and {t3} again.

- **First:** first
- **Second:** second
- **Third:** third

Here is a \u201cquoted\u201d phrase with a zero\u200bwidth space. See https://x.com/?utm_source=chatgpt.com
"""
DEMO = None

def _fact_check():
    """Regressions --compare used to report. Both halves matter: a flag must not be
    read as a fabrication, and a fabrication must not hide behind a flag."""
    flags = facts("[Needs the engagement metric.] It took [12] months, rated [N]/5, "
                  "on AES-256 with SOC 2 and ISO 27001.")
    cases = {
        # the bug: a bracketed flag's first word became a proper name
        "bracketed flag read as a name": "Needs" not in flags["names"],
        # same root cause, the other opener
        "parenthesized sentence read as a name": "Redis" not in facts("(Redis is the cache.)")["names"],
        # digits inside a flag are a slot, not a figure
        "digits inside a flag counted as invented": not {"12", "5"} & flags["numbers"],
        "flagged digits not reported as exempt": {"12", "5"} <= flags["flagged"]["numbers"],
        # a standard's digits belong to its name
        "standard's digits counted as invented": not {"2", "256", "27001"} & flags["numbers"],
        "standard not named as a standard": {"AES-256", "SOC 2", "ISO 27001"} <= flags["standards"],
        # the exemptions must not swallow real specifics
        "real figure no longer counted": "40 ms" in facts("Latency fell 40 ms.")["numbers"],
        "real name no longer counted": "Redis" in facts("We cache in Redis today.")["names"],
        "markdown link text no longer counted": "Redis" in facts("We use [Redis](https://r.io) daily.")["names"],
    }
    # #32: a capitalized common noun is not an invented entity. Each of these appears
    # mid-sentence, where the sentence-initial exemption cannot reach it.
    common = ("We ran an Audit and a Build on Channel two. The Median and the Named "
              "value went to the Owner, the Region and the Sev. It is a Type II report.")
    f = facts(common)
    for w in "Audit Build Channel Median Named Owner Region Sev Type".split():
        cases[f'"{w}" reported as an invented name'] = w not in f["names"]
    cases["Type II not read as a standard"] = "Type II" in f["standards"]
    mon = facts("It slipped again in February and shipped in October.")
    cases["month reported as an invented name"] = not mon["names"]
    cases["month no longer counted as a specific"] = {"February", "October"} <= mon["numbers"]
    # ...and the exemption must not have swallowed real fabrication.
    inv = facts("Latency fell 40 ms after the migration to Valkey in Q3, per Gartner.")
    cases["invented name lost to the common-noun exemption"] = \
        {"Valkey", "Gartner"} <= inv["names"]
    cases["invented figure lost to the common-noun exemption"] = "40 ms" in inv["numbers"]
    cases["invented URL not counted"] = "https://r.io/x" in facts("See https://r.io/x.")["urls"]
    # #43, half one: the markers of a numbered list were reported as invented numbers,
    # which no structured rewrite could ever pass. The control matters more than the
    # fix: small digits in running prose are still figures.
    lst = facts("Why customers stay:\n\n1. Reliability.\n2. Cost.\n3. Support.\n")
    cases["list ordinal reported as an invented number"] = not lst["numbers"]
    cases["small figure lost to the ordinal exemption"] = \
        {"3", "2 s"} <= facts("We run 3 nodes and it answers in 2 s.")["numbers"]
    cases["invented figure lost to the ordinal exemption"] = \
        "99.98%" in facts("Uptime was 99.98% across the fleet.")["numbers"]
    # #43, half two: any bracketed span is a flag, including one in backticks, which is
    # how a rewrite marked all 68 of its gaps. The control is the same value asserted
    # outside brackets, which is a fabrication and must still be reported.
    for form in ("`[ ]`", "`[99.98]`", "[N]", "[needs the uptime figure]", "[TBD]"):
        cases[f'bracketed flag {form} not read as a flag'] = \
            not facts(f"Uptime was {form}% across the fleet.")["numbers"]
    cases["figure inside a flag not reported as exempt"] = \
        "99.98" in facts("Uptime was `[99.98]`% across the fleet.")["flagged"]["numbers"]
    cases["asserted figure hidden by the flag exemption"] = \
        "99.98%" in facts("Uptime was 99.98% and the SLA is [N]%.")["numbers"]
    # #46: retitling a section is reorganizing, not inventing. --compare promises that
    # zero findings is the only acceptable result, so before this a rewrite that gave its
    # sections new names could not pass at all.
    head = facts("## Investigation\n\nWe shipped it.\n\n## Root Cause\n\nIt was the pooler."
                 "\n\n## Next Steps\n\nWe will watch it.\n")
    cases["retitled section reported as an invented name"] = \
        not (head["names"] | head["possible"])
    # The control, both shapes: a heading is not a hiding place for a fabricated product,
    # with a body that repeats the name and with a heading standing alone.
    cases["invented name hidden in a heading"] = \
        "Introducing Vault" in facts("## Introducing Vault\n")["names"]
    cases["invented name hidden in a heading above a body"] = \
        "Introducing Vault" in facts("## Introducing Vault\n\nIt holds credentials.\n")["names"]
    # ...and the other half of the rule: a structural word the body uses as a proper noun
    # is a name, so the exemption cannot be bought by putting the word in a heading too.
    cases["heading word the body uses as a name lost to the exemption"] = \
        "Region" in facts("## Region\n\nWe moved the fleet to Region last night.\n")["possible"]
    # A markdown link is not a flag, and a fenced block is not prose.
    lnk = facts("We moved to [Redis](https://r.io) and cut 40 ms.")
    cases["markdown link read as a flag"] = "40 ms" in lnk["numbers"] and not lnk["flagged"]["numbers"]
    cases["fenced code read as a flag"] = not facts("```\nuptime = [99.98]\n```")["flagged"]["numbers"]
    return [k for k, ok in cases.items() if not ok]

def _fidelity_check():
    """The ten ways a rewrite keeps every token and changes what the text says (#28),
    plus the controls that keep the checks from being noise generators."""
    cases = [
        ("number swap", "The p95 latency was 120 ms and the p99 latency was 480 ms across the fleet.",
         "The p95 latency was 480 ms and the p99 latency was 120 ms across the fleet."),
        ("version-property swap", "pgbouncer 1.17 had a connection-reset bug, and 1.21 did not.",
         "pgbouncer 1.21 had a connection-reset bug, and 1.17 did not."),
        ("qualifier drift", "Latency fell by roughly 40 ms after the cutover on March 11.",
         "Latency fell by 40 ms after the cutover on March 11."),
        ("negation drift", "The 1.17 pooler dropped connections and the 1.21 pooler did not drop them.",
         "The 1.17 pooler did not drop connections and the 1.21 pooler dropped them."),
        ("promise hardening", "We may support Postgres 16 in the 2027 release of the importer.",
         "We will support Postgres 16 in the 2027 release of the importer."),
        ("policy inflation", "Customer records are usually encrypted at rest on the 3 storage tiers.",
         "Customer records are always encrypted at rest on the 3 storage tiers."),
        ("timeline drift", "The proposed cutover date is March 11, pending a review by the 2 owners.",
         "The committed cutover date is March 11, confirmed by a review by the 2 owners."),
        ("owner drift", "Priya wrote the importer in 2021 and Dan reviewed the rollback plan in 2022.",
         "Dan wrote the importer in 2021 and Priya reviewed the rollback plan in 2022."),
        ("citation moved", "Adoption rose 12 points (Gartner, 2024). Retention fell 3 points last quarter.",
         "Adoption rose 12 points last quarter. Retention fell 3 points (Gartner, 2024)."),
        ("silent omission",
         "Runtime went from 4 hours to 11 minutes on the 14 archived nights. The rollout is "
         "blocked until the retention policy for customer events lands.",
         "Runtime went from 4 hours to 11 minutes on the 14 archived nights."),
    ]
    bad = [f"fidelity: {n}" for n, a, b in cases if not fidelity(a, b)]
    # An unchanged rewrite must be silent, or the warnings mean nothing.
    if fidelity(cases[1][1], cases[1][1]): bad.append("fidelity: unchanged text warned")
    return bad

def _phrase_check():
    """Both directions on the phrases.md scan, added the day it was written.

    A catalog scanner that fires on its own catalog is the failure mode here: phrases.md
    quotes all 99 of its phrases, and SKILL.md quotes a dozen more as examples. Reusing
    quoted() is what makes that work, so the check has to prove it still does.
    """
    bad = []
    # Both strings must clear report()'s ~40-word floor or it returns FLOOR and scans nothing,
    # which is how the first version of this check passed by never running.
    FILLER = (" The migration moved twelve nodes onto a single database and the search index "
              "was rebuilt from the existing corpus over three weeks without a cutover window "
              "or any measurable loss of query throughput for the reporting team.")
    used = "Here's the thing: we need to move faster." + FILLER
    quoting = 'The skill tells you to cut "Here\'s the thing:" from an opener.' + FILLER
    hits = lambda t: {k for k, _ in report("x", t) if k == "PHRASE"}
    if not hits(used):
        bad.append("a throat-clearing opener used in earnest was not flagged")
    if hits(quoting):
        bad.append("a phrase quoted as an example was flagged")
    if not PHRASES:
        bad.append("phrases.md parsed empty")
    if any(flat for cat, (items, flat) in PHRASES.items() if cat == "Adverbs"):
        bad.append("Adverbs was treated as flat; it sets its own test")
    # The boundary that keeps --voice from sheltering slop.
    if set(VOICE_TRAITS) & set(PHRASES):
        bad.append("a habit category leaked into VOICE_TRAITS")
    return bad


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__ or "")
        sys.exit(0)
    if "--demo" in sys.argv:
        PLAIN_TEXT = True          # the demo text carries curly quotes on purpose
        got = {k for k, _ in report("demo", _demo_text())}
        want = {"DASH", "TIER1", "TIER2", "TIER3", "ARTIFACT", "FORMAT", "QUOTES", "INVISIBLE"}
        missing = sorted(want - got) + _fact_check() + _fidelity_check() + _phrase_check()
        print(f"\n  self-check: {'PASS' if not missing else 'FAIL, missed ' + ', '.join(missing)}")
        sys.exit(1 if missing else 0)
    if "--voice-demo" in sys.argv:
        import tempfile
        SAMPLE = ("Okay. Search. I hated it! Twelve nodes. Twelve! We ran it for years "
                  "(nobody enjoyed that) and I am not going to pretend otherwise. Fine.")
        FLAT = ("The search infrastructure was operated for a period of several years. "
                "The team did not derive satisfaction from this arrangement, and the "
                "operational burden was considerable throughout the entire duration.")
        KEPT = ("Okay. Search. I hated it! Twelve nodes. Twelve! We ran that thing for years "
                "(nobody enjoyed it) and I am not going to pretend otherwise. Fine.")
        d = pathlib.Path(tempfile.mkdtemp())
        (d / "s.md").write_text(SAMPLE); (d / "flat.md").write_text(FLAT); (d / "kept.md").write_text(KEPT)
        print("  flattened rewrite:")
        bad = voice(str(d / "s.md"), str(d / "flat.md"))
        print("\n  faithful rewrite:")
        good = voice(str(d / "s.md"), str(d / "kept.md"))
        ok = bad and not good
        print(f"\n  self-check: {'PASS' if ok else 'FAIL'} "
              f"(flattened reports findings: {bad}; faithful reports none: {not good})")
        sys.exit(0 if ok else 1)
    if "--voice" in sys.argv:
        i = sys.argv.index("--voice")
        try:
            sam, new_ = sys.argv[i + 1], sys.argv[i + 2]
        except IndexError:
            print("usage: prose-scan.py --voice SAMPLE REWRITE"); sys.exit(2)
        sys.exit(1 if voice(sam, new_) else 0)
    if "--compare" in sys.argv:
        i = sys.argv.index("--compare")
        try:
            src, new = sys.argv[i + 1], sys.argv[i + 2]
        except IndexError:
            print("usage: prose-scan.py --compare SOURCE REWRITE"); sys.exit(2)
        sys.exit(1 if compare(src, new) else 0)
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    for path in [a for a in sys.argv[1:] if not a.startswith("--")]:
        report(path, open(path, encoding="utf-8").read())
