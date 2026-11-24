# Owner decisions

A dated record of the decisions the owner made for this repository. Each entry says what was decided, when, and where it is implemented. Changing any entry needs the owner. An agent that finds a decision blocking a ticket stops and says so.

All entries date from 2026-11-22, except entries 13 and 14 (2026-11-23).

| # | Decision | Implemented in |
|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | `CLAUDE.md`, `.claude/`, `.github/` on `main` |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | `.claude/agents/` ("In this repository" sections, "Use proactively" descriptions), `.claude/skills/implement-ticket/SKILL.md` |
| 3 | Every open ticket is about app implementation. Tooling is installed, not ticketed. | Epic #1 and its child tickets; `.claude/`, `.github/` |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | `CLAUDE.md` ("Git workflow", "Delivery workflow"), `.claude/skills/next-ticket/SKILL.md`, deny rules in `.claude/settings.json`, `docs/RELEASING.md` |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. | `.claude/skills/next-ticket/SKILL.md` (`disable-model-invocation: true`), `LOOP.md` |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles have run after the last code edit. | `.claude/hooks/role_gate.py`, `.claude/settings.json` |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | `LOOP.md`, `loop-constraints.md`, `loop-budget.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | `.github/workflows/ci.yml`; branch protection is set on GitHub by the orchestrator after merge |
| 9 | Documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | `.claude/settings.json` |
| 10 | Open decisions on tickets are settled with the ticket's stated default (list below). | The tickets named below |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed and used for UI work and for copy. | `docs/ui-quality.md`, `.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/` |
| 13 | 2026-11-23. Visual system: Pipenzo Flow look tokens (docs/design-tokens.md). SDLC kit version: jortega0033/sdlc-kit v1.0.0. | `docs/design-tokens.md`, `ttdebug/viewer/static/tokens.css` |
| 14 | 2026-11-23. Accent rules. 14-D1 Current selection: the yellow accent is used for the primary action, the current-step marker and the current selection (UI rule 8). Decided by the owner on 2026-11-23. How (recommended by the orchestrator, adopted under the owner's delegation of the same day): a selection uses a solid `--primary` fill with `--on-primary` text, plus a second sign that is not colour and the existing aria attribute; never a tint with a same-hue border, never a thick one-sided border. 14-D2 Focus ring: `--focus` is a focus indicator, exempt from the accent limit, including where it is yellow in dark. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. 14-D3 Themes: contrast and no-colour-alone checks cover both the light and the dark block of `tokens.css`. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. 14-D4 Linking: a ticket that creates a page or its static allowlist links `tokens.css` before any other stylesheet and serves it (allowlist and its test). Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. The labels 14-D1 to 14-D4 are separate from the Refs D1 to D12 in the Entry 10 table. | `docs/design-tokens.md` ("Rule" and "Accent rules"); the page follows in ticket work |

Entry 11 (Rust verified in CI only) does not apply: this repository has no Rust.

## Entry 10: decisions settled with the ticket default

| Ref | Decision | Default taken | Ticket |
|---|---|---|---|
| D1 | Supported Python | Require 3.12 or newer, refuse older with a message; CI runs 3.12 and 3.13; if the tally sequence differs between them, assert per-version expectations and report it | #2 |
| D2 | Package and command name | `ttdebug`, run as `python -m ttdebug` | #2 |
| D3 | Capture caps | nesting 3, string 256 bytes, 20 collection items, 32 locals, stack depth 50, 200,000 events, 64 MiB trace, 1 MiB record, 10 s deadline; confirmed or adjusted with the first real fixture and written into the spec; budgets and deadline are overridden only by the `record` flags `--deadline`, `--max-events`, `--max-trace-bytes` | #8 (recorder contract) |
| D4 | Fixture stdout and stderr | Discarded, never stored | #8 (recorder contract) |
| D5 | Exit codes | Recorder: 0 complete, 1 failed or truncated, 2 usage, 3 deadline. Viewer (`serve`): 0 normal stop, 1 cannot start (port in use, missing directory), 2 usage; kept separate from the recorder's | #2, #8 (recorder contract) |
| D6 | Browser verification | Manual with recorded evidence; no browser automation and no new dependency; hosted browser tools not assumed | #2, #4, #6 |
| D7 | Meaning of "previous change" | Latest earlier event in the frame whose observed state differs; also report the first later observation; unknown never equal | #5 |
| D8 | Page size above 200 | Clamp to 200 and say so | #3 |
| D9 | Persisted index threshold | Runs of 10,000 events or more | #6 |
| D10 | Performance gates | Twice the median of five runs; enforced only with `TTDEBUG_PERF_GATES=1` | #7 |
| D11 | Licence | Stay unlicensed; no file added | none |
| D12 | Source text in the trace | Each run directory holds a copy of the fixture source with its digest, so a trace is self-contained | #2 |

The recorder-contract ticket is #8.

## Program decisions (owner, 2026-11-24)

The owner accepted the goal and each suggestion below. They apply from the phase they name; the rules of `CLAUDE.md` hold for phase 1 as written.

| Decision | Implemented in |
|---|---|
| The repository has a program goal above phase 1: time-travel debugging for real Python programs, in six phases. | Program issue #26 |
| Running arbitrary local scripts ends the owned-fixtures rule. Suggested: allow it behind an explicit flag, in a separate process with limits. | Program issue #26 |
| Several CPython versions. Suggested: 3.12 first, then 3.13 and 3.14 as a matrix. | Program issue #26 |
