# Owner decisions

A dated record of the decisions the owner made for this repository. Each entry says what was decided, when, and where it is implemented. Changing any entry needs the owner. An agent that finds a decision blocking a ticket stops and says so.

All entries date from 2026-11-22.

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

Entry 11 (Rust verified in CI only) does not apply: this repository has no Rust.

## Entry 10: decisions settled with the ticket default

| Ref | Decision | Default taken | Ticket |
|---|---|---|---|
| D1 | Supported Python | Require 3.12 or newer, refuse older with a message; CI runs 3.12 and 3.13; if the tally sequence differs between them, assert per-version expectations and report it | #2 |
| D2 | Package and command name | `ttdebug`, run as `python -m ttdebug` | #2 |
| D3 | Capture caps | nesting 3, string 256 bytes, 20 collection items, 32 locals, stack depth 50, 200,000 events, 64 MiB trace, 1 MiB record, 10 s deadline; confirmed or adjusted with the first real fixture and written into the spec; budgets and deadline are overridden only by the `record` flags `--deadline`, `--max-events`, `--max-trace-bytes` | recorder-contract ticket |
| D4 | Fixture stdout and stderr | Discarded, never stored | recorder-contract ticket |
| D5 | Exit codes | Recorder: 0 complete, 1 failed or truncated, 2 usage, 3 deadline. Viewer (`serve`): 0 normal stop, 1 cannot start (port in use, missing directory), 2 usage; kept separate from the recorder's | #2, recorder-contract ticket |
| D6 | Browser verification | Manual with recorded evidence; no browser automation and no new dependency; hosted browser tools not assumed | #2, #4, #6 |
| D7 | Meaning of "previous change" | Latest earlier event in the frame whose observed state differs; also report the first later observation; unknown never equal | #5 |
| D8 | Page size above 200 | Clamp to 200 and say so | #3 |
| D9 | Persisted index threshold | Runs of 10,000 events or more | #6 |
| D10 | Performance gates | Twice the median of five runs; enforced only with `TTDEBUG_PERF_GATES=1` | #7 |
| D11 | Licence | Stay unlicensed; no file added | none |
| D12 | Source text in the trace | Each run directory holds a copy of the fixture source with its digest, so a trace is self-contained | #2 |

The recorder-contract ticket's number is assigned when it is created; the orchestrator fills it in on GitHub.
