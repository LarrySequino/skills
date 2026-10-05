# UI copy

Rules for labels, buttons, empty states, settings, error messages, and the short strings a product shows a person. They sit beside the prose rules in `SKILL.md`, which still apply; these cover what those rules do not, which is comprehension rather than voice. Every rule here was harvested on 2026-09-02 from the sources named at the bottom, written fresh, and is a candidate until an eval separates the arms.

## The cold read

Cover the code and judge the screen from what it shows, top to bottom as a visitor would meet it. Four questions per screen: what is this for; what happens to my data or my account when I use each control; how would I choose between the options; what comes next once I act. Any question only the source could answer is a finding. Two guards: never audit from memory of code you just read, since once you know what a handler writes you cannot un-know it; and confirm a behavior before describing it, never invent one to fill a gap. For a set of options, a person is silently asking what each one changes, what it costs, which is the default, whether it can be undone, and which most people pick; the reversibility question is the one most often left unanswered, and its absence is what makes people hesitate.

## The intervention ladder

When a screen is unclear, take the highest rung that solves it, because every lower rung costs the reader attention on every visit: rename the control, which adds no words; label it with what happens; one line beside it, under twelve words; a short block for empty and first-run states; a tooltip, which touch users never see and which only helps someone already suspicious; a link to documentation, which admits the product could not explain itself. A fix on either of the last two rungs earns one question: could the first two have done it? Budget: about three new strings per screen, and a string seen often must be quieter than one seen once. A pass that adds forty strings has misread the problem.

## Six rules for the strings themselves

- A label names what a thing is or does, never where it lives or how to reach it. A button reads "Change plan," not "open the settings menu at the top and choose Change plan." The exemption is text whose whole job is to instruct: documentation, a first-run hint, a guided tour.
- A setting describes its on state. "Send read receipts," not "Don't send read receipts," which turns the toggle into a double negative.
- One flow vocabulary. "Continue" or "Next," pick one and keep it; one capitalization policy per element type.
- A link says where it goes. "Learn more" gets a suffix naming the destination.
- Never concatenate fragments around a variable; the sentence does not survive translation.
- Figures, claims, and commitments are off limits to a copy pass; changing one is a decision, and it goes back to whoever made it.

## Error messages, three checks a reader can verify in code

- One generic message catching causes the code can tell apart is a defect; if the catch block knows whether it was network, validation, or permission, the message says which. Generics are for failures the code cannot distinguish.
- A message rendered in a toast or an `aria-live` region reaches the user with none of the surrounding screen; a lone "Required" read aloud by a screen reader names nothing.
- A rewrite that removes or renames an interpolated variable changes behavior, not wording; report it as a code change and leave the string alone.

## Procedures

- Never "simply," "easy," or "quickly" in a step; if it were, the step would not be there.
- Put "only" and "not" immediately before the word they modify; anywhere else, they modify something else.
- No plurals with "(s)"; write the plural or restructure.
- No slashes; write "a, b, or both."

## Sources

Jakub Krehel, `better-writing` (jakubkrehel/skills, MIT): the on-state, flow-vocabulary, capitalization, link, and concatenation rules. Josh Pigford, `clarity-audit`, `polish`, and `error-message-audit` (license pending; ideas only until confirmed): the cold read, the ladder and budget, the self-narrating label rule, the three error checks, and the number-claim-promise rule. Lauren Tan, `technical-writing` (pstack, cursor/plugins, MIT): the four procedure rules. Each was scanned for shared phrasing with `tools/overlap.py` on 2026-09-02 before this file was written.
