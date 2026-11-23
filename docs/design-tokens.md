# Design tokens

The viewer uses the Pipenzo "Flow look" tokens: a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`) and red only for danger.

## Source and resync

- Source: `jortega0033/clip-to-reel-studio`, `extension/sidepanel/tokens.css`, commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21).
- Installed at `ttdebug/viewer/static/tokens.css`, byte for byte. Never edit the copy.
- To resync: copy the file over it. Nothing else changes.

## Rule

New UI uses these tokens. No new colour literals (`#hex`, `rgb()`, `hsl()`) in the page's CSS or JavaScript. Link `tokens.css` before any other stylesheet. A ticket that creates a page or its static allowlist links `tokens.css` first and serves it (the allowlist and its test). (Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23.) Script that needs a colour (for example on a canvas) reads it with `getComputedStyle(document.documentElement).getPropertyValue('--token')`.

## Accent rules

These rules take precedence over the header comment of `tokens.css`. That header is narrower: it lists yellow only for the primary button, the current-step node, the "your turn" chip and two dots. It cannot be edited here, because the copy must stay identical to the source. Where the two differ, this document decides. Text never sits on a bare alpha layer.

- **Current selection (decided by the owner on 2026-11-23, UI rule 8).** Yellow is used for the primary action, the current-step marker and the current selection. How it is applied was recommended by the orchestrator and adopted under the owner's delegation of the same day: a selection uses a solid `--primary` fill with `--on-primary` text, not only a yellow border (a yellow border is about 1.5:1 against white on light). It also carries a second sign that is not colour (weight, icon or text) and the existing aria attribute (for example `aria-selected` or `aria-current`). Never a tint with a border of the same hue, and never a thick border on one side.
- **Focus ring.** `--focus` is a focus indicator and is exempt from the accent limit, including where it is yellow in the dark block. A ticket that says the focus style stays unchanged means the rule on `main` after the token pull request. (Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23.)
- **Themes.** Contrast checks and the "no colour alone" checks cover both the light block and the dark block of `tokens.css`. (Same source as the focus ring.)
- **Page status.** Where the page still marks a selection in a neutral colour, it does not follow this rule yet. The page follows in ticket work; this document does not claim it is done.

## Light and dark

Dark is the primary design. The default `:root` block is the matching light theme. The dark block sits inside `@media (prefers-color-scheme: dark)`, so the operating system colour scheme decides; there is no toggle. `color-scheme: light dark` is set.

## Token names by role

- Surfaces: `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`
- Text: `--fg`, `--muted`, `--faint`
- Lines: `--border`, `--control-border`, `--hairline`, `--input-border`, `--focus`
- Hero: `--hero-bg`, `--on-hero`, `--on-hero-muted`, `--hero-chip-border`, `--hero-border`, `--hero-shadow`
- Dark block: `--ink`, `--on-ink`, `--on-ink-muted`, `--ink-border`, `--ink-hover`
- Accent: `--primary`, `--primary-press`, `--primary-edge`, `--on-primary`
- Status: `--success`, `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--info`
- Alpha layers: `--glass`, `--glass-strong`, `--glass-border`, `--glass-highlight`, `--glass-video`, `--glass-video-border`, `--scrim`, `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`, `--ring-accent`, `--on-media`
- Shadows and gradients: `--shadow-1`, `--shadow-2`, `--shadow-3`, `--shadow-float`, `--shadow-on-video`, `--shadow-on-video-lg`, `--blur`, `--grad-canvas`, `--grad-scrim-bottom`, `--grad-ink`
- Type: `--font`, `--font-display`, `--mono` (system fonts only; the page loads no font files)
- Space and radius: `--space-1` to `--space-7`, `--radius-control`, `--radius-card`, `--radius-media`, `--radius-hero`, `--radius-chip`, `--radius-pill`
- Motion: `--dur-1` to `--dur-4`, `--ease-out`, `--ease-in-out`

The `docs/ui-quality.md` rules still apply: the glass, blur and gradient tokens exist in the file, but rules 3 and 4 forbid using them as default decoration.
