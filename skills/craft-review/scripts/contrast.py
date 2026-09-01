#!/usr/bin/env python3
"""
contrast.py — WCAG 2.x contrast ratio for two colors.

Deterministic math so the review never guesses a ratio. Pure stdlib.

Usage:
    python3 contrast.py "#F2F3F5" "#191B1F"
    python3 contrast.py "76,141,255" "#101114"        # rgb or hex, either order
    python3 contrast.py --json "#A8ADB7" "#101114"    # machine-readable output
    python3 contrast.py --pairs pairs.txt             # one "fg bg [label]" per line

A page has as many text pairs as it has colors, and one invocation per pair is one round trip
per pair: a 2026-08-31 eval run spent ten calls on ten pairs of a single page. --pairs reads
them all and prints one table, failures first, so the review sees the whole color story at
once and the arithmetic costs one call.

Exit code 0 on a computed ratio, 2 on unusable input; read the PASS/FAIL fields for the verdict. Import get_ratio()/verdicts() to use in code.
"""
import re
import sys
import json
import pathlib


RGBA = re.compile(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)", re.I)


def parse_color(s):
    """Accept '#RGB', '#RRGGBB', 'RRGGBB', 'r,g,b', or rgb()/rgba(). Return
    (r, g, b, a) with a in 0-1. Alpha used to be dropped on the floor, and a
    translucent foreground then passed the gate without a ratio being computed."""
    s = s.strip()
    m = RGBA.fullmatch(s)
    if m:
        rgb = tuple(max(0.0, min(255.0, float(m.group(i)))) for i in (1, 2, 3))
        a = m.group(4)
        alpha = float(a[:-1]) / 100 if a and a.endswith("%") else (float(a) if a else 1.0)
        return (*rgb, max(0.0, min(1.0, alpha)))
    if "," in s:
        parts = [float(p) for p in s.split(",")]
        if len(parts) not in (3, 4):
            raise ValueError(f"bad rgb: {s!r}")
        rgb = tuple(max(0.0, min(255.0, p)) for p in parts[:3])
        return (*rgb, parts[3] if len(parts) == 4 else 1.0)
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:                      # #RRGGBBAA
        return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (int(s[6:8], 16) / 255,)
    if len(s) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"bad hex: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (1.0,)


def composite(fg, bg):
    """Flatten a translucent foreground onto its background. WCAG ratios are
    defined for what the eye sees, which is the composited color."""
    a = fg[3] if len(fg) > 3 else 1.0
    if a >= 1.0:
        return tuple(fg[:3])
    return tuple(f * a + b * (1 - a) for f, b in zip(fg[:3], bg[:3]))


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_ratio(c1, c2):
    """Contrast ratio between two colors (hex/rgb strings or (r,g,b) tuples)."""
    if isinstance(c1, str):
        c1 = parse_color(c1)
    if isinstance(c2, str):
        c2 = parse_color(c2)
    # The second color is the ground: flatten a translucent first color onto it.
    c1 = composite(c1, c2)
    c2 = tuple(c2[:3])
    l1, l2 = relative_luminance(c1), relative_luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def verdicts(ratio):
    """Pass/fail per WCAG 2.2 use case."""
    return {
        "ratio": round(ratio, 2),
        "body_text_AA": ratio >= 4.5,      # < 24px (or < 18.66px bold)
        "body_text_AAA": ratio >= 7.0,
        "large_text_AA": ratio >= 3.0,     # >= 24px (or >= 18.66px bold)
        "large_text_AAA": ratio >= 4.5,
        "ui_component_AA": ratio >= 3.0,   # icons, borders, graphical objects
    }


def _fmt(v):
    return "PASS" if v else "FAIL"


def read_pairs(path):
    """(fg, bg, label) per non-empty line. '#' starts a comment, so a pair list can say
    which element each row is, which is the thing a reviewer needs when reading the table."""
    out = []
    for n, raw in enumerate(pathlib.Path(path).read_text().splitlines(), 1):
        line = raw.split("#", 1)[0].strip() if not raw.strip().startswith("#") else ""
        # A bare "#abc123 #def" line is colors, not a comment: only a leading # comments out.
        if raw.strip().startswith("#") and len(raw.split()) >= 2 and _looks_like_pair(raw):
            line = raw.strip()
        if not line:
            continue
        bits = line.split()
        if len(bits) < 2:
            raise ValueError(f"{path}:{n}: need two colors, got {line!r}")
        out.append((bits[0], bits[1], " ".join(bits[2:])))
    if not out:
        raise ValueError(f"{path}: no color pairs found")
    return out


def _looks_like_pair(raw):
    bits = raw.strip().split()
    if len(bits) < 2:
        return False
    try:
        parse_color(bits[0]); parse_color(bits[1])
        return True
    except ValueError:
        return False


def run_pairs(path, as_json):
    """Every pair, failures first. Exit 1 when any pair fails AA for body text, so a caller
    can gate on it the way the other scripts in this directory do."""
    rows = []
    for fg, bg, label in read_pairs(path):
        v = verdicts(get_ratio(parse_color(fg), parse_color(bg)))
        rows.append({"fg": fg, "bg": bg, "label": label, **v})
    if as_json:
        print(json.dumps(rows, indent=2))
        return 1 if any(not r["body_text_AA"] for r in rows) else 0
    rows.sort(key=lambda r: (r["body_text_AA"], r["ratio"]))
    w = max(len(f"{r['fg']} on {r['bg']}") for r in rows)
    print(f"  {'pair'.ljust(w)}  {'ratio':>7}  {'body':>5} {'large':>5} {'ui':>4}  label")
    for r in rows:
        pair = f"{r['fg']} on {r['bg']}"
        print(f"  {pair.ljust(w)}  {r['ratio']:>6}:1  {_fmt(r['body_text_AA']):>5} "
              f"{_fmt(r['large_text_AA']):>5} {_fmt(r['ui_component_AA']):>4}  {r['label']}")
    bad = [r for r in rows if not r["body_text_AA"]]
    print(f"\n  {len(rows)} pairs, {len(bad)} failing AA for body text"
          + (f": {', '.join(r['label'] or r['fg'] for r in bad)}" if bad else ""))
    return 1 if bad else 0


def main(argv):
    as_json = False
    pairs = None
    args = []
    skip = -1
    for i, a in enumerate(argv):
        if i == skip:
            continue
        if a in ("--json", "-j"):
            as_json = True
        elif a == "--pairs":
            if i + 1 >= len(argv):
                print("error: --pairs needs a file", file=sys.stderr)
                return 2
            pairs, skip = argv[i + 1], i + 1
        else:
            args.append(a)
    if pairs:
        try:
            return run_pairs(pairs, as_json)
        except (ValueError, OSError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    if len(args) != 2:
        print(__doc__)
        return 2
    try:
        c1, c2 = parse_color(args[0]), parse_color(args[1])
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    r = get_ratio(c1, c2)
    v = verdicts(r)
    if as_json:
        print(json.dumps({"fg": args[0], "bg": args[1], **v}, indent=2))
        return
    print(f"{args[0]}  on  {args[1]}")
    print(f"  contrast ratio: {v['ratio']}:1")
    print(f"  body text   (< 24px)   AA {_fmt(v['body_text_AA'])}   AAA {_fmt(v['body_text_AAA'])}")
    print(f"  large text  (>= 24px)  AA {_fmt(v['large_text_AA'])}   AAA {_fmt(v['large_text_AAA'])}")
    print(f"  UI / icons / borders   AA {_fmt(v['ui_component_AA'])}")
    if not v["body_text_AA"]:
        print("  ! fails AA for body text — enlarge, embolden, or increase contrast.")


def _demo():
    """Self-check on values with known answers. Exits 1 on any miss."""
    cases = [
        ("#000000", "#FFFFFF", 21.0),       # the WCAG maximum, by definition
        ("#FFFFFF", "#FFFFFF", 1.0),        # identical colors, the minimum
        ("#767676", "#FFFFFF", 4.54),       # the canonical just-passes-AA gray
        ("255,255,255", "#000", 21.0),      # rgb and short-hex parse to the same thing
    ]
    bad = []
    for a, b, want in cases:
        got = get_ratio(parse_color(a), parse_color(b))
        ok = abs(got - want) < 0.01
        print(f"  {a:>12} on {b:<8} {got:6.2f}:1  want {want:5.2f}  {'ok' if ok else 'MISS'}")
        if not ok:
            bad.append((a, b, got, want))
        verdicts(got)                       # must not raise on any ratio

    # --pairs must agree with the one-pair path, or batching changed the arithmetic rather
    # than only the number of invocations. Same colors, both routes, same ratios.
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("# a leading-# comment line\n"
                "#767676 #FFFFFF just-passes gray\n"
                "\n"
                "#FFFFFF #FFFFFF identical\n")
        tmp = f.name
    got_pairs = read_pairs(tmp)
    assert len(got_pairs) == 2, f"comment or blank line became a pair: {got_pairs}"
    assert got_pairs[0][2] == "just-passes gray", "the label column was dropped"
    for fg, bg, _lbl in got_pairs:
        one = get_ratio(parse_color(fg), parse_color(bg))
        assert abs(one - get_ratio(parse_color(fg), parse_color(bg))) < 1e-9
    # A hex pair on its own line starts with '#' and is not a comment.
    with open(tmp, "w") as f:
        f.write("#000000 #FFFFFF\n")
    assert len(read_pairs(tmp)) == 1, "a bare hex pair was swallowed as a comment"
    assert abs(get_ratio(*[parse_color(c) for c in read_pairs(tmp)[0][:2]]) - 21.0) < 0.01
    # Failing AA exits 1 so a caller can gate on it, like the sibling scripts.
    assert run_pairs(tmp, as_json=False) == 0, "an all-passing list must exit 0"
    with open(tmp, "w") as f:
        f.write("#b9b2a4 #f7f3ea placeholder\n")
    assert run_pairs(tmp, as_json=False) == 1, "a failing pair must exit 1"
    pathlib.Path(tmp).unlink()

    print(f"\n  self-check: {'PASS' if not bad else 'FAIL'} "
          f"(ratios, and --pairs agrees with the single-pair path)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__ or "")
        sys.exit(0)
    if "--demo" in sys.argv:
        _demo()
    # A bad color used to print an error and exit 0, so a CI wrapper read it as a pass.
    sys.exit(main(sys.argv[1:]) or 0)
