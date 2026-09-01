/*
 * collect-boxes.js — emit symmetry.py's JSON schema from a live HTML page.
 *
 * symmetry.py already does the analysis; it only ever needed boxes. CSS has no
 * geometry until a layout engine runs it, so the boxes have to come from a real
 * browser. This is the adapter, not a second analyzer:
 *
 *     browser:  copy(collectBoxes())            // or run via an automation tool
 *     shell:    python3 symmetry.py boxes.json
 *
 * Options: collectBoxes({ root, gridBase, tolerance, minArea, maxFrames })
 *
 * False-positive discipline, matching symmetry.py's own:
 *   - only elements that lay out as a block/flex/grid and actually contain
 *     element children with real boxes count as frames
 *   - pairs are auto-detected ONLY for siblings with an identical class list,
 *     which is the "two cards side by side" case and almost nothing else
 *   - centering is never inferred. Annotate the element with
 *     data-expect="center" | "center-h" | "center-v" to have it checked.
 */
function collectBoxes(opts) {
  opts = opts || {};
  var root = opts.root || document.body;
  var minArea = opts.minArea || 400;         // ignore slivers and icons
  var maxFrames = opts.maxFrames || 400;     // keep the payload sane on big pages
  var LAYOUT = { block: 1, flex: 1, grid: 1, 'inline-block': 1, 'inline-flex': 1, 'list-item': 1 };
  // Type is not a container. A <span> inside an <h2> is not a content inset, and
  // treating it as one reports the position of a word. Headings and paragraphs are
  // excluded as frames; they are still measured as children of whatever holds them.
  // Page-level elements are excluded for the same reason: a centered max-width
  // child makes body's inset (viewport - width) / 2, which is arithmetic, not a
  // decision, and it changes on every resize.
  var NOT_A_FRAME = { H1: 1, H2: 1, H3: 1, H4: 1, H5: 1, H6: 1, P: 1, FIGCAPTION: 1,
                      BODY: 1, HTML: 1 };

  var names = Object.create(null);
  function nameFor(el) {
    var base = el.tagName.toLowerCase();
    if (el.id) base += '#' + el.id;
    else if (el.className && typeof el.className === 'string') {
      var c = el.className.trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
      if (c) base += '.' + c;
    }
    names[base] = (names[base] || 0) + 1;
    return names[base] > 1 ? base + ' (' + names[base] + ')' : base;
  }

  function box(el) {
    var r = el.getBoundingClientRect();
    return {
      x: Math.round(r.left + scrollX),
      y: Math.round(r.top + scrollY),
      w: Math.round(r.width),
      h: Math.round(r.height)
    };
  }

  function laidOut(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || !LAYOUT[cs.display]) return false;
    var r = el.getBoundingClientRect();
    return r.width * r.height >= minArea;
  }

  var frames = [];
  var bySignature = Object.create(null);

  (function walk(el) {
    if (frames.length >= maxFrames) return;
    var kids = [];
    for (var i = 0; i < el.children.length; i++) {
      if (laidOut(el.children[i])) kids.push(el.children[i]);
    }
    if (kids.length && laidOut(el) && !NOT_A_FRAME[el.tagName]) {
      var f = { name: nameFor(el), bounds: box(el), children: [] };
      var expect = el.getAttribute && el.getAttribute('data-expect');
      if (expect) f.expect = expect;
      for (var j = 0; j < kids.length; j++) {
        f.children.push({ name: kids[j].tagName.toLowerCase(), bounds: box(kids[j]) });
      }
      frames.push(f);
      // signature = parent identity + own class list; identical siblings pair up
      var sig = (el.parentElement ? el.parentElement.tagName : 'root') + '|' +
                (typeof el.className === 'string' ? el.className.trim() : '') + '|' +
                el.tagName;
      (bySignature[sig] = bySignature[sig] || []).push(f.name);
    }
    for (var k = 0; k < el.children.length; k++) walk(el.children[k]);
  })(root);

  var pairs = [];
  Object.keys(bySignature).forEach(function (sig) {
    var group = bySignature[sig];
    if (group.length < 2 || !sig.split('|')[1]) return;   // unclassed elements are not a pair
    for (var i = 1; i < group.length; i++) pairs.push([group[0], group[i]]);
  });

  // Interactive elements, collected separately and deliberately outside the frame walk.
  // A frame needs element children and a minimum area; a 24x24 icon button has neither, and
  // it is exactly the control a target-size check exists to catch. Every review run on
  // 2026-08-31 measured hit areas by hand because this was not here.
  //
  // Only what the platform itself treats as operable, plus explicit ARIA and tabindex. A
  // div with a click handler is invisible to the DOM and is not guessed at, the same
  // false-positive discipline the frame walk keeps.
  var INTERACTIVE = 'a[href], button, input, select, textarea, summary, ' +
                    '[role=button], [role=link], [role=checkbox], [role=radio], ' +
                    '[role=switch], [role=tab], [role=menuitem], [tabindex]';
  var controls = [];
  var seen = [];
  var nodes = (opts.root || document).querySelectorAll(INTERACTIVE);
  for (var c = 0; c < nodes.length && controls.length < maxFrames; c++) {
    var el = nodes[c];
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    // A disabled control is exempt from the target-size rule, per thresholds.md.
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    if (el.getAttribute('tabindex') === '-1') continue;   // not in the tab order, not operable
    // WCAG 2.5.8's own inline exception: a target whose size is constrained by the
    // line-height of the text around it is exempt. display:inline IS that constraint --
    // width and height do not apply to it, so its box is the line box and nothing else.
    // Without this, every text link on a page is a Major finding: six of them on
    // tasteful-default.html, which the suite documents as measurably clean.
    if (cs.display === 'inline') continue;
    var b = box(el);
    if (!b.w || !b.h) continue;                            // zero-box: not rendered
    if (seen.indexOf(el) !== -1) continue;
    seen.push(el);
    controls.push({ name: nameFor(el), tag: el.tagName.toLowerCase(),
                    display: cs.display, bounds: b });
  }

  return {
    // In HTML, width and height are computed by the layout engine from the
    // container and the content; they are not authored the way a Figma frame's
    // size is. Grid-checking them reports the viewport, not a decision.
    // Insets still come from authored padding, so those stay meaningful.
    derived_sizes: true,
    grid_base: opts.gridBase || 8,
    tolerance: opts.tolerance == null ? 1 : opts.tolerance,
    frames: frames,
    pairs: pairs,
    controls: controls
  };
}

if (typeof module !== 'undefined') module.exports = { collectBoxes: collectBoxes };
