#!/usr/bin/env python3
"""Prove an edit to a page changed the copy and nothing else.

    markup-diff.py before.html after.html    exit 1 if the machinery moved
    markup-diff.py --demo                    self-check

SKILL.md's "Prose inside a page" section says to edit the prose and leave the machinery.
That is a rule with a destructive failure mode and no instrument: a rewrite that renames a
class, drops an attribute, touches a script, or fixes a string in one of the two places it
appears leaves a broken page and a clean-looking diff of the copy.

This compares the skeleton rather than the text. Tags in order, attributes with their values,
and the exact contents of script, style and pre. All of it must be identical. Text nodes are
expected to change, and the one text rule enforced is that a string appearing more than once
before must still appear the same number of times, because editing one of a pair is how a
button stops matching the selector that drives it.

stdlib html.parser, no dependency, because a check nobody can run is not a check.
"""
import html.parser
import pathlib
import re
import sys
import tempfile

OPAQUE = {"script", "style", "pre", "textarea", "code"}

# Attributes a person reads. They are copy, so they belong with the prose and are allowed to
# change; everything else is machinery and is not. Splitting them matters more than it looks:
# a button's label and its aria-label are the same sentence written twice, and editing one is
# how a control keeps its old name for a screen reader.
COPY_ATTRS = {"alt", "title", "placeholder", "label",
              "aria-label", "aria-description", "aria-placeholder", "aria-roledescription"}


class Skeleton(html.parser.HTMLParser):
    """Everything about a page except the words a reader reads."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.frame = []      # structure: tags, attributes, opaque bodies
        self.text = []       # the prose, kept separately
        self._opaque = None

    def _split(self, attrs):
        keep, copy = [], []
        for k, v in attrs:
            (copy if k.lower() in COPY_ATTRS else keep).append((k, v))
        for _, v in copy:
            if v and v.strip():
                self.text.append(" ".join(v.split()))
        return tuple(sorted(keep))

    def handle_starttag(self, tag, attrs):
        self.frame.append(("open", tag, self._split(attrs)))
        if tag in OPAQUE:
            self._opaque = tag

    def handle_startendtag(self, tag, attrs):
        self.frame.append(("void", tag, self._split(attrs)))

    def handle_endtag(self, tag):
        self.frame.append(("close", tag, ()))
        if tag == self._opaque:
            self._opaque = None

    def handle_data(self, data):
        if self._opaque:
            self.frame.append(("body", self._opaque, data))
        elif data.strip():
            self.text.append(" ".join(data.split()))

    def handle_comment(self, data):
        self.frame.append(("comment", "", data))


def parse(path):
    p = Skeleton()
    p.feed(pathlib.Path(path).read_text())
    p.close()
    return p


def _describe(kind, tag, val):
    if kind == "body":
        one = " ".join(val.split())
        return f"<{tag}> contents: {one[:60]!r}"
    if kind == "comment":
        return "an HTML comment"
    if kind == "close":
        return f"</{tag}>"
    attrs = " ".join(f'{k}="{v}"' for k, v in val) if val else ""
    return f"<{tag}{' ' + attrs if attrs else ''}>"


def compare(before, after):
    """List of human-readable findings. Empty means the copy moved and nothing else."""
    a, b = parse(before), parse(after)
    out = []

    if len(a.frame) != len(b.frame):
        out.append(f"structure changed: {len(a.frame)} markup nodes before, {len(b.frame)} after")
    for i, (x, y) in enumerate(zip(a.frame, b.frame)):
        if x != y:
            out.append(f"markup changed at node {i}: {_describe(*x)!r} became {_describe(*y)!r}")
            if len(out) >= 6:
                out.append("... stopping after 6")
                break

    # A repeated string is repeated on purpose: a label and its aria-label, a heading and
    # the nav item pointing at it, a button and the test selector matching it. Only a PARTIAL
    # edit is the defect. Dropping to zero means every instance moved together, which is a
    # correct rename; leaving some behind is what breaks the pairing.
    for s in {t for t in a.text if a.text.count(t) > 1 and len(t) > 2}:
        before_n, after_n = a.text.count(s), b.text.count(s)
        if 0 < after_n < before_n:
            out.append(f"edited {before_n - after_n} of {before_n} copies of a repeated string, "
                       f"leaving {after_n} behind: {s[:50]!r}")
    return out


def main(before, after):
    findings = compare(before, after)
    if not findings:
        a, b = parse(before), parse(after)
        changed = sum(1 for x, y in zip(a.text, b.text) if x != y)
        print(f"  markup intact: {len(a.frame)} nodes unchanged, "
              f"{changed} of {len(a.text)} text runs edited")
        return 0
    print(f"  {len(findings)} problem(s): the edit moved something that is not copy\n")
    for f in findings:
        print(f"      {f}")
    print("\n  Prose inside a page means the prose. Revert the above and edit only the words.")
    return 1


PAGE = """<!doctype html>
<style>.hero{color:#fff;--brand:#0af}</style>
<div class="hero" data-track="top">
  <h1>Unlocking Team Velocity</h1>
  <p>In today's fast-paced landscape, our robust platform empowers teams.</p>
  <button aria-label="Start now">Start now</button>
</div>
<script>const go = () => document.querySelector('[data-track="top"]');</script>
"""


def demo():
    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        (t / "a.html").write_text(PAGE)

        def after(body, name):
            (t / name).write_text(body)
            return compare(t / "a.html", t / name)

        # The good edit: every rule applied to the copy, nothing else touched.
        good = (PAGE.replace("Unlocking Team Velocity", "Deploys got faster")
                    .replace("In today's fast-paced landscape, our robust platform empowers teams.",
                             "Teams ship in nine minutes instead of forty."))
        assert not after(good, "good.html"), after(good, "good.html")

        # Each trap, one at a time, so a passing demo cannot be one check masking another.
        traps = [
            ("class renamed", PAGE.replace('class="hero"', 'class="banner"')),
            ("attribute dropped", PAGE.replace(' data-track="top"', "")),
            ("script edited", PAGE.replace("const go", "const start")),
            ("style edited", PAGE.replace("--brand:#0af", "--brand:#0bf")),
            ("tag added", PAGE.replace("<h1>", "<em><h1>")),
            ("comment injected", PAGE.replace("<div", "<!-- new -->\n<div")),
        ]
        for label, body in traps:
            f = after(body, "t.html")
            assert f, f"{label}: not caught"

        # The subtle one: a string that appears twice, edited in one place. The button label
        # and its aria-label must move together or the control stops matching.
        half = PAGE.replace(">Start now<", ">Get started<")
        f = after(half, "half.html")
        assert any("leaving" in x for x in f), f"one-of-a-pair edit not caught: {f}"

        # Moving both halves of the pair is a correct copy edit and must pass clean.
        both = PAGE.replace(">Start now<", ">Get started<").replace(
            'aria-label="Start now"', 'aria-label="Get started"')
        assert not after(both, "both.html"), after(both, "both.html")

        # Editing only the aria-label, leaving the visible label, is the same defect mirrored.
        aria_only = PAGE.replace('aria-label="Start now"', 'aria-label="Begin"')
        assert after(aria_only, "aria.html"), "aria-label half of the pair not caught"

        # Reformatting the prose without changing it is not an edit.
        reflow = PAGE.replace("In today's fast-paced landscape, our robust platform empowers teams.",
                              "In today's fast-paced landscape,\n     our robust platform empowers teams.")
        assert not after(reflow, "reflow.html"), "whitespace-only reflow should pass"

    print("  self-check: PASS (clean copy edit passes; class, attribute, script, style, tag "
          "and comment changes each caught alone; one-of-a-pair string edit caught in both "
          "directions; paired copy moved together passes; whitespace reflow ignored)")
    return 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    if len(sys.argv) < 3:
        raise SystemExit("usage: markup-diff.py before.html after.html | --demo")
    sys.exit(main(sys.argv[1], sys.argv[2]))
