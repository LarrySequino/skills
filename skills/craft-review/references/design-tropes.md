# AI Design Tropes to Avoid

The visual counterpart to `deslop`'s `tropes.md`. A catalog of the patterns that make an interface
look *generated* rather than *designed* — the defaults a model reaches for when it isn't grounded in
a specific product, audience, and mood. Use it two ways: as a checklist when auditing a design, and
as context when generating one, so the first draft isn't already slop.

Each entry is: **the tell → why a model reaches for it → what it looks like → what to do instead.**
A single instance is rarely fatal; the tell is the *reflex* — reaching for it by default, everywhere,
without a reason the product forced.

The meta-test sits above the whole catalog:

> **The category-reflex test.** *First-order:* could someone guess this design's theme and palette
> from the product's category alone? ("fintech → navy + gold," "AI tool → dark + purple," "health →
> teal + white"). If yes, it's reflex, not decision. *Second-order:* could they guess the aesthetic
> *family* from the category plus the obvious anti-reference ("developer tool, so *not* corporate →
> therefore terminal-green editorial")? If yes, dig further. Ground the decision in a physical scene —
> who uses this, where, in what light and mood — until the scene forces the answer.

---

## Layout & structure

### The hero-metric template
Three or four big numbers in a row ("10k+ users · 99.9% uptime · 4.9★") under a centered headline.
The strip is a live convention that careful teams ship (Ramp, Mixpanel, Amplemarket, V7, 2026), so
the form on its own is not the tell. The tell is the content: round vanity figures nobody could
check, or numbers supporting no claim the page makes. **Instead:** use figures the product can stand
behind, and put each one beside the claim it evidences. If you cannot source a number, cut it.

### The identical card grid
Every piece of content forced into the same rounded rectangle, same padding, same shadow, tiled 3×N.
It's the model's default container because it's safe and uniform — and uniformity is exactly what
reads as machine-made. **Instead:** vary card size/weight by importance; let some content breathe
without a box. Nested cards (a card inside a card) are a near-certain tell.

### Centered-hero + subhead + two buttons
The landing-page reflex: centered H1, one-line subhead, a filled button next to a ghost button.
**Instead:** justify the composition from the content — asymmetry, a real image, a single primary
action. Two buttons of near-equal weight means you haven't decided what the primary action is.

### Everything in a container
Wrapping every region in a bordered/elevated panel so the page becomes a stack of boxes. **Instead:**
use whitespace and alignment to group; a border is a last resort, not the default separator.

### Numbered labels on an unordered set
*01 Discover / 02 Design / 03 Deliver*. Numbering a genuinely ordered process is correct information
design, and shipped work is full of it done well (Apollo, Squarespace, Trawelt, Craft Agency, 2026).
The tell is digits on a set with no order, imitating editorial structure without adding any.
**Instead:** number only what someone must do or read in sequence; on an unordered set, cut the
digits and let hierarchy and rhythm carry the page.

### Geometrically centered asymmetric glyphs
Play triangles, chevrons, and other asymmetric icons centered by the math look off-center to the
eye; automated alignment checks pass while the composition reads as sloppy. **Instead:** optical
centering — nudge the glyph toward its visual mass (a play icon shifts slightly right) and trust the
eye over the bounding box.

## Color

### Category-reflex palettes
Reaching for whatever palette the category is assumed to wear. The specific mappings age fast, so
test the reflex rather than the list: the 2020s set (navy+gold finance, teal+white health,
dark+purple AI) no longer describes what ships. Consumer fintech in 2026 runs coral, mint and
electric blue (Monzo, N26, Cleo); AI products run black or orange about as often as purple (Grok,
Mistral, FLORA). **Instead:** derive the palette from the product's mood and scene, then check
whether a competitor in the same category could swap it in unchanged.

### Pure black on pure white
`#000` text on a `#fff` ground at reading size, with no tuned neutral anywhere in the palette. Pure
white as a *surface* is not a tell on its own; it is the most common page ground on the web and
plenty of careful work uses it. The tell is the pairing at body size plus the absence of any
adjusted tone. **Instead:** near-black and off-white (e.g. `#0e0d12` / `#f6f4f1`); reduce chroma as
you approach the extremes.

### One-accent-does-everything with no strategy
A single saturated accent sprinkled at random density. **Instead:** decide how much of the page the
color owns before placing any of it. Four workable answers, from `pbakaus/impeccable`'s taxonomy:
one accent on a tenth of the surface at most; a committed 30-60% saturation carried across roles;
three or four hues each holding a distinct semantic job; or color as the ground itself, where the
page has no neutral to retreat to. Any of the four survives a review. Sprinkling does not.

### The cream/beige "tasteful default"
Warm cream or beige page background reached for by reflex — the current wave's replacement for the
purple gradient as the safe "tasteful" choice. **Instead:** a background that comes from a deliberate
palette and the product's scene, not the reflex warm off-white.

### Dark mode with glowing accents
Colored box-shadow glows on dark backgrounds; cyberpunk-by-default, plus the saturated radial halo
behind hero content. **Instead:** subtle purposeful lighting tied to real elevation, or skip the dark
theme entirely.

## Typography

### Inter/Geist everywhere, one weight
The default UI font at a single weight, hierarchy faked with size alone. Not wrong, but reaching for
it *without a reason* is the tell. **Instead:** choose type with intent; build hierarchy from
weight+size+leading as a set (aim for ≥1.25× scale steps), and cap body line length at 65–75ch.

### Gradient text across the whole headline
A gradient fill carrying an entire heading, or every heading on the page. One gradient word used as
an accent is a live and deliberate move (Apple, Dub, Vanta, 2026), so the single instance is not the
tell. Across a full line it costs contrast at the light stop and reads as decoration. **Instead:**
give a gradient one word or one mark, measure the contrast of its lightest stop, and earn the rest
of the emphasis with weight and size.

### Proportional numerals on dynamic values
Timers, counters, prices, and table columns set in default proportional figures jitter and reflow as
digits change width. **Instead:** `font-variant-numeric: tabular-nums` on any number that updates or
must align vertically.

### The icon tile above the heading
A small rounded-square icon container stacked above a feature-card heading — the universal AI
feature-card template; every generator outputs this exact shape. **Instead:** icon beside the
heading, icon in flow without its own container, or no icon.

### The hero eyebrow / repeated kickers
A tiny uppercase letter-spaced label or pill chip floating above an oversized hero headline, and the
same tracked micro-label repeated above every section ("FEATURES" / "PRICING"). Editorial scaffolding
by reflex. **Instead:** fold the kicker into the headline or drop it; let structure and imagery do
the sequencing.

### The italic serif display hero
Oversized italic serif (Instrument Serif and friends) as the hero headline — reads as taste in
isolation but has become the universal AI-startup hero of the current wave. Genuinely editorial
products get a pass; judge by context. **Instead:** set it roman, or choose a non-serif display face.

### The oversized full-sentence headline
A long sentence at display size dominating the viewport. A one-or-two-word headline at that size is
fine; the tell is length × size together. **Instead:** tighten the copy or shrink the type.

## Surface & depth

### Glassmorphism where nothing is layered
Frosted translucent panels on surfaces that float over nothing. This is the entry most likely to
misfire now: since iOS 26 the system material *is* glass, SwiftUI hands it to you by name, and
shipped iOS work is full of it by convention rather than by reflex (Revolut Business, Starling, HBO
Max, 2026). On Apple platforms, translucency that follows the system material is the correct default
and flagging it is a false positive. **Instead:** flag decorative blur on a static surface, or blur
over a solid ground with nothing scrolling beneath it, and leave platform-native materials alone.

### The uniform soft drop-shadow
The same `0 4px 12px rgba(0,0,0,.1)` on every element, so nothing has a real elevation story.
**Instead:** one shadow/elevation scale mapped to actual z-order; most elements sit flat.

### Side-stripe accent borders on plain cards
A 2–4px colored left border added to a content card to "add color." Severity coding on alerts,
callouts and docs admonitions is a semantic use and stays (Stripe's callouts, 2026). The tell is the
stripe on a card that carries no status, where the color means nothing. **Instead:** signal category
with a small icon, a label, or a tint, and keep the stripe for callout, alert and quote roles.

### Hairline border + wide soft shadow
A 1px border paired with a wide diffuse shadow on the same card — a generated-UI signature.
**Instead:** commit to one: a defined edge or a soft elevation, not both.

### Mismatched nested radii
An inner element's corner radius equal to or larger than its container's, or picked independently,
makes nested surfaces look subtly wrong even when nothing is nameably broken. The concentric rule:
outer radius = inner radius + padding between them. **Instead:** compute nested radii from the
parent, don't restate the same token at every level.

### The over-rounded blob
One large radius restated at every scale, so a 40px input, a card and a full-width section all wear
the same corner and the composition softens into a single blob. The 12–16px ceiling this entry used
to state was invented rather than sourced, and current work disproves it: consumer fintech routinely
ships 16 to 24px cards and reads as crisp (Monzo, Cleo, Zing, N26, 2026). **Instead:** let radius
scale with the element rather than repeating one token, and keep full-pill for tags and buttons.

## Motion

### Fade-up-on-scroll on everything
Every section rising 20px and fading in as it enters the viewport. Ubiquitous, and it delays content.
**Instead:** animate to communicate (state change, spatial origin), not to decorate arrival; respect
`prefers-reduced-motion`.

### 200ms-for-everything, with a bounce
One duration and an elastic overshoot applied uniformly. **Instead:** duration tracks distance and
importance; use exponential ease-out (quart/quint/expo); reserve overshoot for gestures that carried
momentum. Never animate layout properties (width/height/top/left) — animate transform/opacity.

### Decorative liveliness
The pulsing status dot on static data, the fake blinking cursor on non-editable hero copy, the
auto-scrolling logo marquee, imagery that scales on hover by default. Motion pretending something is
live or interactive when nothing is. **Instead:** animate only when the data changes or the gesture
demands a response; let people read at their own pace.

## Imagery

### Shape-assembled / hand-coded illustration
Hero art built from generic SVG shapes, or crude hand-coded mascots — reads as placeholder clip art,
not whimsy. **Instead:** real illustration, photography, or a purposeful graphic; if none is
available, ship no illustration.

## UI copy (shared border with `deslop`)

### Generic control labels
"Submit," "Click here," "Continue" on a control whose destination the label could have named.
"Get started" and "Learn more" are signup and detail conventions with a known destination, shipped
by almost everyone (Figma, Coda, Vercel, 2026); flagging those alone is a false positive. The tell is
a label that would sit unchanged on any button in any product. **Instead:** name the specific action,
"Start a pod," "Hear their answers." (This is the design edge of the same anti-slop doctrine `deslop`
applies to prose.)

### Empty/error states as afterthoughts
No empty, loading, or error state, or a generic "Something went wrong." **Instead:** design the
non-happy states with the same care as the happy path; errors say what happened and how to fix it.

### Redundant field writing
Label, sublabel, helper text, and placeholder all saying the same thing in slightly different words.
**Instead:** say it once, where it matters.

---

## Historical

Retired tropes, kept so the record survives and the next sweep does not re-harvest them from an
older catalog. Each carries the year it stopped earning a place and why. They stay useful when
reviewing a surface built in the era named.

### The purple→blue SaaS gradient *(active 2020–2024, retired 2026-08)*
Was: the single most-generated gradient on earth, on a hero or a CTA. Retired on visual evidence:
two Mobbin sweeps aimed straight at it turned up one instance across roughly sixty current sections,
and that one was a brand CTA. Purple survives as a brand color in the AI category, which the
category-reflex test already covers, but the purple-to-blue ramp as default decoration has gone.
Keeping it flags any indigo brand ramp, which several careful products ship.
**Note for maintainers:** `scripts/slop-scan.py` still has a `purple-blue-gradient` check, in its
`PLANTED` set and its `--demo`. Retiring this entry means that check now fires on work the catalog
no longer calls slop.

### Decorative grid-line backgrounds *(active 2023–2025, retired 2026-08)*
Was: a grid texture on a surface that isn't a canvas, map, or measurement task. The blueprint
background was a developer-tool reflex. Current instances are deliberate brand moves on 404s and
editorial pages (Mistral, Shopify Editions, Locomotive, Craft), which is exactly the well-executed
choice this rule would have flagged.

### Theater framing *(moved to `deslop` 2026-08)*
Was: "We killed the growth theater," dismissing things as performative as a copy reflex. Not retired
for going away, retired on the boundary rule in `maintenance.md`: the fix is entirely a change of
words, so it belongs to `deslop` and duplicating it here buys nothing.

---

## Distinctiveness quick-check

Run before calling a design done:

- Could you guess the palette/theme from the product's category alone? (category reflex)
- Every card the same size, padding, and shadow?
- Pure `#000` text on pure `#fff` at body size, with no tuned neutral anywhere?
- A gradient carrying a whole headline rather than one accent word?
- The same soft drop-shadow on everything?
- A colored left-stripe border on a card that carries no status?
- Does *everything* fade-up on scroll?
- One duration for all motion? Any layout-property animation?
- Any generic control label ("Submit," "Learn more")?
- An icon tile above every feature heading? An eyebrow chip or repeated section kickers?
- Cream/beige background, italic-serif hero, or dark-mode glow reached for by reflex?
- Numbers labeling a set that has no order?
- Hairline border + wide shadow on the same card? One radius restated at every scale?
- Any decorative liveliness (pulsing dot, fake cursor, marquee, hover-scale)?
- Nested radii concentric (outer = inner + padding)? Dynamic numbers tabular? Asymmetric icons optically centered?
- Would two different briefs, run through this system, produce visibly different designs — or just
  color-swaps of the same template?

## Scoring

When auditing, rate 1–10 on each dimension; treat below 35/50 as "reads as generated — rework."

| Dimension | Question |
|-----------|----------|
| Intentionality | Does every choice trace to the product/audience/mood, not a default? |
| Distinctiveness | Would you recognize this as *this* product, not a template? |
| Hierarchy | Does one thing clearly win, or is everything the same weight? |
| Restraint | Is anything decorative that isn't earning its place? |
| Coherence | Do color, type, space, and motion say the same thing? |

*Source note: synthesized from `pbakaus/impeccable` (Apache-2.0), `nutlope/hallmark` (MIT), and the
structure of our own `deslop` skill. Same doctrine as `deslop`, applied to pixels. Refreshed
2026-07 against Impeccable's 64-pattern slop catalog (impeccable.style/slop), adding the current-wave
tells: cream/beige default, italic serif hero, eyebrow chips, kickers, icon tiles, hairline+shadow,
over-rounding, decorative liveliness, imagery, redundant field writing, theater framing.*

*Retirement pass 2026-08-22, the first run against shipped product rather than other catalogs. Nine
Mobbin searches across marketing sites, consumer fintech, AI products and iOS apps, sampled across
categories so a category convention could be told apart from a reflex. Three entries retired below,
nine rewritten where the pattern held but the reasoning had rotted. Two classes of entry cannot be
settled this way and rest on reasoning instead: the motion entries, since Mobbin is still frames
rather than film, and the entries about what generators emit (shape-assembled illustration, empty
states as afterthoughts), since a library of shipped work has no unshipped slop in it to measure.*
