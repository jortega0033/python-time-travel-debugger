# Security policy

## Reporting a vulnerability

Report it privately through GitHub: open the repository's Security tab and choose "Report a vulnerability". Do not open a public issue or pull request for a vulnerability.

Include the affected command or endpoint, the steps to reproduce it and the Python version and operating system you used.

## Supported versions

Only the default branch (`main`) is supported. The project has no tagged release yet.

## Scope worth reporting

The viewer is meant to listen on loopback only, answer GET only, take no filesystem path from a request and render captured values as text. A way around any of these, or a way to make the recorder run something other than a bundled fixture, is a vulnerability.
