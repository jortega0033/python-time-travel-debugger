# Python Time-Travel Debugger: technical specification

Planning document. Implementation and verification remain future work.

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
