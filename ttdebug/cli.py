"""Command line: record a bundled fixture and serve recorded runs (cli -> recorder and viewer)."""

from __future__ import annotations

import argparse
import sys

from ttdebug import __version__

MIN_PYTHON = (3, 12)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m ttdebug",
        description="Record a bundled fixture, then step back through the trace in a loopback browser viewer.",
    )
    parser.add_argument("--version", action="version", version=f"ttdebug {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record", help="record a bundled fixture into a run directory")
    record.add_argument("fixture", help="bundled fixture ID (tally)")
    record.add_argument("--out", required=True, help="output root directory")
    serve = sub.add_parser("serve", help="serve recorded runs on 127.0.0.1, read-only")
    serve.add_argument("--traces", required=True, help="directory holding recorded runs")
    serve.add_argument("--port", type=int, default=8765, help="port (0 picks a free port)")
    return parser


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        print("ttdebug needs Python 3.12 or newer", file=sys.stderr)
        return 2
    args = build_parser().parse_args(argv)
    ticket = {"record": 10, "serve": 11}[args.command]
    print(f"not implemented yet: see #{ticket}", file=sys.stderr)
    return 1
