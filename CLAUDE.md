# CLAUDE.md

Working instructions for this repository. Read this file first, then the documents it links to. It does not repeat them.

## What this is

A planned offline Python time-travel debugger. A developer records one run of a bundled, deterministic fixture (`tally`) with CPython 3.12, then reopens the immutable trace in a loopback, read-only browser viewer, steps backwards and finds the earlier line where a local value changed, without running the program again.

**Status: nothing is implemented.** The repository holds the product plan, the technical specification and the backlog. No command below runs until ticket #2 (the walking skeleton) lands. Every command, path and module name in this file is planned and is marked as such; when a ticket makes one real, that ticket's pull request updates this file in the same change.

## Sources of truth

| Topic | Document |
|---|---|
| Product scope, fixture table, acceptance, tickets E48-1 to E48-6 | [docs/PRD.md](docs/PRD.md) |
| Technical contracts (capture, previews, storage, lookup, viewer), fixture and verification | [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) |
| Planned module map for implementers | [docs/architecture.md](docs/architecture.md) |
| Backlog, dependency order, estimates, owner decisions with their defaults | Epic issue #1 and its child issues on GitHub. The epic's table is authoritative. |
| Loop setup and its limits | [LOOP.md](LOOP.md), [loop-constraints.md](loop-constraints.md) |
| Project subagents, origin and local changes | [.claude/agency-agents/README.md](.claude/agency-agents/README.md) |
| Owner decisions (dated) | [docs/owner-decisions.md](docs/owner-decisions.md) |
| UI rules for the viewer | [docs/ui-quality.md](docs/ui-quality.md) |
| Releasing (owner only) | [docs/RELEASING.md](docs/RELEASING.md) |

The PRD and the technical specification repeat the same design text. If they differ, the technical specification wins for contracts and the PRD for scope. A ticket that changes a contract updates both in the same pull request.

## Stack and constraints

All of these come from the PRD and the technical specification, section "Technical design".

- CPython 3.12 and the Python standard library only. A local browser with plain HTML, CSS and JavaScript modules. The baseline needs no network installation: no pip or npm dependency, no build step, no CDN, font or script from another host.
- Two separate parts: an offline recorder command that runs a bundled fixture in a fresh worker process with a deadline, and a read-only web viewer. Their exit codes and failure reasons are separate.
- The viewer listens on loopback only and answers GET only. The application works with external browser requests blocked.
- The recorder accepts a bundled fixture ID and an output directory. There are no arbitrary script paths and no shell commands in the browser API. Filesystem paths never come from a browser request; runs and files use generated IDs and relative paths under an application-owned root.
- Replay never drives the interpreter and never repeats effects of the recorded program. Completed artifacts are read-only.
- Capture uses `sys.settrace`. `sys.monitoring` is an experiment only (ticket #7). Arbitrary `repr`, descriptors, conversion dunders and user-defined equality are never called on captured values.
- Captured strings reach the page through text-safe DOM APIs only (`textContent`, `createElement`), never `innerHTML` or `eval`.
- Platforms are not stated in the plan. Local development here runs on Windows 11 with Python 3.13.14 (3.12 is not installed on this machine); the CI matrix is set by the delivery workflow.
- Licence: not selected. Do not add a LICENSE file or licence headers without the owner.

## Commands (all planned)

Nothing below exists yet. Names are the proposal in [docs/architecture.md](docs/architecture.md); ticket #2 fixes them and corrects this table.

| Purpose | Command | Status |
|---|---|---|
| Run all tests | `python -m unittest` (from the repository root; `python3` on Linux) | planned: introduced by ticket #2 |
| Record the bundled fixture | `python -m ttdebug record tally --out ./traces` | planned: introduced by ticket #2 |
| Open the viewer on loopback | `python -m ttdebug serve --traces ./traces --port 8765` (`--port 0` picks a free port) | planned: introduced by ticket #2 |
| Recorder limits and deadline options | flags on `record` | planned: introduced by the recorder-contract ticket (see the epic) |
| Performance baseline and parity measurement | a documented script, named by ticket #7 | planned: introduced by ticket #7 |

`./traces` and any other trace directory is generated output and is never committed.

## Module boundaries (planned)

The map and the dependency direction are in [docs/architecture.md](docs/architecture.md). The rules:

- The recorder (worker, tracer, serializer, fixtures) writes events and never serves them.
- Only the trace package reads or writes trace files: envelope and versions, staging and atomic publish of the manifest, validation and recovery, the sequence index. Nothing else opens a trace path.
- The viewer service reads finalized or validated-prefix traces through the trace package and never imports the recorder or runs a fixture.
- The browser modules talk to the viewer through its GET endpoints only and keep an explicit cursor.
- Tests use temporary directories and port 0, with no fixed port and no network.

## Git workflow

- `main` is the default branch. One branch per ticket, named `<issue-number>-<short-slug>`. A pull request to `main` per ticket, naming the issue (`Part of #1`, `Closes #n`). Small commits with imperative subjects.
- Only the owner merges. Never push to `main`, never force-push, never merge your own pull request.
- Do not push or open a pull request unless the owner asked in the current session. Starting `/next-ticket` counts as that request for the one ticket it runs.
- Never commit trace directories, `.env*` or generated output.
- Do not change `.claude/agents/`, `LOOP.md`, `loop-constraints.md` or `loop-budget.md` as part of a feature ticket.

## Evidence before a ticket is called done

Record real output; never summarise a run you did not make. Items 1 to 5 are recorded locally before the draft pull request is opened and both gates judge them.

1. The tail of `python -m unittest` from a clean checkout, with the Python version and operating system, and the test count before and after.
2. For each acceptance criterion in the issue: the test that proves it, or the exact manual step and what was observed.
3. For a change to the trace format or the viewer contract: the updated section of `docs/TECHNICAL_SPEC.md` and a test that opens an artifact written by the previous format version or rejects it with the documented error.
4. For a change under the viewer's static files: a manual browser run with the browser name and version, keyboard-only use of the changed controls, and the console and network log free of errors and of external requests. The repository has no approved browser automation; if the ticket introduces one, it must need no network installation.
5. `git status` clean of stray files and confirmation that no dependency, external URL or non-loopback listener was added.
6. After the draft pull request is open: CI green on it (`gh pr checks`). The driver checks this before `gh pr ready`; the acceptance gate is not asked to confirm CI.
7. Anything not verified, said plainly.

Order for every ticket: local checks, Code Reviewer, Reality Checker, draft pull request, CI, then ready only when CI is green.

## Agent roles

Project subagents are in `.claude/agents/`: ten Agency Agents roles (Software Architect, Backend Architect, Frontend Developer, Test Automation Engineer, API Tester, Application Security Engineer, Accessibility Auditor, Performance Benchmarker, Code Reviewer, Reality Checker) and `loop-verifier`, which belongs to the Loop setup. Each Agency Agents role file starts with a section "In this repository", written for this project: the stack and hard rules that bind the role, the files it owns or reviews, its commands or the output it must be given, a checklist, what does not apply from the generic text, and what it hands back. That section and this file override the generic text below it. Sources, licence, local changes and the name collision with a user-level install are in [.claude/agency-agents/README.md](.claude/agency-agents/README.md).

When asked to implement, continue or finish a GitHub issue, follow the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand. Delegate to the roles without waiting to be asked: each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate. The playbook gives the trigger of each role.

- **Before coding:** Software Architect, when the ticket changes a module boundary, the trace format, the viewer contract or a dependency.
- **While coding:** Backend Architect for Python code, Frontend Developer for the viewer's static files, Test Automation Engineer for fixtures and tests.
- **After coding:** each specialist whose trigger matches (Application Security Engineer, Accessibility Auditor, API Tester, Performance Benchmarker).
- **On every ticket, before it is called done:** Code Reviewer, then Reality Checker. Read-only roles cannot run commands: give them the diff, the acceptance criteria and the recorded output.
- The session that wrote a change does not count as its reviewer. List each role that ran, what it was asked and its verdict in the pull request under "Agent roles run".

## Delivery workflow

- **Driver and playbook.** The owner starts a ticket with `/next-ticket` ([`.claude/skills/next-ticket/SKILL.md`](.claude/skills/next-ticket/SKILL.md)); it runs the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Starting it is the go signal; there is no scheduler. Agents take a ticket up to a ready pull request and never merge or release.
- **Review gate hook.** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py), wired in [`.claude/settings.json`](.claude/settings.json), blocks `gh pr create` and `gh pr ready` until Code Reviewer and Reality Checker have run after the last code edit; documentation-only changes pass. `ROLE_GATE=off` in the environment Claude Code is started from switches it off for that session.
- **Permissions.** `.claude/settings.json` allows the documented commands and git and gh read operations, asks before edits to CI, agent configuration, skills, hooks and Loop files, and denies force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env`.
- **CI.** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs the unit tests (once tests exist) and the gate self-test on Linux and Windows with Python 3.12 and 3.13. Every job must be green before a pull request is marked ready.
- **Pull request.** Use [`.github/pull_request_template.md`](.github/pull_request_template.md). Add a line to [`CHANGELOG.md`](CHANGELOG.md) under `Unreleased` in every ticket pull request.
- **Labels.** `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.
- **UI and copy.** UI tickets start with the `ui-ux-pro-max` skill and end with a check of the changed screens against [`docs/ui-quality.md`](docs/ui-quality.md). User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- **Decisions.** [`docs/owner-decisions.md`](docs/owner-decisions.md) records what the owner decided and where it is implemented. A decision that blocks a ticket stops the ticket.
- **Only the owner merges and releases.**
