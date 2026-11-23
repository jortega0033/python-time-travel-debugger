# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## Status

Scaffold only: package skeleton and smoke tests. `record` and `serve` exit 1 with "not implemented yet: see #<ticket>" until tickets #10 and #11 land. See `CLAUDE.md` for which commands are real.

## Test command

```
python -m unittest
```

Run it from the repository root. CPython 3.12, standard library only. Do not add pip or npm dependencies. Lint: `python -m compileall -q ttdebug tests`.

## Ticket work

To implement a GitHub issue, follow [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md) and the agent roles section of [CLAUDE.md](CLAUDE.md). The role files in `.claude/agents/` each start with a section "In this repository" that holds the project rules for that role. An agent that cannot delegate to those roles does the before-coding, while-coding and specialist steps itself and says so in the pull request. The review gate and the acceptance gate still apply to every ticket, but the agent that wrote the change cannot pass them: do not push or open the pull request; report that the gates could not run and leave the run for the owner. Order: local checks, both gates, draft pull request, CI, then ready only on green CI.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no loop workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.
