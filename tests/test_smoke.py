"""Scaffold smoke tests: every module imports and the entry point answers. No product behaviour."""

import importlib
import subprocess
import sys
import unittest

MODULES = [
    "ttdebug",
    "ttdebug.cli",
    "ttdebug.fixtures",
    "ttdebug.recorder",
    "ttdebug.trace",
    "ttdebug.viewer",
]


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "ttdebug", *args], capture_output=True, text=True, timeout=30)


class ModuleImports(unittest.TestCase):
    def test_modules_import_and_state_their_responsibility(self):
        for name in MODULES:
            with self.subTest(module=name):
                self.assertTrue(importlib.import_module(name).__doc__)


class EntryPoint(unittest.TestCase):
    def test_help(self):
        result = run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("record", result.stdout)
        self.assertIn("serve", result.stdout)

    def test_version(self):
        result = run("--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn("ttdebug", result.stdout)

    def test_unbuilt_commands_exit_non_zero_with_ticket(self):
        for args, ticket in ((("record", "tally", "--out", "x"), "#10"), (("serve", "--traces", "x"), "#11")):
            with self.subTest(command=args[0]):
                result = run(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("not implemented yet: see " + ticket, result.stderr)


if __name__ == "__main__":
    unittest.main()
