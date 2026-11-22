# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. The file `loop-verifier.md` in the same folder is not from Agency Agents; it belongs to the Loop Engineering setup described in [`LOOP.md`](../../LOOP.md).

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Reviewer roles have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands. Nothing else in any file was changed by the installation (later local changes are listed below).

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `testing-accessibility-auditor.md` | Accessibility Auditor | `testing/testing-accessibility-auditor.md` | `362935907af23839775b9c6162f38c0c5a740542ab4350cb5c5b5a0d9f9a4268` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `engineering-backend-architect.md` | Backend Architect | `engineering/engineering-backend-architect.md` | `ac717bde4848d7663fff8a3c7edc711fd119256de6a7ce38c036619372f42c99` | none |
| `engineering-frontend-developer.md` | Frontend Developer | `engineering/engineering-frontend-developer.md` | `1ae4cc10b2e0163bd3ed921ad54080b865cd02e591becd8919b64b73fab06dad` | none |
| `testing-api-tester.md` | API Tester | `testing/testing-api-tester.md` | `ab91de9188d48bd9c417282c33673a37b066215e90e08c0f1b270d036084e3bb` | none |
| `testing-test-automation-engineer.md` | Test Automation Engineer | `testing/testing-test-automation-engineer.md` | `4299d038e88387546d645ccbe767b1dfdb7de10da55eba1ab103149972cd2b9b` | none |
| `testing-performance-benchmarker.md` | Performance Benchmarker | `testing/testing-performance-benchmarker.md` | `16a841f67392d084b773c6d9f05341d093e9017f3e116f6df0de59a5a3f59c34` | none |

## Why these roles

The product is planned, not built: a standard-library Python recorder CLI, a durable trace format with indexes, and a read-only loopback web viewer in plain HTML, CSS and JavaScript ([`docs/PRD.md`](../../docs/PRD.md), [`docs/TECHNICAL_SPEC.md`](../../docs/TECHNICAL_SPEC.md)).

| Role | Use in this repository |
|---|---|
| Software Architect (read-only) | Check a ticket's design against the module boundaries in `CLAUDE.md` before code is written: recorder, trace storage, index, viewer service, browser modules. |
| Code Reviewer (read-only, gate) | Review every diff for correctness and broken rules (no arbitrary `repr`, no filesystem path from a request, GET-only viewer, stdlib only). |
| Application Security Engineer (read-only) | Review where untrusted data meets code: captured values, trace files read back from disk, request parameters, text rendered in the page. |
| Accessibility Auditor (read-only) | Review keyboard operation, focus, boundary states and unknown-value text in the viewer. |
| Reality Checker (read-only, gate) | Compare claimed evidence with what was actually run before a ticket is called done. |
| Backend Architect | Implement the Python side: recorder, serializer, storage, index, HTTP service. |
| Frontend Developer | Implement the browser modules served by the viewer. |
| API Tester | Write HTTP-level tests for the viewer endpoints and their error paths. |
| Test Automation Engineer | Build the fixture-driven test harness and the browser check for blocked external requests. |
| Performance Benchmarker | Produce the repeatable baseline in the performance ticket. |

Most of these roles are written for larger stacks and mention frameworks, cloud services and paid tools. In this repository `CLAUDE.md` wins: Python standard library only, no network installation, loopback only.

Roles that were considered and left out: Codebase Onboarding Engineer (no code yet to trace), Database Optimizer and Database Reliability Engineer (no SQL; durability is plain files, covered by Backend Architect and Software Architect), UI Designer and UX Architect (one small tool screen, covered by Frontend Developer and Accessibility Auditor).

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Updating

Fetch the new revision with the command above, compare each file with the table, re-apply the local changes, and update the revision and hashes in this file in the same commit.

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. Nothing else in the role files changed.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, remove that sentence (and the `tools:` line where one was added) first.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

## Local change: project section "In this repository" (2026-11-22)

A section titled "In this repository" was inserted directly after the frontmatter of every Agency Agents role in `.claude/agents/` (not `loop-verifier`). It is project-specific text written for this repository, not upstream text: it describes the planned stack, modules and commands from `docs/TECHNICAL_SPEC.md` and marks them as planned because no code exists yet. To compare a role with the pinned upstream file, remove that section as well as the "Use proactively" sentence (and the `tools:` line where one was added).

## Delivery workflow installed (2026-11-22)

Installed directly, not ticketed: the review gate hook (`.claude/hooks/role_gate.py`, gate roles Code Reviewer and Reality Checker, both present in `.claude/agents/`), `.claude/settings.json`, the `next-ticket` driver, CI, pull request and issue templates, `docs/ui-quality.md`, `docs/owner-decisions.md`, and two skills copied unchanged from the owner's installed copies (`.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/`, each with its own `PROVENANCE.md`).

Local change to three roles: the "In this repository" checklists of Code Reviewer, Frontend Developer and Accessibility Auditor now name `docs/ui-quality.md`. UI Designer and UX Architect are not installed here (one small tool screen), so they have no checklist to extend.

Checks run once on 2026-11-22 (Windows 11, Python 3.13.14):

- `python .claude/hooks/role_gate.py --self-test`: passed (gate roles: Code Reviewer, Reality Checker).
- `.claude/settings.json` parsed as JSON: ok. `ci.yml` and `dependabot.yml` parsed as YAML: ok.
- `python .claude/skills/ui-ux-pro-max/scripts/search.py "developer tool trace viewer" --design-system -p "Time travel debugger"`: printed a design system.
- `python .claude/skills/unslop/scripts/banned_phrase_scan.py <sample>`: reported 2 violations in the sample text.

Loading check (superseded below for `loop-verifier`: it now has `tools: Read, Grep, Glob`), run once from this worktree with `claude -p "List every project subagent ..." --model haiku` (Claude Code 2.1.323). It listed 11 project subagents: Application Security Engineer, Accessibility Auditor, Code Reviewer, Reality Checker and Software Architect with tools `Read, Grep, Glob`; Backend Architect, Frontend Developer, API Tester, Performance Benchmarker, Test Automation Engineer and loop-verifier with no `tools:` line. Ten start with "In this repository"; `loop-verifier` does not (it belongs to the Loop setup). It listed 8 project skills: implement-ticket, next-ticket, issue-triage, loop-budget, loop-constraints, loop-intake, ui-ux-pro-max, unslop. The run printed a warning that the workspace was not trusted and ignored the 23 `permissions.allow` entries from `.claude/settings.json`; trust is granted once interactively.

## Local change: loop-verifier tools and Reality Checker CI check (2026-11-22, review round 1)

`loop-verifier.md` (not an Agency Agents file) gained `tools: Read, Grep, Glob`; before this it had no `tools:` line and held full tool access. Its rules now tell it to answer ESCALATE_HUMAN when a verdict depends on a test run. A repeat loading check (same command as above, Claude Code, one run) lists `loop-verifier` with `Read, Grep, Glob`; the other results are unchanged. The Reality Checker "In this repository" section gained one sentence on checking, from the diff, that CI runs the documented checks.
