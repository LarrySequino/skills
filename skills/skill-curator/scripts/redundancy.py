#!/usr/bin/env python3
"""Redundancy check for a skill edit: which added units restate one already there.

    python3 redundancy.py <skill-dir> --git <rev>        added units from `git show <rev>`, existing from <rev>^
    python3 redundancy.py <skill-dir> --added <file>     added units from a file, existing from the working tree
    python3 redundancy.py <skill-dir> --staged           added units from the index, existing from HEAD
    python3 redundancy.py --demo                         self-check on a built-in fixture

It catches lexical restatement. A thematic duplicate that shares no rare terms (a second
entry about typefaces beside an existing one) is still the reader's to see; run it, then read.

A unit is a paragraph, a list item, a table row, or a numbered step. For each added unit
the script finds the existing unit that shares the most rare terms and prints the pair
when the overlap is high enough to read. It reports; it never decides. An addition that
matches is usually a sentence to append to the existing entry rather than a new entry,
which is the failure this exists to catch: on 2026-09-02 four of about fifteen harvested
additions duplicated entries already in the target skills, and the written rule "search
the existing files first" had been followed.

Stdlib only. Exit 1 only for a REDUNDANT? pair at or above --refuse-at (default 0.5); an
EXTENDS pair (the added unit contains the existing one) never fails, so a hook can refuse a
confident duplicate and let an extension through.
"""
import argparse, math, pathlib, re, subprocess, sys
from collections import Counter

STOP = set("""about above after again against all also and any are because been before being
between both but can could did does doing down during each few for from further had has have
having here how into its itself just more most not off once only other our out over own same
should some such than that the their them then there these they this those through too under
until very was were what when where which while who whom why will with would you your never
every each rule rules skill skills file files user when use uses used one two three four five
six seven eight nine ten first second third than then that this with from into""".split())

def units(text):
    """Paragraphs, list items, table rows, and numbered steps, with wrapped continuation lines
    kept with the item they continue."""
    out, para = [], []
    def flush():
        if para:
            # a paragraph of bold-labeled fields (`**Input:** ... **Confidence:** ...`) is one
            # unit per field, or a field restated elsewhere is diluted by its neighbors
            out.extend(re.split(r"\s(?=\*\*[A-Z][^*]{0,30}:\*\*)", " ".join(para).strip())); para.clear()
    fence = False; last_item = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence; flush(); last_item = False; continue
        if fence or not s or set(s) <= set("-|: "):
            flush(); last_item = False; continue
        item = s.startswith(("|", "- ", "* ", "#")) or bool(re.match(r"^\d+[a-z]?\.\s", s))
        if item:
            flush(); out.append(s); last_item = not s.startswith(("|", "#")); continue
        if last_item and line[:1].isspace() and not para:
            out[-1] += " " + s; continue
        last_item = False
        para.append(s)
    flush()
    return [u for u in out if not u.startswith("#")]

def stem(w):
    for suf in ("ing", "es", "ed", "s"):
        if len(w) > 5 and w.endswith(suf):
            return w[: -len(suf)]
    return w

def terms(u):
    # a table row's first cell is its key, the name of what the row is about (a dimension, a
    # source); a row keyed by a dimension is not a restatement of that dimension's definition.
    # Only a short key: a first cell that carries the rule itself still counts.
    if u.startswith("|") and u.count("|") > 2 and len(u.split("|", 2)[1].split()) <= 4:
        u = u.split("|", 2)[2]
    words = re.findall(r"[a-z][a-z'-]{3,}", u.lower())
    return set(stem(w) for w in words if w not in STOP)

def weights(all_units):
    df = Counter()
    for u in all_units:
        df.update(terms(u))
    n = max(len(all_units), 1)
    return {t: math.log(1 + n / df[t]) for t in df}

def nearest(added, existing, w):
    ta = terms(added)
    if len(ta) < 4:
        return None
    wa = sum(w.get(t, 0) for t in ta) or 1e-9
    best = (0.0, None, set(), "")
    for ex in existing:
        te = terms(ex)
        shared = ta & te
        if len(shared) < 4:
            continue
        we = sum(w.get(t, 0) for t in te) or 1e-9
        ws = sum(w.get(t, 0) for t in shared)
        a_share, e_share = ws / wa, ws / we
        if min(a_share, e_share) < 0.2:
            continue
        score = max(a_share, e_share)
        kind = "EXTENDS" if ex.strip() and ex.strip()[:60] in added else "REDUNDANT?"
        if score > best[0]:
            best = (score, ex, shared, kind)
    return best if best[1] else None

def is_prose(path):
    """Skill prose is Markdown outside evals/ and not the README. A fixture, its wrong answer,
    and its expectations share terms by construction (a map and the reply that answers it),
    so they are test data here, the same way a script's own fixture text is; the README is
    generated from the frontmatter (tools/gen_skill_readme.py) and restates it by design.
    ATTRIBUTION.md is a record, not a rule: a credit necessarily describes what it credits."""
    path = str(path).replace("\\", "/")
    return (path.endswith(".md") and path.rsplit("/", 1)[-1] not in ("README.md", "ATTRIBUTION.md")
            and "/evals/" not in path and not path.startswith("evals/"))

def is_log(path):
    """Maintenance and harvest-log tables are dated records: a new row for a source sits beside
    the older row for the same source by design (the 2026-09-28/29 false refusals)."""
    return str(path).replace("\\", "/").rsplit("/", 1)[-1] in ("maintenance.md", "harvest-log.md")

def prose_units(path, text):
    if is_log(path):
        text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("|"))
    return units(text)

def existing_from_tree(skill_dir):
    out = []
    for f in sorted(pathlib.Path(skill_dir).rglob("*.md")):
        if not is_prose(f.relative_to(skill_dir)):
            continue
        out += prose_units(f, f.read_text(errors="replace"))
    return out

def existing_from_git(rev, skill_dir):
    parent = f"{rev}^"
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", parent, "--", str(skill_dir)],
                           capture_output=True, text=True, check=True).stdout.split()
    out = []
    for n in names:
        if is_prose(n):
            out += prose_units(n, subprocess.run(["git", "show", f"{parent}:{n}"], capture_output=True, text=True).stdout)
    return out

def added_from_diff(diff, sign="+", raw=False):
    """Added (or, with sign "-", removed) lines from Markdown files only; a script's own fixture
    text is not a skill edit. Hunks and files are separated by a blank line so lines from two
    places never join into one unit. raw=True returns the stripped lines instead of units."""
    lines, keep, log = [], False, False
    for l in diff.splitlines():
        if l.startswith("+++ ") or l.startswith("--- "):
            if l.startswith("+++ "): keep, log = is_prose(l.rstrip()), is_log(l.rstrip())
            lines.append(""); continue
        if l.startswith("@@"):
            lines.append(""); continue
        if keep and l.startswith(sign) and not (log and l[1:].lstrip().startswith("|")):
            lines.append(l[1:])
    if raw:
        return [l.strip() for l in lines if l.strip()]
    return units("\n".join(lines))

def removed_from_git(rev, skill_dir):
    return added_from_diff(subprocess.run(["git", "show", "--format=", "--unified=0", rev, "--", str(skill_dir)],
                                          capture_output=True, text=True, check=True).stdout, "-", raw=True)

def removed_from_staged(skill_dir):
    return added_from_diff(subprocess.run(["git", "diff", "--cached", "--unified=0", "--", str(skill_dir)],
                                          capture_output=True, text=True, check=True).stdout, "-", raw=True)

def added_from_git(rev, skill_dir):
    return added_from_diff(subprocess.run(["git", "show", "--format=", "--unified=0", rev, "--", str(skill_dir)],
                                          capture_output=True, text=True, check=True).stdout)

def added_from_staged(skill_dir):
    return added_from_diff(subprocess.run(["git", "diff", "--cached", "--unified=0", "--", str(skill_dir)],
                                          capture_output=True, text=True, check=True).stdout)

def existing_from_head(skill_dir):
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", str(skill_dir)],
                           capture_output=True, text=True, check=True).stdout.split()
    out = []
    for n in names:
        if is_prose(n):
            out += prose_units(n, subprocess.run(["git", "show", f"HEAD:{n}"], capture_output=True, text=True).stdout)
    return out

def run(added, existing, threshold=0.35, refuse_at=0.5, quiet=False, removed=()):
    # a rewritten entry is not a duplicate of the line it replaces, so removed units leave the corpus
    # `removed` is the commit's removed lines. A unit that contains one was edited, not duplicated,
    # so it leaves the corpus; frontmatter joins `name:` and `description:` into one unit, which is
    # why equality on whole units was not enough.
    removed_lines = [l for l in removed if len(l) > 20]
    existing = [e for e in existing if e not in set(added) and not any(rl in e for rl in removed_lines)]
    w = weights(existing + added)
    hits = refuse = 0
    for a in added:
        near = nearest(a, existing, w)
        if near and near[0] >= threshold:
            hits += 1
            score, ex, shared, kind = near
            if kind == "REDUNDANT?" and score >= refuse_at:
                refuse += 1
            if not quiet:
                print(f"[{kind} {score:.2f}] added:    {a[:120]}")
                print(f"                   existing: {ex[:120]}")
                print(f"                   shared:   {', '.join(sorted(shared))[:110]}")
    if not quiet:
        print(f"{len(added)} added units, {hits} with a near-duplicate at or above {threshold}, {refuse} confident enough to refuse")
    return hits, refuse

DEMO_EXISTING = """
- **A string can appear twice, or be matched by code.** Rewriting it fixes one place and breaks another. Flag those rather than editing them, the same way quoted material is flagged.

4b. **Count check.** Skill catalogs have a discovery budget, and past a certain size some skills stop being surfaced at all. Treat roughly ten skills in a single scope as the trigger for a consolidation pass rather than a hard limit.

A trailing wildcard with a space before it also matches the bare command, so a rule for the program alone still matches its subcommands.
"""
DEMO_ADDED = """Before changing any user-facing string, check whether a test, an i18n key, or a duplicate elsewhere matches it. A string that appears twice, or that code matches on, is flagged rather than edited.

9. **Roster cost.** Count the routed descriptions in each scope and compare against the listing budget; past it the least-used skills are dropped silently, and roughly ten routed skills in one scope is the consolidation trigger.

A decorative layer drawn over a control catches every pointer event inside its box, so the button under it appears active and never receives the click.
"""

def demo():
    hits, _ = run(units(DEMO_ADDED), units(DEMO_EXISTING))
    assert hits == 2, f"demo expected 2 redundant units (strings, roster), got {hits}"
    # an edited description is not a duplicate of the line it replaces, even though frontmatter
    # joins `name:` and `description:` into one unit (the 2026-09-04 false refusals on four PRs)
    before = 'name: grill\ndescription: "A plan the user wants stress-tested before it is built. Interview them one question at a time until nothing is assumed."'
    after = 'description: "A plan the user wants stress-tested before it is built. NOT for a problem too big for one sitting."'
    _, refuse = run(units(after), units(before), quiet=True, removed=[before.splitlines()[1]])
    assert refuse == 0, f"demo expected an edited description to pass, got {refuse} refusals"
    print("demo: ok")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir", nargs="?")
    ap.add_argument("--git", help="a commit whose additions under skill_dir are the candidates; existing text is read from its parent")
    ap.add_argument("--added", help="a file of candidate units, blank-line separated; existing text is the working tree")
    ap.add_argument("--staged", action="store_true", help="candidates are the staged additions under skill_dir; existing text is HEAD")
    ap.add_argument("--threshold", type=float, default=0.35)
    ap.add_argument("--refuse-at", type=float, default=0.5)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        demo(); sys.exit(0)
    if not a.skill_dir or not (a.git or a.added or a.staged):
        ap.error("need <skill-dir> and one of --git, --added, or --staged")
    if a.git:
        added, existing = added_from_git(a.git, a.skill_dir), existing_from_git(a.git, a.skill_dir)
        removed = removed_from_git(a.git, a.skill_dir)
    elif a.staged:
        added, existing = added_from_staged(a.skill_dir), existing_from_head(a.skill_dir)
        removed = removed_from_staged(a.skill_dir)
    else:
        added, existing = units(pathlib.Path(a.added).read_text()), existing_from_tree(a.skill_dir)
    _, refuse = run(added, existing, a.threshold, a.refuse_at, removed=locals().get("removed", ()))
    sys.exit(1 if refuse else 0)
