# Design tokens

The viewer uses the Pipenzo "Flow look" tokens: a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`) and red only for danger.

## Source and resync

- Source: `jortega0033/clip-to-reel-studio`, `extension/sidepanel/tokens.css`, commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21).
- Installed at `ttdebug/viewer/static/tokens.css`, byte for byte. Never edit the copy.
- To resync: copy the file over it. Nothing else changes.

## Rule

New UI uses these tokens. No new colour literals (`#hex`, `rgb()`, `hsl()`) in the page's CSS or JavaScript. Link `tokens.css` before any other stylesheet. Script that needs a colour (for example on a canvas) reads it with `getComputedStyle(document.documentElement).getPropertyValue('--token')`.

The file header holds the accent rules: yellow only on the primary action and the current-step marker; text never sits on a bare alpha layer.

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
