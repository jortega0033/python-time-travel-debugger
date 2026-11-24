# Python Time-Travel Debugger

A planned offline project. The product is not implemented. The repository contains the product plan, technical specification, implementation backlog and a package scaffold (`ttdebug/`, `tests/`) with smoke tests only.

Commands that work now: `python -m unittest`, `python -m ttdebug --help`, `python -m ttdebug --version`. `record` and `serve` are parsed but not built (tickets #10 and #11).

## Program goal

Build a time-travel debugger that records a real Python program once, with threads, async code and native calls, and lets a developer run it backwards, ask why a value changed, and edit the past to test a fix.

The program is planned ([#26](https://github.com/jortega0033/python-time-travel-debugger/issues/26)). Phase 1 is the current epic [#1](https://github.com/jortega0033/python-time-travel-debugger/issues/1) and the only phase with tickets.

**Score.** Share of CPython's own test modules that record and replay to the same final state, with the recording overhead next to it.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 42 to 64 | [#1](https://github.com/jortega0033/python-time-travel-debugger/issues/1) |
| 2 | Real programs | 100 to 160 | [#27](https://github.com/jortega0033/python-time-travel-debugger/issues/27) |
| 3 | Deterministic replay | 150 to 250 | [#28](https://github.com/jortega0033/python-time-travel-debugger/issues/28) |
| 4 | Threads and async | 130 to 220 | [#29](https://github.com/jortega0033/python-time-travel-debugger/issues/29) |
| 5 | Why did this change | 110 to 180 | [#30](https://github.com/jortega0033/python-time-travel-debugger/issues/30) |
| 6 | What if | 110 to 190 | [#31](https://github.com/jortega0033/python-time-travel-debugger/issues/31) |

About 640 to 1060 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/python-time-travel-debugger/issues/1)

## Current status

The fixtures describe expected results for future checks. No working baseline or passing implementation tests are claimed. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.
