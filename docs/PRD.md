# Python Time-Travel Debugger

> This document specifies phase 1 of the program in [#26](https://github.com/jortega0033/python-time-travel-debugger/issues/26). Hour figures in it are early estimates for that phase; its open tickets add up to 42 to 64 hours (2026-11-24). Work that it defers is planned in the later phases only where the program names it.

Planning brief for inspiration project #48. Product status is from scratch. The milestones, fixtures, and benchmarks in this brief are planned. Estimates are engineering hours.

## Product requirements

A Python developer troubleshooting a surprising value needs to see how it changed across calls and loop iterations. The tool records one execution of an owned fixture, then lets the developer inspect earlier states without restarting the program. The main workflow is to select a recorded run, jump to its final event, step backwards, and identify the earlier line occurrence where a value became different.

The first milestone records the bundled `tally` fixture with CPython 3.12 and opens its trace in a local browser. The inspector shows sequence number, source location, active call stack and captured locals. Previous and Next navigate individual events. A later milestone adds reverse-continue, saved-run recovery, and indexed lookup. The episode is an immutable recording. Replay does not drive the interpreter or repeat effects from the recorded program.

| Requirement | Acceptance |
|---|---|
| Inspect a completed trace | A developer can select the bundled run, reach each occurrence of a loop line, and see its own state. |
| Retain semantics at boundaries | The UI labels line values as snapshots taken before execution. It distinguishes an unbound local, a captured None, and a value omitted by capture limits. |
| Search backwards | Filter by source location or find the previous observed change to a local in the selected frame. The current event is excluded from both searches. |
| Keep data local | Recorder and viewer use synthetic, owned fixtures. The application works on loopback with external browser requests blocked. |
| Recover safely | A finalized trace can be reopened after restart. An interrupted trace may expose a validated prefix with an incomplete badge. Corruption is reported with the event position. |

Out of scope for this epic are arbitrary uploaded script execution, process or thread attach, asynchronous and multi-threaded trace ordering, unrestricted expressions, native extension internals, and rewinding a live process. A Debug Adapter Protocol integration is a candidate for a later epic after the web workflow is stable.

## Technical design

**Runtime.** CPython 3.12, the Python standard library, and a local browser with plain HTML, CSS, and JavaScript modules. Start with an offline recorder command and a separate read-only web viewer. The recorder command accepts a bundled fixture ID and output directory. A fresh worker process runs a fixed fixture mapping with a deadline. Its exit code and termination reason are separate from the viewing service. There are no arbitrary script paths or shell commands in the browser API.

**Capture.** Define a versioned event envelope containing run ID, strictly increasing sequence, event kind, logical source ID, line number, frame instance ID, call depth, and frame snapshots. First supported events are call, line, return, and exception. Use CPython `sys.settrace` to receive the actual frame. On a call, allocate a monotonically increasing frame ID and associate it with its caller. A line event captures the current state before that line executes. On return, capture the departing frame before removing it from the active stack. An exception is evidence of an event in a particular frame. Later events determine whether execution continued. The final worker status records an unhandled failure. Repeated line numbers are ordinary, so the sequence number is the navigation key. [CPython 3.12 trace semantics](https://docs.python.org/3.12/library/sys.html#sys.settrace)

**Variable previews.** Serialize allowlisted exact built-in primitives and shallow built-in lists, tuples, and string-key dictionaries. Use explicit limits for nesting, string bytes, collection size, locals per frame, and stack depth. Record non-finite numbers and oversized integers with tagged previews. Label unsupported objects as opaque. Do not call arbitrary `repr`, descriptors, conversion dunder methods, or user-defined equality. Detect recursive containers and mark them truncated. Keep stdout and stderr out of the event stream. Render captured strings with text-safe DOM APIs.

**Trace storage.** Use a UTF-8 manifest and JSONL event file inside a run directory under an application-owned root. The manifest stores format version, fixture identifier, logical source names, source digests, limits, and final status. Stage the recording as a partial artifact. Flush successfully completed recordings and publish the manifest last with a same-filesystem atomic replacement. A completed manifest must match final event count and content digest. Recovery validates every complete event record and the monotonic sequence before exposing its prefix. An interrupted final line may be discarded only on an explicitly incomplete run. Reject malformed interior lines, overlong records, unknown major versions, sequence gaps, and manifest mismatches. Source digests and trace files use generated IDs and relative paths. Filesystem paths never come directly from browser requests.

**Lookup.** Begin with an in-memory byte-offset table. Persist a rebuildable index keyed by trace digest when adding restart support. Per-source and per-frame indexes store ordered event sequences. Binary search selects the previous matching sequence strictly before the cursor. Local-change queries compare adjacent observed snapshots for a selected frame and variable. Treat capture limits as unknown. Distinguish absent binding from a captured None and do not claim knowledge of assignments between recorded observations.

**Viewer contract.** A loopback GET-only service lists known run IDs, describes a chosen run and source manifest, returns a capped event page, and returns one event by sequence with its snapshots. Later endpoints add previous matching location or variable-change queries. The interface has a run picker, source and line display, ordered events, stack and locals, keyboard-accessible step buttons, and a stable selected event. An invalid sequence returns a visible error. At sequence 1, Previous is disabled. At the final event, Next is disabled. The browser keeps an explicit cursor after failed lookups.

**Optimization boundary.** CPython 3.12 `sys.monitoring` is an instrumentation API. Its LINE callback receives a code object and a line number. It does not expose a frame or locals through the documented callback signature. A parity experiment may compare event-only sampling and collector overhead. Keep `sys.settrace` as the default for local snapshots unless a verified adapter preserves the same visible results. Record interpreter version, sample count, methodology, and misses. [CPython 3.12 monitoring callbacks](https://docs.python.org/3.12/library/sys.monitoring.html#callback-function-arguments)

## Deterministic fixture and verification

Use an original five-line function named `tally`. Line 1 declares it, line 2 assigns total=0, line 3 starts a loop over the values 2 and 3, line 4 adds the current value to total, and line 5 returns total. Run the bundled fixture once per capture. Expected observations below are reasoned from the fixture and trace semantics. Record actual event sequences during implementation.

| Selected event in tally | Expected captured total | Expected n |
|---|---|---|
| First line 4 event | 0 | 2 |
| Second line 4 event | 2 | 3 |
| Line 5 event | 5 | 3 |
| Return event | 5, return value 5 | 3 |

Additional fixture cases should cover a handled exception, recursive calls with separate frame IDs, a value that transitions from missing to None, and a custom object whose `__repr__` fails if invoked. Unit tests verify capture and bounds. An independent reference assertion reads the normalized event file with a basic decoder and verifies the fixture sequence. Browser checks select and reopen a saved trace, reverse step through both visits to line 4, and repeat with external requests blocked.

Verify Python 3.12 and the availability of a local browser before the first build. The baseline needs no network installation. Browser automation can use the workspace's installed tools if available, plus a documented manual check. Record both the execution method and observed results. Large-trace performance targets require a measured baseline on the actual host.

## Epic E48 · Inspect earlier Python program states from a saved trace

**Outcome.** A developer can record a deterministic Python program, reopen the trace, and find the earlier point where a selected frame first exhibited an unexpected local value.

**Epic acceptance.**

- Starting from a clean checkout, record the bundled fixture and open it using the documented commands.
- Inspect both executions of line 4 and the final return. All fixture states match the table.
- Step and search backwards without executing the fixture or changing the trace.
- Reopen a completed run after restart and label an interrupted trace with its verified final complete event.
- Enforce capture and input limits. Record reproducible browser and index performance checks.

| Ticket | Work | Depends on | Estimate |
|---|---|---|---:|
| E48-1 | Recorder and trace event contract | — | 2–3 h |
| E48-2 | Durable artifacts, validation, and sequence index | E48-1 | 3–5 h |
| E48-3 | Browser source, stack, and timeline | E48-2 | 2–3 h |
| E48-4 | Indexed reverse searches | E48-2 | 3–4 h |
| E48-5 | Browser integration and restart acceptance | E48-3, E48-4 | 2–4 h |
| E48-6 | Bounded performance measurements and monitoring parity | E48-5 | 3–5 h |

**Remaining effort.** 15–24 engineering hours, including implementation, verification, and integration. E48-3 and E48-4 can proceed in parallel after the event API is fixed. Merge their smoke checks in E48-5. E48-6 depends on the integrated reference build.

### E48-1 · Recorder and trace event contract

- Add a fixture-only worker entry point and implement call, line, return, and exception events with a bounded safe serializer.
- Pin the five-line tally fixture and the reference expectations. Verify that recursion produces unique frame IDs and that collecting an opaque value never calls its `__repr__`.
- Exercise timeout, the record and size budgets, and a failed run. The CLI reports the reason and preserves its recorded prefix according to the format contract.

### E48-2 · Durable artifacts, validation, and sequence index

- Persist versioned manifests and event streams and build sequence-to-offset lookup. Support bounded pages of up to 200 events.
- Kill the worker after a known number of deliberately flushed synthetic records. On restart, verify that all complete contiguous events reopen and the manifest labels the run incomplete.
- Reject one corrupted interior record and unknown versions. Verify that selected event offsets and page boundaries match a linear parse. Ensure completed artifacts are read-only in the viewer.

### E48-3 · Browser source, stack, and timeline

- Serve a loopback viewer for finalized traces and show source context, call depth, and captured locals with accessible buttons.
- Start at the first event and step to the two visits to line 4. Verify displayed locals of `total=0, n=2` and `total=2, n=3`. Continue to the return and verify `total=5` plus the return preview.
- Verify keyboard stepping, boundary states, string rendering, and a clear description for unknown values.

### E48-4 · Indexed reverse searches

- Search backwards by source ID and line, or by the previous observed state change to a named local within a selected frame.
- From the return event, search for the previous visit to line 4. It must return the second visit with `total=2`. Repeating must return the first visit with `total=0`. A third search reports no earlier match and leaves the cursor intact.
- For a generated fixture that creates a local as None and then sets it to a number, compare search results to a simple backward scan. Never equate absent, None, and unknown previews.

### E48-5 · Browser integration and restart acceptance

- Join the source viewer and reverse queries into one keyboard-operable workflow. Display a stable incomplete indicator and recorded end sequence for partial runs.
- Run the tally workflow in a fresh browser context with external requests blocked. Restart the viewer and reopen the same trace. Verify both earlier loop values and a frozen artifact digest across the replay.
- Exercise malformed traces, unsupported versions, and missing selections. The viewer displays the appropriate error and keeps the previous valid run usable.

### E48-6 · Bounded performance measurements and monitoring parity

- Generate a 100,000-event synthetic trace within the documented cap and compare indexed lookups against an independent linear result for 1,000 seeded queries.
- Record cold open time, warmed reverse-query p95, peak RSS, interpreter, and fixture shape. Set performance gates from the repeatable baseline. Record regressions and do not infer unmeasured million-event throughput.
- Measure CPython `sys.monitoring` event-only capture against the reference recorder. Check explicit event differences. If the documented interface cannot supply equivalent snapshots, retain the existing collector and document the measured trade-off.

## Open decisions before implementation

Confirm the captured-value caps with the first real fixture, choose the on-disk index persistence threshold, and verify whether the hosted browser automation tools are available. Treat richer source mapping and adapter integration as independent later decisions.
