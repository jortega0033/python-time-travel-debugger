---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Started only by the owner; starting it is the go signal.
disable-model-invocation: true
argument-hint: "[issue number]"
---

# Next ticket

Run one ticket of epic #1 (Python Time-Travel Debugger) from the queue to a ready pull request. The owner starts this with `/next-ticket` or `/next-ticket <issue number>`. That is the go signal: nothing here starts by itself, and there is no scheduler.

One ticket per run. Never merge. Never start another run.

## Steps

1. **Refresh the queue.** `gh issue list --label status:blocked --state open` and read epic #1. A `status:blocked` ticket whose blockers are all closed becomes `status:ready` (`gh issue edit <n> --add-label status:ready --remove-label status:blocked`). Also check parents: a parent whose sub-issues are all closed is closed with a comment.
2. **Pick the ticket.** Only a leaf ticket is work. A ticket labelled `tracking`, or with open sub-issues, is a container and is never picked; the epic itself is one. With an argument, use that issue (stop and say so if it is closed, `status:in-progress`, `needs-decision` or still blocked); if it is a `tracking` parent, refuse and list its open sub-issues. Without one, take the first `status:ready` leaf ticket in the epic's order (the order of the parents in the epic's table, then the order of the sub-issues inside each parent) that is neither `status:in-progress` nor `needs-decision`. If none qualifies, report the queue and stop.
3. **Claim it.** Add the label `status:in-progress` and remove `status:ready`.
4. **Branch in a fresh worktree.** `git fetch origin`, then `git worktree add ../python-time-travel-debugger-<issue-number> -b <issue-number>-<short-slug> origin/main`. Work only there.
5. **Run the playbook** [`.claude/skills/implement-ticket/SKILL.md`](../implement-ticket/SKILL.md) for that issue, with the rules in `CLAUDE.md`. Order: local checks, Code Reviewer, Reality Checker, `gh pr create --draft`, CI, then ready. Record the local evidence before the gates run, and write the reviewer diff files first (see the playbook).
6. **Wait for CI without polling.** After `gh pr create --draft` and `git push`, bind the pull request to the session when the app offers it (the desktop app's pull request tools) and end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When the session is woken (a CI event from the app, or the owner says "continue"), read `gh pr checks <n>` once: green, go to step 7; red, fix, re-run the local checks and both gates, push; still running, end the turn again with the same line. Do not mark the pull request ready while CI is red.
7. **Ready.** When CI is green on the draft: `gh pr ready <number>` (the gate hook checks again), then comment on the issue with the pull request link and the CI run link. Leave the `status:in-progress` label in place; the owner merges and closes. If the ticket is the last open sub-issue of a parent, the pull request body says `Closes #<sub-issue>` and `Closes #<parent>`, so the owner's merge closes both.
8. **Stop.** Report the pull request, the evidence, the roles that ran and anything not verified.

## Stop and say so when

- The ticket names an owner decision with no stated default (`needs-decision`).
- A decision in `docs/owner-decisions.md` blocks the ticket.
- The ticket would need a dependency, an external request, a non-loopback listener, or a change to the trace format that the ticket does not authorise.

Labels used: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.
