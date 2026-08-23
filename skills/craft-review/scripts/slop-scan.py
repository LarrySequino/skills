#!/usr/bin/env python3
"""
slop-scan.py — deterministic detector for the mechanically-checkable AI design tells.

Companion to this skill's Group E (distinctiveness / anti-slop). It does NOT judge
taste — it flags the reflex patterns from `design-tropes.md` that can be found statically in
HTML/CSS source, so a human (or the review pass) can decide whether each is earned or slop.

Usage:
    python3 slop-scan.py file1.html [file2.css ...]
    python3 slop-scan.py --demo          # run against a tiny built-in sample
    python3 slop-scan.py --json file.html

Checks (each maps to an entry in design-tropes.md):
  - pure-black-white     #000 / #fff (and rgb/rgba equivalents) used as color
  - gradient-text        gradient + background-clip:text (gradient text as decoration)
  - layout-animation     transition/animation on layout props (width/height/top/left/margin/...)
  - uniform-shadow       the same box-shadow value repeated across many elements
  - glass-default        many backdrop-filter:blur surfaces (glassmorphism-by-default)
  - side-stripe-border   decorative border-left/right accent stripes
  - one-duration-motion  a single transition duration used everywhere

Exit codes: 0 if no findings, 1 if any findings (so it can gate CI). `--demo` prints the sample
findings and then a self-check, and exits 0 when that self-check passes, 1 only if it fails.
--json prints machine output.

Pure stdlib. No installs. Heuristic by design: report, don't fail the build on its own.
"""
import sys, re, json, colorsys

# ---------- helpers ----------

def _strip_comments(css):
    return re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)

HEX = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b')

def _hex_to_rgb(h):
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in range(0, 6, 2))

def _is_pure_bw(h):
    rgb = _hex_to_rgb(h)
    return rgb in ((0, 0, 0), (255, 255, 255))

def _hue_of(h):
    r, g, b = (c / 255 for c in _hex_to_rgb(h))
    hh, _, s = colorsys.rgb_to_hls(r, g, b)[0], 0, colorsys.rgb_to_hls(r, g, b)[2]
    return hh * 360, s

def _line_of(text, idx):
    return text.count('\n', 0, idx) + 1

# ---------- checks ----------

LAYOUT_PROPS = ('width', 'height', 'top', 'left', 'right', 'bottom',
                'margin', 'padding', 'inset', 'flex-basis')

def scan_text(name, text):
    findings = []
    css = _strip_comments(text)

    # 1. pure black / white as color (ignore #000 inside device-frame bezels is impossible to know;
    #    flag but note context in design-tropes). Also catch rgb(0,0,0)/rgb(255,255,255).
    pure = []
    for m in HEX.finditer(css):
        if _is_pure_bw(m.group(1)):
            pure.append((_line_of(text, m.start()), m.group(0)))
    for m in re.finditer(r'rgba?\(\s*0\s*,\s*0\s*,\s*0\s*(?:,\s*1(?:\.0)?\s*)?\)', css):
        pure.append((_line_of(text, m.start()), 'rgb(0,0,0)'))
    for m in re.finditer(r'rgba?\(\s*255\s*,\s*255\s*,\s*255\s*(?:,\s*1(?:\.0)?\s*)?\)', css):
        pure.append((_line_of(text, m.start()), 'rgb(255,255,255)'))
    # The catalog entry became "pure black ON pure white" on 2026-08-22: #fff as a surface is the
    # most common ground on the web, and flagging either token alone contradicted the entry it
    # claims to implement. Require both to appear.
    has_black = any(sn in ('#000', '#000000', 'rgb(0,0,0)') for _, sn in pure)
    has_white = any(sn in ('#fff', '#ffffff', 'rgb(255,255,255)') for _, sn in pure)
    if pure and has_black and has_white:
        findings.append(('pure-black-white', 'low',
                         f'{len(pure)} pure #000/#fff color use(s) — real materials are never pure; '
                         f'use near-black / off-white',
                         pure[:8]))

    # 2. gradient text as decoration
    gt = []
    for m in re.finditer(r'background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text', css):
        # only a tell if a gradient is nearby in the same rule block
        window = css[max(0, m.start() - 400):m.start() + 100]
        if 'gradient' in window:
            gt.append((_line_of(text, m.start()), 'background-clip:text + gradient'))
    if gt:
        findings.append(('gradient-text', 'med',
                         f'{len(gt)} gradient-text instance(s) — reserve gradient text for a '
                         f'deliberate brand mark, not decoration', gt[:8]))

    # 3. transition/animation on layout properties
    la = []
    for m in re.finditer(r'transition\s*:\s*([^;{}]+)', css):
        val = m.group(1)
        # `transition: all` is the same defect written shorter, and the commonest form of it:
        # it animates whatever happens to change, so a hover that also nudges padding animates
        # layout without anyone deciding to. Named independently by two sources in the
        # 2026-08-22 harvest, and verified as a hole — a page whose only motion is
        # `transition: all .2s` scanned clean before this.
        if re.search(r'(^|[\s,])all([\s,]|$)', val):
            la.append((_line_of(text, m.start()), 'transition: all'))
            continue
        for prop in LAYOUT_PROPS:
            if re.search(r'(^|[\s,])' + prop + r'([\s,]|$)', val):
                la.append((_line_of(text, m.start()), f'transition: …{prop}…'))
                break
    if la:
        findings.append(('layout-animation', 'med',
                         f'{len(la)} transition(s) on layout properties — animate transform/opacity, '
                         f'not width/height/top/left (jank + reflow). `all` counts: it animates '
                         f'whatever changes, so name the properties you meant', la[:8]))

    # 4. uniform shadow: same box-shadow value repeated a lot
    shadows = {}
    for m in re.finditer(r'box-shadow\s*:\s*([^;{}]+)', css):
        val = re.sub(r'\s+', ' ', m.group(1).strip().lower())
        if val in ('none', 'inherit'):
            continue
        shadows.setdefault(val, []).append(_line_of(text, m.start()))
    for val, lines in shadows.items():
        if len(lines) >= 5:
            findings.append(('uniform-shadow', 'low',
                             f'same box-shadow repeated {len(lines)}× — map shadows to a real '
                             f'elevation scale; most elements sit flat',
                             [(l, val[:48]) for l in lines[:6]]))

    # 5. RETIRED 2026-08-22 with the catalog entry. The retirement pass found one instance
    #    across roughly sixty current marketing sections, while the check fires on any indigo
    #    brand ramp, so it was costing more in false positives than it caught. The entry is in
    #    design-tropes.md under ## Historical and this check is one `git revert` away if the
    #    trope comes back. The retirement rests on absence of evidence, which is the weaker
    #    kind: see the close-call note in the harvest log.

    # 6. glassmorphism by default: many backdrop-filter blur surfaces
    glass = [(_line_of(text, m.start()), 'backdrop-filter:blur')
             for m in re.finditer(r'backdrop-filter\s*:\s*[^;{}]*blur', css)]
    # Raised from 4 on 2026-08-22. A sticky translucent header plus a modal plus any component
    # set built on iOS 26's system material clears four without a single decorative choice, and
    # the entry now reads "glassmorphism where nothing is layered". Eight is a surface count that
    # still says "this is the default", not "the platform does this".
    if len(glass) >= 8:
        findings.append(('glass-default', 'low',
                         f'{len(glass)} backdrop-blur surfaces — use translucency only where a real '
                         f'layer floats over scrolling content, not as default decoration', glass[:8]))

    # 7. decorative side-stripe borders
    stripes = []
    for m in re.finditer(r'border-(left|right)\s*:\s*([^;{}]+)', css):
        w = re.search(r'(\d+(?:\.\d+)?)px', m.group(2))
        if w and 1 <= float(w.group(1)) <= 6 and ('var(' in m.group(2) or HEX.search(m.group(2))
                                                   or 'rgb' in m.group(2)):
            stripes.append((_line_of(text, m.start()), m.group(0)[:48]))
    if len(stripes) >= 2:
        findings.append(('side-stripe-border', 'low',
                         f'{len(stripes)} colored side-stripe border(s) — a recognizable reflex; '
                         f'reserve for a genuine quote/citation semantic', stripes[:8]))

    # 8. one-duration motion: a single transition duration dominates
    durs = {}
    for m in re.finditer(r'transition(?:-duration)?\s*:\s*[^;{}]*?(\d+(?:\.\d+)?)(m?s)', css):
        v = float(m.group(1)) * (1000 if m.group(2) == 's' else 1)
        durs[v] = durs.get(v, 0) + 1
    total = sum(durs.values())
    if total >= 8 and durs:
        top_dur, top_n = max(durs.items(), key=lambda kv: kv[1])
        if top_n / total >= 0.8:
            findings.append(('one-duration-motion', 'low',
                             f'{top_n}/{total} transitions use {top_dur:g}ms — duration should track '
                             f'distance & importance, not one value for everything',
                             [(0, f'{top_dur:g}ms ×{top_n}')]))

    return findings


def main(argv):
    as_json = '--json' in argv
    argv = [a for a in argv if a != '--json']

    if '--demo' in argv:
        files = [('demo.html', DEMO)]
    else:
        paths = [a for a in argv if not a.startswith('--')]
        if not paths:
            print(__doc__)
            return 0
        files = []
        for p in paths:
            try:
                files.append((p, open(p, encoding='utf-8', errors='replace').read()))
            except OSError as e:
                print(f'skip {p}: {e}', file=sys.stderr)

    results = {}
    total = 0
    for name, text in files:
        f = scan_text(name, text)
        results[name] = f
        total += len(f)

    if as_json:
        print(json.dumps({n: [{'check': c, 'severity': s, 'message': msg,
                                'hits': [{'line': ln, 'snippet': sn} for ln, sn in ex]}
                               for c, s, msg, ex in fs]
                          for n, fs in results.items()}, indent=2))
        return 1 if total else 0

    SEV = {'high': '🔴', 'med': '🟠', 'low': '🔵'}
    for name, fs in results.items():
        print(f'\n=== {name} ===')
        if not fs:
            print('  clean — no mechanical design tells found')
            continue
        for check, sev, msg, ex in fs:
            print(f'  {SEV.get(sev, "•")} [{check}] {msg}')
            for ln, sn in ex:
                loc = f'L{ln}' if ln else '—'
                print(f'        {loc}: {sn}')
    print(f'\n{total} finding(s) across {len(files)} file(s). '
          f'Heuristic — each is a prompt to check intent, not an automatic failure.')
    return 1 if total else 0


def _selfcheck():
    """Every tell planted in DEMO fires, and nothing fires on CLEAN. Exits 1 on any miss."""
    shorthand = {c for c, _, _, _ in scan_text('x.css', ALL_SHORTHAND)}
    named = {c for c, _, _, _ in scan_text('x.css', NAMED_PROPS)}
    if 'layout-animation' not in shorthand:
        print('  MISS: `transition: all` not caught')
    if 'layout-animation' in named:
        print('  MISS: naming transform and opacity was flagged')
    fired = {c for c, _, _, _ in scan_text('demo.html', DEMO)}
    missing = sorted(PLANTED - fired)
    clean = scan_text('clean.html', CLEAN)
    for c in missing:
        print(f'  MISS: planted [{c}] not found')
    for c, _, msg, _ in clean:
        print(f'  MISS: clean source flagged [{c}] {msg}')
    ok = not missing and not clean and 'layout-animation' in shorthand and 'layout-animation' not in named
    print(f'  self-check: {"PASS" if ok else "FAIL"} '
          f'({len(PLANTED) - len(missing)}/{len(PLANTED)} planted tells found, '
          f'{len(clean)} false positive(s) on clean source)')
    return 0 if ok else 1


DEMO = """<style>
  :root{ --accent:#7c3aed; }
  body{ background:#fff; color:#000; }
  .card{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card2{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card3{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card4{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  .card5{ box-shadow:0 4px 12px rgba(0,0,0,.1); }
  h1{ background:linear-gradient(90deg,#7c3aed,#3b82f6); -webkit-background-clip:text; }
  .panel{ transition:width .2s, opacity .2s; }
  .nav{ backdrop-filter:blur(10px); }
  .callout{ border-left:3px solid var(--accent); }
</style>"""

# The tells DEMO plants, by check name. Update together with DEMO.
PLANTED = {'pure-black-white', 'gradient-text', 'layout-animation',
           'uniform-shadow'}

# `transition: all` and its control, added 2026-08-22. The demo page uses the explicit-property
# form, so without these the shorter and commoner form has no case behind it.
ALL_SHORTHAND = ".btn{ transition:all .2s ease; }"
NAMED_PROPS   = ".btn{ transition:transform .2s ease, opacity .2s ease; }" 

# Same shapes, done deliberately: near-black on off-white, two shadows on a real elevation
# scale, motion on transform/opacity with durations that track distance. Must stay clean.
CLEAN = """<style>
  :root{ --ink:#1a1d21; --paper:#fbfaf7; --accent:#b4541e; }
  body{ background:var(--paper); color:var(--ink); }
  .card{ box-shadow:0 1px 2px rgba(26,29,33,.08); }
  .modal{ box-shadow:0 12px 32px rgba(26,29,33,.18); }
  .btn{ transition:transform .12s ease, opacity .12s ease; }
  .sheet{ transition:transform .32s cubic-bezier(.2,.8,.2,1); }
</style>"""

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__ or '')
        sys.exit(0)
    code = main(sys.argv[1:])
    sys.exit(_selfcheck() if '--demo' in sys.argv else code)
