# Implementer map (planned)

Status: planned, not implemented. This page adds only what the technical specification leaves open for someone writing the first code: where things live and which way dependencies point. Contracts (event envelope, previews, storage, lookup, viewer) stay in [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) and are not repeated here. Ticket #2 creates the layout and corrects this page where it differs.

## Proposed layout

```
ttdebug/
  __main__.py, cli.py     command line: record, serve
  fixtures/               bundled fixtures (tally first); fixture ID -> code is a fixed mapping
  recorder/               worker process entry, settrace tracer, serializer, capture limits
  trace/                  envelope and format version, storage (staging, manifest publish),
                          validation and recovery, sequence and per-source/per-frame indexes
  viewer/                 GET-only loopback service and endpoint handlers
  viewer/static/          plain HTML, CSS and JavaScript modules
tests/                    unittest; fixture tests, storage and recovery tests, HTTP tests
```

The package name `ttdebug` is a proposal; the spec names no layout.

## Dependency direction

`cli` -> `recorder` and `viewer`. `recorder` -> `trace` (writes). `viewer` -> `trace` (reads). `trace` imports neither. `recorder` and `viewer` never import each other: the viewer cannot run a fixture, which is what keeps replay free of effects.

## One workflow, end to end

1. `record tally --out DIR`: the CLI starts a fresh worker process with a deadline. The worker runs the fixed `tally` mapping under `sys.settrace`, the serializer turns each frame snapshot into bounded previews, and the trace package stages the events and publishes the manifest last.
2. `serve --traces DIR`: the viewer lists runs from the root it was given, loads a run through the trace package, and answers GET requests for the run description, an event page (at most 200 events) and one event by sequence.
3. The browser holds an explicit cursor (a sequence number), asks for the event at that cursor and renders it with text-safe DOM calls. Previous and Next change the cursor; a failed lookup leaves it where it was.

## What each ticket fills in

| Area | First real code | Completed by |
|---|---|---|
| Recorder, tally, minimal serializer, finalized trace, viewer page with Previous and Next | #2 | the recorder-contract ticket (exception events, full previews, limits, timeout), #3 (durability and recovery) |
| Viewer page: source, stack, locals, run picker, boundary states | #2 (minimal) | #4 |
| Indexed reverse searches | #5 | #6 (persisted index), #7 (scale) |
