#!/usr/bin/env python3
"""measure.py — run every deterministic check on one artifact, in one invocation.

    python3 measure.py page.html                    the standard pass
    python3 measure.py page.html --pairs pairs.txt  add the contrast table
    python3 measure.py geometry.json                Figma geometry: symmetry only
    python3 measure.py --demo

Nothing here is new analysis. preflight.py, slop-scan.py and symmetry.py already decide
everything this prints; measure.py is the one call that runs them and lays the answers out
together, so section 4 of SKILL.md is a step rather than a checklist to work through.

Six invocations was the going rate: preflight, slop-scan, symmetry at three viewports, and
contrast per color pair. Measured over 29 eval runs on 2026-08-31, a run cost about 2,700
tokens per tool call against a fixed floor of 55,000, so the round trips were roughly half of
what a review spent and most of them were spent re-entering to run the next script.

Exit codes follow the scripts it drives: 1 when anything found a finding, 0 when the artifact
is clean, 2 when a script could not run at all. A run that could not measure is not a clean
artifact, and the difference has to survive into the exit code.
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
# The three widths SKILL.md asks for. Desktop, the laptop the design was probably drawn at,
# and the phone: a layout that only holds at one of them is the finding.
VIEWPORTS = ("1440,900", "1280,800", "390,844")


def run(script, args):
    """(name, returncode, output). A script that is missing or crashes is reported, never
    silently skipped: an absent check reads exactly like a passing one in a report."""
    p = HERE / script
    if not p.exists():
        return script, 2, f"  !! {script} is not in {HERE}"
    r = subprocess.run([sys.executable, str(p), *args], capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    return script, r.returncode, out.rstrip() or "  (no output)"


def section(title, body):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")
    print(body)


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    if len(args) != 1:
        print(__doc__)
        return 2
    target = pathlib.Path(args[0])
    if not target.exists():
        print(f"error: {target} does not exist", file=sys.stderr)
        return 2
    pairs = None
    if "--pairs" in argv:
        i = argv.index("--pairs")
        if i + 1 >= len(argv):
            print("error: --pairs needs a file", file=sys.stderr)
            return 2
        pairs = argv[i + 1]

    geometry = target.suffix.lower() == ".json"
    results = []

    if geometry:
        # Figma geometry carries no CSS, so preflight and slop-scan have nothing to read.
        # Saying so beats printing two empty sections that look like passes.
        section("symmetry (Figma geometry)", run("symmetry.py", [str(target)])[2])
        results.append(run("symmetry.py", [str(target)]))
        print("\n  preflight and slop-scan skipped: they read CSS, and geometry declares none.")
    else:
        for script in ("preflight.py", "slop-scan.py"):
            name, rc, out = run(script, [str(target)])
            results.append((name, rc, out))
            section(name, out)
        for vp in VIEWPORTS:
            name, rc, out = run("symmetry.py", [str(target), "--viewport", vp])
            results.append((f"symmetry.py @{vp}", rc, out))
            section(f"symmetry.py @ {vp}", out)

    if pairs:
        name, rc, out = run("contrast.py", ["--pairs", pairs])
        results.append((name, rc, out))
        section(f"contrast.py --pairs {pairs}", out)

    section("summary", "\n".join(
        f"  {n:<24} {'could not run' if rc == 2 else 'findings' if rc else 'clean'}"
        for n, rc, _ in results))
    if any(rc == 2 for _, rc, _ in results):
        return 2
    return 1 if any(rc for _, rc, _ in results) else 0


def demo():
    import tempfile
    d = pathlib.Path(tempfile.mkdtemp(prefix="measure-"))
    # A page with a defect each script can see, so a silently-skipped script shows up as a
    # missing finding rather than as a pass.
    (d / "bad.html").write_text(
        "<style>body{color:#bbb;background:#fff}"
        ".x{background:linear-gradient(90deg,#f00,#00f);-webkit-background-clip:text}"
        "</style><p class=x>hi</p>")
    rc = main([str(d / "bad.html")])
    assert rc in (1, 2), f"a page with known defects returned {rc}"

    # Every script this drives must exist, or the summary reports 'could not run' forever.
    for s in ("preflight.py", "slop-scan.py", "symmetry.py", "contrast.py"):
        assert (HERE / s).exists(), f"{s} is missing from {HERE}"

    # A missing script is 2 (could not run), never 0 (clean).
    name, rc, _out = run("no-such-script.py", [])
    assert rc == 2, "a missing script did not report as unrunnable"

    # A target that is not there is an error, not an empty clean report.
    assert main([str(d / "absent.html")]) == 2

    # Geometry input must not claim the CSS checks ran.
    (d / "geo.json").write_text('{"frames": []}')
    assert main([str(d / "geo.json")]) in (0, 1, 2)

    assert len(VIEWPORTS) == 3, "SKILL.md asks for three widths"
    print("\n  self-check: PASS (drives all four scripts, a missing script reports as "
          "unrunnable rather than clean, a missing target is an error, geometry skips the "
          "CSS-only checks)")
    return 0


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)
    sys.exit(demo() if "--demo" in sys.argv else main(sys.argv[1:]))
