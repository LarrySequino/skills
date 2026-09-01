#!/usr/bin/env python3
"""
preflight.py — showstopper gate for HTML artifacts. Deterministic only.

Runs in well under a second on a multi-megabyte page. Every check here is one a
script can DECIDE. Nothing in this file has an opinion, which is the whole point:
it is a gate, not a review. Anything needing judgment belongs in the full pass.

Checks:
  theme-only-color   a color declared ONLY inside a media/[data-theme] block, so it
                     never applies in the un-stamped default state. The classic
                     unreadable-artifact bug.
  no-body-bg         body sets no background, so it borrows the host's ground and
                     renders one theme's text on the other theme's surface.
  contrast           rules that set both a foreground and a background, resolved per
                     theme through var() tokens, checked against WCAG 2.2 AA. The floor
                     is 4.5 unless the same rule declares large text (>=24px, or
                     >=18.66px bold), which gets 3.0. An undeclared size takes 4.5.
  off-scale          padding/margin/gap values off the 4/8px scale.
  interactivity      script and handler counts, compared against a baseline file.
                     Catches a rewrite silently dropping behavior.

Usage:
    python3 preflight.py page.html
    python3 preflight.py page.html --baseline previous.html
    python3 preflight.py page.html --json

Exit code 1 if any BLOCK finding, else 0. Pure stdlib.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contrast import get_ratio, parse_color  # noqa: E402

SCALE = {0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80, 96, 128}
COLORISH = re.compile(r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\))")
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")


def strip_noise(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def blocks(html):
    """Every <style> body, with base64 payloads removed first."""
    html = re.sub(r'src="data:[^"]+"', 'src=""', html)
    return [strip_noise(m) for m in re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S)]


def rules(css):
    """(selector, declarations, enclosing_at_rule_or_None), brace-matched so nested
    at-rules are actually seen. A regex cannot do this; the earlier one silently
    dropped every @media block, which is the one place theme bugs hide."""
    out, i = [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            return out
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < len(css) and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1 : k - 1]
        if head.startswith("@"):
            for sel, b, inner in rules(body):
                out.append((sel, b, inner or head))
        else:
            out.append((head, body, None))
        i = k


def decls(body):
    d = {}
    for part in body.split(";"):
        if ":" in part:
            k, _, v = part.partition(":")
            d[k.strip().lower()] = v.strip()
    return d


def theme_of(sel, at):
    """Which theme state does this rule apply in?"""
    if at and "prefers-color-scheme: dark" in at.replace(" ", " "):
        return "dark-media"
    if '[data-theme="dark"]' in sel:
        return "dark-attr"
    if '[data-theme="light"]' in sel:
        return "light-attr"
    return "base"


# px per unit for the units that mean the same thing everywhere on the page. `em` is
# deliberately absent: it depends on the parent, so a rule saying 1.5em could be 24px or
# 12px, and guessing the generous reading is how large-text exemptions get handed out for
# free. Unknown size takes the body bar.
_UNIT_PX = {"px": 1.0, "rem": 16.0, "pt": 4 / 3}
_FONT_SIZE = re.compile(r"\s*(-?\d+(?:\.\d+)?)(px|rem|pt|em)?\s*$")


def text_bar(d):
    """(AA floor, why) for a rule's text. 3.0 is the floor for large text and non-text;
    body text needs 4.5. The rule has to SAY it is large text to get the lower bar —
    a size declared in some other rule, or in em, reads as unknown and takes 4.5."""
    m = _FONT_SIZE.match(d.get("font-size", ""))
    if not m or m.group(2) not in _UNIT_PX:
        return 4.5, "size not declared here, so the body bar applies"
    px = float(m.group(1)) * _UNIT_PX[m.group(2)]
    w = d.get("font-weight", "").strip().lower()
    bold = w in ("bold", "bolder") or (w.isdigit() and int(w) >= 700)
    if px >= 24 or (bold and px >= 18.66):
        return 3.0, f"{px:g}px{' bold' if bold else ''} large text"
    return 4.5, f"{px:g}px{' bold' if bold else ''} body text"


def collect(html):
    tokens = {"base": {}, "dark-media": {}, "dark-attr": {}, "light-attr": {}}
    uses = {}          # token name -> themes whose rules read it
    pairs, spacing, findings = [], [], []
    for css in blocks(html):
        for sel, body, at in rules(css):
            t = theme_of(sel, at)
            d = decls(body)
            for v in d.values():
                for name in VAR.findall(v):
                    uses.setdefault(name, set()).add(t)
            for k, v in d.items():
                if k.startswith("--") and COLORISH.search(v):
                    tokens[t][k] = v.strip()
                if k in ("padding", "margin", "gap", "row-gap", "column-gap") or k.startswith(
                    ("padding-", "margin-")
                ):
                    for num in re.findall(r"(-?\d+(?:\.\d+)?)px", v):
                        spacing.append((sel, k, float(num)))
            fg = d.get("color")
            bg = d.get("background-color") or d.get("background")
            if fg and bg and COLORISH.search(bg + fg + "x") or (fg and bg and VAR.search(fg + bg)):
                pairs.append((sel, t, fg, bg) + text_bar(d))
    return tokens, pairs, spacing, findings, uses


def resolve(val, tokens, theme):
    """Resolve var() chains against a theme, falling back to base."""
    for _ in range(6):
        m = VAR.search(val)
        if not m:
            break
        name = m.group(1)
        repl = tokens[theme].get(name) or tokens["base"].get(name)
        if repl is None:
            return None
        val = val[: m.start()] + repl + val[m.end() :]
    m = COLORISH.search(val)
    return m.group(1) if m else None


def check(html, baseline=None):
    tokens, pairs, spacing, out, uses = collect(html)

    # 1. colors that exist only in a themed block AND are read from outside it.
    # A token defined and consumed entirely inside dark mode is correct; blocking
    # it made a false positive the top finding, since a BLOCK now ranks first.
    base_names = set(tokens["base"])
    # dark-media and dark-attr are the same theme reached two ways. Treating them
    # as separate scopes reported a legitimate dark-only token twice, each block
    # citing the other dark scope as "outside".
    SAME = {"dark-media": {"dark-media", "dark-attr"}, "dark-attr": {"dark-media", "dark-attr"},
            "light-attr": {"light-attr", "base"}}
    reported = set()
    for theme in ("dark-media", "dark-attr", "light-attr"):
        for name in tokens[theme]:
            if name in base_names or name in reported:
                continue
            # defined in the sibling scope too? then it resolves wherever it is read
            if any(name in tokens[t] for t in SAME[theme] - {theme}):
                sibling_covered = True
            else:
                sibling_covered = False
            outside = sorted(uses.get(name, set()) - SAME[theme])
            if sibling_covered and not outside:
                continue
            if not outside:
                continue
            reported.add(name)
            out.append(
                dict(
                    level="BLOCK",
                    check="theme-only-color",
                    detail=f"{name} is read by {', '.join(outside)} rules but defined only in "
                    f"{theme}, so it never resolves in the un-stamped default state",
                )
            )

    # 2. body must paint its own ground
    body_bg = any(
        re.search(r"(^|,)\s*body\b", sel)
        and ("background" in decls(b) or "background-color" in decls(b))
        for css in blocks(html)
        for sel, b, _ in rules(css)
    )
    if not body_bg:
        out.append(
            dict(
                level="BLOCK",
                check="no-body-bg",
                detail="body sets no background; the page borrows the host's ground",
            )
        )

    # 3. contrast on rules that set both fg and bg, per theme
    seen = set()
    for sel, t, fg_raw, bg_raw, bar, why in pairs:
        # a rule authored in the base block still applies while a dark/light token set
        # is active, with different values. Checking only "base" misses exactly half
        # the failures, which is how the dark-theme miss below went unreported.
        # With no custom properties anywhere, every tokens[k] is empty and this used
        # to produce an empty scope list, so a plain-CSS page got no contrast pass
        # at all. Base is always a scope.
        scopes = ([k for k in tokens if tokens[k]] or ["base"]) if t == "base" else [t]
        for theme in scopes:
            fg, bg = resolve(fg_raw, tokens, theme), resolve(bg_raw, tokens, theme)
            if not fg or not bg:
                continue
            try:
                r = get_ratio(parse_color(fg), parse_color(bg))
            except Exception as e:
                # Swallowing this silently turned an uncheckable pair into a pass,
                # which is the one thing a gate must never do.
                out.append(dict(level="WARN", check="uncheckable-color",
                                detail=f"{sel}: could not compute {fg_raw} on {bg_raw} ({e}); "
                                       "check this pair by hand"))
                continue
            # The bar belongs in the dedup key: the same pair is a BLOCK at body size
            # and a WARN at 32px, and keying on color alone reports whichever rule the
            # parser happened to reach first.
            key = (round(r, 2), fg, bg, bar)
            if key in seen:
                continue
            seen.add(key)
            # 3.0 is the floor for large text and UI, not for body text. Blocking only
            # below 3.0 let a real AA body-text failure — anything in the 3.0-to-4.5
            # band — through as a warning.
            if r < 4.5:
                out.append(
                    dict(
                        level="BLOCK" if r < bar else "WARN",
                        check="contrast",
                        detail=f"{sel.strip()[:44]} [{theme}] {fg} on {bg} = {r:.2f}:1, "
                        f"needs {bar} ({why})",
                    )
                )

    # 3b. pinch-zoom disabled. WCAG 2.2 SC 1.4.4 wants text resizable to 200%, and a viewport
    #     that forbids it takes the page away from anyone who needs it larger. A BLOCK because
    #     it is exactly this file's class of defect: wrong in a state the reviewer is not
    #     looking at, since a desktop review never pinches. Every rationale for disabling zoom
    #     is itself the finding. Added 2026-08-22 from the source sweep; verified as a hole,
    #     since a page carrying it passed clean before.
    for m in re.finditer(r'<meta[^>]+name=["\']?viewport["\']?[^>]*>', html, re.I):
        content = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
        if not content:
            continue
        v = content.group(1)
        bad = []
        if re.search(r'user-scalable\s*=\s*(no|0)', v, re.I):
            bad.append("user-scalable=no")
        ms = re.search(r'maximum-scale\s*=\s*([\d.]+)', v, re.I)
        if ms and float(ms.group(1)) < 2:
            bad.append(f"maximum-scale={ms.group(1)}")
        if bad:
            out.append(dict(level="BLOCK", check="no-zoom",
                            detail=f"viewport {' and '.join(bad)} — text cannot reach 200% "
                                   f"(WCAG 2.2 SC 1.4.4); a desktop review never sees this"))

    # 4. spacing off the 4/8 scale
    bad = sorted({v for _, _, v in spacing if v == int(v) and abs(v) not in SCALE and abs(v) < 200})
    if bad:
        out.append(
            dict(
                level="WARN",
                check="off-scale",
                detail=f"{len(bad)} spacing values off the 4/8 scale: "
                + ", ".join(f"{int(v)}px" for v in bad[:10]),
            )
        )

    # 5. interactivity regression against a baseline
    if baseline is not None:
        def sig(doc):
            # a saved/rendered page carries the host's injected runtime before <title>;
            # counting it would report a phantom regression against an authored file
            if "frame-runtime" in doc[:4000] and "<title>" in doc:
                doc = doc[doc.index("<title>"):]
            doc = re.sub(r'src="data:[^"]+"', "", doc)
            return (
                len(re.findall(r"<script", doc)),
                len(re.findall(r"addEventListener", doc)),
                len(re.findall(r"<figure", doc)),
            )
        was, now = sig(baseline), sig(html)
        for i, name in enumerate(("script tags", "event listeners", "figures")):
            if now[i] < was[i]:
                out.append(
                    dict(
                        level="BLOCK",
                        check="interactivity",
                        detail=f"{name}: {was[i]} in baseline, {now[i]} now. A rewrite dropped "
                        f"behavior the old page had",
                    )
                )
    # 6. motion that never asks, and focus that cannot be seen. Both are conditions a
    #    reviewer looking at a static screenshot never enters, which is this file's whole
    #    remit. WARN rather than BLOCK: a page with no animation needs no media query and a
    #    page with no custom outline keeps the browser's, so absence is only a defect when
    #    the page took the thing away. Added 2026-08-31; 22 of 36 review runs checked the
    #    first by hand and 15 checked the second, none of them from a bundled check.
    css_all = " ".join(blocks(html))
    animated = re.search(r"@keyframes|animation\s*:|transition\s*:", css_all, re.I)
    if animated and not re.search(r"prefers-reduced-motion", css_all, re.I):
        out.append(dict(level="WARN", check="reduced-motion",
                        detail="the page animates and never honors prefers-reduced-motion — "
                               "vestibular users get the full motion (WCAG 2.2 SC 2.3.3)"))
    # outline:none is the removal. :focus-visible, or a :focus rule that paints something
    # back, is the replacement; a page that replaces it is fine and one that only removes is
    # not. The declaration that removes must not count as one that restores: the first
    # version of this matched `button:focus{outline:none}` as a restore, because the block
    # contains the word "outline", and reported the page clean. Caught by the negative
    # control, which is the only reason the check works.
    kills = re.search(r"outline\s*:\s*(none|0)\b", css_all, re.I)
    restores = re.search(r":focus-visible", css_all, re.I)
    if not restores:
        for m in re.finditer(r":focus\b[^{]*\{([^}]*)\}", css_all, re.I):
            body = re.sub(r"outline\s*:\s*(none|0)\b[^;]*;?", "", m.group(1), flags=re.I)
            if re.search(r"outline|box-shadow|border|background|ring", body, re.I):
                restores = m
                break
    if kills and not restores:
        out.append(dict(level="WARN", check="focus-invisible",
                        detail="outline is removed and nothing replaces it — keyboard users "
                               "lose the focus indicator (WCAG 2.2 SC 2.4.7 / 2.4.11)"))
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 0
    html = Path(args[0]).read_text(errors="ignore")
    base = None
    if "--baseline" in argv:
        base = Path(argv[argv.index("--baseline") + 1]).read_text(errors="ignore")
    found = check(html, base)
    if "--json" in argv:
        print(json.dumps(found, indent=1))
    else:
        blocking = [f for f in found if f["level"] == "BLOCK"]
        for f in found:
            mark = "BLOCK" if f["level"] == "BLOCK" else " warn"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        if not found:
            print("  clean: no showstoppers")
        print(f"\n{len(blocking)} blocking, {len(found) - len(blocking)} warnings.")
    return 1 if any(f["level"] == "BLOCK" for f in found) else 0


def demo():
    bad = """<style>
    :root { --ink: #111; }
    @media (prefers-color-scheme: dark) { :root { --ghost: #222; } }
    .x { color: var(--ink); background: #1a1a1a; border-color: var(--ghost); }
    .y { padding: 13px; margin: 7px; }
    </style><body><script>x.addEventListener('click',f)</script></body>"""
    f = check(bad)
    kinds = {x["check"] for x in f}
    assert "theme-only-color" in kinds, kinds     # --ghost only in dark
    assert "no-body-bg" in kinds, kinds           # body never painted
    assert "contrast" in kinds, kinds             # #111 on #1a1a1a is unreadable
    assert "off-scale" in kinds, kinds            # 13px / 7px
    drop = check(bad, baseline=bad + "<script>a.addEventListener('x',f)</script>")
    assert any(x["check"] == "interactivity" for x in drop), "baseline drop not detected"

    # The 3.0-to-4.5 band: the same ratio blocks as body text and warns as large text.
    zoom = ('<meta name="viewport" content="width=device-width, user-scalable=no">'
            '<style>body{background:#fff;color:#111}</style>')
    assert any(x["check"] == "no-zoom" and x["level"] == "BLOCK" for x in check(zoom)), "no-zoom missed"
    okz = ('<meta name="viewport" content="width=device-width, initial-scale=1">'
           '<style>body{background:#fff;color:#111}</style>')
    assert not any(x["check"] == "no-zoom" for x in check(okz)), "a normal viewport was flagged"

    band = """<style>
    body { background:#fff; }
    .small { font-size: 13px; color: #767676; background: #d9d9d9; }
    .big   { font-size: 32px; color: #767676; background: #d9d9d9; }
    </style><body></body>"""
    levels = {f["detail"].split()[0]: f["level"] for f in check(band) if f["check"] == "contrast"}
    assert levels.get(".small") == "BLOCK", levels    # 3.4:1 body text fails AA
    assert levels.get(".big") == "WARN", levels       # same pair at 32px passes AA large
    # A page that animates and never asks. The mirror case matters more: a page with no
    # animation at all must not be told to add a media query it has no use for.
    moves = "<style>body{background:#fff;color:#111}.c{animation:p 2s}</style><div class=c>x</div>"
    assert any(x["check"] == "reduced-motion" for x in check(moves))
    still = "<style>body{background:#fff;color:#111}.c{color:#222}</style><div class=c>x</div>"
    assert not any(x["check"] == "reduced-motion" for x in check(still)), \
        "a page with no motion was asked to honor prefers-reduced-motion"
    asks = ("<style>body{background:#fff;color:#111}.c{animation:p 2s}"
            "@media(prefers-reduced-motion:reduce){.c{animation:none}}</style><div class=c>x</div>")
    assert not any(x["check"] == "reduced-motion" for x in check(asks))

    # The removal must not read as its own replacement. The first version of this check
    # matched `button:focus{outline:none}` as a restore, because the block contains the word
    # "outline", and called the page clean.
    kill = "<style>body{background:#fff;color:#111}button:focus{outline:none}</style><button>g</button>"
    assert any(x["check"] == "focus-invisible" for x in check(kill)), \
        "outline:none with nothing replacing it was not caught"
    for ok in ("button:focus{outline:none}button:focus-visible{outline:2px solid #06c}",
               "a:focus{outline:none;box-shadow:0 0 0 3px #06c}"):
        page = f"<style>body{{background:#fff;color:#111}}{ok}</style><button>g</button>"
        assert not any(x["check"] == "focus-invisible" for x in check(page)), ok
    plain = "<style>body{background:#fff;color:#111}</style><button>g</button>"
    assert not any(x["check"] == "focus-invisible" for x in check(plain)), \
        "a page that never touches outline keeps the browser's and is not a defect"

    print("  self-check: PASS — all 7 checks fire on a deliberately broken page, the "
          "body/large-text contrast bars split correctly, and neither motion nor focus "
          "fires on a page that never took the thing away")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__ or "")
        sys.exit(0)
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main(sys.argv[1:]))
