# Releasing

Only the owner releases. Agents never tag, publish or create a release.

## What a release is here

There is no package, no installer and no deployment. A release is a Git tag on `main` plus a GitHub release whose notes come from `CHANGELOG.md`. Nothing exists to release until the epic (#1) is finished, and no licence has been chosen: pick one before the first public release.

## Steps

1. Confirm every ticket of the release is merged and CI is green on `main` (Linux and Windows, Python 3.12 and 3.13).
2. From a clean checkout of `main`, run `python -m unittest` and record the tail of the output.
3. Run the documented demo from the README once: `python -m ttdebug record tally --out ./traces`, then `python -m ttdebug serve --traces ./traces`, and step back in a browser. (Both commands are planned; ticket #2 makes them real.)
4. In `CHANGELOG.md`, rename `Unreleased` to the version and date, and add a fresh empty `Unreleased` section.
5. Merge that change through a pull request.
6. Tag the merge commit (`vX.Y.Z`) and create the GitHub release from the tag with the changelog section as notes.
