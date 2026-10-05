#!/usr/bin/env python3
"""The redundancy gate's verdicts of 2026-09-28/29 (~/.claude/gate-log.csv) as staged fixtures.

    python3 test_redundancy.py [path/to/redundancy.py] [-v]

Each fixture writes a few files of real skill text (excerpts from origin/main at 8cf53ca and the
sweep-logs commit 8ffc882) into a temp git repo, commits them, stages one edit, and runs
`redundancy.py <skill> --staged` the way the pre-commit hook does. Nothing is read from this
repo's history, so it runs in a shallow checkout. F1-F4 are record-keeping the gate refused and
must pass; T1-T2 are restatements it caught and must still refuse, against the right unit. The F4
row is reconstructed from the gate-log note, since a rework round replaced the refused text. F2
stands in for the 12:29:49 row (a craft-review credit vs its maintenance.md row) with the same
class from natural-writing, the slop-index credit vs its log row; the old gate refuses both.
"""
import pathlib, subprocess, sys, tempfile

ARGS = [a for a in sys.argv[1:] if a != "-v"]
SCRIPT = pathlib.Path(ARGS[0] if ARGS else pathlib.Path(__file__).resolve().parent / "redundancy.py").resolve()

NW_WATCH = """## Source watchlist

4. **conorbronsdon/avoid-ai-writing**, https://github.com/conorbronsdon/avoid-ai-writing, Read CHANGELOG.md; harvest entries above the logged version. Note: this skill's local fork once ran ahead of upstream, so upstream versions below the log are already merged.
5. **petergyang/no-ai-slop**, https://github.com/petergyang/no-ai-slop, Diff SKILL.md and eval.md; its preservation-first editing principles feed references/preflight.md.

## Harvest log

| Source | Last checked | Version/state at check |
|---|---|---|
| blader/humanizer | 2026-07-28 | 2.9.1 (patterns 1–33; no-fabrication, voice-sample precedence, secondhand guard) |
"""
CONOR_ROW = "| conorbronsdon/avoid-ai-writing | 2026-07-28 | upstream 3.4.0 (local fork 3.10.0 already merged) |\n"
CONOR_ROW_EDITED = ("| conorbronsdon/avoid-ai-writing | 2026-07-28 | upstream 3.4.0 (local fork 3.10.0 already merged). "
                    "The \"3.4.0\" looks wrong: current is 3.36.0 (see 2026-09-28) |\n")

SLOP_INDEX_ROW = ("| hgaddipati1118/slop-index | 2026-09-29 | 80b1b0d, MIT. Cited the em dash rates (0.04 per 1k in a "
                  "2019-20 Discord corpus against 1.5-15 for models) beside the rule 12 cap, and the EnronSent median "
                  "of about 90 words in rule 15. Its tier-1 finding is #255. |\n")
NW_ROWS = ("| aashaexo/soundshuman | 2026-09-29 | a45cfbb, MIT (API says NOASSERTION; LICENSE file is MIT). "
           "Took `git diff --word-diff` as the edit-mode review view. |\n"
           "| jalaalrd/anti-ai-slop-writing | 2026-09-29 | 63255f9, no LICENSE: idea only. Took Markdown sent to "
           "plain-text destinations into rule 12. |\n"
           "| hardikpandya/stop-slop | 2026-09-29 | 8da1f03, MIT. Nothing new since the 03-17 rules, all covered. |\n")
SLOP_INDEX_CREDIT = ("- **hgaddipati1118/slop-index** @ 80b1b0d, MIT, Copyright (c) 2026 Slashy. Two measurements "
                     "cited in `SKILL.md`: the human and model em dash rates beside the cap in rule 12, and the Enron "
                     "email length medians in rule 15.\n")
NW_ATTR = """# Attribution

- **blader/humanizer** @ c6f7cc2, MIT, Copyright (c) 2025 Siqi Chen. Three emphasis-crutch shapes in `references/phrases.md`: the "read that again" instruction, a period after each word, and one word in capitals.
- **conorbronsdon/avoid-ai-writing** @ 9b8d030 (family added in 3.28.0), MIT, Copyright (c) 2026 Conor Bronsdon; upstream adapted the category from Simon Willison's LLM cliché highlighter. The staged-discovery family, as the Performed Insight section of `references/phrases.md`.
- **aashaexo/soundshuman** @ a45cfbb, MIT, Copyright (c) 2026 aasha. `git diff --word-diff` as the review view in edit mode.
- **jalaalrd/anti-ai-slop-writing** @ 63255f9, no license file: idea only, no text. Markdown sent to a plain-text destination, in rule 12.
"""

DIAG_SKILL = """## Phase 4: The loop

**Three failed fixes stop the loop.** After the third fix that did not make the loop go green,
no fourth is attempted. Before the third: when the two that failed share a premise, write the
premise as one sentence, count which actors it holds for (callers, workers, machines), and read
the skew, not only the one actor that showed the failure; a third fix on an unexamined premise
is the second again.
The record goes back to the human: the loop, the hypotheses, what each probe showed, and
what is now suspected about the architecture rather than the line.
"""
DIAG_ATTR = """# Attribution

- **pstack**, `playbooks/bug-fix.md` and `principle-fix-root-causes`: a "might help" guard is
  a hypothesis, not a fix; revert what a refuted hypothesis motivated; suspect state before
  code on restart bugs.
"""
DIAG_CREDIT = ("  code on restart bugs. From `principle-attack-the-premise` (at `e8d856f`): when two failed fixes\n"
               "  share a premise, state it in one sentence, count which actors it holds for, and read the skew\n"
               "  before a third.\n")

CR_SKILL = """## 4. Dimensions

3. **Color & contrast (measurable)** — WCAG AA: 4.5:1 body, 3:1 large/non-text. Run `scripts/contrast.py`
   on every pair; report ratio + color-blindness risk. Tokens not hardcoded; consistent across states.
15. **Template-reuse gates.** Run the catalog in `references/design-tropes.md` and
    `scripts/slop-scan.py`. One instance is fine; the *reflex* — applied everywhere without a
    reason — is the finding.
16. **The two-briefs test.** Would this design system, run on a *different* brief, produce a visibly
    different result — or just a color-swap of the same template? If the latter, it isn't distinctive.
17. **The subtraction test.** Remove the single most conspicuous effect; if nothing recognizable is
    left, that effect was the whole design.

## 5. Bundled scripts (run these; don't do the math in your head)

- `scripts/contrast.py` — WCAG contrast ratio for two hex colors + AA/AAA pass for normal/large/non-text.
  `python3 scripts/contrast.py "#f4eefb" "#161020"`
  A page has as many pairs as it has colors, and one call per pair is one round trip per pair:
  `python3 scripts/contrast.py --pairs pairs.txt` takes a `fg bg label` per line and prints one
  table, failures first. Exits 1 if any pair fails AA for body text.
"""
CR_EXAMPLE = """## Summary
**Screen:** Sleep — alarm set / bedtime sheet. **Job:** set an alarm time and start a sleep session.
**Assumed user:** someone in bed, low light, one hand, wants this fast. **Input:** Figma frame via MCP
(`get_metadata` geometry + `get_variable_defs` → no tokens defined, measured against fallback scale).
**Confidence:** high on the computed and observed findings, medium on the judgment call.

## Coverage
| Dimension | Status |
|---|---|
| Color & contrast | 1 finding |
| Consistency & tokens | 2 findings, filed under Symmetry (redrawn cards) and Spacing (inter-card gap) |
| Template-reuse gates | Clear |
| The subtraction test | Clear |
"""
# on the base, T1 refused against this record row rather than the Summary
CR_MAINT = """## Adversarial review, 2026-08-21

| What it found | Now covered by |
|---|---|
| The workflow ordered a fallback to the placeholder token file, which `design-system.md` itself says measures the screen against the wrong scale | `SKILL.md` step 2 names the source it measured against |
"""
TOKENS_ROW = "| Consistency & tokens | 2 findings, filed under Symmetry (redrawn cards) and Spacing (inter-card gap) |"
TOKENS_ROW_T1 = "| Consistency & tokens | Clear (no tokens defined; measured against the fallback scale) |"
TWO_BRIEFS_ROW = ("| The two-briefs test | Not reviewed: only one screen was supplied, so the design system was never "
                  "run on a second brief |\n")

PIXELS_RULE = ("\n- Measure every color pair against the WCAG floor and sample the rendered pixels, since a "
               "translucent layer or a gradient changes the ratio the tokens promise.\n")
PIXELS_ROW = ("| Check | Area |\n|---|---|\n"
              "| Measure every color pair against the WCAG floor and sample the rendered pixels | contrast |\n")
CI_ROW = ("| Check | Rule |\n|---|---|\n"
          "| contrast | WCAG AA: 4.5:1 body, 3:1 large/non-text; run `python3 scripts/contrast.py` on every pair "
          "and report ratio + color-blindness risk |\n")

# name, skill, expect_refuse, {path: text} committed, {path: text} staged
CASES = [
    ("F1 new log row vs older entry", "natural-writing", False,
        {"references/maintenance.md": NW_WATCH + CONOR_ROW},
        {"references/maintenance.md": NW_WATCH + CONOR_ROW_EDITED}),
    ("F2 credit vs log row", "natural-writing", False,
        {"references/maintenance.md": NW_WATCH + NW_ROWS + SLOP_INDEX_ROW, "ATTRIBUTION.md": NW_ATTR},
        {"ATTRIBUTION.md": NW_ATTR + SLOP_INDEX_CREDIT}),
    ("F3 rule vs its credit", "diagnose", False,
        {"SKILL.md": DIAG_SKILL, "ATTRIBUTION.md": DIAG_ATTR},
        {"ATTRIBUTION.md": DIAG_ATTR.replace("  code on restart bugs.\n", DIAG_CREDIT)}),
    ("F4 coverage row vs definition", "craft-review", False,
        {"SKILL.md": CR_SKILL, "references/example-review.md": CR_EXAMPLE},
        {"references/example-review.md": CR_EXAMPLE.replace("| The subtraction test", TWO_BRIEFS_ROW + "| The subtraction test")}),
    ("T1 cell restates Summary", "craft-review", True,
        {"SKILL.md": CR_SKILL, "references/example-review.md": CR_EXAMPLE, "references/maintenance.md": CR_MAINT},
        {"references/example-review.md": CR_EXAMPLE.replace(TOKENS_ROW, TOKENS_ROW_T1)}),
    ("T2 item repeats usage", "craft-review", True,
        {"SKILL.md": CR_SKILL},
        {"SKILL.md": CR_SKILL.replace("Run `scripts/contrast.py`\n", "Run `python3 scripts/contrast.py`\n")}),
    # the #274 review's C1: a rule restated as a table row whose first cell carries the rule
    ("T3 rule restated in a first cell", "craft-review", True,
        {"SKILL.md": CR_SKILL + PIXELS_RULE},
        {"references/checks.md": PIXELS_ROW}),
    # the log exclusion is by exact basename: ci-maintenance.md is prose, not a log
    ("T4 rule restated in ci-maintenance.md", "craft-review", True,
        {"SKILL.md": CR_SKILL},
        {"references/ci-maintenance.md": CI_ROW}),
]

# the existing unit each true catch must pair with
PAIRS = {"T1": "existing: **Input:** Figma frame", "T2": "existing: - `scripts/contrast.py`",
         "T3": "existing: - Measure every color pair", "T4": "existing: 3. **Color & contrast"}

def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)

def refuses(skill, base, staged):
    with tempfile.TemporaryDirectory() as tmp:
        git(tmp, "init", "-q")
        for files in (base, staged):
            for rel, text in files.items():
                p = pathlib.Path(tmp, "skills", skill, rel)
                p.parent.mkdir(parents=True, exist_ok=True)
                assert not p.exists() or p.read_text() != text, f"fixture edit is a no-op: {rel}"
                p.write_text(text)
            git(tmp, "add", "-A")
            if files is base:
                git(tmp, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.hooksPath=/dev/null",
                    "commit", "-qm", "base")
        r = subprocess.run([sys.executable, str(SCRIPT), f"skills/{skill}", "--staged"],
                           cwd=tmp, capture_output=True, text=True)
        assert r.returncode in (0, 1), r.stderr
        if "-v" in sys.argv:
            print(r.stdout)
        return r.returncode == 1, r.stdout

if __name__ == "__main__":
    bad = 0
    for name, skill, want, base, staged in CASES:
        got, out = refuses(skill, base, staged)
        ok = got == want and (not want or PAIRS[name[:2]] in out)
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {'refuses' if got else 'passes'} (want {'refuse' if want else 'pass'})")
    sys.exit(1 if bad else 0)
