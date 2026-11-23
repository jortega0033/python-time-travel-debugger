# UI quality rules

These rules are binding for the viewer's page under `ttdebug/viewer/static/` and for every user-facing string. The owner set rules 1 and 2; rules 3 to 10 were approved on 2026-11-22 and have the same standing. They keep the interface from showing the usual marks of generated UI.

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. The screen opens on the user's task (the run picker and the current event).
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form (the locals and the event list are tables or lists).
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

Colours, spacing, radius and motion come from the design tokens in [design-tokens.md](design-tokens.md); new UI uses them and adds no colour literals.

## How the rules are applied

- A UI ticket starts with the `ui-ux-pro-max` skill (design-system search for the product type) and ends with a check of every changed screen against this file. The page still uses plain HTML, CSS and JavaScript only; the skill gives guidance, not dependencies.
- User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- Code Reviewer, Frontend Developer and Accessibility Auditor name this file in their checklists. Enforcement is by the review gate, not by a script. Rule 1 can be linted; rule 2 cannot be detected reliably from CSS.
- These rules sit beside the accessibility requirements in `docs/TECHNICAL_SPEC.md` ("Viewer contract"): unknown values are told apart by text, not by colour alone.
- Rule 8 is read with the "Accent rules" section of [design-tokens.md](design-tokens.md) and owner decision 14 in [owner-decisions.md](owner-decisions.md): the accent also marks the current step, and `--focus` is a focus indicator, exempt from the accent limit.
